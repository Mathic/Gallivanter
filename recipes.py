from buttons import *
from items import *

class Recipe():
    def __init__(self, game, img_name, x, y):
        self.game = game
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'resources')
        img = pg.image.load(path.join(img_folder, img_name)).convert_alpha()
        img = pg.transform.scale(img, (64, 64))
        Button(self.game, img, x, y, 64, 64, self.action)

    def action(self):
        for item in self.remove:
            for i in range(self.remove[item]):
                index = self.game.inventory.remove(item)
                self.game.hotbar.remove_from_hotbar(index, item)

        self.game.close_inventory()

class RSword(Recipe):
    def __init__(self, game, img_name, x, y):
        super().__init__(game, img_name, x, y)
        self.remove = {'rock': 2, 'log': 1}

    def action(self):
        super().action()
        ISword(self.game, (self.game.player.pos.x - 32, self.game.player.pos.y + 64))

class RPickaxe(Recipe):
    def __init__(self, game, img_name, x, y):
        super().__init__(game, img_name, x, y)
        self.remove = {'rock': 1, 'log': 1}

    def action(self):
        super().action()
        IPickaxe(self.game, (self.game.player.pos.x - 32, self.game.player.pos.y + 64))

class RAxe(Recipe):
    def __init__(self, game, img_name, x, y):
        super().__init__(game, img_name, x, y)
        self.remove = {'rock': 2, 'log': 2}

    def action(self):
        super().action()
        IAxe(self.game, (self.game.player.pos.x - 32, self.game.player.pos.y + 64))

class RSteak(Recipe):
    def __init__(self, game, img_name, x, y):
        super().__init__(game, img_name, x, y)
        self.remove = {'meat': 1}

    def action(self):
        super().action()
        ISteak(self.game, (self.game.player.pos.x - 32, self.game.player.pos.y + 64))
