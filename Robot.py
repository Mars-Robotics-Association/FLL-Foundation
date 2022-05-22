#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from math import copysign, sin
from os import path


class LightSensor(ColorSensor):
    black = 20
    white = 80
    line = 50

    def __init__(self, port, low = 10, high = 120):
        super().__init__(port)
        self.black = low + (high-low)*.25
        self.white = low + (high-low)*.8
        self.line = low + (high-low)*.5

    def light(self):
        return sum(self.rgb())

    def isWhite(self):
        if self.light()>=self.white:
            return True
        else:
            return False

    def isBlack(self):
        if self.light()<=self.black:
           # brick.sound.beep(300, 10, 20)
            return True
        else:
            return False

    def waitForWhite(self):
        while not self.isWhite():
            #brick.sound.beep(300, 10, 20)
            pass

    def waitForBlack(self):
        while not self.isBlack():
            pass

    def waitForLine(self):
        self.waitForWhite()
        self.waitForBlack()
    
class Robot():
    def __init__(self):
        self.brick = EV3Brick()
        self.frontMotor=Motor(Port.D)
        self.rearMotor=Motor(Port.A)
        self.leftMotor=Motor(Port.C)
        self.rightMotor=Motor(Port.B)

        if path.exists('sensorpoints.py'):
            import sensorpoints
            self.leftSensor=LightSensor(Port.S3, sensorpoints.leftLow, sensorpoints.leftHigh)
            self.rightSensor=LightSensor(Port.S2, sensorpoints.rightLow, sensorpoints.rightHigh)

        else: 
            self.leftSensor=LightSensor(Port.S3, 10, 105)
            self.rightSensor=LightSensor(Port.S2, 20, 160)

        self.gyroSensor=GyroSensor(Port.S1)
        wait(100)
        self.gyroSensor.speed()
        self.gyroSensor.angle()
        wait(500)
        self.gyroSensor.reset_angle(0.0)
        wait(200)

    def calibrate(self):
        rightHigh = 40
        rightLow = 70
        leftHigh = 40
        leftLow = 70

        timer = StopWatch()
        self.moveSteering(0, 125)
        while timer.time() < 5000:
            if self.rightSensor.light() > rightHigh:
                rightHigh = self.rightSensor.light()
            if self.rightSensor.light() < rightLow:
                rightLow = self.rightSensor.light()
            if self.leftSensor.light() > leftHigh:
                leftHigh = self.leftSensor.light()
            if self.leftSensor.light() < leftLow:
                leftLow = self.leftSensor.light()
        self.stop()
        # write results to file
        with open('sensorpoints.py', 'w') as myFile:
            myFile.write('leftLow = ')
            myFile.write(str(leftLow))
            myFile.write('\nrightLow = ')
            myFile.write(str(rightLow))
            myFile.write('\nleftHigh = ')
            myFile.write(str(leftHigh))
            myFile.write('\nrightHigh = ')
            myFile.write(str(rightHigh))
        
    def moveSteering(self, steering, speed):
        leftMotorSpeed = speed * min(1, 0.02 * steering + 1)
        rightMotorSpeed = speed * min (1, -0.02 * steering + 1)
        self.leftMotor.run(leftMotorSpeed)
        self.rightMotor.run(rightMotorSpeed)

    def drive(self, distance, speed, time=8, kSteering=1): 
        # Startup for gyro
        #kSteering=5     # Steering coefficient
        startDegrees=self.gyroSensor.angle()
        # Startup for ramp speed
        if distance < 0 :
            distance = abs(distance)
            speed = -speed
        rotation= distance*51.9
        self.rightMotor.reset_angle(0)
        #  Loop
        while abs(self.rightMotor.angle()) < abs(rotation) :
            # Do the gyro steering stuff
            currentDegrees=self.gyroSensor.angle()
            errorGyro=currentDegrees-startDegrees
            # Do the ramp speed stuff   
            rampSpeed=min(sin(abs(self.rightMotor.angle()) / rotation * 3.14), abs(speed)-100)
            self.moveSteering(errorGyro*kSteering*copysign(1, speed), rampSpeed * speed + copysign(100, speed))
        # Exit
        self.stop()

    def turn(self, angle, speed, time=5):
        # Startup
        steering = 100
        kTurn=0.01
        offset = 20
        timer = StopWatch()   
        # Loop
        while (abs(self.gyroSensor.angle() - angle) > 0)  & (timer.time() < time * 1000):
            error = self.gyroSensor.angle() - angle
            #if error > 0 : 
            #    steering = 100
            #else:
            #    steering = -100
            self.moveSteering(steering, speed * error * kTurn + copysign(offset,error))
        # Exit
        self.stop(Stop.HOLD)
        print("turning to: ", angle, "  gyro: ", self.gyroSensor.angle())

    def lineFollow2Line(self, speed, rightSide=True, rightFollow=True):
        # Startup
        if rightFollow:
            followSensor = self.rightSensor
            stopSensor = self.leftSensor
        else:
            followSensor = self.leftSensor
            stopSensor = self.rightSensor
        if rightSide:
            kSide = 1
        else:
            kSide = -1

        lastError = 0
        # Loop
        while not stopSensor.isWhite():
            error = followSensor.line - followSensor.light()
            pCorrection = error * 0.25
            dError = lastError - error
            dCorrection = dError * 1.25
            self.moveSteering((pCorrection - dCorrection)*kSide, speed)
            lastError = error
        self.stop()

    def lineFollow4Time(self, speed, time, rightSide=True, rightFollow=True):
            # Startup
        if rightFollow:
            followSensor = self.rightSensor
        else:
            followSensor = self.leftSensor
        if rightSide:
            kSide = 1
        else:
            kSide = -1
        timer = StopWatch()
        lastError = 0
        # Loop
        while timer.time() < time * 1000:
            # Experimental settings: kp = 0.2, kd = 0.4
            error = followSensor.line - followSensor.light()
            pCorrection = error * 0.25  # Used to be 0.25
            dError = lastError - error
            dCorrection = dError * 1.2  # Used to be 1.25
            self.moveSteering((pCorrection - dCorrection)*kSide, speed)
            lastError = error
            #wait(10)
        self.stop()

    def turn2Line(self, speed, rightStop = True, time=5):
        if rightStop:
            stopSensor = self.rightSensor
        else:
            stopSensor = self.leftSensor
        self.moveSteering(100, speed)
        stopSensor.waitForLine()
        self.stop()
    
    def drive2Line(self, speed, distanceBefore, distanceAfter, rightStop=True):
        # Startup
        if rightStop:
            stopSensor = self.rightSensor
        else:
            stopSensor = self.leftSensor
        self.drive(distanceBefore, speed)

        # Loop
        #while self.rightSensor.rgb() < 90:
        #    self.moveSteering(0, 70)
        # Start Driving
        # *** OLD ONE *** self.moveSteering(0, 250)
        self.moveSteering(0, 0.5*speed)
        # execute function wait until we detect a line
        stopSensor.waitForLine()
        self.stop(Stop.HOLD)

        # Exit
        self.drive(distanceAfter, speed)

    def stop(self, brakeType=Stop.HOLD):
        # 3 options: Stop.BRAKE, Stop.COAST, Stop.HOLD
        self.rightMotor.stop(brakeType)
        self.leftMotor.stop(brakeType)

    def wait4Button(self):
        self.brick.speaker.beep()
        while not any (self.brick.buttons.pressed()):
            pass
        
    def gyroSet(self, newAngle=0):
        #while not self.gyroCheck():
           # pass
        startAngle = self.gyroSensor.angle()
        wait(100)
        #self.gyroSensor.speed()
        #self.gyroSensor.angle()
        wait(500)
        self.gyroSensor.reset_angle(newAngle)
        wait(500)
        print("Gyro Start: ", startAngle, "Gyro Reset. Goal: ", newAngle, "  Actual: ", self.gyroSensor.angle())

    def gyroCheck(self):
        angle1 = self.gyroSensor.angle()
        wait(1000)
        if self.gyroSensor.angle() != angle1:
            print("drift detected")
            self.brick.speaker.say("grace forgot her necklace")
            return False
        else:
            print("absence of drift")
            self.brick.speaker.say("grace remebered her necklace")
            return True


