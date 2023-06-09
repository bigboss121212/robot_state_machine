class Test():
    def __init__(self, att1, att2):
        self.att1 = att1;
        self.att2 = att2;
    
    def __repr__(self):
        return f"Test({self.att1}, {self.att2})"
    
    def __str__(self):
        return f"Test object with attributes: att1={self.att1}, att2={self.att2}"
            
        
test = Test(1, 2)

print(test)
print(repr(test))
new_test = eval(repr(test))
print(new_test)
print(new_test.att1)
print(new_test.att2)