import msvcrt
import sys

def main():
    
    proceed = True
    while proceed:
        
        if msvcrt.kbhit():
            input_char = msvcrt.getch().lower().decode('UTF-8')
            
            if input_char == 'q':
                proceed = False
                
            else:
                print(input_char, end='')
                
    print('\nEnd!!!')
    
    
 # --------------------------------------
 # --------------------------------------
 # --------------------------------------
 
 
from msvcrt import kbhit, getch
from time import sleep
from os import system

class SnakeGameDemo001:
    def __init__(self):
        self.__states_info = (
                ('SplashScreen', (1,1), {}, False),
                ('Home', (0,-1), {'q':5, 'g':2, 'c':3}, False),
                ('InGame', (0,-1), {'h':1, 'p':4}, False),
                ('Config', (0,-1), {'h':1}, False),
                ('Paused', (0,-1), {'g':2, 'h':1}, False),
                ('Quit', (0,-1), {}, True),
            )
        self.__initial_state = 0
        self.__current_state = None
        self.__change_state(self.__initial_state)
        
    def __change_state(self, new_state) -> bool:
        self.__current_state = new_state
        state_info = self.__states_info[self.__current_state]
        system('cls')
        print(state_info[0])
        if state_info[1][0]:
            sleep(state_info[1][0])
            self.__change_state(state_info[1][1])
        
    def is_ended(self)->bool:
        return self.__states_info[self.__current_state][3]
        
    def tic(self):
        if kbhit():
            input_char = getch().lower().decode('UTF-8')
            state = self.__states_info[self.__current_state]
            if input_char in state[2]:
                self.__change_state(state[2][input_char])

def main001():
    demo = SnakeGameDemo001()

    while not demo.is_ended():
        demo.tic()
     


 # --------------------------------------
 # --------------------------------------
 # --------------------------------------
 
    
    
from enum import Enum, auto

class SnakeGameDemo002:
    
    class State(Enum):
        SPLASH_SCREEN = (auto(), 'SplashScreen', False)
        HOME = (auto(), 'Home', False)
        IN_GAME = (auto(), 'InGame', False)
        CONFIG = (auto(), 'Configuration', False)
        PAUSED = (auto(), 'Paused', False)
        QUIT = (auto(), 'Quit', True)
    
        def __init__(self, state_id, text, quitting):
            self.state_id = state_id
            self.text = text
            self.quitting = quitting
            
        @staticmethod
        def _finalize():
            SnakeGameDemo002.State.SPLASH_SCREEN.sleeping = (
                1, SnakeGameDemo002.State.HOME)
            SnakeGameDemo002.State.HOME.sleeping = (0, None)
            SnakeGameDemo002.State.IN_GAME.sleeping = (0, None)
            SnakeGameDemo002.State.CONFIG.sleeping = (0, None)
            SnakeGameDemo002.State.PAUSED.sleeping = (0, None)
            SnakeGameDemo002.State.QUIT.sleeping = (0, None)
            
            SnakeGameDemo002.State.SPLASH_SCREEN.keys = {}
            SnakeGameDemo002.State.HOME.keys = {
                    'q':SnakeGameDemo002.State.QUIT, 
                    'g':SnakeGameDemo002.State.IN_GAME, 
                    'c':SnakeGameDemo002.State.CONFIG
                }
            SnakeGameDemo002.State.IN_GAME.keys = {
                    'h':SnakeGameDemo002.State.HOME, 
                    'p':SnakeGameDemo002.State.PAUSED
                }
            SnakeGameDemo002.State.CONFIG.keys = {
                    'h':SnakeGameDemo002.State.HOME
                }
            SnakeGameDemo002.State.PAUSED.keys = {
                    'g':SnakeGameDemo002.State.IN_GAME, 
                    'h':SnakeGameDemo002.State.HOME
                }
            SnakeGameDemo002.State.QUIT.keys = {}
            
    def __init__(self):
        self.__initial_state = SnakeGameDemo002.State.SPLASH_SCREEN
        self.__current_state = None
        self.__change_state(self.__initial_state)
        
    def __change_state(self, new_state) -> bool:
        self.__current_state = new_state
        system('cls')
        print(self.__current_state.text)
        if self.__current_state.sleeping[0]:
            sleep(self.__current_state.sleeping[0])
            self.__change_state(SnakeGameDemo002.State(self.__current_state.sleeping[1]))
        
    def is_ended(self)->bool:
        return self.__current_state.quitting
        
    def tic(self):
        if kbhit():
            input_char = getch().lower().decode('UTF-8')
            if input_char in self.__current_state.keys:
                self.__change_state(self.__current_state.keys[input_char])

SnakeGameDemo002.State._finalize()

def main002():
    demo = SnakeGameDemo002()

    while not demo.is_ended():
 
       demo.tic()
       


 # --------------------------------------
 # --------------------------------------
 # --------------------------------------



class GameState:
    
    def __init__(self, name: str, terminal: bool = False):
        self.name = name
        self.terminal = terminal
        self.timed_transition = None
        self.keyboard_transitions = {}
        
    def set_timed_transition(self, time: float, gameState: 'GameState'):
        self.timed_transition = (time, gameState)
        
    def add_keyboard_transition(self, keyboard_transition: str, gameState: 'GameState'):
        self.keyboard_transitions[keyboard_transition] = gameState

    def is_keyboard_transiting(self, actual_key):
        return self.keyboard_transitions.get(actual_key, None)

    def wait_for_time_transiting(self):
        if self.timed_transition:
            sleep(self.timed_transition[0])
            return self.timed_transition[1]
        else:
            return None


class SnakeGameDemo003:
    def __init__(self):
        self.states = []
        self.initial_state = None
        self.current_state = None
        
    def add_state(self, state: GameState):
        self.states.append(state)
        
    def set_initial_state(self, initial_state: GameState):
        if initial_state in self.states:
            self.initial_state = initial_state
            self.__set_new_state(self.initial_state)

    def __set_new_state(self, state):
        system('cls')
        self.current_state = state
        print(self.current_state.name)
        possible_next_state = self.current_state.wait_for_time_transiting()
        if possible_next_state:
            self.__set_new_state(possible_next_state)

    def tic(self):
        if kbhit():
            input_char = getch().lower().decode('UTF-8')
            possible_next_state = self.current_state.is_keyboard_transiting(input_char)
            if possible_next_state:
                self.__set_new_state(possible_next_state)
            
        
            
    
        
def main003():
    demo = SnakeGameDemo003()
    
    splashScreenState = GameState('SplashScreen', False)
    homeState = GameState('Home', False)
    configState = GameState('Configuration', False)
    inGameState = GameState('In Game', False)
    pausedState = GameState('Paused', False)
    quitState = GameState('Quit', True)
    
    splashScreenState.set_timed_transition(1, homeState)
    homeState.add_keyboard_transition('c', configState)
    homeState.add_keyboard_transition('g', inGameState)
    homeState.add_keyboard_transition('q', quitState)
    inGameState.add_keyboard_transition('h', homeState)
    inGameState.add_keyboard_transition('p', pausedState)
    configState.add_keyboard_transition('h', homeState)
    pausedState.add_keyboard_transition('g', inGameState)
    
    demo.add_state(splashScreenState)
    demo.add_state(homeState)
    demo.add_state(configState)
    demo.add_state(inGameState)
    demo.add_state(pausedState)
    demo.add_state(quitState)
    demo.set_initial_state(splashScreenState)
    
    while not demo.current_state.terminal:
        demo.tic()


          
 # --------------------------------------
 # --------------------------------------
 # --------------------------------------


    
if __name__ == '__main__':
    main003()