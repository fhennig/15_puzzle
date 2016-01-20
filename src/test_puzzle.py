#!/usr/bin/env python3
import unittest
import puzzle as p
import solvers as s
import numpy as np



### test data ###

# solvable
ps1 = np.array([[ 3,  1, 14, 11],
                [ 9, 12,  5, 13],
                [ 4,  7,  0,  8],
                [ 2,  6, 10, 15]])

# not solvable
pn1 = np.array([[ 3,  1, 14, 11],
                [ 9, 12,  5, 13],
                [ 2,  7,  0,  8],
                [ 4,  6, 10, 15]])


### test class(es) ###

class TestPuzzle(unittest.TestCase):

    def test_manhattan_dist(self):
        self.assertEqual(p.manhattan_dist((0, 0), (1, 1)), 2)

    def test_rotate(self):
        self.assertEqual(p.rotate([0, 1, 2]), [1, 2, 0])
        self.assertEqual(p.rotate([0, 1, 2], n = 2), [2, 0, 1])

    def test_on_field(self):
        self.assertTrue(p.on_field((4, 4), (3, 3)))
        self.assertTrue(p.on_field((4, 4), (0, 0)))
        self.assertFalse(p.on_field((4, 4), (-1, 0)))
        self.assertFalse(p.on_field((4, 4), (4, 0)))
        self.assertTrue(p.on_field((4, 4, 2), (0, 0, 0)))
        self.assertFalse(p.on_field((4, 4, 2), (0, 0, 2)))

    def test_reverse_action(self):
        self.assertEqual(p.reverse_action((1, 0)), (-1, 0))
        self.assertEqual(p.reverse_action((-1, 1)), (1, -1))
        self.assertEqual(p.reverse_action((-1, 1, 0)), (1, -1, 0))

    def test_solvable(self):
        self.assertTrue(p.solvable(ps1))
        self.assertFalse(p.solvable(pn1))

    def equal_from_list_with_array(self, a):
        return all(p.from_list(list(a.flat), a.shape).flat == a.flat)

    def test_from_list(self):
        self.assertTrue(self.equal_from_list_with_array(ps1))
        self.assertTrue(self.equal_from_list_with_array(pn1))

# ps1 = np.array([[ 3,  1, 14, 11],
#                 [ 9, 12,  5, 13],
#                 [ 4,  7,  0,  8],
#                 [ 2,  6, 10, 15]])

solved = p.puzzle_from_shape((4, 4))

class TestSolvers(unittest.TestCase):

    def test_manhattan_dist_sum(self):
        self.assertEqual(s.manhattan_dist_sum(ps1, positions = [1, 3]), 3)
        self.assertEqual(s.manhattan_dist_sum(ps1, positions = [1, 2]), 5)

    def test_SubSelect(self):
        self.assertTrue(s.SubSelect().applicable(solved))
        self.assertTrue(all(s.SubSelect().apply(solved).flat == solved[1:, 1:].flat))

if __name__ == "__main__":
    unittest.main()
