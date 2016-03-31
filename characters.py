from enum import Enum
from pyglet.window import key
from physics.entities import Entity
from physics.vec3d import Vec3d


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


class CharacterController:
    def __init__(self):
        self.input_forward = key.W
        self.input_backward = key.S
        self.input_left = key.A
        self.input_right = key.D


class BattleCharacter(Entity):
    def __init__(self, hp=10, speed=6, is_enemy=False, **kwargs):
        super().__init__(**kwargs)
        self.hp = hp
        self.speed = speed
        self.is_enemy = is_enemy
        self.controller = None

        # state
        self.movement_vector = Vec3d(0, 0, 0)
        self.target = None
        self.current_action = None

    def update(self, dt):
        if self.controller is None:
            self.movement_velocity = self.movement_vector.rotated_around_z(self.angle) * self.speed

        if self.hp <= 0:
            print("He's dead, Jim.")
            return
        if self.target:
            self.angle = (self.target.position - self.position).angle_around_z
        if self.current_action:
            self.current_action.update(dt, self.target)
            if self.current_action.state == ActionStates.done:
                self.current_action = None
