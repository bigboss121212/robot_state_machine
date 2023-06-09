from abc import abstractmethod, ABC


class State():
    '''
    State est une classe qui contient un état.
    
    Chaque état possede ses propres paramètres indiquant s'il est dans un état 
    terminal ou non. Chaque état détermine une action doit être faite en entrant et 
    en sortant de l'état. 
    Chaque état possède également sa propre liste de transition. Un état est 
    valide s'il possède au moins une transition et si chacune d'elle 
    est valide.
    
    Les paramètres sont définis à l'initialisation de l'état, tandis que 
    les transitions sont ajoutées par la suite.
    '''

    class Parameters:
        def __init__(self, terminal=False, entering=False, exiting=False):
            self.terminal = terminal
            self.do_in_state_action_when_entering = entering
            self.do_in_state_action_when_exiting = exiting

    def __init__(self, parameter: Parameters=Parameters()):
        self.__parameters = parameter
        self.__transition_list = []

    def add_transition(self, transition: 'Transition'):
        if not isinstance(transition, Transition):
            raise Exception(f'{transition} n\'est pas une Transition.')
        
        self.__transition_list.append(transition)

    def _exec_entering_action(self):
        '''
        Demande l'exécution des actions à faire à l'entrée d'un état. 
        Si requis, on exécute également les actions à faire pendant l'état.
        '''
        self._do_entering_action()
        if (self.__parameters.do_in_state_action_when_entering):
            self._exec_in_state_action() 

    def _exec_in_state_action(self):
        '''
        Demande l'exécution des actions à faire pour la durée de l'état. 
        '''
        self._do_in_state_action() 
    
    def _exec_exiting_action(self):
        '''
        Demande l'exécution des actions à faire à la sortie d'un état. 
        Si requis, on exécute également les actions à faire pendant l'état.
        '''
        if (self.__parameters.do_in_state_action_when_exiting):
            self._exec_in_state_action() 
        self._do_exit_action() 
    
    def _do_entering_action(self): 
        pass

    def _do_in_state_action(self): 
        pass

    def _do_exit_action(self): 
        pass
    
    @property
    def is_valid(self) -> bool:
        '''
        Retourne un booléen sur la validité de l'état
        en vérifiant la présence d'au moins une transition
        et de la validité de chacun d'eux.
        '''
        if self.__transition_list:
            for transition in self.__transition_list:
                if not transition.is_valid:
                    return False
        return True

    @property
    def is_terminal(self) -> bool:
        '''
        Vérifie si l'état est terminal.
        '''
        return self.__parameters.terminal

    @property
    def is_transiting(self) -> 'Transition':
        '''
        Retourne la transition qui transite parmi la 
        liste de transitions contenues dan l'État.
        '''
        for transition in self.__transition_list:
            if transition.is_transiting():
                return transition


class Transition(ABC):
    '''
    Transition contient l'état suivant et sait si elle doit transiter selon 
    sa méthode abstraite is_transiting().
    '''
    def __init__(self, state: 'State' = None):
        self.__next_state = state
    
    @property
    def is_valid(self) -> bool:
        '''
        Détermine la validité de la transition.
        pour le layout
        '''
        return self.__next_state is not None
    
    @property
    def next_state(self) -> State:
        return self.__next_state
    
    @next_state.setter
    def next_state(self, state: State):
        if not isinstance(state, State):
            raise Exception(f'{state} n\'est pas une state.')
        
        self.__next_state = state
    
    @property
    @abstractmethod
    def is_transiting(self) -> bool:
        '''
        Déterminer si la transition doit transiter ou non.
        '''
        pass
    
    def _exec_transiting_action(self):
        self._do_transiting_action()
    
    def _do_transiting_action(self):
        pass
