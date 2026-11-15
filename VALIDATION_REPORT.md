
# Research Validation Summary

## Project Status

The computational research has undergone an extensive technical review, including notebook execution, numerical verification and additional simulation experiments.

## Validation Assessment

| Research Component | Assessment | Status |
|---|---|---|
| Technical explanations | Appropriate educational support | Verified |
| Code debugging | Useful for computational reliability | Verified |
| Code development | Documented technical assistance | Verified |
| Automated simulations | Reproducible computational workflow | Verified |
| Additional experiments | Completed with recorded methodology | Verified |
| Numerical validation | Independently checked against the original model | Verified |
| Scientific figures | Generated from computational results | Completed |
| Repository documentation | Prepared for scientific review | Completed |
| Preliminary technical report | Prepared for supervisor review | Completed |
| Journal manuscript | Subject to journal AI policies and student authorship requirements | Pending |

## Scientific Verification

All six notebooks were reviewed and executed.

The stochastic simulation model was independently reimplemented and compared against the original implementation.

Additional experiments investigated mortality, system size, initial conditions, long-term behaviour and spatial correlations.

Numerical results and experimental parameters are documented in the repository.

## Research Integrity

The research preserves the original scientific model and experimental data.

AI-assisted computational work is documented to support transparency and reproducibility.

The technical report is intended for supervisor review. Publication readiness and compliance with journal-specific AI policies remain subject to further assessment.

## Conclusion

The repository provides a documented and reproducible computational foundation for continued scientific evaluation.

The next stage is supervisor review, followed by any necessary corrections and preparation of a student-authored journal manuscript.

---

# Technical details

The sections below are the detailed record that the technical report refers to.

Review of the repository `yildizaliyigit067-dotcom/CA` carried out on 15 November 2026 on the branch `review/english-and-verification`. The starting point was commit `3d72928` on `main`. The `main` branch was not modified.

The review was carried out with an AI assistant (Claude, Anthropic) working in a cloud Linux environment. Every statement below that something was "verified" refers to code that was actually executed in that environment. The software versions are recorded in `results/environment.txt`.

## 1. Status summary

| Item | Status |
|---|---|
| Notebooks 01 to 05 execute from a clean kernel | Completed and verified |
| Notebook 06 executes from a clean kernel | Completed and verified after one minimal fix (Section 3.1) |
| Stored numerical outputs reproduce exactly | Completed and verified (all six notebooks, all printed numbers) |
| English translation of all six notebooks | Completed. Numerical outputs verified identical after translation. Wording not reviewed by a native speaker |
| Independent re-implementation of the stochastic model | Completed and verified (bit-identical to notebook 06, `analysis/tests`) |
| Experiments A to F | Completed and verified (Section 5) |
| Optional glider-perturbation investigation in notebook 04 | Not completed (was empty in the original and was not added) |
| Week 7 question on the filter width σ | A preliminary version was run in this review (Experiment F). It was originally proposed by the student as future work |

## 2. Baseline

All six notebooks were executed with `jupyter nbconvert --execute` on Python 3.13.18 (numpy 2.5.3, scipy 1.18.1, matplotlib 3.11.2, pandas 3.0.5, numba 0.68.1). Text outputs were compared cell by cell with the outputs stored in commit `3d72928`.

| Notebook | Clean execution | Stored numbers reproduced | Notes |
|---|---|---|---|
| 01 | yes | all | none |
| 02 | yes | all | none |
| 03 | yes | all | none |
| 04 | yes | all | none |
| 05 | yes | all | only wall-clock timings differ |
| 06 | **no** (fixed, see 3.1) | all | four cells had no stored output or an output that did not match their code (see 3.2) |

## 3. Confirmed technical problems and corrections

### 3.1 Notebook 06: variable shadowing breaks top-to-bottom execution (fixed)

Cell 13 contained `for a, b in zip(r1, r2):`. This overwrote the 7×7 test grid `b` defined in cell 11. Cell 32 later calls `update_correlated_life(b, ...)` and fails with `AxisError`. In the uploaded notebook cell 13 had never been executed, which hid the problem. The loop variables were renamed to `arr_1, arr_2`. No test or model logic was changed.

### 3.2 Notebook 06: stored outputs inconsistent with the code (resolved by re-execution)

