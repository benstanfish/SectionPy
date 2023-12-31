"""Library with helpful geometric formulae, frequently used in structural analysis."""
__author__ = "Ben Fisher"
__version__ = "0.0.1"
__license__ = "GPL"
__credits__ = ["Ben Fisher"]
__status__ = "Development"
__maintainer__ = "Ben Fisher"

import numpy as np
import pandas as pd
from math import sqrt, radians, degrees


def closePolygon(coords):
    coords = np.array(coords)
    if not (coords[0][0] == coords[-1][0]) & (coords[0][1] == coords[-1][1]):
        coords = np.vstack((coords, coords[0]))
    return coords

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
    coords = closePolygon(coords)
    n = coords.shape[0]
    x = coords[:,0]
    y = coords[:,1]
    P = 0
    for i in range(0,n-1):
        P += sqrt((x[i+1]-x[i])**2+(y[i+1]-y[i])**2)
    return P

def area(coords):
    coords = closePolygon(coords)
    n = coords.shape[0]
    x = coords[:,0]
    y = coords[:,1]
    A = 0
    for i in range(n-1):
        A += (x[i]*y[i+1]-x[i+1]*y[i])
    A *= 0.5
    return A

def centroids(coords):
    coords = closePolygon(coords)
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

#TODO: This formula does not appear to be working correctly. Need to verify by other means.
def inertias(coords, x_offset = 0, y_offset = 0):
    coords = closePolygon(coords)
    n = coords.shape[0]
    x = coords[:,0]
    y = coords[:,1]
    Ix = Iy = Ixy = 0
    for i in range(0,n-1):
        Ix  += (x[i]*y[i+1]-x[i+1]*y[i])*(y[i]**2+y[i]*y[i+1]+y[i+1]**2)
        Iy  += (x[i]*y[i+1]-x[i+1]*y[i])*(x[i]**2+x[i]*x[i+1]+x[i+1]**2)
        Ixy += (x[i]*y[i+1]-x[i+1]*y[i])*((x[i]*y[i+1])+(2*x[i]*y[i])+(2*x[i+1]*y[i+1])+(x[i+1]*y[i]))
    Ix /= 12
    Iy /= 12
    Ixy /= 24
    # The next block performs parallel axis calculation in either x_offset or y_offset are non-zero
    if (x_offset != 0) | (y_offset != 0):
        A = area(coords)
        Ix += A*y_offset**2
        Iy += A*x_offset**2
        Ixy += A*x_offset*y_offset
    Iz = Ix + Iy   # Polar moment of inertia using perpendicular axis theorem
    return np.array([Ix,Iy,Iz,Ixy])

def Ix(coords):
    return inertias(coords)[0]

def Iy(coords):
    return inertias(coords)[1]

def J(coords):
    return inertias(coords)[2]

def Iz(coords):
    return inertias(coords)[2]

def Ixy(coords):
    return inertias(coords)[3]

def inertias_inclined(coords, angle_degrees = 0):
    inerts = inertias(coords)
    rads = radians(angle_degrees)
    ix = inerts[0]
    iy = inerts[1]
    ixy = inerts[3]
    ix_new = (ix+iy)/2+(ix-iy)/2*cos(2*rads)-ixy*sin(2*rads)
    iy_new = (ix+iy)/2-(ix-iy)/2*cos(2*rads)+ixy*sin(2*rads)
    ixy_new = (ix-iy)/2*sin(2*rads)+ixy*cos(2*rads)
    return [ix_new,iy_new,ix_new+iy_new,ixy_new]

def sectionModulii(coords):
    extremes = extrema(coords)
    cgs = centroids(coords)
    inerts = inertias(coords)
    S_bot = inerts[0]/(extremes[1][0] - cgs[1])
    S_top = inerts[0]/(extremes[1][1] - cgs[1])
    S_left = inerts[1]/(extremes[0][0] - cgs[0])
    S_right = inerts[1]/(extremes[0][1] - cgs[0])
    return [S_bot, S_top, S_left, S_right]

def Sx(coords):
    sectionModulii(coords)[1:2]

def Sy(coords):
    sectionModulii(coords)[3:4]

def radii(xy):
    inerts = inertias(xy)
    A = area(xy)
    return np.array([sqrt(inerts[0]/A),sqrt(inerts[1]/A)])

