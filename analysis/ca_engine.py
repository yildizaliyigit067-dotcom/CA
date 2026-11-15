"""Simulation engine for the stochastic Game of Life experiments.

This module re-implements, without changing the model, the update used in
``06_stochastic_life.ipynb``:

    G_{t+1} = D_mu( F_Life(G_t) )

1. ``F_Life`` is the standard B3/S23 rule on an L x L periodic (toroidal) grid.
2. ``D_mu`` removes cells after the Life step.  A site is marked for removal
   with marginal probability ``mu``.  Marks on dead sites have no effect, so in
   practice each cell that is alive after the Life step is removed with
   probability ``mu``.

Mortality models
----------------
``independent``  marks are i.i.d. Bernoulli(mu) at every site and step
                 (identical to ``apply_random_death`` in notebook 06).
``clustered``    a white Gaussian field is smoothed with a periodic Gaussian
                 kernel of width ``sigma``, rescaled to unit variance and mapped
                 to Uniform(0, 1) with the normal CDF.  A site is marked when the
                 uniform value is below ``mu`` (identical to
                 ``correlated_death_mask`` in notebook 06).  The marginal mark
                 probability is exactly ``mu`` but marks are spatially correlated.
``global_fluct`` control model added in this review.  At each step a clustered
                 field is drawn only to obtain its realised mark fraction m_t.
                 Marks are then placed i.i.d. with probability m_t.  This keeps
                 the step-to-step fluctuations in the total number of marks of
                 the clustered model but removes the spatial correlation.

The Life step is compiled with numba when available.  It is checked against the
``np.roll`` implementation of notebook 04 in ``tests/test_engine.py``.
"""
from __future__ import annotations

import numpy as np
from scipy.ndimage import gaussian_filter
from scipy.special import ndtr

try:
    from numba import njit
except ImportError:  # pragma: no cover
    def njit(*args, **kwargs):
        def deco(f):
            return f
        return deco


# ----------------------------------------------------------------------------
# Deterministic rule
# ----------------------------------------------------------------------------
@njit(cache=True)
def life_step(g):
    """One B3/S23 update on a periodic grid (rows and columns may differ)."""
    n, m = g.shape
    out = np.zeros_like(g)
    for i in range(n):
        im = (i - 1) % n
        ip = (i + 1) % n
        for j in range(m):
            jm = (j - 1) % m
            jp = (j + 1) % m
            c = (g[im, jm] + g[im, j] + g[im, jp] + g[i, jm] + g[i, jp]
                 + g[ip, jm] + g[ip, j] + g[ip, jp])
            if c == 3 or (c == 2 and g[i, j] == 1):
                out[i, j] = 1
    return out


def life_step_roll(grid):
    """Reference implementation copied from notebook 04 (np.roll)."""
    grid = np.asarray(grid, dtype=np.uint8)
    nb = np.zeros_like(grid, dtype=np.uint8)
    for di in (-1, 0, 1):
        for dj in (-1, 0, 1):
            if di == 0 and dj == 0:
                continue
            nb += np.roll(np.roll(grid, di, axis=0), dj, axis=1)
    birth = (grid == 0) & (nb == 3)
    survive = (grid == 1) & ((nb == 2) | (nb == 3))
    return (birth | survive).astype(np.uint8)


# ----------------------------------------------------------------------------
# Mortality masks
# ----------------------------------------------------------------------------
class MaskGenerator:
    """Generates mortality marks for one model on a fixed grid shape."""

    def __init__(self, shape, mu, model="independent", sigma=2.0):
        if not 0.0 <= mu <= 1.0:
            raise ValueError("mu must lie in [0, 1]")
        if model not in ("independent", "clustered", "global_fluct"):
            raise ValueError(model)
        self.shape = tuple(shape)
        self.mu = float(mu)
        self.model = model
        self.sigma = float(sigma)
        if model in ("clustered", "global_fluct"):
            if self.sigma <= 0:
                raise ValueError("sigma must be positive for correlated models")
            imp = np.zeros(self.shape)
            imp[0, 0] = 1.0
            k = gaussian_filter(imp, sigma=self.sigma, mode="wrap")
            self.norm = float(np.sqrt(np.sum(k * k)))

    def _clustered(self, rng):
        z = gaussian_filter(rng.standard_normal(self.shape), sigma=self.sigma,
                            mode="wrap") / self.norm
        return ndtr(z) < self.mu

    def __call__(self, rng):
        if self.mu == 0.0:
            return np.zeros(self.shape, dtype=bool)
        if self.mu == 1.0:
            return np.ones(self.shape, dtype=bool)
        if self.model == "independent":
            return rng.random(self.shape) < self.mu
        if self.model == "clustered":
            return self._clustered(rng)
        # global_fluct
        m_t = self._clustered(rng).mean()
        return rng.random(self.shape) < m_t


# ----------------------------------------------------------------------------
# Simulation
# ----------------------------------------------------------------------------
def random_grid(shape, p0, rng):
    return (rng.random(shape) < p0).astype(np.uint8)


def run(initial, T, mu, model="independent", sigma=2.0, rng=None,
        stop_at_extinction=True, keep_frames=()):
    """Run T updates of the stochastic Life model.

    Returns a dict of per-step series.  Index t of the length-(T+1) series refers
    to the state G_t, with G_0 the initial grid.  Length-T series refer to the
    transition G_{t-1} -> G_t for t = 1..T and are stored at index t-1.

    density[t]        fraction of live sites in G_t
    activity[t-1]     fraction of sites that differ between G_{t-1} and G_t
                      (same definition as notebooks 05 and 06; it includes
                      removals caused by mortality)
    rule_activity[t-1] fraction of sites changed by the Life rule alone,
                      i.e. F(G_{t-1}) != G_{t-1}
    alive_pre[t-1]    number of live cells in F(G_{t-1}) (before mortality)
    killed[t-1]       number of those cells removed by mortality
    marked[t-1]       number of sites marked by the mortality mask (all sites)

    After extinction the empty grid is absorbing, so remaining entries are
    filled with zeros (no further random numbers are drawn).
    """
    g = np.ascontiguousarray(initial, dtype=np.uint8).copy()
    n_sites = g.size
    gen = MaskGenerator(g.shape, mu, model, sigma)
    density = np.zeros(T + 1)
    activity = np.zeros(T)
    rule_activity = np.zeros(T)
    alive_pre = np.zeros(T, dtype=np.int64)
    killed = np.zeros(T, dtype=np.int64)
    marked = np.zeros(T, dtype=np.int64)
    density[0] = g.mean()
    tau = -1
    frames = {}
    if 0 in keep_frames:
        frames[0] = g.copy()
    for t in range(1, T + 1):
        f = life_step(g)
        mask = gen(rng)
        alive_pre[t - 1] = int(f.sum())
        kill = mask & (f == 1)
        killed[t - 1] = int(kill.sum())
        marked[t - 1] = int(mask.sum())
        rule_activity[t - 1] = np.count_nonzero(f != g) / n_sites
        f[kill] = 0
        activity[t - 1] = np.count_nonzero(f != g) / n_sites
        density[t] = f.mean()
        g = f
        if t in keep_frames:
            frames[t] = g.copy()
        if tau < 0 and density[t] == 0.0:
            tau = t
            if stop_at_extinction:
                break
    return dict(density=density, activity=activity, rule_activity=rule_activity,
                alive_pre=alive_pre, killed=killed, marked=marked, tau=tau,
                frames=frames)


def seed_for(*keys):
    """Deterministic RNG from a tuple of non-negative integers."""
    return np.random.default_rng(np.random.SeedSequence(list(keys)))
