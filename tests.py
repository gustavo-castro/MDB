import unittest
import pygame
import random

import characters
import utils

MAX_ITER = 100
all_keys = [pygame.locals.K_a, pygame.locals.K_w,
            pygame.locals.K_d, pygame.locals.K_s]


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
        player_list = pygame.sprite.Group()
        enemy_list = pygame.sprite.Group()
        self.character = characters.Character(
            name, imagedict, hp, screen, rendergroup, wall_list,
            player_list, enemy_list)


class TestRules(unittest.TestCase):
    def test_correct_spawn(self):
        for _ in range(MAX_ITER):
            new_character = TestCharacter().character
            self.assertTrue(self.check_inscreen(new_character))
            self.assertTrue(self.check_no_collisions(new_character))

    def test_correct_walking_after_spawn(self):
        for _ in range(MAX_ITER):
            new_character = TestCharacter().character
            self.assertTrue(self.check_inscreen(new_character))
            self.assertTrue(self.check_no_collisions(new_character))
            key_choices = [random.choice(all_keys) for _ in range(1000)]
            for key in key_choices:
                new_character.update_position(key)
                self.assertTrue(self.check_inscreen(new_character),
                                msg="Player collided in position" +
                                str(new_character.rect.x)+" " +
                                str(new_character.rect.y) + " with w, h:" +
                                str(new_character.rect.width) + " " +
                                str(new_character.rect.height))
                self.assertTrue(self.check_no_collisions(new_character),
                                msg="Player collided in position " +
                                str(new_character.rect.right)+" " +
                                str(new_character.rect.top) + " with w, h:" +
                                str(new_character.rect.width) + " " +
                                str(new_character.rect.height))

    """def test_each_gamemode(self):
        DISPLAYSURF = pygame.display.set_mode((640, 480))
        SCREEN = utils.Screen(640, 480, 5, 15, DISPLAYSURF)
        ImagesPlayer = utils.loadingimages(
            'Images/ss-mercenaries.png', 'player', 5)
        ImagesEnemy = utils.loadingimages(
            'Images/ss-mercenaries.png', 'enemy', 5)
        FPSCLOCK = pygame.time.Clock()
        start = time.time()
        while time.time() - start < 1:
            MDB.runcoop(
                SCREEN, ImagesPlayer, ImagesEnemy, DISPLAYSURF, FPSCLOCK, 15)
                """

    @staticmethod
    def check_inscreen(character):
        screen_without_walls = pygame.Rect(5, 5, 630, 470)
        return screen_without_walls.collidepoint(character.x, character.y)

    @staticmethod
    def check_no_collisions(character):
        return True if not character.check_wall_collision() else False


def main():
    unittest.main()


if __name__ == '__main__':
    main()
