from pymunk import Vec2d
from physics.entities import Entity, Space
from pyglet import gl
from pyglet.window import key
import asyncio
import pyglet

pyglet.options['audio'] = ('alsa', 'openal', 'directsound', 'silent')

WINDOW = pyglet.window.Window()


def update(dt):
    space.update(dt)
    LOOP.call_later(dt, update, dt)


@WINDOW.event
def on_mouse_press(x, y, button, modifiers):
    print("Clicked at ({}, {})".format(x, y))


@WINDOW.event
def on_key_press(symbol, modifiers):
    if symbol == key.A:
        print("It was an A")
    print("Pressed key {} ({})".format(symbol, modifiers))


@WINDOW.event
def on_key_release(symbol, modifiers):
    print("Released key {} ({})".format(symbol, modifiers))


@WINDOW.event
def on_draw():
    WINDOW.clear()
    space.debug_draw()
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


if __name__ == "__main__":
    print("Beginning test...")

    space = Space()

    # player
    player = Entity(mass=1)
    player.movement_velocity = Vec2d(3, 3)
    space.add(player)

    # t-rex
    trex = Entity(position=Vec2d(15, 15), radius=2, mass=3)
    trex.movement_velocity = Vec2d(-3, -3)
    space.add(trex)

    LOOP.call_soon(run_pyglet)
    LOOP.call_soon(update, 1/60.)
    LOOP.run_forever()
    LOOP.close()
    print("Test Completed")
