from enum import Enum, auto
from state_transition import State, Transition
from time import perf_counter
    
    
class FiniteStateMachine:
    '''
    Permet de gérer les états et leurs transitions d'une machine applicative.
    
    Son constructeur a besoin d'un layout à l'initialisation. Un layout comprend 
    une liste de ses états (State), ainsi que son état initial.
    '''
    class Layout:
        '''
        Layout contient une liste des états et un état initial.
        
        Il est possible d'ajouter un état ou une liste d'états.
        '''
        def __init__(self):
            self.__initial_state = None
            self.__state_list = []

        @property
        def is_valid(self) -> bool:
            if not self.__state_list:
                return False
            for state in self.__state_list:
                if not state.is_valid:
                    return False
            return True
            
        @property
        def initial_state(self) -> State:
            return self.__initial_state 
     
        @initial_state.setter
        def initial_state(self, state: State):
            self.__initial_state = state

        def add_state(self, state: State):
            if not isinstance(state, State):
                raise TypeError(f'{state} n\'est pas un State.')
            
            self.__state_list.append(state)

        def add_states(self, state_list): #: list[State]
            for state in state_list:
                if not isinstance(state, State):
                    raise TypeError(f'{state} n\'est pas un State.')
                
                self.__state_list.append(state)
                
    class OperationalState(Enum):
        UNINITIALIZED = auto()
        IDLE = auto()
        RUNNING = auto()
        TERMINAL_REACHED = auto()

    def __init__(self, layout: Layout, uninitialized: bool = True):
        if not layout.is_valid:
            raise Exception("Au moins un des layout n'est pas valide.")
        self.__layout = layout
        if uninitialized: 
            self.reset()

    @property
    def current_operational_state(self) -> OperationalState:
        '''
        L'action en cours de l'engin de résolution.
        '''
        return self.__current_operational_state
    
    @property
    def current_applicative_state(self) -> State:
        '''
        L'état courant de la partie applicative.
        '''
        return self.__current_applicative_state
    
    def _transit_by(self, transition: Transition):
        self.__current_applicative_state._exec_exiting_action()
        self.__current_applicative_state = transition.next_state
        transition._exec_transiting_action()
        self.__current_applicative_state._exec_entering_action()
    
    def transit_to(self, state: State):
        self.__current_applicative_state._exec_exiting_action()
        self.__current_applicative_state = state
        self.__current_applicative_state._exec_entering_action()

    def track(self) -> bool: 
        transition = self.__current_applicative_state.is_transiting
        if (transition):
            self._transit_by(transition)
        else:
            self.__current_applicative_state._exec_in_state_action()
        
        return self.__current_operational_state is not FiniteStateMachine.OperationalState.TERMINAL_REACHED
    
    def reset(self):
        if self.__current_applicative_state is not None:
            self.__current_applicative_state._exec_exiting_action()
        self.__current_operational_state = FiniteStateMachine.OperationalState.IDLE
        self.__current_applicative_state = self.__layout.initial_state
        self.__current_applicative_state._exec_entering_action()


    def run(self, reset: bool = True, time_budget: float = None): 
        self.__current_operational_state = FiniteStateMachine.OperationalState.RUNNING
        still_running = True   
        init_time = perf_counter()
        
        if reset:
            self.reset()
        
        while still_running:
            still_running = self.track()
            if time_budget is not None:
                elapsed_time = perf_counter() - init_time
                still_running = elapsed_time < time_budget 

    def stop(self):
        self.__current_operational_state = FiniteStateMachine.OperationalState.IDLE

