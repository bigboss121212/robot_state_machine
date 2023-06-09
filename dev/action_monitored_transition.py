from time import perf_counter
from typing import Callable
from conditional_transition import ConditionalTransition
from state_transition import State
# from typing import TYPE_CHECKING

# if TYPE_CHECKING:
#     from state_transition import State



class ActionTransition(ConditionalTransition):
    '''
    ActionTransition contient une liste d'actions de transition 
    et permet de les exécuter.
    '''
    Action = Callable[[], None] 

    def __init__(self, next_state: State = None):
        super().__init__(next_state)
        self.__transiting_actions = []

    def _do_transiting_action(self):
        for action in self.__transiting_actions:
            action()

    def add_transiting_action(self, action: Action):
        if not callable(action): 
            raise Exception(f'{action} n\'est pas une Action.')
        
        self.__transiting_actions.append(action)


class MonitoredTransition(ActionTransition):
    '''
    MonitoredTransition contient un compteur du nombre de transitions 
    et un temps de la dernière entrée.
    
    Il peut aussi contenir une valeur supplémentaire au choix.
    '''
    def __init__(self, next_state: State = None):
        super().__init__(next_state)
        self.__transit_count = 0
        self.__last_transit_time = None
        self.custom_value = None 

    @property
    def transit_count(self) -> int:
        return self.__transit_count

    @property
    def last_transit_time(self) -> float:
        return self.__last_transit_time

    def reset_transit_count(self):
        self.__transit_count = 0

    def reset_last_transit_time(self):
        self.__last_transit_time = None

    def _exec_transiting_action(self):
        self._do_transiting_action()
        self.__last_transit_time = perf_counter()
