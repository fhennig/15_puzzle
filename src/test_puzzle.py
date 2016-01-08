#!/usr/bin/env python3
import unittest
import puzzle as p


class TestStuff(unittest.TestCase):

    def test_manhattan_dist(self):
        self.assertEqual(p.manhattan_dist((0, 0), (1, 1)), 2)

    def test_rotate(self):
        self.assertEqual(p.rotate([0, 1, 2]), [1, 2, 0])
        self.assertEqual(p.rotate([0, 1, 2], n = 2), [2, 0, 1])


if __name__ == "__main__":
    unittest.main()
