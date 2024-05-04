from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Text3D
import numpy as np


class Model3D(FigureCanvasQTAgg):
    def __init__(self, width, height):
        self.figure = Figure(figsize=(width, height))
        self.figure.patch.set_facecolor((194 / 255, 217 / 255, 255 / 255))
        self.axes = self.figure.add_subplot(111)
        super(Model3D, self).__init__(self.figure)

    def visualize_graph(self, raycast_end, camera_pos, camera_target, camera_normal, screen_width=250,
                        screen_height=250, ray_number=1, scale_factor=1):
        ax = self.figure.add_subplot(111, projection='3d')
        ax.set_facecolor((194 / 255, 217 / 255, 255 / 255))

        # Set limit for each axis
        ax.set_xlim(250 * scale_factor, -250 * scale_factor)
        ax.set_ylim(0, -500 * scale_factor)
        ax.set_zlim(-250 * scale_factor, 250 * scale_factor)

        # Set label for each axis
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        # Display
        r = 125
        x1 = r
        y1 = -500
        z1 = r
        x2 = - r
        y2 = -500
        z2 = - r
        verts = [(x1, y1, z1), (x2, y1, z1), (x2, y2, z2), (x1, y2, z2)]
        ax.add_collection3d(Poly3DCollection([verts], facecolors='gray', linewidths=1, edgecolors='r', alpha=.25))

        # Display label
        x, y, z = 130, -500, 130
        text = Text3D(x, y, z, 'Display', zdir='x')
        ax.add_artist(text)

        # Eye
        u, v = np.mgrid[0:2 * np.pi:20j, 0:np.pi:10j]
        x3 = 10 * np.cos(u) * np.sin(v)
        y3 = 10 * np.sin(u) * np.sin(v)
        z3 = 10 * np.cos(v)
        ax.plot_wireframe(x3, y3, z3, color="gray", facecolors='gray')

        # Eye label
        x, y, z = 7, 0, 7
        text = Text3D(x, y, z, 'Eye', zdir='x')
        ax.add_artist(text)

        # Camera
        u, v = np.mgrid[0:2 * np.pi:20j, 0:np.pi:10j]
        x3 = 10 * np.cos(u) * np.sin(v) + camera_pos[0]  # switch x axis because of the global axis
        y3 = 10 * np.sin(u) * np.sin(v) + camera_pos[1]  # switch y axis because of the global axis
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

        # Camera normal
        x_start, y_start, z_start = camera_pos[0], camera_pos[1], camera_pos[2]
        x_end, y_end, z_end = camera_normal[0], camera_normal[1], camera_normal[2]

        dx = x_end - x_start
        dy = y_end - y_start
        dz = z_end - z_start

        ax.quiver(x_start, y_start, z_start, dx, dy, dz, length=50, normalize=True, color='blue')

        for i in range(ray_number):
            x_start, y_start, z_start = 0, 0, 0
            x_end, y_end, z_end = raycast_end[i]
            # Plot the line
            ax.plot([x_start, x_end], [y_start, y_end], [z_start, z_end], color='red', linewidth=1)

        ax.view_init(elev=15, azim=-45)
        self.figure.subplots_adjust(left=0, right=1, bottom=0, top=1, wspace=0, hspace=0)

    def visualize_raycast(self):
        ...
