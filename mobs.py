from helper import *
from inventory import *

class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs, game.collides
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game


class Wolf(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs, game.collides
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.images = []
        self.load_sprites()
        self.index = random.randint(0, len(self.images) - 1)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        self.rect.center = self.pos

        self.action_frames = 100
        self.action_frame = 0

        self.animation_frames = 25
        self.current_frame = 0
        self.current_dir = self.images
        self.health = random.randint(50, 100)
        self.actions = ['walk_lf', 'walk_rt', 'walk_fr', 'walk_bk', 'idle']
        self.action_index = 4
        self.action = self.actions[self.action_index]

    def load_sprites(self):
        sprite_sheet = SpriteSheet(WOLF_IMG)
        image = sprite_sheet.get_image(0, 0, 23, 12)
        self.images.append(image)
        image = sprite_sheet.get_image(23, 0, 23, 12)
        self.images.append(image)
        image = sprite_sheet.get_image(46, 0, 23, 12)
        self.images.append(image)
        image = sprite_sheet.get_image(69, 0, 23, 12)
        self.images.append(image)
        image = sprite_sheet.get_image(92, 0, 23, 12)
        self.images.append(image)

    def get_actions(self):
        self.action_frame += 1
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
        collide_with_walls(self, self.game.obstacles, 'x')
        self.rect.y = self.pos.y
        collide_with_walls(self, self.game.obstacles, 'y')

        self.pos += self.vel

    def animate(self, dir=[]):
        self.current_frame += 1
        self.animation_frames = random.randint(6, 10)
        if self.current_frame >= self.animation_frames:
            self.current_frame = 0
            self.index = (self.index + 1) % len(dir)

        if dir is not None:
            if self.index >= len(dir):
                self.index = 0
            self.image = dir[self.index]

    def update(self):
        self.get_actions()
        self.animate(self.images)
        # print(self.action)
        if self.health <= 0:
            drop = random.randint(0, 100)
            if drop < 50:
                Pelt(self.game, self.pos + vec(25, 25))
            if drop < 95:
                Meat(self.game, self.pos - vec(25, 25))
                
            self.game.mob_count -= 1
            self.kill()
