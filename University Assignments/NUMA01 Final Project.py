import numpy as np
import matplotlib.pyplot as plt

m=0.6
rho=1.23
Cd=0.45
d=0.24
g=-9.81

def Fd(velocity):
    """Formula for air resistance
    """
    return 1/2*rho*Cd*np.pi/4*d**2*velocity**2


def EulerMethod(f, T, N, y0):
    """The standard EulerMethod for solving the differential equation y'=f(t, y).
    
    Parameters (4):
        f - function described above
        T - time boundary
        N - amount of iterations
        y0 - intial value of the function
        
    Outputs:
        returns y as an np array
        y - the list representing y in the description above
    """
    dt=T/N
    tl=np.linspace(0, T, int(N))
    y=[y0]
    for i in range(1, int(N)):
        y.append(y[-1]+dt*f(tl[i], y[-1]))
    return np.array(y) 


def speedandpos(time_guess, alpha_guess, stepspersec, velocity, x0, y0):
    """A function for setting up the correct enviroment for the EulerMethod, it defines functions that the EulerMethod can take in.
   Firstly it solves the initial value problem for velocity since acceleratin is a well-defined function of velocity. Then it uses
   the obtained list of velocity to numerically calculate the position for this given trajectory.
    
    Parameters (6):
        time_guess - the time boundary, for how long the simulation will run
        alpha_guess - initial angular direction guess
        stepspersec - number of iterations per second simulated
        velocity - initial total velocity
        x0 - starting right-left position
        y0 - starting height
        
    Outputs:
        returns Vylist, Vxlist, Ylist, Xlist
        Vylist - the list of all Y-velocities of the resulting trajectory, with respect to time
        Xylist - the list of all X-velocities of the resulting trajectory, with respect to time
        Ylist - the list of all Y-coordinates of the resulting trajectory, with respect to time
        Xlist - the list of all X-coordinates of the resulting trajectory, with respect to time
    """
    def ay_func(t, vy):
        return -Fd(vy)+g

    def ax_func(t, vx):
        return -Fd(vx)

    Vylist = EulerMethod(ay_func, time_guess, stepspersec*time_guess, velocity*np.sin(alpha_guess))
    Vxlist = EulerMethod(ax_func, time_guess, stepspersec*time_guess, velocity*np.cos(alpha_guess))

    def vy_func(t, y):
        t_index=int(t*(stepspersec*time_guess-1)/time_guess)
        return Vylist[t_index] 

    def vx_func(t, x):
        t_index=int(t*(stepspersec*time_guess-1)/time_guess)
        return Vxlist[t_index] 

    Ylist = EulerMethod(vy_func, time_guess, time_guess*stepspersec, 1.75)
    Xlist = EulerMethod(vx_func, time_guess, time_guess*stepspersec, 0)
    return Vylist, Vxlist, Ylist, Xlist
    

def whackderivative(y1, y2, x1, x2):
    return (y2-y1)/(x2-x1)


def NewtonMethod(stepspersec, velocity, x0, y0, alpha_guess, time_guess, iterations, margerr):
    """The complete Newton Method. Creates a vector from the intial angle- and time-guess and then iterates the trajectory for said angle.
    Then it computes its x- and y-value at the time inside the vector and together with the inverse of the Jacobian, it computes a proper 
    guess for the next iteration. That process continues until it becomes close enough (dictated by the margerr argument) or it reaches
    the maximum amount of allowed iterations.
    
    Parameters (8):
        stepspersec - number of iterations per second simulated
        velocity - initial velocity
        x0 - starting right-left position
        y0 - starting height
        alpha_guess - initial angular direction guess
        time_guess - initial guess of at what time the intersection will occur
        iterations - how many times the NewtonMethod is allowed to iterate before stopping
        margerr - what distance from the basket that is accepted as close enough
        
    Outputs:
        returns v, Ylist, Xlist
        v - the resulting vector containing angle and time
        Ylist - the list of all Y-coordinates of the resulting trajectory, with respect to time
        Xlist - the list of all X-coordinates of the resulting trajectory, with respect to time
    """
    vector=np.array([float(alpha_guess), time_guess])
    
    def fixrows(v):
        """The purpose of this function is to be able to create a derivate with respect to alpha
        """
        Vylist, Vxlist, Ylist     , Xlist      = speedandpos(v[1], v[0], stepspersec, velocity, x0, y0)
        _     , _     , Ylistalpha, Xlistalpha = speedandpos(v[1], v[0]+0.0001, stepspersec, velocity, x0, y0)
        return Vylist, Vxlist, Ylist, Xlist, Ylistalpha, Xlistalpha
    
    def f(Ylist, Xlist):
        """This is the function in Newton's method. It simply returns the X and Y value minus the coordinates of the rim.
        """
        return np.array([Ylist[-1]-3.05, Xlist[-1]-2.])
    
    def check(v):
        """Checks if the time guess is less than zero and then compensates
        """
        if(v[1]<0):
            v[1]=-v[1]
            v[0]+=np.pi
        v[0]=v[0]%(np.pi*2)
        return v
        
    def Recursion(v, iterations):
        """The core of the Newton Method. This function contains the iterative process and calculates the answer.
        """
        #print("v=", v)
        v=check(v)
        #print("v after=", v)
        Vylist, Vxlist, Ylist, Xlist, Ylistalpha, Xlistalpha=fixrows(v)
        if(np.linalg.norm(f(Ylist, Xlist))<margerr or iterations==0):
            return v, Ylist, Xlist
        #print("VYlist=", Vylist)
        dydt=Vylist[-1]
        dyda=whackderivative(Ylist[-1], Ylistalpha[-1], v[0], v[0]+0.0001)
        dxdt=Vxlist[-1]
        dxda=whackderivative(Xlist[-1], Xlistalpha[-1], v[0], v[0]+0.0001)      
        Jacobian=np.array(  [  [ dyda , dydt ],
                               [ dxda , dxdt ]  ]  )
        
        #if(np.linalg.norm(f(Ylist, Xlist))>8):
        #print("jacobian=", Jacobian)
        
        if(abs(np.linalg.det(Jacobian))==0): #in case the matrix is linearly dependant, but this rarely happens
            print("whoops")
            Jacobian=np.array(  [  [ 9 , 10 ],
                                   [ 11, 12 ]  ]  )   
        Jacobian_Inverse=np.linalg.inv(Jacobian)  
        v-=np.dot(Jacobian_Inverse, f(Ylist, Xlist))
        return Recursion(v, iterations-1)

    return Recursion(vector, iterations)
    

