from PyQt5 import QtGui


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


def qcombobox_font() -> QtGui.QFont:
    font = QtGui.QFont()
    font.setFamily("Yu Gothic UI Semibold")
    font.setPointSize(9)
    font.setBold(True)
    font.setItalic(False)
    font.setWeight(75)
    return font


QWidget_background_color = ("QWidget {\n"
                            "   background-color: rgb(194, 217, 255);\n"
                            "}")

QPushButton_frame = ("QPushButton {\n"
                     "    background-color: rgb(56,65,157);\n"
                     "    color: white;\n"
                     "    border: 0;\n"
                     "}")

QPushButton_left1 = ("QPushButton {\n"
                     "   text-align: left;\n"
                     "   padding-bottom: 4;\n"
                     "   padding-left: 8;\n"
                     "   color: rgb(255, 255, 255);\n"
                     "}\n"
                     'QPushButton:hover{\n'
                     '	font: 63 12pt "Yu Gothic UI Semibold";\n'
                     '}')

QPushButton_right1 = ("QPushButton {\n"
                      "    text-align: right;\n"
                      "    padding-right: 15;\n"
                      "    padding-bottom: 4;\n"
                      "    color: rgb(255, 255, 255);\n"
                      "}\n"
                      'QPushButton:hover{\n'
                      '	font: 63 12pt "Yu Gothic UI Semibold";\n'
                      '}'
                      )

QPushButton_left2 = ("QPushButton {\n"
                     "    text-align: left;\n"
                     "    padding-bottom: 4;\n"
                     "    padding-left: 8;\n"
                     "    color: rgb(255, 255, 255);\n"
                     "}\n"
                     'QPushButton:hover{\n'
                     '	font: 63 12pt "Yu Gothic UI Semibold";\n'
                     '}'
                     )

QPushButton_right2 = ("QPushButton {\n"
                      "    text-align: right;\n"
                      "    padding-right: 15;\n"
                      "    padding-bottom: 4;\n"
                      "    color: rgb(255, 255, 255);\n"
                      "}\n"
                      'QPushButton:hover{\n'
                      '	   font: 63 12pt "Yu Gothic UI Semibold";\n'
                      '}')

QPushButton = ("QPushButton {\n"
               "    color: rgb(25, 32, 80);\n"
               "    border: none\n"
               "}\n")

QLabel_heading = ("QLabel {\n"
                  "    color: rgb(25, 32, 80);\n"
                  "}")

QBackButton = ("QPushButton {\n"
               "    border: none;\n"
               "}")

QButtonFrame = ("QPushButton {\n"
                "    border: none;\n"
                "    background-color: rgb(255, 255, 255);\n"
                "}\n"
                'QPushButton:hover{\n'
                '	   font: 63 12pt "Yu Gothic UI Semibold";\n'
                '}')

QStackedWidget = ("QStackedWidget {\n"
                  "    background-color: rgb(194, 217, 255)\n"
                  "}\n")

QListWidget = ("QListWidget::item::selected {\n"
               "    background-color: rgb(25, 32, 80);\n"
               "    border: none;\n"
               "}\n"
               'QListWidget::item {\n'
               '    text-align: center;\n'
               '    padding: 15px;\n'
               '}\n'
               "QListWidget {\n"
               "    background-color: rgb(56, 65, 157);\n"
               "    color: white;\n"
               "    border: none;\n"
               "}\n"
               'QListWidget::item:hover {\n'
               '    background-color: rgb(25, 32, 80);\n'
               '}\n')

QControlPanelButton = ("QPushButton {\n"
                       "    border-radius: 13px;\n"
                       "    color: rgb(25, 32, 80);\n"
                       "    margin: 0px 10px;\n"
                       "}")

QControlPanelMainButton = ("QPushButton {\n"
                           "    border-radius: 13px;\n"
                           "    background-color: rgb(56, 65, 157);\n"
                           "    color: white;\n"
                           "    margin: 0px 10px;\n"
                           "}\n"
                           "QPushButton::disabled {\n"
                           "    background-color: rgba(56, 65, 157, 50);\n"
                           "}")

