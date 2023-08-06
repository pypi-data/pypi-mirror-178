from constants import *
import nbt

def join(name, *args):
    """Joins the command name and all its arguments"""
    lst = []
    for i in args:
        if i!=None: lst.append(str(i))
    return name+' '+ ' '.join(lst)

def dumps_state(kw:dict):
    def val(v):
        if isinstance(v, bool): return str(v).lower()
        else: return str(v)
    props ='['
    i=0
    for k in kw:
        v = kw.get(k)
        props+=str(k)+'='+val(v)
        if i < len(kw)-1: props+=','
        i+=1
    return props+']'

class rel(int):
    def __init__(self, x):
        """A realitive number `~x`"""
        self.__x = x

    def __new__(self, x):
        self.__x = float(str(x).replace('~', ''))
        return self.__x

    def __str__(self):
        print('reper')
        return '~' + str(self.__x)
    
class summon():
    def __init__(self, entity:str, x:float=0, y:float=0, z:float=0, nbt:dict=None):
        self.entity = entity
        self.x = x
        self.y = y
        self.z = z
        self.nbt = nbt
    
    def __str__(self): return join('summon', self.entity, self.x, self.y, self.z, nbt.dumps(self.nbt))

    def __dict__(self):
        data = {
            'entity': self.entity,
            'x': self.x,
            'y': self.y,
            'z': self.z,
            'nbt': self.nbt
        }
        return data

    def __add__(self, x):
        if isinstance(x, self.__class__):
            n = []
            i=0
            for c1 in self.cords():
                c2 = x.cords()[i]
                n.append(c1 + c2)
                i+=1
            self.cords(*n)
        return self
    
    def __sub__(self, x):
        if isinstance(x, self.__class__):
            n = []
            i=0
            for c1 in self.cords():
                c2 = x.cords()[i]
                n.append(c1 - c2)
                i+=1
            self.cords(*n)
        return self
    
    def __mul__(self, x):
        if isinstance(x, self.__class__):
            n = []
            i=0
            for c1 in self.cords():
                c2 = x.cords()[i]
                n.append(c1 * c2)
                i+=1
            self.cords(*n)
        return self

    def cords(self, x:float=None, y:float=None, z:float=None):
        if x!=None: self.x = x
        if y!=None: self.y = y
        if z!=None: self.z = z
        return self.x, self.y, self.z

    def to_give(self):
        """Converts this command to `give`"""
        return give('minecraft:ghast_spawn_egg', nbt={'EntityTag': {'id': self.entity, **self.nbt}})

class setblock():
    def __init__(self, x, y, z, block:str, state:dict=None, nbt:dict=None):
        self.x = x
        self.y = y
        self.z = z
        self.block = block
        self.state = state
        self.nbt = nbt

    def __str__(self):
        _nbt = ''
        _state = ''
        if self.nbt!=None: _nbt = nbt.dumps(self.nbt)
        if self.state!=None: _state = self.state
        return join('setblock', self.x, self.y, self.z, self.block + _state + _nbt)

    def __dict__(self):
        data = {
            'x': self.x,
            'y': self.y,
            'z': self.z,
            'block': self.block,
            'state': self.state,
            'nbt': self.nbt
        }
        return data
    
    def __add__(self, x):
        if isinstance(x, self.__class__):
            n = []
            i=0
            for c1 in self.cords():
                c2 = x.cords()[i]
                n.append(c1 + c2)
                i+=1
            self.cords(*n)
        return self
    
    def __sub__(self, x):
        if isinstance(x, self.__class__):
            n = []
            i=0
            for c1 in self.cords():
                c2 = x.cords()[i]
                n.append(c1 - c2)
                i+=1
            self.cords(*n)
        return self
    
    def __mul__(self, x):
        if isinstance(x, self.__class__):
            n = []
            i=0
            for c1 in self.cords():
                c2 = x.cords()[i]
                n.append(c1 * c2)
                i+=1
            self.cords(*n)
        return self

    def cords(self, x:int=None, y:int=None, z:int=None):
        if x!=None: self.x = x
        if y!=None: self.y = y
        if z!=None: self.z = z
        return self.x, self.y, self.z

    def to_summon(self):
        """Converts this command to a `summon falling_block` command"""
        nbt = {'BlockState': {'Name': self.block}}
        if self.state!=None: nbt['BlockState']['Properties'] = self.state
        return summon('minecraft:falling_block', self.x, self.y, self.z, nbt=nbt)

