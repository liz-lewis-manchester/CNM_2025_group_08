import numpy as np
from src.model import create_grid, advect

def test_decay():
    x = create_grid(5.0, 0.25, 40.0)

    theta_init = np.zeros_like(x)
    theta_init[0] = 100.0

    C_no_decay, _ = advect(theta_init, 0.1, 0.25, 5.0, 40.0, decay_k=0.0)
    C_decay, _ = advect(theta_init, 0.1, 0.25, 5.0, 40.0, decay_k=0.02)

    max_no = C_no_decay.max()
    max_yes = C_decay.max()

    assert max_yes <= max_no + 1e-6, "Error"
