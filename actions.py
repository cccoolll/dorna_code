import asyncio
from dorna2 import Dorna
from pydantic import BaseModel, Field
import json
from imjoy_rpc import api
from imjoy_rpc.hypha import connect_to_server, login
import argparse

class GrabFromHolderInput(BaseModel):
    """
    This function performs the action of picking up an object from the plate 
    holder on the table. It firsts moves the claw to a position above the holder, 
    lowers itself into the holder, picks up the object and lifts back up. 
    """
    position: str = Field(..., description="position to travel to")

class PlacesAtHolderInput(BaseModel):
    """
    This function performs the action of placing an object at the plate 
    holder on the table. It firsts moves the claw to a position above the holder, 
    lowers itself into the holder, releases the object and lifts back up. 
    """
    position: str = Field(..., description="position to travel to")

class GrabFromMicroscopeInput(BaseModel):
    """
    This function performs the action of grabbing a sample from the microscope.  
    It first moves the claw to a position in front and above the microscope, 
    then moves forward to be ontop of the microscope, then lowers into the tray,
    then grabs the sample, then lifts back up, moves away from the microscope,
    then continues to lift back up. 
    """
    position: str = Field(..., description="position to travel to")

class PlacesAtMicroscopeInput(BaseModel):
    """
    This function performs the action of grabbing a sample from the microscope.  
    It first moves the claw to a position in front and above the microscope, 
    then moves forward to be ontop of the microscope, then lowers into the tray,
    then releases the sample, then lifts back up, moves away from the microscope,
    then continues to lift back up. 
    """
    position: str = Field(..., description="position to travel to")

