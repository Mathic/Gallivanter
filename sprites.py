from tools import *
from interactions import *

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        sprite_init(self, game, y, (game.all_sprites, game.me), None)
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
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE

        self.x_offset = 16
        self.y_offset = 36

        self.hitbox = self.image.get_rect()
        self.hitbox.center = self.pos

        self.rect = self.hitbox
        self.rect = self.rect.inflate(0, -36)
        self.rect.center = self.hitbox.center

        self.hitbox = self.hitbox.move(self.x_offset, self.y_offset)

        self.animation_frames = 6
        self.current_frame = 0
        self.current_dir = self.front
        self.dir_angle = 0
        self.first_time = 0 # increments by 1 when keys are being pressed
        self.last_action = pg.time.get_ticks()
        self.facing = 'front'
        self.health = 100
        self.width = self.rect.size[0]
        self.height = self.rect.size[1]
        self.melee = None

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
        self.animation_frames = 6
        now = pg.time.get_ticks()
        if now - self.last_action > SWING_RATE and self.game.paused == False:
            if keys[pg.K_LEFT] or keys[pg.K_a]:
                self.animate(False, self.left)
                self.vel.x = -PLAYER_SPEED
                self.current_dir = self.left
                self.facing = 'left'
                self.dir_angle = -90
                self.melee = MeleeHitBox(self, self.pos.x, self.pos.y, -self.image.get_width()*2)
            if keys[pg.K_RIGHT] or keys[pg.K_d]:
                self.animate(False, self.right)
                self.vel.x = PLAYER_SPEED
                self.current_dir = self.right
                self.facing = 'right'
                self.dir_angle = -90
                self.melee = MeleeHitBox(self, self.pos.x, self.pos.y, self.image.get_width())
            if keys[pg.K_UP] or keys[pg.K_w]:
                self.animate(False, self.back)
                self.vel.y = -PLAYER_SPEED
                self.current_dir = self.back
                self.facing = 'back'
                self.dir_angle = 0
                self.melee = MeleeHitBox(self, self.pos.x, self.pos.y, 0, -self.image.get_height())
            if keys[pg.K_DOWN] or keys[pg.K_s]:
                self.animate(False, self.front)
                self.vel.y = PLAYER_SPEED
                self.current_dir = self.front
                self.facing = 'front'
                self.dir_angle = 180
                self.melee = MeleeHitBox(self, self.pos.x, self.pos.y, 0, self.image.get_height())
            if self.vel.x != 0 and self.vel.y != 0:
                self.vel /= sqrt(2)
            if keys[pg.K_e]:
                self.last_action = now
                dir = vec(1, 0).rotate(-self.dir_angle)
                width = self.image.get_size()[0]
                height = self.image.get_size()[1]

                mining = Attack(self.game, self.game.resources, self.melee)
                hunting = Attack(self.game, self.game.mobs, self.melee)

                target = mining.target_hit()
                if target != None:
                    if type(target).__name__ == 'Tree' and not target.chopped:
                        Axe(self.game, self.pos, dir, self.facing, width, height)
                        target.health -= 25

                target = hunting.target_hit()
                if target != None:
                    Sword(self.game, self.pos, dir, self.facing, width, height)
                    play_sound(PUNCH)
                    target.health -= 25
                    # print(target.pos)
                    # print(target.health_bar.bar)
                    target.health_bar.first_time = 0

                Pickup(self.game, self.game.items, self.melee)

            if not any(keys):
                if self.first_time > 0:
                    self.image = self.current_dir[2]
                    self.first_time = 0
                self.animation_frames = random.randint(5, 25)
                self.animate(True, None)
                self.current_frame += 1
            else:
                self.first_time += 1
                # if self.first_time == 1:
                #     print(self.pos)
                #     print(self.rect)
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

    def draw_hitbox(self):
        pg.draw.rect(self.game.screen, YELLOW, self.hitbox, 2)
        pg.draw.rect(self.game.screen, MADANG, self.rect, 2)

    def update(self):
        self.get_keys()
        self.pos += self.vel * self.game.dt

        self.rect.x = self.pos.x
        detect_collision(self, self.game.collides, 'x')
        self.rect.y = self.pos.y
        detect_collision(self, self.game.collides, 'y')

        self.hitbox.center = self.pos
        self.hitbox = self.hitbox.move(self.x_offset, self.y_offset)

        self.game.all_sprites.change_layer(self, self.rect.bottom)
