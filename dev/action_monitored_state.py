from time import perf_counter
from typing import Callable
from state_transition import State
Parameters = State.Parameters


class ActionState(State):
    '''
    ActionState contient une liste d'actions à faire à l'entrée l'état, 
    une liste d'actions à faire pendant l'état
    et une liste d'actions à faire à la sortie de l'état.
    '''
    Action = Callable[[], None] 

    def __init__(self, parameter: Parameters = Parameters()):
        super().__init__(parameter) 
        self.__entering_actions = [] 
        self.__in_state_actions = [] 
        self.__exiting_actions = [] 

    def _do_entering_action(self):
        for action in self.__entering_actions:
            action()

    def _do_in_state_action(self):
        for action in self.__in_state_actions:
            action()

    def _do_exiting_action(self):
        for action in self.__exiting_actions:
            action()

    def add_entering_action(self, action: Action):
        if not callable(action): 
            raise Exception(f'{action} n\'est pas une Action.')
            
        self.__entering_actions.append(action)

    def add_in_state_action(self, action: Action):
        if not callable(action): 
            raise Exception(f'{action} n\'est pas une Action.')
        
        self.__in_state_actions.append(action)

    def add_exiting_action(self, action: Action):
        if not callable(action): 
            raise Exception(f'{action} n\'est pas une Action.')
        
        self.__exiting_actions.append(action)


class MonitoredState(ActionState):
    '''
    MonitoredState contient un compteur pour le nombre d'entrées dans l'état, 
    le dernier temps d'entrée dans l'état,
    et le dernier temps de sortie de l'état.
    
    Il peut aussi contenir une valeur supplémentaire au besoin.
    '''
    def __init__(self, parameters: Parameters = Parameters()):
        super().__init__(parameters)
        self.__counter_last_entry = None # derniere fois quon est entre dans letat (TEMPS)
        self.__counter_last_exit = None # derniere fois quon est sortie de letat (TEMPS)
        self.__entry_count = 0
        self.custom_value = None

    @property
    def entry_count(self) -> int:
        return self.__entry_count

    @property
    def last_entry_time(self) -> float:
        return self.__counter_last_entry

    @property
    def last_exit_time(self) -> float:
        return self.__counter_last_exit

    def reset_entry_count(self):
        self.__entry_count = 0

    def reset_last_times(self):
        self.__counter_last_entry = None 
        self.__counter_last_exit = None 

    def _exec_entering_action(self):
        '''
        Demande l'exécution des actions à faire à l'entrée d'un état,  
        après avoir enregistré le moment de la dernière entrée dans l'état 
        et incrémenté le compteur d'entrées dans l'état.
        '''
        self.__counter_last_entry = perf_counter()
        self.__entry_count += 1
        self._do_entering_action()

    def _exec_exiting_action(self):
        '''
        Demande l'exécution des actions à faire à l'entrée d'un état,  
        puis enregistre le moment de la dernière sortie de l'état.
        '''
        self._do_exit_action()
        self.__counter_last_exit = perf_counter()