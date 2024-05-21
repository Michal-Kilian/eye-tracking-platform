from PyQt5 import QtGui
from PyQt5.QtWidgets import QGraphicsDropShadowEffect


class Colors:
    PrimaryBackgroundColor: str = "rgb(194, 217, 255)"
    PrimaryTextColor: str = "rgb(25, 32, 80)"
    PrimaryButtonColor: str = "rgb(56, 65, 157)"
    SecondaryBackgroundColor: str = "rgb(165, 195, 255)"
    White: str = "rgb(255, 255, 255)"
    PrimaryButtonDisabledColor: str = "rgba(56, 65, 157, 50)"
    SecondaryButtonDisabledColor: str = "rgba(255, 255, 255, 95)"
    BlackHalfOpacity: str = "rgba(0, 0, 0, 50)"


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
    StackedWidget: str = (f"""
        QStackedWidget {{
            background-color: {Colors.PrimaryBackgroundColor};
        }}
    """)
    WidgetBackgroundColor: str = (f"""
        QWidget {{
            background-color: {Colors.PrimaryBackgroundColor};
        }}
        """)
    BackAndExitButton: str = ("""
        QPushButton {
            border: none;
        }
    """)
    Heading: str = (f"""
        QLabel {{
            color: {Colors.PrimaryTextColor};
        }}
    """)
    ScrollBar: str = (f"""
        QScrollBar:vertical {{
            border: none;
            background: transparent;
            width: 12px;
            margin: 0px 0px 0px 0px;
        }}
        QScrollBar::handle:vertical {{
            background-color: {Colors.PrimaryButtonColor};
            min-height: 20px;
        }}
        QScrollBar::handle:vertical:hover {{
            background-color: {Colors.PrimaryTextColor};
        }}
        QScrollBar::sub-line:vertical {{
            border: none;
            background: transparent;
            height: 10px;
            subcontrol-position: top;
            subcontrol-origin: margin;
        }}
        QScrollBar::add-line:vertical {{
            border: none;
            background: transparent;
            height: 10px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
        }}
        QScrollBar::sub-line:vertical:hover,
        QScrollBar::add-line:vertical:hover {{
            background: transparent;
        }}
        QScrollBar::up-arrow:vertical,
        QScrollBar::down-arrow:vertical {{
            border: none;
            width: 0px;
            height: 0px;
            background: none;
        }}
        QScrollBar::add-page:vertical,
        QScrollBar::sub-page:vertical {{
            background: none;
        }}
        QScrollArea {{
            border: none;
        }}
        QLabel {{
            color: {Colors.PrimaryTextColor};
        }}
        QLineEdit {{
            padding: 7px;
            border: none;
            background-color: {Colors.SecondaryBackgroundColor};
        }}
        QToolTip {{
            color: {Colors.White}; 
            background-color: {Colors.PrimaryButtonColor}; 
            border: none;
        }}
    """)
    ButtonFrame: str = (f"""
        QPushButton {{
            border: none;
            background-color: {Colors.White};
        }}
        QPushButton:hover{{
           font: 63 12pt "Yu Gothic UI Semibold";
        }}
    """)
    ControlPanelButton: str = (f"""
        QPushButton {{
            border-radius: 13px;
            color: {Colors.PrimaryTextColor};
            margin: 0px 10px;
        }}
    """)
    ControlPanelMainButton: str = (f"""
        QPushButton {{
            border-radius: 13px;
            background-color: {Colors.PrimaryButtonColor};
            color: {Colors.White};
            margin: 0px 10px;
        }}
        QPushButton::disabled {{
            background-color: {Colors.PrimaryButtonDisabledColor};
        }}
        QPushButton:hover {{
            font: 63 12pt 'Yu Gothic UI Semibold';
        }}
    """)
    ControlButton: str = (f"""
        QPushButton {{
            border-radius: 13px;
            color: {Colors.PrimaryTextColor};
            margin: 0px 10px;
        }}
    """)
    WhiteLabel: str = (f"""
        QLabel {{
            padding: 5px;
            background-color: {Colors.White};
            color: {Colors.PrimaryTextColor};
            margin-left: 60px;
            margin-right: 60px;
            border-radius: 13px;
        }}
        QToolTip {{
            color: {Colors.White}; 
            background-color: {Colors.PrimaryButtonColor}; 
            border: none;
        }}
    """)
    WhiteBackgroundColor: str = f"background-color: {Colors.White};"
    NoStyleSheet: str = ""
    BackgroundAndWhiteColor: str = f"background-color: {Colors.PrimaryButtonColor}; color: {Colors.White};"
    MarginTop30: str = "margin-top: 30px;"
    Margin20: str = "margin: 20px;"
    Margin20AndBackground: str = f"margin: 20px; background-color: {Colors.PrimaryBackgroundColor};"
    GazePointOverlay: str = "QLabel {background-color: red; border-radius: 15px}"


