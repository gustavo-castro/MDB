import unittest
import pygame
import random

import characters
import utils

MAX_ITER = 100


class TestCharacter():
    def __init__(self):
        name = "any_name"
        DISPLAYSURF = pygame.display.set_mode((640, 480))
        screen = utils.Screen(640, 480, 5, 15, DISPLAYSURF)
        imagedict = utils.loadingimages(
            'Images/ss-mercenaries.png', 'player', 5)
        hp = 10
        rendergroup = pygame.sprite.RenderPlain()
        wall_list = utils.createwalls(screen, rendergroup)
        self.character = characters.Character(
            name, imagedict, hp, screen, rendergroup, wall_list)


class TestRules(unittest.TestCase):
    def test_correct_spawn(self):
        for _ in range(MAX_ITER):
            new_character = TestCharacter().character
            self.assertTrue(self.check_inscreen(new_character))
            self.assertTrue(self.check_no_collisions(new_character))

    def test_correct_corners(self):
        for _ in range(MAX_ITER):
            new_character = TestCharacter().character
            for pair in [[7, 6]]:
                [new_character.x, new_character.y] = pair
                self.assertTrue(self.check_inscreen(new_character))
                self.assertTrue(self.check_no_collisions(new_character))
                for i in range(10):
                    new_character.update_position(random.choice(
                        [pygame.locals.K_a, pygame.locals.K_w,
                         pygame.locals.K_d, pygame.locals.K_s]))
                    self.assertTrue(self.check_inscreen(new_character))
                    self.assertTrue(self.check_no_collisions(new_character))

    @staticmethod
    def check_inscreen(character):
        screen_without_walls = pygame.Rect(5, 5, 630, 470)
        return screen_without_walls.collidepoint(character.x, character.y)

    @staticmethod
    def check_no_collisions(character):
        return True if not character.check_wall_collision() + \
            character.check_character_collision() else False


def main():
    unittest.main()


if __name__ == '__main__':
    main()
