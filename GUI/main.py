import sys, re, requests, os, time, random, traceback, google_play_scraper, logging
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QProgressBar, QMessageBox, QFileDialog
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QIcon

# Subclass for downloading files in a separate thread
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
        total_files = len(self.file_list) # Get the total number  of files to download
        downloaded_files = 0 

        for i, file in enumerate(self.file_list):
            file_url = f"https://assets.enish-games.com/assets-cancer/Resources/android/{file}"
            self.log_signal.emit(f"<b>Downloading {i+1}/{total_files}</b>: {file}")

            response = requests.get(file_url, stream=True)
            with open(os.path.join(self.output_dir, file), 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)



            downloaded_files += 1
            self.progress_signal.emit(int(downloaded_files / total_files * 100))

        log_message = f"<b><font color='red' size='+1'>All files are downloaded</font></b>"
        self.log_signal.emit(log_message)
        self.download_complete_signal.emit(self.output_dir)

class MyApp(QWidget):
# Class for the gui window
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowIcon(QIcon('nino.ico'))

    def initUI(self):
        layout = QVBoxLayout()

        self.versionLabel = QLabel("Version:")
        layout.addWidget(self.versionLabel)
        

        self.versionLineEdit = QLineEdit()
        self.versionLineEdit.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.versionLineEdit)
        
        self.downloadButton = QPushButton("Download")
        self.downloadButton.clicked.connect(self.on_download_button_clicked)
        layout.addWidget(self.downloadButton)

        self.latestVersionButton = QPushButton("Latest Version")
        self.latestVersionButton.clicked.connect(self.on_latest_version_button_clicked)
        layout.addWidget(self.latestVersionButton)

        self.browseButton = QPushButton("Browse")
        self.browseButton.clicked.connect(self.on_browse_button_clicked)
        layout.addWidget(self.browseButton)

        self.outputDirLabel = QLabel("Output Directory:")
        layout.addWidget(self.outputDirLabel)

        self.progressBar = QProgressBar()
        layout.addWidget(self.progressBar)

        self.logLabel = QLabel("Log:")
        layout.addWidget(self.logLabel)

        self.logTextEdit = QTextEdit()
        layout.addWidget(self.logTextEdit)
        self.setLayout(layout)
        self.setLayout(layout)
        self.setWindowTitle("Gotoupazu Assets Grabber")
        self.setGeometry(600, 600, 800, 600)

    def on_download_button_clicked(self):
        try:
            version = self.versionLineEdit.text().replace(".", "_")
            if not version:
                QMessageBox.critical(self, "Error", "Please enter a version or click 'Latest Version' to fetch the latest version.")
                return
            if not hasattr(self, 'output_dir') or not self.output_dir:
                QMessageBox.critical(self, "Error", "Please select a directory")
                return
            output_dir = os.path.join(self.output_dir, f"v{version}")
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            self.outputDirLabel.setText(f"Output Directory: {os.path.abspath(output_dir)}")
            

            url = f"https://www-cancer.enish-games.com/v{version}/resource/list/Android"
            response = requests.get(url).text # Send HTTP GET request to the url and stores it in a response var.
            file_names = set(re.findall(r"[0-9a-f]{32}", response)) # Find all 32 character names in the response and make unique file names out of them.

            existing_files = set()
            for subdir, dirs, files in os.walk(self.output_dir):
                for file in files:
                    if file in file_names:
                        existing_files.add(file)

            file_list = list(file_names - existing_files) # Find the files that are not already downloaded

            # Display the number of files that will be downloaded
            self.logTextEdit.append(f"<b><font color='red' size='+1'>Number of files to download: {len(file_list)}</font></b>")



            self.download_files(url, version, output_dir, file_list)
        except Exception as e:
            logging.error(f"Error while processing download button click: {e}", exc_info=True)
            QMessageBox.critical(self, "Error", f"An error occurred during download: {e}")


    def on_latest_version_button_clicked(self):
        try:
            app_id = "jp.enish.gotopazu"
            app_details = google_play_scraper.app(app_id)
            app_version = app_details['version']
            if app_version:
                self.versionLineEdit.setText(app_version)
            else:
                QMessageBox.critical(self, "Error", f"Failed to get the latest version")
        except Exception as e:
            error_message = f"Failed to get the latest version: {e}\n{traceback.format_exc()}"
            QMessageBox.critical(self, "Error", f"Failed to get the latest version: {e}")

    def on_browse_button_clicked(self):
        output_dir = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if output_dir:
            self.output_dir = output_dir
            self.outputDirLabel.setText(f"Output Directory: {os.path.abspath(self.output_dir)}")


    def download_files(self, url, version, output_dir, file_list):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Parameters for download thread
        self.download_thread = DownloadThread(url, version, output_dir, file_list)

        # Connect to log
        self.download_thread.log_signal.connect(self.update_log)

        # Connect  to progress bar
        self.download_thread.progress_signal.connect(self.update_progress)

        # Connect to open folder once download is complete
        self.download_thread.download_complete_signal.connect(self.open_folder)

        self.download_thread.start()

    def update_log(self, log_message):
        self.logTextEdit.append(log_message)

    def update_progress(self, progress):
        self.progressBar.setValue(progress)

    def open_folder(self, folder_path):
        os.startfile(folder_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())