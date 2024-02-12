import gym
import os
import time as t
import pybullet as p
import LaRoboLiga24

os.chdir(os.path.dirname(os.getcwd()))

env = gym.make('LaRoboLiga24',
    arena = "arena2",
    car_location=[2,0,1.5]
)

env.move(vels=[[2,2],
               [2,2]])
t.sleep(2)
env.move(vels=[[-2,2],
               [-2,2]])
t.sleep(2)
env.move(vels=[[-2,-2],
               [-2,-2]])
t.sleep(20)
env.close()