
import random
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
        win: Window = None, # type: ignore
        draw_delay: float = 0.05,
        seed: int = None # type: ignore
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
        
        random.seed(a=seed)
        self._create_cells()

    # def __repr__(self) -> str:
    #     return (f"Maze(rows={self._num_rows}, cols={self._num_cols}, "
    #            f"cell_size_x={self._cell_size_x}, cell_size_y={self._cell_size_y})")
        
    # def __repr__(self) -> str:
    #     output = f"Maze(rows={self._num_rows}, cols={self._num_cols})\n"
    #     for row in range(self._num_rows):
    #         for col in range(self._num_cols):
    #             cell = self._cells[col][row]
    #             output += cell.__repr__()
    #         output += "\n"
    #     return output
    
    def generate(self) -> None:
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()
    
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
                
    def _get_cell(self, row: int, col: int) -> Cell:
        """We store our grid as [column][row]. Instead of breaking my brain every time
        I need to look up a cell, as coordinates are usually given as [row][column], 
        have a helper function.
        """
        return self._cells[col][row]
    
    def _in_bounds(self, row: int, col: int) -> bool:
        """Helper function to check if a given coordinate can exist in our maze"""
        return 0 <= row < self._num_rows and 0 <= col < self._num_cols
        
    def _get_neighbors(self, row: int, col: int) -> list[tuple[Cell, str, int, int]]:
        """Generates and returns a list of (Cell, direction, new_row, new_col) 
        tuples for the cell at the given coordinates.

        Args:
            row (int): Cell row coordinate.
            col (int): Cell column coordinate

        Returns:
            list[tuple[Cell, str, int, int]]: 
                A list of tuples with (Cell, direction, new_row, new_col).
        """
        neighbors: list[tuple[Cell, str, int, int]] = []
        directions = [
            (-1, 0, "up"),
            (1, 0, "down"),
            (0, -1, "left"),
            (0, 1, "right"),
        ]

        for d_row, d_col, direction in directions:
            new_row, new_col = row + d_row, col + d_col
            if self._in_bounds(new_row, new_col):
                neighbor = self._get_cell(new_row, new_col)
                neighbors.append((neighbor, direction, new_row, new_col))

        return neighbors
       
    def _draw_cell(self, row: int, col: int) -> None:
        cell = self._get_cell(row, col)
        cell.draw()
        self._animate()
    
    def _animate(self) -> None:
        if self._win is None:
            return # 'Headless' mode for testing
        self._win.redraw()
        sleep(self._draw_delay)
        
    def _break_entrance_and_exit(self):
        entrance = self._get_cell(0, 0)
        entrance.has_top_wall = False
        self._entrance_position = (0, 0)
        entrance.draw()
        exit = self._get_cell(self._num_rows - 1, self._num_cols - 1)
        exit.has_bottom_wall = False
        self._exit_position = (self._num_rows - 1, self._num_cols - 1)
        exit.draw()
    
    def _break_walls_r(self, i: int, j: int) -> None:
        """A recursive back-tracking maze generator.

        Args:
            i (int): Cell row coordinate
            j (int): Cell column coordinate
        """
        current = self._get_cell(i, j)
        current.visited = True
        
        while True:
            # Generate list of tuples of unvisited neighboring cells, refreshed
            # after recursion
            neighbors = [
                (cell, direction, n_row, n_col) 
                for cell, direction, n_row, n_col in self._get_neighbors(i,j) 
                if not cell.visited
            ]
                    
            # Dead end, so start heading home
            if not neighbors:
                current.draw()
                return

            target, direction, new_i, new_j = random.choice(neighbors)
            current.break_wall(direction)
            target.break_wall(direction, inverse=True)
            
            self._break_walls_r(new_i, new_j)
        
    def _reset_cells_visited(self) -> None:
        for col in self._cells:
            for cell in col:
                cell.visited = False

    def solve(self) -> bool:
        return self._solve_r(0, 0)
    
    def _solve_r(self, row: int, col: int) -> bool:
        if (row, col) == self._exit_position:
            return True
        self._animate()
        current = self._get_cell(row, col)
        current.visited = True
        neighbors = self._get_neighbors(row, col)
        for cell, direction, new_row, new_col in neighbors:
            if not current.has_wall(direction) and not cell.visited:
                current.draw_move(cell)
                result = self._solve_r(new_row, new_col)
                if result:
                    return True
                else:
                    current.draw_move(cell, undo=True)
        
        return False