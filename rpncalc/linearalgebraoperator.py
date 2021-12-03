import numpy
import math
from rpncalc.util import ActionEnum, stack


class LinearAlgebraOperator(ActionEnum):

    to_vec2 = 'vec2', \
        "Pop two values and merge into a vector"
    to_vec3 = 'vec3', \
        "Pop three values and merge into a vector"
    to_vec_all = 'veca', \
        "Pop entire stack and merge into a vector"
    to_vecn = 'vecn', \
        "Pop prior value as 'n' before " \
        "popping n values into a vector"
    dotproduct = 'dot'
    crossproduct = 'cross'
    to_mat2 = 'mat2', \
        "Pop four values and make 2x2 matrix"
    to_mat3 = 'mat3', \
        "Pop 9 values and make 3x3 matrix"
    to_matsq = 'matsq', \
        "Pop stack to square matrix." \
        " Errors if non-square length of items"
    to_matmn = 'matmn', \
        "Pop two values for row m and col n" \
        " and then pop m*n values and return matrix." \
        " Ex. '1 2 3 4 5 6 3 2 matmn' gives" \
        " array([[1,2],[3,4],[5,6]])"

    determinant = 'det', "Determinant of matrix"
    inverse = 'inv', "Inverse of matrix"
    transpose = 'T', "Matrix Transpose"

    unit_vec_x = 'e_x', "Pushes vec3(1,0,0) to stack"
    unit_vec_y = 'e_y', "Pushes vec3(0,1,0) to stack"
    unit_vec_z = 'e_z', "Pushes vec3(0,0,1) to stack"

    hstack = 'hstack', "Stack vectors horizontally" \
        "Ex. '1, 2 vec2 3 4 vec2 hstack' gives array([1,2,3,4])"
    vstack = 'vstack', "Stack vectors vertically" \
        "Ex. '1, 2 vec2 3 4 vec2 vstack' gives array([[1,2][3,4]])"

    repeat = 'repeat'
    reshape = 'reshape'

    normalize = 'normalize', "normalize item on top of stack"
    norm = 'norm', "norm of value, vector or matrix on top of stack"

    to_stack = 'to_stack', "flattens numpy object with numpy.flat" \
        ", and places on stack"

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
                size = math.sqrt(self.stack_size())
                if size.is_integer():
                    size = int(size)
                    r = self._to_mat_mn(size, size)
                else:
                    msg = f"Stack of len {len(stack)} is not square"
                    raise ValueError(msg)
            case o.to_matmn:
                N, M = self.take_2()
                r = self._to_mat_mn(M, N)

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
                repeats, item = self.take_2()
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

            case o.to_stack:
                item = self.take_1()
                r = []
                for i in item.flat:  # 1D iterator for numpy objs
                    r.append(i)

            case _:
                msg = f"Missing case match for {self}"
                raise NotImplementedError(msg)

        self.push(r)
