import unittest
import pygame

from game import Bullet1, Bullet2, start_game, bullets2, bullets1

display = pygame.display.set_mode((1200, 752))


class GameTest(unittest.TestCase):

    def test_bullet(self):
        self.assertEqual(Bullet2(), 2)


if __name__ == "__main__":
    unittest.main()
