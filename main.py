# Import libraries
from src.gui.AntenatiDownloader_App import *
import sys
from PySide6 import QtWidgets

# Import resources
import res.resources


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = AntenatiDownloader_App()
    # ui.setupUi(MainWindow)
    ui.launch(MainWindow)


    MainWindow.show()
    # ui.get_manifest_file()
    sys.exit(app.exec())
