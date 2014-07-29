from physics.vec3d import Vec3d
from physics.entities import Entity, Space, Tile
from pyglet import gl
from pyglet.window import key
import asyncio
import pyglet

pyglet.options['audio'] = ('alsa', 'openal', 'directsound', 'silent')

WINDOW = pyglet.window.Window(width=1200, height=1000)
SPACE = Space()
HERO = Entity(position=Vec3d(3, 5, 0), mass=1)
SPACE.add(HERO)


def update(dt):
    SPACE.update(dt)
    LOOP.call_later(dt, update, dt)


@WINDOW.event
def on_mouse_press(x, y, button, modifiers):
    print("Clicked at ({}, {})".format(x, y))


@WINDOW.event
def on_key_press(symbol, modifiers):
    if symbol == key.W:
        HERO.movement_velocity += Vec3d(0, 6, 0)
    elif symbol == key.A:
        HERO.movement_velocity += Vec3d(-6, 0, 0)
    elif symbol == key.S:
        HERO.movement_velocity += Vec3d(0, -6, 0)
    elif symbol == key.D:
        HERO.movement_velocity += Vec3d(6, 0, 0)


@WINDOW.event
def on_key_release(symbol, modifiers):
    if symbol == key.W:
        HERO.movement_velocity -= Vec3d(0, 6, 0)
    elif symbol == key.A:
        HERO.movement_velocity -= Vec3d(-6, 0, 0)
    elif symbol == key.S:
        HERO.movement_velocity -= Vec3d(0, -6, 0)
    elif symbol == key.D:
        HERO.movement_velocity -= Vec3d(6, 0, 0)


@WINDOW.event
def on_draw():
    WINDOW.clear()
    SPACE.debug_draw()
    gl.glFinish()  # instead we should disable vsync


@WINDOW.event
def on_close():
    LOOP.stop()
    return pyglet.event.EVENT_HANDLED


LOOP = asyncio.get_event_loop()


def run_pyglet():
    pyglet.clock.tick()
    for window in pyglet.app.windows:
        window.switch_to()
        window.dispatch_events()
        window.dispatch_event('on_draw')
        window.flip()
    LOOP.call_later(1/60., run_pyglet)

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
    "10000011111000000001",
    "10000011001000000001",
    "10000000000000000001",
    "10000000000000000001",
    "10000000000000000001",
    "10000000000000000001",
    "11111111111111111111",
]


def main():
    print("Beginning test...")

    # tiles
    for y, row in enumerate(reversed(MAP)):
        for x, tile_id in enumerate(row):
            # TODO: tile instancing?
            # TODO: think of a nice data structure for this...
            SPACE._tiles.append(Tile(x, y, collision_type=int(tile_id)))

    # player
    player = Entity(position=Vec3d(3, 3, 0), mass=1)
    player.movement_velocity = Vec3d(3, 3, 0)
    SPACE.add(player)

    # t-rex family
    trex = Entity(position=Vec3d(15, 15, 0), radius=0.25, mass=3)
    trex.movement_velocity = Vec3d(-3, -3, 0)
    SPACE.add(trex)

    trex = Entity(position=Vec3d(15, 5, 0), radius=1, mass=2)
    trex.movement_velocity = Vec3d(-4, 3, 0)
    SPACE.add(trex)

    trex = Entity(position=Vec3d(15, 3, 0), radius=1.5, mass=2)
    trex.movement_velocity = Vec3d(-4, 4, 0)
    SPACE.add(trex)

    trex = Entity(position=Vec3d(5, 15, 0), radius=1, mass=4)
    trex.movement_velocity = Vec3d(4, -4, 0)
    SPACE.add(trex)

    LOOP.call_soon(run_pyglet)
    LOOP.call_soon(update, 1/60.)
    LOOP.run_forever()
    LOOP.close()
    print("Test Completed")


if __name__ == "__main__":
    main()