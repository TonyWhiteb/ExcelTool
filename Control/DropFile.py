import wx
import os,sys
from BasicClass import FileCtrl
from BasicClass import PanelCtrl

class DropFile(FileCtrl.FileCtrl):
    def __init__(self,*args,**kwargs):
        super(DropFile,self).__init__(*args,**kwargs)

        self.Bind(wx.EVT_LEFT_DOWN, self.OnFindCurrentRow )
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)

    def GetInfo(self):
        ##test
        # pathlist = self.filedropctrl.GetEntryList()
        # a = pathlist[0][1]
        ##
        pathlist = self.GetEntries()
        def_dict = defaultdict(list)

        self.big_dict = {}
        for k,r in pathlist:
            self.filename = []
            self.filename.append(k)
            afile_list = []
            sp = {}
            os.chdir(r)
            afile = open(k,"r").readlines()
            afile_list = afile[0].split('\t')
            sp = sp.fromkeys(afile_list)
            m = 1
            n = 0
            while m < len(afile):
                value = []
                value = afile[m].split('\t')
                for n in range(len(afile_list)):
                    if sp[afile_list[n]] ==None:
                        sp[afile_list[n]] = []
                    sp[afile_list[n]].append(value[n])
                m = m + 1
            self.big_dict[k] = sp
        return self.big_dict

class DropFilePanel(PanelCtrl.PanelTemp):
    def __init__(self,*args,**kwargs):
        super(DropFile,self).__init__(*args,**kwargs)

        dfPnl_vertSzr = wx.BoxSizer(wx.VERTICAL)
        dfPnl_vertSzr.Add(fdcLabel, proportion = 0, flag = wx.EXPAND)
        dfPnl_vertSzr.Add(self.filesListCtrl, proportion = 1, flag = wx.EXPAND)
        dfPnl_horzSzr = wx.BoxSizer(wx.HORIZONTAL)
        dfPnl_horzSzr.Add(dfPnl_vertSzr, proportion =1, flag = wx.EXPAND)

        self.SetSizer(dfPnl_horzSzr)
    
    def SetCallbackFunc(self, dropCallbackFunc = None):

        self.DropFileTarget = self.filesListCtrl

        # self.DropFileTarget.SetDropTarget