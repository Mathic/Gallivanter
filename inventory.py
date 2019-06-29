from items import *

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
            index = list(self.contents.keys()).index(name)
            if self.contents[name] > 0:
                self.contents[name] -= 1
            if self.contents[name] == 0:
                del self.contents[name]
            return index

    def contains_item(self, name, amount):
        if amount > 0: # make sure amount required is positive
            if name in self.contents:
                if self.contents[name] >= amount:
                    return True
        return False

    def contains_items(self, dict):
        has_ingredients = False
        for item in dict:
            if dict[item] > 0: # make sure amount required is positive
                if item in self.contents:
                    if self.contents[item] >= dict[item]:
                        has_ingredients = True
                    else:
                        return False

        return has_ingredients

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
        sprite_init(self, game, GUI_LAYER, (game.all_sprites), HOTBAR_IMG)
        self.image = self.sprite_sheet.get_image(0, 0, 113, 17)
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.pos.y += HOTBAR_OFFSET
        self.rect.center = self.pos
        self.selected = None

        self.displays = {}

    # def apply(self, entity):
    #     return entity.rect.move(self.image.topleft)

    def add_to_hotbar(self, index, name):
        # if the index is > 8 (max 9 items in hotbar), do not display
        if index > 8:
            pass

        if name in self.displays:
            self.displays[name].quantity += 1
        else:
            item_pos = vec(self.pos.x + ((index - 4) * 48), self.pos.y)

            if name == 'meat':
                self.displays[name] = IMeat(self.game, item_pos)
            elif name == 'pelt':
                self.displays[name] = IPelt(self.game, item_pos)
            elif name == 'log':
                self.displays[name] = ILog(self.game, item_pos)
            elif name == 'rock':
                self.displays[name] = IRock(self.game, item_pos)
            elif name == 'steak':
                self.displays[name] = ISteak(self.game, item_pos)
            elif name == 'pickaxe':
                self.displays[name] = IPickaxe(self.game, item_pos)
            elif name == 'axe':
                self.displays[name] = IAxe(self.game, item_pos)
            elif name == 'sword':
                self.displays[name] = ISword(self.game, item_pos)

            self.displays[name].quantity = 1

        self.displays[name].in_inventory = True
        # print('Displaying: %s, quantity %2d' %(name, self.displays[name].quantity))

    def remove_from_hotbar(self, index, name):
        if index > 8:
            pass

        if name in self.displays:
            if self.displays[name].quantity > 0:
                self.displays[name].quantity -= 1
                # print('Displaying: %s, quantity %2d' %(name, self.displays[name].quantity))
            if self.displays[name].quantity == 0:
                self.displays[name].in_inventory = False
                self.displays[name].kill()
                del self.displays[name]

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

        # update the positions of items in the hotbar
        for item in self.displays:
            index = list(self.displays.keys()).index(item)
            new_pos = vec(self.pos.x + ((index - 4) * 48), self.pos.y)
            self.displays[item].pos = new_pos
            self.displays[item].rect.center = self.displays[item].pos
