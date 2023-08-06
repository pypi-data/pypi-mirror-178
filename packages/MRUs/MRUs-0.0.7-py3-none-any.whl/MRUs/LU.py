import numpy as np
from MRUs.Eelementary_Row_Operations import *


def lu_factorization(A: np.array):
    print('LU分解')
    A = A.copy()
    # M and N are the number of rows and columns of matrix A respectively
    M, N = A.shape
    L_inverse = np.eye(M)
    
    for col in range(N):
        for row in range(col+1, M):
            P = np.eye(M)
            if A[row, col] == 0:
                continue
            elif A[col, col] == 0:
                operator_1(A, col, row)
                operator_1(P, col, row)
                L_inverse = np.dot(P, L_inverse)
                continue
            else:
                w_tmp = -A[row, col] / A[col, col]
                operator_3(A, row, col, w_tmp)
                operator_3(P, row, col, w_tmp)
                L_inverse = np.dot(P, L_inverse)
    
    return np.linalg.inv(L_inverse), A