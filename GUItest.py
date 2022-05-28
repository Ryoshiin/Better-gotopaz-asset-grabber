import wx


class Example(wx.Frame):
    def __init__(self, parent, title):
        super(Example, self).__init__(parent, title=title)
        self.InitUI()
        self.Centre()
    def InitUI(self):
        panel = wx.Panel(self)
        sizer = wx.GridBagSizer(4, 4)
        text = wx.StaticText(panel, label="Version: ")
        sizer.Add(text, pos=(0, 0), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)
        tc = wx.TextCtrl(panel)
        sizer.Add(tc, pos=(1, 0), span=(1, 5),
            flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=5)
        buttonOk = wx.Button(panel, label="Ok", size=(90, 28))
        buttonClose = wx.Button(panel, label="Close", size=(90, 28))
        buttonClose.Bind(wx.EVT_BUTTON, self.on_close)
        sizer.Add(buttonOk, pos=(3, 3))
        sizer.Add(buttonClose, pos=(3, 4), flag=wx.RIGHT|wx.BOTTOM, border=10)
        sizer.AddGrowableCol(1)
        sizer.AddGrowableRow(2)
        panel.SetSizer(sizer)
    def on_close(self, event):
        self.Close()
def main():
    app = wx.App()
    ex = Example(None, title='Rename')
    ex.Show()
    app.MainLoop()
if __name__ == '__main__':
    main()