class RoboticArm:
    def __init__(self):
        self.robot = Dorna()
        self.robot.connect("192.168.2.20")
        self.robot.set_motor(1)
        self.robot.jmove(
            rel=0,
            j5=0,
            vel=80
        )
        with open("positions.json", 'r') as positions_file: 
            self.positions = json.load(positions_file)
    
    async def run_sync(self, func, *args, **kwargs):
        """Run a synchronous function in an asynchronous manner."""
        return await asyncio.to_thread(func, *args, **kwargs)

    async def robot_info(self, funcname):
        print(f"\nTrack Command in {funcname}")
        track_cmd = await self.run_sync(self.robot.track_cmd)
        print(track_cmd)

    async def pickup(self, pos, clawOpen, microscope):
        # lowers the claw
        await self.run_sync(self.robot.lmove,
            z = pos["z"]-59,
            vel = 50
        )
        # displays robot information
        await self.robot_info("pickup")

        if clawOpen:
            await self.run_sync(self.robot.jmove,
                rel=0,
                j5 = 0,
                vel = 80
            )
        else: 
            # closes the claw
            await self.run_sync(self.robot.jmove,
                rel=0,
                j5 = -375,
                vel = 80
            )
        # displays robot information
        await self.robot_info("pickup close claw")
        
        # lifts up the claw
        if microscope:
            await self.run_sync(self.robot.lmove,
                z = pos["z"]-57+24, 
                vel = 50
            )
        else:
            await self.run_sync(self.robot.lmove,
                z = pos["z"], 
                vel = 50
            )

        # displays robot information
        await self.robot_info("pickup lifts claw")
    
    async def transport(self, j6):
        """
        Description: This function moves the robotic arm into the transportation
        position and then moves the robotic arm along the sliding rail to where it 
        needs to go. 
        Parameters: robot (obj), pos (dict)
        Returns: None
        """
        # rotates the robot to the transportation position
        await self.run_sync(self.robot.jmove,
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
        await self.robot_info("transport")

        # moves the sliding rail to the position given
        await self.run_sync(self.robot.jmove,
            rel=0,
            j6=j6,
            vel=120,
            accel=500,
            jerk=2000
        )
        # displays robot information
        await self.robot_info("transport")
    
    async def move_to_initial(self):
        """
        Description: This function moves the robotic arm to the initial position
        Parameters: robot (obj)
        Returns: None
        """
        # moves the robotic arm to the initial starting position
        await self.run_sync(self.robot.jmove,
            timeout=10, 
            rel=0, 
            j1=100, 
            j2=-100, 
            j3=-88, 
            j4=0, 
            vel=250
        )
        # displays robot information
        await self.robot_info("move_to_initial")

    async def grab_from_holder(self, config: GrabFromHolderInput, context=None):
        """
        Description: This function performs the action of pickup/placing something
        at a holder on the table. It firsts moves the claw to a position above the 
        holder, lowers itself into the holder, picks up or releases the something 
        and lifts back up. 
        """
        position = config.position
        pos = self.positions[position]

        await self.transport(pos["j6"])

        # rotates the robotic arm first to avoid any obstables
        await self.run_sync(self.robot.jmove,
            rel=0,
            j0=pos["j0"],
            vel = 250
        )

        # displays robot information
        await self.robot_info("grab_from_holder")
        
        # moves the rest of the robot arm to the initial holder position
        await self.run_sync(self.robot.jmove,
                rel=0,
                x=pos["x"],
                y=pos["y"],
                z=pos["z"],
                a=pos["a"],
                b=pos["b"],
                d=pos["d"],
                vel = 200
            )
        # displays robot information
        await self.robot_info("grab_from_holder")

        await self.pickup(pos, False, False)

        await self.move_to_initial()

    async def place_at_holder(self, config: PlacesAtHolderInput, context=None): 
        """
        Description: This function performs the action of pickup/placing something
        at a holder on the table. It firsts moves the claw to a position above the 
        holder, lowers itself into the holder, picks up or releases the something 
        and lifts back up. 
        """
        position = config.position
        pos = self.positions[position]

        await self.transport(pos["j6"])

        # rotates the robotic arm first to avoid any obstables
        await self.run_sync(self.robot.jmove,
            rel=0,
            j0=pos["j0"],
            vel = 250
        )

        # displays robot information
        await self.robot_info("action_from_holder")
        
        # moves the rest of the robot arm to the initial holder position
        await self.run_sync(self.robot.jmove,
                rel=0,
                x=pos["x"],
                y=pos["y"],
                z=pos["z"],
                a=pos["a"],
                b=pos["b"],
                d=pos["d"],
                vel = 200
            )
        # displays robot information
        await self.robot_info("action_from_holder")

        await self.pickup(pos, True, False)

        await self.move_to_initial()

    async def grab_from_microscope(self, config: GrabFromMicroscopeInput, context=None):
        """
        Description: This function performs the action of picking-up/placing a 
        sample to the microscope. It first moves the claw to a position in front 
        and above the microscope, then moves forward to be ontop of the microscope,
        it then lowers into the tray, then picks-up or releases the sample, then
        lifts back up, moves away from the microscope, and then lifts back up. 
        Parameters: robot (obj), pos (dict), clawOpen(bool)
        Returns: clawOpen(bool)
        """
        position = config.position
        pos = self.positions[position]

        # this is to lower the claw compared to initial holder position as to not hit the light
        microOffset = -33

        await self.transport(pos["j6"])

        # robots the robotic arm first to avoid any obstables
        await self.run_sync(self.robot.jmove,
            rel=0,
            j0=pos["j0"],
            vel = 200
        )
        # displays robot information
        await self.robot_info("action_from_microscope")

        # determines whether to move forward or backward based on which side of the table it's on
        if pos["y"] > 0:
            deltaY = 90
        else:
            deltaY = -90

        # moves the rest of the robotic arm to the initial microscope position
        await self.run_sync(self.robot.jmove,
            rel=0,
            x = pos["x"],
            y = pos["y"]-deltaY,
            z = pos["z"]+microOffset,
            a = pos["a"],
            d = pos["d"],
            vel = 100
        )
        # displays robot information
        await self.robot_info("action_from_microscope")

        # moves the robotic arm into the microscope to be able to pick-up/place
        await self.run_sync(self.robot.lmove,
            rel=0,
            y = pos["y"],
            b = pos["b"],
            vel = 50
        )
        # displays robot information
        await self.robot_info("action_from_microscope")

        await self.pickup(pos, False, True)

        # moves the robotic arm out of the microscope
        await self.run_sync(self.robot.lmove,
            rel=0,
            y = pos["y"]-deltaY,
            z = pos["z"]+microOffset,
            b = pos["b"],
            vel = 50
        )
        # displays robot information
        await self.robot_info("action_from_microscope")

        await self.move_to_initial()

    async def place_at_microscope(self, config: PlacesAtMicroscopeInput, context=None):
        """
        Description: This function performs the action of picking-up/placing a 
        sample to the microscope. It first moves the claw to a position in front 
        and above the microscope, then moves forward to be ontop of the microscope,
        it then lowers into the tray, then picks-up or releases the sample, then
        lifts back up, moves away from the microscope, and then lifts back up. 
        Parameters: robot (obj), pos (dict), clawOpen(bool)
        Returns: clawOpen(bool)
        """
        position = config.position
        pos = self.positions[position]

        self.robot.connect("192.168.2.20")

        # this is to lower the claw compared to initial holder position as to not hit the light
        microOffset = -33

        await self.transport(pos["j6"])

        # robots the robotic arm first to avoid any obstables
        await self.run_sync(self.robot.jmove,
            rel=0,
            j0=pos["j0"],
            vel = 200
        )
        # displays robot information
        await self.robot_info("action_from_microscope")

        # determines whether to move forward or backward based on which side of the table it's on
        if pos["y"] > 0:
            deltaY = 90
        else:
            deltaY = -90

        # moves the rest of the robotic arm to the initial microscope position
        await self.run_sync(self.robot.jmove,
            rel=0,
            x = pos["x"],
            y = pos["y"]-deltaY,
            z = pos["z"]+microOffset,
            a = pos["a"],
            d = pos["d"],
            vel = 100
        )
        # displays robot information
        await self.robot_info("action_from_microscope")

        # moves the robotic arm into the microscope to be able to pick-up/place
        await self.run_sync(self.robot.lmove,
            rel=0,
            y = pos["y"],
            b = pos["b"],
            vel = 50
        )
        # displays robot information
        await self.robot_info("action_from_microscope")

        await self.pickup(pos, True, True)

        # moves the robotic arm out of the microscope
        await self.run_sync(self.robot.lmove,
            rel=0,
            y = pos["y"]-deltaY,
            z = pos["z"]+microOffset,
            b = pos["b"],
            vel = 50
        )
        # displays robot information
        await self.robot_info("action_from_microscope")

        await self.move_to_initial()

        self.robot.close()

def get_schema():
        return {
            "grab_from_holder": GrabFromHolderInput.schema(),
            "place_at_holder": GrabFromHolderInput.schema(),
            "grab_from_microscope": GrabFromHolderInput.schema(),
            "place_at_microscope": GrabFromHolderInput.schema(),
        }




async def setup():
    robot = RoboticArm()
    # Define an chatbot extension
    robotic_arm_control_extension = {
        "_rintf": True,
        "id": "robotic-arm-control",
        "type": "bioimageio-chatbot-extension",
        "name": "Robotic Arm Control",
        "description": "moves the robotic arm to pickup and place objects from microscopes and plate holders",
        "get_schema": get_schema,
        "tools": {
            "grab_from_holder": robot.grab_from_holder,
            "place_at_holder": robot.place_at_holder,
            "grab_from_microscope": robot.grab_from_microscope,
            "place_at_microscope": robot.place_at_microscope,
        }
    }

    server_url = "https://chat.bioimage.io"
    token = await login({"server_url": server_url})
    server = await connect_to_server({"server_url": server_url, "token": token})
    svc = await server.register_service(robotic_arm_control_extension)

    print(f"Extension service registered with id: {svc.id}, you can visit the service at:\n https://bioimage.io/chat?server={server_url}&extension={svc.id}&assistant=Skyler")

async def main():
    robot = RoboticArm()
    await robot.grab_from_holder(0, 0, 0, 0, 0, 0, 0, 0)  # Example values

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Robotic Arm Control services for Hypha."
    )
    parser.add_argument(
        "--simulation",
        dest="simulation",
        action="store_true",
        default=True,
        help="Run in simulation mode (default: True)"
    )
    parser.add_argument(
        "--no-simulation",
        dest="simulation",
        action="store_false",
        help="Run without simulation mode"
    )
    parser.add_argument("--verbose", "-v", action="count")
    args = parser.parse_args()

    roboticArmController = RoboticArm()

    loop = asyncio.get_event_loop()
    loop.create_task(setup())
    loop.run_forever()
