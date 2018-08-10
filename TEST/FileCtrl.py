import wx

class FileCtrl(wx.ListCtrl):
    def __init__(self,*args,**kwargs):
        super(FileCtrl,self).__init__(*args,**kwargs)

        self.currRow = None

        self.Bind(wx.EVT_LEFT_DOWN, self.OnFindCurrentRow )
        # self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.entriesList = []
        self.numEntries = 0
        self.filename = []
        self.numCols = -1
        self.haveEntries = False

    def OnFindCurrentRow(self,event): #find current row control
        if (self.currRow is not None):
            self.Select(self.currRow, False)

        row,_ignoredFlags = self.HitTest(event.GetPosition())
            # HitTest, Determine which item is at the specified point.
            # Returns index of the item or wxNOT_FOUND if no item is at the specified point.
        self.currRow = row
        self.Select(row)

    def OnRightDown(self,event): #Right click menu

        menu = wx.Menu()
        menuItem = menu.Append(-1,'Delete this file')

        self.Bind(wx.EVT_MENU, self.OnDeleteRow, menuItem)

        self.OnFindCurrentRow(event)

        self.PopupMenu(menu,event.GetPosition())

    def OnDeleteRow(self, event):

        if(self.currRow >= 0):

            assert(self.numEntries == len(self.entriesList))

            self.DeleteItem(self.currRow)
    
    def WriteTextTuple(self, rowDataTuple):

        assert(len(rowDataTuple) >= self.numCols), 'Given data must have at least %d items.' %(self.numCols)

        for idx in range(self.numCols):
            assert(isinstance(rowDataTuple[idx],(bytes,str))),'One or both data elements are not strings.'

        self.rowDataTupleTruncated = tuple(rowDataTuple[:self.numCols])
        if (self.rowDataTupleTruncated not in self.entriesList):

            if (not self.haveEntries):
                self.DeleteAllItems()

            self.Append(self.rowDataTupleTruncated)
            print(self.rowDataTupleTruncated)
            self.entriesList.append(self.rowDataTupleTruncated)
            self.numEntries += 1
            self.haveEntries = True

            self.Autosize()
    
    def Autosize(self):

        self.Append(self.rowDataTupleTruncated)
        for colIndex in range( len( self.rowDataTupleTruncated ) ) :
            self.SetColumnWidth( colIndex, wx.LIST_AUTOSIZE )

        self.DeleteItem( self.GetItemCount() - 1 )
