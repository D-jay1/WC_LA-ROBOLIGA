import gym
import os
import time as t
import LaRoboLiga24
import cv2 as cv
import pybullet as p
import numpy as np

CAR_LOCATION = [-25.5,0,1.5]


VISUAL_CAM_SETTINGS = dict({
    'cam_dist'       : 43,
    'cam_yaw'        : 0,
    'cam_pitch'      : -110,
    'cam_target_pos' : [0,4,0]
})


os.chdir(os.path.dirname(os.getcwd()))
env = gym.make('LaRoboLiga24',
    arena = "arena1",
    car_location=CAR_LOCATION,
    visual_cam_settings=VISUAL_CAM_SETTINGS
)


while True:
    img = env.get_image(cam_height=0, dims=[600,600])
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    ret,binary_thresh = cv.threshold(gray, 180, 255, cv.THRESH_BINARY)
    contours, _ = cv.findContours(binary_thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    left_crop = binary_thresh[100:300 , 56:320]
    right_crop = binary_thresh[100:300 , 320:600]
    left_lane = np.array(left_crop)
    cv.imshow('left lane' , left_crop)
    cv.imshow('right lane' , right_crop)
    right_lane = np.array(right_crop)

    error = (((cv.countNonZero(left_lane)) - (cv.countNonZero(right_lane)))/300)
    l = 16.5 + error
    r = 16.5 - error
    env.move(vels=[[l, r], [l, r]])
    k = cv.waitKey(1)
    if k == ord('q'):
        break
    
t.sleep(100)
env.close()