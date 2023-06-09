from abc import abstractmethod, ABC
from typing import Optional, Any
from action_monitored_state import MonitoredState
from time import perf_counter
NoneType = type(None)


class Condition(ABC):
    '''
    Une Condition est vraie ou fausse selon la méthode de 
    comparaison abstraite implémentée par ses enfants. 
    '''
    def __init__(self, inverse: bool = False):
        self.__inverse = inverse

    def __bool__(self): 
        return self.__inverse ^ self.compare() 

    @property
    @abstractmethod
    def compare(self) -> bool:
        '''
        Déterminer une condition qui retourne un bool qui indiquera si la transition peut avoir lieu.
        '''
        pass
 


class AlwaysTrueCondition(Condition):
    '''
    AlwaysTrueCondition est une condition qui retourne toujours Vrai. messemble c'tividant
    '''
    def __init__(self, inverse: bool = False):
        super().__init__(inverse)

    def compare(self):
        return True


class ValueCondition(Condition):
    '''
    ValueCondition est vrai si la valeur actuelle correspond à la valeur attendue
    préalablement initialisée.
    '''
    def __init__(self, initial_value: Any, expected_value: Any, inverse: bool = False):
        super().__init__(inverse)
        self.__expected_value = expected_value
        self.__value = initial_value

    @property
    def expected_value(self):
        return self.__expected_value

    @expected_value.setter
    def expected_value(self, expected_value: Any):
        self.__expected_value = expected_value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: Any):
        self.__value = value

    def compare(self):
        if type(self.__expected_value) == type(self.__value):
            return self.__value == self.__expected_value


class TimedCondition(Condition):
    '''
    TimedCondition est vrai si la durée atteind le temps du compteur de référence
    ou du temps actuel.
    '''
    def __init__(self, duration: float = 1, time_reference: Optional[float] = None, inverse: bool = False):
        if not isinstance(duration, float):
            raise Exception(f'{duration} n\'est pas une durée (float attendu).')
        if not isinstance(time_reference, (float, NoneType)):
            raise Exception(f'{time_reference} n\'est pas un temps de référence.')
        if not isinstance(inverse, bool):
            raise Exception(f'{inverse} n\'est pas un bool.')

        super().__init__(inverse)
        self.__counter_duration = duration
        self.__counter_reference = time_reference if time_reference else perf_counter()

    def compare(self):
        return self.__counter_duration >= self.__counter_reference

    @property
    def counter_duration(self):
        return self.__counter_duration

    @counter_duration.setter
    def counter_duration(self, counter_duration: float):
        if not isinstance(counter_duration, float):
            raise Exception(f'{counter_duration} n\'est pas un float.')
        
        self.__counter_duration = counter_duration

    def reset(self):
        self.__counter_reference = perf_counter()
        pass
    


class ManyConditions(Condition):
    '''
    ManyConditions contient une liste de conditions diverses.
    
    Il est possible d'en ajouter une ou plusieurs à la fois, ou encore
    d'ajouter une liste de conditions.
    '''
    def __init__(self, inverse: bool = False):
        super().__init__(inverse)
        self._conditions = []

    def add_condition(self, condition: Condition):
        if not isinstance(condition, Condition):
            raise Exception(f'{condition} n\'est pas une condition.')
        self._conditions.append(condition)

    def add_conditions_list(self, condition_list): #: list[Condition]
        for condition in condition_list:
            if not isinstance(condition, Condition):
                raise TypeError(f'{condition} n\'est pas une condition.')
            self._conditions.append(condition)
    
    def add_conditions(self, *args): 
        for condition in args:
            if not isinstance(condition, Condition):
                raise TypeError(f'{condition} n\'est pas une condition.')
            self._conditions.append(condition)


class AllConditions(ManyConditions):
    '''
    AllConditions est vrai si toutes les conditions de la liste sont vraies.
    '''
    def __init__(self, inverse: bool = False):
        super().__init__(inverse)

    def compare(self): 
        for condition in self._conditions:
            if not condition:
                return False
        return True


class NoneConditions(ManyConditions):
    '''
    NoneConditions est vrai si toutes les conditions de la liste sont fausses.
    '''
    def __init__(self, inverse: bool = False):
        super().__init__(inverse)

    def compare(self): 
        for condition in self._conditions:
            if condition:
                return False
        return True
    

class AnyConditions(ManyConditions):
    '''
    AnyConditions est vrai si au moins une des conditions de la liste est vraie.
    '''
    def __init__(self, inverse: bool = False):
        super().__init__(inverse)

    def compare(self): 
        for condition in self._conditions:
            if condition:
                return True
        return False
        
        

class MonitoredStateCondition(Condition):
    '''
    MonitoredStateCondition est une Condition qui contient un MonitoredState.
    '''
    def __init__(self, monitored_state: MonitoredState, inverse: bool = False):
        super().__init__(inverse)
        self._monitored_state = monitored_state

    @property
    def monitored_state(self):
        return self._monitored_state

    @monitored_state.setter
    def monitored_state(self, monitored_state: MonitoredState):
        if not isinstance(monitored_state, MonitoredState):
            raise Exception(f'{monitored_state} n\'est pas un monitored state.')
        
        self._monitored_state = monitored_state


