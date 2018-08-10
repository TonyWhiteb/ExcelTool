class test(object):
    def __init__(self,test):
        self.test = test
    def SetFuc(self, Func = None):
        self.test2 = Func

test = test(2)
test.SetFuc(4)

if (hasattr(test,'test2')) and (test.test2 != None):
    print(1)
print(test.test)