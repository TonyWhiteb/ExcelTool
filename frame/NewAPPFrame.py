import sys,os
import wx

from BasicClass import DropTarget as DT
from BasicClass import FileCtrl as FC


from collections import defaultdict


class Appframe(wx.Frame):

    def __init__(self,args,argc,title = 'Demo'):

        super(Appframe,self).__init__(parent = None, id =-1, title = title, size = (650,400))

        panel = wx.Panel(self)
        
        wx.StaticText(self, -1 "Any files and links",(10,1))
        self.filedropctrl = FC.FileCtrl(panel,pos = (10,15), size = (50,200),style = wx.LC_REPORT|wx.BORDER_SUNKEN)

