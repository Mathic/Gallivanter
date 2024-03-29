from helper import *

# Unlike items, tools have collision and are equipped by the player
class Tool(pg.sprite.Sprite):
    def __init__(self, game, pos, dir, facing, width, height, offset):
        sprite_init(self, game, ITEM_LAYER, (game.all_sprites, game.tools), TOOL_IMG)
        self.image = self.sprite_sheet.get_image(offset, 0, 9, 9)

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

        self.count = 0
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.hitbox = self.rect
        self.hitbox.center = self.rect.center
        self.vel = dir * TOOL_SPEED
        self.swing_speed = 250
        self.angle = 0
        self.spawn_time = pg.time.get_ticks()

    def animate(self):
        pass

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        self.hitbox.center = self.rect.center
        if pg.time.get_ticks() - self.spawn_time > TOOL_LIFETIME:
            self.kill()

class Pickaxe(Tool):
    def __init__(self, game, pos, dir, facing, width, height):
        super().__init__(game, pos, dir, facing, width, height, 0)

class Hatchet(Tool):
    def __init__(self, game, pos, dir, facing, width, height):
        super().__init__(game, pos, dir, facing, width, height, 9)

class Axe(Tool):
    def __init__(self, game, pos, dir, facing, width, height):
        super().__init__(game, pos, dir, facing, width, height, 18)

class Bow(Tool):
    def __init__(self, game, pos, dir, facing, width, height):
        super().__init__(game, pos, dir, facing, width, height, 27)

class Hammer(Tool):
    def __init__(self, game, pos, dir, facing, width, height):
        super().__init__(game, pos, dir, facing, width, height, 36)

class Sword(Tool):
    def __init__(self, game, pos, dir, facing, width, height):
        super().__init__(game, pos, dir, facing, width, height, 45)

class Broadsword(Tool):
    def __init__(self, game, pos, dir, facing, width, height):
        super().__init__(game, pos, dir, facing, width, height, 54)

class Rod(Tool):
    def __init__(self, game, pos, dir, facing, width, height):
        super().__init__(game, pos, dir, facing, width, height, 63)

class Knife(Tool):
    def __init__(self, game, pos, dir, facing, width, height):
        super().__init__(game, pos, dir, facing, width, height, 72)
