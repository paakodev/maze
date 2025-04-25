
from time import sleep
from cell import Cell
from window import Window

class Maze:
    def __init__(
        self,
        x1: int,
        y1: int,
        num_rows: int,
        num_cols: int,
        cell_size_x: int,
        cell_size_y: int,
        win: Window = None,
        draw_delay: float = 0.05
    ) -> None:
        """ The maze class, handles creating the entire maze. Do not leave Window unset,
        the default is there to facilitate testing."""
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._draw_delay = draw_delay
        self._create_cells()
    
    def _create_cells(self) -> None:
        self._cells: list[list[Cell]] = []
        for i in range(self._num_cols):  # Columns first
            column: list[Cell] = []
            for j in range(self._num_rows):  # Then rows
                cell = Cell(self._x1 + i*self._cell_size_x,  # i for column (x)
                            self._y1 + j*self._cell_size_y,  # j for row (y)
                            self._x1 + (i+1)*self._cell_size_x,
                            self._y1 + (j+1)*self._cell_size_y,
                            self._win)
                column.append(cell)
            self._cells.append(column)
        
        # Draw cells after all are created
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(j, i)
    
    def _draw_cell(self, i: int, j: int) -> None:
        cell = self._cells[j][i]
        cell.draw()
        self._animate()
    
    def _animate(self) -> None:
        if self._win is None:
            return # 'Headless' mode for testing
        self._win.redraw()
        sleep(self._draw_delay)
        
    def _break_entrance_and_exit(self):
        entrance = self._cells[0][0]
        entrance.has_top_wall = False
        entrance.draw()
        exit = self._cells[self._num_cols - 1][self._num_rows - 1]
        exit.has_bottom_wall = False
        exit.draw()