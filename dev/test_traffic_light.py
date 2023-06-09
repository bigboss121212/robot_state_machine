from action_monitored_state import MonitoredState
from conditional_transition import ConditionalTransition
from conditions import StateEntryDurationCondition
from finite_state_machine import FiniteStateMachine


class TrafficLight(FiniteStateMachine):
    def __init__(self):
        monitor_rouge = MonitoredState()
        monitor_jaune = MonitoredState()
        monitor_vert = MonitoredState()
        monitor_rouge.add_entering_action(lambda: print("rouge"))
        monitor_jaune.add_entering_action(lambda: print("jaune"))
        monitor_vert.add_entering_action(lambda: print("vert"))
        rouge_state_entry = StateEntryDurationCondition(3.0, monitor_rouge)
        jaune_state_entry = StateEntryDurationCondition(2.0, monitor_jaune)
        vert_state_entry = StateEntryDurationCondition(1.0, monitor_vert)
        transition_rouge = ConditionalTransition(rouge_state_entry)
        transition_jaune = ConditionalTransition(jaune_state_entry)
        transition_vert = ConditionalTransition(vert_state_entry)
        transition_rouge.next_state = monitor_vert
        transition_jaune.next_state = monitor_rouge
        transition_vert.next_state = monitor_jaune
        monitor_rouge.add_transition(transition_rouge)
        monitor_jaune.add_transition(transition_jaune)
        monitor_vert.add_transition(transition_vert)
        states = [monitor_rouge, monitor_vert, monitor_jaune]
        layout = FiniteStateMachine.Layout()
        layout.add_states(states)
        layout.initial_state = monitor_rouge
        super().__init__(layout)
        
tl = TrafficLight()
tl.run()
        
        
        
        