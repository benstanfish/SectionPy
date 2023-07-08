import os, sys, pathlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import *
import collections.abc

def close_polygon(arr):
    return np.append(arr,[arr[0]],axis=0)

def plot_polygon(arr, unit = 1):
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    
    ax.xaxis.set_major_locator(plt.MultipleLocator(unit))
    ax.yaxis.set_major_locator(plt.MultipleLocator(unit))
    plt.grid()
    
    ax.fill(arr[:,0],arr[:,1],color="skyblue",alpha=0.5)
    plt.plot(arr[:,0],arr[:,1],color="dodgerblue",linewidth=3)
    

def circle_points(radius, point_count = 30, max_angle = 2 * pi, is_segment: bool = False):
    xys = np.zeros([point_count,2])
    for i in range(0,n):
        xys[i,0]= radius * cos(min(2*pi, max_angle)/(max(point_count,2)-1)*i)
        xys[i,1]= radius * sin(min(2*pi, max_angle)/(max(point_count,2)-1)*i)
    if is_segment == True:
        if max_angle < 2 * pi:
            xys = np.append(xys,[[0,0]],axis=0)
    return xys

def ellipse_points(short_radius, long_radius, point_count = 30, max_angle = 2 * pi, is_segment: bool = False):
    xys = np.zeros([point_count,2])
    for i in range(0,n):
        xys[i,0]= short_radius * cos(min(2*pi, max_angle)/(max(point_count,2)-1)*i)
        xys[i,1]= long_radius * sin(min(2*pi, max_angle)/(max(point_count,2)-1)*i)
    if is_segment == True:
        if max_angle < 2 * pi:
            xys = np.append(xys,[[0,0]],axis=0)
    return xys

def rectangular_points(length, height):
    return np.array([[0,0],[length,0],[length,height],[0,height]])

def I_points(depth, web_thick, top_flange_width, top_flange_thick, bottom_flange_width, bottom_flange_thick):
    return np.array([[0,0],
                    [bottom_flange_width,0],
                    [bottom_flange_width,bottom_flange_thick],
                    [bottom_flange_width-(bottom_flange_width-web_thick)/2,bottom_flange_thick],
                    [bottom_flange_width-(bottom_flange_width-web_thick)/2,depth-top_flange_thick],
                    [bottom_flange_width,depth-top_flange_thick],
                    [bottom_flange_width,depth],
                    [0,depth],
                    [0,depth-top_flange_thick],
                    [(bottom_flange_width-web_thick)/2,depth-top_flange_thick],
                    [(bottom_flange_width-web_thick)/2,bottom_flange_thick],
                    [0,bottom_flange_thick]])
    
def C_points(depth, web_thick, top_flange_width, top_flange_thick, bottom_flange_width, bottom_flange_thick):
    return np.array([[0,0],
                     [bottom_flange_width,0],
                     [bottom_flange_width,bottom_flange_thick],
                     [web_thick,bottom_flange_thick],
                     [web_thick,depth-top_flange_thick],
                     [top_flange_width,depth-top_flange_thick],
                     [top_flange_width,depth],
                     [0,depth]
                    ])
    
def L_points(depth, web_thick, bottom_flange_width, bottom_flange_thick):
    return np.array([[0,0],
                     [bottom_flange_width,0],
                     [bottom_flange_width,bottom_flange_thick],
                     [web_thick,bottom_flange_thick],
                     [web_thick,depth],
                     [0,depth]
                    ])

def T_points(depth, stem_thick, flange_width, flange_thick):
    return np.array([[(flange_width-stem_thick)/2,0],
                     [flange_width-(flange_width-stem_thick)/2,0],
                     [flange_width-(flange_width-stem_thick)/2,depth-flange_thick],
                     [flange_width,depth-flange_thick],
                     [flange_width,depth],
                     [0,depth],
                     [0,depth-flange_thick],
                     [(flange_width-stem_thick)/2,depth-flange_thick],
                    ])
    

# Transforms

def rotate(arr, rads):
    transform = np.array([[cos(rads),-sin(rads)],[sin(rads),cos(rads)]]).transpose()
    return np.matmul(arr,transform)

def reflection(arr, rads):
    transform = np.array([[cos(2*rads),sin(2*rads)],[sin(2*rads),-cos(2*rads)]])
    return np.matmul(arr,transform)

def translate(arr,d):
    new_arr = np.copy(arr)
    new_arr[:,0] = new_arr[:,0] + d[0]
    new_arr[:,1] = new_arr[:,1] + d[1]
    return new_arr

def scale(arr, scale):
    if isinstance(scale,(collections.abc.Sequence, np.ndarray)):
        transform = np.array([[scale[0],0],[0,scale[1]]])
    else:
        transform = np.array([[scale,0],[0,scale]])
    return np.matmul(arr,transform)

def skew(arr, skew_factors):
    transform = np.array([[1,skew_factors[0]],[skew_factors[1],1]]).transpose()
    return np.matmul(arr,transform)