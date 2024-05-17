from PyQt5 import QtGui
from PyQt5.QtWidgets import QGraphicsDropShadowEffect


class Fonts:
    @staticmethod
    def HeadingFont() -> QtGui.QFont:
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        return font

    @staticmethod
    def TextFont() -> QtGui.QFont:
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        return font

    @staticmethod
    def HeadingTextFont() -> QtGui.QFont:
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(False)
        return font

    @staticmethod
    def ComboBoxFont() -> QtGui.QFont:
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setPointSize(9)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        return font


class GraphicEffects:
    @staticmethod
    def Shadow(blur_size) -> QGraphicsDropShadowEffect:
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(blur_size)
        return shadow


class GlobalStyleSheet:
    StackedWidget: str = ("""
        QStackedWidget {
            background-color: rgb(194, 217, 255)
        }
    """)
    WidgetBackgroundColor: str = ("""
        QWidget {
            background-color: rgb(194, 217, 255);
        }
        """)
    BackAndExitButton: str = ("""
        QPushButton {
            border: none;
        }
    """)
    Heading: str = ("""
        QLabel {
            color: rgb(25, 32, 80);
        }
    """)
    ScrollBar: str = ("""
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
    ButtonFrame: str = ("""
        QPushButton {
            border: none;
            background-color: rgb(255, 255, 255);
        }
        QPushButton:hover{
           font: 63 12pt "Yu Gothic UI Semibold";
        }
    """)
    ControlPanelButton: str = ("""
        QPushButton {
            border-radius: 13px;
            color: rgb(25, 32, 80);
            margin: 0px 10px;
        }
    """)
    ControlPanelMainButton: str = ("""
        QPushButton {
            border-radius: 13px;
            background-color: rgb(56, 65, 157);
            color: white;
            margin: 0px 10px;
        }
        QPushButton::disabled {
            background-color: rgba(56, 65, 157, 50);
        }
        QPushButton:hover {
            font: 63 12pt 'Yu Gothic UI Semibold'
        }
    """)
    ControlButton: str = ("""
        QPushButton {
            border-radius: 13px;
            color: rgb(25, 32, 80);
            margin: 0px 10px;
        }
    """)
    WhiteLabel: str = ("""
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
    WhiteBackgroundColor: str = "background-color: white;"
    NoStyleSheet: str = ""
    BackgroundAndWhiteColor: str = "background-color: rgb(56, 65, 157); color: white;"
    MarginTop30: str = "margin-top: 30px;"
    Margin20: str = "margin: 20px"
    Margin20AndBackground: str = "margin: 20px; background-color: rgb(194, 217, 255);"
    GazePointOverlay: str = "QLabel {background-color: red; border-radius: 15px}"


class HomeScreenStyleSheet:
    ButtonFrame: str = ("""
        QPushButton {
            background-color: rgb(56,65,157);
            color: white;
            border: 0;
        }
    """)
    ButtonLeftUp: str = ("""
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
    ButtonRightUp: str = ("""
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
    ButtonLeftDown: str = ("""
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
    ButtonRightDown: str = ("""
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


class AnalysisScreenStyleSheet:
    DeviceStatusLabel: str = "background-color: rgb(165, 195, 255); color: rgb(25, 32, 80);"
    DeviceStatusLabelNoData: str = "background-color: rgb(165, 195, 255); color: white;"
    LabelWithTooltip: str = ("""
        QLabel {
            background-color: rgb(56, 65, 157); 
            color: rgba(255, 255, 255, 95);
        }
        QToolTip {
            color: white; 
            background-color: rgb(56, 65, 157); 
            border: none;
        }
    """)
    ImageScrollBar: str = ("""
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


class DeviceScreenStyleSheet:
    ComboBox: str = ("""
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
    Label: str = ("""
        QLabel {
            padding-top: 10px;
            border-radius: 13px;
            color: rgb(25, 32, 80);
        }
    """)
    Color: str = "color: rgb(56, 65, 157);"
    RefreshButton: str = ("""
        QPushButton:hover {
            font: 63 12pt 'Yu Gothic UI Semibold';
        }
        QPushButton {
            border: none;
        }
    """)
    DevicePreviewButton: str = ("""
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
    ComboBoxSelected: str = ("""
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


class DialogStyleSheet:
    ButtonOK: str = ("background-color: rgb(56, 65, 157); padding: 15px 15px; margin: 3px; color: white;"
                     "border-radius: 13px;")
    ButtonCancel: str = ("background-color: rgb(194, 217, 255); padding: 15px 15px; margin: 3px; color: rgb(25, 32, "
                         "80); border-radius: 13px;")


class ModeSelectionScreenStyleSheet:
    IconButton: str = ("QPushButton {text-align: center; background-color: white; border-radius: 105; border: 5px "
                       "solid white;}")
    IconButtonSelected: str = ("QPushButton {text-align: center; background-color: white; border-radius: 105; border: "
                               "4px solid rgb(25, 32, 80);}")
    TextLabel: str = "QLabel {color: rgb(56,65,157); border: none; outline: none;}"
    LabelSelected: str = "QLabel {color: rgb(25, 32, 80);}"
    Label: str = "QLabel {color: rgb(56, 65, 157);}"


class VisualizationWindowStyleSheet:
    Image: str = "background-color: rgb(194, 217, 255);"
    TransparentExitButton: str = "QPushButton {border: none; background: transparent}"
    ColorButton1: str = ("""
        QPushButton {
            border: 5px solid rgb(56, 65, 157);
            background-color: black;
            border-radius: 25px;
        }
    """)
    ColorButton2: str = ("""
        QPushButton {
            border: 5px solid rgb(56, 65, 157);
            background-color: white;
            border-radius: 25px;
        }
    """)
    ThresholdInput: str = ("QLineEdit {padding: 7px; border: 3px solid rgb(56, 65, 157); background-color: rgb(165, "
                           "195, 255);}")

    @staticmethod
    def ButtonColorPicked(color_name: str):
        return (f"""
        QPushButton {{
            background-color: {color_name}; 
            border: 5px solid rgb(56, 65, 157); 
            border-radius: 25px;
        }}
        """)


class PreferencesScreenStyleSheet:
    LabelWithTooltip: str = ("""
        QLabel {
            background-color: rgb(56, 65, 157); 
            color: rgba(255, 255, 255, 95);
        }
        QToolTip {
            color: white; 
            background-color: rgb(56, 65, 157); 
            border: none;
        }
    """)


class RecordsScreenStyleSheet:
    IdLabel: str = "margin-bottom: 30px; background-color: white; padding: 15px; border-radius: 30px;"
    DetailLabel: str = ("""
        QLabel {
            background-color: rgb(165, 195, 255);
            padding: 5px;
            border-radius: 20px;
        }
    """)
    ItemWidget: str = "background-color: rgb(165, 195, 255); border-radius: 25px;"
    DetailButton: str = ("QPushButton {background-color: white; color: rgb(25, 32, 80); padding: 10px;} "
                         "QPushButton:hover {font: 63 12pt 'Yu Gothic UI Semibold';}")
