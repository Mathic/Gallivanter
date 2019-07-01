from interactions import *
from items import *
from helper import *
# from tools import *

class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        sprite_init(self, game, CHARACTER_LAYER, (game.all_sprites, game.mobs, game.collides), None)

class Bite(pg.sprite.Sprite):
    def __init__(self, game, pos, dir, facing, width, height):
        sprite_init(self, game, CHARACTER_LAYER, (game.all_sprites, game.melee), TOOL_IMG)
        self.image = self.sprite_sheet.get_image(9, 0, 9, 9, True)

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
        self.vel = dir * TOOL_SPEED
        self.rect.center = self.pos
        self.swing_speed = 250
        self.angle = 0
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.time.get_ticks() - self.spawn_time > TOOL_LIFETIME:
            self.kill()

class Wolf(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        sprite_init(self, game, y, (game.all_sprites, game.mobs, game.collides), None)
        self.front, self.back, self.left, self.right = ([] for i in range(4))
        self.width = 50
        self.height = 35

        self.load_sprites()
        self.index = random.randint(0, len(self.front) - 1)
        self.image = self.front[self.index]

        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        self.x_offset = 0
        self.y_offset = 0
        self.hitbox = self.rect.inflate(-24, -2) # (self.pos.x + 12, self.pos.y + 1, 29, 32)
        self.hitbox.center = self.rect.center

        self.action_frames = 100
        self.action_frame = 0
        self.actions = ['walk_lf', 'walk_rt', 'walk_fr', 'walk_bk', 'idle']
        self.action_index = 4
        self.action = self.actions[self.action_index]
        self.last_action = 0

        self.animation_frames = 6
        self.current_frame = 0
        self.current_dir = self.front
        self.health = random.randint(100, 150)
        self.starting_health = self.health
        self.health_bar = HealthBar(game, self.pos.x, self.pos.y, self.health / self.starting_health * 50)

        self.width = self.rect.size[0]
        self.height = self.rect.size[1]

        # Attacking variables
        self.attacked = False
        self.dir = vec(0, 0)
        self.last_bite = pg.time.get_ticks()
        self.melee = MeleeHitBox(self, self.pos.x, self.pos.y, 0, self.height)

        # print(self.pos, self.rect)

    def load_sprites(self):
        transparent = (255, 0, 0)

        sprite_sheet = SpriteSheet(APRIL_WOLF_IMG)
        image = sprite_sheet.get_image(0, 0, self.width, self.height, False, transparent)
        self.front.append(image)
        image = sprite_sheet.get_image(50, 0, self.width, self.height, False, transparent)
        self.front.append(image)
        image = sprite_sheet.get_image(100, 0, self.width, self.height, False, transparent)
        self.front.append(image)
        image = sprite_sheet.get_image(150, 0, self.width, self.height, False, transparent)
        self.front.append(image)

        image = sprite_sheet.get_image(0, 35, self.width, self.height, False, transparent)
        self.left.append(image)
        image = sprite_sheet.get_image(50, 35, self.width, self.height, False, transparent)
        self.left.append(image)
        image = sprite_sheet.get_image(100, 35, self.width, self.height, False, transparent)
        self.left.append(image)
        image = sprite_sheet.get_image(150, 35, self.width, self.height, False, transparent)
        self.left.append(image)

        image = sprite_sheet.get_image(0, 70, self.width, self.height, False, transparent)
        self.right.append(image)
        image = sprite_sheet.get_image(50, 70, self.width, self.height, False, transparent)
        self.right.append(image)
        image = sprite_sheet.get_image(100, 70, self.width, self.height, False, transparent)
        self.right.append(image)
        image = sprite_sheet.get_image(150, 70, self.width, self.height, False, transparent)
        self.right.append(image)

        image = sprite_sheet.get_image(0, 105, self.width, self.height, False, transparent)
        self.back.append(image)
        image = sprite_sheet.get_image(50, 105, self.width, self.height, False, transparent)
        self.back.append(image)
        image = sprite_sheet.get_image(100, 105, self.width, self.height, False, transparent)
        self.back.append(image)
        image = sprite_sheet.get_image(150, 105, self.width, self.height, False, transparent)
        self.back.append(image)

    def get_actions(self):
        self.width = self.rect.size[0]
        self.height = self.rect.size[1]
        now = pg.time.get_ticks()
        self.action_frame += 1
        if self.attacked:
            dx = self.rect.centerx - self.game.player.rect.centerx
            dy = self.rect.centery - self.game.player.rect.centery
            new_move_speed = MOB_SPEED*(3/2)

            if abs(dy) <= (self.height + self.game.player.height)/2:
                self.vel.y = 0
            else:
                self.vel.y = -new_move_speed if dy >= 0 else new_move_speed
                if self.vel.y < 0:
                    self.action = self.actions[3]
                    self.melee = MeleeHitBox(self, self.pos.x, self.pos.y, 0, -self.height)
                elif self.vel.y > 0:
                    self.action = self.actions[2]
                    self.melee = MeleeHitBox(self, self.pos.x, self.pos.y, 0, self.height)

            if abs(dx) <= (self.width + self.game.player.width)/2:
                self.vel.x = 0
            else:
                self.vel.x = -new_move_speed if dx >= 0 else new_move_speed
                if self.vel.x < 0:
                    self.action = self.actions[0]
                    self.melee = MeleeHitBox(self, self.pos.x, self.pos.y, -(self.width/2))
                elif self.vel.x > 0:
                    self.action = self.actions[1]
                    self.melee = MeleeHitBox(self, self.pos.x, self.pos.y, self.width)

            if self.vel == vec(0, 0):
                self.dir = vec(dx, dy).normalize()
                if abs(self.dir.x) > abs(self.dir.y):
                    if self.dir.x < 0:
                        self.action = self.actions[1]
                        self.melee = MeleeHitBox(self, self.pos.x, self.pos.y, self.width)
                    elif self.dir.x > 0:
                        self.action = self.actions[0]
                        self.melee = MeleeHitBox(self, self.pos.x, self.pos.y, -(self.width/2))
                else:
                    if self.dir.y < 0:
                        self.action = self.actions[2]
                        self.melee = MeleeHitBox(self, self.pos.x, self.pos.y, 0, self.height)
                    elif self.dir.y > 0:
                        self.action = self.actions[3]
                        self.melee = MeleeHitBox(self, self.pos.x, self.pos.y, 0, -self.height)
                self.action = self.actions[4]
                if now - self.last_bite > BITE_RATE:
                    self.attack()
            else:
                self.dir = self.vel.normalize()

            mag = vec(dx, dy).magnitude()
        else:
            if self.action_frame >= self.action_frames:
                self.action_frame = 0
                self.action_index = np.random.choice(len(self.actions), 1, p=[0.125, 0.125, 0.125, 0.125, 0.5])[0]
                self.action = self.actions[self.action_index]

            if self.action == self.actions[0]:
                self.vel.x = -MOB_SPEED
            elif self.action == self.actions[1]:
                self.vel.x = MOB_SPEED
            elif self.action == self.actions[2]:
                self.vel.y = MOB_SPEED
            elif self.action == self.actions[3]:
                self.vel.y = -MOB_SPEED
            elif self.action == self.actions[4]:
                self.vel = vec(0, 0)
            if self.vel.x != 0 and self.vel.y != 0:
                self.vel /= sqrt(2)

        self.rect.x = self.pos.x
        detect_collision(self, self.game.me, 'x')
        self.rect.y = self.pos.y
        detect_collision(self, self.game.me, 'y')

        self.rect.x = self.pos.x
        detect_collision(self, self.game.obstacles, 'x')
        self.rect.y = self.pos.y
        detect_collision(self, self.game.obstacles, 'y')
        self.pos += self.vel

        self.hitbox.center = self.rect.center

    def attack(self):
        if self.melee != None: # if there is a melee hitbox
            Attack(self.game, self.game.me, self.melee)
            now = pg.time.get_ticks()
            self.last_bite = now

    def animate(self, dir=[]):
        # use idle image or animations based on actions
        self.current_dir = dir
        if self.action == self.actions[4]:
            self.index = 1
        else:
            self.current_frame += 1
            # self.animation_frames = random.randint(6, 10)
            if self.current_frame >= self.animation_frames:
                self.current_frame = 0
                self.index = (self.index + 1) % len(dir)
                self.last_action = self.action

        # check if the index is greater than the array size
        if dir is not None:
            if self.index >= len(dir):
                self.index = 0
            self.image = dir[self.index]

    def draw_hitbox(self):
        pg.draw.rect(self.game.screen, MADANG, self.hitbox, 2)

    def update(self):
        if self.health <= 0:
            drop = random.randint(0, 100)
            IMeat(self.game, self.pos - vec(25, 25))
            if drop < 50:
                IPelt(self.game, self.pos + vec(25, 25))
            if drop < 65:
                IMeat(self.game, self.pos - vec(25, 25))

            self.game.mob_count -= 1
            self.kill()
        else:
            if self.action == self.actions[0]:
                self.animate(self.left)
                self.hitbox = self.rect.inflate(-6, 0) # (self.pos.x + 3, self.pos.y, 44, 30)
            elif self.action == self.actions[1]:
                self.animate(self.right)
                self.hitbox = self.rect.inflate(-6, 0) # (self.pos.x + 3, self.pos.y, 44, 30)
            elif self.action == self.actions[2]:
                self.animate(self.front)
                self.hitbox = self.rect.inflate(-24, -2) # (self.pos.x + 12, self.pos.y + 1, 29, 32)
            elif self.action == self.actions[3]:
                self.animate(self.back)
                self.hitbox = self.rect.inflate(-30, 0) # (self.pos.x + 15, self.pos.y, 17, 32)
            elif self.action == self.actions[4]:
                self.animate(self.current_dir)
            # print(self.action)
            self.width = self.rect.size[0]
            self.height = self.rect.size[1]
            self.get_actions()
            self.game.all_sprites.change_layer(self, self.rect.bottom)
