"""Reproducible experiments A-F for the stochastic Game of Life review.

Usage:
    python analysis/experiments.py sweep        # Experiments A, B, E (and F control)
    python analysis/experiments.py size         # Experiment C
    python analysis/experiments.py initial      # Experiment D
    python analysis/experiments.py sigma        # Experiment F (sigma dependence)
    python analysis/experiments.py objects      # Experiment F (mechanism check)
    python analysis/experiments.py masks        # Experiment B/F (mask statistics)
    python analysis/experiments.py all

Every run draws its random numbers from ``numpy.random.SeedSequence`` keys that
are written to the output CSV, so any single run can be regenerated.
Initial grids depend only on (experiment, L, p0, replicate), so the same initial
grids are shared across mortality models and mortality rates (common random
numbers).  Dynamics seeds additionally depend on model, mu and sigma.
"""
from __future__ import annotations

import hashlib
import sys
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ca_engine as E  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"
RES.mkdir(exist_ok=True)

MODEL_ID = {"independent": 0, "clustered": 1, "global_fluct": 2}
EXP_ID = {"sweep": 1, "size": 2, "initial": 3, "sigma": 4, "objects": 5,
          "masks": 6, "icdecomp": 7}
P0 = 0.35
T_LONG = 3000
QUASI_STATIC_WINDOW = 300
QUASI_STATIC_FRACTION = 0.90


def ic_key(exp, L, p0, rep):
    return (EXP_ID[exp], L, int(round(p0 * 1000)), rep, 0)


def dyn_key(exp, L, p0, model, mu, sigma, rep, extra=0):
    return (EXP_ID[exp], L, int(round(p0 * 1000)), MODEL_ID[model],
            int(round(mu * 1e6)), int(round(sigma * 100)), rep, extra, 1)


SETTLE_STEPS = 30       # max noise-free transient for "static"/"periodic"
CONTINUATION = 2000     # noise-free steps searched for an exact recurrence


def config_label(grid, max_period=None):
    """Label a configuration by its noise-free Life continuation.

    The configuration is evolved with the deterministic B3/S23 rule and states
    are hashed until the first exact recurrence (transient length, period).

    extinct_nf  the continuation reaches the empty grid
    static      settles within SETTLE_STEPS steps onto a period-1 state
    periodic    settles within SETTLE_STEPS steps onto a cycle of period > 1
                (this includes gliders travelling around the torus)
    active      needs more than SETTLE_STEPS steps to settle, or shows no
                recurrence within CONTINUATION steps
    """
    g = grid.copy()
    seen = {g.tobytes(): 0}
    for t in range(1, CONTINUATION + 1):
        g = E.life_step(g)
        key = g.tobytes()
        if key in seen:
            transient, period = seen[key], t - seen[key]
            if not g.any():
                return "extinct_nf", transient
            if transient > SETTLE_STEPS:
                return "active", period
            return ("static" if period == 1 else "periodic"), period
        seen[key] = t
    return "active", -1


def classify(res, mu, T):
    """Operational long-time label.  Never based on the final value alone.

    For mu > 0 the configurations at T and at T - 300 are each labelled by
    ``config_label``.  If the two labels differ, the run is marked
    ``uncertain``.  A configuration whose noise-free continuation dies out
    (``extinct_nf``) while the noisy run survived is reported as such.
    """
    if 0 <= res["tau"] <= T:
        return "extinct"
    if mu == 0.0:
        return res.get("mu0_label", "unclassified")
    fr = res["frames"]
    lab_T, per_T = config_label(fr[T])
    lab_0, _ = config_label(fr[T - QUASI_STATIC_WINDOW])
    res["final_period"] = per_T
    if lab_T != lab_0:
        return "uncertain"
    return lab_T


def mu0_recurrence(initial, T):
    """For mu = 0: detect exact recurrence of the full grid by hashing states."""
    g = initial.copy()
    seen = {hashlib.blake2b(g.tobytes(), digest_size=16).digest(): 0}
    for t in range(1, T + 1):
        g = E.life_step(g)
        h = hashlib.blake2b(g.tobytes(), digest_size=16).digest()
        if h in seen:
            period = t - seen[h]
            transient = seen[h]
            if not g.any():
                return "extinct", transient, period
            return ("static" if period == 1 else "periodic"), transient, period
        seen[h] = t
    return "no_recurrence_within_T", -1, -1


