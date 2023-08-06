import numpy as np
from MRUs.Orthogonal_Reduction import orthogonal_reduction


def urv_factorization(A: np.array):
    print('URV分解')
    A = A.copy()
    # M and N are the number of rows and columns of matrix A respectively
    M, N = A.shape
    A_rank = np.linalg.matrix_rank(A)
    Q_A, R_A = orthogonal_reduction(A)
    U = Q_A
    B = R_A[: A_rank]
    Q_B, R_B = orthogonal_reduction(B.T)
    R = np.zeros_like(A)
    R[: R_B.T.shape[0], : R_B.T.shape[1]] = R_B.T
    V = Q_B
    return U, R, V.T
