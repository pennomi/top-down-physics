import asyncio
from physics.entities import Space, Entity
from physics.vec3d import Vec3d


class Game:
    def __init__(self):
        # The main event loop
        self.loop = asyncio.get_event_loop()

        # The Physics world
        self.space = Space()

        self.hero1 = Entity(position=Vec3d(3, 5, 0), mass=1)
        self.space.add(self.hero1)

    def update(self, dt, loop):
        self.space.update(dt)
        loop.call_later(dt, self.update, dt, loop)