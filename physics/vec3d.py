"""A Cython-ready 3D Vector Object
"""

import operator
import math


class Vec3d(object):
    """3D Vector"""
    __slots__ = ['x', 'y', 'z']

    def __init__(self, x_or_triple, y=None, z=None):
        if y is None:
            self.x = x_or_triple[0]
            self.y = x_or_triple[1]
            self.z = x_or_triple[2]
        else:
            self.x = x_or_triple
            self.y = y
            self.z = z

    def __len__(self):
        return 3

    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        elif key == 2:
            return self.z
        else:
            raise IndexError("Invalid subscript " + str(key) + " to Vector3")

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        elif key == 2:
            self.z = value
        else:
            raise IndexError("Invalid subscript " + str(key) + " to Vector3")

    def __repr__(self):
        return 'Vector(%s, %s, %s)' % (self.x, self.y, self.z)

    def __eq__(self, other):
        if hasattr(other, "__getitem__") and len(other) == 3:
            return (self.x == other[0] and
                    self.y == other[1] and
                    self.z == other[2])
        else:
            return False

    def __ne__(self, other):
        if hasattr(other, "__getitem__") and len(other) == 3:
            return (self.x != other[0] or
                    self.y != other[1] or
                    self.z != other[2])
        else:
            return True

    def __bool__(self):
        return bool(self.x or self.y or self.z)

    # Generic operator handlers
    def _o2(self, other, f):
        """Any two-operator operation where the left operand is a Vector3"""
        if isinstance(other, Vec3d):
            return Vec3d(f(self.x, other.x),
                         f(self.y, other.y),
                         f(self.z, other.z))
        elif hasattr(other, "__getitem__"):
            return Vec3d(f(self.x, other[0]),
                         f(self.y, other[1]),
                         f(self.z, other[2]))
        else:
            return Vec3d(f(self.x, other),
                         f(self.y, other),
                         f(self.z, other))

    def _r_o2(self, other, f):
        """Any two-operator operation where the right operand is a Vector3"""
        if hasattr(other, "__getitem__"):
            return Vec3d(f(other[0], self.x),
                         f(other[1], self.y),
                         f(other[2], self.z))
        else:
            return Vec3d(f(other, self.x),
                         f(other, self.y),
                         f(other, self.z))

    def _io(self, other, f):
        """inplace operator"""
        if hasattr(other, "__getitem__"):
            self.x = f(self.x, other[0])
            self.y = f(self.y, other[1])
            self.z = f(self.z, other[2])
        else:
            self.x = f(self.x, other)
            self.y = f(self.y, other)
            self.z = f(self.z, other)
        return self

    # Addition
    def __add__(self, other):
        if isinstance(other, Vec3d):
            return Vec3d(self.x + other.x,
                         self.y + other.y,
                         self.z + other.z)
        elif hasattr(other, "__getitem__"):
            return Vec3d(self.x + other[0],
                         self.y + other[1],
                         self.z + other[2])
        else:
            return Vec3d(self.x + other, self.y + other, self.z + other)

    __radd__ = __add__

    def __iadd__(self, other):
        if isinstance(other, Vec3d):
            self.x += other.x
            self.y += other.y
            self.z += other.z
        elif hasattr(other, "__getitem__"):
            self.x += other[0]
            self.y += other[1]
            self.z += other[2]
        else:
            self.x += other
            self.y += other
            self.z += other
        return self

    # Subtraction
    def __sub__(self, other):
        if isinstance(other, Vec3d):
            return Vec3d(self.x - other.x,
                         self.y - other.y,
                         self.z - other.z)
        elif hasattr(other, "__getitem__"):
            return Vec3d(self.x - other[0],
                         self.y - other[1],
                         self.z - other[2])
        else:
            return Vec3d(self.x - other, self.y - other, self.z - other)

    def __rsub__(self, other):
        if isinstance(other, Vec3d):
            return Vec3d(other.x - self.x,
                         other.y - self.y,
                         other.z - self.z)
        if hasattr(other, "__getitem__"):
            return Vec3d(other[0] - self.x,
                         other[1] - self.y,
                         other[2] - self.z)
        else:
            return Vec3d(other - self.x, other - self.y, other - self.z)

    def __isub__(self, other):
        if isinstance(other, Vec3d):
            self.x -= other.x
            self.y -= other.y
            self.z -= other.z
        elif hasattr(other, "__getitem__"):
            self.x -= other[0]
            self.y -= other[1]
            self.z -= other[2]
        else:
            self.x -= other
            self.y -= other
            self.z -= other
        return self

    # Multiplication
    def __mul__(self, other):
        if isinstance(other, Vec3d):
            return Vec3d(self.x * other.x, self.y * other.y, self.z * other.z)
        if hasattr(other, "__getitem__"):
            return Vec3d(self.x * other[0], self.y * other[1],
                         self.z * other[2])
        else:
            return Vec3d(self.x * other, self.y * other, self.z * other)

    __rmul__ = __mul__

    def __imul__(self, other):
        if isinstance(other, Vec3d):
            self.x *= other.x
            self.y *= other.y
            self.z *= other.z
        elif hasattr(other, "__getitem__"):
            self.x *= other[0]
            self.y *= other[1]
            self.z *= other[2]
        else:
            self.x *= other
            self.y *= other
            self.z *= other
        return self

    # Division
    def __floordiv__(self, other):
        return self._o2(other, operator.floordiv)

    def __rfloordiv__(self, other):
        return self._r_o2(other, operator.floordiv)

    def __ifloordiv__(self, other):
        return self._io(other, operator.floordiv)

    def __truediv__(self, other):
        return self._o2(other, operator.truediv)

    def __rtruediv__(self, other):
        return self._r_o2(other, operator.truediv)

    def __itruediv__(self, other):
        return self._io(other, operator.floordiv)

    # Modulo
    def __mod__(self, other):
        return self._o2(other, operator.mod)

    def __rmod__(self, other):
        return self._r_o2(other, operator.mod)

    # Exponentiation
    def __pow__(self, other):
        return self._o2(other, operator.pow)

    def __rpow__(self, other):
        return self._r_o2(other, operator.pow)

    # Bitwise operators
    def __lshift__(self, other):
        return self._o2(other, operator.lshift)

    def __rlshift__(self, other):
        return self._r_o2(other, operator.lshift)

    def __rshift__(self, other):
        return self._o2(other, operator.rshift)

    def __rrshift__(self, other):
        return self._r_o2(other, operator.rshift)

    def __and__(self, other):
        return self._o2(other, operator.and_)
    __rand__ = __and__

    def __or__(self, other):
        return self._o2(other, operator.or_)
    __ror__ = __or__

    def __xor__(self, other):
        return self._o2(other, operator.xor)
    __rxor__ = __xor__

    def __neg__(self):
        return Vec3d(operator.neg(self.x),
                     operator.neg(self.y),
                     operator.neg(self.z))

    def __pos__(self):
        return Vec3d(operator.pos(self.x),
                     operator.pos(self.y),
                     operator.pos(self.z))

    def __abs__(self):
        return Vec3d(abs(self.x), abs(self.y), abs(self.z))

    def __invert__(self):
        return Vec3d(-self.x, -self.y, -self.z)

    # vector functions
    def get_length_sq(self):
        return self.x ** 2 + self.y ** 2 + self.z ** 2

    @property
    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    @length.setter
    def length(self, value):
        try:
            length = self.length
            self.x *= value / length
            self.y *= value / length
            self.z *= value / length
        except ZeroDivisionError as e:
            raise ValueError("Can't set length on a zero vector.") from e

    def rotate_around_z(self, angle_degrees, anchor=None):
        if anchor is not None:
            self -= anchor

        radians = math.radians(angle_degrees)
        cos = math.cos(radians)
        sin = math.sin(radians)
        x = self.x * cos - self.y * sin
        y = self.x * sin + self.y * cos
        self.x = x
        self.y = y

        if anchor is not None:
            self += anchor

    def rotate_around_x(self, angle_degrees):
        radians = math.radians(angle_degrees)
        cos = math.cos(radians)
        sin = math.sin(radians)
        y = self.y * cos - self.z * sin
        z = self.y * sin + self.z * cos
        self.y = y
        self.z = z

    def rotate_around_y(self, angle_degrees):
        radians = math.radians(angle_degrees)
        cos = math.cos(radians)
        sin = math.sin(radians)
        z = self.z * cos - self.x * sin
        x = self.z * sin + self.x * cos
        self.z = z
        self.x = x

    def rotated_around_z(self, angle_degrees):
        radians = math.radians(angle_degrees)
        cos = math.cos(radians)
        sin = math.sin(radians)
        x = self.x * cos - self.y * sin
        y = self.x * sin + self.y * cos
        return Vec3d(x, y, self.z)

    def rotated_around_x(self, angle_degrees):
        radians = math.radians(angle_degrees)
        cos = math.cos(radians)
        sin = math.sin(radians)
        y = self.y * cos - self.z * sin
        z = self.y * sin + self.z * cos
        return Vec3d(self.x, y, z)

    def rotated_around_y(self, angle_degrees):
        radians = math.radians(angle_degrees)
        cos = math.cos(radians)
        sin = math.sin(radians)
        z = self.z * cos - self.x * sin
        x = self.z * sin + self.x * cos
        return Vec3d(x, self.y, z)

    @property
    def angle_around_z(self):
        if self.get_length_sq() == 0:
            return 0
        return math.degrees(math.atan2(self.y, self.x))

    @angle_around_z.setter
    def angle_around_z(self, angle_degrees):
        self.x = math.sqrt(self.x ** 2 + self.y ** 2)
        self.y = 0
        self.rotate_around_z(angle_degrees)

    @property
    def angle_around_x(self):
        if self.get_length_sq() == 0:
            return 0
        return math.degrees(math.atan2(self.z, self.y))

    @angle_around_x.setter
    def angle_around_x(self, angle_degrees):
        self.y = math.sqrt(self.y ** 2 + self.z ** 2)
        self.z = 0
        self.rotate_around_x(angle_degrees)

    @property
    def angle_around_y(self):
        if self.get_length_sq() == 0:
            return 0
        return math.degrees(math.atan2(self.x, self.z))

    @angle_around_y.setter
    def angle_around_y(self, angle_degrees):
        self.z = math.sqrt(self.z ** 2 + self.x ** 2)
        self.x = 0
        self.rotate_around_y(angle_degrees)

    def get_angle_between(self, other):
        v1 = self.normalized()
        v2 = Vec3d(other)
        v2.normalize_return_length()
        return math.degrees(math.acos(v1.dot(v2)))

    def normalized(self):
        length = self.length
        if length != 0:
            return self / length
        return Vec3d(self)

    def normalize_return_length(self):
        length = self.length
        if length != 0:
            self.x /= length
            self.y /= length
            self.z /= length
        return length

    def dot(self, other):
        return float(self.x * other[0] + self.y * other[1] + self.z * other[2])

    def distance(self, other):
        return math.sqrt((self.x - other[0]) ** 2 +
                         (self.y - other[1]) ** 2 +
                         (self.z - other[2]) ** 2)

    def distance_sq(self, other):
        return ((self.x - other[0]) ** 2 +
                (self.y - other[1]) ** 2 +
                (self.z - other[2]) ** 2)

    def projection(self, other):
        other_length_sq = (other[0] * other[0] +
                           other[1] * other[1] +
                           other[2] * other[2])
        return other * (self.dot(other) / other_length_sq)

    def cross(self, other):
        """Return the cross product"""
        return Vec3d(self.y * other[2] - self.z * other[1],
                     self.z * other[0] - self.x * other[2],
                     self.x * other[1] - self.y * other[0])

    def interpolate_to(self, other, _range):
        return Vec3d(self.x + (other[0] - self.x) * _range,
                     self.y + (other[1] - self.y) * _range,
                     self.z + (other[2] - self.z) * _range)

    def convert_to_basis(self, x_vector, y_vector, z_vector):
        return Vec3d(
            self.dot(x_vector) / x_vector.get_length_sq(),
            self.dot(y_vector) / y_vector.get_length_sq(),
            self.dot(z_vector) / z_vector.get_length_sq())

    def __getstate__(self):
        return [self.x, self.y, self.z]

    def __setstate__(self, dictionary):
        self.x, self.y, self.z = dictionary

