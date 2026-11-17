# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 13:26:54 2024
"""

import numpy as np
import scipy.integrate as it
import matplotlib.pyplot as plt
import scipy.optimize as opt
from mpl_toolkits import mplot3d
from math import comb


#Task 1
print("-----Task 1-----")
def Rie_sum(f,a,b,n=10000):
    s = 0
    dx = (b-a)/n
    for i in range(n):
        s = s+ (f(a+dx*i)+f(a+dx*(i+1)))/2*dx
    return s

def Simple_f(x):
    return 2*x+1

RS = Rie_sum(Simple_f, 1,2, 10000)

print(RS)
loop =True
for i in range(1,10000):
    if np.abs(Rie_sum(Simple_f, 1, 2, i) - 4) < 1.e-8:
        print("The differnce tends to 0.")
        break
else:
    print("Something is wrong")

def speed (t):
    return np.sqrt((2*t)**2+(3*t**2)**2)

length_r = Rie_sum(speed,-2,1,10000)
length_q = it.quad(speed, -2, 1)


print (f"Solution by us is {length_r}, solution by quard is {length_q[0]}." )

#Task 2
print("\n -----Task 2-----")
def f(u):
    return 8*u[0]*u[1]-4*(u[0]**2)*u[1]-2*u[0]*(u[1]**2)+(u[0]**2)*(u[1]**2)

def neg_f(u):
    return -(8*u[0]*u[1]-4*(u[0]**2)*u[1]-2*u[0]*(u[1]**2)+(u[0]**2)*(u[1]**2))

x = np.linspace(-1,3, 1000)
y = np.linspace(-2, 5, 1000)

X,Y = np.meshgrid(x,y)

#print(X)
Z = 8*X*Y-4*(X**2)*Y-2*X*(Y**2)+(X**2)*(Y**2)


fig, ax = plt.subplots()
CS = ax.contour(X, Y, Z,np.linspace(-2,5,200))
#CS = ax.contour(X, Y, Z,200)

lmin = opt.fmin(f, np.array([0,0]),full_output= True, disp = False, retall=True)

lmax = opt.fmin(neg_f,np.array([0,0]), full_output= True, disp = False, retall=True)

#print(lmin)

if lmin[4]==0:
    print(f"local min at {lmin[0]}, and the value is {lmin[1]}.")
else:
    print("There is no local min.")


if lmax[4]==0:
    print(f"local max at {lmax[0]}, and the value is {-lmax[1]}.")
else:
    print("There is no local max.")
    
xTmin=[]
yTmin=[]
for i in range(len(lmin[5])):
    xTmin.append(lmin[5][i][0])
    yTmin.append(lmin[5][i][1])
minTrace = ax.plot(xTmin,yTmin,'m.', label = 'min')

xTmax=[]
yTmax=[]
for i in range(len(lmax[5])):
    xTmax.append(lmax[5][i][0])
    yTmax.append(lmax[5][i][1])
maxTrace = ax.plot(xTmax,yTmax,'r.', label = 'max')
plt.title(" Contour plot of $f(x,y)$")
ax.set_xlabel('$x$')
ax.set_ylabel('$y$')
plt.legend()
plt.xlim(-1, 3)
plt.ylim(-2, 5)


#Task 3
print("\n -----Task 3-----")

def z_func(x, y):
    z_solve = opt.fsolve(lambda z: x + 2*y + z + np.exp(2*z)-1, x0=np.zeros_like(x))
    return z_solve.tolist()[0]


x1_data = np.linspace(-1, 1, 100)
x2_data = np.linspace(-1, 1, 100)

X1, X2 = np.meshgrid(x1_data,x2_data)
grid_shape = X1.shape

X1 = X1.reshape(-1)
X2 = X2.reshape(-1)

position = np.dstack([X1,X2])[0]

X3 = np.array([z_func(xpos, ypos) for xpos, ypos in position])
#print (newg(0))

X1 = X1.reshape(grid_shape)
X2 = X2.reshape(grid_shape)
X3 = X3.reshape(grid_shape)

#print(z_func(0,0))
h = 1e-6
a0 = z_func(0, 0)
print(f"a0 = {a0}")
a1 = (z_func(h,0)-a0)/h
print(f"a1 = {a1}")
a2 = (z_func(0,h)-a0)/h
print(f"a2 = {a2}")
a11 = np.sum([((-1)**(i+2))*(comb(2,i))*z_func(i*h,0) for i in range(3)])/(h**2)/2
print(f"a11 = {a11}")
a12 = (z_func(h,h)-z_func(0, h)-z_func(h, 0)+a0)/(h**2)
print(f"a12 = {a12}")
a22 = np.sum([((-1)**(i+2))*(comb(2,i))*z_func(0,i*h) for i in range(3)])/(h**2)/2
print(f"a22 = {a22}")

def P2_func( x,y, a0,a1,a2,a11,a12,a22):
    return a0 + a1*x +a2*y +a11*x**2 +a12*x*y +a22*y**2

P2 = P2_func( X1,X2, a0,a1,a2,a11,a12,a22)

Er = np.abs(X3-P2)

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot_surface(X1, X2, X3, cmap="plasma")

plt.title("$z$ using fslove")
ax.set_xlabel('$x$')
ax.set_ylabel('$y$')
ax.set_zlabel('$z$')




fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot_surface(X1, X2, P2, cmap="plasma")

plt.title("$z$ using 2nd degree Taylor")
ax.set_xlabel('$x$')
ax.set_ylabel('$y$')
ax.set_zlabel('$z$')


fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot_surface(X1, X2, Er, cmap="plasma")

plt.title("Error between fsolve and Taylor")
ax.set_xlabel('$x$')
ax.set_ylabel('$y$')
ax.set_zlabel('error')













