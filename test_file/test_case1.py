import numpy as np
import os
from src.model import (create_grid, advect)
def test_case1_run():
    x = create_grid(20.0, 0.2, 300.0)
    dt = 10.0
    theta_init = np.zeros_like(x)
    theta_init[0] = 250.0  # pulse at left

    U = 0.1

    C_hist, time_grid = advect(theta_init, U, 0.2, dt, 300.0)

    assert C_hist.shape == (len(time_grid), len(x))

    assert C_hist.min() >= -1e-6
