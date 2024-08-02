import pygame
from dorna2 import Dorna
from time import sleep
import json

class RoboticArmController:
    def __init__(self, *args):
        # Initialize Pygame
        pygame.init()

        # Initialize Xbox Controller
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()

        # initializes the coordinate system, the senstivity, and the counter for new positions
        self.coordsys = "cartesian"
        self.sensitivity = 1
        self.pos_counter = 0

        # if this class is initialized in the chatbot extension
        if len(args) > 1: 
            self.robot = args[0]
            self.robot.connect("192.168.2.20")
            self.positions = args[1]
        else:
            self.robot = Dorna()
            self.robot.connect("192.168.2.20")
            self.robot.set_motor(1)
            with open("positions.json", 'r') as positions_file: 
                self.positions = json.load(positions_file)
        
    def record_pos(self):
        """
        Description: This function records the position of the robot, 
        saves it, and writes it in the positions json file
        Parameter: self (obj)
        Return Val: None
        """
        pos_joint = self.robot.get_all_joint()
        pos_cartesian = self.robot.get_all_pose()
        current_pos = {
            "x": pos_cartesian[0],
            "y": pos_cartesian[1],
            "z": pos_cartesian[2],
            "a": pos_cartesian[3],
            "b": pos_cartesian[4],
            "d": pos_cartesian[6],
            "j0": pos_joint[0],
            "j1": pos_joint[1],
            "j2": pos_joint[2],
            "j3": pos_joint[3],
            "j4": pos_joint[4],
            "j6": pos_joint[6],
        }
        self.positions["New Position %d" % self.pos_counter] = current_pos

        with open("positions.json", 'w') as filename:
            json.dump(self.positions, filename, indent = 4)
        
        self.pos_counter += 1
    
    """
    Description: These functions take the input from the controller and moves in the  
    cartesian coordinate system accordingly
    Parameter: self (obj), val (float)
    Return Val: None
    """
    def move_x(self, val):
        deltaX = val*self.sensitivity
        self.robot.lmove(rel=1, x=deltaX, vel=100)
        print("Moving X by this value: %f" % deltaX)
        print("Current Pos: %s" % self.robot.get_all_pose())
    def move_y(self, val):
        deltaY = val*self.sensitivity
        self.robot.lmove(rel=1, y=deltaY, vel=100)   
        print("Moving Y by this value: %f" % deltaY)
        print("Current Pos: %s" % self.robot.get_all_pose())
    def move_z(self, val):
        deltaZ = val*self.sensitivity
        self.robot.lmove(rel=1, z=deltaZ, vel=100)   
        print("Moving Z by this value: %f" % deltaZ)
        print("Current Pos: %s" % self.robot.get_all_pose())
    def move_a(self, val):
        deltaA = val*self.sensitivity
        self.robot.lmove(rel=1, a=deltaA, vel=100)   
        print("Moving A by this value: %f" % deltaA)
        print("Current Pos: %s" % self.robot.get_all_pose())
    def move_b(self, val):
        deltaB = val*self.sensitivity
        self.robot.lmove(rel=1, b=deltaB, vel=100)   
        print("Moving B by this value: %f" % deltaB)
        print("Current Pos: %s" % self.robot.get_all_pose())
    def move_c(self, val):
        deltaC = val*self.sensitivity
        self.robot.lmove(rel=1, c=deltaC, vel=100)   
        print("Moving C by this value: %f" % deltaC)
        print("Current Pos: %s" % self.robot.get_all_pose())
    def move_d(self, val):
        deltaD = val*self.sensitivity
        self.robot.lmove(rel=1, d=deltaD, vel=100)   
        print("Moving D by this value: %f" % deltaD)
        print("Current Pos: %s" % self.robot.get_all_pose())
    
    """
    Description: These functions take the input from the controller and moves in the  
    joint coordinate system accordingly
    Parameter: self (obj), val (float)
    Return Val: None
    """
    def move_j0(self, val):
        deltaJ0 = val*self.sensitivity
        j0 = self.robot.get_joint(0)
        self.robot.jmove(rel=1, j0=deltaJ0, vel=100)
        print("Moving j0 by this value: %f" % deltaJ0)
        print("Current Pos: %s" % self.robot.get_all_joint())
    def move_j1(self, val):
        deltaJ1 = val*self.sensitivity
        j1 = self.robot.get_joint(1)
        self.robot.jmove(rel=1, j1=deltaJ1, vel=100)
        print("Moving j1 by this value: %f" % deltaJ1)
        print("Current Pos: %s" % self.robot.get_all_joint())
    def move_j2(self, val):
        deltaJ2 = val*self.sensitivity
        j2 = self.robot.get_joint(2)
        self.robot.jmove(rel=1, j2=deltaJ2, vel=100)
        print("Moving j2 by this value: %f" % deltaJ2)
        print("Current Pos: %s" % self.robot.get_all_joint())
    def move_j3(self, val):
        deltaJ3 = val*self.sensitivity
        j3 = self.robot.get_joint(3)
        self.robot.jmove(rel=1, j3=deltaJ3, vel=100)
        print("Moving j3 by this value: %f" % deltaJ3)
        print("Current Pos: %s" % self.robot.get_all_joint())
    def move_j4(self, val):
        deltaJ4 = val*self.sensitivity
        j4 = self.robot.get_joint(4)
        self.robot.jmove(rel=1, j4=deltaJ4, vel=100)
        print("Moving j4 by this value: %f" % deltaJ4)
        print("Current Pos: %s" % self.robot.get_all_joint())
    def move_j5(self, val):
        deltaJ5 = val*self.sensitivity
        j5 = self.robot.get_joint(5)
        self.robot.jmove(rel=1, j5=deltaJ5, vel=100)
        print("Moving j5 by this value: %f" % deltaJ5)
        print("Current Pos: %s" % self.robot.get_all_joint())
    def move_j6(self, val):
        deltaJ6 = val*self.sensitivity
        j6 = self.robot.get_joint(6)
        self.robot.jmove(rel=1, j6=deltaJ6, vel=100)
        print("Moving j6 by this value: %f" % deltaJ6)
        print("Current Pos: %s" % self.robot.get_all_joint())

    def calibrate_arm(self):
        """
        Description: This function runs a while loop until stopped from by the 
        controller. This while loop continuously takes input from the controller 
        to move the robotic arm, records the position of the robotic arm, and 
        updates settings. 
        Parameters: self (obj)
        Return Val: None
        """
        while(self.controller.get_button(7) == 0):
            # updates the event log of the controller
            pygame.event.pump()

            # record the position if button B is pressed
            if self.controller.get_button(1) != 0:
                self.record_pos()
                sleep(0.3)

            # increase the sensitivty if button Y is pressed
            if self.controller.get_button(0) != 0:
                self.sensitivity *= 0.5
                print("Sensitivity is now %f" % self.sensitivity)
                sleep(0.3)
            # decrease the sensitivity if button A is pressed
            if self.controller.get_button(3) != 0:
                self.sensitivity *= 2
                print("Sensitivity is now %f" % self.sensitivity)
                sleep(0.3)

            # change the coordinate system between joint and cartesian is button X is pressed
            if self.controller.get_button(2) != 0:
                if self.coordsys != "joint":
                    self.coordsys = "joint"
                else:
                    self.coordsys = "cartesian"
                print("Coordinate system is now %s" % self.coordsys)
                sleep(0.3)

            # controls for the cartesian coordinate system
            if self.coordsys == "cartesian":
                # moves the robotic arm in the X-axis if the left joystick is moved left or right
                if (self.controller.get_axis(0) < -0.05) or (self.controller.get_axis(0) > 0.05):
                    self.move_x(self.controller.get_axis(0))
                # moves the robotic arm in the Y-axis if the left joystick is moved up or down
                if (self.controller.get_axis(1) < -0.05) or (self.controller.get_axis(1) > 0.05):
                    self.move_y(-self.controller.get_axis(1))
                # moves the robotic arm in the Z-axis if the right joystick is moved up or down
                if (self.controller.get_axis(3) < -0.15) or (self.controller.get_axis(3) > 0.15):
                    self.move_z(-self.controller.get_axis(3))
                
                # if the dpad is pushed
                if self.controller.get_hat(0) != (0,0):
                    # moves the claw up or down if the dpad is moved up or down
                    self.move_a(self.controller.get_hat(0)[1])
                    # moves the claw side to side if the dpad is moved left or right
                    self.move_b(self.controller.get_hat(0)[0])
                    sleep(0.3)
                
                # closes the claw if the left bumper is pressed
                if self.controller.get_button(4) != 0:
                    self.move_c(-1)
                    sleep(0.3)
                # opens the claw if the right bumper is pressed
                if self.controller.get_button(5) != 0:
                    self.move_c(1)
                    sleep(0.3)

                # moves the slide rail to the right if the right trigger is pressed
                if self.controller.get_axis(4) > 0:
                    self.move_d(1)
                # moves the slide rail to the left if the left trigger is pressed
                if self.controller.get_axis(5) > 0:
                    self.move_d(-1)
            
            # controls for the joint coordinate system
            else:
                # rotates j0 based on the inputs from moving the left stick left or right
                if (self.controller.get_axis(0) < -0.05) or (self.controller.get_axis(0) > 0.05):
                    self.move_j0(self.controller.get_axis(0))
                # rotates j1 based on the inputs from moving the left stick up or down
                if (self.controller.get_axis(1) < -0.05) or (self.controller.get_axis(1) > 0.05):
                    self.move_j1(-self.controller.get_axis(1))
                # rotates j2 based on the inputs from moving the right stick up or down
                if (self.controller.get_axis(3) < -0.15) or (self.controller.get_axis(3) > 0.15):
                    self.move_j2(-self.controller.get_axis(3))
                
                # if the dpad is pushed
                if self.controller.get_hat(0) != (0,0):
                    # moves the claw up or down if the dpad is moved up or down
                    self.move_j3(self.controller.get_hat(0)[1])
                    # moves the claw side to side if the dpad is moved left or right
                    self.move_j4(self.controller.get_hat(0)[0])
                    sleep(0.3)

                # closes the claw if the left bumper is pressed
                if self.controller.get_button(4) != 0:
                    self.move_j5(-1)
                    sleep(0.3)
                # opens the claw if the right bumper is pressed
                if self.controller.get_button(5) != 0:
                    self.move_j5(1)
                    sleep(0.3)

                # moves the slide rail to the right if the right trigger is pressed
                if self.controller.get_axis(4) > 0:
                    self.move_j6(1)
                # moves the slide rail to the left if the left trigger is pressed
                if self.controller.get_axis(5) > 0:
                    self.move_j6(-1)


        pygame.quit()
        self.robot.close()

