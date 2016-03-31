from weakref import proxy
import asyncio
from characters import BattleCharacter
from physics.entities import Space
from physics.vec3d import Vec3d


class Game:
    def __init__(self):
        # The main event loop
        self.loop = asyncio.get_event_loop()

        # The Physics world
        self.space = Space()

        self.hero1 = BattleCharacter(position=Vec3d(3, 5, 0), mass=1)
        self.space.add(self.hero1)

        # t-rex
        self.trex = BattleCharacter(position=Vec3d(15, 15, 0), radius=2, mass=3)
        self.trex.movement_velocity = Vec3d(-3, -3, 0)
        self.space.add(self.trex)

        # targeting
        self.hero1.target = proxy(self.trex)
        self.trex.target = proxy(self.hero1)

        self.characters = [self.hero1, self.trex]

    def key_pressed(self, symbol, modifier):
        pass

    def update(self, dt, loop):
        self.space.update(dt)
        for c in self.characters:
            c.update(dt)
        loop.call_later(dt, self.update, dt, loop)