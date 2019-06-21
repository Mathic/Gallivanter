from helper import *
from inventory import *
from tools import *

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.me
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.front, self.back, self.left, self.right = ([] for i in range(4))
        self.idle_fr, self.idle_bk, self.idle_lf, self.idle_rt = ([] for i in range(4))
        self.walking_sprites(P_WALK_FR, self.front)
        self.walking_sprites(P_WALK_BK, self.back)
        self.walking_sprites(P_WALK_LF, self.left)
        self.walking_sprites(P_WALK_RT, self.right)
        self.idle_sprites(P_IDLE_FR, self.idle_fr)
        self.idle_sprites(P_IDLE_BK, self.idle_bk)
        self.idle_sprites(P_IDLE_LF, self.idle_lf)
        self.idle_sprites(P_IDLE_RT, self.idle_rt)
        self.index = 2
        self.image = self.front[self.index]
        self.rect = self.image.get_rect()
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.rect.center = self.pos
        self.animation_frames = 6
        self.current_frame = 0
        self.current_dir = self.front
        self.dir_angle = 0
        self.first_time = 0
        self.last_swing = pg.time.get_ticks()
        self.facing = 'front'

    def walking_sprites(self, name, dir=[]):
        sprite_sheet = SpriteSheet(name)
        image = sprite_sheet.get_image(0, 0, 8, 18)
        dir.append(image)
        image = sprite_sheet.get_image(8, 0, 8, 18)
        dir.append(image)
        image = sprite_sheet.get_image(16, 0, 8, 18)
        dir.append(image)
        image = sprite_sheet.get_image(24, 0, 8, 18)
        dir.append(image)
        image = sprite_sheet.get_image(32, 0, 8, 18)
        dir.append(image)
        image = sprite_sheet.get_image(40, 0, 8, 18)
        dir.append(image)

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
        # event = pg.event.poll()
        self.animation_frames = 6
        now = pg.time.get_ticks()
        if now - self.last_swing > SWING_RATE and self.game.paused == False:
            if keys[pg.K_LEFT] or keys[pg.K_a]:
                self.animate(False, self.left)
                self.vel.x = -PLAYER_SPEED
                self.current_dir = self.left
                self.facing = 'left'
                self.dir_angle = -90
            if keys[pg.K_RIGHT] or keys[pg.K_d]:
                self.animate(False, self.right)
                self.vel.x = PLAYER_SPEED
                self.current_dir = self.right
                self.facing = 'right'
                self.dir_angle = -90
            if keys[pg.K_UP] or keys[pg.K_w]:
                self.animate(False, self.back)
                self.vel.y = -PLAYER_SPEED
                self.current_dir = self.back
                self.facing = 'back'
                self.dir_angle = 0
            if keys[pg.K_DOWN] or keys[pg.K_s]:
                self.animate(False, self.front)
                self.vel.y = PLAYER_SPEED
                self.current_dir = self.front
                self.facing = 'front'
                self.dir_angle = 180
            if self.vel.x != 0 and self.vel.y != 0:
                self.vel /= sqrt(2)
            if keys[pg.K_SPACE]:
                self.last_swing = now
                dir = vec(1, 0).rotate(-self.dir_angle)
                width = self.image.get_size()[0]
                height = self.image.get_size()[1]

                # print(new_pos)
                # print(self.image.get_size()[1] / 2)
                Sword(self.game, self.pos, dir, self.facing, width, height)

            if not any(keys):
                if self.first_time > 0:
                    self.image = self.current_dir[2]
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

                self.index = np.random.choice(len(dir), 1, p=[0.5, 0.1, 0.2, 0.2])[0]
        elif self.current_frame >= self.animation_frames:
            self.current_frame = 0
            self.index = (self.index + 1) % len(dir)

        if dir is not None:
            if self.index >= len(dir):
                self.index = 0

            self.image = dir[self.index]

    def update(self):
        self.get_keys()
        self.pos += self.vel * self.game.dt
        self.rect.x = self.pos.x
        collide_with_walls(self, self.game.collides, 'x')
        self.rect.y = self.pos.y
        collide_with_walls(self, self.game.collides, 'y')
