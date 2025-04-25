from dataclasses import dataclass
from tkinter import Canvas
from point import Point

@dataclass(frozen=True)
class Line:
    point1: Point
    point2: Point
    width: int = 2
    
    def draw(self, canvas: Canvas, fill_color: str) -> None:
        canvas.create_line(self.point1.x, self.point1.y,
                           self.point2.x, self.point2.y,
                           fill=fill_color, width=self.width)