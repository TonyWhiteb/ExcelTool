import wx
import sys,os
import pandas
from collections import defaultdict

class FileCtrl(wx.ListCtrl):
    def __init__(self,*args,**kwargs):
        super(FileCtrl,self).__init__(*args,**kwargs)

        self.currRow = None

        self.Bind(wx.EVT_LEFT_DOWN, self.OnFindCurrentRow )
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.entriesList = []
        self.numEntries = 0
        self.filename = []
        self.numCols = 3
        self.haveEntries = False
        self.supportfiletype = ['errors','xlsx','sql']

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

            # self.DeleteItem(self.currRow)
            allSelectedRowData = self.GetAllSelectedRowData()

    def GetAllSelectedRowData(self):
        allSelectedRowData = []
        idx = -1
        while True: #while True loop forever
            idx = self.GetNextItem(idx,wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)
            #Searches for an item with the given geometry or state,starting from item but excluding the item itself
            #if item is -1, the first item that matches the specified flags will be returned.
            #Return the first item with given state following item or -1 if no such item found.
            if (idx == -1):
                break

            allSelectedRowData.append( self.GetItemInfo(idx))

            if (len( allSelectedRowData ) >= 1) :

                #-----

                rawRowData = allSelectedRowData[ 0 ]    # There can be only a single row selected.
                lineIdx       = rawRowData[ 0 ]
                unknownData   = rawRowData[ 1 ]
                textDataTuple = tuple( rawRowData[ 2: ] )   # Make same type as in self.entriesList

                if self.numEntries :

                    try :
                        entryListIndex = None
                        entryListIndex = self.entriesList.index( textDataTuple )
                    except ValueError :
                        print ('####  ERROR:  textDataTuple NOT FOUND in self.entriesList :')
                        print (' ', textDataTuple)
                        print

                        return
                        #-----

                    #end try

                    # Delete this row item from [ self.entriesList ].
                    del self.entriesList[ entryListIndex ]

                    # Update the status vars.
                    self.numEntries -= 1
                    if (self.numEntries < 1) :

                        self.haveEntries = False
                        self.Append( self.HelpTextTuple )

                    # Finally, detete the textList row item.
                    self.DeleteItem( self.currRow )
    def GetItemInfo(self,idx):
        rowItemList = []
        rowItemList.append(idx)
        rowItemList.append(self.GetItemData(idx)) #Gets the application-defined data associated with this item
        rowItemList.append(self.GetItemText(idx)) #gets the item text for this item, Column 0 is the default

        for i in range(1,self.GetColumnCount()):
            rowItemList.append(self.GetItem(idx, i).GetText())

        return rowItemList
      
    
    def WriteTextTuple(self, rowDataTuple):

        assert(len(rowDataTuple) >= self.numCols), 'Given data must have at least %d items.' %(self.numCols)

        for idx in range(self.numCols):
            assert(isinstance(rowDataTuple[idx],(bytes,str))),'One or both data elements are not strings.'

        self.rowDataTupleTruncated = tuple(rowDataTuple[:self.numCols])
        # print(self.numCols)
        # print(self.rowDataTupleTruncated)
        # print(self.entriesList)
        # print(self.haveEntries)
        if (self.rowDataTupleTruncated not in self.entriesList):

            if (not self.haveEntries):
                self.DeleteAllItems()

            self.Append(self.rowDataTupleTruncated)
            # print(self.rowDataTupleTruncated)
            self.entriesList.append(self.rowDataTupleTruncated)
            # print(self.entriesList)
            self.numEntries += 1
            self.haveEntries = True

            self.Autosize()
    # def GetEntriesList(self):
    #     return self.numEntries
    
    def Autosize(self):

        self.Append(self.rowDataTupleTruncated)
        for colIndex in range( len( self.rowDataTupleTruncated ) ) :
            self.SetColumnWidth( colIndex, wx.LIST_AUTOSIZE )

        self.DeleteItem( self.GetItemCount() - 1 )
        """
        If any one filename is very long the column width was set too long and
          occupies "too much" width in the control causing little or no display
          of the folder paths to be shown.

        Set first row's width to no more than 50% of the control's client width.
        This is a "reasonable" balance which leaves both columns's data
           at least 50% displayed at all times.
        """
        firstColMaxWid = self.GetClientSize()[ 0 ] / 2      # Half the avaiable width.
        firstColIndex = 0                           # Avoid the use of "Magic Numbers".
        firstColActualWid = self.GetColumnWidth( firstColIndex )
        reasonableWid = min( firstColMaxWid, firstColActualWid )
        self.SetColumnWidth( firstColIndex, reasonableWid )
    def GetEntries(self):
        print(self.entriesList)
        return self.entriesList
    def ErrorProcess(self):
        
        pass
    def GetInfo(self,pathlist,type_list,path_list,name_list):
        # print(self.entriesList)
        def_dict = defaultdict(list)
        excel_dict = {}
        error_dict = {}
        self.col_dict = {}
        for p,f,t in pathlist:
            assert(t in self.supportfiletype), "Not support for %s file" %(t)
            # self.filename = []
            # self.filename.append(f)
            os.chdir(p)
            
            if t == 'errors':
                
                afile_list = []
                sp = {}
                
                afile = open(f,"r").readlines()
                afile_list = afile[0].split('\t')
                sp = sp.fromkeys(afile_list)
                for m in range(1,len(afile)):
                    value = []
                    value = afile[m].split('\t')
                    for n in range(len(afile_list)):
                        if sp[afile_list[n]] == None:
                            sp[afile_list[n]] = {m-1:value[n]}
                        else:
                            sp[afile_list[n]].update({m-1:value[n]}) 
                        print(sp)       
                error_dict[f] = sp
            elif t == 'xlsx':
                xl = pd.ExcelFile(f)
                sn = xl.sheet_names
                df = {}
                col = {}
                df = xl.parse(sn[0])
                excel_dict[f] = df.to_dict()  
        
        self.col_dict = error_dict.copy()
        self.col_dict.update(excel_dict)

        return self.col_dict

