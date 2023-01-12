import re, requests, os, time, random, logging
from PyQt5 import QtWidgets, QtGui

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s')

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create a QLineEdit widget to enter the version number
        self.versionEdit = QtWidgets.QLineEdit(self)
        self.versionEdit.move(20, 20)
        self.versionEdit.resize(200, 32)

        # Create a QPushButton to start the download
        self.downloadButton = QtWidgets.QPushButton('Start Download', self)
        self.downloadButton.move(20, 60)
        self.downloadButton.resize(200, 32)
        self.downloadButton.clicked.connect(self.startDownload)
    
        # Set window properties
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Unity2D Downloader')
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.show()

    def startDownload(self):
        try:
            outputDir = "unity2d_test"
            version = self.versionEdit.text()
            version = version.replace('.', '_')
            logging.info(f"Version: {version}")
            if not version:
                logging.info('No version specified, exiting...')
                return
            url = f"https://www-cancer.enish-games.com/v{version}/resource/list/Android"
            logging.info(f"Download url: {url}")
            response = requests.get(url)
            if "メンテナンス中" in response.text:
                raise Exception("Server is in maintenance")
            if not os.path.exists(outputDir):
                os.mkdir(outputDir)
        except Exception as e:
            #I need to add this line after everything works
            #QtWidgets.QMessageBox.warning(self, 'Error', f'An error occurred while downloading: {e}')
            fileNames = set(re.findall(r"[0-9a-f]{32}", response))
            # find all file names in the response
            finddir = set(os.listdir("unity2d_test"))
            # find all file names in the output directory
            filelist = list(fileNames-finddir)
            # find the difference between the two sets
            for file in filelist:
                if file in outputDir:
                    logging.info(f"{file} already exists")
                    continue
                # if file already exists, skip
                else:
                    url = f"https://assets.enish-games.com/assets-cancer/Resources/android/{file}"
                    logging.info(f"Downloading {file}")
                    os.system(
                        " ".join([
                            'wget',
                            '--random-wait',
                            '--no-check-certificate',
                            '-q',
                            '-nv',
                            '-c',
                            '-N',
                            f'--user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53"',
                            url,
                            '-P',
                            outputDir
                        ])
                    )
                    time.sleep(random.uniform(0.1, 1))
                    logging.info(f"{file} downloaded")
                    # download file and log it
                    if not file in filelist:
                        logging.info("All files are downloaded")
                        exit()
                        # all files are downloaded, exit
            
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    app.exec_()

#Planning to add : Logs in the gui =
            #label = QtWidgets.QLabel(self)
            #label.setText(response.text)
            #label.setGeometry(-30 , 100 , 300 , 50)
            #label.show()

             # cant believe all this actually works
             #yeah but you cant make a gui yourself hahahaha L + Ratio + kys
# hey, if you're reading this, i hope you know what you're doing, because i don't, so don't complain
#I dont know what im doing either help oml
