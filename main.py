from maze import Maze
from window import Window

def main() -> None:
    window = Window(800, 600)

    def generate(rows: int, cols: int) -> None:
        window.get_canvas().delete("all")
        maze = Maze(10, 10, rows, cols, 20, 20, window, draw_delay=window.get_delay())
        maze.generate()
        maze.solve()

    window.set_generate_callback(generate)
    # Uncomment for immediate generation
    #window._on_generate()
    window.wait_for_close()

if __name__ == "__main__":
    main()