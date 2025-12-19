import matplotlib.pyplot as plt
import os

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

def plot_initial(x, theta_init):
    plt.figure()
    plt.plot(x, theta_init, "o-")
    plt.xlabel("x (m)")
    plt.ylabel("Concentration (µg/m³)")
    plt.title("Initial condition")
    plt.grid(True)
    plt.show()

def plot_snapshots(x, time_grid, C_hist):
    C_hist = np.array(C_hist)
    t = np.array(num_time_steps)
    nt = len(t)

    idx_list = [0, nt // 2, nt - 1]

    plt.figure()
    for k in idx_list:
        plt.plot(x, C_hist[k, :], label=f"t = {t[k]} s")
    plt.xlabel("x (m)")
    plt.ylabel("C (µg/m³)")
    plt.title("C vs x at different times")
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_heatmap(x, time_grid, C_hist):
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
    plt.colorbar(label="C (µg/m³)")
    plt.xlabel("x (m)")
    plt.ylabel("t (s)")
    plt.title("Space-time plot")
    plt.show()
