import gym
import os
import cv2 as cv
import time as t
import pybullet as p
import LaRoboLiga24

CAR_LOCATION = [3,0,1.5]
# BALL_LOCATION = [-3,0,1.5]
# HUMANOID_LOCATION = [6,7,1.5]
VISUAL_CAM_SETTINGS = dict({
    'cam_dist'       : 13,
    'cam_yaw'        : 0,
    'cam_pitch'      : -110,
    'cam_target_pos' : [0,4,0]
})
BALLS_LOCATION = dict({
    'red': [7, 4, 1.5],
    'blue': [2, -6, 1.5],
    'yellow': [-6, -3, 1.5],
    'maroon': [-5, 9, 1.5]
})
HUMANOIDS_LOCATION = dict({
    'red': [11, 1.5, 1],
    'blue': [-11, -1.5, 1],
    'yellow': [-1.5, 11, 1],
    'maroon': [-1.5, -11, 1]
})


os.chdir(os.path.dirname(os.getcwd()))

env = gym.make('LaRoboLiga24',
    arena = "arena2",
    car_location=CAR_LOCATION,
    ball_location=BALLS_LOCATION,
    humanoid_location=HUMANOIDS_LOCATION,
    visual_cam_settings=VISUAL_CAM_SETTINGS
)

while True:
    img = env.get_image(cam_height=0, dims=[512,512])
    cv.imshow("img", img)
    k = cv.waitKey(1)
    if k==ord('q'):
        break