# ##########################################################################
## Unit Testing                                                          ##
###########################################################################
if __name__ == "__main__":
    import unittest
    import pickle

    class UnitTestVec3d(unittest.TestCase):
        """Execute the test runner."""

        def test_creation_and_access(self):
            """Test instance creation"""
            v = Vec3d(111, 222, 333)
            self.assert_(v.x == 111 and v.y == 222 and v.z == 333)
            v.x = 333
            v[1] = 444
            v.z = 555
            self.assert_(v[0] == 333 and v[1] == 444 and v[2] == 555)

        def test_math(self):
            """Test math operations"""
            v = Vec3d(111, 222, 333)
            self.assertEqual(v + 1, Vec3d(112, 223, 334))
            self.assert_(v - 2 == [109, 220, 331])
            self.assert_(v * 3 == (333, 666, 999))
            self.assert_(v / 2.0 == Vec3d(55.5, 111, 166.5))
            self.assert_(v / 2 == (55, 111, 166))
            self.assert_(v ** Vec3d(2, 3, 2) == [12321, 10941048, 110889])
            self.assert_(v + [-11, 78, 67] == Vec3d(100, 300, 400))
            self.assert_(v / [11, 2, 9] == [10, 111, 37])

        def test_reverse_math(self):
            """Test reverse math"""
            v = Vec3d(111, 222, 333)
            self.assert_(1 + v == Vec3d(112, 223, 334))
            self.assert_(2 - v == [-109, -220, -331])
            self.assert_(3 * v == (333, 666, 999))
            self.assert_([222, 999, 666] / v == [2, 4, 2])
            self.assert_([111, 222, 333] ** Vec3d(2, 3, 2) ==
                         [12321, 10941048, 110889])
            self.assert_([-11, 78, 67] + v == Vec3d(100, 300, 400))

        def test_unary(self):
            """Test Unary operations"""
            v = Vec3d(111, 222, 333)
            v = -v
            self.assert_(v == [-111, -222, -333])
            v = abs(v)
            self.assert_(v == [111, 222, 333])

        def test_length(self):
            """Test length measurements"""
            v = Vec3d(1, 4, 8)
            self.assert_(v.length == 9)
            self.assert_(v.get_length_sq() == 81)
            self.assert_(v.normalize_return_length() == 9)
            self.assert_(v.length == 1)
            v.length = 9
            self.assert_(v == Vec3d(1, 4, 8))
            v2 = Vec3d(10, -2, 12)
            self.assert_(v.distance(v2) == (v - v2).length)

        def test_angles(self):
            """Test angles and rotation"""
            v = Vec3d(0, 3, -3)
            self.assertEquals(v.angle_around_y, 180)
            self.assertEquals(v.angle_around_x, -45)
            self.assertEquals(v.angle_around_z, 90)

            v2 = Vec3d(v)
            v.rotate_around_x(-90)
            self.assertEqual(v.get_angle_between(v2), 90)

            v = Vec3d(v2)
            v.rotate_around_y(-90)
            self.assertAlmostEqual(v.get_angle_between(v2), 60)

            v = Vec3d(v2)
            v.rotate_around_z(-90)
            self.assertAlmostEqual(v.get_angle_between(v2), 60)

            v2.angle_around_z -= 90
            self.assertEqual(v.length, v2.length)
            self.assertEquals(v2.angle_around_z, 0)
            self.assertEqual(v2, [3, 0, -3])
            self.assert_((v - v2).length < .00001)
            self.assertEqual(v.length, v2.length)
            v2.rotate_around_y(300)
            self.assertAlmostEquals(v.get_angle_between(v2), 60)
            v2.rotate_around_y(v2.get_angle_between(v))
            self.assertAlmostEquals(v.get_angle_between(v2), 0)

        def test_high_level(self):
            """Test High Level stuff"""
            basis0 = Vec3d(5.0, 0, 0)
            basis1 = Vec3d(0, .5, 0)
            basis2 = Vec3d(0, 0, 3)
            v = Vec3d(10, 1, 6)
            self.assert_(v.convert_to_basis(basis0, basis1, basis2) ==
                         [2, 2, 2])
            self.assert_(v.projection(basis0) == (10, 0, 0))
            self.assert_(basis0.dot(basis1) == 0)

        def test_cross(self):
            """Test cross product"""
            lhs = Vec3d(1, .5, 3)
            rhs = Vec3d(4, 6, 1)
            self.assert_(lhs.cross(rhs) == [-17.5, 11, 4])

        def test_comparison(self):
            """Test all comparisons"""
            int_vec = Vec3d(3, -2, 4)
            flt_vec = Vec3d(3.0, -2.0, 4.0)
            zero_vec = Vec3d(0, 0, 0)
            self.assert_(int_vec == flt_vec)
            self.assert_(int_vec != zero_vec)
            self.assert_(not (flt_vec == zero_vec))
            self.assert_(not (flt_vec != int_vec))
            self.assert_(int_vec == (3, -2, 4))
            self.assert_(int_vec != [0, 0, 0])
            self.assert_(int_vec != 5)
            self.assert_(int_vec != [3, -2, 4, 15])

        def test_inplace(self):
            """Test in-place functions"""
            inplace_vec = Vec3d(5, 13, 17)
            inplace_ref = inplace_vec
            inplace_src = Vec3d(inplace_vec)
            inplace_vec *= .5
            inplace_vec += .5
            inplace_vec /= (3, 6, 9)
            inplace_vec += Vec3d(-1, -1, -1)
            alternate = (inplace_src * .5 + .5) / Vec3d(3, 6, 9) + [-1, -1,
                                                                    -1]
            self.assertEquals(inplace_vec, inplace_ref)
            self.assertEquals(inplace_vec, alternate)

        def test_pickle(self):
            """Test Pickling and Unpickling"""
            vec = Vec3d(5, .3, 8.6)
            vec_str = pickle.dumps(vec)
            loaded_vec = pickle.loads(vec_str)
            self.assertEquals(vec, loaded_vec)

    unittest.main()
