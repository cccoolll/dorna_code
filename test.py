from dorna2 import Dorna
from time import sleep

def pickup_sample(robot, claw, velocity):
    robot.jmove(
        rel=0, 
        j5=claw, 
        vel=velocity
        )
    print("\nTrack Command")
    print(robot.track_cmd())
    print("Sys Data")
    print(robot.sys())

def pickup_position(robot, x, y, z, a, b, c, d, velocity):
    response1 = robot.lmove(
        timeout=10, 
        rel=0, 
        x=x, 
        y=y, 
        z=z, 
        a=a,
        b=b,
        c=c, 
        #d=d, 
        vel=velocity, 
        accel=500,
        jerk=2500
    )
    print(response1)
    print("\nTrack Command")
    print(robot.track_cmd())
    print("Sys Data")
    print(robot.sys())

def move_to_initial_pose(robot, velocity):
    # Move all joints simultaneously
    response1 = robot.jmove(
        rel=1, 
        j0=0.5, 
        j1=0.5, 
        j2=0.5, 
        j3=0.5, 
        j4=0.5, 
        j5=0.5, 
        vel=velocity, 
        accel=500,
        jerk=2000
    )
    print(response1)
    print("\nTrack Command")
    print(robot.track_cmd())
    print("Sys Data")
    print(robot.sys())

    response2 = robot.jmove(
        timeout=10, 
        rel=0, 
        j0=90, 
        j1=90, 
        j2=-90, 
        j3=-90, 
        j4=0, 
        j5=0,
        j6=100, 
        vel=velocity,
        accel=500,
        jerk=2500
    )
    print(response2)
    print("\nTrack Command")
    print(robot.track_cmd())
    print("Sys Data")
    print(robot.sys())
    sleep(1)  # Give some time for the movement to complete

def main():
    robot = Dorna()
    print(robot.connect("192.168.2.20"))
    robot.set_motor(1)

    # Initial position values including slide motor (j6)
    move_to_initial_pose(robot, 100)
    pickup_position(robot, 0, 372.46, -35, -88, 0, 0, 123, 50)
    pickup_sample(robot, -210, 100)
    move_to_initial_pose(robot, 100)

    robot.close()

main()