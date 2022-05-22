#!/usr/bin/env pybricks-micropython
from Robot import *
robot=Robot ()

def thefinalcountdown():
    #=============== START (in base) =======================
    robot.gyroSet(0)
    #=============== PULL-UP BAR ==========================
    if True:
        robot.drive(33, 550)                        #drive towards first line
        robot.turn(75, 450)                         #turn
        robot.drive2Line(450, 1, 0)                 #drive through pull-up bar
        robot.turn(85, 400)
        robot.rearMotor.run_time(400, 4000, Stop.COAST, False)        #raising hooks
        robot.lineFollow2Line(350, False, True)
        #robot.rearMotor.run_time(-800, 6000, Stop.COAST, False) 
        robot.drive(12, 550)                                          #drive forward and dump blocks
        robot.rearMotor.run_time(-800, 6000, Stop.COAST, False)       #starting lowering hook
        robot.frontMotor.run_time(-800, 1000)
        robot.drive(1,-450)
        robot.turn(89, 400)
        robot.drive(15, -500)                       #back up      
        robot.rearMotor.run_time(-800, 5500,Stop.COAST, False)        #lifting robot
        robot.frontMotor.run_time(800, 500)
        wait(5000)
 
robot.wait4Button()
thefinalcountdown()
