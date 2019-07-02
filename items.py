from helper import *

class Item(pg.sprite.Sprite):
    def __init__(self, game, pos, name, offset, width=9, height=9, resize=True, img=ITEM_IMG):
        sprite_init(self, game, GUI_LAYER, (game.all_sprites, game.items), img)
        self.image = self.sprite_sheet.get_image(offset, 0, width, height, resize)
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

class CraftableItem(Item):
    def __init__(self, game, pos, name, offset):
        super().__init__(game, pos, name, offset, 16, 16, False, CRAFTABLE_IMG)

class ISoup(CraftableItem):
    item_name = 'soup'

    def __init__(self, game, pos):
        super().__init__(game, pos, self.item_name, 0)

class IPoutine(CraftableItem):
    item_name = 'poutine'

    def __init__(self, game, pos):
        super().__init__(game, pos, self.item_name, 16)

class ISteak(CraftableItem):
    item_name = 'steak'

    def __init__(self, game, pos):
        super().__init__(game, pos, self.item_name, 32)

class ICheese(CraftableItem):
    item_name = 'cheese'

    def __init__(self, game, pos):
        super().__init__(game, pos, self.item_name, 48)

class IBPIe(CraftableItem):
    item_name = 'bpie'

    def __init__(self, game, pos):
        super().__init__(game, pos, self.item_name, 64)

class ISPie(CraftableItem):
    item_name = 'spie'

    def __init__(self, game, pos):
        super().__init__(game, pos, self.item_name, 80)

class IEgg(CraftableItem):
    item_name = 'egg'

    def __init__(self, game, pos):
        super().__init__(game, pos, self.item_name, 96)

class IPancake(CraftableItem):
    item_name = 'pancake'

    def __init__(self, game, pos):
        super().__init__(game, pos, self.item_name, 112)

class INanaimo(CraftableItem):
    item_name = 'nanaimo'

    def __init__(self, game, pos):
        super().__init__(game, pos, self.item_name, 128)

class IBeaverTail(CraftableItem):
    item_name = 'btail'

    def __init__(self, game, pos):
        super().__init__(game, pos, self.item_name, 160)





# class IMeat(Item):
# item_name = 'meat'

#     def __init__(self, game, pos):
#         super().__init__(game, pos, self.item_name, 0)

class IPelt(Item):
    item_name = 'pelt'

    def __init__(self, game, pos):
        super().__init__(game, pos, self.item_name, 9)

class ILog(Item):
    item_name = 'log'

    def __init__(self, game, pos):
        super().__init__(game, pos, self.item_name, 18)

class IRock(Item):
    item_name = 'rock'

    def __init__(self, game, pos):
        super().__init__(game, pos, self.item_name, 27)

# class ISteak(Item):
# item_name = 'steak'

#     def __init__(self, game, pos):
#         super().__init__(game, pos, self.item_name, 36)

class IPickaxe(Item):
    item_name = 'pickaxe'

    def __init__(self, game, pos):
        super().__init__(game, pos, self.item_name, 45)

class IAxe(Item):
    item_name = 'axe'

    def __init__(self, game, pos):
        super().__init__(game, pos, self.item_name, 54)

class ISword(Item):
    item_name = 'sword'

    def __init__(self, game, pos):
        super().__init__(game, pos, self.item_name, 63)
