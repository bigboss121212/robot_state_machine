def function(p1, p2, p3):
    pass

def function1(p1, p2, p3, p4):
    pass

def function2(p1, p2, p3=1, p4=None):
    pass

def function3(position, speed, acceleration, /, color=0, size=12):
    pass

def function4(position, speed, acceleration, /, color=0, *, size=12):
    pass


function2(1, 2, 3)
function2(p1=1, p2=2, p3=3, p4=4)
function2(p1=1, p2=2, p4=4)
function2(1, 2, p4=4)

function3(1, 2, 3, 2)
function3(1, 2, 3, size=2, color=3)

function4(1, 2, 3, size=4)



def function5(*args):
    print(type(args))
    for value in args:
        print(value)  

function5(1, 2, 3, 4, 'SELF')
function5(1)
function5()
var1 = (4, 5, 6)
var2 = (4, 5, 6)
function5(*var1)
function5(*var1, *var2)

def sum(*args):
    s = 0
    for value in args:
        s += value
    return s

sum(2,55,85,45,6,5,4,2,85,4)


def function6(**kwargs):
    print(type(kwargs))
    for key, value in kwargs.items():
        print(key, value)

function6(speed=4, color='black', coolness=0)
myArguments = {
    'speed':4, 'color':'black', 'coolness':0
    }
function6(**myArguments)



def function7(p1, p2, *args, **kwargs):
    pass

function7(1, 2)
function7(1, 2, 4, 5, 6, 76, 3546)
function7(1, 2, allo=45, b64='oui il y a un examen DOUBLE SEUIL')
function7(1, 2, 3, 4 , 5, allo=45, b64='oui il y a un examen DOUBLE SEUIL')
