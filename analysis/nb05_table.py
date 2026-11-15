"""Regenerate the full main-sweep table of notebook 05 (19 values of p).

The script executes the code cells of ``05_random_initial_conditions.ipynb`` up to
and including the main experiment (same seeds, same functions) and writes
``results/nb05_main_sweep_table.csv``.  Plotting is disabled.
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
nb = json.load(open(ROOT / "05_random_initial_conditions.ipynb"))
ns = {}
for cell in nb["cells"]:
    if cell["cell_type"] != "code":
        continue
    src = "".join(cell["source"])
    exec(src.replace("plt.show()", "plt.close('all')"), ns)
    if "RUN_MAIN_EXPERIMENT" in src:
        break
rows = []
for p in ns["main_p_values"]:
    r = ns["main_results"][float(p)]
    M = len(r["rho_samples"])
    rows.append(dict(p=round(float(p), 2), M=M, rho_mean=r["rho_mean"],
                     rho_sd=r["rho_std"], rho_se=r["rho_std"] / np.sqrt(M),
                     activity_mean=r["activity_mean"], activity_sd=r["activity_std"],
                     activity_se=r["activity_std"] / np.sqrt(M)))
out = ROOT / "results" / "nb05_main_sweep_table.csv"
pd.DataFrame(rows).to_csv(out, index=False)
print("written", out)
