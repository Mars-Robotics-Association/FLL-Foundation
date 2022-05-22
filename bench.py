#!/usr/bin/env pybricks-micropython
from Robot import *
robot=Robot ()

def bench():
    robot.drive(16, 550)
    wait(500)
    robot.moveSteering(0, 550)
    wait(1000)
    robot.drive(15, -550)

robot.wait4Button
bench()

