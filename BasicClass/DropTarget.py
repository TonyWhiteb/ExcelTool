import wx
import os,sys

class DropTarget(wx.FileDropTarget):
    def __init__(self,targetControl):
        self.targetControl = targetControl

        wx.FileDropTarget.__init__(self)

    def FilenameDropDict(self):

        filenameDropDict = {}

        filenameDropDict['coord'] = (-1,-1)
        filenameDropDict['pathname'] = ''
        filenameDropDict['basenameList'] = []
        filenameDropDict['FullPathList'] = []
        filenameDropDict['ExcelFile'] = []
        filenameDropDict['ErrorFile'] = []

        return filenameDropDict

    def OnDropFiles(self, xOrd, yOrd, pathList):

        pathname, _ignored = os.path.split(pathList[0])

        basenameList = []

        for aPath in pathList :
            _ignoredDir, aBasename = os.path.split(aPath)
            basenameList.append(aBasename)


        filenameDropDict = self.FilenameDropDict()
        filenameDropDict['coord'] = (xOrd,yOrd)
        filenameDropDict['pathList'] = pathList
        filenameDropDict['pathname'] = pathname
        filenameDropDict['basenameList'] = basenameList

        filenameDropDict['ExcelFile'] = [s for s in basenameList if '.xlsx' in s]
        filenameDropDict['ErrorFile'] = [s for s in basenameList if '.error' in s]
        # print(basenameList)

        if (hasattr( self.targetControl, 'dropFunc' ))  and  \
           (self.targetControl.dropFunc != None) :

            # Call the callback function with the processed drop data.
            self.targetControl.dropFunc( filenameDropDict )
        
       # HIGHL: 
        # How to add a function dynamically
