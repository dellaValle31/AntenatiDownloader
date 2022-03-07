import os, re, functools
import user_agent as ua
import src.core.AntenatiDownloader_Core as core

from PySide6.QtCore import QTimer, QThread
from PySide6.QtWidgets import QFileDialog, QMessageBox,QTableWidgetItem, QAbstractScrollArea
from src.gui.AntenatiDownloader_BaseApp import  *



class AntenatiDownloader_App(Ui_MainWindow):
    def __init__(self):
        # Init base class
        super(Ui_MainWindow, self).__init__()

        # Init class
        # Variable for GUI
        self.link_manifest = None    # link manifest
        self.isManifestFile = False  # boolean for 'is manifest a file ?'
        self.results_dir = '.'       # Base results path
        self.parallelism = True      # Enable parallelism
        self.urlPattern = r"((([A-Za-z]{3,9}:(?:\/\/)?)(?:[-;:&=\+\$,\w]+@)?[A-Za-z0-9.-]+|(?:www.|[-;:&=\+\$,\w]+@)[A-Za-z0-9.-]+)((?:\/[\+~%\/.\w\-_]*)?\??(?:[-\+=&;%@.\w_]*)#?(?:[\w]*))?)" # Regex pattern to validate URL link manifest
        self.useful_names = []
        self.all_widgets = []       # Will contains all widgets in GUI


        # Variable for core
        self.headers = {'User-Agent' : ua.generate_user_agent()} # Generate valid, random user-agent
        self.manifests = None       # List of all manifest links
        self.imageMaps = None       # List of all imageMaps
        self.folders = None         # List of all folders
        self.iiif_manifest = None   # List of all manifests as json data

        self.timer_progress = QTimer()       # Timer for updating progressbar
        self.timer_wheaders = QTimer()       # Timer for randomly updating user-agent to avoid server-side restriction

        # Variables for enabling threading and downloading logic
        self.current_folder = None   # Current folder in download
        self.current_imageMap = None # Current imageMap in download
        self.current_idx = 0         # Current idx in download
        self.current_thread = None   # Current thread in download
        self.current_worker = None   # Current worker in download
        self.manifest_thread = None  # Thread to download manifest
        self.manifest_worker = None  # Worker to download manifest

        self.threads = []           # List of all thread ever created
        self.workers = []           # List of all workers ever created


    def launch(self, wnd):
        """Function for creating and launching GUI"""
        # Create GUI
        super().setupUi(wnd)
        # Finish init GUI following core logic rules
        self.init_gui_core_logic()

        # Connection logic
        self.pushButton_browseFile.clicked.connect(self.get_manifest_file)
        self.pushButton_browseDir.clicked.connect(self.get_results_dir)
        self.pushButton_download.clicked.connect(self.core_process_download)
        self.pushButton_checkManifest.clicked.connect(self.core_process_prerequisits)
        self.lineEdit_linkManifest.textChanged.connect(self.check_link_manifest)
        self.lineEdit_resultsDir.textChanged.connect(self.check_results_folder)
        self.timer_progress.timeout.connect(self.core_count_files)
        self.timer_wheaders.timeout.connect(self.core_change_headers)


    def init_gui_core_logic(self):
        """Initialize the GUI core logic"""
        self.all_widgets = [self.lineEdit_resultsDir, self.lineEdit_resultsDir,
                            self.pushButton_browseFile, self.pushButton_browseDir,
                            self.pushButton_checkManifest, self.pushButton_download]

        self.lineEdit_resultsDir.setText(self.results_dir)
        self.radioButton_par.setChecked(True)
        self.define_dynamic_ui(core.GUI_TYPE.INIT)
        self.define_dynamic_ui(core.GUI_TYPE.DIR_RESULT_OK)


    def get_manifest_file(self):
        """Get manifest file from user input"""
        fileName = QFileDialog.getOpenFileName(self.pushButton_browseFile, "Aprire Manifest file", "./", "Manifest files (*.txt);;All files (*.*)")
        self.lineEdit_linkManifest.setText(fileName[0])
        self.define_dynamic_ui(core.GUI_TYPE.MANIFEST_OK)


    def get_results_dir(self):
        """Get results directory from user input"""
        resDir = QFileDialog.getExistingDirectory(self.pushButton_browseDir, "Scegliere cartello di risultati", "./")
        self.lineEdit_resultsDir.setText(resDir)

    def check_link_manifest(self):
        """Checks manifests link and informs user"""
        self.link_manifest = self.lineEdit_linkManifest.text()
        # Check if file or url
        if os.path.isfile(self.link_manifest):
            self.isManifestFile = True
            self.define_dynamic_ui(core.GUI_TYPE.MANIFEST_OK)
        elif re.match(self.urlPattern, self.link_manifest):
            self.isManifestFile = False
            self.define_dynamic_ui(core.GUI_TYPE.MANIFEST_OK)
        else:
            self.define_dynamic_ui(core.GUI_TYPE.MANIFEST_KO)


    def check_results_folder(self):
        """Checks results folder and informs user"""
        self.results_dir = os.path.abspath(self.lineEdit_resultsDir.text())
        # Check if directory exists
        if os.path.isdir(self.results_dir):
            self.define_dynamic_ui(core.GUI_TYPE.DIR_RESULT_OK)
        else:
            self.define_dynamic_ui(core.GUI_TYPE.DIR_RESULT_KO)


    def define_dynamic_ui(self, gui_type):
        """Handle GUI logic following user input"""
        if gui_type == core.GUI_TYPE.INIT:
            self.groupBox_dlMode.setEnabled(False)
            self.pushButton_download.setEnabled(False)
            self.pushButton_checkManifest.setEnabled(False)
            self.lineEdit_linkManifest.setStyleSheet("border: 1px solid red")
            self.lineEdit_resultsDir.setStyleSheet("border: 1px solid red")
            self.update_progressbar(0)

        elif gui_type == core.GUI_TYPE.MANIFEST_OK:
            self.pushButton_checkManifest.setEnabled(True)
            self.lineEdit_linkManifest.setStyleSheet("border: 1px solid black")

        elif gui_type == core.GUI_TYPE.MANIFEST_KO:
            self.pushButton_checkManifest.setEnabled(False)
            self.lineEdit_linkManifest.setStyleSheet("border: 1px solid red")

        elif gui_type == core.GUI_TYPE.DIR_RESULT_OK:
            self.lineEdit_resultsDir.setStyleSheet("border: 1px solid black")

        elif gui_type == core.GUI_TYPE.DIR_RESULT_KO:
            self.lineEdit_resultsDir.setStyleSheet("border: 1px solid red")

        elif gui_type == core.GUI_TYPE.MANIFEST_DIR_OK:
            self.pushButton_checkManifest.setEnabled(True)
            self.groupBox_dlMode.setEnabled(True)
            self.pushButton_download.setEnabled(True)
            self.lineEdit_linkManifest.setStyleSheet("border: 1px solid black")
            self.lineEdit_resultsDir.setStyleSheet("border: 1px solid black")

        elif gui_type == core.GUI_TYPE.FREEZE_ALL:
            for w in self.all_widgets:
                w.setEnabled(False)

        elif gui_type == core.GUI_TYPE.UNFREEZE_ALL:
            for w in self.all_widgets:
                w.setEnabled(True)

    def get_download_mode(self):
        if self.radioButton_par.isChecked():
            return core.DL_TYPE.PARALLEL
        elif self.radioButton_seq.isChecked():
            return core.DL_TYPE.SEQUENTIAL
        else: # impossible
            return core.DL_TYPE.PARALLEL

    def update_progressbar(self, percent):
        """Updates progressbar"""
        self.progressBar.setValue(percent * 100)

    def check_manifest_download(self, status_code_ok):
        if sum(status_code_ok) != len(self.manifests):
            idx_err =  [i for i, x in enumerate(status_code_ok) if not x]
            msgbox = QMessageBox()
            msgbox.setText("{} manifest su {} trovati invalidi".format(len(idx_err), len(self.manifests)))
            msgbox.setInformativeText("I link seguenti sono sbagliati e le immagini associate non verrano scaricate.\nContinuare le scaricamento ?")
            msgbox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msgbox.setIcon(QMessageBox.Warning)
            msgbox.setWindowTitle("AntenatiDownloader - Errore")

            # Prepare detailed Text
            detailledtext = ""
            for idx in idx_err:
                detailledtext += "[linea " + str(idx + 1) + "] : " + self.manifests[idx] + "\n"
            msgbox.setDetailedText(detailledtext)

            # Resize box
            msgbox.setFixedWidth(200)

            msgbox.exec()

    def check_manifest_urlPattern(self, idx_err):
        if len(idx_err) != 0:
            msgbox = QMessageBox()
            msgbox.setText("{} manifest su {} trovati invalidi".format(len(idx_err), len(self.manifests)))
            msgbox.setInformativeText(
                "I link seguenti sono sbagliati e le immagini associate non verrano scaricate.\nContinuare le scaricamento ?")
            msgbox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msgbox.setIcon(QMessageBox.Warning)
            msgbox.setWindowTitle("AntenatiDownloader - Errore")

            # Prepare detailed Text
            detailledtext = ""
            for idx in idx_err:
                detailledtext += "[linea " + str(idx + 1) + "] : " + self.manifests[idx] + "\n"
            msgbox.setDetailedText(detailledtext)

            # Resize box
            msgbox.setFixedWidth(200)

            msgbox.exec()


    # There go core logic in GUI
    def core_process_prerequisits(self):
        """Main function for displaying user information and preparing download"""
        # Reset progressbar
        self.update_progressbar(0)
        # Launch manifest download
        self.core_control_manifest()



    def core_control_manifest(self):
        """Control manifest link after downloading them"""
        # Get all the manifests links
        self.manifests = core.get_manifest_links(self.link_manifest)

        # Check URL pattern
        idx_err = []
        for i, m in enumerate(self.manifests):
            if not re.match(self.urlPattern, m):
                idx_err.append(i)
        self.check_manifest_urlPattern(idx_err)


        # Download manifest in another thread
        self.define_dynamic_ui(core.GUI_TYPE.FREEZE_ALL)
        self.label_downloadInfo.setText("Scaricamento degli manifest...")
        self.core_launch_download_manifest_thread()



    def core_get_manifest_info(self):
        # Get information
        self.imageMaps = core.get_all_canvases(self.iiif_manifest)
        self.folders = core.build_folders_name(self.results_dir, self.iiif_manifest)

        # Build name for user
        self.useful_names = [path.removeprefix(os.path.abspath(self.results_dir) + os.sep).replace(os.sep, ' - ') for path in self.folders]

        # Display to user
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(['Cartello \n risultato',
                                                    'Numero\n immagini',
                                                    'Statuto \ndownload',
                                                    'Aprire \ncartello'])

        self.tableWidget.setRowCount(len(self.folders))

        # Compute number of pages for displaying
        nb_pages = [len(x) for x in self.imageMaps]

        # Populate item
        for (i, (path, nbImg)) in enumerate(zip(self.folders, nb_pages)):
            # Create directiry item
            item_resdir = QTableWidgetItem(path)
            item_resdir.setTextAlignment(Qt.AlignLeft)

            # Create number of pages item
            item_nbpage = QTableWidgetItem(str(nbImg))
            item_nbpage.setTextAlignment(Qt.AlignCenter)

            # Create status item
            item_status = QTableWidgetItem("PRONTO")
            item_status.setTextAlignment(Qt.AlignCenter)
            item_status.setForeground(QColor('blue'))

            # Create folder item
            iconItem = QIcon()
            iconItem.addFile(u":/img/logo-browse.png", QSize(), QIcon.Normal, QIcon.Off)
            item_openFolder = QPushButton()
            item_openFolder.setIcon(iconItem)
            item_openFolder.setIconSize(QSize(20,20))
            item_openFolder.clicked.connect(functools.partial(core.open_result_folder, folder=path))
            item_openFolder.setEnabled(False)

            self.tableWidget.setItem(i, 0, item_resdir)
            self.tableWidget.setItem(i, 1, item_nbpage)
            self.tableWidget.setItem(i, 2, item_status)
            self.tableWidget.setCellWidget(i, 3, item_openFolder)

        # Set the predefined columns width
        self.tableWidget.setColumnWidth(1, 100) # Cell "numero immagini"
        self.tableWidget.setColumnWidth(2, 150) # Cell "statuto"
        self.tableWidget.setColumnWidth(3, 50)  # Cell "aprire cartello"
        # Tell the first columns to auto-resize
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

        self.label_resumeManifest.setText(self.label_resumeManifest.text() + ", per un totale di {} immagini".format(sum(nb_pages)))

    def core_process_download(self):
        # Freeze GUI
        self.define_dynamic_ui(core.GUI_TYPE.FREEZE_ALL)

        # Reset progressbar
        self.update_progressbar(0)

        # Preparing first iteration
        self.current_idx = 0
        self.core_next_manifest_download(isInit=True)

        # Launch timers
        self.timer_progress.setInterval(250) # Each 250ms will the download status be reported
        self.timer_progress.start()

        self.timer_wheaders.setInterval(1000 * 60) # Each minute will change the header passed to request.get
        self.timer_wheaders.start()


    def core_next_manifest_download(self, isInit = False):
        if not isInit:
            if self.current_idx < len(self.imageMaps) - 1:
                self.current_idx = self.current_idx + 1
            else:
                # Download is finished. Clean objects and return
                self.core_end_all_images_downloads()
                return

        # Prepare next download
        self.current_imageMap = self.imageMaps[self.current_idx]
        self.current_folder = self.folders[self.current_idx]

        # Create directory if necessary
        core.safe_create_folder(self.current_folder)

        # If previous download, delete files
        core.rm_file_in_folder(self.current_folder)

        # Update TableView
        self.tableWidget.item(self.current_idx, 2).setText("SCARICAMENTO")
        self.tableWidget.item(self.current_idx, 2).setForeground(QColor('orange'))

        # Update label downloadInfo
        self.label_downloadInfo.setText("Scaricando {} : ".format(self.useful_names[self.current_idx]))

        # Launch threading
        self.core_launch_download_images_thread()

    def core_launch_download_images_thread(self):
        # Initalize Thread and Worker
        self.current_thread = QThread()
        self.current_worker = core.Worker_DL_Img(self.current_imageMap, self.current_folder, self.parallelism, self.headers)

        # Prepare thread
        self.current_worker.moveToThread(self.current_thread)
        self.current_thread.started.connect(self.current_worker.run)
        # self.current_thread.finished.connect(self.current_thread.deleteLater)
        self.current_worker.finished.connect(self.current_thread.quit)
        # self.current_worker.finished.connect(self.current_worker.deleteLater)
        self.current_worker.results.connect(self.core_end_images_download)
        self.current_worker.finished.connect(self.core_next_manifest_download)

        # Launch thread
        self.current_thread.start()

        # Remember thread and worker to avoid app crash (Thread / Worker may be deleted after the next ones are created)
        self.threads.append(self.current_thread)
        self.workers.append(self.current_worker)


    def core_launch_download_manifest_thread(self):
        # Initalize Thread and Worker
        self.manifest_thread = QThread()
        self.manifest_worker = core.Worker_DL_Manifest(self.manifests, headers=self.headers)

        # Prepare thread
        self.manifest_worker.moveToThread(self.manifest_thread)
        self.manifest_thread.started.connect(self.manifest_worker.run)
        self.manifest_thread.finished.connect(self.manifest_thread.deleteLater)
        self.manifest_worker.finished.connect(self.manifest_thread.quit)
        self.manifest_worker.finished.connect(self.manifest_worker.deleteLater)

        # self.manifest_worker.finished.connect(self.core_end_manifest_download)
        self.manifest_worker.manifest_data.connect(self.core_end_manifest_download)
        self.manifest_worker.count.connect(self.update_progressbar)

        # Launch thread
        self.manifest_thread.start()

        # Remember thread and worker to avoid app crash (Thread / Worker may be deleted after the next ones are created)
        self.threads.append(self.manifest_thread)
        self.workers.append(self.manifest_worker)



    def core_end_manifest_download(self, data):
        """Function to execute after all the manifest link have been downloaded"""
        self.iiif_manifest = data[0]
        status_code_ok = data[1]

        self.label_resumeManifest.setText(
            "Trovat{} {} manifest validi".format("o" if len(self.manifests) == 1 else "i", sum(status_code_ok)))

        self.check_manifest_download(status_code_ok)
        self.define_dynamic_ui(core.GUI_TYPE.MANIFEST_DIR_OK)

        # Inform user
        self.update_progressbar(1)
        self.label_downloadInfo.setText("Tutti manifest scaricati - pronto da scaricare le immagini.")
        self.define_dynamic_ui(core.GUI_TYPE.UNFREEZE_ALL)

        # Go to next step
        self.core_get_manifest_info()


    def core_end_images_download(self, dl_results):
        """Function to execute after all images of current manifest have been downloaded"""
        # Update TableView
        if all(dl_results):
            self.tableWidget.item(self.current_idx, 2).setText("SCARICATO")
            self.tableWidget.item(self.current_idx, 2).setForeground(QColor('green'))
        else:
            self.tableWidget.item(self.current_idx, 2).setText("FALLIMENTO")
            self.tableWidget.item(self.current_idx, 2).setForeground(QColor('red'))

        self.tableWidget.cellWidget(self.current_idx, 3).setEnabled(True)


    def core_end_all_images_downloads(self):
        """Function to execute after all images of all manifest have been downloaded"""
        # Inform user
        self.update_progressbar(1)
        self.label_downloadInfo.setText("Scaricato tutto")
        self.define_dynamic_ui(core.GUI_TYPE.UNFREEZE_ALL)

        # Stop timers
        self.timer_progress.stop()
        self.timer_wheaders.stop()

    def core_count_files(self):
        """Function to be executed by timer in order to get download status"""
        self.update_progressbar(core.get_download_status(self.current_folder) / len(self.current_imageMap))

    def core_change_headers(self):
        self.headers = {'User-Agent' : ua.generate_user_agent()}

    # Override destrutor
    def __del__(self):
        # Safely destruct objects before leaving the app
        self.threads.clear()
        self.workers.clear()
