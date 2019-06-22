# colors
# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (80, 200, 100)
LIGHTGREEN = (80, 220, 100)
RED = (205, 0, 0)
LIGHTRED = (255, 0, 0)
YELLOW = (255, 250, 205)

GRASS = (130, 188, 101)
GOSSIP = (135, 211, 124)
MADANG = (200, 247, 197)
DOLLY = (255, 255, 126)
SALOMIE = (255, 236, 139)
CANDYCORN = (254, 241, 96)

def get_darker(color, factor = 2/5):
    if len(color) == 4:
        darker = tuple( [int(c*factor) for c in color[:-1]] + [color[3]] )
    else:
        darker = tuple( [int(c*factor) for c in color] )

    return darker

# game settings
WIDTH = 1024
HEIGHT = 768
FPS = 60
TITLE = 'Gallivanter'
BGCOLOR = GRASS

# tilesize
TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

MAP = 'map2.txt'

# Player settings
PLAYER_SPEED = 250
P_WALK_FR = 'walk_fr.png'
P_WALK_BK = 'walk_bk.png'
P_WALK_LF = 'walk_lf.png'
P_WALK_RT = 'walk_rt.png'
P_IDLE_FR = 'idle_fr.png'
P_IDLE_BK = 'idle_bk.png'
P_IDLE_LF = 'idle_lf.png'
P_IDLE_RT = 'idle_rt.png'

# Tools and structures
STRUCTURE_IMG = 'structures.png'

DOOR_IMG = 'ayenne_door.png'
FLOOR_IMG = 'ayenne_floor.png'
WALL_IMG = 'ayenne_wall.png'
CAMPFIRE_IMG = 'campfire.png'

STEAK_IMG = 'steak.png'

TOOL_IMG = 'tools.png'
SWING_RATE = 375
TOOL_LIFETIME = 375
TOOL_SPEED = 10

PICK_IMG = 'pickaxe.png'
SWORD_IMG = 'sword.png'
AXE_IMG = 'axe.png'

# Reources and mobs
MOB_SPEED = 1

WOLF_IMG = 'wolf2.png'
TREE_IMG = 'tree.png'
GRASS_IMG = 'grass.png'

TREE_GROW_TIME = 180000

# Background
BG_IMG = 'background.png'

# inventory
BACKPACK_IMG = 'backpack.png'

ITEM_IMG = 'items.png'

HOTBAR_IMG = 'hotbar.png'
HOTBAR_OFFSET = 325
HOTBAR_Y_OFFSET = 9
HOTBAR_X_OFFSET = 60

# Music and sounds
VILLAGE_SONG = 'village16.mp3'
INTRO_SONG = 'intro16.mp3'

#  Wall image
BOUNDARY_IMG = 'tile035.png'

# Ground images
GROUND_IMG_1 = 'tile030.png'
GROUND_IMG_2 = 'tile008.png'
GROUND_IMG_3 = 'tile010.png'
GROUND_IMG_4 = 'tile013.png'

# Button Sprites
PLAY_BTN = 'play_btn.png'
EXIT_BTN = 'exit_btn.png'
RESUME_BTN = 'resume_btn.png'
