import easygopigo3 as gpg
from led_blinkers import LedBlinkers
from eye_blinkers import EyeBlinkers


class Robot():
    def __init__(self):
        try:
            self.__robotgopigo = gpg.EasyGoPiGo3()
        except Exception:
            raise Exception("Le robot n'a pas pu etre instancié.")
        try:
            self.__remote_control = self.__robotgopigo.init_remote(port='AD1')
            self.__rear_led = self.__robotgopigo.init_led(port='AD2')
            self.__distance_sensor = self.__robotgopigo.init_distance_sensor(port='I2C')
            self.__camera_servo_control = self.__robotgopigo.init_servo(port='SERVO1')
            self.__range_sensor_servo_control = self.__robotgopigo.init_servo(port='SERVO2')
        except Exception:
            raise Exception("Le robot n'est pas integre.")

        self.__led_blinkers = LedBlinkers(self.__robotgopigo)
        self.__eye_blinkers = EyeBlinkers(self.__robotgopigo, (255, 200, 35))

    @property
    def led_blinkers(self): # -> LedBlinkers:
        return self.__led_blinkers
    
    @property
    def distance_sensor(self):
        return self.__distance_sensor

    @property
    def eye_blinkers(self) -> EyeBlinkers:
        return self.__eye_blinkers

    @property
    def is_instanciated(self) -> bool:
        return self.__robotgopigo is not None

    @property
    def has_integrity(self) -> bool:
        if all(attr is not None for attr in (self.__remote_control, 
                                             self.__rear_led, 
                                             self.__distance_sensor, 
                                             self.__camera_servo_control, 
                                             self.__range_sensor_servo_control)):
            return True
        else:
            return False
    
    @property
    def robotgopigo(self):
        return self.__robotgopigo

    @property
    def remote_control(self):
        return self.__remote_control
    
    def shut_down(self):
        self.__robotgopigo.led_off(0)
        self.__robotgopigo.led_off(1)
        self.__robotgopigo.blinker_off(0)
        self.__robotgopigo.blinker_off(1)
        self.__camera_servo_control.disable_servo()
        self.__range_sensor_servo_control.disable_servo()
        self.__robotgopigo.stop()
    
    def track(self):
        self.__led_blinkers.track()
        self.__eye_blinkers.track()