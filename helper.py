import numpy as np
import pygame as pg
import random

from math import sqrt
from os import path

from settings import *

vec = pg.math.Vector2

def get_plural(word):
    if word != 'meat':
        word += 's'
    # elif word == 'cooked':
    #     word = 'steaks'
    else:
        plural = word
    return plural

def load_image(name):
    game_folder = path.dirname(__file__)
    img_folder = path.join(game_folder, 'resources')
    image = pg.image.load(path.join(img_folder, name)).convert_alpha()
    return image

def load_music(name):
    game_folder = path.dirname(__file__)
    music_folder = path.join(game_folder, 'resources')
    pg.mixer.music.load(path.join(music_folder, name))

def change_song(name):
    pg.mixer.music.pause()
    load_music(name)
    pg.mixer.music.play(-1)

def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False)
        # for hit in hits:
        #     print(type(hit).__name__)
        if hits:
            if sprite.vel.x > 0:
                sprite.pos.x = hits[0].rect.left - sprite.rect.width
            if sprite.vel.x < 0:
                sprite.pos.x = hits[0].rect.right
            sprite.vel.x = 0
            sprite.rect.x = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False)
        if hits:
            if sprite.vel.y > 0:
                sprite.pos.y = hits[0].rect.top - sprite.rect.height
            if sprite.vel.y < 0:
                sprite.pos.y = hits[0].rect.bottom
            sprite.vel.y = 0
            sprite.rect.y = sprite.pos.y

# not being used yet
def mob_collision(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False)
        print(hits)
        if hits:
            if sprite.acc.x > 0:
                sprite.pos.x = hits[0].rect.left - sprite.rect.width
            if sprite.acc.x < 0:
                sprite.pos.x = hits[0].rect.right
            sprite.acc.x = 0
            sprite.rect.x = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False)
        if hits:
            if sprite.acc.y > 0:
                sprite.pos.y = hits[0].rect.top - sprite.rect.height
            if sprite.acc.y < 0:
                sprite.pos.y = hits[0].rect.bottom
            sprite.acc.y = 0
            sprite.rect.y = sprite.pos.y

def sprite_init(self, game, layer, groups, img_name):
    self._layer = layer
    self.groups = groups
    pg.sprite.Sprite.__init__(self, groups)
    self.game = game
    if img_name != None:
        self.sprite_sheet = SpriteSheet(img_name)
    return self

class SpriteSheet(object):
    """ Class used to grab images out of a sprite sheet. """

    def __init__(self, file_name):
        """ Constructor. Pass in the file name of the sprite sheet. """

        # Load the sprite sheet.
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'resources')
        self.sprite_sheet = pg.image.load(path.join(img_folder, file_name)).convert_alpha()


    def get_image(self, x, y, width, height, scale=True, color=BLACK):
        """ Grab a single image out of a larger spritesheet
            Pass in the x, y location of the sprite
            and the width and height of the sprite. """

        # Create a new blank image
        image = pg.Surface([width, height]).convert()

        # Copy the sprite from the large sheet onto the smaller image
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        if scale:
            image = pg.transform.scale(image, (width*4, height*4))
        else:
            image = pg.transform.scale(image, (width*2, height*2))

        # Assuming black works as the transparent color
        image.set_colorkey(color)

        # Return the image
        return image
