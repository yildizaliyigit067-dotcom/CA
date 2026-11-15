"""Cross-check of the review engine against notebook 06 (Section 11, 480 runs).

1. Re-runs a subset of notebook 06 runs with *its own* seed formula and checks
   that the extinction times agree exactly with results/notebook06/*.csv.
2. Runs 40 additional replicates (rep = 20..59) of the condition
   L = 200, mu = 0.02, independent mortality, with the same seed formula.

Writes results/crosscheck_nb06.csv.
"""
import sys
from multiprocessing import Pool
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ca_engine as E  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def nb06_run(args):
    L, mu, sigma, rep = args
    start = 620000 + L * 1000 + rep
    death = start + (10000000 if sigma == 0 else 20000000) + int(mu * 1000000)
    g = (np.random.default_rng(start).random((L, L)) < 0.35).astype(np.uint8)
    model = "independent" if sigma == 0 else "clustered"
    return E.run(g, 3000, mu, model, 2.0, rng=np.random.default_rng(death))["tau"]


if __name__ == "__main__":
    ref = pd.read_csv(ROOT / "results" / "notebook06" / "stochastic_3000_tum_480_simulasyon.csv")
    jobs = [(L, mu, s, rep) for L in (60, 200) for mu in (0.005, 0.02)
            for s in (0.0, 2.0) for rep in range(0, 20, 4)]
    extra = [(200, 0.02, 0.0, rep) for rep in range(20, 60)]
    with Pool(2) as p:
        taus = p.map(nb06_run, jobs + extra)
    rows = []
    mism = 0
    for (L, mu, s, rep), tau in zip(jobs + extra, taus):
        r = dict(L=L, mu=mu, sigma=s, rep=rep, tau_review_engine=tau)
        if rep < 20:
            name = "Independent" if s == 0 else "Clustered"
            q = ref[(ref.L == L) & np.isclose(ref.mu, mu) & (ref.model == name)
                    & (ref.tekrar == rep + 1)]
            r["tau_notebook06"] = int(q.tau.iloc[0])
            mism += int(r["tau_notebook06"] != tau)
        rows.append(r)
    out = pd.DataFrame(rows)
    out.to_csv(ROOT / "results" / "crosscheck_nb06.csv", index=False)
    ex = out[out.rep >= 20]
    print(f"reproduced {len(jobs)} notebook-06 runs, mismatches: {mism}")
    print(f"extra replicates L=200 mu=0.02: {int((ex.tau_review_engine > 0).sum())}/{len(ex)} extinct")
