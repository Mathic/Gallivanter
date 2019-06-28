from items import *

class Tree(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        sprite_init(self, game, y, (game.all_sprites, game.resources, game.obstacles), None)
        self.idle, self.interact, self.stump = ([] for i in range(3))
        self.chopped = False
        self.dropped = False
        self.load_sprites()
        self.index = 0
        self.image = self.idle[self.index]
        self.pos = vec(x, y) * TILESIZE

        self.x_offset = 0
        self.y_offset = 35

        self.hitbox = self.image.get_rect()
        self.hitbox.center = self.pos

        self.rect = self.hitbox
        self.rect = self.rect.inflate(0, -69)
        self.rect.center = self.hitbox.center

        self.hitbox = self.hitbox.move(self.x_offset, self.y_offset)

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

    def draw_hitbox(self):
        pg.draw.rect(self.game.screen, YELLOW, self.hitbox)
        pg.draw.rect(self.game.screen, MADANG, self.rect)

    def update(self):
        self.game.all_sprites.change_layer(self, self.rect.bottom)
        if self.chopped:
            now = pg.time.get_ticks()
            if now - self.last_chopped > TREE_GROW_TIME:
                self.chopped = False
                self.dropped = False
                self.health = 100
                self.image = self.idle[self.index]
                self.pos.y -= self.y_offset*2 + 6
                self.pos.x -= 8
                self.rect.center = self.pos
            else:
                self.image = self.stump[0]

        else:
            self.animate(True, self.idle)
            self.hitbox.center = self.pos
            self.rect.center = self.hitbox.center
            self.hitbox = self.hitbox.move(self.x_offset, self.y_offset)

        if self.health <= 0 and not self.dropped:
            ILog(self.game, self.pos + vec(50, 50))
            self.chopped = True
            self.dropped = True
            self.pos.y += self.y_offset*2 + 6
            self.pos.x += 8
            self.rect.center = self.pos
            self.image = self.stump[0]
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
        sprite_init(self, game, y, (game.all_sprites, game.walls, game.collides, game.obstacles), None)
        self.image = game.boundary_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.hitbox = self.rect
        self.hitbox.x = x * TILESIZE
        self.hitbox.y = y * TILESIZE

    def draw_hitbox(self):
        pg.draw.rect(self.game.screen, YELLOW, self.rect)
        pg.draw.rect(self.game.screen, MADANG, self.hitbox)

    def update(self):
        # self.game.all_sprites.change_layer(self, self.rect.bottom)
        pass