* Cells 13, 15, 21 and 29 had no stored output. After re-execution, cell 21 prints the main-sweep table (all values agree with the plotted data). Cell 29 prints that 0 of 12 runs went extinct within 150 and within 350 frames at μ = 0.02.
* Cell 49 showed the output `Tüm 12 koşul tamamlandı.` although its code prints one progress line per condition. The output therefore came from an earlier version of the code. Re-execution with the current code reproduces the 480-run CSV exactly, so the stored results were not affected.

### 3.3 Notebook 04: toad population (corrected in text)

The observation table and the results table state that the toad population varies "between 6 and 8". The population time series computed in the same notebook shows exactly 6 live cells in both phases. The text was corrected with a visible review note.

### 3.4 Notebook 02: factual and consistency issues (annotated, not changed)

* Answer 1 of "Interpret the figure" compares Rule 90 with "Rule 30" in the first sentence and with Rule 54 in the second. The numbers support the pair Rule 90 and Rule 54. A review note was added.
* Rule 126 is described as the "complement" of Rule 30. This is incorrect. The rules equivalent to Rule 30 under reflection and complementation are 30, 86, 135 and 149. A review note was added.
* The Rule 90 row of the initial-condition table had an extra column, which broke the Markdown table. The content was merged into the correct column.
* The provisional class labels for Rules 4, 54, 60, 90 and 150 differ from the usual Wolfram assignments (4: II, 54: IV, 60/90/150: III for random initial conditions). These are the student's own provisional labels and were kept, with a note.

### 3.5 Minor issues (documented only)

* Notebook 01, cell 30: the plot of the number of occupied cells was titled "activity". The English title now describes what is plotted.
* Notebook 01, observation table: the text says the numbers were measured with analysis code in the next cell, but that cell only draws the plot. The numbers were spot-checked and are consistent with the space-time diagrams.
* Notebook 03, Section 7: the shaded band uses `np.std` with `ddof=0` (population SD). With M = 10 this underestimates the sample SD by about 5%. No conclusion depends on it.
* Notebook 04, Markdown: some equations used the broken delimiter `\$$[ ... \]$$` and did not render. They were rewritten as `$$ ... $$`.
* Notebook 05: the claimed maximum of the late-time density at p = 0.20 (0.07247) is not distinguishable from the value at p = 0.50 (0.07218). The standard error of each mean is about 0.004. A review note was added. The full 19-row table is in `results/nb05_main_sweep_table.csv`.

## 4. Verification of the stochastic model (notebook 06)

### 4.1 Model definition as implemented

At every step the standard B3/S23 rule is applied on an L × L torus, giving F(G). A mortality mask is then drawn on **all** sites and every live cell of F(G) that lies on a marked site is removed. Newly born cells are therefore also exposed to mortality in the same step.

* **Independent model:** sites are marked i.i.d. with probability μ.
* **Clustered model:** a white Gaussian field is smoothed with a periodic Gaussian kernel of width σ (`scipy.ndimage.gaussian_filter`, `mode="wrap"`). It is rescaled to unit variance using the exact discrete kernel norm and mapped to Uniform(0, 1) with the normal CDF. A site is marked when the value is below μ. The marginal marking probability is exactly μ by construction.

The implementation in `analysis/ca_engine.py` reproduces both notebook models **bit for bit** for the same seed (`analysis/tests/test_engine.py`, 6 tests, all passing). The numba Life step is checked against the `np.roll` implementation of notebook 04 on square and rectangular grids.

### 4.2 Matching of the two models (Experiment B)

* Marginal marking probability (2,000 masks per setting, 60 × 60): independent 0.00503 ± 0.00003, clustered (σ = 2) 0.00491 ± 0.00009 for μ = 0.005. Clustered 0.02016 ± 0.00022 for μ = 0.02 and 0.10017 ± 0.00056 for μ = 0.1. All agree with μ within about 1.5 standard errors (`results/mask_statistics.csv`).
* **Observed mortality fraction during the dynamics.** The fraction of cells alive after the Life step that were removed by mortality (pooled over all steps and runs, denominator = live cells after the Life step) is between 0.985 μ and 1.026 μ for all 33 (model, μ) conditions of the sweep (`results/tables/expA_B_E_sweep_summary.csv`, column `kill_ratio`). The two models are therefore matched in expected mortality intensity both per site and per live cell.
* The models are **not** matched in the step-to-step variance of the number of marks. For μ = 0.02 on 60 × 60, the SD of the marked fraction per step is 0.0023 (independent) and 0.0098 (clustered, σ = 2). This is an unavoidable consequence of spatial correlation. It motivated the control model below.

