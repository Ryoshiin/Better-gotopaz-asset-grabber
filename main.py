# this is not overcommented at all
import re,requests,os,time,random,logging,wx

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s')

outputDir = "unity2d_all"
version = str
class Example(wx.Frame):
    def __init__(self, parent, title):
        super(Example, self).__init__(parent, title=title, size=(2125, 1032))
        self.InitUI()
        self.Centre()
    def InitUI(self):
        panel = wx.Panel(self)
        sizer = wx.GridBagSizer(4, 4)
        text = wx.StaticText(panel, label="Version (Find it at https://play.google.com/store/apps/details?id=jp.enish.gotopazu, then open the 'About this game' option, https://files.catbox.moe/et7cek.png and https://files.catbox.moe/k3iwsp.png for reference): ")
        sizer.Add(text, pos=(0, 0), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)
        tc = wx.TextCtrl(panel)
        sizer.Add(tc, pos=(1, 0), span=(1, 5),
            flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=5)
        buttonOk = wx.Button(panel, label="Ok", size=(90, 28))
        buttonOk.Bind(wx.EVT_BUTTON, self.onOk)
        buttonClose = wx.Button(panel, label="Close", size=(90, 28))
        buttonClose.Bind(wx.EVT_BUTTON, self.on_close)
        sizer.Add(buttonOk, pos=(3, 3))
        sizer.Add(buttonClose, pos=(3, 4), flag=wx.RIGHT|wx.BOTTOM, border=10)
        sizer.AddGrowableCol(1)
        sizer.AddGrowableRow(2)
        panel.SetSizer(sizer)
    def on_close(self, event):
        self.Close()
# i hate this code, i hate it so much, why does it not work?
# why does the tc.GetValue() not work?
# how the fuck do i do this?
# it makes no sense at all 
# # at this point it might honestly be easier to figure out how to get the version automatically (5:07pm, 2022-05-28)
    def onOk(self, event):
        global version
        version = self.tc.getValue().replace(".","_")
        #version = version.replace('.', '_')
        logging.info(f"Version: {version}")
        if not version:
            logging.info('No version specified, exiting...')
            exit()
            # no version specified, exit
        url = f"https://www-cancer.enish-games.com/v{version}/resource/list/Android"
        logging.info(f"Download url: {url}")
        response = requests.get(url).text
        if "メンテナンス中" in response:
            raise Exception("Server is in maintenance")
            # server is in maintenance, exit
        if not os.path.exists(outputDir):
            os.mkdir(outputDir)
            # create output directory if it doesn't exist
        fileNames = set(re.findall(r"[0-9a-f]{32}", response))
        # find all file names in the response
        finddir = set(os.listdir("unity2d_all"))
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
def main():
    app = wx.App()
    ex = Example(None, title='test')
    ex.Show()
    app.MainLoop()
if __name__ == '__main__':
    main()
# cant believe all this actually works
# hey, if you're reading this, i hope you know what you're doing, because i don't, so don't complain