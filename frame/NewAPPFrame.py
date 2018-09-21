import sys,os
import wx

from BasicClass import DropTarget as DT
from BasicClass import FileCtrl as FC


from collections import defaultdict


class AppFrame(wx.Frame):

    def __init__(self,args,argc,title = 'Demo',file_path = None):

        self.file_path = file_path

        super(AppFrame,self).__init__(parent = None, id =-1, title = title, size = (600,400))

        self.filesAndLinks = list()


        self.SetBackgroundColour(wx.WHITE)
        panel = wx.Panel(self)
        box_h = wx.BoxSizer(wx.HORIZONTAL)
        box_v = wx.BoxSizer(wx.VERTICAL)

        wx.StaticText(self, -1,"Any files and links",(10,1))
        self.filedropctrl = FC.FileCtrl(panel,size = (550,300),style = wx.LC_REPORT|wx.BORDER_SUNKEN)
        self.filedropctrl.InsertColumn(0,'File or Link Name')
        self.filedropctrl.InsertColumn(1,'Parent Path')
        self.filesDropTarget = self.filedropctrl

        
        self.filedropctrl.SetDropTarget(DT.DropTarget(self.filedropctrl))
        self.filedropctrl.dropFunc = self.OnFilesDropped
        # print(type(self.filedropctrl))
        # print(type(self.filesDropTarget))
        
        helpTextTuple = (' '*40, 'Drop Files and Folders Here')
        self.filedropctrl.Append(helpTextTuple)
        self.filedropctrl.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.filedropctrl.SetColumnWidth(1, wx.LIST_AUTOSIZE)

        onButtonHandlers = self.OnListColButton
        self.buttonpnl = ButtonPanel(panel,onButtonHandlers= onButtonHandlers)

        box_v.AddSpacer(25)
        box_v.Add(self.filedropctrl,0)
        box_v.Add(self.buttonpnl,1,wx.EXPAND)

        box_h.AddSpacer(20)
        box_h.Add(box_v)
        


        panel.SetSizer(box_h)
        panel.Fit()
        # self.srcFileHelpText = 'Put '
        self.Centre()

        self.Show()
    
    def OnFilesDropped(self, filenameDropDict):
        # print('here!')
        dropTarget = self.filedropctrl
        # print(dropTarget)
        dropCoord = filenameDropDict[ 'coord' ]                 # Not used as yet.
        pathList = filenameDropDict[ 'pathList' ]
        leafFolderList = filenameDropDict[ 'basenameList' ]     # leaf folders, not basenames !
        commonPathname = filenameDropDict[ 'pathname' ]
        self.excelfile = filenameDropDict['ExcelFile']
        self.errorfile = filenameDropDict['ErrorFile']

        for aPath in pathList:
            # print('here! 1')
            if not os.path.isdir(aPath):
                # print(self.filesAndLinks)
                if (aPath not in self.filesAndLinks):
                    self.filesAndLinks.append(aPath)
                    # print('here! 3')
                _ParentPath, basename = os.path.split(aPath)
                textTuple = (basename,commonPathname)
                dropTarget.WriteTextTuple( textTuple )
                    # print('here! 4')
        # print(self.filesAndLinks)
                    # self.filedropctrl.WriteTextTuple(textTuple)

    
    def OnListColButton(self,event):
        print('Click Successfully!')
        # self.filedropctrl.GetInfo()
        # print(self.filedropctrl.dropFunc)
        print(self.filesAndLinks)
        pass

class ButtonPanel(wx.Panel):

    def __init__(self,parent = None, id = -1, onButtonHandlers = None):

        super(ButtonPanel, self).__init__(parent = parent , id = id)

        listALL = wx.Button(self,-1,'List Columns')

        listALL.Bind(wx.EVT_LEFT_DOWN, onButtonHandlers)

        btnPanel_innerHorzSzr = wx.BoxSizer( wx.HORIZONTAL )
        btnPanel_innerHorzSzr.AddStretchSpacer( prop=1 )
        btnPanel_innerHorzSzr.Add(listALL)
        btnPanel_innerHorzSzr.AddSpacer( 25 )

        btnPanel_innerHorzSzr.AddStretchSpacer( prop=1 )

        btnPanel_outerVertSzr = wx.BoxSizer( wx.VERTICAL )
        btnPanel_outerVertSzr.AddSpacer( 5 )
        btnPanel_outerVertSzr.Add( btnPanel_innerHorzSzr, flag=wx.EXPAND )
        btnPanel_outerVertSzr.AddSpacer( 5 )

        self.SetSizer( btnPanel_outerVertSzr )
        self.Layout()
