import numpy as np
import time

from dilqr_rs.dilqr import DiLQR

class DiLQR_Exact(DiLQR):
    def __init__(self, system,
        Q, Qd, R, x0, xdt, u_trj, xbound, ubound, solver_name="osqp"):
        super(DiLQR_Exact, self).__init__(system, Q, Qd, R, x0, xdt, u_trj,
            xbound, ubound, solver_name)
        """
        Direct Iterative LQR using exact gradients.
        Requires:
        - jacobian_xu from systems class.
        """

    def get_TV_matrices(self, x_trj, u_trj):
        """
        Get time varying linearized dynamics given a nominal trajectory.
        - args:
            x_trj (np.array, shape (T + 1) x n)
            u_trj (np.array, shape T x m)
        """
        At = np.zeros((self.T, self.dim_x, self.dim_x))
        Bt = np.zeros((self.T, self.dim_x, self.dim_u))
        ct = np.zeros((self.T, self.dim_x))
        for t in range(self.T):
            AB = self.system.jacobian_xu(x_trj[t], u_trj[t])
            At[t] = AB[:,0:self.dim_x]
            Bt[t] = AB[:,self.dim_x:self.dim_x+self.dim_u]
            ct[t] = self.system.dynamics(x_trj[t], u_trj[t]) - At[t].dot(
                x_trj[t]) - Bt[t].dot(u_trj[t])
        return At, Bt, ct
