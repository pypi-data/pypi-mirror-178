import numpy as np


class LinearAlgebra :
    """ This class performs basic calculations and transforms of linear algebra

    Attributes:
        init_matrix(numpy array) representing the initially given matrix
        init_vector(numpy array) representing the initially given vector

    """

    def __init__(self, matrix_one = None, vector_one = None):
        self.matrix_one = matrix_one
        self.vector_one = vector_one


    def scalar_multiply_matrix(self, scalar):
        """ Method to perform scalar multiplication of a matrix  with a scalar

        Args:
          scalar(int, float) : scalar to multiply the matrix with

        Returns:
          numpy : the matrix multiplied by the scalar value

        """
        return scalar*self.matrix_one


    def scalar_multiply_vector(self, scalar):
        """ Method to perform scalar multiplication of a vector  with a scalar

        Args:
          scalar(int, float) : scalar to multiply the vector with

        Returns:
          numpy : the vector multiplied by the scalar value

        """
        return scalar*self.vector_one


    def matrix_multiplication(self, matrix_two):
        """ Method to perform matrix multiplication

        Args:
            matrix_two(numpy) : the matrix to multiply with the initial given matrix

        Returns:
            numpy : the product of the two matrices

        """
        return np.matmul(self.matrix_one, matrix_two)


    def calculate_magnitude(self, arr):
        """ Method to calculate the magnitude of a vector/matrix

        """
        return np.linalg.norm(arr)




