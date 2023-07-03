"""Library with helpful geometric formulae, frequently used in structural analysis."""
__author__ = "Ben Fisher"
__version__ = "0.0.1"
__license__ = "GPL"
__credits__ = ["Ben Fisher"]
__status__ = "Development"
__maintainer__ = "Ben Fisher"

import numpy as np
import pandas as pd
from math import sqrt


def extrema(coords):
    """returns the extrema of a collection of coordinate pairs.

    Args:
        coords (numpy array): vertical array of x,y pairs

    Returns:
        numpy array (floats):   [[xmin, xmax],
                                 [ymin, ymax]]
    """
    coords = np.array(coords)
    n = coords.shape[0]
    x = coords[:,0]
    y = coords[:,1]
    return np.array([[np.min(x),np.max(x)],[np.min(y),np.max(y)]])

def perimeter(coords):
    coords = np.array(coords)
    n = coords.shape[0]
    x = coords[:,0]
    y = coords[:,1]
    P = 0
    for i in range(0,n-1):
        P += sqrt((x[i+1]-x[i])**2+(y[i+1]-y[i])**2)
    return P

def area(coords):
    coords = np.array(coords)
    n = coords.shape[0]
    x = coords[:,0]
    y = coords[:,1]
    A = 0
    for i in range(n-1):
        A += (x[i]*y[i+1]-x[i+1]*y[i])
    A *= 0.5
    return A

def centroids(coords):
    coords = np.array(coords)
    n = coords.shape[0]
    x = coords[:,0]
    y = coords[:,1]
    A = area(coords)
    Cx = Cy = 0
    for i in range(0,n-1):
        Cx += (x[i]+x[i+1])*(x[i]*y[i+1]-x[i+1]*y[i])
        Cy += (y[i]+y[i+1])*(x[i]*y[i+1]-x[i+1]*y[i])
    Cx /= (6*A)
    Cy /= (6*A)
    return np.array([Cx,Cy])

def Cx(coords):
    return centroids(coords)[0]

def Cy(coords):
    return centroids(coords)[1]

def inertias(coords, x_offset = 0, y_offset = 0):
    coords = np.array(coords)
    n = coords.shape[0]
    x = coords[:,0]
    y = coords[:,1]
    Ix = Iy = Ixy = 0
    for i in range(0,n-1):
        term_1 = (x[i]*y[i+1]-x[i+1]*y[i])
        Ix  += term_1*(y[i]**2+y[i]*y[i+1]+y[i+1]**2)
        Iy  += term_1*(x[i]**2+x[i]*x[i+1]+x[i+1]**2)
        # Ixy += term_1*((x[i]*y[i+1])+(2*x[i]*y[i])+(2*x[i+1]*y[i+1])+(x[i+1]*y[i]))
    Ix /= 12
    Iy /= 12
    # The next block performs parallel axis calculation in either x_offset or y_offset are non-zero
    if (x_offset != 0) | (y_offset != 0):
        A = area(coords)
        Ix += A*y_offset**2
        Iy += A*x_offset**2
    Ixy = Ix + Iy   #Ix /= 24  
    return np.array([Ix,Iy,Ixy])

def Ix(xy):
    return inertias(xy)[0]

def Iy(xy):
    return inertias(xy)[1]

def Ixy(xy):
    return inertias(xy)[2]

def radii(xy):
    inerts = inertias(xy)
    A = area(xy)
    return np.array([sqrt(inerts[0]/A),sqrt(inerts[1]/A)])

def rx(xy):
    return radii(xy)[0]

def ry(xy):
    return radii(xy)[1]

