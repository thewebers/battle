import matplotlib.pyplot as plt
import unittest

from christmas.globe import Perlin


class PerlinTest(unittest.TestCase):
    """Visual, qualitative test of snowscape generation."""
    def test(self):
        grid = Perlin.generate(20, 20, 50)
        plt.imshow(grid, origin='upper')
        plt.show()

if __name__ == '__main__':
    unittest.main()