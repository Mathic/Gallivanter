from helper import *

class Tool(pg.sprite.Sprite):
    def __init__(self, game, pos, dir, facing, width, height, offset):
        self.groups = game.all_sprites, game.tools
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.count = 0
        self.groups = game.all_sprites, game.tools
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        sprite_sheet = SpriteSheet(TOOL_IMG)
        self.image = sprite_sheet.get_image(offset, 0, 9, 9)

        if facing == 'left':
            self.pos = vec(pos.x, pos.y + height / 2)
        if facing == 'right':
            self.pos = vec(pos.x + width, pos.y + height / 2)
        if facing == 'back':
            self.pos = vec(pos.x + width / 2, pos.y)
        if facing == 'front':
            self.pos = vec(pos.x + width / 2, pos.y + height)

        if facing == 'left' or facing == 'back':
            self.image = pg.transform.flip(self.image, True, False)
        if facing == 'front':
            self.image = pg.transform.flip(self.image, False, True)

        self.rect = self.image.get_rect()
        self.vel = dir * TOOL_SPEED
        # self.pos = vec(pos) # * TILESIZE
        self.rect.center = self.pos
        self.swing_speed = 250
        self.angle = 0
        self.spawn_time = pg.time.get_ticks()

    def animate(self):
        pass

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.time.get_ticks() - self.spawn_time > TOOL_LIFETIME:
            self.kill()

class Pickaxe(Tool):
    def __init__(self, game, pos, dir, facing, width, height):
        super().__init__(game, pos, dir, facing, width, height, 0)

    def update(self):
        super().update()

class Hatchet(Tool):
    def __init__(self, game, pos, dir, facing, width, height):
        super().__init__(game, pos, dir, facing, width, height, 9)

    def update(self):
        super().update()

class Axe(Tool):
    def __init__(self, game, pos, dir, facing, width, height):
        super().__init__(game, pos, dir, facing, width, height, 18)

    def update(self):
        super().update()

class Bow(Tool):
    def __init__(self, game, pos, dir, facing, width, height):
        super().__init__(game, pos, dir, facing, width, height, 27)

    def update(self):
        super().update()

class Hammer(Tool):
    def __init__(self, game, pos, dir, facing, width, height):
        super().__init__(game, pos, dir, facing, width, height, 36)

    def update(self):
        super().update()

class Sword(Tool):
    def __init__(self, game, pos, dir, facing, width, height):
        super().__init__(game, pos, dir, facing, width, height, 45)

    def update(self):
        super().update()

class Broadsword(Tool):
    def __init__(self, game, pos, dir, facing, width, height):
        super().__init__(game, pos, dir, facing, width, height, 54)

    def update(self):
        super().update()

class Rod(Tool):
    def __init__(self, game, pos, dir, facing, width, height):
        super().__init__(game, pos, dir, facing, width, height, 63)

    def update(self):
        super().update()

class Knife(Tool):
    def __init__(self, game, pos, dir, facing, width, height):
        super().__init__(game, pos, dir, facing, width, height, 72)

    def update(self):
        super().update()
