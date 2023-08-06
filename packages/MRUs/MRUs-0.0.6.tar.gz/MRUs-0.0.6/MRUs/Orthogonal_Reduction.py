import numpy as np


def givens(A: np.array):
    print('givens reduction')
    R = A.copy()
    # M and N are the number of rows and columns of matrix R respectively
    M, N = R.shape
    Q = np.eye(M)
    for col in range(min(M, N) - 1):
        for row in range(col + 1, M):
            a = R[col, col]
            b = R[row, col]
            base = np.sqrt(a ** 2 + b ** 2)
            Q_tmp = np.eye(M)
            Q_tmp[row, row] = Q_tmp[col, col] = a / base
            Q_tmp[col, row] = b / base
            Q_tmp[row, col] = -b / base
            R = np.dot(Q_tmp, R)
            Q = np.dot(Q_tmp, Q)
    return Q.T, R


def householder(A: np.array):
    print('householder reduction')
    R = A.copy()
    # M and N are the number of rows and columns of matrix R respectively
    M, N = R.shape
    Q = np.eye(M)
    for col in range(min(M, N) - 1):
        Q_all = np.eye(M)
        R_j = np.array([R[col: M, col]]).T
        e1 = np.zeros_like(R_j)
        e1[[0]] = 1
        R_j = R_j - np.sqrt(np.dot(R_j.T, R_j)) * e1
        Q_tmp = np.eye(M - col) - 2 * np.dot(R_j, R_j.T) / np.dot(R_j.T, R_j)
        Q_all[col: M, col: M] = Q_tmp
        Q = np.dot(Q_all, Q)
        R = np.dot(Q_all, R)
    return Q.T, R


def orthogonal_reduction(A: np.array, core='householder'):
    print('正交分解')
    assert(core in ['householder', 'givens'])
    if core == 'householder':
        return householder(A)
    else:
        return givens(A)