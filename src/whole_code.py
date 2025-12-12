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
