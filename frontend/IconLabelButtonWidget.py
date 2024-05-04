from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QPushButton, QVBoxLayout, QGraphicsDropShadowEffect
from PyQt5.QtGui import QPixmap, QIcon, QColor

from frontend.StyleSheets import text_font, heading_text_font, get_shadow


class IconLabelButtonWidget(QWidget):
    def __init__(self, icon_path, label_text):
        super().__init__()

        # Create icon button
        self.icon_button = QPushButton()
        icon = QIcon()
        icon.addPixmap(QPixmap(icon_path), QIcon.Normal, QIcon.Off)
        self.icon_button.setIcon(icon)
        self.icon_button.setIconSize(QSize(140, 140))
        self.icon_button.setFixedSize(210, 210)
        self.icon_button.setStyleSheet("QPushButton {text-align: center; background-color: white; border-radius: 105; "
                                       "border: 5px solid white;}")
        self.icon_button.setGraphicsEffect(get_shadow(30))

        # Create text label
        self.text_label = QLabel(label_text)
        self.text_label.setAlignment(Qt.AlignHCenter)
        self.text_label.setFixedHeight(50)
        self.text_label.setStyleSheet("QLabel {color: rgb(56,65,157); border: none; outline: none;}")
        self.text_label.setFont(heading_text_font())

        # Create layout for button content (icon and text)
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.icon_button)
        button_layout.addWidget(self.text_label)
        button_layout.setAlignment(self.icon_button, Qt.AlignCenter)

        # Set button content layout
        self.setLayout(button_layout)
