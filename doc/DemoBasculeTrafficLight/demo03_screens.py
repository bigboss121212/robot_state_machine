import msvcrt

def main():
    
    proceed = True
    while proceed:
        if msvcrt.kbhit():
            input_char = msvcrt.getch().lower().decode('UTF-8')
            
            if input_char == 'q':
                proceed = False
            elif input_char in inputs:
                next_state = input_char
            
            else: 
                print(input_char, end = ' ')
                
    print('\nEND')
    
    