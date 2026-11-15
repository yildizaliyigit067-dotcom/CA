"""Build all report figures and summary tables from the CSV files in results/.

Usage:  python analysis/make_figures.py
No simulation results are generated here except the small illustrative
snapshots in Figure 1, which use fixed seeds.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ca_engine as E  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"
FIG = ROOT / "figures"
TAB = RES / "tables"
FIG.mkdir(exist_ok=True)
TAB.mkdir(exist_ok=True)

# Validated categorical order (dataviz reference palette, slots 1-3).
COL = {"independent": "#2a78d6", "clustered": "#eb6834", "global_fluct": "#1baf7a"}
MRK = {"independent": "o", "clustered": "s", "global_fluct": "^"}
NAME = {"independent": "Independent", "clustered": "Clustered (σ = 2)",
        "global_fluct": "Fluctuation control"}
INK, MUTED = "#222222", "#666666"
T = 3000
RNG = np.random.default_rng(12345)  # bootstrap only

plt.rcParams.update({
    "font.size": 9, "axes.titlesize": 9.5, "axes.labelsize": 9,
    "axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": MUTED,
    "ytick.color": MUTED, "axes.grid": True, "grid.color": "#e6e6e6",
    "grid.linewidth": 0.6, "axes.spines.top": False, "axes.spines.right": False,
    "lines.linewidth": 1.6, "lines.markersize": 4.5, "legend.frameon": False,
    "savefig.dpi": 200, "savefig.bbox": "tight", "font.family": "DejaVu Sans",
})


def wilson(k, n, z=1.96):
    if n == 0:
        return np.nan, np.nan
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return max(0.0, c - h), min(1.0, c + h)


def censored_median(tau, T=T):
    """Median extinction time with right-censoring at T (tau < 0 = survived)."""
    x = np.where(np.asarray(tau) < 0, np.inf, np.asarray(tau, float))
    return float(np.median(x))


def boot_median_ci(tau, B=2000):
    x = np.where(np.asarray(tau) < 0, np.inf, np.asarray(tau, float))
    meds = np.median(RNG.choice(x, size=(B, len(x)), replace=True), axis=1)
    return float(np.percentile(meds, 2.5)), float(np.percentile(meds, 97.5))


def survival_curve(tau, T=T):
    t = np.arange(T + 1)
    x = np.where(np.asarray(tau) < 0, np.inf, np.asarray(tau, float))
    return t, (x[None, :] > t[:, None]).mean(axis=1)


def mu_axis(ax, mus):
    ax.set_xscale("symlog", linthresh=0.001, linscale=0.4)
    ax.set_xticks([0, 0.001, 0.01, 0.1])
    ax.set_xticklabels(["0", "0.001", "0.01", "0.1"])
    ax.set_xlabel("Mortality probability μ")


# ----------------------------------------------------------------------------
# Figure 1: illustrative snapshots and masks
# ----------------------------------------------------------------------------
def fig_snapshots():
    L, mu = 60, 0.005
    init = E.random_grid((L, L), 0.35, E.seed_for(99, 1))
    times = (0, 50, 500, 1500, 3000)
    fig, axs = plt.subplots(3, len(times) + 1, figsize=(7.2, 4.1))
    for r, model in enumerate(("independent", "clustered")):
        res = E.run(init, T, mu, model, 2.0, rng=E.seed_for(99, 2, r),
                    stop_at_extinction=False, keep_frames=times)
        for c, t in enumerate(times):
            ax = axs[r, c]
            ax.imshow(res["frames"][t], cmap="Greys", vmin=0, vmax=1,
                      interpolation="nearest")
            ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
            if r == 0:
                ax.set_title(f"t = {t}")
            if c == 0:
                ax.set_ylabel(NAME[model].split(" (")[0])
        ax = axs[r, -1]
        tt = np.arange(T + 1)
        ax.plot(tt, res["density"], color=COL[model], lw=1)
        ax.set_title("ρ(t)" if r == 0 else "")
        ax.set_xticks([0, 1500, 3000]); ax.tick_params(labelsize=7)
        ax.set_ylim(0, 0.4)
    for c, (model, title) in enumerate((("independent", "Independent marks"),
                                        ("clustered", "Clustered marks"))):
        gen = E.MaskGenerator((L, L), 0.02, model, 2.0)
        m = gen(E.seed_for(99, 3, c))
        ax = axs[2, c]
        ax.imshow(m, cmap="Greys", vmin=0, vmax=1, interpolation="nearest")
        ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
        ax.set_title(title.split()[0], fontsize=8)
    for c in range(2, len(times) + 1):
        axs[2, c].axis("off")
    axs[2, 2].text(0.0, 0.5, "Bottom left: one mortality mask of each model at\n"
                   "μ = 0.02 (black = marked site). Both masks have\n"
                   "the same per-site marking probability μ.", fontsize=7.5,
                   color=MUTED, va="center", transform=axs[2, 2].transAxes)
    fig.tight_layout()
    fig.savefig(FIG / "fig1_snapshots.png")
    plt.close(fig)


# ----------------------------------------------------------------------------
# Experiments A, B, E: mortality sweep
# ----------------------------------------------------------------------------
def sweep_tables(d):
    d = d.copy()
    d["kill_frac"] = d.killed_sum / d.alive_pre_sum.replace(0, np.nan)
    rows = []
    for (model, mu), g in d.groupby(["model", "mu"]):
        n = len(g)
        k = int(g.extinct.sum())
        lo, hi = wilson(k, n)
        r = dict(model=model, mu=mu, M=n, T=T, p0=0.35, L=60,
                 extinct=k, extinct_frac=k / n, extinct_ci_lo=lo, extinct_ci_hi=hi,
                 tau_median=censored_median(g.tau))
        for end, w in ((800, 50), (800, 160), (3000, 50), (3000, 160), (3000, 500)):
            x = g[f"rho_T{end}_W{w}"]
            a = g[f"act_T{end}_W{w}"]
            r[f"rho_mean_T{end}_W{w}"] = x.mean()
            r[f"rho_sd_T{end}_W{w}"] = x.std(ddof=1)
            r[f"rho_se_T{end}_W{w}"] = x.std(ddof=1) / np.sqrt(n)
            r[f"act_mean_T{end}_W{w}"] = a.mean()
            r[f"act_sd_T{end}_W{w}"] = a.std(ddof=1)
            r[f"rho_temporal_sd_T{end}_W{w}"] = g[f"rho_tsd_T{end}_W{w}"].mean()
            r[f"act_temporal_sd_T{end}_W{w}"] = g[f"act_tsd_T{end}_W{w}"].mean()
        kf = g.kill_frac.dropna()
        pooled = g.killed_sum.sum() / g.alive_pre_sum.sum()
        r.update(kill_frac_pooled=pooled, kill_frac_run_mean=kf.mean(),
                 kill_frac_run_sd=kf.std(ddof=1),
                 mark_frac_pooled=g.marked_sum.sum() / (g.steps_simulated.sum() * 3600),
                 kill_ratio=pooled / mu if mu > 0 else np.nan)
        for lab in ("extinct", "static", "periodic", "active", "uncertain",
                    "no_recurrence_within_T"):
            r[f"n_{lab}"] = int((g.label == lab).sum())
        rows.append(r)
    t = pd.DataFrame(rows)
    t.to_csv(TAB / "expA_B_E_sweep_summary.csv", index=False)
    return t


def fig_sweep(t, curves):
    fig, axs = plt.subplots(1, 3, figsize=(7.4, 2.6))
    for model in ("independent", "global_fluct", "clustered"):
        s = t[t.model == model].sort_values("mu")
        if model == "independent":
            pass
        kw = dict(color=COL[model], marker=MRK[model], label=NAME[model])
        axs[0].errorbar(s.mu, s["rho_mean_T3000_W50"], yerr=s["rho_sd_T3000_W50"],
                        capsize=2, elinewidth=0.8, **kw)
        axs[1].errorbar(s.mu, s["rho_mean_T800_W160"], yerr=s["rho_sd_T800_W160"],
                        capsize=2, elinewidth=0.8, **kw)
        axs[2].plot(s.mu, s.extinct_frac, **kw)
        axs[2].fill_between(s.mu, s.extinct_ci_lo, s.extinct_ci_hi,
                            color=COL[model], alpha=0.12, lw=0)
    axs[0].set_title("Late density, T = 3000, W = 50")
    axs[1].set_title("Late density, T = 800, W = 160\n(notebook 06 protocol)")
    axs[2].set_title("Fraction extinct by T = 3000")
    axs[0].set_ylabel("Mean ρ over window (± SD)")
    axs[2].set_ylabel("Fraction of runs (95% CI)")
    for ax in axs:
        mu_axis(ax, None)
    axs[2].set_ylim(-0.03, 1.03)
    axs[2].legend(loc="lower right", fontsize=7)
    fig.tight_layout()
    fig.savefig(FIG / "fig2_mortality_sweep.png")
    plt.close(fig)

    # survival curves
    fig, axs = plt.subplots(1, 3, figsize=(7.4, 2.4), sharey=True)
    for ax, mu in zip(axs, (0.002, 0.005, 0.01)):
        for model in ("independent", "global_fluct", "clustered"):
            c = curves[(curves.model == model) & np.isclose(curves.mu, mu)]
            ax.plot(c.t, c.surviving, color=COL[model], label=NAME[model])
        ax.set_title(f"μ = {mu}")
        ax.set_xlabel("Time step t")
        ax.set_ylim(-0.03, 1.03)
    axs[0].set_ylabel("Fraction of runs alive")
    axs[0].legend(fontsize=7, loc="lower left")
    fig.tight_layout()
    fig.savefig(FIG / "fig3_survival_curves.png")
    plt.close(fig)


def fig_killfrac(t, masks):
    fig, axs = plt.subplots(1, 2, figsize=(7.0, 2.5))
    for model in ("independent", "global_fluct", "clustered"):
        s = t[(t.model == model) & (t.mu > 0)].sort_values("mu")
        axs[0].plot(s.mu, s.kill_ratio, color=COL[model], marker=MRK[model],
                    label=NAME[model])
    axs[0].axhline(1, color=MUTED, lw=0.8, ls="--")
    axs[0].set_xscale("log")
    axs[0].set_ylim(0.9, 1.1)
    axs[0].set_xlabel("Mortality probability μ")
    axs[0].set_ylabel("Observed kill fraction / μ")
    axs[0].set_title("Fraction of live cells removed per step")
    axs[0].legend(fontsize=7)
    m = masks[np.isclose(masks.mu, 0.02)].copy()
    lab = [f"{r.model.replace('_', ' ')}\nσ={r.sigma:g}" if r.model != "independent"
           else "independent" for r in m.itertuples()]
    x = np.arange(len(m))
    axs[1].bar(x - 0.2, m.mark_fraction_sd_per_step / 0.02, width=0.38,
               color="#2a78d6", label="SD of marked fraction per step / μ")
    axs[1].bar(x + 0.2, m.cond_neighbour_prob, width=0.38, color="#eb6834",
               label="P(neighbour marked | site marked)")
    axs[1].set_xticks(x, lab, fontsize=6.5)
    axs[1].set_title("Mask statistics at μ = 0.02 (60 × 60)")
    axs[1].set_ylim(0, 1.35)
    axs[1].legend(fontsize=6.5, loc="upper left", ncol=1)
    fig.tight_layout()
    fig.savefig(FIG / "fig4_mortality_fraction.png")
    plt.close(fig)


# ----------------------------------------------------------------------------
# Experiment C: system size
# ----------------------------------------------------------------------------
def size_analysis(s):
    rows = []
    for (model, mu, L), g in s.groupby(["model", "mu", "L"]):
        n = len(g)
        k = int(g.extinct.sum())
        lo, hi = wilson(k, n)
        med = censored_median(g.tau)
        blo, bhi = boot_median_ci(g.tau)
        ext1000 = int(((g.tau > 0) & (g.tau <= 1000)).sum())
        rows.append(dict(model=model, mu=mu, L=L, M=n, extinct=k, extinct_frac=k / n,
                         ci_lo=lo, ci_hi=hi, extinct_by_1000=ext1000,
                         tau_median=med, tau_median_ci_lo=blo, tau_median_ci_hi=bhi,
                         rho_mean_T3000_W50=g.rho_T3000_W50.mean(),
                         rho_sd_T3000_W50=g.rho_T3000_W50.std(ddof=1)))
    t = pd.DataFrame(rows)
    t.to_csv(TAB / "expC_size_summary.csv", index=False)
    fig, axs = plt.subplots(1, 2, figsize=(7.0, 2.6))
    for model in ("independent", "clustered"):
        for mu, ls in ((0.005, "-"), (0.02, "--")):
            q = t[(t.model == model) & np.isclose(t.mu, mu)].sort_values("L")
            fin = np.isfinite(q.tau_median)
            lab = f"{NAME[model].split(' (')[0]}, μ = {mu}"
            axs[0].plot(q.L, q.extinct_frac, ls=ls, color=COL[model],
                        marker=MRK[model], label=lab)
            if fin.any():
                qq = q[fin]
                axs[1].errorbar(qq.L, qq.tau_median,
                                yerr=[qq.tau_median - qq.tau_median_ci_lo,
                                      np.where(np.isfinite(qq.tau_median_ci_hi),
                                               qq.tau_median_ci_hi, T) - qq.tau_median],
                                ls=ls, color=COL[model], marker=MRK[model],
                                capsize=2, elinewidth=0.8, label=lab)
    axs[0].set_xlabel("Lattice size L"); axs[1].set_xlabel("Lattice size L")
    axs[0].set_ylabel("Fraction extinct by T = 3000")
    axs[1].set_ylabel("Median extinction time (95% CI)")
    axs[0].set_ylim(-0.03, 1.03)
    axs[1].set_xscale("log"); axs[1].set_yscale("log")
    axs[1].set_xticks([40, 60, 100, 200], ["40", "60", "100", "200"])
    axs[0].legend(fontsize=6.5, loc="center right")
    axs[0].set_title("Extinction within the observation window")
    axs[1].set_title("Median extinction time (finite medians only)")
    fig.tight_layout()
    fig.savefig(FIG / "fig5_system_size.png")
    plt.close(fig)
    return t


# ----------------------------------------------------------------------------
# Mechanism check: isolated objects
# ----------------------------------------------------------------------------
def objects_analysis(o):
    rows = []
    for (obj, mu, model), g in o.groupby(["object", "mu", "model"]):
        rows.append(dict(object=obj, mu=mu, model=model, M=len(g),
                         survived_T=int((g.tau < 0).sum()),
                         tau_median=censored_median(g.tau),
                         tau_median_ci_lo=boot_median_ci(g.tau)[0],
                         tau_median_ci_hi=boot_median_ci(g.tau)[1]))
    t = pd.DataFrame(rows)
    t.to_csv(TAB / "mechanism_objects_summary.csv", index=False)
    fig, axs = plt.subplots(1, 3, figsize=(7.4, 2.4), sharey=True)
    for ax, obj in zip(axs, ("block", "beehive", "blinker")):
        for model in ("independent", "global_fluct", "clustered"):
            g = o[(o.object == obj) & np.isclose(o.mu, 0.005) & (o.model == model)]
            tt, S = survival_curve(g.tau)
            ax.plot(tt, S, color=COL[model], label=NAME[model])
        ax.set_xscale("symlog", linthresh=10)
        ax.set_title(f"Isolated {obj}, μ = 0.005")
        ax.set_xlabel("Time step t")
        ax.set_xticks([0, 10, 100, 1000], ["0", "10", "100", "1000"])
    axs[0].set_ylabel("Fraction of runs alive")
    axs[0].legend(fontsize=6.5, loc="lower left")
    fig.tight_layout()
    fig.savefig(FIG / "fig6_object_lifetimes.png")
    plt.close(fig)
    return t


# ----------------------------------------------------------------------------
# Experiment F: sigma dependence
# ----------------------------------------------------------------------------
def sigma_analysis(sg, sweep):
    rows = []
    for (model, sigma, mu), g in sg.groupby(["model", "sigma", "mu"]):
        k = int(g.extinct.sum()); n = len(g)
        lo, hi = wilson(k, n)
        rows.append(dict(model=model, sigma=sigma, mu=mu, M=n, extinct=k,
                         extinct_frac=k / n, ci_lo=lo, ci_hi=hi,
                         tau_median=censored_median(g.tau),
                         kill_ratio=(g.killed_sum.sum() / g.alive_pre_sum.sum()) / mu))
    ind = sweep[(sweep.model == "independent") & sweep.mu.isin([0.002, 0.005, 0.01, 0.02])]
    for mu, g in ind.groupby("mu"):
        k = int(g.extinct.sum()); n = len(g)
        lo, hi = wilson(k, n)
        rows.append(dict(model="independent", sigma=0.0, mu=mu, M=n, extinct=k,
                         extinct_frac=k / n, ci_lo=lo, ci_hi=hi,
                         tau_median=censored_median(g.tau),
                         kill_ratio=(g.killed_sum.sum() / g.alive_pre_sum.sum()) / mu))
    t = pd.DataFrame(rows)
    t.to_csv(TAB / "expF_sigma_summary.csv", index=False)
    fig, axs = plt.subplots(1, 4, figsize=(7.4, 2.4), sharey=True)
    for ax, mu in zip(axs, (0.002, 0.005, 0.01, 0.02)):
        for model in ("clustered", "global_fluct"):
            q = t[(t.model == model) & np.isclose(t.mu, mu)].sort_values("sigma")
            ax.errorbar(q.sigma, q.extinct_frac,
                        yerr=[q.extinct_frac - q.ci_lo, q.ci_hi - q.extinct_frac],
                        color=COL[model], marker=MRK[model], capsize=2,
                        elinewidth=0.8, label=NAME[model].split(" (")[0])
        i = t[(t.model == "independent") & np.isclose(t.mu, mu)]
        ax.axhline(float(i.extinct_frac.iloc[0]), color=COL["independent"], lw=1,
                   ls="--", label="Independent (σ = 0)")
        ax.set_title(f"μ = {mu}")
        ax.set_xlabel("Correlation length σ")
        ax.set_xticks([1, 2, 4])
        ax.set_ylim(-0.03, 1.03)
    axs[0].set_ylabel("Fraction extinct by T = 3000")
    axs[0].legend(fontsize=6.3, loc="center left")
    fig.tight_layout()
    fig.savefig(FIG / "fig7_sigma.png")
    plt.close(fig)
    return t


# ----------------------------------------------------------------------------
# Experiment D: initial conditions
# ----------------------------------------------------------------------------
def initial_analysis(ini, dec):
    rows = []
    for (model, mu, p0), g in ini.groupby(["model", "mu", "p0"]):
        k = int(g.extinct.sum()); n = len(g)
        lo, hi = wilson(k, n)
        rows.append(dict(model=model, mu=mu, p0=p0, M=n, extinct=k, extinct_frac=k / n,
                         ci_lo=lo, ci_hi=hi, tau_median=censored_median(g.tau),
                         rho_mean_T3000_W50=g.rho_T3000_W50.mean(),
                         rho_sd_T3000_W50=g.rho_T3000_W50.std(ddof=1),
                         rho_mean_T800_W160=g.rho_T800_W160.mean()))
    t = pd.DataFrame(rows)
    t.to_csv(TAB / "expD_initial_density_summary.csv", index=False)

    # one-way random-effects decomposition: K initial grids x R dynamics seeds
    drows = []
    for (model, mu), g in dec.groupby(["model", "mu"]):
        for var, f in (("rho_T800_W160", lambda x: x),
                       ("tau_capped", None)):
            if var == "tau_capped":
                y = np.where(g.tau < 0, T, g.tau).astype(float)
            else:
                y = g[var].to_numpy(float)
            gg = pd.DataFrame(dict(k=g.ic_rep.to_numpy(), y=y))
            K = gg.k.nunique(); R = len(gg) // K
            means = gg.groupby("k").y.mean()
            msb = R * means.var(ddof=1)
            msw = gg.groupby("k").y.var(ddof=1).mean()
            var_b = max(0.0, (msb - msw) / R)
            icc = var_b / (var_b + msw) if (var_b + msw) > 0 else np.nan
            F = msb / msw if msw > 0 else np.nan
            from scipy.stats import f as fdist
            pval = 1 - fdist.cdf(F, K - 1, K * (R - 1)) if np.isfinite(F) else np.nan
            drows.append(dict(model=model, mu=mu, quantity=var, K=K, R=R,
                              grand_mean=gg.y.mean(), var_between_ic=var_b,
                              var_within_ic=msw, icc=icc, F=F, p_value=pval,
                              extinct_frac=float(g.extinct.mean())))
    dt = pd.DataFrame(drows)
    dt.to_csv(TAB / "expD_variance_decomposition.csv", index=False)

    fig, axs = plt.subplots(1, 2, figsize=(7.0, 2.5))
    for model in ("independent", "clustered"):
        for mu, ls in ((0.005, "-"), (0.02, "--")):
            q = t[(t.model == model) & np.isclose(t.mu, mu)].sort_values("p0")
            lab = f"{NAME[model].split(' (')[0]}, μ = {mu}"
            axs[0].errorbar(q.p0, q.extinct_frac,
                            yerr=[q.extinct_frac - q.ci_lo, q.ci_hi - q.extinct_frac],
                            ls=ls, color=COL[model], marker=MRK[model], capsize=2,
                            elinewidth=0.8, label=lab)
            axs[1].errorbar(q.p0, q.rho_mean_T800_W160, ls=ls, color=COL[model],
                            marker=MRK[model], label=lab)
    axs[0].set_xlabel("Initial density p₀"); axs[1].set_xlabel("Initial density p₀")
    axs[0].set_ylabel("Fraction extinct by T = 3000")
    axs[1].set_ylabel("Mean ρ, T = 800, W = 160")
    axs[0].set_ylim(-0.03, 1.03)
    axs[0].set_xticks([0.2, 0.35, 0.5]); axs[1].set_xticks([0.2, 0.35, 0.5])
    axs[0].legend(fontsize=6.5)
    fig.tight_layout()
    fig.savefig(FIG / "fig8_initial_density.png")
    plt.close(fig)
    return t, dt


def window_check(t):
    """Does the averaging window change the conclusions?"""
    cols = ["model", "mu", "rho_mean_T3000_W50", "rho_mean_T3000_W160",
            "rho_mean_T3000_W500", "rho_sd_T3000_W50", "rho_temporal_sd_T3000_W50",
            "act_mean_T3000_W50", "act_mean_T3000_W500", "act_sd_T3000_W50",
            "act_temporal_sd_T3000_W50"]
    w = t[cols].copy()
    w.to_csv(TAB / "expA_window_and_variance_components.csv", index=False)
    return w


def main():
    sweep = pd.read_csv(RES / "sweep_runs.csv")
    curves = pd.read_csv(RES / "sweep_curves.csv")
    masks = pd.read_csv(RES / "mask_statistics.csv")
    t = sweep_tables(sweep)
    window_check(t)
    fig_snapshots()
    fig_sweep(t, curves)
    fig_killfrac(t, masks)
    objects_analysis(pd.read_csv(RES / "objects_runs.csv"))
    if (RES / "size_runs.csv").exists():
        size_analysis(pd.read_csv(RES / "size_runs.csv"))
    if (RES / "sigma_runs.csv").exists():
        sigma_analysis(pd.read_csv(RES / "sigma_runs.csv"), sweep)
    if (RES / "initial_runs.csv").exists() and (RES / "icdecomp_runs.csv").exists():
        initial_analysis(pd.read_csv(RES / "initial_runs.csv"),
                         pd.read_csv(RES / "icdecomp_runs.csv"))
    print("figures and tables written")


if __name__ == "__main__":
    main()
