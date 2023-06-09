from robot import Robot
from state_with_robot import StateWithRobot
from finite_state_machine import FiniteStateMachine
from conditions import *
from conditional_transition import ConditionalTransition
from blinker_side_blinker import SideBlinker
from task1 import Task1FSM
from task2 import Task2FSM


class C64Project(FiniteStateMachine):
    def __init__(self):
        self.__robot = Robot()
        robot_instanciation_state = RobotInstanciationState(self.__robot)
        robot_instanciation_failed_state = InstanciationFailedState(self.__robot)
        robot_integrity_state = RobotIntegrityState(self.__robot)
        robot_integrity_failed_state = IntegrityFailedState(self.__robot)
        robot_integrity_succeed_state = IntegritySucceedState(self.__robot)
        c64_end_state = EndState(self.__robot)
        robot_shut_down_state = ShutDownState(self.__robot)
        c64_home_state = HomeState(self.__robot)
        robot_task1 = Task1State(self.__robot)
        robot_task2 = Task2State(self.__robot)

        #robot_instantiation
        robot_instanciation_succeed_condition = StateValueCondition(True, robot_instanciation_state)
        robot_instanciation_failed_condition = StateValueCondition(False, robot_instanciation_state)

        robot_instantiation_succeed_transition = ConditionalTransition(robot_instanciation_succeed_condition)
        robot_instantiation_succeed_transition.next_state = robot_integrity_state
        robot_instanciation_failed_transition = ConditionalTransition(robot_instanciation_failed_condition)
        robot_instanciation_failed_transition.next_state = robot_instanciation_failed_state

        robot_instanciation_state.add_transition(robot_instantiation_succeed_transition)
        robot_instanciation_state.add_transition(robot_instanciation_failed_transition)

        #instantiation_failed
        failed_condtion = AlwaysTrueCondition()
        failed_transition = ConditionalTransition(failed_condtion)
        failed_transition.next_state = c64_end_state

        robot_instanciation_failed_state.add_transition(failed_transition)

        #robot_integrity
        robot_integrity_succeed_condition = StateValueCondition(True, robot_integrity_state)
        robot_integrity_failed_condition = StateValueCondition(False, robot_integrity_state)

        robot_integrity_succeed_transition = ConditionalTransition(robot_integrity_succeed_condition)
        robot_integrity_succeed_transition.next_state = robot_integrity_succeed_state
        robot_integrity_failed_transition = ConditionalTransition(robot_integrity_failed_condition)
        robot_integrity_failed_transition.next_state = robot_integrity_failed_state

        robot_integrity_state.add_transition(robot_integrity_succeed_transition)
        robot_integrity_state.add_transition(robot_integrity_failed_transition)

        #integrity_failed
        integrity_failed_condition = StateEntryCountCondition(0.5, robot_integrity_failed_state)
        integrity_failed_transition = ConditionalTransition(integrity_failed_condition)
        integrity_failed_transition.next_state = robot_shut_down_state

        robot_integrity_failed_state.add_transition(integrity_failed_transition)

        #integrity_succeeded
        integrity_succeeded_condition = StateEntryCountCondition(0.3, robot_integrity_succeed_state)
        integrity_succeeded_transition = ConditionalTransition(integrity_succeeded_condition)
        integrity_succeeded_transition.next_state = c64_home_state

        robot_integrity_succeed_state.add_transition(integrity_succeeded_transition)

        #shut_down
        shut_down_condition = StateEntryDurationCondition(0.3, robot_shut_down_state)
        shut_down_transition = ConditionalTransition(shut_down_condition)
        shut_down_transition.next_state = c64_end_state

        robot_shut_down_state.add_transition(shut_down_transition)

        #remote
        remote_condition_ok = RemoteControlCondition('ok', self.__robot.remote_control)
        remote_condition_hash = RemoteControlCondition('#', self.__robot.remote_control)
        remote_condition_1 = RemoteControlCondition('1', self.__robot.remote_control)
        remote_condition_2 = RemoteControlCondition('2', self.__robot.remote_control)

        #home
        home_transition = ConditionalTransition(remote_condition_hash)
        home_transition.next_state = robot_shut_down_state

        home_transition1 = ConditionalTransition(remote_condition_1)
        home_transition1.next_state = robot_task1

        home_transition2 = ConditionalTransition(remote_condition_2)
        home_transition2.next_state = robot_task2

        c64_home_state.add_transition(home_transition)
        c64_home_state.add_transition(home_transition1)
        c64_home_state.add_transition(home_transition2)

        #task1
        task1_transition = ConditionalTransition(remote_condition_ok)
        task1_transition.next_state = c64_home_state

        robot_task1.add_transition(task1_transition)

        #task2
        task2_transition = ConditionalTransition(remote_condition_ok)
        task2_transition.next_state = c64_home_state

        robot_task2.add_transition(task2_transition)

        #layout
        states = [robot_instanciation_state,
                  robot_instanciation_failed_state,
                  robot_integrity_state,
                  robot_integrity_failed_state,
                  robot_integrity_succeed_state,
                  c64_end_state,
                  robot_shut_down_state,
                  c64_home_state,
                  robot_task1,
                  robot_task2]

        layout = FiniteStateMachine.Layout()
        layout.add_states(states)
        layout.initial_state = robot_instanciation_state

        super().__init__(layout)


