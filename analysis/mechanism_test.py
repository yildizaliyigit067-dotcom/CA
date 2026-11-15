"""Quantitative test of the block self-repair mechanism.

Hypothesis: a block is destroyed in a given update if and only if at least two of
its four cells are removed in that update (a single removal is repaired by the
Life rule in the next update). Then its lifetime is geometric with per-update
death probability q = P(at least 2 of the block's 4 sites marked).

Test 1 (isolated blocks): estimate q for each mortality model directly from
mortality masks (no Life dynamics involved), predict the survival probability
S(3000) = (1-q)^3000 and the median lifetime, and compare with the 400
simulated isolated blocks in results/objects_runs.csv.

Test 2 (populations made only of blocks): place K isolated, non-interacting
blocks on a 60 x 60 torus and run the full stochastic Life dynamics. If the
surviving ash of random runs is dominated by blocks, the extinction behaviour of
such block-only populations should reproduce that of the random-initial runs in
results/sweep_runs.csv. The block-only prediction is also computed from q:
P(extinct by t) = (1 - (1-q)^t)^K for independent blocks.

Writes results/mechanism_test.csv and results/mechanism_block_populations.csv.
"""
import sys
from multiprocessing import Pool
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ca_engine as E  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
T = 3000
MUS = (0.002, 0.005, 0.01, 0.02)
MODELS = ("independent", "global_fluct", "clustered")


def estimate_q(model, mu, n_masks=50000, L=32, seed=0):
    """P(>=2 of the 4 cells of a 2x2 block are marked) and P(exactly 1).

    Independent model: exact binomial values. Correlated models: estimated from
    masks, reading 16 block positions spaced 8 sites apart in every mask (spacing
    of 4 correlation lengths for sigma = 2, so positions are nearly independent).
    """
    if model == "independent":
        p0 = (1 - mu) ** 4
        p1 = 4 * mu * (1 - mu) ** 3
        return 1 - p0 - p1, p1
    gen = E.MaskGenerator((L, L), mu, model, 2.0)
    rng = E.seed_for(77, seed, MODELS.index(model), int(mu * 1e6))
    n2 = n1 = n = 0
    for _ in range(n_masks):
        m = gen(rng).astype(np.int8)
        h = m[0::8, 0::8] + m[1::8, 0::8] + m[0::8, 1::8] + m[1::8, 1::8]
        n2 += int((h >= 2).sum())
        n1 += int((h == 1).sum())
        n += h.size
    return n2 / n, n1 / n


def block_population(job):
    model, mu, K, rep = job
    rng0 = E.seed_for(78, K, rep)
    L = 60
    g = np.zeros((L, L), np.uint8)
    # K blocks on a coarse grid of 6 x 6 cells per slot, randomly chosen slots,
    # so that blocks never interact
    slots = [(r, c) for r in range(0, L, 6) for c in range(0, L, 6)]
    chosen = rng0.choice(len(slots), size=K, replace=False)
    for k in chosen:
        r, c = slots[k]
        g[r + 2:r + 4, c + 2:c + 4] = 1
    res = E.run(g, T, mu, model, 2.0,
                rng=E.seed_for(79, MODELS.index(model), int(mu * 1e6), K, rep))
    return dict(model=model, mu=mu, K=K, rep=rep, tau=res["tau"],
                extinct=int(res["tau"] >= 0))


def main():
    obj = pd.read_csv(ROOT / "results" / "objects_runs.csv")
    rows = []
    for model in MODELS:
        for mu in MUS:
            q, p1 = estimate_q(model, mu)
            pred_S = (1 - q) ** T
            pred_med = np.log(2) / -np.log(1 - q) if q > 0 else np.inf
            r = dict(model=model, mu=mu, q_two_or_more_hits=q, p_exactly_one_hit=p1,
                     predicted_survival_3000=pred_S, predicted_median=pred_med)
            o = obj[(obj.object == "block") & (obj.model == model) & np.isclose(obj.mu, mu)]
            if len(o):
                x = np.where(o.tau < 0, np.inf, o.tau)
                r.update(simulated_n=len(o),
                         simulated_survival_3000=float(np.mean(o.tau < 0)),
                         simulated_median=float(np.median(x)))
            rows.append(r)
            print(r, flush=True)
    pd.DataFrame(rows).to_csv(ROOT / "results" / "mechanism_test.csv", index=False)

    # Test 2: block-only populations. K chosen to match the typical number of
    # blocks in the random-initial ash (about 6 blocks per run at mu = 0.005,
    # from analysis/census.py: 223 blocks in 40 runs).
    jobs = [(m, mu, 6, rep) for m in ("independent", "clustered")
            for mu in (0.005, 0.02) for rep in range(200)]
    with Pool(2) as p:
        out = p.map(block_population, jobs, chunksize=10)
    df = pd.DataFrame(out)
    df.to_csv(ROOT / "results" / "mechanism_block_populations.csv", index=False)
    print(df.groupby(["model", "mu"]).agg(extinct=("extinct", "mean"),
          tau_median=("tau", lambda x: np.median(np.where(x < 0, np.inf, x)))))


if __name__ == "__main__":
    main()
