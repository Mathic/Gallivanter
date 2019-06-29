from helper import *

class Button(pg.sprite.Sprite):
    def __init__(self, game, img, x, y, width, height, action, sound=HOVER_SOUND, remove=True, hover=True):
        sprite_init(self, game, GUI_LAYER, (game.all_sprites, game.buttons), None)
        self.image = img
        self.image = pg.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.action = action
        self.remove = remove
        self.last_click = pg.time.get_ticks()
        self.hover = hover
        self.sound = sound

        if self.hover:
            s = pg.Surface((width, height))
            s.fill(CANDYCORN)
            self.game.screen.blit(s, (x, y))

    def handle_events(self, event):
        if not hasattr(event, 'pos'):
            return
        if self.action == None:
            return

        if self.rect.collidepoint(event.pos): # when hovered
            play_sound(HOVER_SOUND)
            if self.hover:
                width = self.game.hover.image.get_size()[0]
                height = self.game.hover.image.get_size()[1]
                x = self.game.hover.rect.x
                y = self.game.hover.rect.y

                s = pg.Surface((width, height))
                s.fill(CANDYCORN)
                self.game.screen.blit(s, (x, y))

                self.game.hover.rect = self.rect
                self.game.buttons.draw(self.game.screen)

            if event.type == pg.MOUSEBUTTONDOWN: # when clicked
                if event.button == LEFT_CLICK and self.action is not None:
                    if self.sound != HOVER_SOUND:
                        play_sound(self.sound)
                    self.action()

    def change_image(self, image, x, y, width, height):
        self.image = image # pg.image.load(path.join(img_folder, MUTE_BTN)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image = pg.transform.scale(self.image, (width, height))

    # def update(self):
    #     self.image = pg.transform.scale(self.image, (width, height))
    #     self.rect = self.image.get_rect()
