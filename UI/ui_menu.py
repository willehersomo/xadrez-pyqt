# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'menu_design.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(300, 250)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)
        self.label_id = QLabel(Form)
        self.label_id.setObjectName(u"label_id")

        self.verticalLayout.addWidget(self.label_id)

        self.input_id = QLineEdit(Form)
        self.input_id.setObjectName(u"input_id")

        self.verticalLayout.addWidget(self.input_id)

        self.label_nome = QLabel(Form)
        self.label_nome.setObjectName(u"label_nome")

        self.verticalLayout.addWidget(self.label_nome)

        self.input_nome = QLineEdit(Form)
        self.input_nome.setObjectName(u"input_nome")

        self.verticalLayout.addWidget(self.input_nome)

        self.label_cor = QLabel(Form)
        self.label_cor.setObjectName(u"label_cor")

        self.verticalLayout.addWidget(self.label_cor)

        self.combo_cor = QComboBox(Form)
        self.combo_cor.addItem("")
        self.combo_cor.addItem("")
        self.combo_cor.setObjectName(u"combo_cor")

        self.verticalLayout.addWidget(self.combo_cor)

        self.verticalSpacer = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.btn_entrar = QPushButton(Form)
        self.btn_entrar.setObjectName(u"btn_entrar")
        self.btn_entrar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.verticalLayout.addWidget(self.btn_entrar)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Xadrez - Menu Inicial", None))
        Form.setStyleSheet(QCoreApplication.translate("Form", u"QWidget { background-color: #2b2b2b; color: white; font-size: 14px; }", None))
        self.label_id.setText(QCoreApplication.translate("Form", u"ID da Partida:", None))
        self.input_id.setStyleSheet(QCoreApplication.translate("Form", u"background-color: #3b3b3b; border: 1px solid #555; padding: 4px;", None))
        self.label_nome.setText(QCoreApplication.translate("Form", u"Seu Nome:", None))
        self.input_nome.setStyleSheet(QCoreApplication.translate("Form", u"background-color: #3b3b3b; border: 1px solid #555; padding: 4px;", None))
        self.label_cor.setText(QCoreApplication.translate("Form", u"Escolha sua cor:", None))
        self.combo_cor.setItemText(0, QCoreApplication.translate("Form", u"Brancas", None))
        self.combo_cor.setItemText(1, QCoreApplication.translate("Form", u"Pretas", None))

        self.combo_cor.setStyleSheet(QCoreApplication.translate("Form", u"background-color: #3b3b3b; border: 1px solid #555; padding: 4px;", None))
        self.btn_entrar.setStyleSheet(QCoreApplication.translate("Form", u"background-color: #4CAF50; color: white; font-weight: bold; padding: 8px; border-radius: 4px;", None))
        self.btn_entrar.setText(QCoreApplication.translate("Form", u"Entrar na Partida", None))
    # retranslateUi