def theoparabola(time, x0, y0, velocity, alpha, labell):  
    """Function that plots the trajectory without air resistance
    
    Parameters (6):
        time - the time boundary
        x0 - starting right-left position
        y0 - starting height
        velocity - initial velocity
        alpha - initial angular direction
        labell - the label for the graph
        
    Outputs:
        returns nothing but plots one trajectory
    """
    startvx=velocity*np.cos(alpha)
    startvy=velocity*np.sin(alpha)
    Tl=np.linspace(0, time, int(time*1000))
    Xl=[startvx*t+x0 for t in Tl]
    Yl=[y0+startvy/startvx*x+g*x**2/(2*startvx**2) for x in Xl]
    plt.plot(Xl, Yl, label=labell)
    
    
def plottrajectory(stepspersec, velocity, x0, y0, alpha_guess, time_guess, margerr, iterations):
    """Function that plots a single trajectory together with the theoretical trajectory of its initial guess and its resulting angle
    
    Parameters (8):
        stepspersec - number of iterations
        velocity - initial velocity
        x0 - starting right-left position
        y0 - starting height
        alpha_guess - initial angular direction guess
        time_guess - initial guess of at what time the intersection will occur
        iterations - how many times the NewtonMethod is allowed to iterate before stopping
        margerr - what distance from the basket that is accepted as close enough
        
    Outputs:
        returns nothing but plots three trajectories
    """
    vector, Ylist, Xlist=NewtonMethod(stepspersec, velocity, x0, y0, alpha_guess, time_guess, iterations, margerr)
    print("The correct angle is", vector[0])
    theoparabola(vector[1], x0, y0, 9, alpha_guess, "original guess")
    theoparabola(vector[1], x0, y0, 9, vector[0], "no air resistance")
    plt.scatter(2, 3.05, label="rim")
    plt.plot(Xlist, Ylist, label="numerical")
    plt.legend()
    
    
def plottrajectories(stepspersec, velocity, x0, y0, time_guess, iterations, margerr, guesses):
    """Function that plots multiple trajectories 
    
    Parameters (8):
        stepspersec - number of iterations per second simulated
        velocity - initial velocity
        x0 - starting right-left position
        y0 - starting height
        alpha_guess - initial angular direction guess
        time_guess - initial guess of at what time the intersection will occur
        iterations - how many times the NewtonMethod is allowed to iterate before stopping
        margerr - what distance from the basket that is accepted as close enough
        guesses - divides the interval [0, pi/2] into this many, evenly spaced, angles
        
    Outputs:
        returns nothing but plots all the trajectories of the angles created from "guesses"
    """
    for a in np.linspace(0, np.pi/2, guesses):
        vector, Ylist, Xlist=NewtonMethod(stepspersec, velocity, x0, y0, a, time_guess, iterations, margerr)
        plt.plot(Xlist, Ylist, label="")
    plt.scatter(2, 3.05, label="rim")
    plt.title(f"with max {iterations} iterations")
    plt.legend()
    

def plotsolutions(stepspersec, velocity, x0, y0, time_guess, iterations, margerr, points):
    """Function that plots the resulting angle with respect to intial angle guess
    
    Parameters (8):
        stepspersec - number of iterations per second simulated
        velocity - initial velocity
        x0 - starting right-left position
        y0 - starting height
        alpha_guess - initial angular direction guess
        time_guess - initial guess of at what time the intersection will occur
        iterations - how many times the NewtonMethod is allowed to iterate before stopping
        margerr - what distance from the basket that is accepted as close enough
        points - divides the interval [0, pi/2] into this many, evenly spaced, angles
        
    Outputs:
        returns nothing but plots all the angles obtained after the NewtonMethod with respect to all intial angle guesses
    """
    axis=plt.axes()
    axis.set_xlim(0, np.pi/2)
    axis.set_ylim(0, np.pi/2)
    plt.xlabel("Guessed angle")
    plt.ylabel("Resulting angle")
    AI=np.linspace(0, np.pi/2, points)
    AO=[]
    for a in AI:
        AO.append((NewtonMethod(stepspersec, velocity, x0, y0, a, 1, iterations, margerr)[0][0])%(2*np.pi))
    plt.plot(AI, AO)
    plt.scatter(AI, AO)
    plt.scatter(max(AO), max(AO))
    plt.legend()    

plottrajectory(1000, 9, 0, 1.75, 1, 1, 0.01, 10)
#print(NewtonMethod.__doc__)