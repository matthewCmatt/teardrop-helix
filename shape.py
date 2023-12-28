import numpy as np
import matplotlib.pyplot as plt


# --- Initialize Plot
fig = plt.figure()
view_range = 2.4
ax = plt.axes(
    projection="3d",
    xlim=(-view_range, view_range),
    ylim=(-view_range, view_range),
    zlim=(-view_range, view_range),
)


def spiral(phase_shift, color_sphere, color_cone):
    # --- Parameters
    r = 1  # Radius of sphere (and basic cone)
    h = 2.5  # Height of cone (basic before cutoff/offset)
    freq = 3  # Frequency of spiral
    base = 0  # Z coordinate for center of sphere, which the cone is offset from
    phase_shift = phase_shift  # Phase shift of spiral

    # --- Compute cone offset
    sphere_cutoff = r * r / (np.sqrt(h * h + r * r))  # Z cutoff of sphere
    rcone = r - sphere_cutoff * r / h  # Radius of base of cone at cutoff
    rsphere = np.sqrt(
        r * r - sphere_cutoff * sphere_cutoff
    )  # Radius of face where sphere is cut off
    roffset = rsphere - rcone  # Extra width needed for cone
    zoffset = roffset * h / r  # Vertical offset needed to provide extra width
    phase_shift_cone = zoffset * freq
    # ^ Offsetting cone means its spiral must be phase-shifted
    # by an amount to intersect with sphere spiral

    # --- Cone
    cone_z = base + np.linspace(sphere_cutoff - zoffset, h, 1000)
    cone_x = (
        ((h - cone_z) / h) * r * np.cos(freq * cone_z + phase_shift + phase_shift_cone)
    )
    cone_y = (
        ((h - cone_z) / h) * r * np.sin(freq * cone_z + phase_shift + phase_shift_cone)
    )
    cone_z = cone_z + zoffset  # Add vertical offset after generating x's and y's

    # --- Sphere
    sphere_z = base + np.linspace(-r, sphere_cutoff, 1000)
    sphere_x = np.sqrt(r * r - sphere_z * sphere_z) * np.cos(
        freq * sphere_z + phase_shift
    )
    sphere_y = np.sqrt(r * r - sphere_z * sphere_z) * np.sin(
        freq * sphere_z + phase_shift
    )

    # --- Plot and visualize
    ax.plot3D(sphere_x, sphere_y, sphere_z, color_sphere)
    ax.plot3D(cone_x, cone_y, cone_z, color_cone)


pi = np.pi
n = 3
colors = ("red", "orange", "gold", "green", "blue", "purple")
for i in range(0, n):
    spiral(i / (n / 2) * pi, colors[i], colors[i + 3])

ax.view_init(10, 35)

plt.savefig("foo.png", dpi=300)
