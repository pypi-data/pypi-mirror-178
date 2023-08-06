import numpy as np


def qr_factorization(A: np.array):
    print('QR分解')
    A = A.copy()
    # M and N are the number of rows and columns of matrix A respectively
    M, N = A.shape
    Q = np.empty_like(A)
    R = np.zeros((M, M))
    Q_cnt = 0
    for col in range(N):
        ui = A[:, [col]]
        for col_Q in range(0, Q_cnt):
            u_pre = Q[:, [col_Q]]
            inner_product = np.dot(u_pre.T, ui)
            R[col_Q, col] = inner_product
            ui = ui - u_pre*inner_product
        ui_norm = np.sqrt(np.dot(ui.T, ui))
        R[col, col] = ui_norm
        ui = ui / ui_norm
        Q[:, [col]] = ui
        Q_cnt += 1
    return Q, R    
        