### 4.3 Control model for the attribution to spatial correlation

To test whether the faster extinction under clustered mortality is caused by the spatial arrangement of deaths or merely by larger fluctuations in their total number, a **fluctuation control** (`global_fluct`) was added. At each step a clustered field is drawn only to obtain its realised marked fraction m_t, and sites are then marked i.i.d. with probability m_t. This reproduces the per-step fluctuations of the clustered model (SD 0.0101 versus 0.0098 at μ = 0.02) while removing the spatial correlation (conditional neighbour marking probability 0.025 versus 0.668).

## 5. Experiments

All runs use L = 60, p0 = 0.35, T = 3000 updates and M = 40 independent realisations unless stated otherwise. Initial grids depend only on (experiment, L, p0, replicate), so all mortality models and rates see the same initial grids. Seeds are written to every CSV row.

### Experiment A: independent mortality sweep

Twelve values μ ∈ {0, 0.001, 0.002, 0.003, 0.005, 0.0075, 0.01, 0.015, 0.02, 0.03, 0.05, 0.1}, three models, 1,360 runs (`results/sweep_runs.csv`).

* Mean and SD of the late-time density and activity are reported for windows ending at T = 800 (the notebook 06 protocol, W = 160) and T = 3000 (W = 50, 160 and 500).
* **Window length:** at T = 3000, changing W from 50 to 500 changes the mean late density by less than 5% except near μ = 0.01, where it changes by about 15% because some runs are still declining. No qualitative conclusion depends on the window.
* **Temporal versus realisation variation:** for the independent model at μ = 0.005, the mean within-run temporal SD of ρ over the last 50 steps is 0.00011, while the SD of the window means across 40 runs is 0.0026. The dominant variability is between realisations, not in time.
* Independent model, T = 3000: no extinction for μ ≤ 0.005 (0/40 each), 4/40 at μ = 0.0075, 6/40 at μ = 0.01, 31/40 at μ = 0.015, 39/40 at μ = 0.02 and 40/40 for μ ≥ 0.03.
* The notebook 06 main-sweep numbers (T = 800, M = 16) fall within the ranges of the new runs. For example the late density at μ = 0.005 is 0.0099 in notebook 06 and 0.0101 ± 0.0051 (mean ± SD, M = 40) here.

### Experiment B: mortality fraction

See Section 4.2. The observed kill fraction equals μ within sampling error in all models.

### Experiment C: system size

L ∈ {40, 60, 80, 100, 140, 200}, μ ∈ {0.005, 0.02}, independent and clustered, M = 40, 960 runs (`results/tables/expC_size_summary.csv`).

* At μ = 0.005 the difference between the models is present at every L. Clustered: 40/40 extinct by T = 3000 at every L. Independent: 0/40 extinct for L ≥ 60 (2/40 at L = 40).
* Median extinction times increase with L in both models (clustered μ = 0.005: 647 at L = 40 to 1,335 at L = 200. Independent μ = 0.02: 767 to 2,426). The bootstrap 95% intervals of neighbouring sizes often overlap, but the increase from L = 40 to L = 200 is well outside sampling noise.
* At μ = 0.02 and L = 200 the independent model is 31/40 extinct by T = 3000 here, compared with 20/20 in notebook 06 (Fisher exact p = 0.023). Because this difference is nominally significant, it was investigated. (a) Running notebook 06's own seeds through the review engine reproduces its extinction times exactly (40 of 40 runs checked), so both codes implement the same model. (b) 40 additional runs with notebook 06's seed formula (replicates 20 to 59) gave 36/40 extinct, with 4 runs surviving to step 3000. The notebook 06 result of 20/20 is therefore a chance outcome of a condition in which the median extinction time (about 2,400 steps) lies close to the 3000-step cutoff. The statement in notebook 06 that all runs at μ = 0.02 had died out by step 3000 is true for its 20 runs but should not be generalised. Pooled over L = 60, 80, 100 and 200, this review finds 149/160 runs extinct by step 3000.
* The data are consistent with an extinction time that grows slowly (roughly logarithmically) with the number of sites. This was **not** fitted or tested formally and no scaling law is claimed.

