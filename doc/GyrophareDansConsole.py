import math
import time

def smooth_wave(elapsed_time, min, max, frequency):
    return (math.sin(elapsed_time * math.tau * frequency) * 0.5 + 0.5) * (max - min) + min

def step_wave(elapsed_time, min, max, frequency):
    return round((elapsed_time % frequency) / frequency) * (max - min) + min

def sawtooth_wave(elapsed_time, min, max, frequency):
    return (elapsed_time % frequency) / frequency * (max - min) + min

def blend_color(c1, c2, percent):
    inv_percent = 1.0 - percent
    return tuple(round(c1[i] * percent + c2[i] * inv_percent) for i in range(3))

def alternate_blend(color1, color2, percent):
    blend1 = blend_color(color1, color2, percent)
    blend2 = blend_color(color1, color2, 1.0 - percent)
    return (blend1, blend2)

def color_text(text, color):
    return f'\033[38;2;{color[0]};{color[1]};{color[2]}m{text}\033[0m'


block_char = 'â–ˆ'
block_length = 15
block_text = block_char * block_length
frequency = 2.5 / 1.0
color1 = (255, 255, 0)
color2 = (0, 0, 0)
wave = smooth_wave



while True:
    percent = wave(time.perf_counter(), 0.0, 1.0, frequency)
    # print(percent)
    blend1, blend2 = alternate_blend(color1, color2, percent)
    print(f"\r{color_text(block_text, blend1)}{color_text(block_text, blend2)}", sep = "", end="")




# Exemple bidon sur les 'comprehension list' et les 'generator' (enlever le 'True' dans le 'while')
a = [i**2 for i in range(10) if i % 2 == 0]
print(a, type(a))
a = (i**2 for i in range(10) if i % 2 == 0)
print(a, type(a))


for value in a:
    print(value)