def summarize_run(res, mu, T, ends=(800, 3000), windows=(50, 160, 300, 500)):
    out = {"tau": res["tau"], "extinct": int(0 <= res["tau"] <= T)}
    dens = np.zeros(T + 1)
    act = np.zeros(T)
    ract = np.zeros(T)
    n = len(res["density"])
    dens[:n] = res["density"]
    act[:len(res["activity"])] = res["activity"]
    ract[:len(res["rule_activity"])] = res["rule_activity"]
    for end in ends:
        if end > T:
            continue
        for w in windows:
            d = dens[end - w + 1:end + 1]      # states G_{end-w+1} .. G_end
            a = act[end - w:end]               # transitions ending at those states
            out[f"rho_T{end}_W{w}"] = float(d.mean())
            out[f"rho_tsd_T{end}_W{w}"] = float(d.std(ddof=1))
            out[f"act_T{end}_W{w}"] = float(a.mean())
            out[f"act_tsd_T{end}_W{w}"] = float(a.std(ddof=1))
            out[f"ruleact_T{end}_W{w}"] = float(ract[end - w:end].mean())
    alive = res["alive_pre"]
    killed = res["killed"]
    out["alive_pre_sum"] = int(alive.sum())
    out["killed_sum"] = int(killed.sum())
    out["marked_sum"] = int(res["marked"].sum())
    out["steps_simulated"] = int(len(alive) if res["tau"] < 0 else res["tau"])
    out["label"] = classify(res, mu, T)
    out["final_period"] = res.get("final_period", -1)
    ra = ract[T - QUASI_STATIC_WINDOW:T]
    out["frac_steps_rule_inactive_last300"] = float(np.mean(ra == 0))
    return out


# ----------------------------------------------------------------------------
# Generic worker
# ----------------------------------------------------------------------------
def worker(job):
    exp, L, p0, model, mu, sigma, rep, T = job[:8]
    extra = job[8] if len(job) > 8 else 0
    ic_rep = job[9] if len(job) > 9 else rep
    ik = ic_key(exp, L, p0, ic_rep)
    dk = dyn_key(exp, L, p0, model, mu, sigma, rep, extra)
    init = E.random_grid((L, L), p0, E.seed_for(*ik))
    res = E.run(init, T, mu, model, sigma, rng=E.seed_for(*dk),
                keep_frames=(T - QUASI_STATIC_WINDOW, T))
    if mu == 0.0:
        lab, tr, per = mu0_recurrence(init, T)
        res["mu0_label"] = lab
    row = dict(experiment=exp, L=L, p0=p0, model=model, mu=mu,
               sigma=sigma if model != "independent" else 0.0, rep=rep,
               ic_rep=ic_rep, dyn_extra=extra, T=T,
               ic_seed_key="-".join(map(str, ik)),
               dyn_seed_key="-".join(map(str, dk)),
               initial_density=float(init.mean()))
    row.update(summarize_run(res, mu, T))
    if mu == 0.0:
        row["mu0_transient"] = tr
        row["mu0_period"] = per
    # thinned mean curves are aggregated by the caller
    dens = np.zeros(T + 1)
    dens[:len(res["density"])] = res["density"]
    act = np.zeros(T)
    act[:len(res["activity"])] = res["activity"]
    return row, dens[::5].astype(np.float32), act[4::5].astype(np.float32)


def run_jobs(jobs, name, curve_keys=("model", "mu", "L", "sigma")):
    t0 = time.time()
    with Pool(2) as pool:
        out = pool.map(worker, jobs, chunksize=1)
    rows = [o[0] for o in out]
    df = pd.DataFrame(rows)
    df.to_csv(RES / f"{name}_runs.csv", index=False)
    # mean time series per condition (every 5th step)
    curves = []
    for (row, d, a) in out:
        curves.append({**{k: row[k] for k in curve_keys}, "d": d, "a": a})
    cdf = pd.DataFrame(curves)
    recs = []
    for key, grp in cdf.groupby(list(curve_keys)):
        D = np.stack(grp["d"].values)
        A = np.stack(grp["a"].values)
        tt = np.arange(D.shape[1]) * 5
        for i, t in enumerate(tt):
            rec = dict(zip(curve_keys, key))
            rec.update(t=int(t), n_runs=len(D), rho_mean=float(D[:, i].mean()),
                       rho_sd=float(D[:, i].std(ddof=1)),
                       surviving=float(np.mean(D[:, i] > 0)))
            if i < A.shape[1]:
                rec.update(act_mean=float(A[:, i].mean()),
                           act_sd=float(A[:, i].std(ddof=1)))
            recs.append(rec)
    pd.DataFrame(recs).to_csv(RES / f"{name}_curves.csv", index=False)
    print(f"{name}: {len(jobs)} runs in {time.time() - t0:.0f} s", flush=True)
    return df


# ----------------------------------------------------------------------------
# Experiments
# ----------------------------------------------------------------------------
MU_SWEEP = [0.0, 0.001, 0.002, 0.003, 0.005, 0.0075, 0.01, 0.015, 0.02,
            0.03, 0.05, 0.1]


def exp_sweep(M=40, L=60):
    jobs = []
    for model in ("independent", "clustered", "global_fluct"):
        for mu in MU_SWEEP:
            if mu == 0.0 and model != "independent":
                continue
            for rep in range(M):
                jobs.append(("sweep", L, P0, model, mu, 2.0, rep, T_LONG))
    return run_jobs(jobs, "sweep")


