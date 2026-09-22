import math

class Vectors():
    def dotproduct(v1, v2):
        return v1[0] * v2[0] + v1[1] * v2[1]

    def crossproduct(v1, v2):
        return v1[0] * v2[1] - v1[1] * v2[0]

    def magnitude(v):
        return math.sqrt(v[0]**2 + v[1]**2)

    def scalar_vector_multiplication(v, c):
        # multiply a vector v by a scalar c
        return [c * v[0], c * v[1]]

    def return_perpendicular(v):
        # multiply by a rotation matrix of 90 degrees cw (- pi / 2)
        return Vectors.matrix_vector_multiplication(v, [[0, 1], [-1, 0]])

    def matrix_vector_multiplication(v, mx):
        # takes in a 2 component vector and a 2x2 matrix
        # 2x2 matrix is in the form [v1, v2] where v1 and v2 are vectors
        return [mx[0][0] * v[0] + mx[1][0] * v[1], mx[0][1] * v[0] + mx[1][1] * v[1]]

    def return_transverse(mx):
        # takes in a 2x2 matrix and gets its transverse (which for orthonormal matrices is its inverse)
        return [[mx[0][0], mx[1][0]], [mx[0][1], mx[1][1]]]