# en python la surcharge de fonction n'existe pas
# 2 approches
#   - avec des décorateurs (limité à un seul argument en python, très limité)
#     il existe des librairies qui offrent plus sinon écrire notre propre décorateur
#     mais c'est très laborieux 
#   - approche plus simple

# blink(a, b, c)
# blink(a, b, d=1)
# blink(a, d, e)

# mettre tout ce qui est réccurent en premier et ce qui ne l'est pas sera passé
# comme un dictionnaire avec kwargs

def blink(self, a, **kwargs):
    if kwargs.keys() == set('b', 'c'):
        ... # type checking et configuration
    elif kwargs.keys() == set('b'):  # d=1 (pas eu besoin de la passer)
        ...
    elif kwargs.keys() == set('b', 'd'):
        ...
    elif kwargs.keys() == set('d', 'e'):
        ...
    else:
        raise Exception('Erreur dans les paramêtres passées')
    
    # ici le code sera appelé