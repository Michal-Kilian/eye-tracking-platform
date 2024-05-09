import matplotlib
from matplotlib import pyplot
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Text3D
import numpy as np
from backend import CONFIG
matplotlib.use('TkAgg')


def visualize_raycast(all_rays, raycast_end, camera_pos, camera_target, camera_dirs, gaze_dir, screen_width=310,
                      screen_height=174, ray_number=1):
    fig = pyplot.figure(facecolor='#C2D9FF')
    ax = fig.add_subplot(111, projection='3d')
    scale = 1.0 / max(CONFIG.SCALE_FACTOR, 0.1)

    # Set limit for each axis
    ax.set_xlim(250 * scale, -250 * scale)
    ax.set_ylim(0, -500 * scale)
    ax.set_zlim(-250 * scale, 250 * scale)

    # Set label for each axis
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Display
    x1 = screen_width / 2
    y1 = -500
    z1 = screen_height / 2
    x2 = - screen_width / 2
    y2 = -500
    z2 = - screen_height / 2
    verts = [(x1, y1, z1), (x2, y1, z1), (x2, y2, z2), (x1, y2, z2)]
    ax.add_collection3d(Poly3DCollection([verts], facecolors='gray', linewidths=1, edgecolors='r', alpha=.25))

    # Display label
    x, y, z = screen_width / 2 + 10, -500, screen_height / 2 + 10
    text = Text3D(x, y, z, 'Display', zdir='x')
    ax.add_artist(text)

    # Eye
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    x3 = 10 * np.cos(u)*np.sin(v)
    y3 = 10 * np.sin(u)*np.sin(v)
    z3 = 10 * np.cos(v)
    ax.plot_wireframe(x3, y3, z3, color="gray", facecolors='gray')

    # Eye label
    x, y, z = 7, 0, 7
    text = Text3D(x, y, z, 'Eye', zdir='x')
    ax.add_artist(text)

    # Camera
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    x3 = 10 * np.cos(u)*np.sin(v) + camera_pos[0]  # switch x-axis because of the global axis
    y3 = 10 * np.sin(u)*np.sin(v) + camera_pos[1]  # switch y-axis because of the global axis
    z3 = 10 * np.cos(v) + camera_pos[2]
    ax.plot_wireframe(x3, y3, z3, color="green", facecolors='green')

    # Camera label
    x, y, z = camera_pos[0] + 7, camera_pos[1], camera_pos[2] + 7
    text = Text3D(x, y, z, 'Camera', zdir='x')
    ax.add_artist(text)

    # Camera target
    x_start, y_start, z_start = camera_pos[0], camera_pos[1], camera_pos[2]
    x_end, y_end, z_end = camera_target[0], camera_target[1], camera_target[2]
    ax.plot([x_start, x_end], [y_start, y_end], [z_start, z_end], color='green', linewidth=1)

    # Camera axes
    ax.quiver(*camera_pos, *camera_dirs[0], length=25, normalize=True, color='red')
    ax.quiver(*camera_pos, *camera_dirs[1], length=25, normalize=True, color='green')
    ax.quiver(*camera_pos, *camera_dirs[2], length=25, normalize=True, color='blue')

    # Eye axes
    origin = (0, 0, 0)
    dirs = ((1, 0, 0), (0, 1, 0), (0, 0, 1))

    # Camera axes
    ax.quiver(*origin, *dirs[0], length=25, normalize=True, color='red')
    ax.quiver(*origin, *dirs[1], length=25, normalize=True, color='green')
    ax.quiver(*origin, *dirs[2], length=25, normalize=True, color='blue')

    # Gaze direction
    x_start, y_start, z_start = origin
    x_end, y_end, z_end = raycast_end[0], raycast_end[1], raycast_end[2]
    ax.plot([x_start, x_end], [y_start, y_end], [z_start, z_end], color='red', linewidth=1)

    for i in range(ray_number):
        ax.scatter(all_rays[i][0], all_rays[i][1], all_rays[i][2], color='blue')

    ax.view_init(elev=CONFIG.ELEVATION, azim=CONFIG.AZIMUTH)
    fig.set_size_inches(8, 6)
    fig.tight_layout()
    fig.canvas.draw()
    data = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    pyplot.close(fig)
    return data
