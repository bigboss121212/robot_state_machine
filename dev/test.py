from state_transition import *
from finite_state_machine import FiniteStateMachine
import time


class TrafficLightTrans(Transition):
    def __init__(self, state):
        super().__init__(state)

    def is_transiting(self):
        time.sleep(1)
        print("yo")
        return True


class TrafficLightState(State):
    def __init__(self, color: str, parameter: State.Parameters = State.Parameters()):
        super().__init__(parameter)
        self.__color = color

    def _do_entering_action(self):
        print(self.__color)


class TrafficLight(FiniteStateMachine):
    def __init__(self):
        rouge = TrafficLightState("rouge")
        vert = TrafficLightState("vert")
        jaune = TrafficLightState("jaune")

        trafficTransRouge = TrafficLightTrans(vert)
        trafficTransVert = TrafficLightTrans(jaune)
        trafficTransJaune = TrafficLightTrans(rouge)

        rouge.add_transition(trafficTransRouge)
        vert.add_transition(trafficTransVert)
        jaune.add_transition(trafficTransJaune)

        states = [rouge, vert, jaune]

        layout = FiniteStateMachine.Layout()
        layout.add_states(states)
        layout.initial_state = rouge

        super().__init__(layout)

trafficFSM = TrafficLight()

trafficFSM.run()

