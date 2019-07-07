from helper import *

class Item(pg.sprite.Sprite):
    def __init__(self, game, pos, name, offset, width=9, height=9, resize=True, img=ITEM_IMG):
        sprite_init(self, game, GUI_LAYER, (game.all_sprites, game.items), img)
        self.pos = pos
        self.offset = offset
        self.width = width
        self.height = height
        self.resize = resize

        self.image = self.sprite_sheet.get_image(self.offset, 0, self.width, self.height, self.resize)
        self.pos = vec(self.pos) # * TILESIZE
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.hitbox = self.rect
        self.hitbox.center = self.rect.center

        self.item_name = name
        self.quantity = 0
        self.in_inventory = False

class CraftableItem(Item):
    def __init__(self, game, pos, name, offset):
        super().__init__(game, pos, name, offset, 16, 16, False, CRAFTABLE_IMG)

class ISoup(CraftableItem):
    item_name = 'soup'
    description = 'Hot tomato soup to soothe the soul'

    def __init__(self, game, pos):
        super().__init__(game, pos, self.item_name, 0)

class IPoutine(CraftableItem):
    item_name = 'poutine'
    description = 'Fries, gravy and cheese curds.'

    def __init__(self, game, pos):
        super().__init__(game, pos, self.item_name, 16)

class ISteak(CraftableItem):
    item_name = 'steak'
    description = 'Deliciously grilled barbecue steak.'

    def __init__(self, game, pos):
        super().__init__(game, pos, self.item_name, 32)

class ICheese(CraftableItem):
    item_name = 'cheese'
    description = 'Cheese.'

    def __init__(self, game, pos):
        super().__init__(game, pos, self.item_name, 48)

class IBPIe(CraftableItem):
    item_name = 'bpie'
    description = 'Blueberry filling, flaky crust. What more could you want?'

    def __init__(self, game, pos):
        super().__init__(game, pos, self.item_name, 64)

class ISPie(CraftableItem):
    item_name = 'spie'
    description = 'Strawberry pie when you\'ve had enough blueberry pie.'

    def __init__(self, game, pos):
        super().__init__(game, pos, self.item_name, 80)

class IEggCooked(CraftableItem):
    item_name = 'egg_cooked'
    description = 'Egg cooked the way you like it.'

    def __init__(self, game, pos):
        super().__init__(game, pos, self.item_name, 96)

class IFlapjack(CraftableItem):
    item_name = 'flapjack'
    description = 'Fluffy flapjacks topped with Canadian maple syrup.'

    def __init__(self, game, pos):
        super().__init__(game, pos, self.item_name, 112)

class INanaimo(CraftableItem):
    item_name = 'nanaimo'
    description = 'A three-layered dessert: \"a wafer and coconut crumb-base, custard flavoured butter icing in the middle and a layer of chocolate ganache on top\"'

    def __init__(self, game, pos):
        super().__init__(game, pos, self.item_name, 128)

class IBeaverTail1(CraftableItem):
    item_name = 'beaver_tail_1'
    description = 'A crunchy pastry topped with cinnamon and sugar.'

    def __init__(self, game, pos):
        super().__init__(game, pos, self.item_name, 144)

class IBeaverTail2(CraftableItem):
    item_name = 'beaver_tail_2'
    description = 'Also a beaver tail but topped with peanut butter and nutella.'

    def __init__(self, game, pos):
        super().__init__(game, pos, self.item_name, 160)

class GatherableItem(Item):
    def __init__(self, game, pos, name, offset):
        super().__init__(game, pos, name, offset, 16, 16, False, GATHERABLE_IMG)

class ITomato(GatherableItem):
    item_name = 'tomato'
    description = 'A fruit that is eaten like avegetable.'

    def __init__(self, game, pos):
        super().__init__(game, pos, self.item_name, 0)

class IPotato(GatherableItem):
    item_name = 'potato'
    description = 'A starchy root that is versatile and can be cooked in many ways.'

    def __init__(self, game, pos):
        super().__init__(game, pos, self.item_name, 16)

class IMeat(GatherableItem):
    item_name = 'meat'
    description = 'Raw flesh of an animal.'

    def __init__(self, game, pos):
        super().__init__(game, pos, self.item_name, 32)

class IMilk(GatherableItem):
    item_name = 'milk'
    description = 'Baby food for animals.'

    def __init__(self, game, pos):
        super().__init__(game, pos, self.item_name, 48)

class IBlueberry(GatherableItem):
    item_name = 'blueberry'
    description = 'Sweet blueberries gathered from bushes.'

    def __init__(self, game, pos):
        super().__init__(game, pos, self.item_name, 64)

class IStrawberry(GatherableItem):
    item_name = 'strawberry'
    description = 'Sweet and sour strawberries.'

    def __init__(self, game, pos):
        super().__init__(game, pos, self.item_name, 80)

class IEgg(GatherableItem):
    item_name = 'egg'
    description = 'Egg gathered from chickens.'

    def __init__(self, game, pos):
        super().__init__(game, pos, self.item_name, 96)

class IFlour(GatherableItem):
    item_name = 'flour'
    description = 'Flour made from ground up grains.'

    def __init__(self, game, pos):
        super().__init__(game, pos, self.item_name, 112)

class IChocolate(GatherableItem):
    item_name = 'chocolate'
    description = 'Chocolate made from sweet cocoa, milk and sugar.'

    def __init__(self, game, pos):
        super().__init__(game, pos, self.item_name, 128)

class IGravy(GatherableItem):
    item_name = 'gravy'
    description = 'Gravy.'

    def __init__(self, game, pos):
        super().__init__(game, pos, self.item_name, 144)

class ISyrup(GatherableItem):
    item_name = 'syrup'
    description = 'Canadian maple syrup gathered from maple trees.'

    def __init__(self, game, pos):
        super().__init__(game, pos, self.item_name, 160)

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
