from finite_state_machine import FiniteStateMachine
from conditions import StateValueCondition, StateEntryDurationCondition
from conditional_transition import ConditionalTransition
from typing import Callable, Any
from enum import Enum, auto
from action_monitored_state import MonitoredState


class Blinker(FiniteStateMachine):
    StateGenerator = Callable[[], MonitoredState]

    def __init__(self, off_state_generator: StateGenerator, on_state_generator: StateGenerator):
        self.__on = on_state_generator()
        if not isinstance(self.__on, MonitoredState):
            raise Exception(f'{self.__on} n\'est pas une MonitoredState.')
        self.__off = off_state_generator()
        if not isinstance(self.__off, MonitoredState):
            raise Exception(f'{self.__off} n\'est pas une MonitoredState.')
        self.__on_duration = on_state_generator()
        if not isinstance(self.__on_duration, MonitoredState):
            raise Exception(f'{self.__on_duration} n\'est pas une MonitoredState.')
        self.__off_duration = off_state_generator()
        if not isinstance(self.__off_duration, MonitoredState):
            raise Exception(f'{self.__off_duration} n\'est pas une MonitoredState.')
        self.__blink_on = on_state_generator()
        if not isinstance(self.__blink_on, MonitoredState):
            raise Exception(f'{self.__blink_on} n\'est pas une MonitoredState.')
        self.__blink_off = off_state_generator()
        if not isinstance(self.__blink_off, MonitoredState):
            raise Exception(f'{self.__blink_off} n\'est pas une MonitoredState.')
        self.__blink_stop_on = on_state_generator()
        if not isinstance(self.__blink_stop_on, MonitoredState):
            raise Exception(f'{self.__blink_stop_on} n\'est pas une MonitoredState.')
        self.__blink_stop_off = off_state_generator()
        if not isinstance(self.__blink_stop_off, MonitoredState):
            raise Exception(f'{self.__blink_stop_off} n\'est pas une MonitoredState.')
        
        # duration on off
        self.__on_duration_condition = self.__connect_timed_state_to_transit(self.__on_duration, self.__on_duration, self.__off)
        self.__off_duration_condition = self.__connect_timed_state_to_transit(self.__off_duration, self.__off_duration, self.__on)
        
        # MonitoredState blink_begin 
        self.__blink_begin = MonitoredState()
        self.__connect_monitoredstate_to_state(True, self.__blink_begin, self.__blink_on)
        self.__connect_monitoredstate_to_state(False, self.__blink_begin, self.__blink_off)
        
        self.__blink_on_condition = self.__connect_timed_state_to_transit(self.__blink_on, self.__blink_on, self.__blink_off)
        self.__blink_off_condition = self.__connect_timed_state_to_transit(self.__blink_off, self.__blink_off, self.__blink_on)
        
        # MonitoredState blink_stop_begin 
        self.__blink_stop_begin = MonitoredState()
        # Transition blink_stop_begin vers blink_stop_on et blink_stop_off
        self.__connect_monitoredstate_to_state(True, self.__blink_stop_begin, self.__blink_stop_on)
        self.__connect_monitoredstate_to_state(False, self.__blink_stop_begin, self.__blink_stop_off)
        
        # MonitoredState blink_stop_end 
        self.__blink_stop_end = MonitoredState()
        # Transition blink_stop_end vers on et off
        self.__connect_monitoredstate_to_state(True, self.__blink_stop_end, self.__on)
        self.__connect_monitoredstate_to_state(False, self.__blink_stop_end, self.__off)

        # Transition blink_stop_on and off vers blink_stop_end (vérifications des transitions vers blink_stop_end prioritaires)
        self.__blink_on_stop_to_end_condition = self.__connect_timed_state_to_transit(self.__blink_stop_begin, self.__blink_stop_on, self.__blink_stop_end)
        self.__blink_off_stop_to_end_condition = self.__connect_timed_state_to_transit(self.__blink_stop_begin, self.__blink_stop_off, self.__blink_stop_end)
        # Transitions blink_stop_on <-> blink_stop_off
        self.__blink_on_stop_to_off_condition = self.__connect_timed_state_to_transit(self.__blink_stop_on, self.__blink_stop_on, self.__blink_stop_off)
        self.__blink_off_stop_to_on_condition = self.__connect_timed_state_to_transit(self.__blink_stop_off, self.__blink_stop_off, self.__blink_stop_on)

        # Création du layout finite state machine
        states = [self.__on, self.__off, self.__on_duration, self.__off_duration, self.__blink_begin, self.__blink_on, self.__blink_off]
        layout = FiniteStateMachine.Layout()
        layout.add_states(states)
        layout.initial_state = self.__off
        super().__init__(layout)


    @property
    def is_off(self) -> bool:
        """Aller récupérer si je suis dans un état off selon le current applicative state."""
        return self.current_applicative_state == self.__off

    @property
    def is_on(self) -> bool:
        """Aller récupérer si je suis dans un état on selon le current applicative state."""
        return self.current_applicative_state == self.__on

    def __connect_monitoredstate_to_state(self, expected_value: Any, monitored_state: MonitoredState, next_state: MonitoredState):
        '''
        Crée une transition à partir d'une StateValueCondition 
        qui nécessite une expected_value et l'ajoute au monitored_state 
        passée en paramètre. 
        Le next_state correspond au prochain état ajouté à la transition.
        '''
        condition = StateValueCondition(expected_value, monitored_state)
        transit = ConditionalTransition(condition)
        transit.next_state = next_state
        monitored_state.add_transition(transit)

    def __connect_timed_state_to_transit(self, monitored_state: MonitoredState, state_from: MonitoredState, state_to: MonitoredState, time: float = 0) -> StateEntryDurationCondition:
        '''
        Crée une transition à partir d'une StateEntryDurationCondition 
        qui nécessite un time. 
        Le state_from correspond à l'état auquel on ajoute la transition. 
        Le state_to correspond au prochain état ajouté à la transition.
        Retourne la condition pour pouvoir en modifier son paramètre duration.
        '''
        condition = StateEntryDurationCondition(time, monitored_state)
        transit = ConditionalTransition(condition)
        transit.next_state = state_to
        state_from.add_transition(transit)
        return condition

    def turn_on(self):
        self.transit_to(self.__on)

    def turn_off(self):
        self.transit_to(self.__off)
    
    def turn_on_dur(self, duration: float = None):
        self.__on_duration_condition.duration = duration
        self.transit_to(self.__on_duration)

    def turn_off_dur(self, duration: float = None):
        self.__off_duration_condition.duration = duration
        self.transit_to(self.__off_duration)

    def blink1(self, cycle_duration: float = 1.0,  percent_on: float= 0.5, begin_on : bool = True):
        '''
        cycle_duration permet de faire clignoter selon un cycle. 
        percent_on permet de spécifier le temps allumé par rapport à la durée du cycle. 
        begin_on permet de savoir si on commence le cycle allumé. 
        '''
        self.__blink_begin.custom_value = begin_on
        self.__blink_on_condition.duration = cycle_duration * percent_on
        self.__blink_off_condition.duration = cycle_duration *  (1 - percent_on)
        self.transit_to(self.__blink_begin)

    def blink2(self, total_duration: float, cycle_duration: float = 1.0, percent_on: float = 0.5, begin_on: bool = True, end_off: bool = True):
        '''
        total_duration détermine une durée de clignotement. 
        cycle_duration permet de faire clignoter un nombre de fois selon la durée. 
        percent_on permet de spécifier le temps allumé par rapport à la durée du cycle. 
        begin_on permet de savoir si on commence le cycle allumé. 
        end_off permet de savoir si on termine le cycle fermé.
        '''
        self.__blink_stop_begin.custom_value = begin_on
        self.__blink_off_stop_to_on_condition.duration = cycle_duration *  (1 - percent_on)
        self.__blink_off_stop_to_end_condition.duration = total_duration
        self.__blink_on_stop_to_off_condition.duration = cycle_duration * percent_on
        self.__blink_on_stop_to_end_condition.duration = total_duration
        self.__blink_stop_end.custom_value = end_off
        self.transit_to(self.__blink_stop_begin)

    def blink3(self, total_duration: float, n_cycles: int, percent_on: float = 0.5, begin_on: bool = True, end_off: bool = True):
        '''
        total_duration détermine une durée de clignotement. 
        n_cycles permet de faire clignoter un nombre de fois selon la durée. 
        percent_on permet de spécifier le temps allumé par rapport à la durée du cycle. 
        begin_on permet de savoir si on commence le cycle allumé. 
        end_off permet de savoir si on termine le cycle fermé. 
        '''
        self.__blink_stop_begin.custom_value = begin_on
        self.__blink_off_stop_to_on_condition.duration = (total_duration/n_cycles) *  (1 - percent_on)
        self.__blink_off_stop_to_end_condition.duration = total_duration
        self.__blink_on_stop_to_off_condition.duration = (total_duration/n_cycles) * percent_on
        self.__blink_on_stop_to_end_condition.duration = total_duration
        self.__blink_stop_end.custom_value = end_off
        self.transit_to(self.__blink_stop_begin)

    def blink4(self, n_cycles: int, cycle_duration: float = 1.0, percent_on: float= 0.5, begin_on : bool = True, end_off: bool = True):
        '''
        n_cycles permet de faire clignoter un nombre de fois selon la durée. 
        cycle_duration permet de faire clignoter un nombre de fois selon la durée. 
        percent_on permet de spécifier le temps allumé par rapport à la durée du cycle. 
        begin_on permet de savoir si on commence le cycle allumé. 
        end_off permet de savoir si on termine le cycle fermé. 
        '''
        self.__blink_stop_begin.custom_value = begin_on
        self.__blink_off_stop_to_on_condition.duration =  cycle_duration * (1 - percent_on)
        self.__blink_off_stop_to_end_condition.duration = (n_cycles*cycle_duration)
        self.__blink_on_stop_to_off_condition.duration = cycle_duration * percent_on
        self.__blink_on_stop_to_end_condition.duration = (n_cycles*cycle_duration)
        self.__blink_stop_end.custom_value = end_off
        self.transit_to(self.__blink_stop_begin)
        

    def blink(self, **kwargs):
        '''
            Permet une opération de clignotement selon différents paramètres.
            Les paramètres sont les suivants :
            - cycle_duration : durée d'un cycle de clignotement 
            - total_duration : durée totale de clignotement
            - n_cycles : nombre de cycles de clignotement
            - percent_on : pourcentage de temps on par rapport à la durée d'un cycle
            - begin_on : permet de savoir si on commence le cycle on
            - end_off : permet de savoir si on termine le cycle off

            Les paramètres sont à utiliser selon les combinaisons suivantes :
            - cycle_duration, percent_on, begin_on
            - total_duration, cycle_duration, percent_on, begin_on, end_off
            - total_duration, n_cycles, percent_on, begin_on, end_off
            - n_cycles, cycle_duration, percent_on, begin_on, end_off
        '''

        begin_on = kwargs.get('begin_on', True)
        percent_on = kwargs.get('percent_on', 0.5)
        
        if 'total_duration' in kwargs:
            total_duration = kwargs.get('total_duration')
            on_to_end = total_duration
            off_to_end = total_duration  
            
            if 'n_cycles' in kwargs:
                n_cycles = kwargs.get('n_cycles')
                cycle_duration = total_duration / n_cycles
                on_to_off = cycle_duration * percent_on
                off_to_on = cycle_duration * (1 - percent_on)

            elif 'cycle_duration' in kwargs:
                cycle_duration = kwargs.get('cycle_duration')
                on_to_off = cycle_duration * percent_on
                off_to_on = cycle_duration * (1 - percent_on)

        elif 'n_cycles' in kwargs and 'cycle_duration' in kwargs:
                n_cycles = kwargs.get('n_cycles')
                cycle_duration = kwargs.get('cycle_duration')
                on_to_off = cycle_duration * percent_on
                off_to_on = cycle_duration * (1 - percent_on)
                on_to_end = n_cycles * cycle_duration
                off_to_end = n_cycles * cycle_duration
        
        self.__blink_begin.custom_value = begin_on 
        
        if 'end_off' not in kwargs and 'cycle_duration' in kwargs:
            cycle_duration = kwargs.get('cycle_duration')
            self.__blink_on_condition.duration = cycle_duration * percent_on
            self.__blink_off_condition.duration = cycle_duration * (1 - percent_on)
            self.transit_to(self.__blink_begin) 
        
        else:
            self.__blink_on_stop_to_off_condition.duration = on_to_off
            self.__blink_on_stop_to_end_condition.duration = on_to_end
            self.__blink_off_stop_to_on_condition.duration =  off_to_on
            self.__blink_off_stop_to_end_condition.duration = off_to_end
            self.__blink_stop_end.custom_value = kwargs.get('end_off', True)
            self.transit_to(self.__blink_stop_begin)

