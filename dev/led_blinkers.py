from action_monitored_state import MonitoredState
from blinker_side_blinker import SideBlinker
from robot import Robot
# from typing import TYPE_CHECKING

# if TYPE_CHECKING:
#     from robot import Robot


class RobotLedOnState(MonitoredState):
    def __init__(self, robot: 'Robot', side: bool):
        self.robot = robot
        self.side = side
        super().__init__()

    def _do_entering_action(self):
        super()._do_entering_action()
        self.robot.led_on(self.side)

class RobotLedOffState(MonitoredState):
    def __init__(self, robot: 'Robot', side: bool):
        self.robot = robot
        self.side = side
        super().__init__()

    def _do_entering_action(self):
        super()._do_entering_action()
        self.robot.led_off(self.side)

class RobotStateGenerator:
    def __init__(self, robot:'Robot', side: bool ,is_on: bool):
        self._robot = robot
        self._side = side
        self.is_on = is_on

    def __call__(self) -> MonitoredState:
        return RobotLedOnState(self._robot, self._side) if self.is_on else RobotLedOffState(self._robot, self._side)


class LedBlinkers(SideBlinker):
    def __init__(self, robot: 'Robot') -> None:
        # 1er bool du constructeur de RobotStateGenerator : False = Right (0 du robot)
        on_generator_left = RobotStateGenerator(robot, True, True)
        off_generator_left = RobotStateGenerator(robot, True, False)
        on_generator_right = RobotStateGenerator(robot, False, True)
        off_generator_right = RobotStateGenerator(robot, False, False)
        
        super().__init__(off_generator_left, on_generator_left, off_generator_right, on_generator_right)
        
    
        