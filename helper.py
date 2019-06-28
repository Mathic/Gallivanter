import heapq
import numpy as np
import pygame as pg
import random

from collections import deque
from math import sqrt, ceil
from os import path

from settings import *

vec = pg.math.Vector2
game_folder = path.dirname(__file__)
music_folder = path.join(game_folder, 'resources')
img_folder = path.join(game_folder, 'resources')

def vec2int(v):
    return (ceil(v.x), ceil(v.y))

# stuff for breadth first search
# self.connections = [vec(1,0), vec(-1,0), vec(0,1), vec(0,-1)]
# self.grid = self.game.grid
# self.path = {}

# self.arrows = {}
# arrow_img = pg.image.load(path.join(img_folder, 'arrow1_e.gif')).convert_alpha()
# arrow_img = pg.transform.scale(arrow_img, (64, 64))
# for dir in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
#     self.arrows[dir] = pg.transform.rotate(arrow_img, vec(dir).angle_to(vec(1, 0)))

class Grid():
    def __init__(self, game, width, height):
        self.game = game
        self.width = width
        self.height = height
        self.walls = []
        self.connections = [vec(1, 0), vec(-1, 0), vec(0, 1), vec(0, -1)]

    def in_bounds(self, node):
        return 0 <= node.x < self.width and 0 <= node.y < self.height

    def passable(self, node):
        return node not in self.walls

    def find_neighbors(self, node):
        # print('NODE: ', node)
        neighbors = [node + connection for connection in self.connections]
        neighbors = filter(self.in_bounds, neighbors)
        neighbors = filter(self.passable, neighbors)
        # print(list(neighbors))
        return neighbors

class WeightedGrid(Grid):
    def __init__(self, game, width, height):
        super().__init__(game, width, height)
        self.weights = {}

    def cost(self, from_node, to_node):
        if (vec(to_node) - vec(from_node)).length_squared() == 1:
            return self.weights.get(to_node, 0) + 10
        else:
            return self.weights.get(to_node, 0) + 14

    def draw(self):
        for wall in self.walls:
            rect = pg.Rect(wall * TILESIZE, (TILESIZE, TILESIZE))
            pg.draw.rect(screen, LIGHTGRAY, rect)
        for tile in self.weights:
            x, y = tile
            rect = pg.Rect(x * TILESIZE + 3, y * TILESIZE + 3, TILESIZE - 3, TILESIZE - 3)
            pg.draw.rect(screen, FOREST, rect)

class PriorityQueue:
    def __init__(self):
        self.nodes = []

    def put(self, node, cost):
        heapq.heappush(self.nodes, (cost, node))

    def get(self):
        return heapq.heappop(self.nodes)[1]

    def empty(self):
        return len(self.nodes) == 0

def heuristic(a, b):
    # return abs(a.x - b.x) ** 2 + abs(a.y - b.y) ** 2
    return (abs(a.x - b.x) + abs(a.y - b.y)) * 10

def a_star_search(graph, start, end):
    frontier = PriorityQueue()
    frontier.put(vec2int(start), 0)
    path = {}
    cost = {}
    path[vec2int(start)] = None
    cost[vec2int(start)] = 0

    while not frontier.empty():
        current = frontier.get()
        if current == end:
            break
        for next in graph.find_neighbors(vec(current)):
            next = vec2int(next)
            next_cost = cost[current] + graph.cost(current, next)
            if next not in cost or next_cost < cost[next]:
                cost[next] = next_cost
                priority = next_cost + heuristic(end, vec(next))
                frontier.put(next, priority)
                path[next] = vec(current) - vec(next)
    # print('NEW PATH')
    # print(path)
    return path, cost

def breadth_first_search(graph, start, end):
    frontier = deque()
    frontier.append(start)
    path = {}
    path[vec2int(start)] = None
    while len(frontier) > 0:
        current = frontier.popleft()
        if current == end:
            break
        for next in graph.find_neighbors(current):
            if vec2int(next) not in path:
                frontier.append(next)
                path[vec2int(next)] = current - next
    # print(frontier, graph, path)
    # print(list(path))
    return path

def random_vec(xmin, xmax, ymin, ymax):
    x = random.randint(xmin, xmax)
    y = random.randint(ymin, ymax)
    pos = vec(x, y)
    return pos

def random_goal(available):
    index = random.randint(0, len(available) - 1)
    return available[index]

def get_plural(word):
    if word != 'meat':
        word += 's'
    # elif word == 'cooked':
    #     word = 'steaks'
    else:
        plural = word
    return plural

def load_image(name):
    image = pg.image.load(path.join(img_folder, name)).convert_alpha()
    return image

def load_music(name):
    pg.mixer.music.load(path.join(music_folder, name))

def change_song(name):
    pg.mixer.music.pause()
    load_music(name)
    pg.mixer.music.play(-1)

def play_sound(name, channel=0, volume=1.0):
    effect = pg.mixer.Sound(path.join(music_folder, name))
    effect.set_volume(volume)
    channel = pg.mixer.Channel(channel)
    channel.play(effect)

# This callback function is passed as the `collided`argument
# to pygame.sprite.spritecollide or groupcollide.
def collided(sprite, other):
    """Check if the hitboxes of the two sprites collide."""
    # Check if the hitboxes collide (instead of the rects).
    if hasattr(sprite, 'hitbox') and hasattr(other, 'hitbox'):
        return sprite.hitbox.colliderect(other.hitbox)
    else:
        return

# broken now
def collide_with_walls(sprite, group, dir, x_offset=0, y_offset=0):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collided)
        # for hit in hits:
        #     print(type(hit).__name__)
        if hits:
            old_posx = sprite.pos.x
            if type(sprite).__name__ == 'Player' and sprite.vel.x != 0:
                print('Velocity x', sprite.vel.x)
                print('Old position x', sprite.pos.x)
                print(hits[0].hitbox.left, hits[0].hitbox.right, sprite.hitbox.width, sprite.rect.width)

            if sprite.vel.x > 0:
                sprite.pos.x = hits[0].hitbox.left - sprite.hitbox.width # + 10
            if sprite.vel.x < 0:
                sprite.pos.x = hits[0].hitbox.right # - x_offset
            sprite.vel.x = 0
            sprite.rect.x = sprite.pos.x
            sprite.hitbox.x = sprite.rect.x

            if type(sprite).__name__ == 'Player' and sprite.pos.x != old_posx:
                print('New position x', sprite.pos.x)
            # if hasattr(sprite, 'self.x_offset'):
            #     sprite.hitbox.x += sprite.x_offset
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collided)
        if hits:
            old_posy = sprite.pos.y
            if type(sprite).__name__ == 'Player' and sprite.vel.y != 0:
                # print('Velocity y', sprite.vel.y)
                print('Old position y', sprite.pos.y)
                print(hits[0].hitbox.top, hits[0].hitbox.bottom, sprite.hitbox.height, sprite.rect.height)

            if sprite.vel.y > 0:
                sprite.pos.y = hits[0].hitbox.top - sprite.hitbox.height # - y_offset*2
            if sprite.vel.y < 0:
                sprite.pos.y = hits[0].hitbox.bottom # + y_offset*2
            sprite.vel.y = 0
            sprite.rect.y = sprite.pos.y
            sprite.hitbox.y = sprite.rect.y

            if type(sprite).__name__ == 'Player' and sprite.pos.y != old_posy:
                print('New position y', sprite.pos.y)

def detect_collision(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False)
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
                sprite.pos.y = hits[0].rect.bottom # + sprite.rect.height
            sprite.vel.y = 0
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
