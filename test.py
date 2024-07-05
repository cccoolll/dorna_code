from dorna2 import Dorna

def main():
    robot = Dorna()
    print(robot.connect("192.168.2.20"))
    robot.set_motor(1)

    robot.play(timeout=-1, cmd="jmove", rel=1, j0 = -10, vel = 20)
    robot.play(timeout=-1, cmd="jmove", rel=1, j1 = 10, vel = 20)

    robot.set_motor(0)
    robot.close()


main()