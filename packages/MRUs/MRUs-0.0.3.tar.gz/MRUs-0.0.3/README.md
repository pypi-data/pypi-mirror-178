# MRUs: Matrix Reduction Utils  
[toc]  
## LU Factorization  
```python
A = np.array([[0, 1, 1],
              [1, 1, 1],
              [1, 1, 1]], dtype=float)
L, U = lu_factorization(A)
print('A 矩阵')
print(A)
print('L 矩阵')
print(L)
print('U 矩阵')
print(U)
print('验证: LU')
print(np.dot(L, U))
```  
## QR Factorization  
```python
A = np.array([[0, -20, -14],
              [3, 27, -4],
              [4, 11, -2]], dtype=float)
Q, R = qr_factorization(A)
print('A 矩阵')
print(A)
print('Q 矩阵')
print(Q)
print('R 矩阵')
print(R)
print('验证: QR')
print(np.dot(Q, R))
```
## Orthogonal Reduction
### Householder Reduction
```python
A = np.array([[3, 2, 9],
              [4, 5, 1],
              [0, 0, 0]], dtype=float)
Q, R = orthogonal_reduction(A, core='householder')
print('A 矩阵')
print(A)
print('Q 矩阵')
print(Q)
print('R 矩阵')
print(R)
print('验证: QR')
print(np.dot(Q, R))
```  
### Givens Reduction  
```python
A = np.array([[3, 2, 9],
              [4, 5, 1],
              [0, 0, 0]], dtype=float)
Q, R = orthogonal_reduction(A, core='givens')
print('A 矩阵')
print(A)
print('Q 矩阵')
print(Q)
print('R 矩阵')
print(R)
print('验证: QR')
print(np.dot(Q, R))
```  
## URV Factorization
```python
A = np.array([[-4, -2, 4, 2],
                  [2, -2, -2, -1],
                  [-4, 1, 4, 2]], dtype=float) 
U, R, V = urv_factorization(A)
print('A矩阵')
print(A)
print('U矩阵')
print(U)
print('R矩阵')
print(R)
print('V矩阵')
print(V)
print('验证: URV^T')
print(np.dot(np.dot(U, R), V))
```  