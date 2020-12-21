import game

import unittest
from unittest.mock import patch
import pygame


class GameTests(unittest.TestCase):
   
    @patch('game.stop_game')
    def test_game_start(self, test_patch):
        """Проверяем работает ли остановка игры при health = 0"""
        test_patch.return_value = 'win_test' 
        game.health2 = 0
       self.assertEqual(game.run_game(), 'win_test')
      
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
