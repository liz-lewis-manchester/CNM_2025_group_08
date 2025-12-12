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
