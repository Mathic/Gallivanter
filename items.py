from helper import *

class Item(pg.sprite.Sprite):
    def __init__(self, game, pos, name, offset):
        sprite_init(self, game, GUI_LAYER, (game.all_sprites, game.items), ITEM_IMG)
        self.image = self.sprite_sheet.get_image(offset, 0, 9, 9)
        self.pos = vec(pos) # * TILESIZE
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.hitbox = self.rect
        self.hitbox.center = self.rect.center
        self.item_name = name
        self.quantity = 0
        self.in_inventory = False

    def spawn_point():
        pass

    # def update(self):
    #     if self.quantity > 0:
    #         pass

class IMeat(Item):
    def __init__(self, game, pos):
        super().__init__(game, pos, 'meat', 0)

class IPelt(Item):
    def __init__(self, game, pos):
        super().__init__(game, pos, 'pelt', 9)

class ILog(Item):
    def __init__(self, game, pos):
        super().__init__(game, pos, 'log', 18)

class IRock(Item):
    def __init__(self, game, pos):
        super().__init__(game, pos, 'rock', 27)

class ISteak(Item):
    def __init__(self, game, pos):
        super().__init__(game, pos, 'steak', 36)

class IPickaxe(Item):
    def __init__(self, game, pos):
        super().__init__(game, pos, 'pickaxe', 45)

class IAxe(Item):
    def __init__(self, game, pos):
        super().__init__(game, pos, 'axe', 54)

class ISword(Item):
    def __init__(self, game, pos):
        super().__init__(game, pos, 'sword', 63)
