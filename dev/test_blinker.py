from blinker_side_blinker import Blinker, SideBlinker
from action_monitored_state import MonitoredState
from state_transition import State
Parameters = State.Parameters


class OnState(MonitoredState):
    def __init__(self, parameters: Parameters = Parameters()):
        super().__init__(parameters)
        #super().add_entering_action(lambda: print("on"))

    def _do_entering_action(self):
        super()._do_entering_action()
        print("on")


class OffState(MonitoredState):
    def __init__(self, parameters: Parameters = Parameters()):
        super().__init__(parameters)
        #super().add_entering_action(lambda: print("off"))

    def _do_entering_action(self):
        super()._do_entering_action()
        print("off")


class StateGenerator:
    def __init__(self, is_on: bool):
        self.is_on = is_on

    def __call__(self) -> MonitoredState:
        return OnState() if self.is_on else OffState()

on_generator = StateGenerator(True)
off_generator = StateGenerator(False)

# on_state_entry = StateEntryDurationCondition(2.0, on_generator)

blinker = Blinker(off_generator, on_generator)

# blinker.turn_on_dur(5.0)
# blinker.run(False, time_budget=1)

# blinker.turn_off_dur(3.0)
# blinker.run(False, time_budget=5)

# blinker.blink1(3)
# blinker.run(False, time_budget=20)

# blinker.blink2(20.0, percent_on=0.3)
# blinker.run(False, time_budget=20)

# blinker.blink3(10.0, 5, percent_on=0.3, begin_on=False, end_off=False)
# blinker.run(False, time_budget=10)

# blinker.blink4(5, 2.0, percent_on=0.3, end_off=False)
# blinker.run(False, time_budget=10)

sideBlinker = SideBlinker(off_generator, on_generator, off_generator, on_generator)

# sideBlinker.blink1(side=SideBlinker.Side.LEFT_RECIPROCAL, cycle_duration=10.0, percent_on=0.3)
# while True:
#     sideBlinker.track()

sideBlinker.blink1(side=SideBlinker.Side.LEFT, cycle_duration=2.0, percent_on=0.3)
while True:
    sideBlinker.track()