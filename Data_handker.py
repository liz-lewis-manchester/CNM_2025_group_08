import numpy as np

def advect(theta_init, U, dx, dt, num_time_steps):
    CFL = U * dt / dx

    if CFL > 1.0:
      print(f"*** WARNING: CFL condition (U*dt/dx <= 1) violated (CFL={CFL:.2f}). Solution is unstable. ***")

    num_points = len(theta_init)
    theta_current = theta_init.copy()

    theta_all = np.zeros((num_time_steps +1, num_points))
    theta_all[0, :] = theta_init

    for n in range(num_time_steps):
        d_theta = -CFL * (theta_current[1:] - theta_current[:-1])

        theta_next = theta_current.copy()
        theta_next[1:] = theta_current[1:] + d_theta

        theta_next[0] = 0.0

        theta_current = theta_next
        theta_all[n + 1, :] = theta_current

    return theta_all

def test_steady_advection_case():
    U_test = 1.0
    dx_test = 0.1
    dt_test = 0.05
    T_max_test = 1.0

    num_time_steps = int(T_max_test / dt_test)

    theta_init_test = np.full(int(1.0/0.1) + 1, 10.0)

    theta_result = advect(theta_init_test, U_test, dx_test, dt_test, num_time_steps)

    assert np.allclose(theta_result[-1, :], 10.0, atol=1e-5), "Steady Advection test failed."
    print("Steady Advection test passed successfully (Result is approximately constant)>")

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
