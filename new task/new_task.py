#!/usr/bin/env python3
#coding=utf-8
#bgr8 to jpeg format
import enum
import cv2
import numpy as np
import time
import random
from task2 import inverse_K


def bgr8_to_jpeg(value, quality=75):
    return bytes(cv2.imencode('.jpg', value)[1])

#Import library
from Arm_Lib import Arm_Device

Arm = Arm_Device()

def get_color(img):
    H = []
    color_name={}
    img = cv2.resize(img, (640, 480), )

    HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    cv2.rectangle(img, (280, 180), (360, 260), (0, 255, 0), 2)
    #Take out the H, S, V values of each row and each column in turn and put them into the container
    for i in range(280, 360):
        for j in range(180, 260): H.append(HSV[j, i][0])
    #Calculate the maximum and minimum of H, S, and V respectively
    H_min = min(H);H_max = max(H)
#     print(H_min,H_max)
    #Judging the color
    if H_min >= 0 and H_max <= 10 or H_min >= 156 and H_max <= 180: color_name['name'] = 'red'
    elif H_min >= 26 and H_max <= 34: color_name['name'] = 'yellow'
    elif H_min >= 35 and H_max <= 78: color_name['name'] = 'green'
    elif H_min >= 100 and H_max <= 124: color_name['name'] = 'blue'
    return img, color_name

# Define variable parameters at different locations
look_at = [90, 164, 18, 0, 90, 90]
p_top = [90, 80, 50, 50, 270]

p_Yellow = [65, 22, 64, 56, 270]
p_Red = [118, 19, 66, 56, 270]

p_Green = [136, 66, 20, 29, 270]
p_Blue = [44, 66, 20, 28, 270]

p_gray = [90, 48, 35, 30, 270]

# Define control DOFBOT function, control No.1-No.6 servo，p=[S1,S2,S3,S4,S5,S6]
def arm_move_6(p, s_time = 500):
    for i in range(6):
        id = i + 1
        Arm.Arm_serial_servo_write(id, p[i], s_time)
        time.sleep(.01)
    time.sleep(s_time/1000)
    
#Define control DOFBOT function, control No.1-No.5 servo，p=[S1,S2,S3,S4,S5]
def arm_move(p, s_time = 500):
    for i in range(5):
        id = i + 1
        if id == 5:
            time.sleep(.1)
            Arm.Arm_serial_servo_write(id, p[i], int(s_time*1.2))
        elif id == 1 :
            Arm.Arm_serial_servo_write(id, p[i], int(3*s_time/4))
        else:
            Arm.Arm_serial_servo_write(id, p[i], int(s_time))
        time.sleep(.01)
    time.sleep(s_time/1000)
    
# enable=1：clip，=0：release
def arm_clamp_block(enable):
    if enable == 0:
        Arm.Arm_serial_servo_write(6, 60, 400)
    else:
        Arm.Arm_serial_servo_write(6, 130, 400)
    time.sleep(.5)
    
arm_move_6(look_at, 1000)
time.sleep(1)

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
cap.set(5, 30)  
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))

# Red is selected by default, and the program will automatically switch the color according to the color detected in the box
# Red value
color_lower = np.array([0, 43, 46])
color_upper = np.array([10, 255, 255])

# green value
# color_lower = np.array([35, 43, 46])
# color_upper = np.array([77, 255, 255])

# blue value
# color_lower=np.array([100, 43, 46])
# color_upper = np.array([124, 255, 255])

# yellow value
# color_lower = np.array([26, 43, 46])
# color_upper = np.array([34, 255, 255])

# orange value
# color_lower = np.array([11, 43, 46])
# color_upper = np.array([25, 255, 255])


def Color_Recongnize():
    Arm.Arm_Buzzer_On(1)
    s_time = 300
    Arm.Arm_serial_servo_write(4, 10, s_time)
    time.sleep(s_time/1000)
    Arm.Arm_serial_servo_write(4, 0, s_time)
    time.sleep(s_time/1000)
    Arm.Arm_serial_servo_write(4, 10, s_time)
    time.sleep(s_time/1000)
    Arm.Arm_serial_servo_write(4, 0, s_time)
    time.sleep(s_time/1000)
    
    while(1):

        ret, frame = cap.read()
        frame, color_name = get_color(frame)
        if len(color_name)==1:
            global color_lower
            global color_upper
            if color_name['name'] == 'yellow':
                color_lower = np.array([26, 43, 46])
                color_upper = np.array([34, 255, 255])
                print('yellow')
                return 1
            elif color_name['name'] == 'red':
                color_lower = np.array([0, 43, 46])
                color_upper = np.array([10, 255, 255])
                print('red')
                return 2
            elif  color_name['name'] == 'green':
                color_lower = np.array([35, 43, 46])
                color_upper = np.array([77, 255, 255])
                print('green')
                return 3
            elif color_name['name'] == 'blue':
                color_lower=np.array([100, 43, 46])
                color_upper = np.array([124, 255, 255])
                print('blue')
                return 4

        #cv2.imshow('Capture', frame)

        # change to hsv model
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        time.sleep(0.01)

