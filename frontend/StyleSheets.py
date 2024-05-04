from PyQt5 import QtGui
from PyQt5.QtWidgets import QGraphicsDropShadowEffect


def heading_font() -> QtGui.QFont:
    font = QtGui.QFont()
    font.setPointSize(24)
    font.setBold(True)
    font.setWeight(75)
    return font


def text_font() -> QtGui.QFont:
    font = QtGui.QFont()
    font.setFamily("Yu Gothic UI Semibold")
    font.setPointSize(11)
    font.setBold(True)
    font.setItalic(False)
    font.setWeight(75)
    return font


def heading_text_font() -> QtGui.QFont:
    font = QtGui.QFont()
    font.setFamily("Yu Gothic UI Semibold")
    font.setPointSize(15)
    font.setBold(True)
    font.setItalic(False)
    return font


def qcombobox_font() -> QtGui.QFont:
    font = QtGui.QFont()
    font.setFamily("Yu Gothic UI Semibold")
    font.setPointSize(9)
    font.setBold(True)
    font.setItalic(False)
    font.setWeight(75)
    return font


def get_shadow(blur_size) -> QGraphicsDropShadowEffect:
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(blur_size)
    return shadow


QWidget_background_color = ("""
    QWidget {
        background-color: rgb(194, 217, 255);
    }
""")

QPushButton_frame = ("""
    QPushButton {
        background-color: rgb(56,65,157);
        color: white;
        border: 0;
    }
""")

QPushButton_left1 = ("""
    QPushButton {
        text-align: left;
        padding-bottom: 4;
        padding-left: 8;
        color: rgb(255, 255, 255);
    }
    QPushButton:hover{
        font: 63 12pt "Yu Gothic UI Semibold";
    }
""")

QPushButton_right1 = ("""
    QPushButton {
        text-align: right;
        padding-right: 15;
        padding-bottom: 4;
        color: rgb(255, 255, 255);
    }
    QPushButton:hover{
        font: 63 12pt "Yu Gothic UI Semibold";
    }
""")

QPushButton_left2 = ("""
    QPushButton {
        text-align: left;
        padding-bottom: 4;
        padding-left: 8;
        color: rgb(255, 255, 255);
    }
    QPushButton:hover{
        font: 63 12pt "Yu Gothic UI Semibold";
    }
""")

QPushButton_right2 = ("""
    QPushButton {
        text-align: right;
        padding-right: 15;
        padding-bottom: 4;
        color: rgb(255, 255, 255);
    }
    QPushButton:hover{
        font: 63 12pt "Yu Gothic UI Semibold";
    }
""")

QPushButton = ("""
    QPushButton {
        color: rgb(25, 32, 80);
        border: none;
    }
""")

QLabel_heading = ("""
    QLabel {
        color: rgb(25, 32, 80);
    }
""")

QBackButton = ("""
    QPushButton {
        border: none;
    }
""")

QButtonFrame = ("""
    QPushButton {
        border: none;
        background-color: rgb(255, 255, 255);
    }
    QPushButton:hover{
       font: 63 12pt "Yu Gothic UI Semibold";
    }
""")

QStackedWidget = ("""
    QStackedWidget {
        background-color: rgb(194, 217, 255)
    }
""")

QListWidget = ("""
    QListWidget::item::selected {
        background-color: rgb(56, 65, 157);
        border: none;
        color: white;
        outline: 0;
    }
    QListWidget::item {
        text-align: center;
        padding: 15px;
        border: none;
        border-radius: 30px;
    }
    QListWidget {
        background-color: rgb(194, 217, 255);
        color: rgb(56, 65, 157);
        outline: 0;
        border: none;
    }
    QListWidget::item:hover {
        background-color: rgb(165, 195, 255);
        color: rgb(56, 65, 157);
    }
""")

QControlPanelButton = ("""
    QPushButton {
        border-radius: 13px;
        color: rgb(25, 32, 80);
        margin: 0px 10px;
    }
""")

QControlPanelMainButton = ("""
    QPushButton {
        border-radius: 13px;
        background-color: rgb(56, 65, 157);
        color: white;
        margin: 0px 10px;
    }
    QPushButton::disabled {
        background-color: rgba(56, 65, 157, 50);
    }
""")

QControlButton = ("""
    QPushButton {
        border-radius: 13px;
        color: rgb(25, 32, 80);
        margin: 0px 10px;
    }
""")

QLabel_device = ("""
    QLabel {
        padding-top: 10px;
        border-radius: 13px;
        color: rgb(25, 32, 80);
    }
""")

QLabel_2D_3D = ("""
    QLabel {
        padding: 5px;
        background-color: white;
        color: rgb(25, 32, 80);
        margin-left: 60px;
        margin-right: 60px;
        border-radius: 13px;
    }
    QToolTip {
        color: white; 
        background-color: rgb(56, 65, 157); 
        border: none;
    }
""")

QFrame_device = ("""
    QFrame {
        background-color: rgb(56, 65, 157);
        color: rgb(25, 32, 80);
    }
""")

