#!/usr/bin/env pybricks-micropython
from Robot import *

robot=Robot()

def dancingqueen():
    #=============== START (in base) =================

    #============ STEP COUNTER =======================
    if True:
        robot.drive(26, 550)            # Drive out of base (fast)
        robot.moveSteering(1, 40)       # Push Step Counter very slowly
        wait (10200)
        robot.stop()                    # Done with Step counter
        robot.turn(-10, 550, .5)
        robot.drive(4, -400)
        robot.turn(35, 550)
        robot.drive2Line(300, 4, 3.1)
        robot.turn2Line(150, True)
        robot.lineFollow4Time(250, 2, False)    # (250, 3, False)
    #===================== TREADMILL =======================
    if True:
        robot.lineFollow2Line(200, False)       # (200, False)
        print("Gyro Angle = ", robot.gyroSensor.angle())
        robot.gyroSet(0)
        robot.turn(2, 550)
        # ------------ Checkpoint at Wheel Thing -------------
        robot.frontMotor.run(800)
        robot.drive(6.3, 450)
        wait(7700)
        robot.stop()
        robot.frontMotor.stop()
        robot.frontMotor.run(-750)
        # -------------- End of Wheel Thing ---------------------
        robot.turn(0, 550, .5)
        robot.drive2Line(-350, 0.5, 2.5, False) #back away from treadmill
        robot.frontMotor.stop()

    #=================== ROWING MACHINE ===================
    if True:
        robot.turn(-90, 350)
        robot.drive(13.5, -350) #going towards rowing machine  *** was (14, -350)
        robot.turn(-185 , 350)                                   # Was (-190, 350)
        #robot.rearMotor.run_time(350, 3000) #raising forklift
        robot.drive(3.3, -300) #At weigh thing
        robot.rearMotor.run_time(-750, 1000)#lowering forklift
        robot.drive(5, 300)
        wait(500)
    #================= WEIGHT MACHINE =====================
    if True:
        robot.rearMotor.run_time(750, 3250, Stop.COAST, False) # raise all the way up
        wait(1500)
        robot.turn(-84, 250) # Currently -86  Was as low as -78
        robot.drive(11.4, -550) # at weight machine #18.4
        robot.turn(-90, 550)
        robot.drive(7, -550)
        robot.gyroSet(-90)
        wait(500)
        robot.drive(4.8, 400)
        robot.turn(-105, 200, 0.8)
        robot.rearMotor.run(-750) # lowering forklift
        wait(3500)
        robot.rearMotor.stop()
        robot.rearMotor.run_time(750, 1500, Stop.COAST, False)
        robot.drive(4.5, 300)
        robot.turn(-155, 550)
        #robot.rearMotor.stop()

    #------------------- Line Stuff -----------------------
    if True:
        robot.drive2Line(300, 0, 0, False)  # driving away from weight machine to line 
        robot.lineFollow4Time(200, 1.5, True, False)
        robot.lineFollow2Line(200, True, False)
        robot.rearMotor.run_time(-650, 1600, Stop.COAST, False)
        robot.drive(3, 250)
    
    #================== SLIDE =====================
    if True:
        robot.lineFollow2Line(300, True, False)
        robot.gyroSet(-180)
        robot.turn(-183, 400)
        robot.drive(12.8, 500)
        #robot.turn(-188, 400)
        robot.rearMotor.run_time(750, 2200, Stop.COAST, False) # raising forklift
        robot.turn(-220, 100)

    #=============== COLOR BOXES ===================
    if True:
        robot.turn(-200, 500, 1)
        robot.drive2Line(300, 3, 3.5)
        robot.rearMotor.run_time(-750, 3200, Stop.COAST, False) # lowering forklift for basketball 
        robot.turn2Line(150, True)

    #============= BASKETBALL ================
    if True:
        robot.lineFollow2Line(350, False, True) # at color blocks
        robot.gyroSet(-270)
        robot.drive(2, 100) #hits color boxes
        robot.drive(6, -350)
        robot.turn(-365, 350)
        robot.drive(7.6, -350)  
        robot.turn(-415, 325, 0.6) # under hoop  Was at (-415, 400, 0.5)
        robot.rearMotor.run_time(750, 5000) # raising hoop
        robot.turn(-380, 400)
        robot.drive(30, -550)

def thefinalcountdown():
    #=============== START (in base) =======================
    robot.gyroSet(0)
    #=============== PULL-UP BAR ==========================
    if True:
        robot.drive(33, 550)                        #drive towards first line
        robot.turn(75, 450)                         #turn
        robot.drive2Line(450, 1, 0)                 #drive through pull-up bar
        robot.turn(85, 400)
        robot.rearMotor.run_time(300, 4000, Stop.COAST, False)         #raising hooks
        robot.lineFollow2Line(350, False, True)
        robot.rearMotor.run_time(800, 2000, Stop.COAST, False)
        wait(1000)
        robot.rearMotor.run_time(-700, 5500, Stop.COAST, False)       #start raising arms
        robot.drive(12, 550)                                          #drive forward and dump blocks      
        robot.frontMotor.run_time(-800, 800)
        robot.drive(1,-450)
        robot.turn(88, 400)
        robot.drive(15, -500)                                          #back up      
        robot.rearMotor.run_time(-800, 5500,Stop.COAST, False)        #lifting robot
        robot.frontMotor.run_time(800, 500)
        wait(5000)

def bench():
    robot.drive(16, 550)
    wait(500)
    robot.moveSteering(0, 550)
    wait(1000)
    robot.drive(15, -550)


print("Gyro Angle = ", robot.gyroSensor.angle())
#robot.gyroCheck()
clock = StopWatch()
robot.wait4Button()
dancingqueen()
robot.wait4Button()
bench()
robot.wait4Button()
thefinalcountdown()


if False:
    robot.lineFollow2Line(350, False)

print ("Time = ", clock.time())
print("Gyro Angle = ", robot.gyroSensor.angle())



# Coach's Notes:
# IMPORTANT:
# ___ Tweak the timing for pneumatics (slower lift, faster lower)
# ___ Tweak the blocker dropper attachment (slower and lower)
# ___ Speed up - take 3-5 seconds off the time:
#       - Lower lift at weight machine earlier
#       - Reduce time lifting basketball
#       - Remove one of the gyro resets
#       - Remove pause before dumping blocks
#
# OPTIONAL: