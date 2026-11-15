# Changelog

All changes below were made on the branch `review/english-and-verification`, starting from commit `3d72928` on `main`. The original Turkish notebooks remain available on `main` and in the history of this branch.

## 2026-11-15: English translation and scientific verification

### Fixed
- `06_stochastic_life.ipynb`, Section 4 (cell 13): renamed the loop variables `a, b` to `arr_1, arr_2`. The old names overwrote the test grid `b`, so the notebook failed at Section 8 when run from top to bottom. No other code logic was changed.
- `04_game_of_life.ipynb`: toad population corrected from "between 6 and 8" to 6 in two tables, as shown by the notebook's own population time series. A visible review note marks the change.
- `04_game_of_life.ipynb`: equations written as `\$$[ ... \]$$` did not render and were rewritten as `$$ ... $$`.
- `02_rule_classification.ipynb`: the Rule 90 row of the initial-condition table had an extra column. Its text was moved into the correct column.
- `01_elementary_CA.ipynb`: the plot of the number of occupied cells was titled "activity" in Turkish. The English title now describes the plotted quantity.

### Changed
- All six notebooks: Markdown, headings, comments, docstrings, printed messages, assertion messages, plot titles, axis labels and legend labels translated from Turkish into English. Variable names, function names, dictionary keys and output file names were kept unchanged (for example `uzun_deney`, `tekrar`, `stochastic_3000_tum_480_simulasyon.csv`). The model labels `Bağımsız` and `Kümelenmiş` became `Independent` and `Clustered`.
- All six notebooks were re-executed from a clean kernel (Python 3.13.18). Every printed number is identical to the original outputs. Only wall-clock timings differ.
- `06_stochastic_life.ipynb`: the unchecked item "re-run the current version from start to finish" in the submission checklist was marked as done, with a note on how it was verified.
- `AI_NOTES.md`: translated into English and extended with a "Review session" section.
- `README.md`: rewritten in English.
- `.gitignore`: added `*.pyc` and `.pytest_cache/`.

### Added
- Review notes (marked *[Review note ...]*) in notebooks 02, 03, 04, 05 and 06 where a statement was found to be inaccurate, unresolved by the data or in need of context. The original statements were kept.
- `analysis/ca_engine.py`: simulation engine for the stochastic Game of Life, bit-identical to notebook 06 for the same seeds. Adds the `global_fluct` control model.
- `analysis/tests/test_engine.py`: 6 tests (Life step against `np.roll`, known patterns, bit-identical independent and clustered models, limits, bookkeeping).
- `analysis/experiments.py`: Experiments A to F with recorded seeds.
- `analysis/make_figures.py`, `analysis/nb05_table.py`, `analysis/crosscheck_nb06.py`.
- `results/`: run-level CSV files, summary tables (`results/tables/`), mask statistics, notebook 06 data files, environment record.
- `figures/`: eight figures used in the technical report.
- `report/`: LaTeX source and PDF of the technical report for supervisor review.
- `VALIDATION_REPORT.md`, `CHANGELOG.md`, `requirements.txt`.

### Not changed
- No model definition, parameter value, seed or stored result in the notebooks was changed.
- The optional glider-perturbation investigation in notebook 04 (Section 10) remains empty, as in the original.
