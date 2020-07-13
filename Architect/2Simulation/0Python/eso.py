import numpy as np
import matplotlib.pyplot as plt

#runge-kutta
def dxdt(F, X, t, h=1e-2):
    assert(len(F)==len(X))
    X = np.array(X)
    K1 = np.array([f(X, t) for f in F])
    dX = h*K1/2
    K2 = np.array([f(X+dX, t+h/2) for f in F]) 
    dX = h*K2/2
    K3 = np.array([f(X+dX, t+h/2) for f in F])
    dX = h*K3 
    K4 = np.array([f(X+dX, t+h) for f in F])
    dX = (K1 + 2*K2 + 2*K3 + K4)*h/6

    return dX, np.array([f(X, t) for f in F])

#calcute function trajectory
def trajectory(F, initial_point, num_points=1e4, h=1e-2):
    assert(len(F)==len(initial_point))
    #initialize n*dim array.
    n = int(num_points)
    dim = len(initial_point)
    X = np.zeros([n,dim])
    D = np.zeros([n,dim])
    #set col 0 as initial point
    X[0,:] = initial_point
    #
    for k in range(1,n):
        dX, D[k-1,:] = dxdt(F,X[k-1,:],h*(k-1),h)
        X[k,:] = X[k-1,:] + dX
        
    return X.T, D.T


def f1(X, t):
    x, y = X[0], X[1]
    return y

def f2(X, t):
    x, y = X[0], X[1]
    return -x*x*x - x -0.2*y + v(t)

def v(t):
    return 0.5 * np.sign(np.cos(t/2))

# Orange trajectory
h = 1e-2
N = 2000
x,d = trajectory([f1,f2],(0,0),N,h)
# fig = plt.figure()
# plt.plot(x[0], color='red', label='original')
# plt.plot(x[1], color='blue', label='1st order')
# plt.plot(d[1], color='black', label='2nd order')
# plt.legend()
# plt.show()

#Tracking trajectory
v0 = x[0]

def v(t):
    return v0[int(t/h)]

# 极点配置
p = np.poly1d([-15,-15,-15],True)
_, b1, b2, b3 = tuple(p.coef)


def g1(X, t):
    x1,x2,x3 = X[0], X[1], X[2]
    return x2 - b1 * nle(x1 - v(t))

def g2(X, t):
    x1, x2, x3 = X[0], X[1], X[2]
    return x3 - b2 * nle(x1 - v(t))

def g3(X, t):
    x1, x2, x3 = X[0], X[1], X[2]
    return -b3 * nle(x1 - v(t))

# 论文中使用非线性误差，这里实验用线性的
def nle(e):
    # nonlinear error
    # return  np.sign(e)*np.sqrt(np.abs(e))
    return e

N = 2000
z,_ = trajectory([g1,g2,g3],(0,0,0),N,h)
fig = plt.figure()
plt.plot(z[0], color='red', label='tracking',ls = '--')
plt.plot(z[1], color='blue', label='1st order',ls = '--')
plt.plot(z[2], color='black', label='2nd order',ls = '--')

plt.plot(x[0], color='red', label='original',ls = '-')
plt.plot(x[1], color='blue', label='1st order',ls = '-')
plt.plot(d[1], color='black', label='2nd order',ls = '-')
plt.legend()
plt.show()

