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
