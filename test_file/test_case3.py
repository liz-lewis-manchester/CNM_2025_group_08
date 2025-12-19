import numpy as np
import os
from src.model import create_grid, advect

def test_param_sensitivity():
    x = create_grid(20.0, 0.2, 300.0)
    theta_init = np.zeros_like(x)
    theta_init[0] = 250.0

 #test different U value
    C_hist_slow, time_grid = advect(theta_init, 0.05, 0.2, 10.0, 300.0)
    C_hist_normal, time_grid = advect(theta_init, 0.1, 0.2, 10.0, 300.0)
    C_hist_fast, time_grid = advect(theta_init, 0.15, 0.2, 10.0, 300.0)
    assert C_hist_slow.shape == (len(time_grid), len(x)), "Error when U=0.05"
    assert C_hist_normal.shape == (len(time_grid), len(x)), "Error when U=0.1"
    assert C_hist_fast.shape == (len(time_grid), len(x)), "Error when U=0.15"

#test different dx
   x_dx1= create_grid(20.0, 0.1, 300.0)
   theta_init_dx1 = np.zeros_like(x_dx1)
   theta_init_dx1[0] = 250.0
   C_hist_dx1, time_grid_dx1 = advect(theta_init_dx1, 0.1, 0.1, 10.0, 300.0)
   assert C_hist_dx1.shape == (len(time_grid_dx1), len(x_dx1)), "Error when dx=0.1s"

   x_dx2 = create_grid(20.0, 0.5, 300.0)
   theta_init_dx2 = np.zeros_like(x_dx2)
   theta_init_dx2[0] = 250.0
   C_hist_dx2, time_grid_dx2 = advect(theta_init_dx2, 0.1, 0.5, 10.0, 300.0)
   assert C_hist_dx2.shape == (len(time_grid_dx2), len(x_dx2)),"Error when dx=0.5"

# test differen dt
   x_dt1 = create_grid(20.0, 0.2, 300.0)
   theta_init_dt1 = np.zeros_like(x_dt1)
   theta_init_dt1[0] = 250.0
   C_hist_dt1, time_grid_dt1 = advect(theta_init_dt1, 0.1, 0.2, 5.0, 300.0)
   assert C_hist_dt1.shape == (len(time_grid_dt1), len(x_dt1)), "Error when dt=5s"
  
   x_dt2 = create_grid(20.0, 0.2, 300.0)
   theta_init_dt2 = np.zeros_like(x_dt2)
   theta_init_dt2[0] = 250.0
   C_hist_dt2, time_grid_dt2 = advect(theta_init_dt2, 0.1, 0.2, 20.0, 300.0)
   assert C_hist_dt2.shape == (len(time_grid_dt2), len(x_dt2)), "Error when dt=20s"
