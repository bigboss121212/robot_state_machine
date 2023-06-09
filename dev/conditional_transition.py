from state_transition import Transition
from conditions import Condition


class ConditionalTransition(Transition):
    '''
    ConditionalTransition contient une condition permettant 
    de savoir si on transitionnera selon sa validité.
    '''
    def __init__(self, condition: Condition = None):
        super().__init__()
        self.__condition = condition

    @property
    def is_valid(self) -> bool:
        return super().is_valid and self.__condition is not None
    
    @property
    def condition(self) -> Condition:
        return self.__condition

    @condition.setter
    def condition(self, condition: Condition):
        if not isinstance(condition, Condition):
            raise Exception(f'{condition} n\'est pas une condition.')
        self.__condition = condition

    def is_transiting(self) -> bool : 
        return self.__condition
