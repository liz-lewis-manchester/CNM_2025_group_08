import numpy as np
import os
from src.model import (create_grid, advect)
def test_case1_run():
    x = create_grid(20.0, 0.2, 300.0)
    dt = 10.0
    theta_init = np.zeros_like(x)
    theta_init[0] = 250.0  # pulse at left

    U = 0.1

    C_hist, time_grid = advect(theta_init, U, 0.2, dt, T)

    assert C_hist.shape == (len(t), len(x))

    assert C_hist.min() >= -1e-6

import numpy as np
import os
from src.model import (read_boundary_conditions, interpolate_conditions,
    create_grid)

def test_case2_csv():
    x = create_grid(2.0, 0.2, 10.0)

    x_raw = np.array([0.0, 0.5, 1.0, 1.5, 2.0])
    C_raw = np.array([5.0, 10.0, 8.0, 6.0, 3.0])

    df = pd.DataFrame({"x": x_raw, "C": C_raw})
    csv_path = "initial_conditions.csv"
    df.to_csv(csv_path, index=False)
try:
    dist, conc = read_boundary_conditions(csv_path)
    _, theta_init = interpolate_conditions(dist, conc, target_x=x, kind='linear')
    theta_init = np.array(theta_init)

    assert len(theta_init) == len(x)
    # values should not explode
    assert theta_init.min() >= 0.0


def test_decay():
    x, t = create_grid(5.0, 0.25, 40.0, 5.0)

    theta_init = np.zeros_like(x)
    theta_init[0] = 100.0

    C_no_decay = advect(theta_init, 0.1, 0.25, 5.0, t, 0.0)
    C_decay = advect(theta_init, 0.1, 0.25, 5.0, t, 0.02)

    max_no = C_no_decay.max()
    max_yes = C_decay.max()

    assert max_yes <= max_no + 1e-6

def test_param_sensitivity():
    x, time_grid = create_grid(20.0, 0.2, 300.0, 10.0)
    theta_init = np.zeros_like(x)
    theta_init[0] = 250.0

 #test different U value
    C_hist_slow = advect(theta_init, 0.05, 0.2, 10.0, time_grid)
    C_hist_normal = advect(theta_init, 0.1, 0.2, 10.0, time_grid)
    C_hist_fast = advect(theta_init, 0.15, 0.2, 10.0, time_grid)
    assert C_hist_slow.shape == (len(time_grid), len(x))
    assert C_hist_normal.shape == (len(time_grid), len(x))
    assert C_hist_fast.shape == (len(time_grid), len(x))

#test different dx
   x_dx1, time_grid_dx1 = create_grid(20.0, 0.1, 300.0, 10.0)
   theta_init_dx1 = np.zeros_like(x_dx1)
   theta_init_dx1[0] = 250.0
   C_hist_dx1 = advect(theta_init_dx1, 0.1, 0.1, 10.0, time_grid_dx1)
   assert C_hist_dx1.shape == (len(time_grid_dx1), len(x_dx1))

   x_dx2, time_grid_dx2 = create_grid(20.0, 0.5, 300.0, 10.0)
   theta_init_dx2 = np.zeros_like(x_dx2)
   theta_init_dx2[0] = 250.0
   C_hist_dx2 = advect(theta_init_dx2, 0.1, 0.5, 10.0, time_grid_dx2)
   assert C_hist_dx2.shape == (len(time_grid_dx2), len(x_dx2))

# test differen dt
   x_dt1, time_grid_dt1 = create_grid(20.0, 0.2, 300.0, 5.0)
   theta_init_dt1 = np.zeros_like(x_dt1)
   theta_init_dt1[0] = 250.0
   C_hist_dt1 = advect(theta_init_dt1, 0.1, 0.2, 5.0, time_grid_dt1)
   assert C_hist_dt1.shape == (len(time_grid_dt1), len(x_dt1))
  
   x_dt2, time_grid_dt2 = create_grid(20.0, 0.2, 300.0, 20.0)
   theta_init_dt2 = np.zeros_like(x_dt2)
   theta_init_dt2[0] = 250.0
   C_hist_dt2 = advect(theta_init_dt2, 0.1, 0.2, 20.0, time_grid_dt2)
   assert C_hist_dt2.shape == (len(time_grid_dt2), len(x_dt2))

def test_variable_velocity():
    x, time_grid = create_grid(20.0, 0.2, 300.0, 10.0)
    U_mean = 0.1  

  #add 10%
    U_variable = U_mean * (1 + 0.1 * (np.random.rand(len(x)) - 0.5) * 2)
    theta_init = np.zeros_like(x)
    theta_init[0] = 250.0  
    C_hist_var = advect(theta_init, U_variable, 0.2, 10.0, time_grid)
    assert C_hist_var.shape == (len(time_grid), len(x))
    assert C_hist_var.min() >= -1e-6  