### Experiment D: initial conditions

* p0 ∈ {0.20, 0.35, 0.50} at μ ∈ {0.005, 0.02}: the extinction fractions are unchanged (independent μ = 0.005: 0/40 for every p0. Clustered μ = 0.005: 40/40 for every p0).
* Variance decomposition with 12 initial grids × 12 dynamics seeds per condition: the fraction of variance attributable to the initial grid (intraclass correlation) is between 0 and 0.07 for the late density and the extinction time. One of six tests gives p = 0.039 and none survives a correction for multiple testing. Within this design, outcome variability is dominated by the random mortality draws rather than by the initial grid.

### Experiment E: long-time behaviour

Operational labels (`analysis/experiments.py`, functions `classify` and `config_label`):

* **extinct** if ρ(t) = 0 for some t ≤ 3000
* for μ = 0, the full trajectory is hashed and the first exact recurrence of the whole grid gives **static** (period 1) or **periodic** (period > 1, including gliders crossing the torus)
* for μ > 0, the configurations at t = 2700 and t = 3000 are each evolved without noise. **static** or **periodic** means the noise-free continuation settles within 30 steps onto an exact cycle, **active** means it does not. If the labels at 2700 and 3000 differ the run is **uncertain**.

Results (L = 60): at μ = 0, 39/40 runs reached an exact periodic state within 3000 steps (mostly blinkers in a still-life background) and 1/40 showed no recurrence. For every surviving independent run with μ ≥ 0.002 the label is **static**, meaning that the surviving populations are still-life ash (blocks, beehives and similar) that is occasionally damaged and repaired. Oscillators did not persist under mortality. A survival label at T = 3000 is not evidence of indefinite survival. Section 4 of notebook 06 explains correctly that extinction is certain in the infinite-time limit for any μ > 0 on a finite grid.

### Experiment F: spatially correlated mortality

1. **Fluctuation control** (Experiment A data). At μ = 0.005 the control behaves like the independent model (0/40 extinct, versus 40/40 clustered). At μ = 0.01 it gives 13/40, versus 6/40 independent and 40/40 clustered. The large effect of clustering at low μ is therefore **not** explained by fluctuations in the total number of deaths.
2. **σ dependence** (σ ∈ {1, 2, 4}, μ ∈ {0.002, 0.005, 0.01, 0.02}, 960 runs). Clustered mortality causes complete extinction at μ ≥ 0.005 for all three widths. The fluctuation control approaches the clustered result only for σ = 4 at μ ≥ 0.01 (36/40), where the per-step variance of the death count is largest. At σ = 4 fluctuations therefore contribute substantially, while at σ ≤ 2 and μ ≤ 0.005 they do not.
3. **Mechanism check** (isolated objects on a 32 × 32 torus, 400 runs per condition). A block that loses one cell is restored by the Life rule in the next step. It dies only if two or more of its cells are removed in the same step. Under independent mortality at μ = 0.005, 252/400 blocks survived 3000 steps. Under clustered mortality the median block lifetime was 124 steps. Fragile objects that die from a single hit (beehive, blinker) instead live slightly **longer** under clustered mortality (median 63 versus 26 steps for the beehive), because clustered marks hit fewer distinct objects per step. Combined with Experiment E (surviving populations consist of still lifes), this supports, but does not prove, the explanation that **clustered deaths defeat the self-repair of still lifes** such as blocks.

## 6. Points that remain open

* A preliminary literature search (15 November 2026) found stochastic Game of Life variants with site-independent noise only, and found that the general effect of spatially aggregated disturbance on extinction is known in spatial ecology (Kallimanis et al. 2005, Liao et al. 2015). The search was not systematic.
* The extinction-time growth with L was not fitted. A formal analysis would need larger M and more sizes.
* The control model removes spatial correlation but keeps the temporal fluctuation of the global rate. Other controls (for example matching the number of distinct objects hit) were not tried.
* The 30-step settling threshold and the 300-step comparison interval in Experiment E are operational choices. Their influence was not studied systematically.
