#!/usr/bin/env python3

import time
import wpilib
import sys

class MyRobot(wpilib.SampleRobot):
    '''Main robot class'''

    
    def robotInit(self):
        '''Robot-wide initialization code should go here'''

        self.SPEED = .125 #constant speed in SECONDS/METER NO TOUCHY

        self.lstick = wpilib.Joystick(0) #xbox controller
        self.rstick = wpilib.Joystick(1)
        
        self.lfMotor = wpilib.Jaguar(1) #init left front motor with port 1
        self.rfMotor = wpilib.Jaguar(2) #init right front motor with port 2
        self.lbMotor = wpilib.Jaguar(3) #init left back motor with port 3
        self.rbMotor = wpilib.Jaguar(4) #init right back motor with port 4
        
        self.left = wpilib.SpeedControllerGroup(self.lfMotor, self.lbMotor)
        self.right = wpilib.SpeedControllerGroup(self.rfMotor, self.rbMotor) #init speed control groups for tread-like movement

        # angle gets automatically updated as robot moves
        self.gyro = wpilib.AnalogGyro(1)
        
        self.robot_drive = wpilib.RobotDrive(self.left, self.right) #init drive with wheel groups
        
        self.motor = wpilib.Jaguar(5) #currently unused(climb)
        
        self.limit1 = wpilib.DigitalInput(1)	# simulator walls
        self.limit2 = wpilib.DigitalInput(2)
        
        self.position = wpilib.AnalogInput(2) #position from something?
        #self.testMotor(self.lfMotor)
        #self.testMotor(self.lbMotor)
        #self.testMotor(self.rfMotor)
        #self.testMotor(self.rbMotor)


    def testMotor(self, motor):
        motor.setPosition(0) #ensure motor is at pos 0
        motor.setSpeed(1.0) #test motors by setting speed
        time.sleep(5)
        motor.setSpeed(0)
        if motor.getPosition() <=1:
            print("motor failure: " + str(motor.getPosition()))
            sys.exit()





    def disabled(self):
        '''Called when the robot is disabled'''
        while self.isDisabled(): # pause timer, doubly shutdown
            wpilib.Timer.delay(0.01)

    def autonomous(self):
        '''Called when autonomous mode is enabled'''
        wpilib.DriverStation.getInstance().getGameSpecificMessage() #get switch-scale-switch from your start
        timer = wpilib.Timer()
        timer.start()
        while self.isAutonomous() and self.isEnabled():

            if timer.get() < 15*self.SPEED:
                self.robot_drive.arcadeDrive(-10, 0)
            else:
                if timer.get()< 5:
                    self.robot_drive.arcadeDrive(-10, 4) #turn second, positive = right
                else:
                    self.robot_drive.arcadeDrive(0, 0)

            wpilib.Timer.delay(0.01)

    def operatorControl(self):
        '''Called when operation control mode is enabled'''
        
        timer = wpilib.Timer()
        timer.start()

        while self.isOperatorControl() and self.isEnabled():
            
            self.robot_drive.arcadeDrive(self.lstick)

            # Move a motor with a Joystick
            y = self.rstick.getY()
            
            # stop movement backwards when 1 is on
            if self.limit1.get():
                y = max(0, y)
                
            # stop movement forwards when 2 is on
            if self.limit2.get():
                y = min(0, y)
                
            self.motor.set(y)

            wpilib.Timer.delay(0.04)

if __name__ == '__main__':
    
    wpilib.run(MyRobot,
               physics_enabled=True)

