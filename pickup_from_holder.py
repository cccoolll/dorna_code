from dorna2 import Dorna
from time import sleep

def robot_info(robot):
    print("\nTrack Command")
    print(robot.track_cmd())
    print("Sys Data")
    print(robot.sys())

def pickup(robot, positions, location):
    print(list(positions))
    numSteps = 0
    velocities = [50, 5]
    for item in list(positions):
        if location in item:
            numSteps += 1
            pos = positions[location+str(numSteps)]
            robot.lmove(
                rel=0,
                x=pos["x"],
                y=pos["y"],
                z=pos["z"],
                a=pos["a"],
                b=pos["b"],
                c=pos["c"],
                d=pos["d"],
                vel=velocities[numSteps-1]
            )
             

def move_to_initial_pose(robot, pos, velo):
    # For some reason, if the all motors besides the slide rail move first, there will be no operational issues with the slide rail
    robot.jmove(
        rel=1, 
        j0=0.5, 
        j1=0.5, 
        j2=0.5, 
        j3=0.5, 
        j4=0.5, 
        vel=velo, 
        accel=500,
        jerk=2000
    )
    robot_info(robot)

    # moves the robotic arm to the initial starting position
    robot.jmove(
        timeout=10, 
        rel=0, 
        j0=pos["j0"], 
        j1=pos["j1"], 
        j2=pos["j2"], 
        j3=pos["j3"], 
        j4=pos["j4"], 
        j5=pos["j5"],
        j6=pos["j6"], 
        vel=velo
    )
    robot_info(robot)

def get_positions():
    positions = {}
    with open("keyPositions.csv", 'r') as file:
        for line in file:
            line = line.split(",")

            position = {}
            if line[1] == "j":
                try:
                    position["j0"] = float(line[2])
                    position["j1"] = float(line[3])
                    position["j2"] = float(line[4])
                    position["j3"] = float(line[5])
                    position["j4"] = float(line[6])
                    position["j5"] = float(line[7])
                    position["j6"] = float(line[8])
                except ValueError:
                    print("Values for %s are incorrect" % line[0])
            elif line[1] == "c":
                try:
                    position["x"] = float(line[2])
                    position["y"] = float(line[3])
                    position["z"] = float(line[4])
                    position["a"] = float(line[5])
                    position["b"] = float(line[6])
                    position["c"] = float(line[7])
                    position["d"] = float(line[8])
                except ValueError:
                    print("Values for %s are incorrect" % line[0])
            else:
                print("Values for %s are incorrect" % line[0])

            positions[line[0]] = position

    return positions

def main():
    #"""
    robot = Dorna()
    print(robot.connect("192.168.2.20"))
    robot.set_motor(1)
    #"""

    positions = get_positions()
    print(positions)

    
    # Initial position values including slide motor (j6)
    move_to_initial_pose(robot, positions["Initial"], 100)
    print("moved to inital position")
    sleep(1)

    pickup(robot, positions, "TestPlateHolder")
    """
    move_to_initial_pose(robot, positions["Initial"], vel = 50)
    print("moved to initial position")

    #"""
    robot.close()
    


main()