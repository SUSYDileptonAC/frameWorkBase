class A:
    fun = True
    def __getitem__(self, key):
        return getattr(self, "for"+key)
    
class A1:
    x = 1
    
class A2: 
    x = 2
    
setattr(A, "for1", A1)
setattr(A, "for2", A2)

a = A()

print a.for1.x
print a["2"].x
