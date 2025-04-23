from window import Window
from line import Line
from point import Point

def main() -> None:
    window = Window(800, 600)
    window.draw_line(
        line=Line(Point(10, 10), Point(20, 20)), fill_color="red"
    )
    window.draw_line(
        Line(Point(150, 250), Point(456, 765)), "red"
    )
    window.wait_for_close()

if __name__ == "__main__":
    main()