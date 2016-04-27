
import UserDict
import json
import pprint as pp


# Everything here is a dictionary ... i think it might make things easier
# Bob() -> dict -> json -> ZeroMQ ->de-json -> dict

# class Bob(UserDict.UserDict):
class Bob(dict):
    # __slots__ = ['x','y','z']
    # def __init__(self, data = {}, **kw):
    def __init__(self,**kw):
        # UserDict.UserDict.__init__(self)
        dict.__init__(self)
        # if True:
        default = {'x':0.0, 'y':0.0, 'z':0.0}
        self.update(default)
        if kw: self.update(kw)
        # self.update(m='5')
        # print 'data',data
        # print 'kw',kw
        # self.update(x=1)
        # self.update(y=2)
        # self.update(z=3)

class Tom(dict):
    def __init__(self):
        # self.x = 1
        # self.lin = Bob(x=500.0, z=-234.1)
        # self.ang = Bob()
        self.update(x=1)
        self.update(lin=Bob(x=500.0, z=-234.1))
        self.update(ang=Bob())

t = Tom()

# d = vars(t)
print t['x']

# pp.pprint(d)
print 'lin.x',t['lin']['x']

t['lin']['x']=5
print 'new lin.x',t['lin']['x']

# print 'serialize',t.serialize()
pp.pprint( json.dumps(t, default=lambda o: vars(o)) )
