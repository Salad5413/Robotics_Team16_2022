from cmath import pi
import math
import numpy as np
import warnings
import sys
def rotatez(theta):
    #rotatation around Z-axis
    ImatrixRz = np.zeros((3,3))
    ImatrixRz[0,0] = math.cos(theta)
    ImatrixRz[0,1] = -math.sin(theta)
    ImatrixRz[1,1] = math.cos(theta)
    ImatrixRz[1,0] = math.sin(theta)
    ImatrixRz[2,2] = 1
    return  ImatrixRz

def rotatey(theta):
    #rotatation around Y-axis
    ImatrixRy = np.zeros((3,3))
    ImatrixRy[0,0] = math.cos(theta)
    ImatrixRy[0,2] = math.sin(theta)
    ImatrixRy[2,2] = math.cos(theta)
    ImatrixRy[2,0] = -math.sin(theta)
    ImatrixRy[1,1] = 1
    return  ImatrixRy

def rotatex(theta):
    #rotatation around X-axis
    ImatrixRx = np.zeros((3,3))
    ImatrixRx[1,1] = math.cos(theta)
    ImatrixRx[1,2] = -math.sin(theta)
    ImatrixRx[2,2] = math.cos(theta)
    ImatrixRx[2,1] = math.sin(theta)
    ImatrixRx[0,0] = 1
    return  ImatrixRx

def rotation(q1,q2,q3,q4,q5):
    #Rotation for R0T
    Rt = np.matmul(np.matmul(rotatez(q1),rotatey(-q2-q3-q4),),rotatex(-q5))

    return Rt

def position(q1,q2,q3,q4,q5):
    #length of the arms in meters
    l0 = 61 / 1000
    l1 = 43.5 / 1000
    l2 = 82.85 / 1000
    l3 = 82.85 / 1000
    l4 = 73.85 / 1000
    l5 = 54.57 / 1000
    # arrays for Pi,i+1
    P01 = np.array([[0],[0],[l0+l1]])
    P12 = np.array([[0],[0],[0]])
    P23 = np.array([[l2],[0],[0]])
    P34 = np.array([[0],[0],[-l3]])
    P45 = np.array([[0],[0],[0]])
    P5T = np.array([[-l4-l5],[0],[0]])
    
    #put all matrcies into a list, do corss product and use a for loop to add them together
    empty = [P01 , np.matmul(rotatez(q1),P12) , np.matmul((np.matmul(rotatez
    (q1),rotatey(-q2))),P23) , np.matmul((np.matmul(rotatez
    (q1),rotatey(-q2-q3))),P34) , np.matmul((np.matmul(rotatez
    (q1),rotatey(-q2-q3-q4))),P45) , np.matmul(np.matmul(np.matmul(rotatez
    (q1),rotatey(-q2-q3-q4)),rotatex(-q5)),P5T)]

    for i in range(len(empty)-1):
        empty[i+1]  = np.add(empty[i],empty[i+1])
        Pt = empty[i+1]
        
    return Pt 

