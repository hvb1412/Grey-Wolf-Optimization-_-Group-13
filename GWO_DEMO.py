import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os

# HAM MUC TIEU (MINIMIZE)
def sphere(x):
    return np.sum(x**2, axis=1)

# THAM SO GWO
n_wolves = 30
dim = 2
max_iter = 50
lb, ub = -500, 500

# KHOI TAO DAN SOI
positions = np.random.uniform(lb, ub, (n_wolves, dim))

if not os.path.exists("frames"):
    os.makedirs("frames")

# TAO HINH VE
fig, ax = plt.subplots(figsize=(8, 8))

# Ve duong dong muc (contour)
x = np.linspace(lb, ub, 300)
y = np.linspace(lb, ub, 300)
X, Y = np.meshgrid(x, y)
Z = X**2 + Y**2
ax.contour(X, Y, Z, levels=15, colors="black", alpha=0.3)

# Ve cac con soi
scat = ax.scatter(
    positions[:, 0],
    positions[:, 1],
    c="orange",
    s=30,
    label="Wolves"
)

# Alpha, Beta, Delta
alpha_dot = ax.scatter([], [], c="red", s=120, marker="*", label="Alpha")
beta_dot  = ax.scatter([], [], c="blue", s=80, marker="*", label="Beta")
delta_dot = ax.scatter([], [], c="green", s=80, marker="*", label="Delta")

ax.set_xlim(lb, ub)
ax.set_ylim(lb, ub)
ax.set_xlabel("x₁")
ax.set_ylabel("x₂")
ax.legend(frameon=False)

# HAM CAP NHAT MOI ITERATION
def gwo_step(iteration):
    global positions

    a = 2 - 2 * iteration / max_iter

    fitness = sphere(positions)
    idx = np.argsort(fitness)

    alpha = positions[idx[0]]
    beta  = positions[idx[1]]
    delta = positions[idx[2]]

    for i in range(n_wolves):
        X = positions[i]

        # Alpha
        r1, r2 = np.random.rand(), np.random.rand()
        A1 = 2 * a * r1 - a
        C1 = 2 * r2
        X1 = alpha - A1 * abs(C1 * alpha - X)

        # Beta
        r1, r2 = np.random.rand(), np.random.rand()
        A2 = 2 * a * r1 - a
        C2 = 2 * r2
        X2 = beta - A2 * abs(C2 * beta - X)

        # Delta
        r1, r2 = np.random.rand(), np.random.rand()
        A3 = 2 * a * r1 - a
        C3 = 2 * r2
        X3 = delta - A3 * abs(C3 * delta - X)

        positions[i] = (X1 + X2 + X3) / 3

    positions[:] = np.clip(positions, lb, ub)

    # cap nhat ve
    scat.set_offsets(positions)
    alpha_dot.set_offsets(alpha)
    beta_dot.set_offsets(beta)
    delta_dot.set_offsets(delta)

    ax.set_title(
        f"Grey Wolf Optimizer (Iteration {iteration + 1}/{max_iter})",
        fontsize=12
    )

    # LUU ANH MOI ITERATION 
    fig.savefig(
        f"frames/gwo_iter_{iteration:03d}.png",
        dpi=300,
        bbox_inches="tight"
    )

    return scat, alpha_dot, beta_dot, delta_dot

# ANIMATION
ani = animation.FuncAnimation(
    fig,
    gwo_step,
    frames=max_iter,
    interval=1200,
    repeat=False
)

plt.show()
