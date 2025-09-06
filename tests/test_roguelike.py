import os
import random
import sys

import pytest
import tcod

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from roguelike import make_dungeon, handle_keys


def test_make_dungeon_player_start_is_floor():
    random.seed(0)
    dungeon, px, py = make_dungeon()
    assert len(dungeon) == 80 and len(dungeon[0]) == 45
    assert not dungeon[px][py]


def test_handle_keys_arrows_and_escape():
    class Dummy:
        def __init__(self, sym):
            self.sym = sym

    assert handle_keys(Dummy(tcod.event.KeySym.UP)) == (0, -1)
    assert handle_keys(Dummy(tcod.event.KeySym.DOWN)) == (0, 1)
    assert handle_keys(Dummy(tcod.event.KeySym.LEFT)) == (-1, 0)
    assert handle_keys(Dummy(tcod.event.KeySym.RIGHT)) == (1, 0)
    with pytest.raises(SystemExit):
        handle_keys(Dummy(tcod.event.KeySym.ESCAPE))
