import sys
import re
import requests
import os
import logging
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTextEdit, QProgressBar, QMessageBox, QFileDialog, QCheckBox, QSizePolicy, QSpacerItem
)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QIcon
import google_play_scraper

# Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
APP_ID = "jp.enish.gotopazu"
DOWNLOAD_URL_TEMPLATE = "https://www-cancer.enish-games.com/v{version}/resource/list/Android"
ASSET_URL_TEMPLATE = "https://assets.enish-games.com/assets-cancer/Resources/android/{file}"
CHUNK_SIZE = 8192
CONFIG_FILE = "config.txt"

class DownloadThread(QThread):
    log_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)
    download_complete_signal = pyqtSignal(str)

    def __init__(self, url, version, output_dir, file_list):
        super().__init__()
        self.url = url
        self.version = version
        self.output_dir = output_dir
        self.file_list = file_list

    def run(self):
        total_files = len(self.file_list)
        downloaded_files = 0 

        for i, file in enumerate(self.file_list):
            file_url = ASSET_URL_TEMPLATE.format(file=file)
            self.log_signal.emit(f"<b>Downloading {i+1}/{total_files}</b>: {file}")

            response = requests.get(file_url, stream=True)
            with open(os.path.join(self.output_dir, file), 'wb') as f:
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    if chunk:
                        f.write(chunk)

            downloaded_files += 1
            self.progress_signal.emit(int(downloaded_files / total_files * 100))

        log_message = f"<b><font color='red' size='+1'>All files are downloaded</font></b>"
        self.log_signal.emit(log_message)
        self.download_complete_signal.emit(self.output_dir)

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowIcon(QIcon('nino.ico'))
        self.output_dir = None
        self.load_config()

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        version_layout = QVBoxLayout()
        version_layout.addWidget(QLabel("Versions (comma-separated):"))

        self.versionLineEdit = QLineEdit()
        self.versionLineEdit.setAlignment(Qt.AlignCenter)
        version_layout.addWidget(self.versionLineEdit)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        self.downloadButton = QPushButton("Download")
        self.downloadButton.clicked.connect(self.on_download_button_clicked)
        button_layout.addWidget(self.downloadButton)

        self.latestVersionButton = QPushButton("Latest Version")
        self.latestVersionButton.clicked.connect(self.on_latest_version_button_clicked)
        button_layout.addWidget(self.latestVersionButton)

        self.browseButton = QPushButton("Browse")
        self.browseButton.clicked.connect(self.on_browse_button_clicked)
        button_layout.addWidget(self.browseButton)

        version_layout.addLayout(button_layout)

        self.setDefaultDirCheckbox = QCheckBox("Set as Default Directory")
        version_layout.addWidget(self.setDefaultDirCheckbox)

        # Output Directory Layout
        output_dir_layout = QHBoxLayout()
        self.outputDirLabel = QLabel("Output Directory: ")
        output_dir_layout.addWidget(self.outputDirLabel)
        self.outputDirPathLabel = QLabel("")
        self.outputDirPathLabel.setTextInteractionFlags(Qt.TextSelectableByMouse)
        output_dir_layout.addWidget(self.outputDirPathLabel)
        output_dir_layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))

        version_layout.addLayout(output_dir_layout)
        main_layout.addLayout(version_layout)

        # Progress layout
        progress_layout = QVBoxLayout()
        self.progressBar = QProgressBar()
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        progress_layout.addWidget(self.progressBar)

        # Log button layout
        log_button_layout = QHBoxLayout()
        log_button_layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.showLogButton = QPushButton("Show Log")
        self.showLogButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.showLogButton.setMaximumWidth(100)
        self.showLogButton.clicked.connect(self.toggle_log_visibility)
        log_button_layout.addWidget(self.showLogButton)
        log_button_layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))

        progress_layout.addLayout(log_button_layout)
        main_layout.addLayout(progress_layout)

        # Log layout
        self.logLayoutWidget = QWidget()
        self.logLayoutWidget.setVisible(False)
        log_layout = QVBoxLayout(self.logLayoutWidget)
        self.logLabel = QLabel("Log:")
        self.logTextEdit = QTextEdit()
        self.logTextEdit.setReadOnly(True)
        log_layout.addWidget(self.logLabel)
        log_layout.addWidget(self.logTextEdit)
        log_layout.setSpacing(5)
        main_layout.addWidget(self.logLayoutWidget)

        self.setLayout(main_layout)
        self.setWindowTitle("Gotoupazu Assets Grabber")
        self.setMinimumSize(800, 300)
        self.setGeometry(600, 600, 800, 300)

    def on_download_button_clicked(self):
        try:
            versions = self.versionLineEdit.text().split(",")
            versions = [version.strip().replace(".", "_") for version in versions if version.strip()]
            if not versions:
                QMessageBox.critical(self, "Error", "Please enter at least one version or click 'Latest Version' to fetch the latest version.")
                return
            if not self.output_dir:
                QMessageBox.critical(self, "Error", "Please select a directory")
                return

            self.total_files = 0
            self.file_lists = {}

            for version in versions:
                version_dir = os.path.join(self.output_dir, f"v{version}")
                if not os.path.exists(version_dir):
                    os.makedirs(version_dir)

                url = DOWNLOAD_URL_TEMPLATE.format(version=version)
                response = requests.get(url).text
                file_names = set(re.findall(r"[0-9a-f]{32}", response))

                existing_files = set()
                for subdir, _, files in os.walk(self.output_dir):
                    for file in files:
                        if file in file_names:
                            existing_files.add(file)

                file_list = list(file_names - existing_files)
                self.file_lists[version] = file_list
                self.total_files += len(file_list)

            self.logTextEdit.append(f"<b><font color='red' size='+1'>Number of files to download: {self.total_files}</font></b>")

            if self.total_files > 0:
                self.download_files(versions)
            else:
                self.logTextEdit.append("<b><font color='green' size='+1'>No new files to download.</font></b>")
        except Exception as e:
            logging.error(f"Error while processing download button click: {e}", exc_info=True)
            QMessageBox.critical(self, "Error", f"An error occurred during download: {e}")

    def on_latest_version_button_clicked(self):
        try:
            app_details = google_play_scraper.app(APP_ID)
            app_version = app_details['version']
            if app_version:
                self.versionLineEdit.setText(app_version)
            else:
                QMessageBox.critical(self, "Error", "Failed to get the latest version")
        except Exception as e:
            logging.error(f"Failed to get the latest version: {e}", exc_info=True)
            QMessageBox.critical(self, "Error", f"Failed to get the latest version: {e}")

    def on_browse_button_clicked(self):
        try:
            output_dir = QFileDialog.getExistingDirectory(self, "Select Output Directory")
            if output_dir:
                self.output_dir = output_dir
                self.outputDirPathLabel.setText(os.path.abspath(self.output_dir))
                if self.setDefaultDirCheckbox.isChecked():
                    self.save_config()
        except Exception as e:
            logging.error(f"Failed to browse for directory: {e}", exc_info=True)
            QMessageBox.critical(self, "Error", f"Failed to browse for directory: {e}")

    def save_config(self):
        try:
            with open(CONFIG_FILE, "w") as f:
                f.write(f"directory={self.output_dir}\n")
                f.write(f"log_visible={self.logLayoutWidget.isVisible()}\n")
        except Exception as e:
            logging.error(f"Failed to save config: {e}", exc_info=True)

    def load_config(self):
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, "r") as f:
                    config = f.readlines()
                    for line in config:
                        if line.startswith("directory="):
                            self.output_dir = line.strip().split("=")[1]
                            self.outputDirPathLabel.setText(os.path.abspath(self.output_dir))
                        if line.startswith("log_visible="):
                            log_visible = line.strip().split("=")[1] == 'True'
                            self.logLayoutWidget.setVisible(log_visible)
                            self.showLogButton.setText("Hide Log" if log_visible else "Show Log")
                            self.adjust_window_size(log_visible)
        except Exception as e:
            logging.error(f"Failed to load config: {e}", exc_info=True)

    def toggle_log_visibility(self):
        try:
            log_visible = not self.logLayoutWidget.isVisible()
            self.logLayoutWidget.setVisible(log_visible)
            self.showLogButton.setText("Hide Log" if log_visible else "Show Log")
            self.adjust_window_size(log_visible)
            self.save_config()
        except Exception as e:
            logging.error(f"Failed to toggle log visibility: {e}", exc_info=True)
            QMessageBox.critical(self, "Error", f"Failed to toggle log visibility: {e}")

    def adjust_window_size(self, show_log):
        if show_log:
            self.resize(800, 600)
        else:
            self.resize(800, 300)
        self.layout().activate()

    def download_files(self, versions):
        self.progressBar.setValue(0)
        self.download_thread = DownloadThreadManager(versions, self.file_lists, self.output_dir, self.total_files)
        self.download_thread.log_signal.connect(self.update_log)
        self.download_thread.progress_signal.connect(self.update_progress)
        self.download_thread.download_complete_signal.connect(self.open_folder)
        self.download_thread.start()

    def update_log(self, log_message):
        self.logTextEdit.append(log_message)

    def update_progress(self, progress):
        self.progressBar.setValue(progress)

    def open_folder(self, folder_path):
        QMessageBox.information(self, "Download Complete", f"Files have been downloaded to: {folder_path}")
        os.startfile(folder_path)

class DownloadThreadManager(QThread):
    log_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)
    download_complete_signal = pyqtSignal(str)

    def __init__(self, versions, file_lists, output_dir, total_files):
        super().__init__()
        self.versions = versions
        self.file_lists = file_lists
        self.output_dir = output_dir
        self.total_files = total_files
        self.downloaded_files = 0

    def run(self):
        for version in self.versions:
            version_dir = os.path.join(self.output_dir, f"v{version}")
            if not os.path.exists(version_dir):
                os.makedirs(version_dir)
            url = DOWNLOAD_URL_TEMPLATE.format(version=version)
            file_list = self.file_lists[version]
            download_thread = DownloadThread(url, version, version_dir, file_list)
            download_thread.log_signal.connect(self.log_signal)
            download_thread.progress_signal.connect(self.progress_signal)
            download_thread.download_complete_signal.connect(self.on_download_complete)
            download_thread.run()

    def on_download_complete(self, output_dir):
        self.downloaded_files += 1
        if self.downloaded_files == len(self.versions):
            self.download_complete_signal.emit(output_dir)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
