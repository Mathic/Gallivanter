from tools import *
from interactions import *
from hud import *

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        sprite_init(self, game, y, (game.all_sprites, game.me), None)
        self.front, self.back, self.left, self.right = ([] for i in range(4))
        self.idle_fr, self.idle_bk, self.idle_lf, self.idle_rt = ([] for i in range(4))
        self.walking_sprites(CHARACTER_SPRITES)
        self.index = 2
        self.image = self.front[self.index]
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE

        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.width = self.rect.size[0]
        self.height = self.rect.size[1]
        self.x_offset = self.width / 2
        self.y_offset = self.height / 4
        self.hitbox = self.rect.inflate(-24, -self.height/2)

        self.animation_frames = 6
        self.current_frame = 0
        self.current_dir = self.front
        self.dir_angle = 0
        self.first_time = 0 # increments by 1 when keys are being pressed
        self.last_action = pg.time.get_ticks()
        self.facing = 'front'

        self.starting_health = 100
        self.health = 100
        self.health_bar_width = 250
        self.health_bar = HUD(game, 60, 30, self.health, self.starting_health)

        self.starting_hunger = 100
        self.hunger = 100
        self.hunger_bar_width = 150
        self.hunger_bar = HUD(game, 60, 60, self.hunger, self.starting_hunger )

        self.melee = None

    def walking_sprites(self, name, dir=[]):
        sprite_sheet = SpriteSheet(name)

        image = sprite_sheet.get_image(0, 0, 32, 32, False)
        self.front.append(image)
        image = sprite_sheet.get_image(64, 0, 32, 32, False)
        self.front.append(image)
        image = sprite_sheet.get_image(32, 0, 32, 32, False)
        self.front.append(image)
        image = sprite_sheet.get_image(64, 0, 32, 32, False)
        self.front.append(image)
        image = sprite_sheet.get_image(64, 0, 32, 32, False)
        self.front.append(image)
        self.idle_fr.append(image)

        image = sprite_sheet.get_image(0, 32, 32, 32, False)
        self.left.append(image)
        self.right.append(pg.transform.flip(image, True, False))
        image = sprite_sheet.get_image(64, 32, 32, 32, False)
        self.left.append(image)
        self.right.append(pg.transform.flip(image, True, False))
        image = sprite_sheet.get_image(32, 32, 32, 32, False)
        self.left.append(image)
        self.right.append(pg.transform.flip(image, True, False))
        image = sprite_sheet.get_image(64, 32, 32, 32, False)
        self.left.append(image)
        self.idle_lf.append(image)
        self.right.append(pg.transform.flip(image, True, False))
        self.idle_rt.append(pg.transform.flip(image, True, False))

        image = sprite_sheet.get_image(0, 64, 32, 32, False)
        self.back.append(image)
        image = sprite_sheet.get_image(64, 64, 32, 32, False)
        self.back.append(image)
        image = sprite_sheet.get_image(32, 64, 32, 32, False)
        self.back.append(image)
        image = sprite_sheet.get_image(64, 64, 32, 32, False)
        self.back.append(image)
        self.idle_bk.append(image)

    def idle_sprites(self, name, dir=[]):
        sprite_sheet = SpriteSheet(name)
        image = sprite_sheet.get_image(0, 0, 8, 18)
        dir.append(image)
        image = sprite_sheet.get_image(8, 0, 8, 18)
        dir.append(image)
        image = sprite_sheet.get_image(16, 0, 8, 18)
        dir.append(image)
        image = sprite_sheet.get_image(24, 0, 8, 18)
        dir.append(image)

    def get_keys(self):
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        self.animation_frames = 6
        now = pg.time.get_ticks()
        if now - self.last_action > SWING_RATE and self.game.paused == False:
            if keys[pg.K_LEFT] or keys[pg.K_a]:
                self.animate(False, self.left)
                self.vel.x = -PLAYER_SPEED
                self.current_dir = self.left
                self.facing = 'left'
                self.dir_angle = -90
                self.melee = MeleeHitBox(self, self.pos.x, self.pos.y, -self.width/2)
            if keys[pg.K_RIGHT] or keys[pg.K_d]:
                self.animate(False, self.right)
                self.vel.x = PLAYER_SPEED
                self.current_dir = self.right
                self.facing = 'right'
                self.dir_angle = -90
                self.melee = MeleeHitBox(self, self.pos.x, self.pos.y, self.width/2)
            if keys[pg.K_UP] or keys[pg.K_w]:
                self.animate(False, self.back)
                self.vel.y = -PLAYER_SPEED
                self.current_dir = self.back
                self.facing = 'back'
                self.dir_angle = 0
                self.melee = MeleeHitBox(self, self.pos.x, self.pos.y, 0, -self.height/2)
            if keys[pg.K_DOWN] or keys[pg.K_s]:
                self.animate(False, self.front)
                self.vel.y = PLAYER_SPEED
                self.current_dir = self.front
                self.facing = 'front'
                self.dir_angle = 180
                self.melee = MeleeHitBox(self, self.pos.x, self.pos.y, 0, self.height/2)
            if self.vel.x != 0 and self.vel.y != 0:
                self.vel /= sqrt(2)
            if keys[pg.K_e]:
                Pickup(self.game, self.game.items, self.melee)

            if not any(keys):
                if self.first_time > 0:
                    self.image = self.current_dir[1]
                    self.first_time = 0
                self.animation_frames = random.randint(5, 25)
                self.animate(True, None)
                self.current_frame += 1
            else:
                self.first_time += 1
                self.current_frame += 1

    def animate(self, idle, dir=[]):
        if idle:
            if self.current_frame >= self.animation_frames*5:
                self.current_frame = 0

                if self.current_dir == self.front:
                    dir = self.idle_fr
                elif self.current_dir == self.back:
                    dir = self.idle_bk
                elif self.current_dir == self.left:
                    dir = self.idle_lf
                elif self.current_dir == self.right:
                    dir = self.idle_rt

                self.index = 0 # np.random.choice(len(dir), 1, p=[0.5, 0.1, 0.2, 0.2])[0]
        elif self.current_frame >= self.animation_frames:
            self.current_frame = 0
            self.index = (self.index + 1) % len(dir)

        if dir is not None:
            if self.index >= len(dir):
                self.index = 0

            self.image = dir[self.index]

    def draw_hitbox(self):
        pg.draw.rect(self.game.screen, YELLOW, self.hitbox, 2)
        pg.draw.rect(self.game.screen, MADANG, self.rect, 2)

    def update(self):
        self.get_keys()
        self.pos += self.vel * self.game.dt

        self.hitbox.x = self.pos.x
        self.rect.x = self.pos.x
        hitbox_collision(self, self.game.collides, 'x')
        self.hitbox.y = self.pos.y
        self.rect.y = self.pos.y
        hitbox_collision(self, self.game.collides, 'y')

        self.hitbox.center = self.pos
        self.hitbox = self.hitbox.move(self.x_offset, self.y_offset)

        self.game.all_sprites.change_layer(self, self.rect.bottom)
