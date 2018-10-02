import sys,os
import wx

from BasicClass import DropTarget as DT
from BasicClass import FileCtrl as FC
from frame import NewListFrame as NLF

from collections import defaultdict


class AppFrame(wx.Frame):

    def __init__(self,args,argc,title = 'Demo',file_path = None):

        self.file_path = file_path

        super(AppFrame,self).__init__(parent = None, id =-1, title = title, size = (800,600))

        self.filesAndLinks = list()
        self.no_resize = wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER | 
                                                # wx.RESIZE_BOX | 
                                                wx.MAXIMIZE_BOX)

        self.SetBackgroundColour(wx.WHITE)
        panel = wx.Panel(self,-1)
        

        # wx.StaticText(self, -1,"Any files and links",(10,1))
        self.filedropctrl = FC.FileCtrl(panel,size = (550,300),style = wx.LC_REPORT|wx.BORDER_SUNKEN)
        self.filedropctrl.InsertColumn(0,'File or Link Name')
        self.filedropctrl.InsertColumn(1,'Parent Path')
        self.filedropctrl.InsertColumn(2,'File Type')
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
        self.buttonpnl = ButtonPanel(panel,onButtonHandlers= onButtonHandlers,size = (-1,100),style= self.no_resize)
        # self.buttonpnl.SetAutoLayout(True) 
        # self.buttonpnl.SetSize(wx.Size(300,400)) 
        # style = self.buttonpnl.GetWindowStyle()
        # self.buttonpnl.SetWindowStyle(style & (~wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX))
        # self.Refresh()
        # listALL = wx.Button(self,-1,'List Columns')
        box_h = wx.BoxSizer(wx.VERTICAL)
        box_v = wx.BoxSizer(wx.HORIZONTAL)
        box_v.AddSpacer(25)
        box_v.Add(self.filedropctrl,1,wx.EXPAND)
        box_v.AddSpacer(25)
        box_v.Add(self.buttonpnl,0,wx.EXPAND)
        # box_v.Add(listALL,0，wx.EXPAND)

        box_h.AddSpacer(20)
        box_h.Add(box_v,-1,wx.EXPAND)
        box_h.AddSpacer(20)


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
        filetype = filenameDropDict['filetype']
        # self.excelfile = filenameDropDict['ExcelFile']
        # self.errorfile = filenameDropDict['ErrorFile']
        for aPath in pathList :     # May include folders.

            # Keep just files and link files.
            if not os.path.isdir( aPath ) :

                if (aPath not in self.filesAndLinks) :
                    self.filesAndLinks.append( aPath )

                _ParentPath, basename = os.path.split( aPath )
                namelist = basename.split('.')
                afiletype = namelist[len(namelist)-1]
                textTuple = (commonPathname, basename, afiletype)
                dropTarget.WriteTextTuple( textTuple )
        # for aPath in pathList:
        #     # print('here! 1')
        #     if not os.path.isdir(aPath):
        #         # print(self.filesAndLinks)
        #         if (aPath not in self.filesAndLinks):
        #             self.filesAndLinks.append(aPath)
        #             # print('here! 3')
        #         _ParentPath, basename = os.path.split(aPath)
        #         textTuple = (basename,commonPathname)
        #         dropTarget.WriteTextTuple( textTuple )
                    # print('here! 4')
        # print(self.filesAndLinks)
                    # self.filedropctrl.WriteTextTuple(textTuple)

    # def FrameStyle(self):
        
    # def OnListColButton(self,event):
    #     print('Click Successfully!')
    #     # self.filedropctrl.GetInfo()
    #     # print(self.filedropctrl.dropFunc)
    #     print(self.filesAndLinks)
    #     pass
    def ListCol(self): 
        pathlist = self.filedropctrl.GetEntries()
        # listcol_error_meg = ''
        self.col_dict = {}
        type_list = []
        path_list = []
        name_list = []
        print(pathlist)
        for p,f,t in pathlist:
            assert(t in self.filedropctrl.supportfiletype), "Not support for %s file" %(t)
            # print(type(p))
            # print(f)
            # print(t)
            path_list.append(p)
            type_list.append(t)
            name_list.append(f)
        # print(path_list,type_list,name_list)   
        num_errors = type_list.count('errors')
        num_xlsx = type_list.count('xlsx')
        num_sql = type_list.count('sql')

        if len(type_list) == num_errors + num_xlsx:
            return self.filedropctrl.GetInfo(pathlist,type_list,path_list,name_list)
        else: 
            raise Exception('Only support Excel or Error file!') 
            # TODO: ErrorFrame here!
    def OnListColButton(self, event):
        col_dict = self.ListCol()
        ListCol_frame = NLF.NewListFrame(col_dict,self.file_path)
        list_ctrl = ListCol_frame.ListColInfo(col_dict)
        ListCol_frame.Show()

class ButtonPanel(wx.Panel):

    def __init__(self,parent = None, id = -1, onButtonHandlers = None,size = wx.DefaultSize,style = wx.DEFAULT_FRAME_STYLE):

        super(ButtonPanel, self).__init__(parent = parent , id = id,size = size, style = style)

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
