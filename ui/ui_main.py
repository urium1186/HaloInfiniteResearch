# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.3.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QLineEdit,
    QMainWindow, QMenu, QMenuBar, QScrollArea,
    QSizePolicy, QStatusBar, QTreeView, QVBoxLayout,
    QWidget)

class Ui_MainWindow(QObject):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.actionCoatings = QAction(MainWindow)
        self.actionCoatings.setObjectName(u"actionCoatings")
        self.actionFrom_Json_Them = QAction(MainWindow)
        self.actionFrom_Json_Them.setObjectName(u"actionFrom_Json_Them")
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionSetting = QAction(MainWindow)
        self.actionSetting.setObjectName(u"actionSetting")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")

        self.verticalLayout_2.addWidget(self.lineEdit)

        self.treeView = QTreeView(self.centralwidget)
        self.treeView.setObjectName(u"treeView")

        self.verticalLayout_2.addWidget(self.treeView)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 516, 537))
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout.addWidget(self.scrollArea)

        self.horizontalLayout.setStretch(1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        self.menuMenu = QMenu(self.menubar)
        self.menuMenu.setObjectName(u"menuMenu")
        self.menuTools = QMenu(self.menubar)
        self.menuTools.setObjectName(u"menuTools")
        self.menuExports = QMenu(self.menuTools)
        self.menuExports.setObjectName(u"menuExports")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuMenu.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menuMenu.addSeparator()
        self.menuMenu.addAction(self.actionOpen)
        self.menuMenu.addAction(self.actionSetting)
        self.menuTools.addAction(self.menuExports.menuAction())
        self.menuExports.addSeparator()
        self.menuExports.addAction(self.actionCoatings)
        self.menuExports.addAction(self.actionFrom_Json_Them)

        self.retranslateUi(MainWindow)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionCoatings.setText(QCoreApplication.translate("MainWindow", u"Coatings", None))
        self.actionFrom_Json_Them.setText(QCoreApplication.translate("MainWindow", u"From Json Theme", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.actionSetting.setText(QCoreApplication.translate("MainWindow", u"Setting", None))
        self.menuMenu.setTitle(QCoreApplication.translate("MainWindow", u"Menu", None))
        self.menuTools.setTitle(QCoreApplication.translate("MainWindow", u"Tools", None))
        self.menuExports.setTitle(QCoreApplication.translate("MainWindow", u"Exports", None))
    # retranslateUi

