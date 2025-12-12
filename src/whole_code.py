import numpy as np
import panda as dp

csv_file = input("csv file")
L = input("length of river domain (m): ")
dx = input("change in space (m): ")
T = input("simulation time (s): ")
dt = input("change in time (s): ")

initial_concentration = pd.read_csv('csv_file')
# Distance (m) (not finish)
# Concentration (�g/m_ ) (not finish)

def create_grid(L, dx, T, dt):
    # this creates spatial and temporal grids 
    # L = length of river domain (m)
    # dx = change in space (m) 
    # T = simulation time (s)
    # dt = change in time (s) 

    if L <= 0 or dx <= 0 or dt <= 0 or T < 0:
        raise ValueError('Invalid grid parameters')

    nx = int(L/dx) + 1  
    nt = int(T/dt) + 1

    x = np.linspace(0, L, nx)
    t = np.linspace(0, T, nt)

    return x, t


def cfl_number(U, dx, dt):
    # this computes cfl number 
    if dx <= 0 or dt <= 0:
        raise ValueError('dx and dt must be positive')

    return U * dt / dx


def is_cfl_stable(U, dx, dt):
    # This checks the CFL stability condition
    return cfl_number(U, dx, dt) <= 1


--------------------- #SECOUND PART ------------------------

import numpy as np

def advect(theta_init, U, dx, dt, num_time_steps): 
    # Solves the advection equation using the first-order upwind scheme.
    # Calculate the CFL number which represents how much information travels across a grid cell in one time step.
    CFL = U * dt / dx

    # This is a stability check as upwind schemes require CFL <= 1 to remain numerically stable.
    if CFL > 1.0:
      print(f"*** WARNING: CFL condition (U*dt/dx <= 1) violated (CFL={CFL:.2f}). Solution is unstable. ***")

    num_points = len(theta_init)
    theta_current = theta_init.copy()

    # Initialise a 2D array to store the profile at every time step.
    theta_all = np.zeros((num_time_steps +1, num_points))
    theta_all[0, :] = theta_init

    for n in range(num_time_steps):
        # Calculate the spatial difference (Upwind: theta[i] - theta[i-1]).
        d_theta = -CFL * (theta_current[1:] - theta_current[:-1])

        # Update the profile for next time step.
        theta_next = theta_current.copy()
        theta_next[1:] = theta_current[1:] + d_theta

        # Boundary condition: Set LHS boundary to 0.
        theta_next[0] = 0.0

        # Progress to next step.
        theta_current = theta_next
        theta_all[n + 1, :] = theta_current

    return theta_all

def test_steady_advection_case():
    # Parameters for the simulation.
    U_test = 1.0 # Velocity.
    dx_test = 0.1 # Spatial Step.
    dt_test = 0.05 # Time Step.
    T_max_test = 1.0 # Total Simulation Time.

    # Determine total iterations.
    num_time_steps = int(T_max_test / dt_test)

    # Calculate initial condition.
    theta_init_test = np.full(int(1.0/0.1) + 1, 10.0)

    # Run the solver.
    theta_result = advect(theta_init_test, U_test, dx_test, dt_test, num_time_steps)

    assert np.allclose(theta_result[-1, :], 10.0, atol=1e-5), "Steady Advection test failed."
    print("Steady Advection test passed successfully (Result is approximately constant)>")



#----------THIRD-----------

import numpy as np
from data_handler import read_boundary_conditions, interpolate_conditions
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import pandas as pd
import os

def read_boundary_conditions(intial_conditions.csv):
    """
    Reads the initial boundary condition data from a CSV file.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        tuple: A tuple containing two numpy arrays:
               - distances (x coordinates)
               - concentrations (pollutant levels)
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    try:
        # Load data using pandas
        # Assuming the CSV has headers like 'Distance (m)' and 'Concentration (µg/m³)'
        # We use index_col=False to ensure we just get the columns as they are
        df = pd.read_csv(file_path)
        
        # Extract columns. We assume the first column is distance and second is concentration.
        # You might need to adjust column names based on the exact CSV format if headers differ.
        distances = df.iloc[:, 0].values
        concentrations = df.iloc[:, 1].values
        
        return distances, concentrations

    except Exception as e:
        raise RuntimeError(f"An error occurred while reading the file: {e}")

def interpolate_conditions(distances, concentrations, num_points=100, kind='linear'):
    """
    Interpolates the concentration data to a finer grid.

    Args:
        distances (np.array): Original distance points.
        concentrations (np.array): Original concentration values.
        num_points (int): The number of points desired in the interpolated grid.
        kind (str): The type of interpolation ('linear', 'cubic', etc.).

    Returns:
        tuple: A tuple containing:
               - new_distances (the finer grid)
               - new_concentrations (interpolated values)
    """
    # Create an interpolation function based on the input data
    # fill_value="extrapolate" allows estimation outside the original range if needed,
    # though usually we stay within the bounds.
    interpolator = interp1d(distances, concentrations, kind=kind, fill_value="extrapolate")
    
    # Generate a new, finer grid of distances
    new_distances = np.linspace(min(distances), max(distances), num_points)
    
    # Calculate interpolated concentrations
    new_concentrations = interpolator(new_distances)
    
    return new_distances, new_concentrations

def plot_data(original_dist, original_conc, interp_dist, interp_conc):
    """
    Plots the original vs interpolated data for verification.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(original_dist, original_conc, 'o', label='Original Data', markersize=8)
    plt.plot(interp_dist, interp_conc, '-', label='Interpolated Data', linewidth=2)
    plt.xlabel('Distance (m)')
    plt.ylabel('Concentration (µg/m³)')
    plt.title('Pollutant Concentration Interpolation')
    plt.legend()
    plt.grid(True)
    plt.show()

# Example Usage
if __name__ == "__main__":
    # Path to your uploaded file
    file_path = 'initial_conditions.csv' 
    
    try:
        # 1. Read Data
        dist, conc = read_boundary_conditions(file_path)
        print("Data read successfully.")
        print(f"Original Distance points: {len(dist)}")

        # 2. Interpolate Data
        # Generating a grid with more points (e.g., 50) for smoother simulation input
        new_dist, new_conc = interpolate_conditions(dist, conc, num_points=100, kind='cubic')
        print("Data interpolated successfully.")

        # 3. Plot to visualize
        plot_data(dist, conc, new_dist, new_conc)
        
    except Exception as e:
        print(e)
