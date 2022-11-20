# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'enum_w.ui'
##
## Created by: Qt User Interface Compiler version 6.3.2
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout,
    QLabel, QSizePolicy, QWidget)

class Ui_EnumFrame(QObject):
    def setupUi(self, EnumFrame):
        if not EnumFrame.objectName():
            EnumFrame.setObjectName(u"EnumFrame")
        EnumFrame.resize(351, 40)
        EnumFrame.setMaximumSize(QSize(16777215, 40))
        EnumFrame.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout = QHBoxLayout(EnumFrame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.fieldLabel = QLabel(EnumFrame)
        self.fieldLabel.setObjectName(u"fieldLabel")

        self.horizontalLayout.addWidget(self.fieldLabel)

        self.valuesComboBox = QComboBox(EnumFrame)
        self.valuesComboBox.setObjectName(u"valuesComboBox")
        self.valuesComboBox.setFrame(True)

        self.horizontalLayout.addWidget(self.valuesComboBox)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 2)

        self.retranslateUi(EnumFrame)

        QMetaObject.connectSlotsByName(EnumFrame)
    # setupUi

    def retranslateUi(self, EnumFrame):
        EnumFrame.setWindowTitle(QCoreApplication.translate("EnumFrame", u"Frame", None))
        self.fieldLabel.setText(QCoreApplication.translate("EnumFrame", u"TextLabel", None))
    # retranslateUi

