from dorna2 import Dorna
from time import sleep

def robot_info(robot, funcname):
    """
    Description: This function displays the commands sent to the robot and
    information stored about the robot
    Parameters: robot (obj), funcname (str)
    Returns: None
    """
    
    # displays the data in the command given to the robot and the function it's in
    print("\nTrack Command in %s" % funcname)
    print(robot.track_cmd())

def move_claw(clawOpen):
    """
    Description: This function determines whether or not the claw is open.
    If the claw is open, it closes it. If the claw is closed, it opens it. 
    Parameters: clawOpen (bool)
    Returns: j5 (float) clawOpen (bool)
    """

    # if the claw is open, it sets the claw to close and vise versa
    if clawOpen:
        j5 = -375
        clawOpen = False
    else:
        j5 = 0
        clawOpen = True

    return j5, clawOpen

def counter_j0(robot):
    """
    Description: This function is to rotate the claw to offset the rotation 
    by j0 for times when it is not perfectly 90. 
    Parameters: robot (obj)
    Returns: None
    """

    # current position of the j0 joint
    currentJ0 = robot.get_joint(0)
    if  currentJ0> 0:
        b = -90+currentJ0+0.65
    else:
        b = 90+currentJ0-0.65
    
    # moves the claw
    robot.jmove(
        rel=0,
        b=b,
        vel=200
    )

def pickup(robot, pos, clawOpen, microscope):
    """
    Description:
    Parameters: robot (obj), pos (dict), clawOpen (bool)
    Return: clawOpen (bool)
    """
    # lowers the claw
    robot.lmove(
        z = pos["z"]-59,
        vel = 50
    )
    # displays robot information
    robot_info(robot, "pickup")

    # gets the position to which the claw needs to go
    j5, clawOpen = move_claw(clawOpen)
    print(j5)
    print(clawOpen)

    # closes the claw
    robot.jmove(
        rel=0,
        j5 = j5,
        vel = 80
    )
    # displays robot information
    robot_info(robot, "pickup close claw")

    # lifts up the claw
    if microscope:
        robot.lmove(
            z=pos["z"]-57+24,
            vel = 50
        )
    else:
        robot.lmove(
        z = pos["z"], 
        vel = 50
    )
    # displays robot information
    robot_info(robot, "pickup lifts claw")

    return clawOpen

def transport(robot, pos):
    """
    Description: This function moves the robotic arm into the transportation
    position and then moves the robotic arm along the sliding rail to where it 
    needs to go. 
    Parameters: robot (obj), pos (dict)
    Returns: None
    """

    # rotates the robot to the transportation position
    robot.jmove(
        timeout=10, 
        rel=0, 
        j0=0,
        j1=100, 
        j2=-100, 
        j3=-88, 
        j4=0, 
        vel=200
    )
    # displays robot information
    robot_info(robot, "transport")

    # moves the sliding rail to the position given
    robot.jmove(
        rel=0,
        j6=pos["j6"],
        vel=120,
        accel=500,
        jerk=2000
    )
    # displays robot information
    robot_info(robot, "transport")

def action_from_microscope(robot, pos, clawOpen):
    """
    Description: This function performs the action of picking-up/placing a 
    sample to the microscope. It first moves the claw to a position in front 
    and above the microscope, then moves forward to be ontop of the microscope,
    it then lowers into the tray, then picks-up or releases the sample, then
    lifts back up, moves away from the microscope, and then lifts back up. 
    Parameters: robot (obj), pos (dict), clawOpen(bool)
    Returns: clawOpen(bool)
    -1021
    """

    # this is to lower the claw compared to initial holder position as to not hit the light
    microOffset = -33

    # displays whether or not the claw is open for debugging purposes
    print("Claw Open: %s" % clawOpen)

    # moves the robot to the position it needs to be on the slide rail
    transport(robot, pos)

    # robots the robotic arm first to avoid any obstables
    robot.jmove(
        rel=0,
        j0=pos["j0"],
        vel = 200
    )
    # displays robot information
    robot_info(robot, "action_from_microscope")

    # determines whether to move forward or backward based on which side of the table it's on
    if pos["y"] > 0:
        deltaY = 90
    else:
        deltaY = -90

    # moves the rest of the robotic arm to the initial microscope position
    robot.jmove(
        rel=0,
        x = pos["x"],
        y = pos["y"]-deltaY,
        z = pos["z"]+microOffset,
        a = pos["a"],
        d = pos["d"],
        vel = 100
    )
    # displays robot information
    robot_info(robot, "action_from_microscope")

    # moves the robotic arm into the microscope to be able to pick-up/place
    robot.lmove(
        rel=0,
        y = pos["y"],
        b = pos["b"],
        vel = 50
    )
    # displays robot information
    robot_info(robot, "action_from_microscope")

    # pickups/places the sample
    clawOpen = pickup(robot, pos, clawOpen, True)

    # moves the robotic arm out of the microscope
    robot.lmove(
        rel=0,
        y = pos["y"]-deltaY,
        z = pos["z"]+microOffset,
        b = pos["b"],
        vel = 50
    )
    # displays robot information
    robot_info(robot, "action_from_microscope")

    # moves the robotic arm back to the initial position
    move_to_initial(robot)

    return clawOpen

