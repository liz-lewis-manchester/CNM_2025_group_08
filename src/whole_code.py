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
