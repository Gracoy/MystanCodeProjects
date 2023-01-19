from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GLabel
from campy.gui.events.mouse import onmouseclicked


class Sierpinski:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.window = GWindow(self.width, self.height)  # The window to print Sierpinski Triangle

        self.__active = False
        self.__finish = False

        self.__start_icon = GLabel('START')
        self.__start_icon.font = 'Times New Roman-24-bold'
        self.window.add(self.__start_icon, 10, 50)

        self.__clear_icon = GLabel('CLEAR')
        self.__clear_icon.font = 'Times New Roman-24-bold'
        self.window.add(self.__clear_icon, 150, 50)

        onmouseclicked(self.start_or_clear)

    def start_or_clear(self, event):
        if self.window.get_object_at(event.x, event.y) is self.__start_icon:
            if not self.__finish:
                self.__active = True
        elif self.window.get_object_at(event.x, event.y) is self.__clear_icon:
            if not self.__active:
                self.window.clear()
                self.window.add(self.__start_icon, 10, 50)
                self.window.add(self.__clear_icon, 150, 50)
                self.__finish = False

    @property
    def program_active(self):
        return self.__active

    def set_turn_off_active(self):
        self.__active = False

    def set_turn_on_finish(self):
        self.__finish = True
