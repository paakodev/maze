import unittest
from cell import Cell
from maze import Maze

class Tests(unittest.TestCase):
    # ----------------------------
    # Tests for Maze
    # ----------------------------
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
            
    def test_maze_grid_indexing(self):
        m = Maze(0, 0, 3, 4, 10, 10)  # 3 rows, 4 columns
        # Top-left corner cell
        tl = m._cells[0][0]
        self.assertEqual(tl._x1, 0)
        self.assertEqual(tl._y1, 0)
        # Bottom-right corner cell
        br = m._cells[4 - 1][3 - 1]
        self.assertEqual(br._x1, 30)
        self.assertEqual(br._y1, 20)

    def test_maze_cell_spacing(self):
        m = Maze(0, 0, 2, 2, 15, 20)
        cell00 = m._cells[0][0]
        cell01 = m._cells[0][1]
        self.assertEqual(cell01._y1 - cell00._y1, 20)
        cell10 = m._cells[1][0]
        self.assertEqual(cell10._x1 - cell00._x1, 15)

    def test_all_cells_are_cells(self):
        m = Maze(0, 0, 3, 3, 10, 10)
        for col in m._cells:
            for cell in col:
                self.assertIsInstance(cell, Cell)

    def test_maze_headless_mode(self):
        try:
            m = Maze(0, 0, 5, 5, 10, 10, win=None)
        except Exception as e:
            self.fail(f"Maze init failed in headless mode: {e}")

    def test_maze_draw_cell_headless(self):
        m = Maze(0, 0, 1, 1, 10, 10, win=None)
        try:
            m._draw_cell(0, 0)  # Should no-op
        except Exception as e:
            self.fail(f"_draw_cell failed in headless mode: {e}")
            
    def test_break_entrance(self):
        m = Maze(0, 0, 5, 5, 10, 10, win=None)
        m._break_entrance_and_exit()
        entrance = m._cells[0][0]
        self.assertFalse(entrance.has_top_wall)

    def test_break_exit(self):
        m = Maze(0, 0, 5, 5, 10, 10, win=None)
        m._break_entrance_and_exit()
        exit = m._cells[5 - 1][5 - 1]  # last column, last row
        self.assertFalse(exit.has_bottom_wall)

            
    # ----------------------------
    # Tests for Cell
    # ----------------------------

    def test_cell_geometry(self):
        c = Cell(10, 20, 30, 40)
        self.assertEqual(c._top_left.x, 10)
        self.assertEqual(c._top_left.y, 20)
        self.assertEqual(c._bottom_right.x, 30)
        self.assertEqual(c._bottom_right.y, 40)
        self.assertEqual(c._center.x, 20)
        self.assertEqual(c._center.y, 30)

    def test_default_wall_flags(self):
        c = Cell(0, 0, 10, 10)
        self.assertTrue(c.has_top_wall)
        self.assertTrue(c.has_bottom_wall)
        self.assertTrue(c.has_left_wall)
        self.assertTrue(c.has_right_wall)

    def test_custom_wall_flags(self):
        c = Cell(0, 0, 10, 10, has_top_wall=False, has_right_wall=False)
        self.assertFalse(c.has_top_wall)
        self.assertTrue(c.has_bottom_wall)
        self.assertTrue(c.has_left_wall)
        self.assertFalse(c.has_right_wall)

    def test_cell_draw_headless(self):
        c = Cell(0, 0, 10, 10)
        try:
            c.draw()  # Should not raise
        except Exception as e:
            self.fail(f"draw() failed in headless mode: {e}")

    def test_cell_draw_move_headless(self):
        c1 = Cell(0, 0, 10, 10)
        c2 = Cell(10, 0, 20, 10)
        try:
            c1.draw_move(c2)
        except Exception as e:
            self.fail(f"draw_move() failed in headless mode: {e}")


if __name__ == "__main__":
    unittest.main()