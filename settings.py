from sounds import *

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

INVENTORY = (211, 170, 116)
INV_SLOT_IMG = 'inventory_slot.png'
HOVER_SLOT_IMG = 'hover_slot.png'

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

MOUSE_CLICK_TIMER = 500

LEFT_CLICK = 1
RIGHT_CLICK = 3

# tilesize
TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

MAP = 'map2.txt'

# Layers
BG_LAYER = 0
FG_LAYER = 1
STRUCTURE_LAYER = 2
ITEM_LAYER = 3
CHARACTER_LAYER = 4
GUI_LAYER = 50000

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

CHARACTER_SPRITES = 'character.png'

# Tools and structures
STRUCTURE_IMG = 'structures.png'

DOOR_IMG = 'ayenne_door.png'
FLOOR_IMG = 'ayenne_floor.png'
WALL_IMG = 'ayenne_wall.png'
CAMPFIRE_IMG = 'campfire.png'

STEAK_IMG = 'tile019.png'

TOOL_IMG = 'tools.png'
SWING_RATE = 375
TOOL_LIFETIME = 375
TOOL_SPEED = 10

PICK_IMG = 'tile011.png'
SWORD_IMG = 'tile014.png'
AXE_IMG = 'tile028.png'

# Reources and mobs
BITE_RATE = 600
MOB_SPEED = 2

# WOLF_IMG = 'wolf2.png'
# IDLE_WOLF_IMG = 'idle_wolf.png'
APRIL_WOLF_IMG = 'aprilsilverwolf.png'
TREE_IMG = 'tree.png'
GRASS_IMG = 'grass.png'

PINE_IMG = 'pine_tree.png'
BIRCH_IMG = 'birch_tree.png'
MAPLE_IMG = 'maple_tree.png'

BOULDER_IMG = 'boulder.png'

TREE_GROW_TIME = 180000

# Background image
BG_IMG = 'bg.png'

# Inventory
ITEM_IMG = 'items.png'

CRAFTABLE_IMG = 'craftables.png'
GATHERABLE_IMG = 'gatherables.png'

SPRITES = 'assets.png'

HOTBAR_IMG = 'hotbar.png'
HOTBAR_OFFSET = 325
HOTBAR_Y_OFFSET = 9
HOTBAR_X_OFFSET = 60

#  Wall image
BOUNDARY_IMG = 'tile035.png'

# Button Sprites
PLAY_BTN = 'play_btn.png'
EXIT_BTN = 'exit_btn.png'
MUTE_BTN = 'mute_btn.png'
HOVER_BTN = 'hover.png'
UNMUTE_BTN = 'unmute_btn.png'
RESUME_BTN = 'resume_btn.png'
