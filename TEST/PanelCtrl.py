import wx

import FileCtrl

# class PanelCtrl(FileCtrl):
#     def __init__(self,*args,**kwargs):
#         super(PanelCtrl,self).__init__(*args,**kwargs)

class PanelTemp(wx.Panel):
    def __init__(self, parent, callbackFunc = None, size= (100,200), label = 'default title',DEVEL = False):
        super(PanelTemp,self).__init__(parent = parent, id = -1, style = wx.SIMPLE_BORDER)

        self.callbackFunc = callbackFunc

        fdcID = wx.NewId()

        self.filesListCtrl = FileCtrl.FileCtrl(self,fdcID, size = size, style = wx.LC_REPORT)

        


    def WriteHeaderLabels( self, headerLabelList ) :
        """ Write the column header labels. """

        self.headerLabelList = headerLabelList
        #-----

        # This sets the "official" number of columns the textCtrl has.
        self.numCols = len( self.headerLabelList )
        self.filesListCtrl.numCols = self.numCols

        for col in range( self.numCols ) :
            self.filesListCtrl.InsertColumn( col, self.headerLabelList[ col ] )

        # AUTOSIZE
        for col in range( self.numCols ) :
            self.filesListCtrl.SetColumnWidth( col, wx.LIST_AUTOSIZE )

        # Widen the header-list-as-row-data in order to completely show the column labels.
        # This hack works very well !
        # hdrListWidened = headerLabelList
        # for i in range( len( hdrListWidened ) ) :
        #     hdrListWidened[ i ] += ' '     # Estimated number of spaces needed
        #                                     #   to fully show the header.
        # # Delete the header-list-as-row-data.
        # self.filesListCtrl.Append( hdrListWidened )   # Does NOT add to item/row data list.
        # numRows = self.filesListCtrl.GetItemCount()
        # self.filesListCtrl.DeleteItem( numRows - 1 )

    def WriteHelptext( self, helpText = 'Drop here!') :
        """ Write a message to be erased on the first file drop. """

        helpTextTuple = [ ' '*20, helpText ]
        self.filesListCtrl.Append( helpTextTuple )

        for col in range( 2 ) :       # Widen the column widths.
            self.filesListCtrl.SetColumnWidth( col, wx.LIST_AUTOSIZE )

        # Save for rewriting if all list entries have been deleted.
        self.filesListCtrl.HelpTextTuple = helpTextTuple