QLabel_device = ("QLabel {\n"
                 "    padding-top: 10px;\n"
                 "    border-radius: 13px;\n"
                 "    color: rgb(25, 32, 80);\n"
                 "}")

QLabel_2D_3D = ("QLabel {\n"
                "    padding: 5px;\n"
                "    background-color: white;\n"
                "    color: rgb(25, 32, 80);\n"
                "    margin-left: 60px;\n"  
                "    margin-right: 60px;\n"  
                "    border-radius: 13px;\n"
                "}")

QFrame_device = ("QFrame {\n"
                 "    background-color: rgb(56, 65, 157);\n"
                 "    color: rgb(25, 32, 80);\n"
                 "}")

QComboBox_device2 = ("QComboBox {\n"
                     "    background-color: rgb(56, 65, 157);\n"
                     "    color: white;\n"
                     "    border-radius: 13px;\n"
                     "    padding: 15px;\n"
                     "    text-decoration: none;\n"
                     "}\n"
                     "QComboBox::drop-down {\n"
                     "    background-color: white;\n"
                     "    color: white;\n"
                     "}\n")

QComboBox_device3 = ("QComboBox {\n"
                     "    background-color: rgb(56, 65, 157);\n"
                     "    color: white;\n"
                     "    border-radius: 13px;\n"
                     "    padding: 20px;\n"
                     "}\n"
                     "QComboBox QAbstractItemView {\n"
                     "    border: 2px solid darkgray;\n"
                     "    selection-background-color: lightgray;\n"
                     "}\n")

QDevicePreviewButton = ("QPushButton {\n"
                        "    background-color: white;\n"
                        "    color: black;\n"
                        "    padding: 15px;\n"
                        "    border-radius: 13px;\n"
                        "    border: none;\n"
                        "}\n"
                        "QPushButton::disabled {\n"
                        "    color: rgba(0, 0, 0, 50);\n"
                        "}\n"
                        "QPushButton:hover {\n"
                        "	 font: 63 12pt 'Yu Gothic UI Semibold';\n"
                        "}\n")

QRefreshButton = ("QPushButton:hover {\n"
                  "	 font: 63 12pt 'Yu Gothic UI Semibold';\n"
                  "}\n"
                  "QPushButton {"
                  "border: none;"
                  "}")

QComboBox_device = (
    '''
QComboBox {
    background-color: rgb(165, 195, 255);
    color: white;
    padding: 15px;
    border: none;
}

QComboBox:editable {

}

/* QComboBox gets the "on" state when the popup is open */
QComboBox:!editable:on, QComboBox::drop-down:editable:on {
    
}

QComboBox:on { /* shift the text when the popup opens */
    
}

QComboBox::drop-down {
    width: 0px;
}

QComboBox::down-arrow {
    
}

QComboBox::down-arrow:on { /* shift the arrow when popup is open */
    
}
QComboBox QAbstractItemView {
    padding: 15px;
    background-color: white;
    color: rgb(25, 32, 80);
    selection-background-color: rgb(25, 32, 80);
    selection-color: white;
    outline: none;
}
'''
)

QScrollBar = ("""
    QScrollBar:vertical {
        border: none;
        background: transparent;
        width: 12px; /* adjust as needed */
        margin: 0px 0px 0px 0px;
    }

    QScrollBar::handle:vertical {
        background-color: rgb(165, 195, 255);
        min-height: 20px;
    }

    QScrollBar::handle:vertical:hover {
        background-color: rgb(56, 65, 157); /* Color of the scrollbar handle when hovered */
    }

    QScrollBar::sub-line:vertical {
        border: none; /* Remove border from the sub-line */
        background: transparent;
        height: 10px; /* adjust as needed */
        subcontrol-position: top;
        subcontrol-origin: margin;
    }

    QScrollBar::add-line:vertical {
        border: none; /* Remove border from the add-line */
        background: transparent;
        height: 10px; /* adjust as needed */
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
        color: red;
    }
    QLineEdit {
        padding: 5px;
    }
""")
