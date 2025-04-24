from window import Window
from point import Point
from line import Line

class Cell:
    def __init__(self, 
                 x1: int, y1: int, x2: int, y2: int, window: Window,
                 wall_color: str = "black",
                 has_left_wall: bool = True, 
                 has_right_wall: bool = True,
                 has_top_wall: bool = True,
                 has_bottom_wall: bool = True
                 ) -> None:
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self._win = window
        # Precompute the four corner points
        self._top_left = Point(x1, y1)
        self._top_right = Point(x2, y1)
        self._bottom_left = Point(x1, y2)
        self._bottom_right = Point(x2, y2)
        # Precompute potential wall lines
        self._left_wall = Line(self._top_left, self._bottom_left)
        self._right_wall = Line(self._top_right, self._bottom_right)
        self._top_wall = Line(self._top_left, self._top_right)
        self._bottom_wall = Line(self._bottom_left, self._bottom_right)
        # Precompute center
        self._center = Point((x1+x2)//2, (y1+y2)//2)
        self._wall_color = wall_color
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall

    def draw(self) -> None:
        if self.has_top_wall:
            self._win.draw_line(self._top_wall, self._wall_color)
        if self.has_left_wall:
            self._win.draw_line(self._left_wall, self._wall_color)
        if self.has_bottom_wall:
            self._win.draw_line(self._bottom_wall, self._wall_color)
        if self.has_right_wall:
            self._win.draw_line(self._right_wall, self._wall_color)
            
    def draw_move(self, to_cell: 'Cell', undo: bool = False) -> None:
        fill_color = "gray" if undo else "red"
        self._win.draw_line(Line(self._center, to_cell._center), fill_color)