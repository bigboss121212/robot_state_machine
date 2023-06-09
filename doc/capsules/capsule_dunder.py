# dunder functions

# __new__
# __init__
# __bool__
# __str__
# __repr__
# __call__
# __enter__     concept raii
# __exit__      concept raii  
# __len__
# __doc__
# __lt__        less than
# __eq__        equal
# __neq__       not-equal
# (...)


# fonction qui sont appellées par le langage lors de certains 
# traitements. Permettent de tirer de la puissance du langage
# sans allourdir la syntaxe. Mécanisme d'automatisation implémentées 
# par le langage

class A():
    ''' Ceci est pour la classe '''
    
    def __init__(self, long, larg):
        ''' Ceci est un A'''
        self.long = long
        self.larg = larg
        
    def __str__(self):
        return 'Allo'
    
    def __repr__(self):
        return 'Allo repr'
        
a1 = A(3, 5)
a2 = A(6, 7)

print(str(a1))
print(repr(a1))
print(A.__init__.__doc__)
print(a1.__doc__)
# help(A)
# help(A.__init__)