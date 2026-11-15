"""Checks that the analysis engine reproduces the notebook implementations exactly.

Run with:  python -m pytest analysis/tests -q
"""
import sys
from pathlib import Path

import numpy as np
from scipy.ndimage import gaussian_filter
from scipy.special import ndtr

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import ca_engine as E  # noqa: E402


# --- copies of the notebook 06 functions (unchanged logic) -------------------
def nb_update_life(grid):
    return E.life_step_roll(grid)


def nb_apply_random_death(grid, mu, rng):
    draws = rng.random(grid.shape)
    return ((grid == 1) & (draws >= mu)).astype(np.uint8)


def nb_simulate_noisy_life(initial, steps, mu, rng):
    h = np.zeros((steps, *initial.shape), dtype=np.uint8)
    h[0] = initial
    for t in range(1, steps):
        h[t] = nb_apply_random_death(nb_update_life(h[t - 1]), mu, rng)
    return h


def nb_correlated_death_mask(shape, mu, sigma, rng):
    noise = rng.standard_normal(shape)
    field = gaussian_filter(noise, sigma=sigma, mode="wrap")
    w = np.zeros(shape)
    w[0, 0] = 1
    k = gaussian_filter(w, sigma=sigma, mode="wrap")
    field = field / np.sqrt(np.sum(k ** 2))
    return ndtr(field) < mu


def nb_simulate_correlated(initial, steps, mu, sigma, rng):
    h = np.zeros((steps, *initial.shape), dtype=np.uint8)
    h[0] = initial
    for t in range(1, steps):
        nxt = nb_update_life(h[t - 1])
        nxt[nb_correlated_death_mask(initial.shape, mu, sigma, rng)] = 0
        h[t] = nxt
    return h


# --- tests -------------------------------------------------------------------
def test_life_step_matches_roll_square_and_rectangular():
    rng = np.random.default_rng(0)
    for shape in [(5, 5), (8, 12), (60, 60), (40, 90)]:
        for _ in range(20):
            g = (rng.random(shape) < rng.random()).astype(np.uint8)
            assert np.array_equal(E.life_step(g), E.life_step_roll(g))


def test_known_patterns():
    blk = np.zeros((8, 8), np.uint8); blk[3:5, 3:5] = 1
    assert np.array_equal(E.life_step(blk), blk)
    bl = np.zeros((8, 8), np.uint8); bl[4, 3:6] = 1
    assert np.array_equal(E.life_step(E.life_step(bl)), bl)
    gl = np.zeros((20, 20), np.uint8)
    for r, c in [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]:
        gl[5 + r, 5 + c] = 1
    g = gl.copy()
    for _ in range(4):
        g = E.life_step(g)
    assert np.array_equal(g, np.roll(np.roll(gl, 1, 0), 1, 1))


def test_independent_model_is_bitwise_identical_to_notebook():
    init = E.random_grid((30, 30), 0.35, np.random.default_rng(5))
    for mu in (0.003, 0.02, 0.2):
        h = nb_simulate_noisy_life(init, 201, mu, np.random.default_rng(11))
        r = E.run(init, 200, mu, "independent", rng=np.random.default_rng(11),
                  stop_at_extinction=False)
        assert np.allclose(r["density"], h.mean(axis=(1, 2)))
        assert np.allclose(r["activity"], (h[1:] != h[:-1]).mean(axis=(1, 2)))


def test_clustered_model_is_bitwise_identical_to_notebook():
    init = E.random_grid((30, 30), 0.35, np.random.default_rng(6))
    for mu in (0.005, 0.05):
        h = nb_simulate_correlated(init, 151, mu, 2.0, np.random.default_rng(13))
        r = E.run(init, 150, mu, "clustered", sigma=2.0,
                  rng=np.random.default_rng(13), stop_at_extinction=False)
        assert np.allclose(r["density"], h.mean(axis=(1, 2)))


def test_limits():
    init = E.random_grid((20, 20), 0.35, np.random.default_rng(1))
    r0 = E.run(init, 30, 0.0, rng=np.random.default_rng(1))
    g = init.copy()
    for t in range(1, 31):
        g = E.life_step(g)
        assert np.isclose(r0["density"][t], g.mean())
    r1 = E.run(init, 5, 1.0, rng=np.random.default_rng(1))
    assert r1["tau"] == 1
    for model in ("independent", "clustered", "global_fluct"):
        r = E.run(init, 5, 1.0, model, rng=np.random.default_rng(1))
        assert r["tau"] == 1


def test_bookkeeping_consistency():
    init = E.random_grid((40, 40), 0.35, np.random.default_rng(3))
    for model in ("independent", "clustered", "global_fluct"):
        r = E.run(init, 300, 0.01, model, rng=np.random.default_rng(4),
                  stop_at_extinction=False)
        n = init.size
        post = r["alive_pre"] - r["killed"]
        assert np.allclose(post / n, r["density"][1:])
        assert np.all(r["killed"] <= r["marked"])
