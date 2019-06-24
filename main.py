# KidsCanCode - Game Development with Pygame video series
# Tile-based game - Part 1
# Project setup
# Video link: https://youtu.be/3UxnelT9aCo

import sys

from buttons import *
from inventory import *
from mobs import *
from recipes import *
from resources import *
from sprites import *
from structures import *
from tilemap import *

# import pygameMenu
# from pygameMenu.locals import *  # Import constants (like actions)

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
        self.play_btn = pg.image.load(path.join(img_folder, PLAY_BTN)).convert_alpha()
        self.exit_btn = pg.image.load(path.join(img_folder, EXIT_BTN)).convert_alpha()
        self.resume_btn = pg.image.load(path.join(img_folder, RESUME_BTN)).convert_alpha()

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
        self.all_sprites = pg.sprite.Group()
        self.buttons = pg.sprite.Group()
        self.collides = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.me = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.obstacles = pg.sprite.Group()
        self.resources = pg.sprite.Group()
        self.structures = pg.sprite.Group()
        self.tools = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.paused = False
        self.last_hit = 0
        self.inventory_open = False
        self.inventory = Inventory()
        self.mob_count = 0
        self.available_tiles = []

        player_row = player_col = 0

        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Boundary(self, col, row)
                elif tile == 'M':
                    Wolf(self, col, row)
                    self.mob_count += 1
                elif tile == 'T':
                    Tree(self, col, row)
                elif tile == 'F':
                    Floor(self, col, row)
                elif tile == 'D':
                    Door(self, col, row)
                elif tile == 'W':
                    Wall(self, col, row)
                elif tile == 'C':
                    self.campfire = Campfire(self, col, row)
                elif tile == 'P':
                    player_col = col
                    player_row = row
                else:
                    self.available_tiles.append((col, row))
                    draw = random.randint(0, 25)
                    if draw < 2:
                        Grass(self, col, row)
                    elif draw == 25:
                        pos = vec(col, row) * TILESIZE
                        IRock(self, pos)

        self.player = Player(self, player_col, player_row)
        self.camera = Camera(self.map.width, self.map.height)
        self.hotbar = Hotbar(self, self.player.pos)

        # index = self.inventory.add('meat')
        # self.hotbar.add_to_hotbar(index, 'meat')
        # print(self.available_tiles)

        index = self.inventory.add('sword')
        self.hotbar.add_to_hotbar(index, 'sword')

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)

        mobs = pg.sprite.groupcollide(self.mobs, self.tools, False, False)
        now = pg.time.get_ticks()
        for mob in mobs:
            if now - self.last_hit > TOOL_LIFETIME:
                self.last_hit = now
                mob.health -= random.randint(10, 25)

        if self.mob_count <= 2:
            index = random.randint(0, len(self.available_tiles) - 1)
            x_pos = self.available_tiles[index][0]
            y_pos = self.available_tiles[index][1]
            Wolf(self, x_pos, y_pos)
            self.mob_count += 1

        resources = pg.sprite.groupcollide(self.resources, self.tools, False, False)
        now = pg.time.get_ticks()
        for resource in resources:
            if now - self.last_hit > TOOL_LIFETIME:
                self.last_hit = now
                resource.health -= 25

        pickups = pg.sprite.spritecollide(self.player, self.items, False)
        for pickup in pickups:
            if not pickup.in_hotbar:
                index = self.inventory.add(pickup.item_name)
                self.hotbar.add_to_hotbar(index, pickup.item_name)
                pickup.kill()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        # self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.paused = True
                    self.show_pause_screen()
                if event.key == pg.K_e:
                    self.inventory_open = True
                    self.paused = True
                    self.show_inventory_screen()

    def text_objects(self, text, font):
        textSurface = font.render(text, True, BLACK)
        return textSurface, textSurface.get_rect()

    def draw_button(self,msg,x,y,w,h,ic,ac,action=None):
        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            pg.draw.rect(self.screen, ac,(x,y,w,h))
            if click[0] == 1 and action != None:
                action()
        else:
            pg.draw.rect(self.screen, ic,(x,y,w,h))

        smallText = pg.font.SysFont("segoeprint", 20)
        textSurf, textRect = self.text_objects(msg, smallText)
        textRect.center = ( (x+(w/2)), (y+(h/2)) )
        self.screen.blit(textSurf, textRect)

    def show_start_screen(self):
        intro = True
        load_music(INTRO_SONG)
        pg.mixer.music.play(-1)
        self.screen.blit(self.bg_img, (0, 0))
        Button(self, self.play_btn, 250, 450, 150, 75, self.game_loop)
        Button(self, self.exit_btn, 650, 450, 150, 75, self.quit)
        self.buttons.draw(self.screen)

        while intro:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    for btn in self.buttons:
                        if btn.clicked(event):
                            btn.action()

            pg.display.update()
            self.clock.tick(15)

    def unpause(self):
        # change_song('village16.wav')
        self.paused = False
        for btn in self.buttons:
            btn.kill()

    def close_inventory(self):
        # change_song('village16.wav')
        self.paused = False
        self.inventory_open = False
        for btn in self.buttons:
            btn.kill()

    def show_pause_screen(self):
        # change_song('intro16.wav')
        # Translucent pause menu
        s = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
        s.fill((255,255,255,128))
        self.screen.blit(s, (0, 0))
        resume_btn = Button(self, self.resume_btn, 250, 450, 150, 75, self.unpause)
        quit_btn = Button(self, self.exit_btn, 650, 450, 150, 75, self.quit)
        self.buttons.draw(self.screen)

        while self.paused:
            for event in pg.event.get():
                #print(event)
                if event.type == pg.QUIT:
                    self.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.paused = False
                        for btn in self.buttons:
                            btn.kill()
                if event.type == pg.MOUSEBUTTONDOWN:
                    for btn in self.buttons:
                        if btn.clicked(event):
                            btn.action()

            if resume_btn.rect.collidepoint(pg.mouse.get_pos()):
                resume_btn.image = pg.transform.scale(resume_btn.image, (120, 70))
            else:
                resume_btn.image = pg.transform.scale(resume_btn.image, (100, 50))

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
        textSurf, textRect = self.text_objects("Inventory contents:", smallText)
        textRect.center = (100, y_pos + y_offset)
        self.screen.blit(textSurf, textRect)
        for item in self.inventory.contents:
            y_pos += y_offset

            smallText = pg.font.SysFont("segoeprint", 20)

            if self.inventory.contents[item] > 1:
                msg = str(self.inventory.contents[item]) + " " + item.capitalize() + "s"
            else:
                msg = str(self.inventory.contents[item]) + " " + item.capitalize()
            textSurf, textRect = self.text_objects(msg, smallText)
            textRect.center = (100, y_pos + y_offset)
            self.screen.blit(textSurf, textRect)

        # Show craftable items
        x_pos = 320
        x_offset = 80

        smallText = pg.font.SysFont("segoeprint", 20)
        textSurf, textRect = self.text_objects("Craftable items:", smallText)
        textRect.center = (400, 150)
        self.screen.blit(textSurf, textRect)

        # STRUCTURES!!! DO NOT DELETE!!
        # Button(self, self.door_img, x_pos, 200, 64, 64, self.craft)
        # x_pos += x_offset
        # Button(self, self.wall_img, x_pos, 200, 64, 64, self.craft)
        # x_pos += x_offset
        # Button(self, self.floor_img, x_pos, 200, 64, 64, self.craft)
        # x_pos += x_offset
        # Button(self, self.campfire_img, x_pos, 200, 64, 64, self.craft)
        if 'log' in self.inventory.contents and 'rock' in self.inventory.contents:
            RPickaxe(self, PICK_IMG, x_pos, 200)
            x_pos += x_offset
            if self.inventory.contents['rock'] >= 2:
                RSword(self, SWORD_IMG, x_pos, 200)
                x_pos += x_offset
            if self.inventory.contents['log'] >= 2 and self.inventory.contents['rock'] >= 2:
                RAxe(self, AXE_IMG, x_pos, 200)
                x_pos += x_offset

        if abs(self.player.pos.x - self.campfire.x * TILESIZE) <= 128 and abs(self.player.pos.y - self.campfire.y * TILESIZE) <= 128 and 'meat' in self.inventory.contents:
            # Button(self, self.steak_img, x_pos, 200, 64, 64, self.cook)
            RSteak(self, STEAK_IMG, x_pos, 200)
            x_pos += x_offset

        resume_btn = Button(self, self.resume_btn, 850, 650, 150, 75, self.close_inventory)
        # quit_btn = Button(self, self.exit_btn, 650, 450, 150, 75, self.quit)
        self.buttons.draw(self.screen)

        while self.inventory_open:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_e:
                        # self.inventory_gui.kill()
                        self.close_inventory()
                if event.type == pg.MOUSEBUTTONDOWN:
                    for btn in self.buttons:
                        if btn.clicked(event):
                            btn.action()

            pg.display.update()
            self.clock.tick(15)

    def show_go_screen(self):
        pass

    def game_loop(self):
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
