from dorna2 import Dorna

def main():
    robot = Dorna()
    print(robot.connect("192.168.2.20"))

    robot.close()


main()