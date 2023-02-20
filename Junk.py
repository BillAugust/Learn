class whatever:
    foo = 0

    def _init_(self):
        pass
    def getOne(self):
        foo = 1
        return foo
    def setFoo(self, garbage):
        whatever.foo = garbage
    def getFoo(self):
        return whatever.foo
b = whatever()
x = b.getOne()
b.setFoo(2)
y = b.getFoo()
print(x, y)

