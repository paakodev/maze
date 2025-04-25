from tkinter import Tk, BOTH, Canvas
from line import Line

class Window:
    def __init__(self, width: int, height: int) -> None:
        self.__root = Tk()
        self.__root.title("A simple maze solver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__canvas = Canvas(self.__root, width=width, height=height)
        self.bg_color = self.__canvas.cget("background")
        self.__canvas.pack()
        self.__running = False
        
    def redraw(self) -> None:
        self.__root.update_idletasks()
        self.__root.update()
        
    def wait_for_close(self) -> None:
        """Enter main loop and keep redrawing until the window is closed."""
        self.__running = True
        while self.__running:
            self.redraw()
            
    def close(self) -> None:
        self.__running = False
        
    def draw_line(self, line: Line, fill_color: str) -> None:
        line.draw(self.__canvas, fill_color)