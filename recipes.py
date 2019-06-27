from buttons import *
# from helper import *
from items import *

class Recipe():
    def __init__(self, game, img_name, x, y):
        self.game = game
        img = load_image(img_name)
        img = pg.transform.scale(img, (64, 64))
        Button(self.game, img, x, y, 64, 64, self.action)

    def action(self, sound):
        for item in self.remove:
            for i in range(self.remove[item]):
                index = self.game.inventory.remove(item)
                self.game.hotbar.remove_from_hotbar(index, item)

        effect = pg.mixer.Sound(path.join(music_folder, sound))
        channel = pg.mixer.Channel(0)
        channel.play(effect, -1, 2500)
        while channel.get_busy():
            pg.time.wait(10)

class RSword(Recipe):
    def __init__(self, game, img_name, x, y):
        super().__init__(game, img_name, x, y)
        self.remove = {'rock': 2, 'log': 1}

    def action(self):
        super().action(CRAFTING)
        ISword(self.game, (self.game.player.pos.x - 32, self.game.player.pos.y + 64))

class RPickaxe(Recipe):
    def __init__(self, game, img_name, x, y):
        super().__init__(game, img_name, x, y)
        self.remove = {'rock': 1, 'log': 1}

    def action(self):
        super().action(CRAFTING)
        IPickaxe(self.game, (self.game.player.pos.x - 32, self.game.player.pos.y + 64))

class RAxe(Recipe):
    def __init__(self, game, img_name, x, y):
        super().__init__(game, img_name, x, y)
        self.remove = {'rock': 2, 'log': 2}

    def action(self):
        super().action(CRAFTING)
        IAxe(self.game, (self.game.player.pos.x - 32, self.game.player.pos.y + 64))

class RSteak(Recipe):
    def __init__(self, game, img_name, x, y):
        super().__init__(game, img_name, x, y)
        self.remove = {'meat': 1}

    def action(self):
        super().action(COOKING)
        ISteak(self.game, (self.game.player.pos.x - 32, self.game.player.pos.y + 64))
