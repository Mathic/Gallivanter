from items import *

class Tree(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        sprite_init(self, game, FG_LAYER, (game.all_sprites, game.resources, game.collides, game.obstacles), None)
        self.idle, self.interact, self.stump = ([] for i in range(3))
        self.chopped = False
        self.dropped = False
        self.load_sprites()
        self.index = 0
        self.image = self.idle[self.index]
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * TILESIZE
        self.rect.center = self.pos
        self.animation_frames = 25
        self.current_frame = 0
        self.current_dir = self.idle
        self.health = 100
        self.last_chopped = pg.time.get_ticks()

    def load_sprites(self):
        sprite_sheet = SpriteSheet(TREE_IMG)
        image = sprite_sheet.get_image(0, 0, 18, 29)
        self.idle.append(image)
        image = sprite_sheet.get_image(18, 0, 18, 29)
        self.idle.append(image)

        image = sprite_sheet.get_image(0, 29, 18, 29)
        self.interact.append(image)
        image = sprite_sheet.get_image(18, 29, 18, 29)
        self.interact.append(image)

        image = sprite_sheet.get_image(20, 77, 11, 10)
        self.stump.append(image)

    def animate(self, idle, dir=[]):
        self.current_frame += 1
        self.animation_frames = random.randint(250, 750)
        if self.current_frame >= self.animation_frames:
            self.current_frame = 0
            self.index = (self.index + 1) % len(dir)

        if dir is not None:
            if self.index >= len(dir):
                self.index = 0

            self.image = dir[self.index]

    def update(self):
        if self.chopped:
            now = pg.time.get_ticks()
            if now - self.last_chopped > TREE_GROW_TIME:
                self.chopped = False
                self.dropped = False
                self.health = 100
                self.image = self.idle[self.index]
                self.rect = self.image.get_rect()
                self.pos.y -= 38
                self.pos.x += 6
                self.rect.center = self.pos
            else:
                self.image = self.stump[0]
                self.rect = self.image.get_rect()
                self.rect.center = self.pos
        else:
            self.animate(True, self.idle)

        if self.health <= 0 and not self.dropped:
            ILog(self.game, self.pos + vec(50, 50))
            self.chopped = True
            self.dropped = True
            self.pos.y += 38
            self.pos.x -= 6
            self.image = self.stump[0]
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.last_chopped = pg.time.get_ticks()

class Grass(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        sprite_init(self, game, BG_LAYER, (game.all_sprites), None)
        self.images = []
        self.load_sprites()
        self.index = random.randint(0, len(self.images) - 1)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * TILESIZE
        self.rect.center = self.pos

    def load_sprites(self):
        sprite_sheet = SpriteSheet(GRASS_IMG)
        image = sprite_sheet.get_image(0, 0, 5, 4)
        self.images.append(image)
        image = sprite_sheet.get_image(5, 0, 5, 4)
        self.images.append(image)
        image = sprite_sheet.get_image(10, 0, 5, 4)
        self.images.append(image)
        image = sprite_sheet.get_image(15, 0, 5, 4)
        self.images.append(image)
        image = sprite_sheet.get_image(20, 0, 5, 4)
        self.images.append(image)
        image = sprite_sheet.get_image(25, 0, 5, 4)
        self.images.append(image)
        image = sprite_sheet.get_image(30, 0, 5, 4)
        self.images.append(image)
        image = sprite_sheet.get_image(35, 0, 5, 4)
        self.images.append(image)

class Boundary(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        sprite_init(self, game, FG_LAYER, (game.all_sprites, game.walls, game.collides, game.obstacles), None)
        self.image = game.boundary_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