def rx(xy):
    return radii(xy)[0]

def ry(xy):
    return radii(xy)[1]


def doLinesIntersect(line1,line2):
    """Determines if projection of two line segments ever intersect.

    Args:
        line1 (array_like): coordinates of line 1
        line2 (array_like): coordinates of line 1

    Returns:
        boolean: if lines intersect as some point on a plane, returns True
    """
    line1 = np.array(line1)
    line2 = np.array(line2)
    x11 = line1.copy()
    x21 = line2.copy()
    x11[:,1]=1
    x21[:,1]=1
    y11 = line1.copy()
    y21 = line2.copy()
    y11[:,[0,1]] = y11[:,[1,0]] #column swap
    y11[:,1]=1
    y21[:,[0,1]] = y21[:,[1,0]]
    y21[:,1]=1
    denom_det = np.linalg.det(np.array([[np.linalg.det(x11),np.linalg.det(y11)],[np.linalg.det(x21),np.linalg.det(y21)]]))
    if denom_det == 0:
        return False
    else:
        return True

def intersection(line1, line2):
    line1 = np.array(line1)
    line2 = np.array(line2)
    x11 = line1.copy()
    x21 = line2.copy()
    x11[:,1]=1
    x21[:,1]=1
    y11 = line1.copy()
    y21 = line2.copy()
    y11[:,[0,1]] = y11[:,[1,0]] #column swap
    y11[:,1]=1
    y21[:,[0,1]] = y21[:,[1,0]]
    y21[:,1]=1
    denom_det = np.linalg.det(np.array([[np.linalg.det(x11),np.linalg.det(y11)],[np.linalg.det(x21),np.linalg.det(y21)]]))
    numer_det_x = np.linalg.det(np.array([[np.linalg.det(line1),np.linalg.det(x11)],[np.linalg.det(line2),np.linalg.det(x21)]]))
    numer_det_y = np.linalg.det(np.array([[np.linalg.det(line1),np.linalg.det(y11)],[np.linalg.det(line2),np.linalg.det(y21)]]))
    x0 = numer_det_x / denom_det
    y0 = numer_det_y / denom_det
    return np.array([x0,y0])

def x0(line1, line2):
    """Returns the x coordinate where two lines intersect.
    """
    return intersection(line1, line2)[0]

def y0(line1, line2):
    """Returns the y coordinate where two lines intersect.
    """
    return intersection(line1, line2)[1]

def bezierParams(line1, line2):
    """returns the t and u first-order bezier parameters of two lines, which represent where the two lines intersect. The line segment, between the provided ordinates ranges from 0 - 1. Therefore, the line is intersected if t or u is between 0 - 1. If the number is outside, it is intersected at that point instead.

    Args:
        line1 (_type_): _description_
        line2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    line1 = np.array(line1)
    line2 = np.array(line2)
    t = np.linalg.det(np.array([[line1[0,0]-line2[0,0],line2[0,0]-line2[1,0]],[line1[0,1]-line2[0,1],line2[0,1]-line2[1,1]]])) / np.linalg.det(np.array([[line1[0,0]-line1[1,0],line2[0,0]-line2[1,0]],[line1[0,1]-line1[1,1],line2[0,1]-line2[1,1]]]))
    u = np.linalg.det(np.array([[line1[0,0]-line2[0,0],line1[0,0]-line1[1,0]],[line1[0,1]-line2[0,1],line2[0,1]-line1[1,1]]])) / np.linalg.det(np.array([[line1[0,0]-line1[1,0],line2[0,0]-line2[1,0]],[line1[0,1]-line1[1,1],line2[0,1]-line2[1,1]]]))
    return t,u

def doSegmentsIntersect(line1,line2):
    """Determines of two line segments intersect each other. It is possible that one of the lines can intersect the other with an endpoint. In this case, the bezier param of one would be between 0 and 1.
    
    This test does not treat 0 or 1 inclusive, as this is the i or j endpoint of a segment.

    Args:
        line1 (array_like): coordinates of line 1
        line2 (array_like): coordinates of line 1

    Returns:
        boolean, boolean: Returns true for each segment that is intersected
    """
    ret1 = ret2 = False
    t, u = bezierParams(line1,line2)
    if (t>0)&(t<1):
        ret1 = True
    if (u>0)&(u<1):
        ret2 = True
    return ret1,ret2


    