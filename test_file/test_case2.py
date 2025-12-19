import numpy as np
import os
from src.model import (read_boundary_conditions, interpolate_conditions,
    create_grid)

def test_case2_csv():
    x = create_grid(2.0, 0.2, 10.0)

    x_raw = np.array([0.0, 0.5, 1.0, 1.5, 2.0])
    C_raw = np.array([5.0, 10.0, 8.0, 6.0, 3.0])

    df = pd.DataFrame({"x": x_raw, "C": C_raw})
    csv_path = "initial_conditions.csv"
    df.to_csv(csv_path, index=False)
try:
    dist, conc = read_boundary_conditions(csv_path)
    _, theta_init = interpolate_conditions(dist, conc, target_x=x, kind='linear')
    theta_init = np.array(theta_init)

    assert len(theta_init) == len(x)
    # values should not explode
    assert theta_init.min() >= 0.0