class HomeScreenStyleSheet:
    ButtonFrame: str = (f"""
        QPushButton {{
            background-color: {Colors.PrimaryButtonColor};
            color: {Colors.White};
            border: 0;
        }}
    """)
    ButtonLeftUp: str = (f"""
        QPushButton {{
            text-align: left;
            padding-bottom: 4;
            padding-left: 8;
            color: {Colors.White};
        }}
        QPushButton:hover{{
            font: 63 12pt "Yu Gothic UI Semibold";
        }}
    """)
    ButtonRightUp: str = (f"""
        QPushButton {{
            text-align: right;
            padding-right: 15;
            padding-bottom: 4;
            color: {Colors.White};
        }}
        QPushButton:hover{{
            font: 63 12pt "Yu Gothic UI Semibold";
        }}
    """)
    ButtonLeftDown: str = (f"""
        QPushButton {{
            text-align: left;
            padding-bottom: 4;
            padding-left: 8;
            color: {Colors.White};
        }}
        QPushButton:hover{{
            font: 63 12pt "Yu Gothic UI Semibold";
        }}
    """)
    ButtonRightDown: str = (f"""
        QPushButton {{
            text-align: right;
            padding-right: 15;
            padding-bottom: 4;
            color: {Colors.White};
        }}
        QPushButton:hover{{
            font: 63 12pt "Yu Gothic UI Semibold";
        }}
    """)


class AnalysisScreenStyleSheet:
    DeviceStatusLabel: str = f"background-color: {Colors.SecondaryBackgroundColor}; color: {Colors.PrimaryTextColor};"
    DeviceStatusLabelNoData: str = f"background-color: {Colors.SecondaryBackgroundColor}; color: {Colors.White};"
    LabelWithTooltip: str = (f"""
        QLabel {{
            background-color: {Colors.PrimaryButtonColor}; 
            color: {Colors.SecondaryButtonDisabledColor};
        }}
        QToolTip {{
            color: {Colors.White}; 
            background-color: {Colors.PrimaryButtonColor}; 
            border: none;
        }}
    """)
    ImageScrollBar: str = (f"""
        QScrollBar:vertical {{
            border: none;
            background: transparent;
            width: 12px;
            margin: 0px 0px 0px 0px;
        }}
        QScrollBar::handle:vertical {{
            background-color: {Colors.PrimaryButtonColor};
            min-height: 20px;
        }}
        QScrollBar::handle:vertical:hover {{
            background-color: {Colors.PrimaryTextColor};
        }}
        QScrollBar::sub-line:vertical {{
            border: none;
            background: transparent;
            height: 10px;
            subcontrol-position: top;
            subcontrol-origin: margin;
        }}
        QScrollBar::add-line:vertical {{
            border: none;
            background: transparent;
            height: 10px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
        }}
        QScrollBar::sub-line:vertical:hover,
        QScrollBar::add-line:vertical:hover {{
            background: transparent;
        }}
        QScrollBar::up-arrow:vertical,
        QScrollBar::down-arrow:vertical {{
            border: none;
            width: 0px;
            height: 0px;
            background: none;
        }}
        QScrollBar::add-page:vertical,
        QScrollBar::sub-page:vertical {{
            background: none;
        }}
        QScrollArea {{
            border: none;
        }}
        QPushButton {{
            color: {Colors.PrimaryTextColor};
            border: none;
            padding: 5px;
            border-radius: 20px;
        }}
        QToolTip {{
            color: {Colors.White}; 
            background-color: {Colors.PrimaryButtonColor}; 
            border: none;
        }}
    """)


