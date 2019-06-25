from os import path
import os
import pygame as pg
import random
from settings import *

game_folder = path.dirname(__file__)
music_folder = path.join(game_folder, 'resources')

class Attack():
    def __init__(self, game, target, weapon):
        targets = pg.sprite.groupcollide(target, weapon, False, False)
        now = pg.time.get_ticks()
        for target in targets:
            if now - game.last_hit > TOOL_LIFETIME:
                game.last_hit = now
                target.attacked = True
                target.health -= 25
                # print(type(target).__name__)
                if type(target).__name__ == 'Tree' and not target.chopped:
                    index = random.randint(0, len(WOOD_CHOP) - 1)
                    effect = pg.mixer.Sound(path.join(music_folder, WOOD_CHOP[index]))
                    effect.play()

class Pickup():
    def __init__(self, game, target):
        pickups = pg.sprite.spritecollide(game.player, target, False)
        for pickup in pickups:
            if not pickup.in_inventory:
                index = game.inventory.add(pickup.item_name)
                game.hotbar.add_to_hotbar(index, pickup.item_name)
                if pickup.item_name == 'rock': # temp rock spawn before cave level
                    game.rock_count -= 1
                    index = random.randint(0, len(ROCK_MINE) - 1)
                    effect = pg.mixer.Sound(path.join(music_folder, ROCK_MINE[index]))
                    effect.play()
                pickup.kill()
