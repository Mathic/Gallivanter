import pygame as pg

class Button(pg.sprite.Sprite):
    def __init__(self, game, img, x, y, action):
        self.groups = game.all_sprites, game.buttons
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = img
        self.image = pg.transform.scale(self.image, (150, 75))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.action = action

    def clicked(self, event):
        if self.rect.collidepoint(event.pos):
            self.kill()
            return True
