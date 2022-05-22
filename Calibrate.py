#!/usr/bin/env pybricks-micropython
from Robot import *

robot=Robot()

robot.wait4Button()
robot.brick.speaker.set_volume(100)
robot.brick.speaker.play_file('grace-calibrate-01.wav')
robot.calibrate()
robot.brick.speaker.play_file('grace-calibrate-02.wav')
