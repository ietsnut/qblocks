import numpy as np
import sys, random

isq2 = 1.0/(2.0**0.5)

class state:
  def __init__(self, n):
    self.n = n
    self.state = np.zeros(2**self.n, dtype=np.complex)
    self.state[0] = 1
    self.matrix = []
    for i in range(1<<n):
      s=bin(i)[2:]
      s='0'*(n-len(s))+s
      self.matrix.append(list(s))

  def op(self, t, i):
    eyeL = np.eye(2**i, dtype=np.complex)
    eyeR = np.eye(2**(self.n - i - int(t.shape[0]**0.5)), 
        dtype = np.complex)
    t_all = np.kron(np.kron(eyeL, t), eyeR)
    self.state = np.matmul(t_all, self.state)

  def h(self, i):
    h_matrix = isq2 * np.array([
        [1,1],
        [1,-1]
    ])
    self.op(h_matrix, i)

  def t(self, i):
    t_matrix = np.array([
        [1,0],
        [0,isq2 + isq2 * 1j]
    ])
    self.op(t_matrix, i)

  def s(self, i):
    s_matrix = np.array([
        [1,0],
        [0,0+1j]
    ])
    self.op(s_matrix,i)

  def cnot(self, i):
    cnot_matrix = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0]
    ])
    self.op(cnot_matrix, i)

  def swap(self, i):
    swap_matrix = np.array([
        [1, 0, 0, 0],
        [0, 0, 1, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1]
    ])
    self.op(swap_matrix, i)

  def x(self, i):
    x_matrix = np.array([
        [0,1],
        [1,0]
    ])
    self.op(x_matrix, i)
