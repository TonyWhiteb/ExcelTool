import sys,os
import wx
import pandas as pd
from pandas import ExcelWriter

from BasicClass import FileCtrl as fc

class NewListFrame(wx.Frame):

    def __init__(self,col_dict,file_path):

        wx.Frame.__init__(self,None,wx.ID_ANY,"List Columns",pos= (700,300))
        self.SetClientSize((650,400))
        panel = wx.Panel(self,wx.ID_ANY)

        self.col_dict = col_dict
        self.file_path = file_path
        self.filelist = []
        self.filedict = {}

        self.list_ctrl = fc.FileCtrl(panel, size = (500,304),style = wx.LC_REPORT|wx.BORDER_SUNKEN)
        self.list_ctrl.InsertColumn(0,'Column Name')
        self.list_ctrl.InsertColumn(1,'File Name')

        helpTextTuple = (' '*40, 'These is no columns in this file')
        self.list_ctrl.Append(helpTextTuple)
        self.list_ctrl.SetColumnWidth(0,wx.LIST_AUTOSIZE)
        self.list_ctrl.SetColumnWidth(1,wx.LIST_AUTOSIZE)

        onButtonHandlers = self.onSaveFile
        self.buttonpnl = ButtonPanel(panel, onButtonHandlers=onButtonHandlers)

        box_h = wx.BoxSizer(wx.HORIZONTAL)
        box_v = wx.BoxSizer(wx.VERTICAL)
        box_v.AddSpacer(25)
        box_v.Add(self.list_ctrl,0,wx.EXPAND)
        box_v.Add(self.buttonpnl,100,wx.EXPAND)


        box_h.AddSpacer(20)
        box_h.Add(box_v,2,wx.EXPAND)
        box_h.AddSpacer(20)
        panel.SetSizer(box_h)
        panel.Fit()
        self.Centre()
        self.Show()

    def ListColInfo(self,col_dict):
        key_list = []
        value_list =[]

        for key, value in col_dict.items():
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

    def onSaveFile(self,event):
        pass
        # dlg = wx.FileDialog(
        #       self, message = "Save File As",
        #       defaultDir=self.currentDirectory,
        #       defaultFile = "",wildcard="Excel files (*.xlsx)|*.xlsx",
        #       style= wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        # )
        # if dlg.ShowModal() == wx.ID_OK:
        #     final_filename = dlg.GetFilename()
        #     path = dlg.GetPath()
        #     self.index_list = self.list_ctrl.getSelected_id()
        #     column_name = []
        #     # items = self.list_ctrl.GetItem(index_list[0], 1)
        #     for filename in self.filelist:
        #         item_list = []
        #         for i in range(len(self.index_list)):
        #             if filename == self.list_ctrl.GetItemText(self.index_list[i],1):
        #                 item_list.append(self.list_ctrl.GetItemText(self.index_list[i],0))
        #         self.filedict[filename]= item_list
        #         column_name += self.filedict[filename]
        #     column_name = list(set(column_name))
        #     df_final = pd.DataFrame(columns = column_name)
        #     for key in self.filedict:
        #         df = pd.DataFrame.from_dict(self.col_dict[key])
        #         df_need = df.loc[:,self.filedict.get(key)]
        #         df_final = df_final.append(df_need)
        #     basename = os.path.split(path)
        #     os.chdir(basename[0])
        #     # print(filename)
        #     writer = ExcelWriter(final_filename)
        #     df_final.to_excel(writer,'Sheet1', index = False)
        #     writer.save()

        # dlg.Destroy()


class ButtonPanel(wx.Panel):

    def __init__(self,parent = None, id = -1, onButtonHandlers = None):

        super(ButtonPanel, self).__init__(parent = parent , id = id)

        listALL = wx.Button(self,-1,'Create Final File')

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