class SideBlinker():
    StateGenerator = Callable[[], MonitoredState]

    class Side(Enum):
        LEFT = auto()
        RIGHT = auto()
        BOTH = auto()
        LEFT_RECIPROCAL = auto()
        RIGHT_RECIPROCAL = auto()

    def __init__(self, left_off_state_generator: StateGenerator, left_on_state_generator: StateGenerator, right_off_state_generator: StateGenerator, right_on_state_generator: StateGenerator):
        self.__left_blinker = Blinker(left_off_state_generator, left_on_state_generator)
        self.__right_blinker = Blinker(right_off_state_generator, right_on_state_generator)

    def is_off(self, side: Side) -> bool:
        if side == SideBlinker.Side.LEFT:
            return self.__left_blinker.is_off
        if side == SideBlinker.Side.RIGHT:
            return self.__right_blinker.is_off
        if side == SideBlinker.Side.BOTH:
            return self.__right_blinker.is_off and self.__left_blinker.is_off
        if side == SideBlinker.Side.LEFT_RECIPROCAL:
            return self.__right_blinker.is_on and self.__left_blinker.is_off
        if side == SideBlinker.Side.RIGHT_RECIPROCAL:
            return self.__right_blinker.is_off and self.__left_blinker.is_on

    def is_on(self, side: Side) -> bool:
        if side == SideBlinker.Side.LEFT:
            return self.__left_blinker.is_on
        elif side == SideBlinker.Side.RIGHT:
            return self.__right_blinker.is_on
        elif side == SideBlinker.Side.BOTH:
            return self.__right_blinker.is_on and self.__left_blinker.is_on
        elif side == SideBlinker.Side.LEFT_RECIPROCAL:
            return self.__right_blinker.is_off and self.__left_blinker.is_on
        elif side == SideBlinker.Side.RIGHT_RECIPROCAL:
            return self.__right_blinker.is_on and self.__left_blinker.is_off

    def turn_on(self, side: Side, duration: float = None):
        if side == SideBlinker.Side.LEFT:
            if duration == None:
                self.__left_blinker.turn_on()
            else:
                self.__left_blinker.turn_on_dur(duration)
        elif side == SideBlinker.Side.RIGHT:
            if duration == None:
                self.__right_blinker.turn_on()
            else:
                self.__right_blinker.turn_on_dur(duration)
        elif side == SideBlinker.Side.BOTH:
            if duration == None:
                self.__right_blinker.turn_on()
                self.__left_blinker.turn_on()
            else:
                self.__right_blinker.turn_on_dur(duration)
                self.__left_blinker.turn_on_dur(duration)
        elif side == SideBlinker.Side.LEFT_RECIPROCAL:
            if duration == None:
                self.__right_blinker.turn_off() 
                self.__left_blinker.turn_on()
            else:
                self.__right_blinker.turn_off_dur(duration) 
                self.__left_blinker.turn_on_dur(duration)
        elif side == SideBlinker.Side.RIGHT_RECIPROCAL:
            if duration == None:
                self.__right_blinker.turn_on()
                self.__left_blinker.turn_off()
            else: 
                self.__right_blinker.turn_on_dur(duration)
                self.__left_blinker.turn_off_dur(duration)


    def turn_off(self, side: Side, duration: float = None):
        if side == SideBlinker.Side.LEFT:
            if duration == None:
                self.__left_blinker.turn_off()
            else:
                self.__left_blinker.turn_off_dur(duration)
        elif side == SideBlinker.Side.RIGHT:
            if duration == None:
                self.__right_blinker.turn_off()
            else:
                self.__right_blinker.turn_off_dur(duration)
        elif side == SideBlinker.Side.BOTH:
            if duration == None:
                self.__right_blinker.turn_off()
            else:
                self.__left_blinker.turn_off_dur(duration)
        elif side == SideBlinker.Side.LEFT_RECIPROCAL:
            if duration == None:
                self.__right_blinker.turn_on() 
                self.__left_blinker.turn_off()
            else:
                self.__right_blinker.turn_on_dur(duration) 
                self.__left_blinker.turn_off_dur(duration)
        elif side == SideBlinker.Side.RIGHT_RECIPROCAL:
            if duration == None:
                self.__right_blinker.turn_off()
                self.__left_blinker.turn_on()
            else:
                self.__right_blinker.turn_off_dur(duration)
                self.__left_blinker.turn_on_dur(duration)

    def blink1(self, side: Side, cycle_duration: float = 1.0, percent_on: float = 0.5, begin_on: bool = True):
        '''
        side détermine quel côté clignotera. 
        cycle_duration permet de faire clignoter selon un cycle. 
        percent_on permet de spécifier le temps allumé par rapport à la durée du cycle. 
        begin_on permet de savoir si on commence le cycle allumé. 
        '''
        self.__left_blinker.turn_off()
        self.__right_blinker.turn_off()
        reciprocal_begin_on = not begin_on
        if side == SideBlinker.Side.LEFT:
            self.__left_blinker.blink1(cycle_duration, percent_on, begin_on)
        elif side == SideBlinker.Side.RIGHT:
            self.__right_blinker.blink1(cycle_duration, percent_on, begin_on)
        elif side == SideBlinker.Side.BOTH:
            self.__right_blinker.blink1(cycle_duration, percent_on, begin_on)
            self.__left_blinker.blink1(cycle_duration, percent_on, begin_on)
        elif side == SideBlinker.Side.LEFT_RECIPROCAL:
            self.__right_blinker.blink1(cycle_duration, percent_on, begin_on = reciprocal_begin_on)
            self.__left_blinker.blink1(cycle_duration, percent_on, begin_on)
        elif side == SideBlinker.Side.RIGHT_RECIPROCAL:
            self.__right_blinker.blink1(cycle_duration, percent_on, begin_on)
            self.__left_blinker.blink1(cycle_duration, percent_on, begin_on = reciprocal_begin_on)
    
    def blink2(self, side: Side, total_duration: float, cycle_duration: float = 1.0, percent_on: float = 0.5, begin_on: bool = True, end_off: bool = True):
        '''
        side détermine quel côté clignotera. 
        total_duration détermine une durée de clignotement. 
        cycle_duration permet de faire clignoter un nombre de fois selon la durée. 
        percent_on permet de spécifier le temps allumé par rapport à la durée du cycle. 
        begin_on permet de savoir si on commence le cycle allumé. 
        end_off permet de savoir si on termine le cycle fermé.
        '''
        self.__left_blinker.turn_off()
        self.__right_blinker.turn_off()
        reciprocal_begin_on = not begin_on
        reciprocal_end_off = not end_off
        if side == SideBlinker.Side.LEFT:
            self.__left_blinker.blink2(total_duration, cycle_duration, percent_on, begin_on, end_off)
        elif side == SideBlinker.Side.RIGHT:
            self.__right_blinker.blink2(total_duration, cycle_duration, percent_on, begin_on, end_off)
        elif side == SideBlinker.Side.BOTH:
            self.__right_blinker.blink2(total_duration, cycle_duration, percent_on, begin_on, end_off)
            self.__left_blinker.blink2(total_duration, cycle_duration, percent_on, begin_on, end_off)
        elif side == SideBlinker.Side.LEFT_RECIPROCAL:
            self.__right_blinker.blink2(total_duration, cycle_duration, percent_on, begin_on = reciprocal_begin_on, end_off = reciprocal_end_off)
            self.__left_blinker.blink2(total_duration, cycle_duration, percent_on, begin_on, end_off)
        elif side == SideBlinker.Side.RIGHT_RECIPROCAL:
            self.__right_blinker.blink2(total_duration, cycle_duration, percent_on, begin_on, end_off)
            self.__left_blinker.blink2(total_duration, cycle_duration, percent_on, begin_on = reciprocal_begin_on, end_off = reciprocal_end_off)
            
    def blink3(self, side: Side, total_duration: float, n_cycles: int, percent_on: float = 0.5, begin_on: bool = True, end_off: bool = True):
        '''
        side détermine quel côté clignotera. 
        total_duration détermine une durée de clignotement. 
        n_cycles permet de faire clignoter un nombre de fois selon la durée. 
        percent_on permet de spécifier le temps allumé par rapport à la durée du cycle. 
        begin_on permet de savoir si on commence le cycle allumé. 
        end_off permet de savoir si on termine le cycle fermé. 
        '''
        self.__left_blinker.turn_off()
        self.__right_blinker.turn_off()
        reciprocal_begin_on = not begin_on
        reciprocal_end_off = not end_off
        if side == SideBlinker.Side.LEFT:
            self.__left_blinker.blink3(total_duration, n_cycles, percent_on, begin_on, end_off)
        elif side == SideBlinker.Side.RIGHT:
            self.__right_blinker.blink3(total_duration, n_cycles, percent_on, begin_on, end_off)
        elif side == SideBlinker.Side.BOTH:
            self.__right_blinker.blink3(total_duration, n_cycles, percent_on, begin_on, end_off)
            self.__left_blinker.blink3(total_duration, n_cycles, percent_on, begin_on, end_off)
        elif side == SideBlinker.Side.LEFT_RECIPROCAL:
            self.__right_blinker.blink3(total_duration, n_cycles, begin_on = reciprocal_begin_on, end_off = reciprocal_end_off)
            self.__left_blinker.blink3(total_duration, n_cycles, percent_on, begin_on, end_off)
        elif side == SideBlinker.Side.RIGHT_RECIPROCAL:
            self.__right_blinker.blink3(total_duration, n_cycles, percent_on, begin_on, end_off)
            self.__left_blinker.blink3(total_duration, n_cycles, begin_on = reciprocal_begin_on, end_off = reciprocal_end_off)
            
    def blink4(self, side: Side, n_cycles: int, cycle_duration: float = 1.0, percent_on: float = 0.5, begin_on: bool = True, end_off: bool = True):
        '''
        side détermine quel côté clignotera. 
        n_cycles permet de faire clignoter un nombre de fois selon la durée. 
        cycle_duration permet de faire clignoter un nombre de fois selon la durée. 
        percent_on permet de spécifier le temps allumé par rapport à la durée du cycle. 
        begin_on permet de savoir si on commence le cycle allumé. 
        end_off permet de savoir si on termine le cycle fermé. 
        '''
        self.__left_blinker.turn_off()
        self.__right_blinker.turn_off()
        if side == SideBlinker.Side.LEFT:
            self.__left_blinker.blink4(n_cycles, cycle_duration, percent_on, begin_on, end_off)
        elif side == SideBlinker.Side.RIGHT:
            self.__right_blinker.blink4(n_cycles, cycle_duration, percent_on, begin_on, end_off)
        elif side == SideBlinker.Side.BOTH:
            self.__right_blinker.blink4(n_cycles, cycle_duration, percent_on, begin_on, end_off)
            self.__left_blinker.blink4(n_cycles, cycle_duration, percent_on, begin_on, end_off)
        elif side == SideBlinker.Side.LEFT_RECIPROCAL:
            self.__right_blinker.blink4(n_cycles, cycle_duration, percent_on, begin_on = False, end_off = False)
            self.__left_blinker.blink4(n_cycles, cycle_duration, percent_on, begin_on, end_off)
        elif side == SideBlinker.Side.RIGHT_RECIPROCAL:
            self.__right_blinker.blink4(n_cycles, cycle_duration, percent_on, begin_on, end_off)
            self.__left_blinker.blink4(n_cycles, cycle_duration, percent_on, begin_on = False, end_off = False)

    def track(self):
        self.__right_blinker.track()
        self.__left_blinker.track()