QComboBox_device2 = ("""
    QComboBox {
        background-color: rgb(56, 65, 157);
        color: white;
        border-radius: 13px;
        padding: 15px;
        text-decoration: none;
    }
    QComboBox::drop-down {
        background-color: white;
        color: white;
    }
""")

QComboBox_device3 = ("""
    QComboBox {
        background-color: rgb(56, 65, 157);
        color: white;
        border-radius: 13px;
        padding: 20px;
    }
    QComboBox QAbstractItemView {
        border: 2px solid darkgray;
        selection-background-color: lightgray;
    }
""")

QDevicePreviewButton = ("""
    QPushButton {
        background-color: white;
        color: black;
        padding: 15px;
        border-radius: 13px;
        border: none;
    }
    QPushButton::disabled {
        color: rgba(0, 0, 0, 50);
    }
    QPushButton:hover {
        font: 63 12pt 'Yu Gothic UI Semibold';
    }
""")

QRefreshButton = ("""
    QPushButton:hover {
        font: 63 12pt 'Yu Gothic UI Semibold';
    }
    QPushButton {
        border: none;
    }
""")

QComboBox_device = ("""
    QComboBox {
        background-color: rgb(165, 195, 255);
        color: white;
        padding: 15px;
        border: none;
    }
    QComboBox::drop-down {
        width: 0px;
    }
    QComboBox QAbstractItemView {
        padding: 15px;
        background-color: white;
        color: rgb(25, 32, 80);
        selection-background-color: rgb(25, 32, 80);
        selection-color: white;
        outline: none;
    }
""")

QComboBox_selected = ("""
    QComboBox {
        background-color: rgb(165, 195, 255);
        color: rgb(25, 32, 80);
        padding: 15px;
        border: none;
    }
    QComboBox::drop-down {
        width: 0px;
    }
    QComboBox QAbstractItemView {
        padding: 15px;
        background-color: white;
        color: rgb(25, 32, 80);
        selection-background-color: rgb(25, 32, 80);
        selection-color: white;
        outline: none;
    }
""")

QScrollBar = ("""
    QScrollBar:vertical {
        border: none;
        background: transparent;
        width: 12px; /* adjust as needed */
        margin: 0px 0px 0px 0px;
    }
    QScrollBar::handle:vertical {
        background-color: rgb(56, 65, 157);
        min-height: 20px;
    }
    QScrollBar::handle:vertical:hover {
        background-color: rgb(25, 32, 80);
    }
    QScrollBar::sub-line:vertical {
        border: none;
        background: transparent;
        height: 10px;
        subcontrol-position: top;
        subcontrol-origin: margin;
    }
    QScrollBar::add-line:vertical {
        border: none;
        background: transparent;
        height: 10px;
        subcontrol-position: bottom;
        subcontrol-origin: margin;
    }
    QScrollBar::sub-line:vertical:hover,
    QScrollBar::add-line:vertical:hover {
        background: transparent;
    }
    QScrollBar::up-arrow:vertical,
    QScrollBar::down-arrow:vertical {
        border: none;
        width: 0px;
        height: 0px;
        background: none;
    }
    QScrollBar::add-page:vertical,
    QScrollBar::sub-page:vertical {
        background: none;
    }
    QScrollArea {
        border: none;
    }
    QLabel {
        color: rgb(25, 32, 80);
    }
    QLineEdit {
        padding: 7px;
        border: none;
        background-color: rgb(165, 195, 255);
    }
    QToolTip {
        color: white; 
        background-color: rgb(56, 65, 157); 
        border: none;
    }
""")

QLabel_Analysis = ("""
    QLabel {
        background-color: rgb(56,65,157); 
        color: rgba(255, 255, 255, 95);
    }
    QToolTip {
        color: white; 
        background-color: rgb(56, 65, 157); 
        border: none;
    }
""")


QScrollBar_Images = ("""
    QScrollBar:vertical {
        border: none;
        background: transparent;
        width: 12px; /* adjust as needed */
        margin: 0px 0px 0px 0px;
    }
    QScrollBar::handle:vertical {
        background-color: rgb(56, 65, 157);
        min-height: 20px;
    }
    QScrollBar::handle:vertical:hover {
        background-color: rgb(25, 32, 80);
    }
    QScrollBar::sub-line:vertical {
        border: none;
        background: transparent;
        height: 10px;
        subcontrol-position: top;
        subcontrol-origin: margin;
    }
    QScrollBar::add-line:vertical {
        border: none;
        background: transparent;
        height: 10px;
        subcontrol-position: bottom;
        subcontrol-origin: margin;
    }
    QScrollBar::sub-line:vertical:hover,
    QScrollBar::add-line:vertical:hover {
        background: transparent;
    }
    QScrollBar::up-arrow:vertical,
    QScrollBar::down-arrow:vertical {
        border: none;
        width: 0px;
        height: 0px;
        background: none;
    }
    QScrollBar::add-page:vertical,
    QScrollBar::sub-page:vertical {
        background: none;
    }
    QScrollArea {
        border: none;
    }
    QPushButton {
        color: rgb(25, 32, 80);
        border: none;
        padding: 5px;
        border-radius: 20px;
    }
    QToolTip {
        color: white; 
        background-color: rgb(56, 65, 157); 
        border: none;
    }
""")
