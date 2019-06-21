# KidsCanCode - Game Development with Pygame video series
# Tile-based game - Part 1
# Project setup
# Video link: https://youtu.be/3UxnelT9aCo

import sys

from mobs import *
from resources import *
from sprites import *
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

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'resources')
        self.map = Map(path.join(img_folder, MAP))
        self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (64, 64))

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.collides = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.me = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.obstacles = pg.sprite.Group()
        self.resources = pg.sprite.Group()
        self.tools = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.paused = False
        self.last_hit = 0
        self.inventory_open = False
        self.inventory = {}

        player_row = player_col = 0

        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                elif tile == 'M':
                    Wolf(self, col, row)
                elif tile == 'T':
                    Tree(self, col, row)
                elif tile == 'P':
                    player_col = col
                    player_row = row
                else:
                    if random.randint(0, 25) < 2:
                        Grass(self, col, row)

        self.player = Player(self, player_col, player_row)
        print("Player pos: ", self.player.pos)
        # dir = vec(1, 0).rotate(-self.player.dir_angle)
        # self.sword = Sword(self, self.player.pos, dir)
        self.camera = Camera(self.map.width, self.map.height)
        self.hotbar = Hotbar(self, self.player.pos)

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

        attacks = pg.sprite.groupcollide(self.mobs, self.tools, False, False)
        now = pg.time.get_ticks()
        for attack in attacks:
            if now - self.last_hit > TOOL_LIFETIME:
                self.last_hit = now
                attack.health -= random.randint(10, 25)

        resources = pg.sprite.groupcollide(self.resources, self.tools, False, False)
        now = pg.time.get_ticks()
        for resource in resources:
            if now - self.last_hit > TOOL_LIFETIME:
                self.last_hit = now
                resource.health -= 25

        pickups = pg.sprite.spritecollide(self.player, self.items, True)
        for pickup in pickups:
            if pickup.item_name in self.inventory:
                self.inventory[pickup.item_name] += 1
                print(self.inventory)
            else:
                self.inventory[pickup.item_name] = 1
                print(self.inventory)

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
                    if self.inventory_open:
                        print('close inventory')
                        self.inventory_gui.kill()
                        self.inventory_open = False
                        self.paused = False
                    else:
                        print('open inventory')
                        self.inventory_gui = InventoryGUI(self, self.player.pos)
                        self.inventory_open = True
                        self.paused = True

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

        smallText = pg.font.SysFont("comicsansms",20)
        textSurf, textRect = self.text_objects(msg, smallText)
        textRect.center = ( (x+(w/2)), (y+(h/2)) )
        self.screen.blit(textSurf, textRect)

    def show_start_screen(self):
        intro = True
        load_music(INTRO_SONG)
        pg.mixer.music.play(-1)
        while intro:
            for event in pg.event.get():
                #print(event)
                if event.type == pg.QUIT:
                    self.quit()

            self.screen.fill(WHITE)
            largeText = pg.font.SysFont("comicsansms",115)
            TextSurf, TextRect = self.text_objects(TITLE, largeText)
            TextRect.center = ((WIDTH/2),(HEIGHT/4))
            self.screen.blit(TextSurf, TextRect)

            self.draw_button("GO!",250,450,100,50,GREEN,LIGHTGREEN,self.game_loop)
            self.draw_button("Quit",650,450,100,50,RED,LIGHTRED,self.quit)

            pg.display.update()
            self.clock.tick(15)

    def unpause(self):
        # change_song('village16.wav')
        self.paused = False

    def show_pause_screen(self):
        # change_song('intro16.wav')
        # Transparent pause menu
        s = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
        s.fill((255,255,255,128))
        self.screen.blit(s, (0, 0))

        while self.paused:
            for event in pg.event.get():
                #print(event)
                if event.type == pg.QUIT:
                    self.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.paused = False

            largeText = pg.font.SysFont("comicsansms",115)
            TextSurf, TextRect = self.text_objects(TITLE, largeText)
            TextRect.center = ((WIDTH/2),(HEIGHT/2))
            self.screen.blit(TextSurf, TextRect)

            self.draw_button("Continue",250,450,100,50,GREEN,LIGHTGREEN,self.unpause)
            self.draw_button("Quit",650,450,100,50,RED,LIGHTRED,self.quit)

            pg.display.update()
            self.clock.tick(15)

    def show_go_screen(self):
        pass

    def game_loop(self):
        change_song(VILLAGE_SONG)
        g.new()
        while True:
            g.run()
            g.show_go_screen()

# create the game object
g = Game()
g.show_start_screen()
