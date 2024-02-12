import gym
import os
import time as t
import LaRoboLiga24
import cv2
import pybullet as p
import numpy as np

CAR_LOCATION = [0,0,1.5]

BALLS_LOCATION = dict({
    'red': [7, 4, 1.5],
    'blue': [2, -6, 1.5],
    'yellow': [-6, -3, 1.5],
    'maroon': [-5, 9, 1.5]
})
BALLS_LOCATION_BONOUS = dict({
    'red': [9, 10, 1.5],
    'blue': [10, -8, 1.5],
    'yellow': [-10, 10, 1.5],
    'maroon': [-10, -9, 1.5]
})

HUMANOIDS_LOCATION = dict({
    'red': [11, 1.5, 1],
    'blue': [-11, -1.5, 1],
    'yellow': [-1.5, 11, 1],
    'maroon': [-1.5, -11, 1]
})

VISUAL_CAM_SETTINGS = dict({
    'cam_dist'       : 17,
    'cam_yaw'        : 0,
    'cam_pitch'      : -110,
    'cam_target_pos' : [0,4,0]
})


os.chdir(os.path.dirname(os.getcwd()))
env = gym.make('LaRoboLiga24',
    arena = "arena2",
    car_location=CAR_LOCATION,
    ball_location=BALLS_LOCATION,  # toggle this to BALLS_LOCATION_BONOUS to load bonous arena
    humanoid_location=HUMANOIDS_LOCATION,
    visual_cam_settings=VISUAL_CAM_SETTINGS
)

"""
CODE AFTER THIS
"""

def wait(time=1):
    t.sleep(time)


def open():
    env.open_grip()


def stop(time=1):
    wait(time)
    env.move(vels=[[0, 0], [0, 0]])


def close():
    env.close_grip()


def shoot(hit=800):
    global first_run
    global index
    env.open_grip()
    env.shoot(hit)
    index += 1
    first_run = True


def move(mode="f", speed=5):
    if mode.lower() == "f":
        mat = [[speed, speed], [speed, speed]]
    elif mode.lower() == "r":
        mat = [[speed, -speed], [speed, -speed]]
    else:
        print("Error Occurred , Unexpected mode in Move Function.")
        return "Error"
    env.move(vels=mat)


def isBall(cnt):
    x, y, w, h = cv2.boundingRect(cnt)
    rectangle_area = w * h
    (x2, y2), radius = cv2.minEnclosingCircle(cnt)
    circle_area = np.pi * (radius ** 2)
    area = cv2.contourArea(cnt) if ((rectangle_area - circle_area)> 0) else 0
    return area

def post(cnt):
    global Holding
    x, y, w, h = cv2.boundingRect(cnt)
    r = x + w / 2
    if ((x > 282) or (r>320)):
        move('r', 2)
    elif r > 320:
        move('r', -1)
    elif r < 300:
        move('r', 1)
    else:
        shoot()
        Holding = False


index = 0
start_time = 0
end_time = 0
first_run = True
    

def MoveHold(cnt):
    x, y, w, h = cv2.boundingRect(cnt)
    x = x + w / 2
    if x > 340 :
        move('r',2)
    elif x < 260:
        move('r',-2)
    else:
        global first_run
        global start_time
        if first_run:
            start_time = t.time()
            first_run = False
        move('f', 6)
        area = cv2.contourArea(cnt)
        if area > 40000:
            global Holding
            stop(.2)
            close()
            end_time = t.time()
            duration = end_time - start_time
            stop(.25)
            Holding = True
            if Holding==True:
                move("f",-4)
                t.sleep(0.7 * duration)
                move("f",0)
                t.sleep(1)
                
l_ball_clr = [[0,200,140],[23, 168, 109],[134,0,0],[80,102,0]]

u_ball_clr = [[16,255,255],[102, 255, 255],[255,255,255],[139,255,255]]

def Findcontour(img, lowerRange, UpperRange):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lowerRange, UpperRange)
    res = cv2.bitwise_and(img, img, mask=mask)
    imgray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    contours, hierarchy = cv2.findContours(imgray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

## setup

open()
Holding = False
post1 = False
End = False

while True:
    if (index > 3):
        t.sleep(10)
    img = env.get_image(cam_height=0, dims=[600, 600])
    lower_color = np.array(l_ball_clr[index], dtype=np.uint8)
    upper_color = np.array(u_ball_clr[index], dtype=np.uint8)
    unsorted_contours = Findcontour(img, lower_color, upper_color)
    contours = sorted(unsorted_contours, key=cv2.contourArea, reverse=True)


    if contours:
        if not Holding:
            cnt = contours[0]
            if isBall(cnt):
                MoveHold(cnt)
            else:
                move('r')
        else:
            if len(contours)>2:
                cnt=contours[1]
                post(cnt)

            else:
                move('r')
    else:
        move('r')


    k = cv2.waitKey(1)
    if k == ord('q'):
        break

t.sleep(10)
env.close()