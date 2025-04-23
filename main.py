from window import Window
from line import Line
from point import Point
from cell import Cell

def main() -> None:
    window = Window(800, 600)
    # window.draw_line(
    #     line=Line(Point(50, 50), Point(90, 90)), fill_color="red"
    # )
    # window.draw_line(
    #     Line(Point(150, 250), Point(456, 565)), "red"
    # )
    cell1 = Cell(10, 10, 40, 40, window, "black")
    cell1.has_left_wall = False
    cell1.draw()
    cell2 = Cell(130, 240, 400, 570, window, "red")
    cell2.has_bottom_wall = False
    cell2.draw()
    window.wait_for_close()

if __name__ == "__main__":
    main()