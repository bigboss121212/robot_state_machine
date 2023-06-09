from time import perf_counter

# Action
def do_action(is_on, text_on, text_off):
    print(f'\r{text_on if is_on else text_off}', end='')

# Flashing
def flashing(text_on, text_off, cycle_duration, total_duration):
    # contrôle du temps écoulé
    cur_time = perf_counter()
    prev_time = cur_time
    elapsed_time = 0.0

    # contrôle d'état
    total_time = 0      # accumulateur du temps total
    cycle_time = 0      # accumulateur du temps de cycle
    is_on = True        # état courant

    # boucle principale
    while total_time < total_duration:
        # contrôle du temps écoulé
        cur_time = perf_counter()
        elapsed_time = cur_time - prev_time
        prev_time = cur_time
        
        # maj des accumulateurs
        total_time += elapsed_time
        cycle_time += elapsed_time
        
        # contrôle du cycle de la bascule
        if cycle_time >= cycle_duration / 2:        # condition de la bascule
            cycle_time -= cycle_duration / 2        # reset accumulateur du cycle
            is_on = not is_on                       # bascule de l'état
            do_action(is_on, text_on, text_off)     # <<< action!

    print('')



# Main
def main():
    flashing('*****', '     ', 0.5, 3.0)

# execution
if __name__ == '__main__':
    main()