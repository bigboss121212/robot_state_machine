# ... elipsis 
# même impact que pass, mais avec une nuance, 
# à remettre plus tard ou parce que la fonction 
# est définie ailleurs

def function():
    ...

# p1, p2, p3 sont des paramètres
def function(p1, p2, p3):
    pass


# 1, 2, 3 sont des arguments
function(1, 2, 3)

# il n'y a pas de surcharge en python 
# (sans utilisation d'une librairie tierce
#  ou décorateur) 

def function1(p1, p2, p3, p4):
    pass

def function1(p1, p2, p3=1, p4=None):
    pass

function1(1, 2, 3, 4) # positionel

function1(p1=1, p2=2, p3=3, p4=4) # par mot clé
function1(p1=1, p2=2, p4=4)
function1(1, 2, p4=4)

# les trois premiers parametres sont obligatoirement par position
def function3(position, speed, acceleration, /, color=0, size=12):
    pass

# function3(speed=1, color=2, position=4) # NE FONCTIONNERA PAS

def function4(position, speed, acceleration, /, color=0, *, size=12):
    pass

function4(1, 2, 3, size=3)

def function5(*args):
    for value in args:
        print(value)

function5(1, 2, 3, 4, 5, 'SELF')

var = (4, 5, 6)
function5(*var) # unfolding operator (dans la zone exécutive)
# fonctionnera aussi sur function4


def sum(*args):
    s = 0
    for value in args:
        s += value
    return s

var = tuple(range(40))
print(type(var))
print(sum(1, 2, 4))
print(sum(*var)) ### vérifier

def function6(**kwargs): #key word arguments 
    print(type(kwargs))
    for key, value in kwargs.items():
        print(f'In function 6: {key=}, {value=}')    
    
function6(speed=4)

myArguments = {
    'speed': 4, 'color':'black', 'coolness':0
}

function6(patate=myArguments)
function6(**myArguments)    
    
    
def function7(p1, p2, *args, **kwargs):
    print(f'{p1, p2}')
    print(args)
    print(kwargs)

function7(1, 2)
function7(1, 2, 12, 34, 45, 56, 67, 78)
function7(1, 2, 12, 34, 45, 56, 67, 78)
function7(1, 2, 3, 4, 5, allo=45, b64='oui il y a un DOUBLE SEUIL')
function7(1, 2, allo=45, b64='oui il y a un DOUBLE SEUIL')