def action_from_holder(robot, pos, clawOpen):
    """
    Description: This function performs the action of pickup/placing something
    at a holder on the table. It firsts moves the claw to a position above the 
    holder, lowers itself into the holder, picks up or releases the something 
    and lifts back up. 
    Parameters: robot (obj), pos (dict), clawOpen(bool)
    Returns: clawOpen (bool)
    """
    # displays whether or not the claw is open for debugging purposes
    print("Claw Open: %s" % clawOpen)

    # moves the robot to the position it needs to be on the slide rail
    transport(robot, pos)

    # rotates the robotic arm first to avoid any obstables
    robot.jmove(
        rel=0,
        j0=pos["j0"],
        vel = 250
    )
    # displays robot information
    robot_info(robot, "action_from_holder")
    
    # moves the rest of the robot arm to the initial holder position
    robot.jmove(
            rel=0,
            j0=pos["j0"],
            j1=pos["j1"],
            j2=pos["j2"],
            j3=pos["j3"],
            j4=pos["j4"],
            j6=pos["j6"],
            vel = 200
        )
    # displays robot information
    robot_info(robot, "action_from_holder")

    # picks up the sample with the claw
    clawOpen = pickup(robot, pos, clawOpen, False)

    # moves the robotic arm back to the initial position
    move_to_initial(robot)

    return clawOpen

def move_to_initial(robot):
    """
    Description: This function moves the robotic arm to the initial position
    Parameters: robot (obj)
    Returns: None
    """

    # For some reason, if the all motors besides the slide rail move first, 
    # there will be no operational issues with the slide rail
    robot.jmove(
        rel=1, 
        j1=0.5, 
        j2=0.5, 
        j3=0.5, 
        j4=0.5, 
        vel=100, 
        accel=500,
        jerk=2000
    )
    # displays robot information
    robot_info(robot, "move_to_initial")

    # moves the robotic arm to the initial starting position
    robot.jmove(
        timeout=10, 
        rel=0, 
        j1=100, 
        j2=-100, 
        j3=-88, 
        j4=0, 
        vel=250
    )
    # displays robot information
    robot_info(robot, "move_to_initial")

def get_positions():
    """
    Description: This function reads a file that contains the joint and cartesian coordinate
    positions of all microscopes and sample holders on the table and saves that information. 
    Parameters: None
    Returns: positions (dict)
    """

    # positions is a dictionary of dictionaries that holds the positions
    positions = {}
    lineCount = 0
    with open("keyPositions.csv", 'r') as file:
        lineCount += 1

        for line in file:
            # each line contains the cartesian and joint system coordinates for each position
            line = line.split(",")
            print(line)

            # position is a dictionary that holds the cartesian and joint system coordinates
            position = {}
            try:
                # reads in the cartesian coordinates
                # a is rotating up&down of claw
                # b is rotating side-to-side of claw
                # c (not included) is opening/closing of claw
                # d is left/right of sliding rail
                if line[1] == "c":
                    try:
                        position["x"] = float(line[2])
                        position["y"] = float(line[3])
                        position["z"] = float(line[4])
                        position["a"] = float(line[5])
                        position["b"] = float(line[6])
                        position["d"] = float(line[7])
                    except ValueError:
                        print("Values for %s are incorrect" % line[0])
                else:
                    print("Values for %s are incorrect" % line[0])

                # reads in the joint coordinates
                # j0, j1, j2, j3, j4 are the robot's 5 main joints
                # j6 is the position of the claw
                # j7 is the position of the sliding rail
                if line[8] == "j":
                    try:
                        position["j0"] = float(line[9])
                        position["j1"] = float(line[10])
                        position["j2"] = float(line[11])
                        position["j3"] = float(line[12])
                        position["j4"] = float(line[13])
                        position["j6"] = float(line[14])
                    except ValueError:
                        print("Values for %s are incorrect" % line[0])
                else:
                    print("Values for %s are incorrect" % line[0])
            except IndexError:
                print("Improper position on line %d" % lineCount)

            # adds each position to the positions dicitonary
            positions[line[0]] = position

    return positions

def testingHolder(robot, positions, clawOpen):
    # test actions
    move_to_initial(robot)
    for i in range(4):
        clawOpen = action_from_holder(robot, positions["TestPlateHolder3"], clawOpen)
        clawOpen = action_from_holder(robot, positions["TestPlateHolder1"], clawOpen)
        clawOpen = action_from_holder(robot, positions["TestPlateHolder4"], clawOpen)

    return clawOpen

def testingMicroscope(robot, positions, clawOpen):
    # test actions
    move_to_initial(robot)
    clawOpen = action_from_microscope(robot, positions["Microscope1"], clawOpen)
    clawOpen = action_from_holder(robot, positions["TestPlateHolder3"], clawOpen)

    return clawOpen


if __name__ == "__main__":
    # connects to the robot and engages the motors
    robot = Dorna()
    print(robot.connect("192.168.2.20"))
    robot.set_motor(1)
    clawOpen = True

    # making sure the claw is open
    robot.jmove(
        rel=0,
        j5 = 0,
        vel = 70
    )

    # gets the positions of the microscopes and plate holders
    positions = get_positions()
    print(positions)

    # testingHolder(robot, positions, clawOpen)
    # testingMicroscope(robot, positions, clawOpen)

    move_to_initial(robot)
    
    clawOpen = action_from_holder(robot, positions["TestPlateHolder1"], clawOpen)
    clawOpen = action_from_microscope(robot, positions["Microscope1"], clawOpen)
    clawOpen = action_from_holder(robot, positions["TestPlateHolder3"], clawOpen)
    clawOpen = action_from_holder(robot, positions["TestPlateHolder2"], clawOpen)
    clawOpen = action_from_microscope(robot, positions["Microscope1"], clawOpen)
    clawOpen = action_from_holder(robot, positions["TestPlateHolder3"], clawOpen)
    
    for i in range(2):
        robot.jmove(
            rel=1,
            j3 = 5,
            vel = 250,
            accel = 1000,
            jerk=2500
        )
        robot.jmove(
            rel=1,
            j3 = -5,
            vel = 250,
            accel = 1000,
            jerk=2500
        )

    # finishes the sequence
    robot.close()