from items import *
from recipes import *

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
                else:
                    return False

        return has_ingredients

class ItemData():
    def __init__(self, game, name, x, y, width, height, img_name):
        self.x = 0
        self.y = 0
        self.game = game
        self.pos = vec(x, y)
        self.width = width
        self.height = height
        self.image = pg.image.load(path.join(img_folder, img_name)).convert_alpha()
        self.image = pg.transform.scale(self.image, (width*4, height*4))
        self.rect = None
        self.sound = HOVER_SOUND
        self.name = name
        self.selected = False

    def handle_events(self, event):
        # print(event)
        if self.rect == None:
            return

        mx, my = pg.mouse.get_pos()
        ox = self.rect.x - mx
        oy = self.rect.y - my

        if self.rect.collidepoint(pg.mouse.get_pos()): # when hovered
            self.redraw(HOVER_SLOT_IMG)

             # when clicked
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == LEFT_CLICK:
                    self.selected = True
                    mx, my = pg.mouse.get_pos()
                    ox = self.rect.x - mx
                    oy = self.rect.y - my
                    # if self.sound != HOVER_SOUND:
                    play_sound(self.sound)
                    # self.action()
        else:
            self.redraw(INV_SLOT_IMG)

        if event.type == pg.MOUSEBUTTONUP:
            self.selected = False
            mx, my = pg.mouse.get_pos()
            self.rect.x = mx + ox
            self.rect.y = my + oy
            self.game.screen.blit(self.image, self.rect)
            pg.display.flip()
        elif event.type == pg.MOUSEMOTION:
            if self.selected:
                # print(pg.mouse.get_pos())
                pass

    def redraw(self, img):
        if self.game.inventory.contains_item(self.name, 1):
            hover_img = pg.image.load(path.join(img_folder, img)).convert_alpha()
            hoverrect = hover_img.get_rect()
            hoverrect.center = self.rect.center
            self.game.screen.blit(hover_img, hoverrect)
            self.game.screen.blit(self.image, self.rect)
            smallText = pg.font.SysFont("pixelated", 20)
            inv_text, inv_rect = self.game.text_objects(str(self.game.inventory.contents[self.name]), smallText)
            inv_rect.center = self.rect.center + vec(20, 20)
            self.game.screen.blit(inv_text, inv_rect)

# Item library to draw on the inventory menu
class ItemLibrary():
    def __init__(self, game):
        self.images = {}
        self.game = game
        # FIRST ROW
        self.images['tomato'] = ItemData(game, 'tomato', 0, 0, 16, 16, 'tile000.png')
        self.images['potato'] = ItemData(game, 'potato', 16, 0, 16, 16, 'tile001.png')
        self.images['meat'] = ItemData(game, 'meat', 32, 0, 16, 16, 'tile002.png')
        self.images['milk'] = ItemData(game, 'milk', 48, 0, 16, 16, 'tile003.png')
        self.images['blueberry'] = ItemData(game, 'blueberry', 64, 0, 16, 16, 'tile004.png')
        self.images['strawberry'] = ItemData(game, 'strawberry', 80, 0, 16, 16, 'tile005.png')
        self.images['egg'] = ItemData(game, 'egg', 96, 0, 16, 16, 'tile006.png')
        self.images['flour'] = ItemData(game, 'flour', 112, 0, 16, 16, 'tile007.png')
        self.images['chocolate'] = ItemData(game, 'chocolate', 128, 0, 16, 16, 'tile008.png')
        self.images['gravy'] = ItemData(game, 'gravy', 144, 0, 16, 16, 'tile009.png')
        self.images['syrup'] = ItemData(game, 'syrup', 160, 0, 16, 16, 'tile010.png')
        self.images['pickaxe'] = ItemData(game, 'pickaxe', 176, 0, 16, 16, 'tile011.png')
        self.images['hatchet'] = ItemData(game, 'hatchet', 192, 0, 16, 16, 'tile012.png')
        self.images['bow'] = ItemData(game, 'bow', 208, 0, 16, 16, 'tile013.png')
        self.images['sword'] = ItemData(game, 'sword', 224, 0, 16, 16, 'tile014.png')
        self.images['knife'] = ItemData(game, 'knife', 240, 0, 16, 16, 'tile015.png')
        self.images['rock'] = ItemData(game, 'rock', 256, 0, 16, 16, 'tile016.png')
        # SECOND ROW
        self.images['soup'] = ItemData(game, 'soup', 0, 16, 16, 16, 'tile017.png')
        self.images['poutine'] = ItemData(game, 'poutine', 16, 16, 16, 16, 'tile018.png')
        self.images['steak'] = ItemData(game, 'steak', 32, 16, 16, 16, 'tile019.png')
        self.images['cheese'] = ItemData(game, 'cheese', 48, 16, 16, 16, 'tile020.png')
        self.images['bpie'] = ItemData(game, 'bpie', 64, 16, 16, 16, 'tile021.png')
        self.images['spie'] = ItemData(game, 'spie', 80, 16, 16, 16, 'tile022.png')
        self.images['egg_cooked'] = ItemData(game, 'egg_cooked', 96, 16, 16, 16, 'tile023.png')
        self.images['flapjack'] = ItemData(game, 'flapjack', 112, 16, 16, 16, 'tile024.png')
        self.images['nanaimo'] = ItemData(game, 'nanaimo', 128, 16, 16, 16, 'tile025.png')
        self.images['beaver_tail_1'] = ItemData(game, 'beaver_tail_1', 144, 16, 16, 16, 'tile026.png')
        self.images['beaver_tail_2'] = ItemData(game, 'beaver_tail_2', 160, 16, 16, 16, 'tile027.png')
        self.images['axe'] = ItemData(game, 'axe', 176, 16, 16, 16, 'tile028.png')
        self.images['hammer'] = ItemData(game, 'hammer', 192, 16, 16, 16, 'tile029.png')
        self.images['broadsword'] = ItemData(game, 'broadsword', 208, 16, 16, 16, 'tile030.png')
        self.images['rod'] = ItemData(game, 'rod', 224, 16, 16, 16, 'tile031.png')
        self.images['log'] = ItemData(game, 'log', 240, 16, 16, 16, 'tile032.png')
        self.images['pelt'] = ItemData(game, 'pelt', 256, 16, 16, 16, 'tile033.png')

    def draw_image(self, name, pos):
        image = self.images[name].image
        self.images[name].rect = image.get_rect()
        self.images[name].rect.center = pos
        self.game.screen.blit(image, self.images[name].rect)

