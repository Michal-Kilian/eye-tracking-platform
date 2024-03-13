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
               "    color: red;\n"
               "    border: none;\n"
               "}\n"
               'QListWidget::item {\n'
               '    text-align: center;\n'
               '}\n'
               "QListWidget {\n"
               "    background-color: rgb(56, 65, 157);\n"
               "    color: white;\n"
               "    border: none;\n"
               "}\n"
               'QListWidget::item::hover {\n'
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
                           "    color: white\n"
                           "}\n"
                           "QPushButton::disabled {\n"
                           "    background-color: rgb(56, 65, 157, 50);\n"
                           "}")

QLabel_device = ("QLabel {\n"
                 "    padding: 10px;\n"
                 "    border-radius: 13px;\n"
                 "    color: rgb(25, 32, 80);\n"
                 "}")

QFrame_device = ("QFrame {\n"
                 "    background-color: rgb(56, 65, 157);\n"
                 "    color: rgb(25, 32, 80);\n"
                 "}")

QComboBox_device = ("QComboBox {\n"
                    "    background-color: rgb(56, 65, 157);\n"
                    "    color: white;\n"
                    "    border-radius: 13px;\n"
                    "    padding: 20px;\n"
                    "    text-decoration: none;\n"
                    "}\n"
                    "QComboBox::drop-down {\n"
                    "    background-color: white;\n"
                    "    color: white;\n"
                    "}\n")
