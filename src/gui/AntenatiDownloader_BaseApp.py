# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'AntenatiDownloader_BaseApp.ui'
##
## Created by: Qt User Interface Compiler version 6.2.3
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
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QMainWindow, QProgressBar,
    QPushButton, QRadioButton, QSizePolicy, QSpacerItem,
    QStatusBar, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(946, 586)
        MainWindow.setWindowTitle(u"AntenatiDownloader")
        icon = QIcon()
        icon.addFile(u":/img/logo-antenati.png", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.pushButton_lang = QPushButton(self.centralwidget)
        self.pushButton_lang.setObjectName(u"pushButton_lang")
        self.pushButton_lang.setMinimumSize(QSize(60, 40))
        self.pushButton_lang.setLocale(QLocale(QLocale.Italian, QLocale.Italy))
        icon1 = QIcon()
        icon1.addFile(u":/img/logo-lang.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_lang.setIcon(icon1)
        self.pushButton_lang.setIconSize(QSize(30, 30))

        self.horizontalLayout_4.addWidget(self.pushButton_lang)

        self.horizontalSpacer_4 = QSpacerItem(408, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)

        self.pushButton_help = QPushButton(self.centralwidget)
        self.pushButton_help.setObjectName(u"pushButton_help")
        self.pushButton_help.setMinimumSize(QSize(60, 40))
        self.pushButton_help.setLocale(QLocale(QLocale.Italian, QLocale.Italy))
        icon2 = QIcon()
        icon2.addFile(u":/img/logo-help.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_help.setIcon(icon2)
        self.pushButton_help.setIconSize(QSize(30, 30))

        self.horizontalLayout_4.addWidget(self.pushButton_help)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.verticalSpacer_2 = QSpacerItem(20, 13, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_linkManifest = QLabel(self.centralwidget)
        self.label_linkManifest.setObjectName(u"label_linkManifest")
        font = QFont()
        font.setPointSize(12)
        self.label_linkManifest.setFont(font)
        self.label_linkManifest.setLocale(QLocale(QLocale.Italian, QLocale.Italy))

        self.horizontalLayout_3.addWidget(self.label_linkManifest, 0, Qt.AlignLeft)

        self.horizontalSpacer_3 = QSpacerItem(418, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_1 = QHBoxLayout()
        self.horizontalLayout_1.setObjectName(u"horizontalLayout_1")
        self.lineEdit_linkManifest = QLineEdit(self.centralwidget)
        self.lineEdit_linkManifest.setObjectName(u"lineEdit_linkManifest")

        self.horizontalLayout_1.addWidget(self.lineEdit_linkManifest)

        self.pushButton_browseFile = QPushButton(self.centralwidget)
        self.pushButton_browseFile.setObjectName(u"pushButton_browseFile")
        icon3 = QIcon()
        icon3.addFile(u":/img/logo-browse.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_browseFile.setIcon(icon3)
        self.pushButton_browseFile.setIconSize(QSize(16, 16))

        self.horizontalLayout_1.addWidget(self.pushButton_browseFile)


        self.verticalLayout.addLayout(self.horizontalLayout_1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_resultsDir = QLabel(self.centralwidget)
        self.label_resultsDir.setObjectName(u"label_resultsDir")
        self.label_resultsDir.setFont(font)
        self.label_resultsDir.setLocale(QLocale(QLocale.Italian, QLocale.Italy))

        self.horizontalLayout.addWidget(self.label_resultsDir)

        self.horizontalSpacer_5 = QSpacerItem(418, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_5)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.lineEdit_resultsDir = QLineEdit(self.centralwidget)
        self.lineEdit_resultsDir.setObjectName(u"lineEdit_resultsDir")

        self.horizontalLayout_5.addWidget(self.lineEdit_resultsDir)

        self.pushButton_browseDir = QPushButton(self.centralwidget)
        self.pushButton_browseDir.setObjectName(u"pushButton_browseDir")
        self.pushButton_browseDir.setIcon(icon3)
        self.pushButton_browseDir.setIconSize(QSize(16, 16))

        self.horizontalLayout_5.addWidget(self.pushButton_browseDir)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.verticalSpacer_3 = QSpacerItem(20, 13, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButton_checkManifest = QPushButton(self.centralwidget)
        self.pushButton_checkManifest.setObjectName(u"pushButton_checkManifest")
        self.pushButton_checkManifest.setMinimumSize(QSize(60, 40))
        font1 = QFont()
        font1.setFamilies([u"Segoe UI"])
        font1.setPointSize(11)
        self.pushButton_checkManifest.setFont(font1)
        self.pushButton_checkManifest.setLocale(QLocale(QLocale.Italian, QLocale.Italy))
        icon4 = QIcon()
        icon4.addFile(u":/img/logo-check.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_checkManifest.setIcon(icon4)
        self.pushButton_checkManifest.setIconSize(QSize(20, 20))
        self.pushButton_checkManifest.setCheckable(False)
        self.pushButton_checkManifest.setFlat(False)

        self.horizontalLayout_2.addWidget(self.pushButton_checkManifest)

        self.horizontalSpacer_2 = QSpacerItem(30, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.groupBox_dlMode = QGroupBox(self.centralwidget)
        self.groupBox_dlMode.setObjectName(u"groupBox_dlMode")
        font2 = QFont()
        font2.setPointSize(10)
        self.groupBox_dlMode.setFont(font2)
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_dlMode)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.radioButton_seq = QRadioButton(self.groupBox_dlMode)
        self.radioButton_seq.setObjectName(u"radioButton_seq")

        self.verticalLayout_3.addWidget(self.radioButton_seq)

        self.radioButton_par = QRadioButton(self.groupBox_dlMode)
        self.radioButton_par.setObjectName(u"radioButton_par")

        self.verticalLayout_3.addWidget(self.radioButton_par)


        self.horizontalLayout_2.addWidget(self.groupBox_dlMode)

        self.horizontalSpacer_1 = QSpacerItem(30, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_1)

        self.pushButton_download = QPushButton(self.centralwidget)
        self.pushButton_download.setObjectName(u"pushButton_download")
        self.pushButton_download.setMinimumSize(QSize(60, 40))
        font3 = QFont()
        font3.setPointSize(11)
        self.pushButton_download.setFont(font3)
        self.pushButton_download.setLocale(QLocale(QLocale.Italian, QLocale.Italy))
        icon5 = QIcon()
        icon5.addFile(u":/img/logo-download.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_download.setIcon(icon5)
        self.pushButton_download.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.pushButton_download)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.label_resumeManifest = QLabel(self.centralwidget)
        self.label_resumeManifest.setObjectName(u"label_resumeManifest")
        self.label_resumeManifest.setFont(font)
        self.label_resumeManifest.setLocale(QLocale(QLocale.Italian, QLocale.Italy))

        self.verticalLayout.addWidget(self.label_resumeManifest)

        self.tableWidget = QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setLocale(QLocale(QLocale.Italian, QLocale.Italy))

        self.verticalLayout.addWidget(self.tableWidget)

        self.label_downloadInfo = QLabel(self.centralwidget)
        self.label_downloadInfo.setObjectName(u"label_downloadInfo")
        self.label_downloadInfo.setFont(font2)
        self.label_downloadInfo.setLocale(QLocale(QLocale.Italian, QLocale.Italy))

        self.verticalLayout.addWidget(self.label_downloadInfo)

        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setFont(font2)
        self.progressBar.setValue(0)

        self.verticalLayout.addWidget(self.progressBar)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        QWidget.setTabOrder(self.pushButton_lang, self.pushButton_help)
        QWidget.setTabOrder(self.pushButton_help, self.lineEdit_linkManifest)
        QWidget.setTabOrder(self.lineEdit_linkManifest, self.pushButton_browseFile)
        QWidget.setTabOrder(self.pushButton_browseFile, self.tableWidget)

        self.retranslateUi(MainWindow)

        self.pushButton_checkManifest.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
#if QT_CONFIG(tooltip)
        self.pushButton_lang.setToolTip(QCoreApplication.translate("MainWindow", u"Cambiare lingua.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_lang.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_help.setToolTip(QCoreApplication.translate("MainWindow", u"Aprire guida all'applicazione.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_help.setText("")
        self.label_linkManifest.setText(QCoreApplication.translate("MainWindow", u"Link dello manifest :", None))
#if QT_CONFIG(tooltip)
        self.pushButton_browseFile.setToolTip(QCoreApplication.translate("MainWindow", u"Navigare il disc e scegliere il file contenado i link dei manifest.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_browseFile.setText("")
        self.label_resultsDir.setText(QCoreApplication.translate("MainWindow", u"Cartello risultato :", None))
#if QT_CONFIG(tooltip)
        self.pushButton_browseDir.setToolTip(QCoreApplication.translate("MainWindow", u"Navigare il disc per scegliere il cartello in cui verrano scaricate le immagini.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_browseDir.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_checkManifest.setToolTip(QCoreApplication.translate("MainWindow", u"Controllare i manifest prima di scaricare.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_checkManifest.setText(QCoreApplication.translate("MainWindow", u"Controllo Manifest", None))
        self.groupBox_dlMode.setTitle(QCoreApplication.translate("MainWindow", u"Tipo scaricamento", None))
#if QT_CONFIG(tooltip)
        self.radioButton_seq.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>In questo modo, le immagini verrano scaricate in modo <span style=\" font-weight:700; text-decoration: underline;\">sequenziale</span> per ogni manifest, cio\u00e8 le immagini verrano scaricate l'una dopo l'altra.</p><p>Servirono meno risrorsi dello computer per\u00f2 sar\u00e0 meno veloce lo scaricamento.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.radioButton_seq.setText(QCoreApplication.translate("MainWindow", u"Sequenziale", None))
#if QT_CONFIG(tooltip)
        self.radioButton_par.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>In questo modo, le immagini verrano scaricate in modo <span style=\" font-weight:700; text-decoration: underline;\">parallelo</span> per ogni manifest, cio\u00e8 parecchie immagini verrano scaricate nello stesso tempo.</p><p>Servirono pi\u00f9 risorsi dello computer per\u00f2 sar\u00e0 pi\u00f9 veloce lo scaricamento.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.radioButton_par.setText(QCoreApplication.translate("MainWindow", u"Parallelo", None))
#if QT_CONFIG(tooltip)
        self.pushButton_download.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Avviare lo scaricamento usando il modo sequenziale oppure parallelo scelto.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_download.setText(QCoreApplication.translate("MainWindow", u"Scaricare", None))
        self.label_resumeManifest.setText("")
        self.label_downloadInfo.setText("")
        pass
    # retranslateUi

