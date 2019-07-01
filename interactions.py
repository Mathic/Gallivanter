from helper import *
from tools import *

game_folder = path.dirname(__file__)
music_folder = path.join(game_folder, 'resources')

class MeleeHitBox():
    def __init__(self, game, x, y, width=0, height=0):
        self.game = game
        self.hitbox = pg.Rect(x + width, y + height, 64, 64)

    def draw_hitbox(self, game, color):
        pg.draw.rect(game.screen, color, self.hitbox, 2)

class HealthBar():
    def __init__(self, game, x, y, width=50):
        self.game = game
        self.bar = pg.Rect(x, y, width, 10)
        self.first_time = 0

    def draw_health(self, game, x, y, color, width=50):
        self.bar = pg.Rect(x, y, width, 10)
        pg.draw.rect(game.screen, color, self.bar)
        pg.draw.rect(game.screen, BLACK, self.bar, 2)

class Attack():
    def __init__(self, game, target, weapon):
        sprites = target.sprites()
        self.game = game
        dir = vec(1, 0).rotate(-self.game.player.dir_angle)
        width = self.game.player.image.get_size()[0]
        height = self.game.player.image.get_size()[1]
        self.now = pg.time.get_ticks()

        for target in sprites:
            if collided(weapon, target):
                self.game.player.last_action = pg.time.get_ticks()
                if self.now - self.game.last_hit > TOOL_LIFETIME:
                    self.now = pg.time.get_ticks()
                    self.game.last_hit = self.now
                    if type(target).__name__ == 'TreeBottom' and not target.chopped:
                        index = random.randint(0, len(WOOD_CHOP) - 1)
                        play_sound(WOOD_CHOP[index])
                        Axe(self.game, self.game.player.pos, dir, self.game.player.facing, width, height)
                        target.health -= 25
                    if type(target).__name__ == 'Wolf':
                        target.health -= 25
                        if target.health <= 25: # number should be weapon damage
                            play_sound(WOLF_WHINE, 1)
                        else:
                            Sword(self.game, self.game.player.pos, dir, self.game.player.facing, width, height)
                            play_sound(PUNCH)
                            target.health_bar.first_time = 0
                        target.attacked = True
                    if type(target).__name__ == 'Player':
                        target.health -= random.randint(3, 8)
                        print('%s is attacking %s! %d' %(type(self).__name__, 'me', self.game.player.health))
                        play_sound(PAINB, 0, 0.5)
                        play_sound(GRUNT, 1)

class Pickup():
    def __init__(self, game, target, hitbox):
        pickups = target.sprites()
        for pickup in pickups:
            if collided(hitbox, pickup):
                game.player.last_action = pg.time.get_ticks()
                if not pickup.in_inventory:
                    index = game.inventory.add(pickup.item_name)
                    game.hotbar.add_to_hotbar(index, pickup.item_name)
                    if pickup.item_name == 'rock': # temp rock spawn before cave level
                        game.rock_count -= 1
                        index = random.randint(0, len(ROCK_MINE) - 1)
                        play_sound(ROCK_MINE[index])
                    else:
                        play_sound(PICKUP_SOUND)
                    pickup.kill()
