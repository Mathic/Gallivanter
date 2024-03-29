from helper import *

class Structure(pg.sprite.Sprite):
    def __init__(self, game, x , y, offset, name): # pos, dir, facing, width, height, offset):
        self.groups = game.all_sprites, game.structures, game.obstacles
        sprite_init(self, game, STRUCTURE_LAYER, self.groups, None)

        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'resources')
        self.sprite_sheet = pg.image.load(path.join(img_folder, STRUCTURE_IMG)).convert_alpha()
        self.image = pg.Surface([32, 32]).convert()
        self.image.blit(self.sprite_sheet, (0, 0), (offset, 0, 32, 32))
        self.image = pg.transform.scale(self.image, (64, 64))
        self.image.set_colorkey(BLACK)

        # if facing == 'left':
        #     self.pos = vec(pos.x, pos.y + height / 2)
        # if facing == 'right':
        #     self.pos = vec(pos.x + width, pos.y + height / 2)
        # if facing == 'back':
        #     self.pos = vec(pos.x + width / 2, pos.y)
        # if facing == 'front':
        #     self.pos = vec(pos.x + width / 2, pos.y + height)
        #
        # if facing == 'left' or facing == 'back':
        #     self.image = pg.transform.flip(self.image, True, False)
        # if facing == 'front':
        #     self.image = pg.transform.flip(self.image, False, True)

        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.pos = vec(x, y) * TILESIZE
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

        self.hitbox = self.rect
        self.hitbox.center = self.rect.center

        self.name = name

class Campfire(Structure):
    def __init__(self, game, x , y):
        super().__init__(game, x, y, 96, type(self).__name__)
        game.collides.add(self)
        game.workbench.add(self)
        print(self.name)

    def update(self):
        self.game.all_sprites.change_layer(self, self.rect.bottom)

class Floor(Structure):
    def __init__(self, game, x , y):
        super().__init__(game, x, y, 32, type(self).__name__)

class Wall(Structure):
    def __init__(self, game, x , y):
        super().__init__(game, x, y, 64, type(self).__name__)
        game.collides.add(self)

    def update(self):
        self.game.all_sprites.change_layer(self, self.rect.bottom)

class Door(Structure):
    def __init__(self, game, x , y):
        super().__init__(game, x, y, 0, type(self).__name__)

    def update(self):
        self.game.all_sprites.change_layer(self, self.rect.bottom)
