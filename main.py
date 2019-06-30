# KidsCanCode - Game Development with Pygame video series
# Tile-based game - Part 1
# Project setup
# Video link: https://youtu.be/3UxnelT9aCo

import sys

from buttons import *
from interactions import *
from inventory import *
from mobs import *
from recipes import *
from resources import *
from sprites import *
from structures import *
from tilemap import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
        # print(pg.font.get_fonts())

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'resources')
        self.map = Map(path.join(img_folder, MAP))
        self.bg_img = pg.image.load(path.join(img_folder, BG_IMG)).convert_alpha()
        self.boundary_img = pg.image.load(path.join(img_folder, BOUNDARY_IMG)).convert_alpha()
        self.boundary_img = pg.transform.scale(self.boundary_img, (64, 64))

        self.play_img = pg.image.load(path.join(img_folder, PLAY_BTN)).convert_alpha()
        self.exit_img = pg.image.load(path.join(img_folder, EXIT_BTN)).convert_alpha()
        self.mute_img = pg.image.load(path.join(img_folder, MUTE_BTN)).convert_alpha()
        self.unmute_img = pg.image.load(path.join(img_folder, UNMUTE_BTN)).convert_alpha()
        self.resume_img = pg.image.load(path.join(img_folder, RESUME_BTN)).convert_alpha()
        self.hover_img = pg.image.load(path.join(img_folder, HOVER_BTN)).convert_alpha()

        self.door_img = pg.image.load(path.join(img_folder, DOOR_IMG)).convert_alpha()
        self.door_img = pg.transform.scale(self.door_img, (64, 64))
        self.floor_img = pg.image.load(path.join(img_folder, FLOOR_IMG)).convert_alpha()
        self.floor_img = pg.transform.scale(self.floor_img, (64, 64))
        self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (64, 64))
        self.campfire_img = pg.image.load(path.join(img_folder, CAMPFIRE_IMG)).convert_alpha()
        self.campfire_img = pg.transform.scale(self.campfire_img, (64, 64))

    def new(self):
        # initialize all variables and do all the setup for a new game
        # Not visible: collides, obstacles
        # Visible: items, tools, mobs, me, structures, walls, buttons
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.buttons = pg.sprite.LayeredUpdates()
        self.collides = pg.sprite.LayeredUpdates()
        self.items = pg.sprite.LayeredUpdates()
        self.me = pg.sprite.LayeredUpdates()
        self.melee = pg.sprite.LayeredUpdates()
        self.mobs = pg.sprite.LayeredUpdates()
        self.obstacles = pg.sprite.LayeredUpdates()
        self.resources = pg.sprite.LayeredUpdates()
        self.structures = pg.sprite.LayeredUpdates()
        self.tools = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.LayeredUpdates()
        self.workbench = pg.sprite.LayeredUpdates()

        self.paused = False
        self.muted = False
        self.crafting = False
        self.last_hit = 0
        self.inventory_open = False
        self.inventory = Inventory()
        self.mob_count = 0
        self.rock_count = 0
        self.available_tiles = []
        self.grid = WeightedGrid(self, WIDTH, HEIGHT)

        self.mutebutton = None
        self.hover = Button(self, self.hover_img, WIDTH - 200, 150, 150, 75, None)
        load_music(INTRO_SONG)

        player_row = player_col = 0

        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                # self.graph.append(vec(row, col))
                if tile == '1':
                    Boundary(self, col, row)
                    self.grid.walls.append(vec(row, col))
                elif tile == 'M':
                    Wolf(self, col, row)
                    self.mob_count += 1
                elif tile == 'T':
                    # Tree(self, col, row)
                    self.grid.walls.append(vec(row, col))
                    tree = random.randint(0, 2)
                    if tree == 0:
                        img = PINE_IMG
                        TreeTop(self, col, row - 2, img)
                        TreeBottom(self, col, row, img)
                    elif tree == 1:
                        img = MAPLE_IMG
                        TreeBottom(self, col, row, img)
                    else:
                        img = BIRCH_IMG
                        TreeTop(self, col, row - 2, img)
                        TreeBottom(self, col, row, img)

                elif tile == 'F':
                    Floor(self, col, row)
                elif tile == 'D':
                    Door(self, col, row)
                elif tile == 'W':
                    Wall(self, col, row)
                    # self.wall_tiles.append(vec(row, col))
                    self.grid.walls.append(vec(row, col))
                elif tile == 'C':
                    self.campfire = Campfire(self, col, row)
                    self.grid.walls.append(vec(row, col))
                elif tile == 'P':
                    self.player = Player(self, col, row)
                else:
                    self.available_tiles.append((col, row))
                    draw = random.randint(0, 100)
                    if draw < 10:
                        Grass(self, col, row)
                    elif draw == 99:
                        pos = vec(col, row) * TILESIZE
                        IRock(self, pos)
                        self.rock_count += 1

        self.camera = Camera(self.map.width, self.map.height)
        self.hotbar = Hotbar(self, self.player.pos)

        index = self.inventory.add('sword')
        self.hotbar.add_to_hotbar(index, 'sword')
        self.total_rocks = self.rock_count

        # print(self.all_sprites.layers())
        # print(list(self.available_tiles))

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            if not self.paused:
                self.events()
                self.update()
            self.draw()

    def quit(self):
        play_sound(QUIT_BUTTON_SOUND)
        pg.time.wait(500)
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)

        if self.mob_count <= 2:
            index = random.randint(0, len(self.available_tiles) - 1)
            x_pos = self.available_tiles[index][0]
            y_pos = self.available_tiles[index][1]
            Wolf(self, x_pos, y_pos)
            self.mob_count += 1

        if self.rock_count <= self.total_rocks: # temp rock spawn before cave level
            index = random.randint(0, len(self.available_tiles) - 1)
            x_pos = self.available_tiles[index][0]
            y_pos = self.available_tiles[index][1]
            pos = vec(x_pos, y_pos) * TILESIZE
            IRock(self, pos)
            self.rock_count += 1

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw_hitboxes(self, sprite):
        if hasattr(sprite, 'draw_hitbox') and type(sprite).__name__ == 'Player':
            sprite.draw_hitbox()
            if sprite.melee != None:
                sprite.melee.draw_hitbox(self, DARKGREY)
        if hasattr(sprite, 'draw_hitbox') and type(sprite).__name__ == 'TreeBottom':
            sprite.draw_hitbox()
        if hasattr(sprite, 'melee') and type(sprite).__name__ != 'Player':
            if hasattr(sprite.melee, 'draw_hitbox') and sprite.melee != None:
                sprite.melee.draw_hitbox(self, RED)
        if hasattr(sprite, 'health_bar'):
            if sprite.attacked:
                sprite.health_bar.draw_health(self, sprite.pos.x, sprite.pos.y, GREEN, (sprite.health / sprite.starting_health) * 50)

    def draw(self):
        self.screen.fill(BGCOLOR)
        # self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            self.draw_hitboxes(sprite)
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    play_sound(RESUME_BUTTON_SOUND)
                    self.paused = True
                    self.show_pause_screen()
                if event.key == pg.K_q:
                    play_sound(LEATHER_INVENTORY, channel=1)
                    self.inventory_open = True
                    self.paused = True
                    self.show_inventory_screen()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == LEFT_CLICK:
                    now = pg.time.get_ticks()
                    if now - self.player.last_action > SWING_RATE and self.paused == False:
                        self.player.last_action = now
                        dir = vec(1, 0).rotate(-self.player.dir_angle)
                        width = self.player.image.get_size()[0]
                        height = self.player.image.get_size()[1]

                        mining = Attack(self, self.resources, self.player.melee)
                        hunting = Attack(self, self.mobs, self.player.melee)

                        target = mining.target_hit()
                        if target != None:
                            if type(target).__name__ == 'Tree' and not target.chopped:
                                Axe(self, self.player.pos, dir, self.player.facing, width, height)
                                target.health -= 25

                        target = hunting.target_hit()
                        if target != None:
                            Sword(self, self.player.pos, dir, self.player.facing, width, height)
                            play_sound(PUNCH)
                            target.health -= 25
                            target.health_bar.first_time = 0

    def text_objects(self, text, font):
        textSurface = font.render(text, True, BLACK)
        return textSurface, textSurface.get_rect()

    def unpause(self):
        if not self.muted:
            change_song(VILLAGE_SONG)
        self.paused = False
        for btn in self.buttons:
            btn.kill()

    def close_inventory(self):
        # change_song('village16.wav')
        self.paused = False
        self.inventory_open = False
        self.crafting = False
        for btn in self.buttons:
            btn.kill()

    def mute(self):
        if self.muted:
            pg.mixer.music.play()
            self.mutebutton.change_image(self.mute_img, WIDTH - 200, 350, 150, 75)
        else:
            pg.mixer.music.fadeout(200)
            self.mutebutton.change_image(self.unmute_img, WIDTH - 200, 350, 150, 75)

        self.muted = not self.muted
        self.buttons.draw(self.screen)
        pg.display.update()

    def show_start_screen(self):
        intro = True
        if not self.muted:
            change_song(INTRO_SONG)
        self.screen.fill(BGCOLOR)
        self.screen.blit(self.bg_img, (0, 0))
        Button(self, self.play_img, WIDTH - 200, 150, 150, 75, self.game_loop, PLAY_BUTTON_SOUND)
        Button(self, self.exit_img, WIDTH - 200, 250, 150, 75, self.quit, QUIT_BUTTON_SOUND)
        if self.muted:
            self.mutebutton = Button(self, self.unmute_img, WIDTH - 200, 350, 150, 75, self.mute, MUTE_BUTTON_SOUND)
        else:
            self.mutebutton = Button(self, self.mute_img, WIDTH - 200, 350, 150, 75, self.mute, MUTE_BUTTON_SOUND)
        self.buttons.draw(self.screen)

        while intro:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()

                for btn in self.buttons:
                    btn.handle_events(event)

            pg.display.update()
            self.clock.tick(15)

    def show_pause_screen(self):
        if not self.muted:
            change_song(INTRO_SONG)
        # Translucent pause menu
        s = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
        s.fill((0, 0, 0, 64))
        self.screen.blit(s, (0, 0))
        self.screen.blit(self.bg_img, (0, 0))
        self.hover = Button(self, self.hover_img, WIDTH - 200, 150, 150, 75, None)
        Button(self, self.resume_img, WIDTH - 200, 150, 150, 75, self.unpause, RESUME_BUTTON_SOUND)
        Button(self, self.exit_img, WIDTH - 200, 250, 150, 75, self.quit, QUIT_BUTTON_SOUND)
        if self.muted:
            self.mutebutton = Button(self, self.unmute_img, WIDTH - 200, 350, 150, 75, self.mute, MUTE_BUTTON_SOUND)
        else:
            self.mutebutton = Button(self, self.mute_img, WIDTH - 200, 350, 150, 75, self.mute, MUTE_BUTTON_SOUND)
        self.buttons.draw(self.screen)

        while self.paused:
            for event in pg.event.get():
                #print(event)
                if event.type == pg.QUIT:
                    self.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        play_sound(RESUME_BUTTON_SOUND)
                        self.paused = False
                        for btn in self.buttons:
                            btn.kill()

                for btn in self.buttons:
                    btn.handle_events(event)

            pg.display.update()
            self.clock.tick(15)

    def show_inventory_screen(self):
        s = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
        s.fill((255, 255, 255, 80))
        self.screen.blit(s, (0, 0))
        # self.inventory_gui = InventoryGUI(self, self.player.pos)

        # Show Inventory contents
        y_pos = 100
        y_offset = 50

        smallText = pg.font.SysFont("segoeprint", 20)
        inv_text, inv_rect = self.text_objects("Inventory contents:", smallText)
        inv_rect.center = (200, y_pos + y_offset)
        self.screen.blit(inv_text, inv_rect)

        for item in self.inventory.contents:
            y_pos += y_offset
            smallText = pg.font.SysFont("segoeprint", 20)
            if self.inventory.contents[item] > 1:
                msg = str(self.inventory.contents[item]) + " " + item.capitalize() + "s"
            else:
                msg = str(self.inventory.contents[item]) + " " + item.capitalize()
            textSurf, textRect = self.text_objects(msg, smallText)
            textRect.center = (200, y_pos + y_offset)
            textRect.left = inv_rect.left
            self.screen.blit(textSurf, textRect)

        # Show craftable items
        x_pos = 420
        x_offset = 80

        smallText = pg.font.SysFont("segoeprint", 20)
        textSurf, textRect = self.text_objects("Craftable items:", smallText)
        textRect.center = (500, 150)
        self.screen.blit(textSurf, textRect)

        # STRUCTURES!!! DO NOT DELETE!!
        # Button(self, self.door_img, x_pos, 200, 64, 64, self.craft)
        # x_pos += x_offset
        # Button(self, self.wall_img, x_pos, 200, 64, 64, self.craft)
        # x_pos += x_offset
        # Button(self, self.floor_img, x_pos, 200, 64, 64, self.craft)
        # x_pos += x_offset
        # Button(self, self.campfire_img, x_pos, 200, 64, 64, self.craft)

        for recipe in Recipe.__subclasses__():
            craft_name = recipe.__name__
            workbench_in_range = False

            if hasattr(recipe, 'proximity'):
                for workbench in self.workbench:
                    print(workbench)
                    if workbench.name == recipe.proximity:
                        if abs(self.player.pos.x - workbench.x * TILESIZE) <= recipe.range and abs(self.player.pos.y - workbench.y * TILESIZE) <= recipe.range:
                            workbench_in_range = True
                            break
            else:
                workbench_in_range = True

            if workbench_in_range and self.inventory.contains_items(recipe.ingredients):
                recipe(self, x_pos, 200)
                x_pos += x_offset

        Button(self, self.resume_img, 850, 650, 150, 75, self.close_inventory, RESUME_BUTTON_SOUND)
        self.hover = Button(self, self.hover_img, 850, 650, 150, 75, None)
        # quit_btn = Button(self, self.exit_img, 650, 450, 150, 75, self.quit)
        self.buttons.draw(self.screen)

        while self.inventory_open:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_e:
                        # self.inventory_gui.kill()
                        play_sound(RESUME_BUTTON_SOUND)
                        self.close_inventory()

                for btn in self.buttons:
                    btn.handle_events(event)

            pg.display.update()
            self.clock.tick(15)

    def show_go_screen(self):
        pass

    def game_loop(self):
        if not self.muted:
            change_song(VILLAGE_SONG)
        for btn in self.buttons:
            btn.kill()

        while True:
            g.run()
            g.show_go_screen()

# create the game object
g = Game()
g.new()
g.show_start_screen()
