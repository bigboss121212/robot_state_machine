
# from led_blinkers import LedBlinkers
# from eye_blinkers import EyeBlinkers
from robot import Robot
from blinker_side_blinker import SideBlinker


# from typing import TYPE_CHECKING

# if TYPE_CHECKING:

robot = Robot()

#robot.led_blinkers.blink1(side=SideBlinker.Side.LEFT, cycle_duration=2.0, percent_on=0.3)
#robot.led_blinkers.blink1(side=SideBlinker.Side.LEFT_RECIPROCAL, cycle_duration=2.0, percent_on=0.3)
#robot.led_blinkers.turn_on(side=SideBlinker.Side.LEFT, duration=5.0)
#robot.led_blinkers.turn_off(side=SideBlinker.Side.LEFT, duration=5.0)

robot.eye_blinkers.blink1(side=SideBlinker.Side.LEFT_RECIPROCAL, cycle_duration=2.0, percent_on=0.3) 


while True:
    #robot.led_blinkers.track()
    robot.eye_blinkers.track()

