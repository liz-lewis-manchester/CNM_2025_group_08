import numpy as np
from src.model import create_grid, advect

def test_variable_velocity():
    x = create_grid(20.0, 0.2, 300.0)
    U_mean = 0.1  

  #add 10%
    U_variable = U_mean * (1 + 0.1 * (np.random.rand(len(x)) - 0.5) * 2)
    theta_init = np.zeros_like(x)
    theta_init[0] = 250.0  
    C_hist_var, _ = advect(theta_init, U_variable, 0.2, 10.0, 300.0)
    assert C_hist_var.shape == (len(_), len(x)),"Error"
    assert C_hist_var.min() >= -1e-6, "the result be negative"