class fill():
    def __init__(self, x0:int, y0:int, z0:int, x1:int, y1:int, z1:int, block:str, state:dict=None, nbt:dict=None, mode:str=REPLACE, filter:str=None, filter_state:dict=None, filter_nbt:dict=None):
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1
        self.block = block
        self.state=state
        self.nbt = nbt
        self.mode = mode
        self.filter = filter
        self.filter_state = filter_state
        self.filter_nbt = filter_nbt

    def __str__(self):
        _nbt = ''
        state = ''
        if self.nbt!=None: _nbt = nbt.dumps(self.nbt)
        if self.state!=None: state = dumps_state(self.state)
        res = join('fill', self.x0, self.y0, self.z0, self.x1, self.y1, self.z1, self.block+state+_nbt, self.mode)
        if self.mode == REPLACE and self.filter!=None:
            filter_nbt = ''
            filter_state = ''
            if self.filter_nbt!=None: filter_nbt = nbt.dumps(self.filter_nbt)
            if self.filter_state!=None: filter_state = dumps_state(self.state)
            res = res+' '+str(self.filter) + filter_state+filter_nbt
        return res

    def __add__(self, x):
        if isinstance(x, self.__class__):
            n = []
            i=0
            for c1 in self.cords():
                c2 = x.cords()[i]
                n.append(c1 + c2)
                i+=1
            self.cords(*n)
        return self
    
    def __sub__(self, x):
        if isinstance(x, self.__class__):
            n = []
            i=0
            for c1 in self.cords():
                c2 = x.cords()[i]
                n.append(c1 - c2)
                i+=1
            self.cords(*n)
        return self
    
    def __mul__(self, x):
        if isinstance(x, self.__class__):
            n = []
            i=0
            for c1 in self.cords():
                c2 = x.cords()[i]
                n.append(c1 * c2)
                i+=1
            self.cords(*n)
        return self

    def size(self):
        """Returns a tuple that has the size of the volume"""
        x = abs(self.x0 - self.x1) + 1
        y = abs(self.y0 - self.y1) + 1
        z = abs(self.z0 - self.z1) + 1
        return x, y, z
        
    def area(self):
        """Returns with the total area for the volume"""
        x, y, z = self.size()
        return (x * y * z)

    def matrix(self):
        """Returns with all the coords (X, Y, Z) from the volume"""
        matrix = []
        if self.x0 <= self.x1: _x=list(range(self.x0, self.x1+1))
        else: _x=list(range(self.x1, self.x0+1))

        if self.y0 <= self.y1: _y=list(range(self.y0, self.y1+1))
        else: _y=list(range(self.y1, self.y0+1))

        if self.z0 <= self.z1: _z=list(range(self.z0, self.z1+1))
        else: _z=list(range(self.z1, self.z0+1))
        for x in _x:
            for y in _y:
                for z in _z:
                    matrix.append((x, y, z))
        return matrix

    def offset(self, x:int=0, y:int=0, z:int=0):
        """Move the entire volume"""
        if x!=0:
            self.x0 +=x
            self.x1 +=x
        if y!=0:
            self.y0 +=y
            self.y1 +=y
        if z!=0:
            self.z0 +=z
            self.z1 +=z
        return self
    
    def resize(self, x:int=0, y:int=0, z:int=0):
        """Increase (positive) or decrease (negative) the size of the volume"""
        if x!=0:
            if self.x0 >= self.x1: self.x0 +=x
            else: self.x1 +=x
        if y!=0:
            if self.y0 >= self.y1: self.y0 +=y
            else: self.y1 +=y
        if z!=0:
            if self.z0 >= self.z1: self.z0 +=z
            else: self.z1 +=z
        return self
    
    def to_setblock(self):
        """Converts this command into multiple `setblock` commands"""
        cmds = []
        for x, y, z in self.matrix(): cmds.append(setblock(x, y, z, self.block))
        return cmds

    def to_summon(self):
        """Converts this command to `summon falling_block`"""
        cmds = []
        for blk in self.to_setblock(): cmds.append(blk.to_summon())
        return cmds
    
    def verticies(self):
        """Returns with the 4 corners of the volume."""
        return [
                (self.x0, self.y0, self.z0),
                (self.x1, self.y1, self.z1),
                (self.x0, self.y0, self.z1),
                (self.x1, self.y0, self.z0),
                (self.x1, self.y0, self.z1),
                (self.x1, self.y1, self.z0),
                (self.x0, self.y1, self.z1),
                (self.x0, self.y1, self.z0)
            ]

    def validate(self):
        """Checks if this command contains any errors."""
        if self.area() > int(32768): return False
        return True

    def split(self):
        """Splts this fill command into multiple diffrent fill commands so it does not exced the max area limit (32768)"""        
        if self.validate()==False:
            cmds = []
            print('max')
            _x = 0
            _y = 0
            _z = 0
            _last = None
            state='from'
            for x, y, z in self.matrix():
                if state=='from':
                    _x = x
                    _y = y
                    _z = z
                    state='to'

                elif state=='to':
                    f = fill(_x, _y, _z, x, y, z, self.block)
                    if f.validate()==False:
                        _x = 0
                        _y = 0
                        _z = 0
                        cmds.append(_last)
                        state='from'
                        _last = None

                    else: _last = f

            if _last!=None: cmds.append(_last)
            return cmds
        else: return [self]

    def cords(self, x0:int=None, y0:int=None, z0:int=None, x1:int=None, y1:int=None, z1:int=None):
        if x0!=None: self.x0 = x0
        if y0!=None: self.y0 = y0
        if z0!=None: self.z0 = z0
        if x1!=None: self.x1 = x1
        if y1!=None: self.y1 = y1
        if z1!=None: self.z1 = z1
        return self.x0, self.y0, self.z0, self.x1, self.y1, self.z1

class give():
    def __init__(self, item:str, count:int=None, target:str='@s', nbt:dict=None):
        self.item = item
        self.target = target
        self.nbt = nbt
        self.count = count

    def __str__(self):
        _nbt = ''
        if self.nbt!=None: _nbt = nbt.dumps(self.nbt)
        return join('give', self.target, self.item+_nbt, self.count)

if __name__ == '__main__':
    # f = fill(0,0,0, 31,31,31, 'stone')
    f = fill(0,0,0, 31,31,32, 'stone')

    for c in f.split():
        print(c)
