# Copyright (C) 2020-2022 Sebastian Blauth
#
# This file is part of cashocs.
#
# cashocs is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# cashocs is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with cashocs.  If not, see <https://www.gnu.org/licenses/>.

"""For the documentation of this demo see https://cashocs.readthedocs.io/en/latest/demos/optimal_control/doc_state_constraints.html.

"""

from fenics import *
import numpy as np

import cashocs

config = cashocs.load_config("config.ini")
mesh, subdomains, boundaries, dx, ds, dS = cashocs.regular_mesh(25)
V = FunctionSpace(mesh, "CG", 1)

y = Function(V)
p = Function(V)
u = Function(V)

e = inner(grad(y), grad(p)) * dx - u * p * dx
bcs = cashocs.create_dirichlet_bcs(V, Constant(0), boundaries, [1, 2, 3, 4])

y_d = Expression("sin(2*pi*x[0]*x[1])", degree=1)
alpha = 1e-3
J_init_form = (
    Constant(0.5) * (y - y_d) * (y - y_d) * dx + Constant(0.5 * alpha) * u * u * dx
)
J_init = cashocs.IntegralFunctional(J_init_form)
ocp_init = cashocs.OptimalControlProblem(e, bcs, J_init, y, u, p, config=config)
ocp_init.solve()


y_bar = 1e-1
gammas = [pow(10, i) for i in np.arange(1, 9, 3)]

for gamma in gammas:

    J_form = J_init_form + cashocs._utils.moreau_yosida_regularization(
        y, gamma, dx, upper_threshold=y_bar
    )
    J = cashocs.IntegralFunctional(J_form)

    ocp_gamma = cashocs.OptimalControlProblem(e, bcs, J, y, u, p, config=config)
    ocp_gamma.solve()

y_max = np.max(y.vector()[:])
error = abs(y_max - y_bar) / abs(y_bar) * 100
print("Maximum value of y: " + str(y_max))
print("Relative error between y_max and y_bar: " + str(error) + " %")


### Post Processing

import matplotlib.pyplot as plt

plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
fig = plot(u)
plt.colorbar(fig, fraction=0.046, pad=0.04)
plt.title("Control variable u")

plt.subplot(1, 3, 2)
fig = plot(y)
plt.colorbar(fig, fraction=0.046, pad=0.04)
plt.title("State variable y")

plt.subplot(1, 3, 3)
fig = plot(y_d, mesh=mesh)
plt.colorbar(fig, fraction=0.046, pad=0.04)
plt.title("Desired state y_d")

plt.tight_layout()
# plt.savefig('./img_state_constraints.png', dpi=150, bbox_inches='tight')
