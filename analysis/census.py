"""Census of the surviving structures at t = 3000.

Re-runs the 40 independent-mortality runs of Experiment A at mu = 0.005
(same seeds as analysis/experiments.py) and classifies the connected
components (8-neighbourhood) of the final grid. Components that touch the
periodic boundary may be split in two, which slightly overcounts small
fragments. Writes results/census_independent_mu0.005.csv.
"""
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.ndimage import label

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ca_engine as E  # noqa: E402
import experiments as X  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
L, P0, MU, T = 60, 0.35, 0.005, 3000
rows = []
for rep in range(40):
    init = E.random_grid((L, L), P0, E.seed_for(*X.ic_key("sweep", L, P0, rep)))
    rng = E.seed_for(*X.dyn_key("sweep", L, P0, "independent", MU, 2.0, rep))
    res = E.run(init, T, MU, "independent", 2.0, rng=rng, keep_frames=(T,))
    if T not in res["frames"]:
        continue
    lab, n = label(res["frames"][T], structure=np.ones((3, 3), int))
    counts = Counter()
    for k in range(1, n + 1):
        ys, xs = np.nonzero(lab == k)
        is_block = len(ys) == 4 and np.ptp(ys) == 1 and np.ptp(xs) == 1
        counts["block" if is_block else f"other_{len(ys)}_cells"] += 1
    for kind, c in counts.items():
        rows.append(dict(rep=rep, kind=kind, n_objects=c))
df = pd.DataFrame(rows)
df.to_csv(ROOT / "results" / "census_independent_mu0.005.csv", index=False)
tot = df.groupby("kind").n_objects.sum()
cells = sum(int(k.split("_")[1]) * v if k != "block" else 4 * v for k, v in tot.items())
print(tot.sort_values(ascending=False).to_string())
print("block share of objects:", round(tot.get("block", 0) / tot.sum(), 3))
print("block share of live cells:", round(4 * tot.get("block", 0) / cells, 3))
