import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import os


csv_file = input("csv file")
L = input("length of river domain (m): ")
dx = input("change in space (m): ")
T = input("simulation time (s): ")
dt = input("change in time (s): ")
U = input("velocity (ms^-1): ")


# change value to correct type
try:
    L = float(L)
    dx = float(dx)
    T = float(T)
    dt = float(dt)
    U = float(U)
except ValueError:
    raise SystemExit("type wrong")
    
    
#----------THIRD-----------


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
    # L = length of river domain (m)
    # dx = change in space (m) 
    # T = simulation time (s)
    # dt = change in time (s) 

    if L <= 0 or dx <= 0 or dt <= 0 or T < 0:
        raise ValueError('Invalid grid parameters')

    nx = int(L/dx) + 1  
    nt = int(T/dt) + 1

    x = np.linspace(0, L, nx)
    num_time_steps = np.linspace(0, T, nt)

    return x, num_time_steps            

x, num_time_steps = create_grid(L, dx, T, dt)  # use function to generate list x and t

original_dist, original_conc = read_boundary_conditions(csv_file)

theta_init = interpolate_conditions(original_dist, original_conc, target_x=x, kind='linear')
theta_init = np.array(theta_init)


def cfl_number(U, dx, dt):
    if dx <= 0 or dt <= 0:
        raise ValueError('dx and dt must be positive')

    return U * dt / dx      ## maybe can delete this, because secound part has test


def is_cfl_stable(U, dx, dt):
    return cfl_number(U, dx, dt) <= 1           ## maybe can delete this, because secound part has test


# ---------------------SECOUND PART ------------------------


def advect(theta_init, U, dx, dt, num_time_steps): 
    # Solves the advection equation using the first-order upwind scheme.
    # Calculate the CFL number which represents how much information travels across a grid cell in one time step.
    CFL = U * dt / dx

   
    if CFL > 1.0:
      print(f"*** WARNING: CFL condition (U*dt/dx <= 1) violated (CFL={CFL:.2f}). Solution is unstable. ***")

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

        # Progress to next step.
        theta_current = theta_next
        theta_all[n + 1, :] = theta_current

    return theta_all

def test_steady_advection_case():
    # Our test parameters for the simulation.
    U_test = 1.0 # Velocity.
    dx_test = 0.1 # Spatial Step.
    dt_test = 0.05 # Time Step.
    T_max_test = 1.0 # Total Simulation Time.

    x_test, time_points_test = create_grid(1.0, dx_test, T_max_test, dt_test)
    theta_init_test = np.full(len(x_test), 10.0)

    # Run the solver.
    theta_result = advect(theta_init_test, U_test, dx_test, dt_test, time_points_test)

    assert np.allclose(theta_result[-1, :], 10.0, atol=1e-5), "Steady Advection test failed."
    print("Steady Advection test passed successfully (Result is approximately constant)>")


def plot_data(original_dist, original_conc, interp_dist, interp_conc):

    plt.figure(figsize=(10, 6))
    plt.plot(original_dist, original_conc, 'o', label='Original Data', markersize=8)
    plt.plot(interp_dist, interp_conc, '-', label='Interpolated Data', linewidth=2)
    plt.xlabel('Distance (m)')
    plt.ylabel('Concentration (µg/m³)')
    plt.title('Pollutant Concentration Interpolation')
    plt.legend()
    plt.grid(True)
    plt.show()

# Example
if __name__ == "__main__":
    # Path to your uploaded file

    
    try:
        # 1. Reading Data
        dist, conc = read_boundary_conditions(csv_file)
        print("Data read successfully.")
        print(f"Original Distance points: {len(dist)}")

        # 2. Interpolating Data
        # Generating a grid with more points (e.g., 50) for smoother simulation input
        new_dist, new_conc = interpolate_conditions(dist, conc, target_x=x, kind='cubic')
        print("Data interpolated successfully.")

        # 3. A Plot to visualize
        plot_data(dist, conc, new_dist, new_conc)
        
    except Exception as e:
        print(e)


#-------------------FOURTH---------------------

import numpy as np
import matplotlib.pyplot as plt

def plot_initial(x, C0):
    plt.figure()
    plt.plot(x, C0, "o-")
    plt.xlabel("x (m)")
    plt.ylabel("C")
    plt.title("Initial condition")
    plt.grid(True)
    plt.show()


def plot_snapshots(x, t, C_hist):
    C_hist = np.array(C_hist)
    t = np.array(t)
    nt = len(t)

    idx_list = [0, nt // 2, nt - 1]

    plt.figure()
    for k in idx_list:
        plt.plot(x, C_hist[k, :], label=f"t = {t[k]} s")
    plt.xlabel("x (m)")
    plt.ylabel("C")
    plt.title("C vs x at different times")
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_heatmap(x, t, C_hist):
    x = np.array(x)
    t = np.array(t)
    C_hist = np.array(C_hist)

    plt.figure()
    plt.imshow(
        C_hist,
        origin="lower",
        aspect="auto",
        extent=[x.min(), x.max(), t.min(), t.max()]
    )
    plt.colorbar(label="C")
    plt.xlabel("x (m)")
    plt.ylabel("t (s)")
    plt.title("Space-time plot")
plt.show()

from plotting import plot_initial, plot_snapshots, plot_heatmap

plot_initial(x, C0)
plot_snapshots(x, t, C_hist)
plot_heatmap(x, t, C_hist)




main model file has these functions:
•	make_grid(x_max, dx, t_max, dt) → returns x, t
•	solve_advection(x, t, U, C0, decay_k=0.0) → returns C_hist
•	read_initial_conditions_csv(path, x_grid) → returns C0



import numpy as np
import pandas as pd

from src.model import make_grid, solve_advection, read_initial_conditions_csv


def test_case1_run():
    x, t = make_grid(x_max=20.0, dx=0.2, t_max=300.0, dt=10.0)

    C0 = np.zeros_like(x)
    C0[0] = 250.0  # pulse at left

    U = 0.1

    C_hist = solve_advection(x, t, U, C0)

    assert C_hist.shape == (len(t), len(x))

    assert C_hist.min() >= -1e-6


def test_case2_csv():
    x, t = make_grid(x_max=2.0, dx=0.2, t_max=10.0, dt=5.0)

    x_raw = np.array([0.0, 0.5, 1.0, 1.5, 2.0])
    C_raw = np.array([5.0, 10.0, 8.0, 6.0, 3.0])

    df = pd.DataFrame({"x": x_raw, "C": C_raw})
    csv_path = "tmp_ic.csv"
    df.to_csv(csv_path, index=False)

    C0 = read_initial_conditions_csv(csv_path, x)

    assert len(C0) == len(x)
    # values should not explode
    assert C0.min() >= 0.0


def test_decay():
    x, t = make_grid(x_max=5.0, dx=0.25, t_max=40.0, dt=5.0)

    C0 = np.zeros_like(x)
    C0[0] = 100.0

    C_no_decay = solve_advection(x, t, U=0.1, C0=C0, decay_k=0.0)
    C_decay = solve_advection(x, t, U=0.1, C0=C0, decay_k=0.02)

    max_no = C_no_decay.max()
    max_yes = C_decay.max()

    assert max_yes <= max_no + 1e-6
