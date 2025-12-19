import os
from model import (read_boundary_conditions, interpolate_conditions,
                   create_grid, advect)
from plotting import (plot_data, plot_initial, plot_snapshots, plot_heatmap)

if __name__ == "__main__":
  csv_file = input("csv file: ")
  L = input("length of river domain (m): ")
  dx = input("change in space (m): ")
  T = input("simulation time (s): ")
  dt = input("change in time (s): ")
  U = input("velocity (ms^-1): ")

  try:
    L = float(L)
    dx = float(dx)
    T = float(T)
    dt = float(dt)
    U = float(U)
  except ValueError:
      raise SystemExit("type wrong")

  try:
    x = create_grid(L, dx, T)  # use function to generate list x and t

     # 1. Reading Data
    dist, conc = read_boundary_conditions(csv_file)
    print("Data read successfully.")
    print(f"Original Distance points: {len(dist)}")

        # 2. Interpolating Data
        # Generating a grid with more points (e.g., 50) for smoother simulation input
    new_dist, theta_init = interpolate_conditions(dist, conc, target_x=x, kind='cubic')
    print("Data interpolated successfully.")

        # 3. A Plot to visualize
    plot_data(dist, conc, new_dist, theta_init)

    theta_all, time_grid = advect(theta_init, U, dx, dt, T)

    plot_initial(x, theta_init)
    plot_snapshots(x, time_grid, theta)
    plot_heatmap(x, time_grid, theta)
  except Exception as e:
    print(e)