def main():
    Arm.Arm_serial_servo_write6(90, 90, 90, 90, 90, 90, 500)
    time.sleep(1)
    
    while(True):
        print("please select: \n1 -> change speed manually\
                \n2 -> change speed automatically\
                \n3 -> exit the program")
        mode = input()
        if mode == "1":
            manual_speed()
        elif mode == "2": 
            auto_speed()
        elif mode == "3": 
            break
        else:
            print("Unknown input")

# convert speed from degree/second to millisecond
def speed_conversion(speed, start_angle, desired_angle):

    step = abs(desired_angle - start_angle)
    time = step/speed
    milli_time = round(time * 1000)
    time_sec = round(time)
    return milli_time, time_sec

def move_servo(desired_angle, servo_number, speed):
    # read the current angle of servo 5
    
    current_angle = Arm.Arm_serial_servo_read(servo_number)
    time.sleep(1)

    milli_time, time_sec = speed_conversion(speed, current_angle, desired_angle)
    
    Arm.Arm_serial_servo_write(servo_number, desired_angle, milli_time)
    time.sleep(time_sec + 0.5)
    
    
    # Wait until the servo reaches the desired angle
    #while(Arm.Arm_serial_servo_read(servo_number) != desired_angle):
        #pass
    
    reach_angle = Arm.Arm_serial_servo_read(servo_number)
    time.sleep(0.5)
    
    print("The servo %d reached the desired angle %d" % (servo_number, reach_angle))

def manual_speed():
    while(True):
        desired_angle = 70
        speed = [0]*5
        while ((1 <= speed[0] <= 45) == False):
            print("please input the speed1 in degree/second(range: 1-45)")
            speed[0] = int(input())
        while ((1 <= speed[1] <= 45) == False):
            print("please input the speed2 in degree/second(range: 1-45)")
            speed[1] = int(input())
        while ((1 <= speed[2] <= 45) == False):
            print("please input the speed3 in degree/second(range: 1-45)")
            speed[2] = int(input())
        while ((1 <= speed[3] <= 45) == False):
            print("please input the speed4 in degree/second(range: 1-45)")
            speed[3] = int(input())
        while ((1 <= speed[4] <= 45) == False):
            print("please input the speed5 in degree/second(range: 1-45)")
            speed[4] = int(input())

        for i in range(0,5):
            move_servo(desired_angle, i+1, speed[i])

        print("Press \"r\" to reset the servo to 90 degree,\nor press any key else to select another mode")
        end_choice = input()
        if end_choice == "r":

            Arm.Arm_serial_servo_write(servo_number, 90, 500)
            time.sleep(1)
        else: 
            break

            
def select_speed(a):
    if a == 1:
        return 3000
    if a == 2:
        return 2000
    if a == 3:
        return 1000
    if a == 4:
        return 500



def auto_speed():
    Rd = [[-0.75, -0.1047, -0.6531],
          [-0.433, 0.8241, 0.3652],
          [0.5   , 0.5567, -0.6634]]
    Pd = [0.2058, 0.1188, 0.1464]   
    q0 = np.deg2rad(np.transpose([25, 50, 75, 30, 30]))
    a,b,c = inverse_K(Rd, Pd, q0, alpha=0.3,  tol=[0.02,0.02,0.02,0.001,0.001,0.001], Nmax=200)
    sa = np.rad2deg(a)

    while (True):
        Arm.Arm_serial_servo_write6(90, 90, 90, 90, 90, 90, 1000)
        print("Press \"s\" to start, press any key else to select another mode")
        start = input()
        if start == "s":
            Choice = Color_Recongnize()
            speed = select_speed(Choice)
            Arm.Arm_serial_servo_write6(sa[0], sa[1], sa[2], sa[3], sa[4],90, speed)
        print("Press \"r\" to restart, Press \"s\" to stop")
        result = input()
        if result == "s":
            break


try :
    main()
except KeyboardInterrupt:
    print(" Program closed! ")
    pass