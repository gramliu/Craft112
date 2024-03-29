from components.clickable import Clickable
from components.component import Component
from components.label import Label
from utility.constants import Constants

# Button UI component
class Button(Clickable, Component):
    def __init__(self, window, x, y,
                 width=Constants.DEFAULT_WIDTH,
                 height=Constants.DEFAULT_HEIGHT,
                 fillColor=None, borderColor=(0, 0, 0),
                 borderWidth=1, text=None, font=None,
                 textColor=(0, 0, 0), padding=0):
        Component.__init__(self, window, x, y, width=width, height=height,
            fillColor=fillColor, borderColor=borderColor,
            borderWidth=borderWidth)
        Clickable.__init__(self, x, y, width=width, height=height)
        self.type = "Button"
        self.font = font
        self.textColor = textColor
        self.label = None
        self.padding = padding
        self.text = text

        if text is not None:
            self.initText()

    def draw(self):
        if not self.isEnabled: return
        super().draw()
        if self.label is not None:
            self.label.draw()

    def setText(self, text):
        self.text = text
        self.initText()

    def initText(self):
        self.label = Label(self.window, self.x, self.y, self.text, self.font,
                               color=self.textColor)
        rect = self.label.label.get_rect()
        self.width, self.height = rect.width, rect.height
        self.width += 2*self.padding
        self.height += 2*self.padding

    def setFillColor(self, fillColor):
        self.fillColor = fillColor
