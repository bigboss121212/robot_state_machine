from state_with_robot import StateWithRobot
from finite_state_machine import FiniteStateMachine
from conditions import RemoteControlCondition
from conditional_transition import ConditionalTransition
from blinker_side_blinker import SideBlinker
from robot import Robot
# from typing import TYPE_CHECKING

# if TYPE_CHECKING:
#     from robot import Robot


class Task1FSM(FiniteStateMachine):
    def __init__(self, robot: Robot):
        self.__robot = robot
        
        stop_state = StopState(self.__robot)
        forward_state = ForwardState(self.__robot)
        backward_state = BackwardState(self.__robot)
        rotate_left_state = RotateLeftState(self.__robot)
        rotate_right_state = RotateRightState(self.__robot)

        # stop_state   
        stop_state_condition_up = RemoteControlCondition('up', self.__robot.remote_control)
        stop_state_condition_left = RemoteControlCondition('left', self.__robot.remote_control)
        stop_state_condition_right = RemoteControlCondition('right', self.__robot.remote_control)
        stop_state_condition_down = RemoteControlCondition('down', self.__robot.remote_control)
        
        stop_state_transition_up = ConditionalTransition(stop_state_condition_up)
        stop_state_transition_up.next_state = forward_state
        stop_state_transition_left = ConditionalTransition(stop_state_condition_left)
        stop_state_transition_left.next_state = rotate_left_state
        stop_state_transition_right = ConditionalTransition(stop_state_condition_right)
        stop_state_transition_right.next_state = rotate_right_state
        stop_state_transition_down = ConditionalTransition(stop_state_condition_down)
        stop_state_transition_down.next_state = backward_state

        stop_state.add_transition(stop_state_transition_up)
        stop_state.add_transition(stop_state_transition_left)
        stop_state.add_transition(stop_state_transition_right)
        stop_state.add_transition(stop_state_transition_down)

        # forward_state
        forward_state_condition = RemoteControlCondition('up', self.__robot.remote_control, inverse=True)
        forward_state_transition = ConditionalTransition(forward_state_condition)
        forward_state_transition.next_state = stop_state
        forward_state.add_transition(forward_state_transition)

        # backward_state
        backward_state_condition = RemoteControlCondition('down', self.__robot.remote_control, inverse=True)
        backward_state_transition = ConditionalTransition(backward_state_condition)
        backward_state_transition.next_state = stop_state
        backward_state.add_transition(backward_state_transition)

        # rotate_left_state
        rotate_left_state_condition = RemoteControlCondition('left', self.__robot.remote_control, inverse=True)
        rotate_left_state_transition = ConditionalTransition(rotate_left_state_condition)
        rotate_left_state_transition.next_state = stop_state
        rotate_left_state.add_transition(rotate_left_state_transition)

        # rotate_right_state
        rotate_right_state_condition = RemoteControlCondition('right', self.__robot.remote_control, inverse=True)
        rotate_right_state_transition = ConditionalTransition(rotate_right_state_condition)
        rotate_right_state_transition.next_state = stop_state
        rotate_right_state.add_transition(rotate_right_state_transition)

        #layout
        states = [stop_state, 
                  forward_state, 
                  backward_state, 
                  rotate_left_state, 
                  rotate_right_state]

        layout = FiniteStateMachine.Layout()
        layout.add_states(states)
        layout.initial_state = stop_state

        super().__init__(layout)

class ForwardState(StateWithRobot):
    def __init__(self, robot: Robot):
        super().__init__(robot)
        self.__robot = robot

    def _do_entering_action(self):
        self.__robot.led_blinkers.blink1(SideBlinker.Side.BOTH, 1.0, 0.25)
        self.__robot.robotgopigo.forward()

class RotateLeftState(StateWithRobot):
    def __init__(self, robot: Robot):
        super().__init__(robot)
        self.__robot = robot
        
    def _do_entering_action(self):
        self.__robot.led_blinkers.blink1(SideBlinker.Side.LEFT, 1.0, 0.50)
        self.__robot.robotgopigo.left()

class RotateRightState(StateWithRobot):
    def __init__(self, robot: Robot):
        super().__init__(robot)
        self.__robot = robot
        
    def _do_entering_action(self):
        self.__robot.led_blinkers.blink1(SideBlinker.Side.RIGHT, 1.0, 0.50)
        self.__robot.robotgopigo.right()

class StopState(StateWithRobot):
    def __init__(self, robot: Robot):
        super().__init__(robot)
        self.__robot = robot
        
    def _do_entering_action(self):
        self.__robot.led_blinkers.turn_off(SideBlinker.Side.BOTH)
        self.__robot.robotgopigo.stop()

class BackwardState(StateWithRobot):
    def __init__(self, robot: Robot):
        super().__init__(robot)
        self.__robot = robot
        
    def _do_entering_action(self):
        self.__robot.led_blinkers.blink1(SideBlinker.Side.BOTH, 1.0, 0.75)
        self.__robot.robotgopigo.backward()