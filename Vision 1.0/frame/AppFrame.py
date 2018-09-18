import sys,os
import wx

from DropDragCtrl import FileDropCtrl as fdctrl
from DropDragCtrl import DragandDrop as ddt
from frame import ListColFrame as lcc
import  wx.lib.mixins.listctrl  as  listmix
from collections import defaultdict

try :                   # For shortening long paths in MSW, only.
    import win32api
    ntGetShortpathname = win32api.GetShortPathName
except :
    ntGetShortpathname = None


class AppFrame(wx.Frame):

    def __init__(self, args,argc,title = 'Demo', file_path = None):


        self.file_path = file_path
        super(AppFrame, self).__init__(parent = None, id= -1, title = title, pos=(800,400))
        self.SetClientSize((650,400))
        frmPanel = wx.Panel(self,-1)
        frmPanel.SetName('frmPanel')
        frmPanel.SetBackgroundColour(wx.WHITE)
        #
        self.filesAndLinks = list()
        self.exeFolder = None
        self.incFoldersList = list()
        self.filename = []
        self.excelfile = []
        self.errorfile = []
        # create the basic panel and go to create first control
        self.filedropctrl = fdctrl.FileDropCtrl(frmPanel,size = (50,200), label='Any Files and Links :')
        self.filedropctrl.SetName('AppFrame::self.filesDropCtrl')
        #Create the sub panel for list control
        self.filedropctrl.SetCallbackFunc(self.OnFilesDropped)
        # self.filedropctrl.SetBackgroundColour(wx.BLUE)
        headerLabelList = [ 'File or Link Name', 'Parent Path' ]
        self.filedropctrl.WriteHeaderLabels( headerLabelList )

        srcFilesHelpText = 'Drop Files and Links Here'
        self.filedropctrl.WriteHelptext( srcFilesHelpText )

        onButtonHandlers = self.OnListColButton

        self.buttonPanel = ButtonPanel(frmPanel, onButtonHandlers = onButtonHandlers)
        #
        #Frame layout control
        #
        frmPnl_vertSzr = wx.BoxSizer( wx.VERTICAL )
        frmPnl_vertSzr.AddSpacer( 10 ) #space on the top
        frmPnl_vertSzr.Add(self.filedropctrl, flag = wx.EXPAND) #insert sub panel
        frmPnl_vertSzr.AddSpacer(10) #space on the bottom
        frmPnl_vertSzr.Add( self.buttonPanel,    flag=wx.EXPAND )
        frmPnl_vertSzr.AddSpacer( 10 )

        frmPnl_outerHorzSzr = wx.BoxSizer( wx.HORIZONTAL )
        frmPnl_outerHorzSzr.AddSpacer( 10 )     # space on the left
        frmPnl_outerHorzSzr.Add( frmPnl_vertSzr, proportion=1 )
        frmPnl_outerHorzSzr.AddSpacer( 10 ) #space on the right
        #
        #
        #
        frmPanel.SetSizerAndFit( frmPnl_outerHorzSzr )
        self.Show()

    def OnFilesDropped(self, filenameDropDict):

        dropTarget = self.filedropctrl.GetDropTarget()

        dropCoord = filenameDropDict[ 'coord' ]                 # Not used as yet.
        pathList = filenameDropDict[ 'pathList' ]
        leafFolderList = filenameDropDict[ 'basenameList' ]     # leaf folders, not basenames !
        commonPathname = filenameDropDict[ 'pathname' ]
        self.excelfile = filenameDropDict['ExcelFile']
        self.errorfile = filenameDropDict['ErrorFile']
        if (os.name == 'nt')  and  (ntGetShortpathname != None) :
            if (len( commonPathname ) > 40) :             # Set an arbitrary max width.
                commonPathname = ntGetShortpathname( commonPathname )

        # Write (.append) a text 2-element list for each basename
        for aPath in pathList :     # May include folders.

            # Keep just files and link files.
            if not os.path.isdir( aPath ) :

                if (aPath not in self.filesAndLinks) :
                    self.filesAndLinks.append( aPath )

                _longFormParentPath, basename = os.path.split( aPath )
                textTuple = (basename, commonPathname)
                dropTarget.WriteTextTuple( textTuple )





        # col1 = []
        # col2 = []
        # col3 = []
        # for i in range(len(pathlist)):
        #     os.chdir(ntGetShortpathname(pathlist[i][1]))
        #     afile = open(pathlist[i][0],"r").readlines()
        #     col1 = afile[0].split('\t')
        #     col3 = list(set(col1)|set(col2))
        #     col2 = col1




    def OnListColButton(self, event):
        big_dict = self.filedropctrl.GetInfo()
        new_frame = lcc.ListColFrame(big_dict,self.file_path)
        list_ctrl = new_frame.ListColInfo(big_dict)
        new_frame.Show()
        print(big_dict)



#
#
#
class ButtonPanel(wx.Panel):

    def __init__(self, parent= None, id= -1, onButtonHandlers = None):

        super(ButtonPanel, self).__init__(parent = parent, id = id)

        listAllBtn = wx.Button(self, -1, 'List Columns')

        listAllBtn.Bind(wx.EVT_LEFT_DOWN, onButtonHandlers)

        btnPanel_innerHorzSzr = wx.BoxSizer( wx.HORIZONTAL )
        btnPanel_innerHorzSzr.AddStretchSpacer( prop=1 )
        btnPanel_innerHorzSzr.Add( listAllBtn )
        btnPanel_innerHorzSzr.AddSpacer( 25 )

        btnPanel_innerHorzSzr.AddStretchSpacer( prop=1 )

        btnPanel_outerVertSzr = wx.BoxSizer( wx.VERTICAL )
        btnPanel_outerVertSzr.AddSpacer( 5 )
        btnPanel_outerVertSzr.Add( btnPanel_innerHorzSzr, flag=wx.EXPAND )
        btnPanel_outerVertSzr.AddSpacer( 5 )

        self.SetSizer( btnPanel_outerVertSzr )
        self.Layout()
