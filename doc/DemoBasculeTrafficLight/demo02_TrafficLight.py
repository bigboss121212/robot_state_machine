from time import sleep

# Développement incrémental d'une classe TrafficLight 
# 
# Objectif, pratiquer le changement d'état.
# 
# On utilise 'sleep' dans ces exemples pour simplifier 
# et focuser l'exercice sur le changement d'état


# 
# Implémentation 00
#
# Utilisation d'un pseudo 'switch case' avec des 
# entiers comme flags de contrôle de l'état.
class TrafficLight00:
    def __init__(self, name):
        self.name = name
        self.initial_state = 0
        self.current_state = self.initial_state

    def reset(self):
        self.current_state = self.initial_state

    def tic(self):
        if self.current_state == 0:
            print(f'\r{self.name}  Rouge', end='')
            sleep(1.0)
            self.current_state = 1
        elif self.current_state == 1:
            print(f'\r{self.name}  Vert ', end='')
            sleep(0.8)
            self.current_state = 2
        elif self.current_state == 2:
            print(f'\r{self.name}  Jaune', end='')
            sleep(0.2)
            self.current_state = 0

        # self.current_state += 1
        # self.current_state %= 3

def main00():
    traffic_light = TrafficLight00('00')
    while True:
        traffic_light.tic()
        
        
# ######################################  
# 
# Implémentation 01
#
# Utilisation d'un pseudo 'switch case' avec 
# un Enum comme flags de contrôle de l'état.

from enum import Enum, auto

class TrafficLight01:
    
    class TrafficState(Enum):
        RED = auto()
        GREEN = auto()
        YELLOW = auto()
    
    def __init__(self, name):
        self.name = name
        self.initial_state = TrafficLight01.TrafficState.RED
        self.current_state = self.initial_state

    def reset(self):
        self.current_state = self.initial_state

    def tic(self):
        if self.current_state == TrafficLight01.TrafficState.RED:
            print(f'\r{self.name}  Rouge', end='')
            sleep(1.0)
            self.current_state = TrafficLight01.TrafficState.GREEN
        elif self.current_state == TrafficLight01.TrafficState.GREEN:
            print(f'\r{self.name}  Vert ', end='')
            sleep(0.8)
            self.current_state = TrafficLight01.TrafficState.YELLOW
        elif self.current_state == TrafficLight01.TrafficState.YELLOW:
            print(f'\r{self.name}  Jaune', end='')
            sleep(0.2)
            self.current_state = TrafficLight01.TrafficState.RED

        # self.current_state += 1
        # self.current_state %= 3

def main01():
    traffic_light = TrafficLight01('01')
    while True:
        traffic_light.tic()        




# ######################################
# 
# Implémentation 02
#
# Utilisation d'un LUT pour stocker les infos. 
# Branchless programming!

class TrafficLight02:

    def __init__(self, name):
        self.name = name
        self.__states_and_transit = (
            ('Rouge', 1.0, 1),
            ('Vert ', 0.8, 2),
            ('Jaune', 0.2, 0),
        )
        
        self.initial_state = 0
        self.current_state = self.initial_state

    def tic(self):
        state = self.__states_and_transit[self.current_state]
        print(f'\r{self.name}  {state[0]}', end='')
        sleep(state[1])
        self.current_state = state[2]

def main02():
    traffic_light = TrafficLight02('02')
    while True:
        traffic_light.tic()




# ######################################
# 
# Implémentation 03
#
# Utilisation d'un Dict avec Enum pour stocker 
# les infos. Branchless programming!

class TrafficLight03:
    
    class TrafficState(Enum):
        RED = auto()
        GREEN = auto()
        YELLOW = auto()
            
    def __init__(self, name):
        self.name = name
        self.__states_and_transit = {
            TrafficLight03.TrafficState.RED : ('Rouge', 1.0, TrafficLight03.TrafficState.GREEN),
            TrafficLight03.TrafficState.GREEN : ('Vert ', 0.8, TrafficLight03.TrafficState.YELLOW),
            TrafficLight03.TrafficState.YELLOW : ('Jaune', 0.2, TrafficLight03.TrafficState.RED),
        }        
        self.initial_state = TrafficLight03.TrafficState.RED
        self.current_state = self.initial_state

    def tic(self):
        state = self.__states_and_transit[self.current_state]
        print(f'\r{self.name}  {state[0]}', end='')
        sleep(state[1])
        self.current_state = state[2]

def main03():
    traffic_light = TrafficLight03('03')
    while True:
        traffic_light.tic()




# ######################################
# 
# Implémentation 04
#
# Utilisation uniquement d'un Enum pour stocker 
# les infos. Branchless programming!

class TrafficLight04:
    
    class TrafficState(Enum):
        
        #        /¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
        # ______/  Idéalement, cette approche!
        # RED = (auto(), 'Rouge', 1.0, TrafficLight04.TrafficState.GREEN)
        # GREEN = (auto(), 'Vert ', 0.8, TrafficLight04.TrafficState.YELLOW)
        # YELLOW = (auto(), 'Jaune', 0.2, TrafficLight04.TrafficState.RED)
        # ¯¯¯¯¯¯\  malheureusement, les Enums ne sont                  ^
        #        \   pas encore déclarés et ne peuvent                 |
        #         \    être référencés ici ----------------------------+
        #          ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
        #  /¯¯'---,____/¯¯¯ Solution, le faire en 2 étapes 
        # V            \___ Voir la fonction _set_next
        RED = (auto(), 'Rouge', 1.0)
        GREEN = (auto(), 'Vert ', 0.8)
        YELLOW = (auto(), 'Jaune', 0.2)
        
        def __init__(self, state, name, duration):
            self.state = state
            self.state_name = name
            self.duration = duration
            
        @staticmethod
        def _set_next():
            state_map = { 
                    TrafficLight04.TrafficState.RED: TrafficLight04.TrafficState.GREEN,
                    TrafficLight04.TrafficState.GREEN: TrafficLight04.TrafficState.YELLOW,
                    TrafficLight04.TrafficState.YELLOW: TrafficLight04.TrafficState.RED,
                }
            for cur_state, next_state in state_map.items():
                cur_state.next_state = next_state

    def __init__(self, name):
        self.name = name
        self.current_state = TrafficLight04.TrafficState.RED

    def tic(self):
        print(f'\r{self.name}  {self.current_state.state_name}', end='')
        sleep(self.current_state.duration)
        self.current_state = self.current_state.next_state

TrafficLight04.TrafficState._set_next()

def main04():
    traffic_light = TrafficLight04('04')
    while True:
        traffic_light.tic()


# ##########################################        
# ##########################################        
# ##########################################        
if __name__ == '__main__':
    main04()