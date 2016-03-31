from game import Game
from physics.vec3d import Vec3d
from physics.entities import Tile
from pyglet import gl
from pyglet.window import key
import pyglet

pyglet.options['audio'] = ('alsa', 'openal', 'directsound', 'silent')


class GameWindow(pyglet.window.Window):
    def __init__(self, game, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = game

    def on_mouse_press(self, x, y, button, modifiers):
        print("Clicked at ({}, {})".format(x, y))

    def on_key_press(self, symbol, modifiers):
        self.game.key_pressed(symbol, modifiers)
        if symbol == key.W:
            self.game.hero1.movement_vector += Vec3d(1, 0, 0)
        elif symbol == key.A:
            self.game.hero1.movement_vector += Vec3d(0, 1, 0)
        elif symbol == key.S:
            self.game.hero1.movement_vector += Vec3d(-1, 0, 0)
        elif symbol == key.D:
            self.game.hero1.movement_vector += Vec3d(0, -1, 0)

    def on_key_release(self, symbol, modifiers):
        if symbol == key.W:
            self.game.hero1.movement_vector -= Vec3d(1, 0, 0)
        elif symbol == key.A:
            self.game.hero1.movement_vector -= Vec3d(0, 1, 0)
        elif symbol == key.S:
            self.game.hero1.movement_vector -= Vec3d(-1, 0, 0)
        elif symbol == key.D:
            self.game.hero1.movement_vector -= Vec3d(0, -1, 0)

    def on_draw(self,):
        self.clear()
        self.game.space.debug_draw()
        gl.glFinish()  # instead we should disable vsync

    def on_close(self):
        self.game.loop.stop()
        return pyglet.event.EVENT_HANDLED


def run_pyglet(loop):
    pyglet.clock.tick()
    for window in pyglet.app.windows:
        window.switch_to()
        window.dispatch_events()
        window.dispatch_event('on_draw')
        window.flip()
    loop.call_later(1/60., run_pyglet, loop)

MAP = [
    "11111111111111111111",
    "10000000000000000001",
    "10000000000000000001",
    "10000000000000000001",
    "10000000000000000001",
    "10000000000000000001",
    "10000000000000000001",
    "10000000000000000001",
    "10000000000000000001",
    "10000000000000000001",
    "10000000000000000001",
    "10000000000000000001",
    "10000000000000000001",
    "10000000000000000001",
    "10000000000000000001",
    "10000000000000000001",
    "10000000000000000001",
    "10000000000000000001",
    "11111111111111111111",
]


def main():
    print("Beginning test...")

    game = Game()
    window = GameWindow(game, width=650, height=610)

    # tiles
    for y, row in enumerate(reversed(MAP)):
        for x, tile_id in enumerate(row):
            # TODO: tile instancing?
            # TODO: think of a nice data structure for this...
            game.space.tiles.append(Tile(x, y, collision_type=int(tile_id)))

    # TODO: maybe loop should exist in the window. Let's think of a reusable
    # TODO: class that does all this crap for us... probably Panda3d anyway.
    game.loop.call_soon(run_pyglet, game.loop)
    game.loop.call_soon(game.update, 1/60., game.loop)
    game.loop.run_forever()
    game.loop.close()
    print("Test Completed")


if __name__ == "__main__":
    main()