class RobotInstanciationState(StateWithRobot):
    def __init__(self, robot: Robot):
        super().__init__(robot)
        self._robot = robot

    def _do_entering_action(self):
        self.custom_value = self._robot.is_instanciated
        
class InstanciationFailedState(StateWithRobot):
    def __init__(self, robot: Robot):
        super().__init__(robot)

    def _do_entering_action(self):
        print("Instanciation du robot échouée.")

class EndState(StateWithRobot):
    def __init__(self, robot: Robot):
        super().__init__(robot)

    def _do_entering_action(self):
        print("État terminal atteint.")
        self.current_operational_state = FiniteStateMachine.OperationalState.TERMINAL_REACHED

class RobotIntegrityState(StateWithRobot):
    def __init__(self, robot: Robot):
        super().__init__(robot)
        self._robot = robot

    def _do_entering_action(self):
        self.custom_value = self._robot.has_integrity
                
class IntegrityFailedState(StateWithRobot):
    def __init__(self, robot: Robot):
        super().__init__(robot)
        self._robot = robot

    def _do_entering_action(self):
        self._robot.led_blinkers.blink2(SideBlinker.Side.BOTH, 5.0, 0.5)
        self._robot.eye_blinkers.eye_blinkers_color = (255, 0, 0)
        self._robot.eye_blinkers.blink2(SideBlinker.Side.BOTH, 5.0, 0.5)

class IntegritySucceedState(StateWithRobot):
    def __init__(self, robot: Robot):
        super().__init__(robot)
        self._robot = robot

    def _do_entering_action(self):
        self._robot.led_blinkers.turn_off(SideBlinker.Side.BOTH)
        self._robot.eye_blinkers.eye_blinkers_color = (0, 255, 0)
        self._robot.eye_blinkers.blink2(SideBlinker.Side.BOTH, 3.0, 1.0)

class ShutDownState(StateWithRobot):
    def __init__(self, robot: Robot):
        super().__init__(robot)
        self._robot = robot

    def _do_entering_action(self):
        self._robot.led_blinkers.turn_off(SideBlinker.Side.BOTH)
        self._robot.eye_blinkers.eye_blinkers_color = (255, 255, 0)
        self._robot.eye_blinkers.blink2(SideBlinker.Side.BOTH, 3.0, 0.75)
        self._robot.shut_down()
        self._robot.robotgopigo.close_eyes()
        
class HomeState(StateWithRobot):
    def __init__(self, robot: Robot):
        super().__init__(robot)
        self._robot = robot

    def _do_entering_action(self):
        self._robot.led_blinkers.turn_off(SideBlinker.Side.BOTH)
        self._robot.eye_blinkers.eye_blinkers_color = (255, 255, 0)
        self._robot.eye_blinkers.blink1(SideBlinker.Side.LEFT_RECIPROCAL, 1.5)

class Task1State(StateWithRobot):
    def __init__(self, robot: Robot):
        super().__init__(robot)
        self._robot = robot
        self._t1FSM = Task1FSM(self._robot)
        
    def _do_entering_action(self):
        self._robot.eye_blinkers.eye_blinkers_color = (255, 255, 0)
        self._robot.eye_blinkers.blink1(SideBlinker.Side.BOTH, 1.5)
            
    def _do_in_state_action(self):
        self._t1FSM.track()

class Task2State(StateWithRobot):
    def __init__(self, robot: Robot):
        super().__init__(robot)
        self._robot = robot
        self._t2FSM = Task2FSM(self._robot)

    def _do_entering_action(self):
        self._robot.eye_blinkers.eye_blinkers_color = (255, 255, 0)
        self._robot.eye_blinkers.blink1(SideBlinker.Side.BOTH, 1.5)
        
    def _do_in_state_action(self):
        self._t2FSM.track()
   
        


