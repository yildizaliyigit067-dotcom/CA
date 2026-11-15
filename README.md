# Emergent Complexity in Cellular Automata

A computational study, carried out by a high-school student, of how simple local update rules produce complex large-scale behaviour. The project ends with a stochastic version of Conway's Game of Life in which live cells die at random after every update. The main question is whether the **spatial arrangement** of these deaths, and not only their probability, changes the long-time fate of the system.

> **Status:** research in progress. This repository contains weekly notebooks prepared in a summer project supervised by Levent Hoca (Istanbul Technical University) and an accompanying technical report prepared for his review. The work has **not** been peer reviewed or published. The notebooks were originally written in Turkish and were translated into English in November 2026.

The repository was originally forked from `subasilevent/CA`.

## Research objectives

1. Implement elementary cellular automata (ECA) and Conway's Game of Life from first principles and verify them against known patterns.
2. Describe large-scale behaviour with measurable observables (density, activity, Hamming distance, perturbation radius) instead of visual impressions alone.
3. Use ensembles of random initial conditions to distinguish typical behaviour from individual trajectories.
4. Add random mortality to the Game of Life and compare **independent** deaths with **spatially clustered** deaths that have the same per-cell probability.

## Scientific background (short)

An elementary cellular automaton updates a ring of 0/1 cells synchronously using the states of each cell and its two nearest neighbours. There are 256 such rules, which Wolfram grouped into four qualitative classes. Conway's Game of Life is a two-dimensional automaton with the rule B3/S23 (birth with exactly 3 live neighbours, survival with 2 or 3). From random initial states it typically settles into a sparse "ash" of still lifes and oscillators. The stochastic model studied here applies the deterministic Life step and then removes each live cell with probability μ. The empty grid is absorbing, so on a finite grid every run with μ > 0 eventually dies out. The question is how quickly, and how this depends on the way deaths are distributed in space.

## Computational methodology

* Periodic (toroidal) boundaries in all simulations.
* Random initial grids with each cell alive independently with probability p (ECA) or p0 (Life).
* Observables: density ρ(t), activity a(t) (fraction of cells that change between steps), first extinction time τ, Hamming distance D(t) and radius R(t) for perturbations.
* Stochastic model: G(t+1) = D_μ(F_Life(G(t))). Independent mortality marks every site i.i.d. with probability μ. Clustered mortality thresholds a Gaussian-smoothed random field (width σ) that has been mapped to Uniform(0, 1), so every site is still marked with probability exactly μ but marks are spatially correlated.
* All experiments use explicit seeds (`numpy.random.default_rng` or `SeedSequence`), repeated independent realisations, and report mean, standard deviation and, where relevant, standard errors and 95% confidence intervals.

## Repository structure

```
01_elementary_CA.ipynb              Week 1: ECA engine, rules 0, 30, 90, 110, N1(t) = 2^popcount(t) for Rule 90
02_rule_classification.ipynb        Week 2: all 256 rules, Wolfram classes, density and activity
03_sensitivity.ipynb                Week 3: perturbation spreading, Hamming distance, light cone, Rule 90 linearity
04_game_of_life.ipynb               Week 4: B3/S23 engine, still lifes, oscillators, glider velocity
05_random_initial_conditions.ipynb  Week 5: ensembles over the initial density p, birth probability q, grid shape
06_stochastic_life.ipynb            Week 6: random mortality, independent versus clustered deaths, L up to 200, T = 3000
analysis/                           Review code: engine, experiments A to F, figures, tests, cross-checks
results/                            CSV output of all experiments, summary tables, environment record
figures/                            Figures used in the technical report
report/                             LaTeX source and PDF of the technical report
AI_NOTES.md                         Record of AI assistance
VALIDATION_REPORT.md                What was checked, what was corrected, what remains open
CHANGELOG.md                        Changes made on the review branch
requirements.txt                    Python dependencies
```

The notebooks are numbered in the order in which they should be read. Each notebook runs on its own from top to bottom.

## Installation

```bash
git clone https://github.com/yildizaliyigit067-dotcom/CA.git
cd CA
python -m venv .venv && source .venv/bin/activate     # optional
pip install -r requirements.txt
```

Python 3.10 or newer is expected. The exact versions used for the stored outputs are listed in `results/environment.txt`. `numba` is optional. Without it, notebook 06 Section 10 and the `analysis/` code run more slowly.

## Reproducing the results

