import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
import os

def read_boundary_conditions(csv_file):

    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"The file {csv_file} does not exist.")

    try:
        df = pd.read_csv(csv_file, encoding="latin1")
        distances = df.iloc[:, 0].values
        concentrations = df.iloc[:, 1].values
        
        return distances, concentrations

    except Exception as e:
        raise RuntimeError(f"An error occurred while reading the file: {e}")

def interpolate_conditions(distances, concentrations, target_x, kind='linear'):
    interpolator = interp1d(distances, concentrations, kind=kind, fill_value="extrapolate")
    # Calculate interpolated concentrations
    new_concentrations = interpolator(target_x)
    return target_x, new_concentrations
def create_grid(L, dx, T, dt):
    # this creates spatial and temporal grids 
    
    if L <= 0 or dx <= 0 or dt <= 0 or T < 0:
        raise ValueError('Parameters are invalid')

    nx = int(L/dx) + 1  
    nt = int(T/dt) + 1

    x = np.linspace(0, L, nx)
    time_grid = np.linspace(0, T, nt)

    return x, time_grid  

def advect(theta_init, U, dx, dt, num_time_steps, decay_k=0.0):
    # Solves the advection equation using the first-order upwind scheme.
    # Calculate the CFL number which represents how much information travels across a grid cell in one time step.
    CFL = U * dt / dx
    max_CFL = 0.9   # we need to limit CFL to made each test conform to the laws of physics
    
    if CFL > max_CFL:
        dt_new = max_CFL * dx / U
        print(f"*** WARNING: CFL condition (U*dt/dx <= 1) violated (CFL={CFL:.2f}). Changing dt from {dt:.2f}s to {dt_new:.2f}s ***")
        dt = dt_new
        CFL = max_CFL
    num_points = len(theta_init)
    theta_current = theta_init.copy()

  
    theta_all = np.zeros((len(num_time_steps), num_points))
    theta_all[0, :] = theta_init

    for n in range(len(num_time_steps) - 1):  
        # Calculate the spatial difference 
        d_theta = -CFL * (theta_current[1:] - theta_current[:-1])

        theta_next = theta_current.copy()
        theta_next[1:] = theta_current[1:] + d_theta
        
        # Boundary condition: Set Left side boundary to 0.
        theta_next[0] = theta_init[0]
        
        theta_next = theta_next * np.exp(-decay_k * dt)
        
        # Progress to next step.
        theta_current = theta_next
        theta_all[n + 1, :] = theta_current

    return theta_all
