# Emergent Complexity in Cellular Automata

This is a high-school research project about cellular automata: simple grids of cells that follow simple rules but can still produce complex patterns.

The project was done as a summer project supervised by Prof. Levent Subaşı (Istanbul Technical University). It is still in progress and has **not** been peer reviewed or published. The notebooks were first written in Turkish and translated into English in November 2026. The repository is a fork of `subasilevent/CA`.

## The main question

In Conway's Game of Life, each cell lives or dies depending on its eight neighbours. In this project, an extra rule is added: after every step, each live cell dies at random with probability $\mu$.

The question is:

> If every cell has the same chance of dying, does it matter **where** the deaths happen?

Two cases are compared:

* **Independent deaths:** every cell dies on its own, with probability $\mu$.
* **Clustered deaths:** cells close to each other tend to die together. Each cell still dies with the same probability $\mu$.

## What was found

All results below are for a $60 \times 60$ grid (unless stated otherwise), starting with 35% of cells alive, and watched for up to 3000 steps.

1. **Same chance of death, very different result.** At $\mu = 0.005$, none of 40 runs with independent deaths died out. With clustered deaths, all 40 runs died out (typically after about 840 steps). This was also true for grid sizes from 60 to 200 and for different starting densities.
2. **The death rate really is the same.** In both cases, the fraction of live cells that die each step matches $\mu$ (within about 3%). So the difference is not because one model kills more cells.
3. **It is the location of deaths that matters.** A test model that has the same ups and downs in the number of deaths, but with no clustering, behaves like the independent model at low $\mu$.
4. **Why it happens: blocks repair themselves.** After a while, almost everything left alive is a 2×2 "block" (93% of objects). If a block loses one cell, the Game of Life rules rebuild it in the next step. It only dies if two or more of its cells die at the same time. Clustered deaths often hit several cells of a block at once, so blocks cannot repair themselves. A simple formula based on this idea predicts the block lifetimes in the simulations very closely.
5. **Bigger grids take longer to die out**, in both models.

The early weeks (1 to 5) also reproduce known results, for example the Rule 90 formula $N_1(t) = 2^{\mathrm{popcount}(t)}$ and the glider speed of 1/4 cell per step.

More details are in the report: [`report/report.pdf`](report/report.pdf).

## Files

| File or folder | What it contains |
|---|---|
| `01_elementary_CA.ipynb` | Week 1: one-dimensional cellular automata (rules 0, 30, 90, 110) |
| `02_rule_classification.ipynb` | Week 2: all 256 rules and Wolfram's four classes |
| `03_sensitivity.ipynb` | Week 3: how a one-cell change spreads |
| `04_game_of_life.ipynb` | Week 4: Game of Life, still lifes, oscillators and gliders |
| `05_random_initial_conditions.ipynb` | Week 5: random starting grids and averages over many runs |
| `06_stochastic_life.ipynb` | Week 6: random deaths, independent versus clustered |
| `analysis/` | Code for the extra experiments, figures and tests |
| `results/` | Data from all experiments (CSV files) |
| `figures/` | Figures used in the report |
| `report/` | The report (PDF and LaTeX source) |
| `AI_NOTES.md` | How AI tools were used in the project |
| `VALIDATION_REPORT.md` | Summary of how the results were checked |
| `CHANGELOG.md` | List of changes made during the November 2026 review |

## How to run it

```bash
git clone https://github.com/yildizaliyigit067-dotcom/CA.git
cd CA
pip install -r requirements.txt
```

Then open any notebook in Jupyter or Google Colab and run it from top to bottom. Each notebook works on its own.

To repeat the extra experiments and make the figures (about 25 minutes):

```bash
python -m pytest analysis/tests -q
python analysis/experiments.py all
python analysis/make_figures.py
```

All random numbers use fixed seeds, so the results come out the same every time.

Open in Colab:
[01](https://colab.research.google.com/github/yildizaliyigit067-dotcom/CA/blob/main/01_elementary_CA.ipynb) ·
[02](https://colab.research.google.com/github/yildizaliyigit067-dotcom/CA/blob/main/02_rule_classification.ipynb) ·
[03](https://colab.research.google.com/github/yildizaliyigit067-dotcom/CA/blob/main/03_sensitivity.ipynb) ·
[04](https://colab.research.google.com/github/yildizaliyigit067-dotcom/CA/blob/main/04_game_of_life.ipynb) ·
[05](https://colab.research.google.com/github/yildizaliyigit067-dotcom/CA/blob/main/05_random_initial_conditions.ipynb) ·
[06](https://colab.research.google.com/github/yildizaliyigit067-dotcom/CA/blob/main/06_stochastic_life.ipynb)

## Limitations

* The grids are finite (at most $200 \times 200$) and the runs are finite (at most 3000 steps). A run that survives 3000 steps would still die out eventually.
* Most results use 40 runs per setting, so the percentages have some uncertainty.
* Only one kind of clustering (a Gaussian blur) was tested.
* The search for earlier studies was short. The general idea that clustered disasters are more dangerous is already known in ecology, so the new part here is the Game of Life case and the block-repair explanation.

## Status

* Weeks 1 to 6: finished, translated and checked.
* Report: ready for review by the supervisor.

## Acknowledgments

The weekly assignments and notebook templates were provided by Prof. Levent Subaşı (Istanbul Technical University). AI tools (Claude and ChatGPT) were used as described in `AI_NOTES.md`. The English translation, the extra experiments in `analysis/` and the report were prepared with the help of Claude (Anthropic) in November 2026.