class DeviceScreenStyleSheet:
    ComboBox: str = (f"""
        QComboBox {{
            background-color: {Colors.SecondaryBackgroundColor};
            color: {Colors.White};
            padding: 15px;
            border: none;
        }}
        QComboBox::drop-down {{
            width: 0px;
        }}
        QComboBox QAbstractItemView {{
            padding: 15px;
            background-color: {Colors.White};
            color: {Colors.PrimaryTextColor};
            selection-background-color: {Colors.PrimaryTextColor};
            selection-color: {Colors.White};
            outline: none;
        }}
    """)
    Label: str = (f"""
        QLabel {{
            padding-top: 10px;
            border-radius: 13px;
            color: {Colors.PrimaryTextColor};
        }}
    """)
    Color: str = f"color: {Colors.PrimaryButtonColor};"
    RefreshButton: str = ("""
        QPushButton:hover {
            font: 63 12pt 'Yu Gothic UI Semibold';
        }
        QPushButton {
            border: none;
        }
    """)
    DevicePreviewButton: str = (f"""
        QPushButton {{
            background-color: {Colors.White};
            color: black;
            padding: 15px;
            border-radius: 13px;
            border: none;
        }}
        QPushButton::disabled {{
            color: {Colors.BlackHalfOpacity};
        }}
        QPushButton:hover {{
            font: 63 12pt 'Yu Gothic UI Semibold';
        }}
    """)
    ComboBoxSelected: str = (f"""
        QComboBox {{
            background-color: {Colors.SecondaryBackgroundColor};
            color: {Colors.PrimaryTextColor};
            padding: 15px;
            border: none;
        }}
        QComboBox::drop-down {{
            width: 0px;
        }}
        QComboBox QAbstractItemView {{
            padding: 15px;
            background-color: {Colors.White};
            color: {Colors.PrimaryTextColor};
            selection-background-color: {Colors.PrimaryTextColor};
            selection-color: {Colors.White};
            outline: none;
        }}
    """)


class DialogStyleSheet:
    ButtonOK: str = (f"background-color: {Colors.PrimaryButtonColor}; padding: 15px 15px; margin: 3px; color: "
                     f"{Colors.White}; border-radius: 13px;")
    ButtonCancel: str = (f"background-color: {Colors.PrimaryBackgroundColor}; padding: 15px 15px; margin: 3px; color: "
                         f"{Colors.PrimaryTextColor}; border-radius: 13px;")


class ModeSelectionScreenStyleSheet:
    IconButton: str = (f"QPushButton {{text-align: center; background-color: {Colors.White}; border-radius: 105; "
                       f"border: 5px solid {Colors.White};}}")
    IconButtonSelected: str = (f"QPushButton {{text-align: center; background-color: {Colors.White}; border-radius: "
                               f"105; border: 4px solid {Colors.PrimaryTextColor};}}")
    TextLabel: str = f"QLabel {{color: {Colors.PrimaryButtonColor} border: none; outline: none;}}"
    LabelSelected: str = f"QLabel {{color: {Colors.PrimaryTextColor};}}"
    Label: str = f"QLabel {{color: {Colors.PrimaryButtonColor};}}"


class VisualizationWindowStyleSheet:
    Image: str = "background-color: {Colors.GlobalBackgroundColor};"
    TransparentExitButton: str = "QPushButton {border: none; background: transparent;}"
    ColorButton1: str = (f"""
        QPushButton {{
            border: 5px solid {Colors.PrimaryButtonColor};
            background-color: black;
            border-radius: 25px;
        }}
    """)
    ColorButton2: str = (f"""
        QPushButton {{
            border: 5px solid {Colors.PrimaryButtonColor};
            background-color: {Colors.White};
            border-radius: 25px;
        }}
    """)
    ThresholdInput: str = (f"QLineEdit {{padding: 7px; border: 3px solid {Colors.PrimaryButtonColor}; background"
                           f"-color: {Colors.SecondaryBackgroundColor};}}")

    @staticmethod
    def ButtonColorPicked(color_name: str):
        return (f"""
        QPushButton {{
            background-color: {color_name}; 
            border: 5px solid {Colors.PrimaryButtonColor}; 
            border-radius: 25px;
        }}
        """)


class PreferencesScreenStyleSheet:
    LabelWithTooltip: str = (f"""
        QLabel {{
            background-color: {Colors.White}; 
            color: {Colors.PrimaryTextColor};
            border-radius: 30px;
        }}
        QToolTip {{
            color: {Colors.White}; 
            background-color: {Colors.PrimaryButtonColor}; 
            border: none;
        }}
    """)


class RecordsScreenStyleSheet:
    IdLabel: str = f"margin-bottom: 30px; background-color: {Colors.White}; padding: 15px; border-radius: 30px;"
    DetailLabel: str = (f"""
        QLabel {{
            background-color: {Colors.SecondaryBackgroundColor};
            padding: 5px;
            border-radius: 20px;
        }}
    """)
    ItemWidget: str = f"background-color: {Colors.SecondaryBackgroundColor}; border-radius: 25px;"
    DetailButton: str = (f"QPushButton {{background-color: {Colors.White}; color: {Colors.PrimaryTextColor}; padding: "
                         f"10px;}} QPushButton:hover {{font: 63 12pt 'Yu Gothic UI Semibold';}}")
