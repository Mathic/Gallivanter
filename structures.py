from helper import *

class Structure(pg.sprite.Sprite):
    def __init__(self, game, x , y, offset): # pos, dir, facing, width, height, offset):
        sprite_init(self, game, STRUCTURE_LAYER, (game.all_sprites, game.structures, game.obstacles), None)

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
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def update(self):
        pass

class Campfire(Structure):
    def __init__(self, game, x , y): # pos, dir, facing, width, height, offset):
        super().__init__(game, x, y, 96) # pos, dir, facing, width, height, 96)
        self.groups = game.collides
        pg.sprite.Sprite.__init__(self, self.groups)

class Floor(Structure):
    def __init__(self, game, x , y): # pos, dir, facing, width, height, offset):
        super().__init__(game, x, y, 32) # pos, dir, facing, width, height, 96)

class Wall(Structure):
    def __init__(self, game, x , y): # pos, dir, facing, width, height, offset):
        super().__init__(game, x, y, 64) # pos, dir, facing, width, height, 96)
        self.groups = game.collides
        pg.sprite.Sprite.__init__(self, self.groups)

class Door(Structure):
    def __init__(self, game, x , y): # pos, dir, facing, width, height, offset):
        super().__init__(game, x, y, 0) # pos, dir, facing, width, height, 96)
