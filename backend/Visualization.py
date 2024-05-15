import csv
import cv2
import numpy as np
from PyQt5 import QtWidgets, QtCore, QtGui
from matplotlib import pyplot
from math import sqrt, atan2, cos, sin
from PyQt5.QtGui import QImage
from Helpers import MathHelpers
from PopupWindow import PopupWindow
from backend import CONFIG


class VisualizationWindow(PopupWindow):
    def __init__(self, image_path=None, raw_data=None, heatmap=None, scanpath=None):
        super().__init__()

        with open('./coordinates/random_uv_coords.csv') as f:
            reader = csv.reader(f)
            self.raw = list(map(lambda q: (float(q[0]), float(q[1])), reader))

        # self.raw = {i: self.raw[i] for i in range(0, len(self.raw))}

        self.imagePath = image_path
        img = cv2.imread(self.imagePath)
        self.imageHeight = img.shape[0]
        self.imageWidth = img.shape[1]

        self.paddedImage = None
        self.paddingMax = None
        self.qimg = None
        self.color_1 = (0, 0, 0)
        self.color_2 = (255, 255, 255)
        self.threshold = 1

        self.uv_coords = []
        self.outliers = []
        self.outliersToDraw = []
        self.dir_vectors = {}
        self.points_group = {}
        self.repeat = False
        self.thresholdChanged = False
        self.points_group_keys = []
        self.rawData = raw_data
        self.heatmap = heatmap
        self.scanpath = scanpath
        self.saveImage.clicked.connect(self.save_image)
        self.color1_button.clicked.connect(self.set_first_color)
        self.color2_button.clicked.connect(self.set_second_color)

        self.thresholdInput.setValidator(QtGui.QRegularExpressionValidator(
            QtCore.QRegularExpression("^(1?\d{1,2}|2[0-4]\d|25[0-5])$")))
        self.thresholdInput.setText(str(self.threshold))
        self.thresholdInput.textChanged.connect(self.threshold_change)
        self.thresholdButton.clicked.connect(self.change_threshold)
        if not self.scanpath:
            self.color1_button.hide()
            self.color2_button.hide()
            self.thresholdInput.hide()
            self.thresholdButton.hide()

        if self.rawData:
            self.raw_to_point()
        else:
            for item in self.raw:
                self.uv_coords.append(MathHelpers.convert_uv_to_px(item, self.imageWidth, self.imageHeight))

        if self.imagePath:
            self.display_image()

    def change_threshold(self):
        self.display_image()

    def threshold_change(self):
        if self.thresholdInput.text() != "":
            self.thresholdChanged = False
            self.threshold = int(self.thresholdInput.text())

    def set_first_color(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            r, g, b, _ = color.getRgb()
            self.color1_button.setStyleSheet(
                "QPushButton {background-color: " + color.name() + "; border: 5px solid rgb(56, 65, 157); "
                                                                   "border-radius: 25px;}")
            self.color_1 = (b, g, r)
            self.display_image()

    def set_second_color(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            r, g, b, _ = color.getRgb()
            self.color2_button.setStyleSheet(
                "QPushButton {background-color: " + color.name() + "; border: 5px solid rgb(56, 65, 157); "
                                                                   "border-radius: 25px;}")
            self.color_2 = (b, g, r)
            self.display_image()

    def save_image(self):
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Image", "",
                                                             "PNG (*.png);;JPEG (*.jpg *.jpeg);;All Files (*)")
        if file_name:
            self.qimg.save(file_name)

    def raw_to_point(self):
        for item in self.rawData:
            eye_pos_world = MathHelpers.transform(np.array(item["sphere"]["center"]),
                                                  CONFIG.OFFLINE_CAMERA_POSITION,
                                                  CONFIG.OFFLINE_CAMERA_ROTATION_MATRIX)
            gaze_ray = MathHelpers.normalize(
                MathHelpers.rotate(item["circle_3d"]["normal"], CONFIG.OFFLINE_CAMERA_ROTATION_MATRIX))

            intersection_time = MathHelpers.intersect_plane(CONFIG.OFFLINE_DISPLAY_NORMAL_WORLD,
                                                            CONFIG.OFFLINE_DISPLAY_POSITION,
                                                            eye_pos_world,
                                                            gaze_ray)

            if intersection_time > 0.0:
                plane_intersection = MathHelpers.get_point([eye_pos_world, gaze_ray], intersection_time)
                plane_intersection = MathHelpers.transform(plane_intersection, CONFIG.OFFLINE_DISPLAY_POSITION,
                                                           CONFIG.OFFLINE_DISPLAY_ROTATION_MATRIX)
                result = MathHelpers.convert_to_uv_offline(plane_intersection, 250, 250, include_outliers=True)
                if result[0] > 1 or result[0] < 0 or result[1] > 1 or result[1] < 0:
                    self.outliers.append(result)
                else:
                    self.uv_coords.append(result)

    def display_image(self):
        if self.scanpath:
            image = self.scanpath_visualization()
            if len(self.outliers):
                image = self.outliers_visualization(image)
            self.repeat = True
        elif self.heatmap:
            image = self.heatmap_visualization()
            if len(self.outliers):
                image = self.outliers_visualization(image)
            self.repeat = True
        else:
            image = cv2.imread(self.imagePath)

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h, w, c = image.shape
        self.qimg = QImage(image.data, w, h, c * w, QImage.Format_RGB888)

        if image.shape[1] > self.image.width() or image.shape[0] > self.image.height():
            self.image.setPixmap(
                QtGui.QPixmap.fromImage(self.qimg).scaled(self.image.size(), QtCore.Qt.KeepAspectRatio,
                                                          QtCore.Qt.SmoothTransformation))
        else:
            self.image.setPixmap(QtGui.QPixmap.fromImage(self.qimg))
            self.image.setAlignment(QtCore.Qt.AlignCenter)

    def outliers_visualization(self, image):
        if not self.repeat:
            img = cv2.imread(self.imagePath)
            self.imageHeight = img.shape[0]
            self.imageWidth = img.shape[1]
            self.paddingMax = min(self.imageHeight, self.imageWidth) // 10

            for i in range(0, len(self.outliers)):
                self.outliers[i] = MathHelpers.convert_uv_to_px(self.outliers[i], self.imageWidth, self.imageHeight)
                if self.outliers[i][0] + self.paddingMax < 0:
                    continue
                if self.outliers[i][1] + self.paddingMax < 0:
                    continue
                if self.outliers[i][0] > self.imageWidth + self.paddingMax:
                    continue
                if self.outliers[i][1] > self.imageHeight + self.paddingMax:
                    continue
                self.outliersToDraw.append(self.outliers[i])

            self.paddedImage = np.zeros((self.imageHeight + 2 * self.paddingMax,
                                         self.imageWidth + 2 * self.paddingMax, 3), np.uint8)

        if len(self.outliersToDraw):
            self.paddedImage[self.paddingMax:self.paddingMax + self.imageHeight,
            self.paddingMax:self.paddingMax + self.imageWidth] = image

            for i in range(0, len(self.outliersToDraw)):
                cv2.circle(self.paddedImage,
                           (self.outliers[i][0] + self.paddingMax, self.outliers[i][1] + self.paddingMax),
                           5, (0, 0, 255), -1)

            # x = 1
            # y = 1
            # points = []
            # for i in range(11):
            #     for j in range(11):
            #         points.append((x, y))
            #         y -= 0.1

            #     y = 1
            #     x -= 0.1

            # for i in range(0, len(points)): cv2.circle(self.paddedImage, (int(points[i][0] * self.imageWidth +
            # self.paddingMax), int(points[i][1] * self.imageHeight + self.paddingMax)), 10, (0, 255, 0), -1)

            return self.paddedImage

        return image

    def scanpath_visualization(self):
        if not len(self.uv_coords):
            return cv2.imread(self.imagePath)

        image = cv2.imread(self.imagePath)
        image_width = image.shape[1]
        image_height = image.shape[0]
        circle_radius = min(image_width, image_height) // 100

        overlay_circles = image.copy()
        overlay_lines = image.copy()
        alpha_circles = 0.6
        outline_width = 3
        alpha_lines = 0.2
        text_face = cv2.FONT_HERSHEY_SIMPLEX
        text_scale = 0.8
        text_thickness = 2
        text_color = (0, 0, 0)

        colors = {}
        order = 0

        if self.rawData:
            if not self.repeat:
                for i in range(0, len(self.uv_coords)):
                    self.uv_coords[i] = MathHelpers.convert_uv_to_px(self.uv_coords[i], image_width, image_height)

        if not self.thresholdChanged:
            self.thresholdChanged = True
            self.points_group = {}
            main_point = None

            for i in range(0, len(self.uv_coords)):
                if not main_point:
                    main_point = (self.uv_coords[i][0], self.uv_coords[i][1])

                if abs(self.uv_coords[i][0] - main_point[0]) <= self.threshold and abs(
                        self.uv_coords[i][1] - main_point[1]) <= self.threshold:
                    if not self.points_group.get(order):
                        self.points_group[order] = {'points': [self.uv_coords[i]], 'middle': {'x': 0, 'y': 0},
                                                    'diameter': 0, 'index': order + 1}
                    else:
                        self.points_group[order]['points'].append(self.uv_coords[i])

                else:
                    order += 1
                    main_point = (self.uv_coords[i][0], self.uv_coords[i][1])
                    self.points_group[order] = {'points': [self.uv_coords[i]], 'middle': {'x': 0, 'y': 0},
                                                'diameter': 0, 'index': order + 1}

            # self.points_group = dict(sorted(self.points_group.items(), key=lambda item: len(item[1]['points']),
            # reverse=False))
            self.points_group_keys = list(self.points_group)

            for key in self.points_group:
                points = self.points_group[key]['points']
                x = 0
                y = 0

                for point in points:
                    x += point[0]
                    y += point[1]

                x = int(x / len(points))
                y = int(y / len(points))
                self.points_group[key]['middle']['x'] = x
                self.points_group[key]['middle']['y'] = y

            different_lengths = {}
            for key in self.points_group:
                if not different_lengths.get(len(self.points_group[key]['points'])):
                    different_lengths[len(self.points_group[key]['points'])] = [key]
                else:
                    different_lengths[len(self.points_group[key]['points'])].append(key)

            # base pixel for diameter ---- diameter = 20 normalize between new_min and new_max ---- normalized_value
            # = ((original_value - min_value) / (max_value - min_value)) * (new_max - new_min) + new_min
            new_min = CONFIG.OFFLINE_MINIMAL_DIAMETER_FIXATION
            new_max = CONFIG.OFFLINE_MAXIMAL_DIAMETER_FIXATION
            # normalize between 1 and 2 ---- normalized_value = (value - min_length) / (max_length - min_length) + 1

            if len(different_lengths) > 1:
                max_length = max(different_lengths)
                min_length = min(different_lengths)
                for value in different_lengths:
                    normalized_value = ((value - min_length) / (max_length - min_length)) * (
                            new_max - new_min) + new_min
                    for key in different_lengths[value]:
                        self.points_group[key]['diameter'] = int(circle_radius * normalized_value)
            else:
                for key in different_lengths:
                    for value in different_lengths[key]:
                        self.points_group[value]['diameter'] = circle_radius

        if len(self.points_group) > 1:
            t = 0
            for key in self.points_group:
                r = min(255, max(0, int(MathHelpers.lerp(self.color_1[0], self.color_2[0], t))))
                g = min(255, max(0, int(MathHelpers.lerp(self.color_1[1], self.color_2[1], t))))
                b = min(255, max(0, int(MathHelpers.lerp(self.color_1[2], self.color_2[2], t))))
                colors[key] = (r, g, b)
                t += 1 / (len(self.points_group) - 1)
        else:
            colors[0] = (self.color_1[0], self.color_1[1], self.color_1[2])

        for key in range(0, len(self.points_group)):
            x1 = self.points_group[self.points_group_keys[key]]['middle']['x']
            y1 = self.points_group[self.points_group_keys[key]]['middle']['y']
            radius1 = self.points_group[self.points_group_keys[key]]['diameter']
            if key < len(self.points_group) - 1:
                x2 = self.points_group[self.points_group_keys[key + 1]]['middle']['x']
                y2 = self.points_group[self.points_group_keys[key + 1]]['middle']['y']
                radius2 = self.points_group[self.points_group_keys[key + 1]]['diameter']

                distance = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

                if distance >= (radius1 + radius2):
                    angle = atan2(y2 - y1, x2 - x1)
                    point1_x = x1 + (radius1 + outline_width // 2) * cos(angle)
                    point1_y = y1 + (radius1 + outline_width // 2) * sin(angle)
                    point2_x = x2 - (radius2 + outline_width // 2) * cos(angle)
                    point2_y = y2 - (radius2 + outline_width // 2) * sin(angle)
                    cv2.line(overlay_lines, (int(point1_x), int(point1_y)), (int(point2_x), int(point2_y)),
                             colors[list(self.points_group)[key]], 4)

            text_size, _ = cv2.getTextSize(str(self.points_group[self.points_group_keys[key]]['index']), text_face,
                                           text_scale, text_thickness)
            text_origin = (int(x1 - text_size[0] / 2), int(y1 + text_size[1] / 2))

            # cv2.circle(overlay_circles, (x1, y1), radius1, colors[points_group_keys[key]], -1)
            cv2.circle(overlay_circles, (x1, y1), radius1, colors[self.points_group_keys[key]], outline_width)
            # cv2.putText(overlay_circles, str(points_group[points_group_keys[key]]['index']), text_origin,
            # TEXT_FACE, TEXT_SCALE, TEXT_COLOR, TEXT_THICKNESS, cv2.LINE_AA)

        result = cv2.addWeighted(overlay_circles, alpha_circles, image, 1 - alpha_circles, 0)
        result = cv2.addWeighted(overlay_lines, alpha_lines, result, 1 - alpha_lines, 0)
        return result

    def heatmap_visualization(self):
        if not len(self.uv_coords):
            return cv2.imread(self.imagePath)

        img = cv2.imread(self.imagePath)

        dpi = 100.0
        alpha = 0.5
        ngaussian = 200
        sd = 8
        width = img.shape[1]
        height = img.shape[0]

        if self.rawData:
            for i in range(0, len(self.uv_coords)):
                self.uv_coords[i] = MathHelpers.convert_uv_to_px(self.uv_coords[i], width, height)

        figsize = (width / dpi, height / dpi)
        fig = pyplot.figure(figsize=figsize, dpi=dpi, frameon=False)

        ax = pyplot.Axes(fig, [0, 0, 1, 1])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.axis([0, width, 0, height])
        ax.imshow(img)

        # HEATMAP
        # Gaussian
        gwh = ngaussian
        gsdwh = sd

        xo = gwh / 2
        yo = gwh / 2

        gaus = np.zeros([gwh, gwh], dtype=float)

        for i in range(gwh):
            for j in range(gwh):
                gaus[j, i] = np.exp(
                    -1.0 * (((float(i) - xo) ** 2 / (2 * gsdwh * gsdwh)) + (
                            (float(j) - yo) ** 2 / (2 * gsdwh * gsdwh))))

        # matrix of zeroes
        strt = gwh // 2
        heatmapsize = height + 2 * strt, width + 2 * strt
        heatmap = np.zeros(heatmapsize, dtype=float)
        # create heatmap
        for i in range(0, len(self.uv_coords)):
            # get x and y coordinates
            x = strt + self.uv_coords[i][0] - int(gwh / 2)
            y = strt + self.uv_coords[i][1] - int(gwh / 2)
            # correct Gaussian size if either coordinate falls outside of
            # display boundaries
            if (not 0 < x < width) or (not 0 < y < height):
                hadj = [0, gwh]
                vadj = [0, gwh]
                if 0 > x:
                    hadj[0] = abs(x)
                    x = 0
                elif width < x:
                    hadj[1] = gwh - int(x - width)
                if 0 > y:
                    vadj[0] = abs(y)
                    y = 0
                elif height < y:
                    vadj[1] = gwh - int(y - height)
                # add adjusted Gaussian to the current heatmap
                try:
                    heatmap[y:y + vadj[1], x:x + hadj[1]] += gaus[vadj[0]:vadj[1], hadj[0]:hadj[1]] * self.uv_coords[i][
                        2]
                except Exception as e:
                    print(e)
                    # fixation was probably outside of display
                    pass
            else:
                # add Gaussian to the current heatmap
                heatmap[y:y + gwh, x:x + gwh] += gaus
        # resize heatmap
        heatmap = heatmap[strt:height + strt, strt:width + strt]
        # remove zeros
        lowbound = np.mean(heatmap[heatmap > 0])
        heatmap[heatmap < lowbound] = np.NaN
        # draw heatmap on top of image
        ax.imshow(heatmap, cmap='jet', alpha=alpha)

        # FINISH PLOT
        # invert the y axis, as (0,0) is top left on a display
        ax.invert_yaxis()
        fig.canvas.draw()
        data = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        pyplot.close(fig)
        return data
