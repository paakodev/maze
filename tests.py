import unittest
from maze import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )
    
    def test_cell_coordinates(self):
        num_cols = 2
        num_rows = 2
        cell_size = 10
        m = Maze(0, 0, num_rows, num_cols, cell_size, cell_size)
        
        top_left = m._cells[0][0]  # col 0, row 0
        self.assertEqual(top_left._x1, 0)
        self.assertEqual(top_left._y1, 0)
        self.assertEqual(top_left._x2, 10)
        self.assertEqual(top_left._y2, 10)
        
        bottom_right = m._cells[1][1]
        self.assertEqual(bottom_right._x1, 10)
        self.assertEqual(bottom_right._y1, 10)
        self.assertEqual(bottom_right._x2, 20)
        self.assertEqual(bottom_right._y2, 20)

    def test_default_cell_walls(self):
        m = Maze(0, 0, 1, 1, 10, 10)
        cell = m._cells[0][0]
        self.assertTrue(cell.has_top_wall)
        self.assertTrue(cell.has_bottom_wall)
        self.assertTrue(cell.has_left_wall)
        self.assertTrue(cell.has_right_wall)

    def test_cell_draw_headless(self):
        from cell import Cell
        c = Cell(0, 0, 10, 10, window=None)
        try:
            c.draw()  # Should do nothing and not raise
        except Exception as e:
            self.fail(f"draw() raised unexpectedly in headless mode: {e}")


if __name__ == "__main__":
    unittest.main()