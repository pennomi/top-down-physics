import math
import pyglet
from physics.vec3d import Vec3d

MULTIPLIER = 32


def points(plist, batch=None):
    color = (255, 0, 255)

    pyglet.gl.glPointSize(5)
    mode = pyglet.gl.GL_POINTS

    bg = pyglet.graphics.OrderedGroup(0)

    vs = [i*MULTIPLIER for sub in plist for i in sub]
    l = len(vs)//3

    if batch is None:
        pyglet.graphics.draw(l, mode,
                            ('v3f', vs),
                            ('c3B', color*l))
    else:
        batch.add(len(vs)/2, mode, bg,
                 ('v3f', vs),
                 ('c3B', color*l))


def tiles(space_map, batch=None):
    for t in space_map:
        position = t.position * MULTIPLIER

        if t.collision_type == 0:
            continue

        if t.colliding:
            color = (255, 255, 0)
        else:
            color = (255, 255, 255)

        mode = pyglet.gl.GL_TRIANGLE_STRIP

        bg = pyglet.graphics.OrderedGroup(0)

        vs = (
            position.x, position.y,
            position.x, position.y+MULTIPLIER,
            position.x+MULTIPLIER, position.y,
            position.x+MULTIPLIER, position.y+MULTIPLIER,
        )
        l = len(vs)//2

        if batch is None:
            pyglet.graphics.draw(l, mode,
                                ('v2f', vs),
                                ('c3B', color*l))
        else:
            batch.add(len(vs)/2, mode, bg,
                     ('v2f', vs),
                     ('c3B', color*l))


def circle(circle_entity, batch=None):
    center = circle_entity.position * MULTIPLIER
    radius = circle_entity.radius * MULTIPLIER

    if circle_entity.color:
        color = circle_entity.color
    elif circle_entity.colliding:
        color = (255, 0, 0)
    else:
        color = (0, 255, 0)

    num_segments = int(4 * math.sqrt(radius))
    theta = 2 * math.pi / num_segments
    c = math.cos(theta)
    s = math.sin(theta)

    x = radius
    y = 0

    ps = []

    for i in range(num_segments):
        ps += [Vec3d(center.x + x, center.y + y, 0)]
        t = x
        x = c * x - s * y
        y = s * t + c * y

    mode = pyglet.gl.GL_TRIANGLE_STRIP
    ps2 = [ps[0]]
    for i in range(1, len(ps)):
        ps2.append(ps[i])
        ps2.append(ps[-i])
    ps = ps2
    vs = []
    for p in [ps[0]] + ps + [ps[-1]]:
            vs += [p.x, p.y]

    c = center + Vec3d(radius, 0, 0).rotated_around_z(circle_entity.angle)
    cvs = [center.x, center.y, c.x, c.y]

    bg = pyglet.graphics.OrderedGroup(0)
    fg = pyglet.graphics.OrderedGroup(1)

    l = len(vs)//2

    if batch is None:
        pyglet.graphics.draw(l, mode,
                            ('v2f', vs),
                            ('c3B', color*l))
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                            ('v2f', cvs),
                            ('c3B', (0, 0, 255)*2))
    else:
        batch.add(len(vs)/2, mode, bg,
                 ('v2f', vs),
                 ('c3B', color*l))
        batch.add(2, pyglet.gl.GL_LINES, fg,
                 ('v2f', cvs),
                 ('c3B', (0, 0, 255)*2))
