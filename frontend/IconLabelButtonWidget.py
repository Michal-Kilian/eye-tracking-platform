from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QPushButton, QVBoxLayout, QGraphicsDropShadowEffect
from PyQt5.QtGui import QPixmap, QIcon, QColor

from frontend.StyleSheets import Fonts, GraphicEffects, ModeSelectionScreenStyleSheet


class IconLabelButtonWidget(QWidget):
    def __init__(self, icon_path, label_text):
        super().__init__()

        self.icon_button = QPushButton()
        icon = QIcon()
        icon.addPixmap(QPixmap(icon_path), QIcon.Normal, QIcon.Off)
        self.icon_button.setIcon(icon)
        self.icon_button.setIconSize(QSize(140, 140))
        self.icon_button.setFixedSize(210, 210)
        self.icon_button.setStyleSheet(ModeSelectionScreenStyleSheet.IconButton)
        self.icon_button.setGraphicsEffect(GraphicEffects.Shadow(30))

        self.text_label = QLabel(label_text)
        self.text_label.setAlignment(Qt.AlignHCenter)
        self.text_label.setFixedHeight(50)
        self.text_label.setStyleSheet(ModeSelectionScreenStyleSheet.TextLabel)
        self.text_label.setFont(Fonts.HeadingTextFont())

        button_layout = QVBoxLayout()
        button_layout.addWidget(self.icon_button)
        button_layout.addWidget(self.text_label)
        button_layout.setAlignment(self.icon_button, Qt.AlignCenter)

        self.setLayout(button_layout)
