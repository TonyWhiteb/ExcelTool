import sys,os
import wx
import pandas as pd
from pandas import ExcelWriter

from DropDragCtrl import ListColCtrl as lcc

class ListColFrame(wx.Frame):

    # def __init__(self, title ='2nd Demo'):
    #
    #
    #     super(ListColFrame, self).__init__(parent = None, id = -1, title = title, pos = (700,300))
    #     self.SetClientSize((650,400))
    #     colPanel = wx.Panel(self,-1)
    #     colPanel.SetName('colPanel')
    #     colPanel.SetBackgroundColour(wx.WHITE)
    #
    #     self.listcolctrl = lcc.ListColCtrl(colPanel, size= (50,200), label = 'All columns list')
    def __init__(self,big_dict,file_path):
        wx.Frame.__init__(self,None, wx.ID_ANY, "2nd_Demo",pos=(700,300))
        self.SetClientSize((650,400))
        panel = wx.Panel(self, wx.ID_ANY)
        onButtonHandlers = self.onSaveFile
        self.buttonPanel = ButtonPanel(panel, onButtonHandlers = onButtonHandlers)
        self.file_path = file_path
        self.currentDirectory = os.getcwd()
        self.big_dict = big_dict
        self.filelist = []
        self.filedict = {}
        self.index_list =[]
        self.final_col_list = []
        self.items = []
        self.index = 0
        # self.column_name = []
        self.list_ctrl = lcc.ListColCtrl(panel, size = (500,304), style = wx.LC_REPORT|wx.BORDER_SUNKEN)
        self.list_ctrl.InsertColumn(0,'Column Name')
        self.list_ctrl.InsertColumn(1,'File Name')
        #
        #
        #
        frmPnl_vertSzr = wx.BoxSizer( wx.VERTICAL )
        frmPnl_vertSzr.AddSpacer( 10 ) #space on the top
        frmPnl_vertSzr.Add(self.list_ctrl, flag = wx.EXPAND) #insert sub panel
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
        panel.SetSizerAndFit( frmPnl_outerHorzSzr )
    def ListColInfo(self,big_dict):
        key_list = []
        value_list =[]

        for key, value in big_dict.items():
            key_list.append(key)
            value_list.append(value)
        if len(key_list) == len(value_list):
            for i in range(len(key_list)):
                for k in value_list[i]:
                    k_list =[]
                    k_list.append(k)
                    for j in range(len(k_list)) :
                        self.list_ctrl.InsertItem(j,k_list[j])
                        self.list_ctrl.SetItem(j,1,key_list[i])

        self.Autosize()
        self.filelist = key_list
        self.filedict = self.filedict.fromkeys(key_list)
        return self.list_ctrl

    def Autosize(self):
        for colIndex in range(2):
            self.list_ctrl.SetColumnWidth(colIndex,wx.LIST_AUTOSIZE)

    def OnFinalButton(self,event):
        self.index_list = self.list_ctrl.getSelected_id()
        column_name = []
        # items = self.list_ctrl.GetItem(index_list[0], 1)
        for filename in self.filelist:
            item_list = []
            for i in range(len(self.index_list)):
                if filename == self.list_ctrl.GetItemText(self.index_list[i],1):
                    item_list.append(self.list_ctrl.GetItemText(self.index_list[i],0))
            self.filedict[filename]= item_list
            column_name += self.filedict[filename]
        column_name = list(set(column_name))
        self.final_col_list = column_name

        # for i in range(len(self.index_list)):
        #     # self.items.append(self.list_ctrl.GetItemText(self.index_list[i],0))
        #     for filename in self.filelist:
        #         item_list = []
        #         if filename == self.list_ctrl.GetItemText(self.index_list[i],1):
        #             item_list.append(self.list_ctrl.GetItemText(self.index_list[i],0))
        #             self.filedict[filename]= item_list

        os.chdir(self.file_path)
        self.onSaveFile()
        print(self.file_path)
        print(self.currentDirectory)


        # print(column_name)
    def onSaveFile(self,event):

        dlg = wx.FileDialog(
              self, message = "Save File As",
              defaultDir=self.currentDirectory,
              defaultFile = "",wildcard="Excel files (*.xlsx)|*.xlsx",
              style= wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        )
        if dlg.ShowModal() == wx.ID_OK:
            final_filename = dlg.GetFilename()
            path = dlg.GetPath()
            self.index_list = self.list_ctrl.getSelected_id()
            column_name = []
            # items = self.list_ctrl.GetItem(index_list[0], 1)
            for filename in self.filelist:
                item_list = []
                for i in range(len(self.index_list)):
                    if filename == self.list_ctrl.GetItemText(self.index_list[i],1):
                        item_list.append(self.list_ctrl.GetItemText(self.index_list[i],0))
                self.filedict[filename]= item_list
                column_name += self.filedict[filename]
            column_name = list(set(column_name))
            df_final = pd.DataFrame(columns = column_name)
            for key in self.filedict:
                df = pd.DataFrame.from_dict(self.big_dict[key])
                df_need = df.loc[:,self.filedict.get(key)]
                df_final = df_final.append(df_need)
            basename = os.path.split(path)
            os.chdir(basename[0])
            # print(filename)
            writer = ExcelWriter(final_filename)
            df_final.to_excel(writer,'Sheet1', index = False)
            writer.save()

        dlg.Destroy()

    def SaveFile(self):
        df_final = pd.DataFrame(columns = self.final_col_list)
        for key in self.filedict:
            df = pd.DataFrame.from_dict(self.big_dict[key])
            df_need = df.loc[:,self.filedict.get(key)]
            df_final = df_final.append(df_need)

        writer = ExcelWriter('PythonExport.xlsx')
        df_final.to_excel(writer,'Sheet1', index = False)
        writer.save()


    def GetWidth(self):
        table_width = self.list_ctrl.GetSize()[0]
        return table_width

class ButtonPanel(wx.Panel):

    def __init__(self, parent= None, id= -1, onButtonHandlers = None):

        super(ButtonPanel, self).__init__(parent = parent, id = id)

        listAllBtn = wx.Button(self, -1, 'Create Final File')

        listAllBtn.Bind(wx.EVT_LEFT_DOWN, onButtonHandlers)

        btnPanel_innerHorzSzr = wx.BoxSizer( wx.HORIZONTAL )
        btnPanel_innerHorzSzr.AddStretchSpacer( prop=1 )
        btnPanel_innerHorzSzr.Add( listAllBtn )
        btnPanel_innerHorzSzr.AddSpacer( 25 )

        btnPanel_innerHorzSzr.AddStretchSpacer( prop=1 )

        btnPanel_outerVertSzr = wx.BoxSizer( wx.VERTICAL )
        btnPanel_outerVertSzr.AddSpacer( 5 )
        btnPanel_outerVertSzr.Add( btnPanel_innerHorzSzr)
        btnPanel_outerVertSzr.AddSpacer( 5 )

        self.SetSizer( btnPanel_outerVertSzr )
        self.Layout()
