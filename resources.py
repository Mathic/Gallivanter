from helper import *
from inventory import *

class Tree(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.resources, game.collides, game.obstacles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.idle, self.interact, self.stump = ([] for i in range(3))
        self.chopped = False
        self.dropped = False
        self.load_sprites()
        self.index = 0
        self.image = self.idle[self.index]
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * TILESIZE
        self.rect.center = self.pos
        self.animation_frames = 25
        self.current_frame = 0
        self.current_dir = self.idle
        self.health = 100

    def load_sprites(self):
        sprite_sheet = SpriteSheet(TREE_IMG)
        image = sprite_sheet.get_image(0, 0, 18, 29)
        self.idle.append(image)
        image = sprite_sheet.get_image(18, 0, 18, 29)
        self.idle.append(image)

        image = sprite_sheet.get_image(0, 29, 18, 29)
        self.interact.append(image)
        image = sprite_sheet.get_image(18, 29, 18, 29)
        self.interact.append(image)

        image = sprite_sheet.get_image(20, 77, 11, 10)
        self.stump.append(image)

    def animate(self, idle, dir=[]):
        self.current_frame += 1
        self.animation_frames = random.randint(500, 1000)
        if self.current_frame >= self.animation_frames:
            self.current_frame = 0
            self.index = (self.index + 1) % len(dir)

        if dir is not None:
            if self.index >= len(dir):
                self.index = 0

            self.image = dir[self.index]

    def update(self):
        if self.chopped:
            self.image = self.stump[0]
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
        else:
            self.animate(True, self.idle)

        if self.health <= 0 and not self.dropped:
            print(self.dropped)
            Log(self.game, self.pos + vec(50, 50))
            self.chopped = True
            self.dropped = True
            self.pos.y += 38
            self.pos.x -= 6
            self.image = self.stump[0]
            self.rect = self.image.get_rect()
            self.rect.center = self.pos

class Grass(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.images = []
        self.load_sprites()
        self.index = random.randint(0, len(self.images) - 1)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * TILESIZE
        self.rect.center = self.pos

    def load_sprites(self):
        sprite_sheet = SpriteSheet(GRASS_IMG)
        image = sprite_sheet.get_image(0, 0, 5, 4)
        self.images.append(image)
        image = sprite_sheet.get_image(5, 0, 5, 4)
        self.images.append(image)
        image = sprite_sheet.get_image(10, 0, 5, 4)
        self.images.append(image)
        image = sprite_sheet.get_image(15, 0, 5, 4)
        self.images.append(image)
        image = sprite_sheet.get_image(20, 0, 5, 4)
        self.images.append(image)
        image = sprite_sheet.get_image(25, 0, 5, 4)
        self.images.append(image)
        image = sprite_sheet.get_image(30, 0, 5, 4)
        self.images.append(image)
        image = sprite_sheet.get_image(35, 0, 5, 4)
        self.images.append(image)

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls, game.collides, game.obstacles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