if __name__ == "__main__":
    # """
    controller = RoboticArmController()
    controller.calibrate_arm()
    """
    # Initialize Pygame
    pygame.init()

    # Initialize Xbox Controller
    pygame.joystick.init()
    controller = pygame.joystick.Joystick(0)
    controller.init()

    while(controller.get_button(2) == 0):
        pygame.event.pump()
        print("Axis-0")
        print(controller.get_axis(0))
        print("Axis-1")
        print(controller.get_axis(1))
        print("Axis-3")
        print(controller.get_axis(3))
        print("L/R Dpad")
        print(controller.get_hat(0)[0])
        print("U/D Dpad")
        print(controller.get_hat(0)[1])
        print("Left Bumper")
        print(controller.get_button(4))
        print("Right Bumper")
        print(controller.get_button(5))
        print("Left Trigger")
        print(controller.get_axis(4))
        print("Right Trigger")
        print(controller.get_axis(5))
        print("Start Button")
        print(controller.get_button(7))
        print("-----------------------------------")
        sleep(1)
    # """
    """
        # Connect to Dorna2 Arm
        robot = Dorna()
        robot.connect("192.168.2.20")
        robot.set_motor(1)
    
    try:
        while True:
            move_arm(controller, robot)
    except KeyboardInterrupt:
        print("Exiting program")
    finally:
        robot.close()
    
        """
    pygame.quit()
    