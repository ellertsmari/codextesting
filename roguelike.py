import os
import random
import tcod

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
MAP_WIDTH = 80
MAP_HEIGHT = 45
ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30

class Rect:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return center_x, center_y

    def intersect(self, other):
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

def create_room(dungeon, room):
    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1 + 1, room.y2):
            dungeon[x][y] = False

def create_h_tunnel(dungeon, x1, x2, y):
    for x in range(min(x1, x2), max(x1, x2) + 1):
        dungeon[x][y] = False

def create_v_tunnel(dungeon, y1, y2, x):
    for y in range(min(y1, y2), max(y1, y2) + 1):
        dungeon[x][y] = False

def make_dungeon():
    dungeon = [[True for y in range(MAP_HEIGHT)] for x in range(MAP_WIDTH)]
    rooms = []
    for r in range(MAX_ROOMS):
        w = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        h = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        x = random.randint(0, MAP_WIDTH - w - 1)
        y = random.randint(0, MAP_HEIGHT - h - 1)
        new_room = Rect(x, y, w, h)
        if any(new_room.intersect(other) for other in rooms):
            continue
        create_room(dungeon, new_room)
        if rooms:
            prev_x, prev_y = rooms[-1].center()
            new_x, new_y = new_room.center()
            if random.randint(0, 1) == 1:
                create_h_tunnel(dungeon, prev_x, new_x, prev_y)
                create_v_tunnel(dungeon, prev_y, new_y, new_x)
            else:
                create_v_tunnel(dungeon, prev_y, new_y, prev_x)
                create_h_tunnel(dungeon, prev_x, new_x, new_y)
        rooms.append(new_room)
    player_x, player_y = rooms[0].center()
    return dungeon, player_x, player_y

def render_all(root_console, con, dungeon, player_x, player_y):
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            wall = dungeon[x][y]
            if wall:
                con.bg[x, y] = tcod.dark_gray
            else:
                con.bg[x, y] = tcod.dark_sepia
    con.ch[player_x, player_y] = ord('@')
    con.fg[player_x, player_y] = tcod.white
    root_console.blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0)
    tcod.console_flush()

    con.ch[player_x, player_y] = ord('.')

def handle_keys(key):
    if key.sym == tcod.event.KeySym.ESCAPE:
        raise SystemExit()
    if key.sym == tcod.event.KeySym.UP:
        return 0, -1
    if key.sym == tcod.event.KeySym.DOWN:
        return 0, 1
    if key.sym == tcod.event.KeySym.LEFT:
        return -1, 0
    if key.sym == tcod.event.KeySym.RIGHT:
        return 1, 0
    return 0, 0

def main():
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    tileset = tcod.tileset.get_default()
    with tcod.context.new_terminal(
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        tileset=tileset,
        title="Roguelike",
        vsync=True,
    ) as context:
        root_console = tcod.Console(SCREEN_WIDTH, SCREEN_HEIGHT, order="F")
        con = tcod.Console(MAP_WIDTH, MAP_HEIGHT, order="F")
        dungeon, player_x, player_y = make_dungeon()
        test_mode = os.environ.get("RUN_HEADLESS_TEST") == "1"
        while True:
            render_all(root_console, con, dungeon, player_x, player_y)
            context.present(root_console)
            if test_mode:
                break
            for event in tcod.event.wait():
                if event.type == "QUIT":
                    raise SystemExit()
                if event.type == "KEYDOWN":
                    dx, dy = handle_keys(event)
                    new_x = max(0, min(MAP_WIDTH - 1, player_x + dx))
                    new_y = max(0, min(MAP_HEIGHT - 1, player_y + dy))
                    if not dungeon[new_x][new_y]:
                        player_x, player_y = new_x, new_y

if __name__ == "__main__":
    main()