class StateEntryDurationCondition(MonitoredStateCondition):
    '''
    StateEntryDurationCondition est vrai si le temps d'entrée de l'état est 
    plus grand ou égal à la durée déterminée.
    '''
    def __init__(self, duration: float, monitored_state: MonitoredState, inverse: bool = False):
        super().__init__(monitored_state, inverse)
        self.__duration = duration

    @property
    def duration(self):
        return self.__duration

    @duration.setter
    def duration(self, duration: float):
        if not isinstance(duration, float):
            raise Exception(f'{duration} n\'est pas un float.')
        
        self.__duration = duration

    def compare(self):
        return perf_counter() - self._monitored_state.last_entry_time >= self.__duration


class StateValueCondition(MonitoredStateCondition):
    '''
    StateValueCondition est vrai si la valeur attendue correspond à 
    la valeur au choix prédéterminée.
    '''
    def __init__(self, expected_value: Any, monitored_state: MonitoredState, inverse: bool = False):
        super().__init__(monitored_state, inverse)
        self.__expected_value = expected_value

    @property
    def expected_value(self):
        return self.__expected_value

    @expected_value.setter
    def expected_value(self, expected_value: Any):
        self.__expected_value = expected_value

    def compare(self): 
        if type(self.__expected_value) == type(self.monitored_state.custom_value):
            return self.__expected_value == self.monitored_state.custom_value
        else:
            raise Exception("Les types de self.__expected_value et self.monitored_state.custom_value ne sont pas les même. La condition ne peut pas être comparée.")


class StateValueInferiorCondition(MonitoredStateCondition):
    '''
    StateValueInferiorCondition est vrai si la valeur attendue est égale ou plus petite 
    la valeur au choix prédéterminée.
    '''
    def __init__(self, expected_value: Any, monitored_state: MonitoredState, inverse: bool = False):
        super().__init__(monitored_state, inverse)
        self.__expected_value = expected_value

    @property
    def expected_value(self):
        return self.__expected_value

    @expected_value.setter
    def expected_value(self, expected_value: Any):
        self.__expected_value = expected_value

    def compare(self): 
        if type(self.__expected_value) == type(self.monitored_state.custom_value):
            return self.__expected_value >= self.monitored_state.custom_value
        else:
            raise Exception("Les types de self.__expected_value et self.monitored_state.custom_value ne sont pas les même. La condition ne peut pas être comparée.")


class StateEntryCountCondition(MonitoredStateCondition):
    '''
    StateEntryCountCondition est vrai si le compteur de référence 
    est plus grand que le nombre d'entrée dans l'état attendu.
    
    Si l'auto_reset est vrai, on ajuste le compteur de référence au nombre d'entrée 
    actuel dans l'état. 
    '''
    def __init__(self, expected_count: int, monitored_state: MonitoredState, auto_reset: bool = True, inverse: bool = False):
        super().__init__(monitored_state, inverse)
        self.__auto_reset = auto_reset 
        self.__ref_count = self._monitored_state.entry_count 
        self.__expected_count = expected_count

    @property
    def expected_count(self):
        return self.__expected_count

    @expected_count.setter
    def expected_count(self, expected_count: int):
        if not isinstance(expected_count, int):
            raise Exception(f'{expected_count} n\'est pas un int.')
        
        self.__expected_count = expected_count

    def compare(self):
        if self._monitored_state.entry_count - self.__ref_count >= self.__expected_count:
            if self.__auto_reset:
                self.reset_count()
            return True
        return False

    def reset_count(self): 
        self.__ref_count = self._monitored_state.entry_count 


class RemoteControlCondition(Condition):
    '''
    RemoteControlCondition permet de saisir une valeur à partir de la télécommande du robot et de la comparer 
    à une valeur attendue. Si les valeurs correspondent, la condition est vraie. 
    '''
    def __init__(self, expected_value: str, remote_control: Any, inverse: bool = False):
        super().__init__(inverse)
        self.__remote_control = remote_control 
        self.__expected_value = expected_value
        self.__keycodes = ['~', 'up', 'left', 'ok', 'right', 'down', '1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '0', '#']
        #self.__previous_read = None
        #self.__current_read = None

    @property
    def expected_value(self):
        return self.__expected_value

    @expected_value.setter
    def expected_value(self, expected_value: str): 
        if expected_value not in self.__keycodes:
            raise Exception(f'{expected_value} n\'est pas dans la liste des keycodes possibles de la télécommande.')
        
        self.__expected_value = expected_value

    def compare(self):
        # intégrer la bascule ici
        #self.__current_read = self.__remote_control.read()
        #if self.__previous_read != self.__current_read:
        #    self.__previous_read = self.__current_read
        #return self.__keycodes[self.__current_read] == self.__expected_value 

        # sinon tel qu'avant
        return self.__keycodes[self.__remote_control.read()] == self.__expected_value

