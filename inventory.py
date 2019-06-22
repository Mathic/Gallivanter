from helper import *

class Inventory():
    def __init__(self):
        self.contents = {}

    def add(self, name):
        if name in self.contents:
            self.contents[name] += 1
        else:
            self.contents[name] = 1

        return list(self.contents.keys()).index(name)

    def remove(self, name):
        if name in self.contents:
            self.contents[name] -= 1

class InventoryGUI(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        sprite_sheet = SpriteSheet(BACKPACK_IMG)
        self.image = sprite_sheet.get_image(0, 0, 113, 17)
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = self.pos
        print('initialized')

    def update(self):
        # print(pg.mouse.get_pos())
        pass
        # s = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
        # s.fill((255,255,255,128))
        # self.game.screen.blit(s, (0, 0))
        # pg.display.update()
        # self.game.clock.tick(15)

class Hotbar(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        sprite_sheet = SpriteSheet(HOTBAR_IMG)
        self.image = sprite_sheet.get_image(0, 0, 113, 17)
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.pos.y += HOTBAR_OFFSET
        self.rect.center = self.pos

        self.displays = {}

    def apply(self, entity):
        return entity.rect.move(self.image.topleft)

    def add_to_hotbar(self, index, name):
        # also check if the index is > 8 (max 9 items in hotbar), do not display
        if index > 8:
            pass

        if name in self.displays:
            self.displays[name].quantity += 1
        else:
            item_pos = vec(self.pos.x + ((index - 4) * 48), self.pos.y)

            if name == 'meat':
                self.displays[name] = Meat(self.game, item_pos)
            elif name == 'pelt':
                self.displays[name] = Pelt(self.game, item_pos)
            elif name == 'log':
                self.displays[name] = Log(self.game, item_pos)
            elif name == 'rock':
                self.displays[name] = Rock(self.game, item_pos)

            self.displays[name].quantity = 1

        self.displays[name].in_hotbar = True
        print('Displaying: %s, quantity %2d' %(name, self.displays[name].quantity))

    def update(self):
        # move with the player
        self.pos.x = self.game.player.pos.x
        self.pos.y = self.game.player.pos.y + HOTBAR_OFFSET

        max_y = HEIGHT*4 - self.image.get_size()[1] + HOTBAR_Y_OFFSET
        min_y = HEIGHT - self.image.get_size()[1] + HOTBAR_Y_OFFSET
        max_x = WIDTH*4 - self.image.get_size()[0] - HOTBAR_X_OFFSET*2 + 4
        min_x = WIDTH - self.image.get_size()[0] - HOTBAR_X_OFFSET

        # limit the hotbar
        if self.pos.y > max_y:
            self.pos.y = max_y
        elif self.pos.y < min_y:
            self.pos.y = min_y

        if self.pos.x > max_x:
            self.pos.x = max_x
        if self.pos.x < min_x:
            self.pos.x = min_x

        self.rect.center = self.pos

        for item in self.displays:
            index = list(self.displays.keys()).index(item)
            new_pos = vec(self.pos.x + ((index - 4) * 48), self.pos.y)
            self.displays[item].pos = new_pos
            self.displays[item].rect.center = self.displays[item].pos

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
        self.quantity = 0
        self.in_hotbar = False

    def spawn_point():
        pass

    # def update(self):
    #     if self.quantity > 0:
    #         pass

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
