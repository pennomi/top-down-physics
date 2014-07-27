from pymunk import Vec2d  # TODO: internalize this
from physics import debug_draw
from itertools import combinations


class Entity:
    def __init__(self, position=None, angle=0.0, radius=0.5, mass=float('inf')):
        if position is None:
            position = Vec2d(0, 0)
        self.position = position
        self.angle = angle
        self.radius = radius
        self.mass = mass
        self.movement_velocity = Vec2d(0, 0)

        # Special Variables to persist state
        self.colliding = False

    def collides_with(self, other: 'Entity'):
        d = self.position.get_distance(other.position)
        return self.radius + other.radius >= d


class Space:
    def __init__(self):
        self._entities = []

    def add(self, entity: Entity):
        # noinspection PyTypeChecker
        self._entities.append(entity)

    def debug_draw(self):
        for e in self._entities:
            debug_draw.circle(e)

    def update(self, dt):
        for e in self._entities:
            # reset state
            e.colliding = False

            # Do the pre-movement (no Continuous Collision Detection... yet)
            e.position += e.movement_velocity * dt

        collisions = []
        for c in combinations(self._entities, 2):
            a, b = c
            if a.collides_with(b):
                a.colliding = True
                b.colliding = True
                collisions.append(c)

        for c in collisions:
            a, b = c

            # get amount penetrated
            d = a.position.get_distance(b.position)
            penetration = a.radius + b.radius - d

            # apply movement to the objects to push them away the proper amount
            direction = (a.position - b.position).normalized()

            ratio_a = a.mass / (a.mass + b.mass)
            ratio_b = b.mass / (a.mass + b.mass)
            a.position += direction * (penetration * ratio_b)
            b.position -= direction * (penetration * ratio_a)

