from physics.vec3d import Vec3d
from physics import debug_draw
from itertools import combinations, product


class Entity:
    def __init__(self, position=None, angle=0.0, radius=0.5, mass=float('inf')):
        if position is None:
            position = Vec3d(0, 0, 0)
        self.position = position
        self.angle = angle
        self.radius = radius
        self.mass = mass
        self.movement_velocity = Vec3d(0, 0, 0)

        # Special Variables to persist state
        self.colliding = False

    def collides_with(self, other: 'Entity'):
        d = self.position.distance(other.position)
        return self.radius + other.radius >= d


def intersects(entity: Entity, tile_coords) -> bool:
    # TODO: Maybe using only the closest vertex would be faster!
    # FIXME: This logic was incorrect for the segment intersecting the circle
    tile_coords = Vec3d(tile_coords)
    verts = [tile_coords, tile_coords + Vec3d(1, 0, 0),
             tile_coords + Vec3d(1, 1, 0), tile_coords + Vec3d(0, 1, 0)]
    p = entity.position
    return any((
        does_segment_intersect_circle(verts[0], verts[1], p, entity.radius),
        does_segment_intersect_circle(verts[1], verts[2], p, entity.radius),
        does_segment_intersect_circle(verts[2], verts[3], p, entity.radius),
        does_segment_intersect_circle(verts[3], verts[0], p, entity.radius),
    ))


def closest_point_on_seg(seg_a, seg_b, circ_pos):
    seg_v = seg_b - seg_a
    pt_v = circ_pos - seg_a
    seg_v_unit = seg_v.normalized()
    projection = pt_v.dot(seg_v_unit)
    if projection <= 0:
        return Vec3d(seg_a)  # copy
    if projection >= seg_v.length:
        return Vec3d(seg_b)  # copy
    return seg_v_unit * projection + seg_a


def does_segment_intersect_circle(seg_a, seg_b, circ_pos, circ_rad):
    closest = closest_point_on_seg(seg_a, seg_b, circ_pos)
    distance = (circ_pos - closest).length
    if distance > circ_rad:
        return False
    return True


class Tile:
    def __init__(self, x: int, y: int, collision_type=0):
        self.collision_type = collision_type
        self.position = Vec3d(x, y, 0)

        # temporary state (please don't set these)
        self.colliding = False

    def __str__(self):
        return "<Tile @ ({}, {})>".format(self.position.x, self.position.y)

    def __repr__(self):
        return str(self)


class Space:
    def __init__(self):
        self._entities = []
        self._tiles = []
        self.points_to_render = []

    def add(self, entity: Entity):
        # noinspection PyTypeChecker
        self._entities.append(entity)

    def collision_tiles_for_entity(self, e: Entity) -> list:
        r = e.radius
        x_values = range(int(e.position.x - r), int(e.position.x + r) + 1)
        y_values = range(int(e.position.y - r), int(e.position.y + r) + 1)
        matches = set()
        for h in product(x_values, y_values):
            h = h + (0,)
            # hard match... a corner may actually not be a hit
            for t in self._tiles:
                if (t.collision_type and t.position == Vec3d(h) and
                        intersects(e, h)):
                    matches.add(t)
                    t.colliding = True
        return matches

    def debug_draw(self):
        debug_draw.tiles(self._tiles)
        for e in self._entities:
            debug_draw.circle(e)
        debug_draw.points(self.points_to_render)

    def update(self, dt):
        for t in self._tiles:
            t.colliding = False
        for e in self._entities:
            # reset state
            e.colliding = False

            # Do the pre-movement (no Continuous Collision Detection... yet)
            e.position += e.movement_velocity * dt

        # Collisions for entities
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
            d = a.position.distance(b.position)
            penetration = a.radius + b.radius - d

            # apply movement to the objects to push them away the proper amount
            direction = (a.position - b.position).normalized()

            # TODO: infinite mass
            ratio_a = a.mass / (a.mass + b.mass)
            ratio_b = b.mass / (a.mass + b.mass)
            a.position += direction * (penetration * ratio_b)
            b.position -= direction * (penetration * ratio_a)

        # Now do collisions for walls
        # TODO: This gets stuck in the space between the walls
        self.points_to_render = []
        for e in self._entities:
            collisions = self.collision_tiles_for_entity(e)
            for tile in collisions:
                tile_p = tile.position
                verts = [tile_p, tile_p + Vec3d(1, 0, 0),
                         tile_p + Vec3d(1, 1, 0), tile_p + Vec3d(0, 1, 0)]
                c1 = closest_point_on_seg(verts[0], verts[1], e.position)
                c2 = closest_point_on_seg(verts[1], verts[2], e.position)
                c3 = closest_point_on_seg(verts[2], verts[3], e.position)
                c4 = closest_point_on_seg(verts[3], verts[0], e.position)
                closest = sorted([c1, c2, c3, c4],
                                 key=lambda x: (x-e.position).length)
                self.points_to_render.append(closest[0])
                penetration_v = e.position - closest[0]
                target_length = e.radius - penetration_v.length
                if target_length:
                    penetration_v.length = target_length
                    penetration = penetration_v.length
                    if penetration < e.radius:
                        e.position += penetration_v
