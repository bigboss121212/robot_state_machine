from action_monitored_state import MonitoredState
from robot import Robot
# from typing import TYPE_CHECKING

# if TYPE_CHECKING:
#     from robot import Robot


class StateWithRobot(MonitoredState):
    def __init__(self, robot: Robot):
        self._robot = robot
        super().__init__()

    def _do_in_state_action(self):
        super()._do_in_state_action()
        self._robot.track()

