import wx


class MyButton(wx.PyControl):

    def __init__(self, parent, id = wx.ID_ANY, label= '', pos = wx.DefaultPosition,
                 size = wx.DefaultSize,style = wx.NO_BORDER, validator = wx.DefaultValidator,
                 name = 'MyButton'  ):
        wx.PyControl.__init__(self,parent, id, pos,size,style, validator, name)
        """
        Default class constructor.

        :param `parent`: the MyButton parent;
        :param `id`: window identifier. A value of -1 indicates a default value;
        :param `label`: the button text label;
        :param `pos`: the control position. A value of (-1, -1) indicates a default position,
         chosen by either the windowing system or wxPython, depending on platform;
        :param `size`: the control size. A value of (-1, -1) indicates a default size,
         chosen by either the windowing system or wxPython, depending on platform;
        :param `style`: the button style (unused);
        :param `validator`: the validator associated to the button;
        :param `name`: the button name.
        """
        self.Bind(wx.EVT_LEFT_DOWN, self._onMouseDown)
        self.Bind(wx.EVT_LEFT_UP, self._onMouseUp)
        self.Bind(wx.EVT_LEAVE_WINDOW, self._onMouseLeave)
        self.Bind(wx.EVT_ENTER_WINDOW, self._onMouseEnter)
        self.Bind(wx.EVT_SET_FOCUS, self._OnGainFocus)
        self.Bind(wx.EVT_KILL_FOCUS, self._OnLoseFocus)
        self.Bind(wx.EVT_ERASE_BACKGROUND,self._onEraseBackground)
        self.Bind(wx.EVT_PAINT,self._onPaint)

        self._mouseIn = self._mouseDown = False
        self._hasFocus = False

        self.SetLabel(label)
        self.SetInitialSize(size)

    def _onMouseDown(self, event):
        self._mouseDown = True

    def _onMouseUp(self, event):
        self._mouseDown = False
        self.sendButtonEvent()

    def _onMouseEnter(self, event):
        self._mouseIn = True

    def _onMouseLeave(self, event):
        self._mouseIn = False

    

    def sendButtonEvent(self):
        event = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, self.GetId())
        event.SetInt(0)
        event.SetEventObject(self)
        self.GetEventHandler().ProcessEvent(event)

    def _onEraseBackground(self,event):
        # reduce flicker
        pass

    def _onPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        dc.SetFont(self.GetFont())
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        # draw whatever you want to draw
        # draw glossy bitmaps e.g. dc.DrawBitmap
        if self._mouseIn:
            pass# on mouserover may be draw different bitmap
        if self._mouseDown:
            pass # draw different image text 