class InventoryGUI():
    def __init__(self, game):
        s = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
        s.fill((128, 128, 128, 80))
        game.screen.blit(s, (0, 0))

        # Show Inventory contents
        slot_img = pg.image.load(path.join(img_folder, INV_SLOT_IMG)).convert_alpha()
        imgrect = slot_img.get_rect()
        hover_img = pg.image.load(path.join(img_folder, HOVER_SLOT_IMG)).convert_alpha()
        hoverrect = hover_img.get_rect()

        x_start = 192
        y_start = 385

        offset = 64
        for row in range(9):
            for col in range(4):
                imgrect.centerx = x_start + ((row + 1) * offset)
                imgrect.centery = y_start + ((col + 1) * offset)
                game.screen.blit(slot_img, imgrect)

        col = 0
        row = 0
        for content in game.inventory.contents:
            # print('contains: ', content)
            x = x_start + ((col + 1) * offset)
            y = y_start + ((row + 1) * offset)
            pos = vec(x, y)
            game.iLibrary.draw_image(content, pos)
            col += 1
            if col > 8:
                row = (row + 1) % 4
            col = col % 9
            # print(row, col)
            smallText = pg.font.SysFont("pixelated", 20)
            inv_text, inv_rect = game.text_objects(str(game.inventory.contents[content]), smallText)
            inv_rect.center = pos + vec(20, 20)
            game.screen.blit(inv_text, inv_rect)
        pg.display.flip()

        # Show craftable items
        x_pos = 200
        x_offset = 80
        smallText = pg.font.SysFont("segoeprint", 20)
        textSurf, textRect = game.text_objects("Craftable items:", smallText)
        textRect.center = (500, 90)
        game.screen.blit(textSurf, textRect)

        for recipe in Recipe.__subclasses__():
            craft_name = recipe.__name__
            workbench_in_range = False

            if hasattr(recipe, 'proximity'):
                for workbench in game.workbench:
                    if workbench.name == recipe.proximity:
                        if abs(game.player.pos.x - workbench.x * TILESIZE) <= recipe.range and abs(game.player.pos.y - workbench.y * TILESIZE) <= recipe.range:
                            workbench_in_range = True
                            break
            else:
                workbench_in_range = True

            if workbench_in_range and game.inventory.contains_items(recipe.ingredients):
                recipe(game, x_pos, 122)
                x_pos += x_offset

class Hotbar(pg.sprite.Sprite):
    def __init__(self, game, pos):
        sprite_init(self, game, GUI_LAYER, (game.all_sprites), HOTBAR_IMG)
        self.image = self.sprite_sheet.get_image(0, 0, 576, 64, False)
        self.image = pg.transform.scale(self.image, (576, 64))
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.pos.y += HOTBAR_OFFSET
        self.rect.center = self.pos
        self.selected = None

        self.displays = {}

    def add_to_hotbar(self, index, name):
        # if the index is > 8 (max 9 items in hotbar), do not display
        if index > 8:
            return

        if name in self.displays:
            self.displays[name].quantity += 1
        else:
            item_pos = vec(self.pos.x + ((index - 4) * 64), self.pos.y)

            for item in Item.__subclasses__():
                craft_name = item.__name__
                if craft_name == 'CraftableItem':
                    for i in CraftableItem.__subclasses__():
                        if i.item_name == name:
                            self.displays[name] = i(self.game, item_pos)
                elif craft_name == 'GatherableItem':
                    for i in GatherableItem.__subclasses__():
                        if i.item_name == name:
                            self.displays[name] = i(self.game, item_pos)
                elif item.item_name == name:
                    self.displays[name] = item(self.game, item_pos)

            self.displays[name].quantity = 1
            self.displays[name]

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
        # move hotbar with the player
        self.pos.x = self.game.player.pos.x
        self.pos.y = self.game.player.pos.y + HOTBAR_OFFSET

        max_y = HEIGHT*4 - self.image.get_size()[1] + HOTBAR_Y_OFFSET
        min_y = HEIGHT - self.image.get_size()[1] + HOTBAR_Y_OFFSET - 4
        max_x = WIDTH*4 - self.image.get_size()[0] - HOTBAR_X_OFFSET*2 + 4
        min_x = WIDTH - self.image.get_size()[0] - HOTBAR_X_OFFSET + 124

        # limit the hotbar position
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
            new_pos = vec(self.pos.x + ((index - 4) * 64), self.pos.y)
            self.displays[item].pos = new_pos
            self.displays[item].rect.center = self.displays[item].pos
