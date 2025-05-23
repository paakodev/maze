from window import Window
from point import Point
from line import Line

class Cell:
    def __init__(self, 
                 x1: int, y1: int, x2: int, y2: int, 
                 window: Window = None, # type: ignore
                 wall_color: str = "black",
                 removed_color: str = None, # type: ignore
                 has_left_wall: bool = True, 
                 has_right_wall: bool = True,
                 has_top_wall: bool = True,
                 has_bottom_wall: bool = True
                 ) -> None:
        """This class represents a single cell of a rectangular maze.

        Args:
            x1 (int): Upper-left X coordinate
            y1 (int): Upper-left Y coordinate
            x2 (int): Lower-right X coordinate
            y2 (int): Lower-right Y coordinate
            window (Window): The window this cell is to be painted in. Do not leave empty, the default exists to handle testing.
            wall_color (str, optional): The color used for the walls. Defaults to "black".
            removed_color (str, optional): The color used for removed walls. Defaults to the canvas' background color.
            has_left_wall (bool, optional): Is the left wall present. Defaults to True.
            has_right_wall (bool, optional): Is the right wall present. Defaults to True.
            has_top_wall (bool, optional): Is the top wall present. Defaults to True.
            has_bottom_wall (bool, optional): Is the bottom wall present. Defaults to True.
        """
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
        self._removed_color = removed_color or (self._win.bg_color if self._win else "white")
        
        self.visited = False # For generation/solving
        
    def __repr__(self) -> str:
        return (f"Cell(x1={self._x1}, y1={self._y1}, x2={self._x2}, y2={self._y2}, "
                f"L={'Y' if self.has_left_wall else 'N'}, "
                f"R={'Y' if self.has_right_wall else 'N'}, "
                f"T={'Y' if self.has_top_wall else 'N'}, "
                f"B={'Y' if self.has_bottom_wall else 'N'}, "
                f"visited={'Y' if self.visited else 'N'})")

    def draw(self) -> None:
        """Draws the separate walls of the cell."""
        if self._win is None:
            return # 'Headless' mode for testing purposes.
        
        walls = [
            (self._top_wall, self.has_top_wall),
            (self._left_wall, self.has_left_wall),
            (self._bottom_wall, self.has_bottom_wall),
            (self._right_wall, self.has_right_wall),
        ]

        # Pass 1: draw removed walls (erase)
        for wall, exists in walls:
            if not exists:
                self._win.draw_line(wall, self._removed_color)

        # Pass 2: draw present walls (overwrite)
        for wall, exists in walls:
            if exists:
                self._win.draw_line(wall, self._wall_color)
            
    def draw_move(self, to_cell: 'Cell', undo: bool = False) -> None:
        """Draws a line between the center of this cell and another.

        Args:
            to_cell (Cell): The target cell
            undo (bool, optional): Whether this draw operation is an undo.
                Normal lines are colored red, but undo lines are colored gray.
                Defaults to False.
        """
        if self._win is None:
            return # 'Headless' mode for testing purposes.
        fill_color = "gray" if undo else "red"
        self._win.draw_line(Line(self._center, to_cell._center), fill_color)
        
    def has_wall(self, direction: str) -> bool:
        """Check for wall based on direction (as a string)"""
        match (direction):
            case "up":
                return self.has_top_wall
            case "down":
                return self.has_bottom_wall
            case "left":
                return self.has_left_wall
            case "right":
                return self.has_right_wall
            case _:
                raise ValueError(f"Unknown direction: {direction}")

    def break_wall(self, direction: str, inverse: bool = False) -> None:
        """Break the wall in the indicated direction. If 'inverse' is set,
        break the opposite wall.
        """
        if not inverse:
            match (direction):
                case "up":
                    self.has_top_wall = False
                case "down":
                    self.has_bottom_wall = False
                case "left":
                    self.has_left_wall = False
                case "right":
                    self.has_right_wall = False
                case _:
                    raise ValueError(f"Unknown direction: {direction}")
        else: # Opposite wall
            match (direction):
                case "up":
                    self.has_bottom_wall = False
                case "down":
                    self.has_top_wall = False
                case "left":
                    self.has_right_wall = False
                case "right":
                    self.has_left_wall = False
                case _:
                    raise ValueError(f"Unknown direction: {direction}")