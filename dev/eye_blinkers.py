from action_monitored_state import MonitoredState
from blinker_side_blinker import SideBlinker
from typing import Tuple
from robot import Robot
# from typing import TYPE_CHECKING

# if TYPE_CHECKING:
#     from robot import Robot


class RobotEyeOnState(MonitoredState):
    def __init__(self, robot: 'Robot', side: bool, color:Tuple[int, int, int]):
        self.robot = robot
        self.side = side
        self.color = color
        super().__init__()

    def _do_entering_action(self):
        super()._do_entering_action()
        if self.side:
            self.robot.set_left_eye_color(self.color)
            self.robot.open_left_eye()
        else:
            self.robot.set_right_eye_color(self.color)
            self.robot.open_right_eye()


class RobotEyeOffState(MonitoredState):
    def __init__(self, robot: 'Robot', side: bool):
        self.robot = robot
        self.side = side
        super().__init__()

    def _do_entering_action(self):
        super()._do_entering_action()

        if self.side:
            self.robot.close_left_eye()
        else:
            self.robot.close_right_eye()

class RobotStateGenerator:
    def __init__(self, robot:'Robot', side: bool ,is_on: bool, color:Tuple[int, int, int] = None):
        self._robot = robot
        self._side = side
        self._is_on = is_on
        self._color = color
        
    def __call__(self) -> MonitoredState:
        return RobotEyeOnState(self._robot, self._side, self._color) if self._is_on else RobotEyeOffState(self._robot, self._side)

class EyeBlinkers(SideBlinker):

    def __init__(self, robot: 'Robot', color:Tuple[int, int, int]) -> None:
        self.__color = color
        self._robot = robot
        # 1er bool : False = Right (0 du robot)
        self._on_generator_left = RobotStateGenerator(self._robot, True, True, color)
        self._off_generator_left = RobotStateGenerator(self._robot, True, False)
        self._on_generator_right = RobotStateGenerator(self._robot, False, True, color)
        self._off_generator_right = RobotStateGenerator(self._robot, False, False)
        
        super().__init__(self._off_generator_left, self._on_generator_left, self._off_generator_right, self._on_generator_right)

    @property
    def eye_blinkers_color(self) -> Tuple[int, int, int]:
        return self.__color

    @eye_blinkers_color.setter
    def eye_blinkers_color(self, color: Tuple[int, int, int]) -> None: 
        self.__color = color
        self._on_generator_left = RobotStateGenerator(self._robot, True, True, color)
        self._on_generator_right = RobotStateGenerator(self._robot, False, True, color)
 