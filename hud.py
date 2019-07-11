from helper import *

class HUD():
    def __init__(self, game, x, y, numerator, denominator, width=250, height=30):
        self.game = game
        self.bar = pg.Rect(60, 30, width, height)

    def draw_hud(self, game, x, y, numerator, denominator, text, width=250, height=30):
        new_width = numerator / denominator * width
        hp = str(numerator) + ' / ' + str(denominator)

        self.bar = pg.Rect(x, y, new_width, height)
        pg.draw.rect(game.screen, GREEN, self.bar)

        full = pg.Rect(x, y, width, height)
        pg.draw.rect(game.screen, BLACK, full, 2)

        smallText = pg.font.SysFont("pixelated", 20)
        inv_text, inv_rect = text_objects(text + ":", smallText)
        inv_rect.center = vec(x, y) - vec(30, -15)
        self.game.screen.blit(inv_text, inv_rect)

        smallText = pg.font.SysFont("pixelated", 20)
        inv_text, inv_rect = text_objects(hp, smallText)
        inv_rect.center = vec(x, y) + vec(125, 15)
        self.game.screen.blit(inv_text, inv_rect)

class MeleeHitBox():
    def __init__(self, game, x, y, width=0, height=0):
        self.game = game
        self.hitbox = pg.Rect(x + width, y + height, 64, 64)

    def draw_hitbox(self, game, color):
        pg.draw.rect(game.screen, color, self.hitbox, 2)

class HealthBar():
    def __init__(self, game, x, y, width=50):
        self.game = game
        self.bar = pg.Rect(x, y, width, 10)
        self.first_time = 0

    def draw_health(self, game, x, y, width=50):
        self.bar = pg.Rect(x, y, width, 10)
        self.bar = self.bar.move(self.game.camera.camera.topleft)
        pg.draw.rect(game.screen, GREEN, self.bar)
        full = pg.Rect(x, y, 50, 10)
        full = full.move(self.game.camera.camera.topleft)
        pg.draw.rect(game.screen, BLACK, full, 2)
