from dorna2 import Dorna
from time import sleep

def robot_info(robot):
    """
    Description: This function displays the commands sent to the robot and
    information stored about the robot
    Parameters: robot (obj)
    Returns: None
    """
    
    print("\nTrack Command in %s")
    print(robot.track_cmd())
    print("Sys Data")
    print(robot.sys())

def move_claw(clawOpen):
    """
    Description: This function determines whether or not the claw is open.
    If the claw is open, it closes it. If the claw is closed, it opens it. 
    Parameters: clawOpen (bool)
    Returns: clawOpen (bool)
    """

    if clawOpen:
        j5 = -240
        clawOpen = False
    else:
        j5 = 0
        clawOpen = True

    return j5, clawOpen

def counter_j0(robot, pos):
    currentJ0 = robot.get_joint(0)
    if  currentJ0> 0:
        b = -90+currentJ0+0.65
    else:
        b = 90+currentJ0-0.65
    robot.jmove(
        rel=0,
        b=b,
        vel=50
    )


def action_from_microscope(robot, pos, clawOpen):
    """
    Description: This function performs the action of picking-up/placing a 
    sample to the microscope. It first moves the claw to a position in front 
    and above the microscope, then moves forward to be ontop of the microscope,
    it then lowers into the tray, then picks-up or releases the sample, then
    lifts back up, moves away from the microscope, and then lifts back up. 
    Parameters: robot (obj), pos (dict), clawOpen(bool)
    Returns: clawOpen(bool)
    """

    print("Claw Open: %s" % clawOpen)

    transport(robot, pos)

    if pos["y"] > 0:
        deltaY = 140
    else:
        deltaY = -140

    robot.jmove(
        rel=0,
        x = pos["x"],
        y = pos["y"]-deltaY,
        z = pos["z"],
        a = pos["a"],
        d = pos["d"],
        vel = 50
    )
    sleep(0.5)

    robot.lmove(
        rel=0,
        y = pos["y"],
        b = pos["b"],
        vel = 25
    )

    clawOpen = pickup(robot, pos, clawOpen)

    robot.lmove(
        rel=0,
        y = pos["y"]-deltaY,
        b = pos["b"],
        vel = 25
    )

    return clawOpen

def pickup(robot, pos, clawOpen):
    """
    Description:
    Parameters: robot (obj), pos (dict), clawOpen (bool)
    Return: clawOpen (bool)
    """
    # lowers the claw
    robot.lmove(
        z = pos["z"]-50,
        vel = 40
    )

    # gets the position to which the claw needs to go
    j5, clawOpen = move_claw(clawOpen)
    print(j5)
    print(clawOpen)

    # closes the claw
    robot.jmove(
        rel = 0, 
        j5 = j5,
        vel = 80, 
    )

    # lifts up the claw
    robot.lmove(
        z = pos["z"]-20, 
        vel = 60
    )
    sleep(0.5)

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

    print("Claw Open: %s" % clawOpen)

    # moves the robot to the position it needs to be on the slide rail
    transport(robot, pos)

    # robots the robotic arm first to avoid any obstables
    robot.jmove(
        rel=0,
        j0=pos["j0"],
        vel = 100
    )
    
    # moves the rest of the robot arm to the position
    robot.jmove(
            rel=0,
            j0=pos["j0"],
            j1=pos["j1"],
            j2=pos["j2"],
            j3=pos["j3"],
            j4=pos["j4"],
            j6=pos["j6"],
            vel = 70
        )
    sleep(0.5)

    # picks up the sample with the claw
    clawOpen = pickup(robot, pos, clawOpen)
    
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
        j1=90, 
        j2=-90, 
        j3=-90, 
        j4=0, 
        vel=100
    )

    # moves the sliding rail to the position given
    robot.jmove(
        rel=0,
        j6=pos["j6"],
        vel=120,
        accel=500,
        jerk=2000
    )

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
    robot_info(robot)

    # moves the robotic arm to the initial starting position
    robot.jmove(
        timeout=10, 
        rel=0, 
        j1=90, 
        j2=-90, 
        j3=-90, 
        j4=0, 
        vel=100
    )
    # displays robot information
    robot_info(robot)

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
    clawOpen = action_from_holder(robot, positions["TestPlateHolder3"], clawOpen)
    clawOpen = action_from_holder(robot, positions["TestPlateHolder1"], clawOpen)
    clawOpen = action_from_holder(robot, positions["TestPlateHolder2"], clawOpen)
    clawOpen = action_from_holder(robot, positions["TestPlateHolder3"], clawOpen)
    move_to_initial(robot)

def testingMicroscope(robot, positions, clawOpen):
    move_to_initial(robot)
    clawOpen = action_from_microscope(robot, positions["TestPlateHolder4"], clawOpen)
    clawOpen = action_from_holder(robot, positions["TestPlateHolder1"], clawOpen)
    move_to_initial(robot)


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
    testingMicroscope(robot, positions, clawOpen)
    

    # finishes the sequence
    robot.close()