```bash
# notebooks (01 to 05 take under a minute each, 06 takes about 6 minutes on 2 cores)
jupyter nbconvert --to notebook --execute --inplace 06_stochastic_life.ipynb

# tests of the review engine against the notebook implementation
python -m pytest analysis/tests -q

# experiments A to F (about 20 minutes on 2 cores), then figures and tables
python analysis/experiments.py all
python analysis/make_figures.py
python analysis/nb05_table.py
python analysis/crosscheck_nb06.py
```

Every row of `results/*_runs.csv` records the seed keys of its initial grid and of its random dynamics, so any single run can be regenerated.

Notebooks can also be opened in Google Colab:

[01](https://colab.research.google.com/github/yildizaliyigit067-dotcom/CA/blob/main/01_elementary_CA.ipynb) ·
[02](https://colab.research.google.com/github/yildizaliyigit067-dotcom/CA/blob/main/02_rule_classification.ipynb) ·
[03](https://colab.research.google.com/github/yildizaliyigit067-dotcom/CA/blob/main/03_sensitivity.ipynb) ·
[04](https://colab.research.google.com/github/yildizaliyigit067-dotcom/CA/blob/main/04_game_of_life.ipynb) ·
[05](https://colab.research.google.com/github/yildizaliyigit067-dotcom/CA/blob/main/05_random_initial_conditions.ipynb) ·
[06](https://colab.research.google.com/github/yildizaliyigit067-dotcom/CA/blob/main/06_stochastic_life.ipynb)

## Main findings (verified by re-execution)

These statements hold for the parameters stated (p0 = 0.35, periodic L × L grid, observation up to 3,000 updates). They are not claims about infinite systems or infinite times.

1. **Same probability, different fate.** At μ = 0.005 and L = 60, no run with independent mortality died out within 3,000 steps (0/40), whereas every run with clustered mortality (σ = 2) did (40/40, median extinction time 841 steps). The same contrast holds for every lattice size tested from L = 60 to L = 200, and for initial densities p0 = 0.20, 0.35 and 0.50.
2. **The models are matched in mortality intensity.** In both models the realised fraction of live cells removed per step equals μ within about 3%. The difference is therefore not caused by a stronger average mortality.
3. **Spatial correlation, not only fluctuations, is responsible at low μ.** A control model with the same step-to-step fluctuations in the number of deaths as the clustered model, but without spatial correlation, behaves like the independent model at μ ≤ 0.005 (0/40 extinct). For the widest kernel tested (σ = 4) and μ ≥ 0.01, fluctuations alone do account for much of the extra extinction.
4. **A likely mechanism.** At μ > 0 the surviving populations consist of still lifes. An isolated 2 × 2 block repairs the loss of one cell in a single Life step. Under independent mortality at μ = 0.005, 63% of isolated blocks survive 3,000 steps, while under clustered mortality their median lifetime is 124 steps. This supports, but does not prove, the explanation that clustered deaths defeat self-repair.
5. **Extinction times grow with system size.** Median extinction times increase from L = 40 to L = 200 in both models. No scaling law is claimed.
6. **Earlier weeks.** The Rule 90 formula N1(t) = 2^popcount(t), the light-cone bound R(t) ≤ t, the exact linearity test for Rule 90, the glider velocity of 1/4 cell per step and the non-monotonic dependence of the late-time Life density on the initial density all reproduce exactly.

Details, uncertainties and corrections are in `VALIDATION_REPORT.md` and in the technical report in `report/`.

## Limitations

* Finite grids (L ≤ 200) and finite observation times (T ≤ 3,000). Survival up to T is not survival forever.
* Forty realisations per condition in most experiments. Extinction fractions carry 95% confidence intervals of up to about ±0.15.
* One functional form of spatial correlation (Gaussian kernel) and three widths.
* Long-time behaviour is classified with explicit but operational criteria (see `VALIDATION_REPORT.md`, Experiment E).
* The literature comparison is preliminary. No Game of Life study with spatially correlated mortality was found, but the general effect (clustered disturbances raise extinction risk) is known from spatial ecology, for example Kallimanis et al., *Conservation Biology* 19, 534 (2005). See the Discussion of the report.

## Research status

* Weekly notebooks 1 to 6: complete, translated, re-executed and verified.
* Technical report for supervisor review: prepared (`report/`). Not yet reviewed.
* Week 7 investigation (dependence on the filter width σ): a preliminary version appears in the report as Experiment F.

## Acknowledgments

The weekly assignments and notebook templates were provided by Levent Hoca (Istanbul Technical University), who supervises the project. AI tools (Claude and ChatGPT) were used as described in `AI_NOTES.md`. The English translation, the verification experiments in `analysis/` and the technical report were prepared with the help of Claude (Anthropic) during a review session in November 2026.
