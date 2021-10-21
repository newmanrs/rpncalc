import numpy
import math
from rpncalc.util import ActionEnum


class LinearAlgebraOperator(ActionEnum):

    to_vec2 = 'vec2'
    to_vec3 = 'vec3'
    to_vec_all = 'veca'
    to_vecn = 'vecn'
    dotproduct = 'dot'
    crossproduct = 'cross'
    to_mat2 = 'mat2'
    to_mat3 = 'mat3'
    to_matsq = 'matsq'
    to_matmn = 'matmn'
    determinant = 'det'
    inverse = 'inv'
    transpose = 'T'

    unit_vec_x = 'e_x'
    unit_vec_y = 'e_y'
    unit_vec_z = 'e_z'

    hstack = 'hstack'
    vstack = 'vstack'
    repeat = 'repeat'
    reshape = 'reshape'

    normalize = 'normalize'
    norm = 'norm'

    def _to_vec_n(self, n):
        return numpy.flip(self.take_n(n))

    def _to_vec_all(self):
        return numpy.flip(self.take_all())

    def _to_mat_mn(self, m, n):
        return numpy.flip(self.take_n(m*n)).reshape((m, n))

    def action(self):

        o = type(self)
        match self:

            case o.to_vec2:
                r = self._to_vec_n(2)
            case o.to_vec3:
                r = self._to_vec_n(3)
            case o.to_vecn:
                n = self.take_1()
                r = self._to_vec_n(n)
            case o.to_vec_all:
                r = self._to_vec_all()
            case o.dotproduct:
                v1, v0 = self.take_2()
                r = numpy.dot(v0, v1)
            case o.crossproduct:
                v1, v0 = self.take_2()
                r = numpy.cross(v0, v1)
            case o.to_mat2:
                r = self._to_mat_mn(2, 2)
            case o.to_mat3:
                r = self._to_mat_mn(3, 3)
            case o.to_matsq:
                size = math.sqrt(len())
                if size.is_integer():
                    size = int(size)
                    r = self._to_mat_mn(size, size, stack)
                else:
                    msg = f"Stack of len {len()} is not square"
                    raise ValueError(msg)
            case o.to_matmn:
                M, N = self.take_2()
                r = self._to_mat_mn(M, N, stack)

            case o.inverse:
                r = numpy.linalg.inv(self.take_1())

            case o.determinant:
                mat = self.take_1()
                r = numpy.linalg.det(mat)

            case o.transpose:
                mat = self.take_1()
                r = numpy.transpose(mat)

            case o.unit_vec_x:
                r = numpy.asarray((1, 0, 0))

            case o.unit_vec_y:
                r = numpy.asarray((0, 1, 0))

            case o.unit_vec_z:
                r = numpy.asarray((0, 0, 1))

            case o.hstack:
                j, i = self.take_2()
                r = numpy.hstack((i, j))

            case o.vstack:
                j, i = self.take_2()
                r = numpy.vstack((i, j))

            case o.repeat:
                repeats,item = self.take_2()
                r = numpy.repeat(item, repeats)

            case o.reshape:
                N, M, item = self.take_3()
                r = item.reshape(M, N)

            case o.normalize:
                item = self.take_1()
                r = item / numpy.linalg.norm(item)
            case o.norm:
                item = self.take_1()
                r = numpy.linalg.norm(item)

            case _:
                msg = f"Missing case match for {self}"
                raise NotImplementedError(msg)

        self.push(r)
