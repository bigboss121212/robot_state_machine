from state_with_robot import StateWithRobot
from finite_state_machine import FiniteStateMachine
from conditions import StateValueInferiorCondition, RemoteControlCondition
from conditional_transition import ConditionalTransition
from blinker_side_blinker import SideBlinker
from robot import Robot
# from typing import TYPE_CHECKING

# if TYPE_CHECKING:
#     from robot import Robot


class Task2FSM(FiniteStateMachine):
    def __init__(self, robot: Robot):
        self.__robot = robot
        
        forward_state = ForwardState(self.__robot)
        stop_state = StopState(self.__robot)
        
        #forward_state
        forward_state_condition = StateValueInferiorCondition(100, forward_state)
        forward_state_transition = ConditionalTransition(forward_state_condition)
        forward_state_transition.next_state = stop_state
        #forward_state.add_transition(forward_state_transition)
        
        #stop_state
        stop_state_condition = RemoteControlCondition('up', self.__robot.remote_control)
        stop_state_transition = ConditionalTransition(stop_state_condition)
        stop_state_transition.next_state = forward_state
        stop_state.add_transition(stop_state_transition)
        
        #layout
        states = [forward_state, stop_state]

        layout = FiniteStateMachine.Layout()
        layout.add_states(states)
        layout.initial_state = stop_state

        super().__init__(layout)

class ForwardState(StateWithRobot):
    def __init__(self, robot: Robot):
        super().__init__(robot)
        self.__robot = robot

    def _do_entering_action(self):
        self.__robot.robotgopigo.forward()
        self.__robot.led_blinkers.blink1(SideBlinker.Side.BOTH, 1.0, 0.75)
        self.custom_value = 300
        
    def _do_in_state_action(self):
        self.custom_value = self.__robot.distance_sensor.read_mm()
    
class StopState(StateWithRobot):
    def __init__(self, robot: Robot):
        super().__init__(robot)
        self.__robot = robot

    def _do_entering_action(self):
        self.__robot.robotgopigo.stop()
        self.__robot.led_blinkers.turn_off(SideBlinker.Side.BOTH)
       
