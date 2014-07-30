from enum import Enum
from game import Game
from physics.vec3d import Vec3d
from physics.entities import Entity, Tile
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
        if symbol == key.W:
            self.game.hero1.movement_velocity += Vec3d(0, 6, 0)
        elif symbol == key.A:
            self.game.hero1.movement_velocity += Vec3d(-6, 0, 0)
        elif symbol == key.S:
            self.game.hero1.movement_velocity += Vec3d(0, -6, 0)
        elif symbol == key.D:
            self.game.hero1.movement_velocity += Vec3d(6, 0, 0)

    def on_key_release(self, symbol, modifiers):
        if symbol == key.W:
            self.game.hero1.movement_velocity -= Vec3d(0, 6, 0)
        elif symbol == key.A:
            self.game.hero1.movement_velocity -= Vec3d(-6, 0, 0)
        elif symbol == key.S:
            self.game.hero1.movement_velocity -= Vec3d(0, -6, 0)
        elif symbol == key.D:
            self.game.hero1.movement_velocity -= Vec3d(6, 0, 0)

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
    "10000011111000000001",
    "10000011001000000001",
    "10000000000000000001",
    "10000000000000000001",
    "10000000000000000001",
    "10000000000000000001",
    "11111111111111111111",
]


class ActionStates(Enum):
    prep = 0
    action = 1
    recovery = 2
    done = 3


class Action():
    def __init__(self, prep_duration=2, action_duration=1, recovery_duration=1):
        self.prep_duration = prep_duration
        self.action_duration = action_duration
        self.recovery_duration = recovery_duration
        self.current_position = 0
        self.has_triggered = False

    def on_trigger(self, target):
        # Intended for subclassing
        pass

    @property
    def state(self):
        c, p = self.current_position, self.prep_duration
        if c >= p + self.action_duration + self.recovery_duration:
            return ActionStates.done
        elif c >= p + self.action_duration:
            return ActionStates.recovery
        elif c >= p:
            return ActionStates.action
        return ActionStates.prep

    def update(self, dt, target):
        self.current_position += dt
        trigger_states = [ActionStates.recovery, ActionStates.done]
        if not self.has_triggered and self.state in trigger_states:
            self.on_trigger(target)


class BattleCharacter(Entity):
    def __init__(self, hp=10, is_enemy=False, **kwargs):
        super().__init__(**kwargs)
        self.is_enemy = is_enemy
        self.hp = hp

        # state
        self.target = None
        self.current_action = None

    def update(self, dt):
        if self.hp <= 0:
            print("He's dead, Jim.")
            return
        if self.current_action:
            self.current_action.update(dt, self.target)
        if self.current_action.state == ActionStates.done:
            self.current_action = None


def main():
    print("Beginning test...")

    game = Game()
    window = GameWindow(game, width=1200, height=1000)

    # tiles
    for y, row in enumerate(reversed(MAP)):
        for x, tile_id in enumerate(row):
            # TODO: tile instancing?
            # TODO: think of a nice data structure for this...
            game.space.tiles.append(Tile(x, y, collision_type=int(tile_id)))

    # t-rex family
    trex = BattleCharacter(position=Vec3d(15, 15, 0), radius=2, mass=3)
    trex.movement_velocity = Vec3d(-3, -3, 0)
    game.space.add(trex)

    characters = [game.hero1, trex]

    # TODO: maybe loop should exist in the window. Let's think of a reusable
    # TODO: class that does all this crap for us... probably Panda3d anyway.
    game.loop.call_soon(run_pyglet, game.loop)
    game.loop.call_soon(game.update, 1/60., game.loop)
    game.loop.run_forever()
    game.loop.close()
    print("Test Completed")


if __name__ == "__main__":
    main()