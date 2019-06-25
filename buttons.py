from helper import *

class Button(pg.sprite.Sprite):
    def __init__(self, game, img, x, y, width, height, action):
        sprite_init(self, game, GUI_LAYER, (game.all_sprites, game.buttons), None)
        self.image = img
        self.image = pg.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.action = action

    def clicked(self, event):
        if self.rect.collidepoint(event.pos):
            self.kill()
            return True