def exp_size(M=40):
    jobs = []
    for L in (40, 60, 80, 100, 140, 200):
        for model in ("independent", "clustered"):
            for mu in (0.005, 0.02):
                for rep in range(M):
                    jobs.append(("size", L, P0, model, mu, 2.0, rep, T_LONG))
    return run_jobs(jobs, "size")


def exp_initial(M=40, L=60):
    jobs = []
    for p0 in (0.20, 0.35, 0.50):
        for model in ("independent", "clustered"):
            for mu in (0.005, 0.02):
                for rep in range(M):
                    jobs.append(("initial", L, p0, model, mu, 2.0, rep, T_LONG))
    df = run_jobs(jobs, "initial", curve_keys=("model", "mu", "p0"))
    # variance decomposition: K initial grids x R dynamics seeds
    K, R = 12, 12
    jobs = []
    for model in ("independent", "clustered"):
        for mu in (0.005, 0.02):
            for k in range(K):
                for r in range(R):
                    jobs.append(("icdecomp", L, P0, model, mu, 2.0, k * R + r,
                                 T_LONG, r, k))
    run_jobs(jobs, "icdecomp", curve_keys=("model", "mu"))
    return df


def exp_sigma(M=40, L=60):
    jobs = []
    for sigma in (1.0, 2.0, 4.0):
        for model in ("clustered", "global_fluct"):
            for mu in (0.002, 0.005, 0.01, 0.02):
                for rep in range(M):
                    jobs.append(("sigma", L, P0, model, mu, sigma, rep, T_LONG))
    return run_jobs(jobs, "sigma")


# --- mechanism check: lifetime of isolated still lifes and oscillators -------
OBJECTS = {
    "block": [(0, 0), (0, 1), (1, 0), (1, 1)],
    "beehive": [(0, 1), (0, 2), (1, 0), (1, 3), (2, 1), (2, 2)],
    "blinker": [(0, 0), (0, 1), (0, 2)],
}


def object_worker(job):
    name, model, mu, sigma, rep, T, L = job
    g = np.zeros((L, L), np.uint8)
    for r, c in OBJECTS[name]:
        g[L // 2 + r, L // 2 + c] = 1
    key = (EXP_ID["objects"], list(OBJECTS).index(name), MODEL_ID[model],
           int(round(mu * 1e6)), int(round(sigma * 100)), rep)
    res = E.run(g, T, mu, model, sigma, rng=E.seed_for(*key))
    return dict(object=name, model=model, mu=mu, sigma=sigma, rep=rep, T=T, L=L,
                seed_key="-".join(map(str, key)), tau=res["tau"],
                extinct=int(res["tau"] >= 0),
                first_kill=int(np.argmax(res["killed"] > 0) + 1)
                if res["killed"].any() else -1)


def exp_objects(M=400, T=3000, L=32):
    jobs = [(name, model, mu, 2.0, rep, T, L)
            for name in OBJECTS
            for model in ("independent", "clustered", "global_fluct")
            for mu in (0.005, 0.02)
            for rep in range(M)]
    t0 = time.time()
    with Pool(2) as pool:
        rows = pool.map(object_worker, jobs, chunksize=20)
    pd.DataFrame(rows).to_csv(RES / "objects_runs.csv", index=False)
    print(f"objects: {len(jobs)} runs in {time.time() - t0:.0f} s")


def exp_masks(n_fields=2000, L=60):
    """Marginal mark probability and nearest-neighbour co-marking."""
    rows = []
    for model, sigma in (("independent", 0.0), ("clustered", 1.0),
                         ("clustered", 2.0), ("clustered", 4.0),
                         ("global_fluct", 2.0)):
        for mu in (0.005, 0.02, 0.1):
            gen = E.MaskGenerator((L, L), mu, model, sigma if sigma else 2.0)
            rng = E.seed_for(EXP_ID["masks"], MODEL_ID[model], int(sigma * 100),
                             int(mu * 1e6))
            fr = np.empty(n_fields)
            pair = np.empty(n_fields)
            for i in range(n_fields):
                m = gen(rng)
                fr[i] = m.mean()
                pair[i] = (m & np.roll(m, 1, axis=0)).mean()
            rows.append(dict(model=model, sigma=sigma, mu=mu, L=L,
                             n_fields=n_fields,
                             mark_fraction_mean=fr.mean(),
                             mark_fraction_se=fr.std(ddof=1) / np.sqrt(n_fields),
                             mark_fraction_sd_per_step=fr.std(ddof=1),
                             pair_mean=pair.mean(),
                             cond_neighbour_prob=pair.mean() / fr.mean()))
    pd.DataFrame(rows).to_csv(RES / "mask_statistics.csv", index=False)
    print("masks done")


if __name__ == "__main__":
    which = sys.argv[1:] or ["all"]
    if "all" in which:
        which = ["masks", "objects", "sweep", "size", "initial", "sigma"]
    for w in which:
        {"sweep": exp_sweep, "size": exp_size, "initial": exp_initial,
         "sigma": exp_sigma, "objects": exp_objects, "masks": exp_masks}[w]()
