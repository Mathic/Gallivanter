from helper import *

class Inventory():
    def __init__(self, game, pos):
        self.contents = {}

    def add(name):
        if name in self.contents:
            self.contents[name] += 1
            print(self.contents)
        else:
            self.contents[name] = 1
            print(self.contents)

    def remove(name):
        if name in self.contents:
            self.contents[name] -= 1
            print(self.contents)

class InventoryGUI(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        sprite_sheet = SpriteSheet(BACKPACK_IMG)
        self.image = sprite_sheet.get_image(0, 0, 113, 17)
        self.rect = self.image.get_rect()
        self.pos = vec(pos) # * TILESIZE
        self.rect.center = self.pos

class Hotbar(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        sprite_sheet = SpriteSheet(HOTBAR_IMG)
        self.image = sprite_sheet.get_image(0, 0, 113, 17)
        self.rect = self.image.get_rect()
        self.pos = vec(pos) # * TILESIZE
        self.pos.y += HOTBAR_OFFSET
        print(self.pos)
        self.rect.center = self.pos

    def update(self):
        self.pos.x = self.game.player.pos.x
        self.pos.y = self.game.player.pos.y + HOTBAR_OFFSET
        self.rect.center = self.pos

class Item(pg.sprite.Sprite):
    def __init__(self, game, pos, name, offset):
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.item_name = name
        sprite_sheet = SpriteSheet(ITEM_IMG)
        self.image = sprite_sheet.get_image(offset, 0, 9, 9)
        self.rect = self.image.get_rect()
        self.pos = vec(pos) # * TILESIZE
        self.rect.center = self.pos

    def spawn_point():
        pass

class Meat(Item):
    def __init__(self, game, pos):
        super().__init__(game, pos, 'meat', 0)

class Pelt(Item):
    def __init__(self, game, pos):
        super().__init__(game, pos, 'pelt', 9)

class Log(Item):
    def __init__(self, game, pos):
        super().__init__(game, pos, 'log', 18)

class Rock(Item):
    def __init__(self, game, pos):
        super().__init__(game, pos, 'rock', 27)
