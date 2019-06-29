from buttons import *
# from helper import *
from items import *

class Recipe():
    def __init__(self, game, img_name, x, y):
        self.game = game
        img = load_image(img_name)
        img = pg.transform.scale(img, (64, 64))
        Button(self.game, img, x, y, 64, 64, self.action, hover=False)

    def action(self, sound, ingredients):
        self.game.crafting = True
        self.game.close_inventory()
        for item in ingredients:
            for i in range(ingredients[item]):
                index = self.game.inventory.remove(item)
                self.game.hotbar.remove_from_hotbar(index, item)

        effect = pg.mixer.Sound(path.join(music_folder, sound))
        channel = pg.mixer.Channel(0)
        channel.play(effect, -1, 2500)
        while channel.get_busy():
            pg.time.wait(10)

class RSword(Recipe):
    ingredients = {'rock': 2, 'log': 1}

    def __init__(self, game, x, y):
        super().__init__(game, SWORD_IMG, x, y)

    def action(self):
        super().action(CRAFTING, self.ingredients)
        ISword(self.game, (self.game.player.pos.x - 32, self.game.player.pos.y + 64))

class RPickaxe(Recipe):
    ingredients = {'rock': 1, 'log': 1}

    def __init__(self, game, x, y):
        super().__init__(game, PICK_IMG, x, y)

    def action(self):
        super().action(CRAFTING, self.ingredients)
        IPickaxe(self.game, (self.game.player.pos.x - 32, self.game.player.pos.y + 64))

class RAxe(Recipe):
    ingredients = {'rock': 2, 'log': 2}

    def __init__(self, game, x, y):
        super().__init__(game, AXE_IMG, x, y)

    def action(self):
        super().action(CRAFTING, self.ingredients)
        IAxe(self.game, (self.game.player.pos.x - 32, self.game.player.pos.y + 64))

class RSteak(Recipe):
    ingredients = {'meat': 1}
    proximity = 'Campfire'
    range = 128

    def __init__(self, game, x, y):
        super().__init__(game, STEAK_IMG, x, y)

    def action(self):
        super().action(COOKING, self.ingredients)
        ISteak(self.game, (self.game.player.pos.x - 32, self.game.player.pos.y + 64))
