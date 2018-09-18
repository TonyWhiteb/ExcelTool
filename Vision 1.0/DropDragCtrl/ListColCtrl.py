import sys,os
import wx
import  wx.lib.mixins.listctrl  as  listmix
class ListColCtrl(wx.ListCtrl, listmix.CheckListCtrlMixin, listmix.ListCtrlAutoWidthMixin):

    # def __init__(self, parent, size =(-1,200), label = 'default col list'):
    #
    #     super( ListColCtrl, self).__init__(parent = parent, id= -1, style = wx.SIMPLE_BORDER)
    #
    #     lccLabel = wx.StaticText(self, -1, label = label, size = (-1,20))
    def __init__(self, *args, **kwargs):
        wx.ListCtrl.__init__(self,*args,**kwargs)
        listmix.CheckListCtrlMixin.__init__(self)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        # self.setResizeColumn(0)

        self.selected = []
        self.selected_id = []

        self.Bind(wx.EVT_CHECKBOX, self.OnCheckItem)

    def OnCheckItem(self,index, flag ):

        if flag == True:
            self.selected.append(self.GetItemText(index))
            self.selected_id.append(index)
        else:
            self.selected.remove(self.GetItemText(index))
            self.selected_id.remove(index)

    def getSelected_id(self):
        return  self.selected_id
