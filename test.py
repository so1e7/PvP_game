import game

import unittest
from unittest.mock import patch
import pygame


class GameTests(unittest.TestCase):
    
    @patch('pygame.key.get_pressed')
    @patch('game.pause_game')
    def test_exit_game(self, patch_pause, patch_keys):
        """Проверяем, работает ли пауза."""
        patch_keys.return_value = {pygame.K_ESCAPE : True, pygame.K_RETURN : False}
        patch_pause.return_value = 'paused'
        try:
            game.run_game()
        except KeyError as e:
            pass
        self.assertTrue(patch_pause.called)

if __name__ == "__main__":
    unittest.main()
