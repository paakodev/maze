from tkinter import LEFT, Button, Entry, Frame, Label, OptionMenu, StringVar, Tk, Canvas
from typing import Callable
from line import Line

class Window:
    def __init__(self, width: int, height: int) -> None:
        self.__root = Tk()
        self.__root.title("A simple maze solver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        
        self.__input_frame = Frame(self.__root)
        self.__input_frame.pack()

        Label(self.__input_frame, text="Rows:").pack(side=LEFT)
        self.rows_entry = Entry(self.__input_frame, width=5)
        self.rows_entry.insert(0, "10")
        self.rows_entry.pack(side=LEFT)

        Label(self.__input_frame, text="Cols:").pack(side=LEFT)
        self.cols_entry = Entry(self.__input_frame, width=5)
        self.cols_entry.insert(0, "10")
        self.cols_entry.pack(side=LEFT)
        
        self.speed_var = StringVar(self.__root)
        self.speed_var.set("Medium")  # Default

        self.speed_menu = OptionMenu(self.__input_frame, self.speed_var, "Super-fast", "Fast", "Medium", "Slow")
        self.speed_menu.pack(side=LEFT)

        self.animation_speeds = {
            "Super-fast": 0.001,
            "Fast": 0.01,
            "Medium": 0.05,
            "Slow": 0.2,
        }

        self.generate_button = Button(self.__input_frame, text="Generate!", command=self._on_generate)
        self.generate_button.pack(side=LEFT)
        
        self.__canvas = Canvas(self.__root, width=width, height=height)
        self.bg_color = self.__canvas.cget("background")
        self.__canvas.pack()
        
        self.__running = False
        self._generate_callback = None
        
        self._input_widgets = [
            self.rows_entry,
            self.cols_entry,
            self.speed_menu,
            self.generate_button,
        ]

    def _set_inputs_enabled(self, enabled: bool) -> None:
        state = "normal" if enabled else "disabled"
        for widget in self._input_widgets:
            widget.config(state=state)

    def set_generate_callback(self, fn: Callable[[int, int], None]) -> None:
        self._generate_callback = fn

    def _on_generate(self) -> None:
        if self._generate_callback:
            self._set_inputs_enabled(False)
            try:
                rows = int(self.rows_entry.get())
                cols = int(self.cols_entry.get())
                self._generate_callback(rows, cols)
            finally:
                self._set_inputs_enabled(True)

    def get_canvas(self) -> Canvas:
        return self.__canvas
    
    def get_delay(self) -> float:
        return self.animation_speeds.get(self.speed_var.get(), 0.05)
        
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