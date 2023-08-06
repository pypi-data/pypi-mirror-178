
__single_quote__ = [
    'CustomName',
    'Name',
    'Lore'
]

class NBTEncoder():
    def __init__(self, separators=(',', ':')):
        self.separators = separators
    
    def _byte(self, value: int):
        """byte (8-bit int -128 to 127) <num>b"""
        return str(value)+'b'
    
    def _short(self, value: int):
        """short (16-bit int -32768 to 32767) <num>s"""
        return str(value)+'s'
    
    def _integer(self, value: int):
        """int (32-bit int -2147483648 to 2147483647)"""
        return str(value)
    
    def _long(self, value: int):
        """long (64-bit int -9223372036854775808 to 9223372036854775807) <num>l"""
        return str(value)+'l'
    
    def _float(self, value: float):
        """float (32 single-pres -3.4e+38 to 3.4e+38) <num>f"""
        return str(value)+'f'
    
    def _double(self, value: float):
        """double (64-bit double-pres -1.7e+308 to 1.7e+308) <num>d"""
        return str(value)+'d'
    
    def _boolean(self, value: bool):
        """boolean (can be true, false, 1b, 0b)"""
        if value==True: return self._byte(1)
        elif value==False: return self._byte(0)
        else: return 'null'
    
    def _string(self, value: str, key:str=None):
        """string (sequence of chars)"""
        if key!=None:
            for i in __single_quote__:
                if i == key: return "'%s'"%value.replace("'", "\\'")
        return '"%s"'%value.replace('"', '\\"')
    
    def _list(self, value: list, key:str=None):
        """list (ordered list of tags)"""
        s = '['
        i=0
        for _s in value:
            if i<len(value)-1: s+=self.encode(_s, key) + self.separators[0]
            else: s+=self.encode(_s, key)
            i+=1
        return s+']'
    
    def _compound(self, value: dict):
        """compound (ordered list of att pairs)"""
        s = '{'
        i=0
        for k in value:
            v = value.get(k)
            _s = k + self.separators[1] + self.encode(v, k)
            if i < len(value)-1: s+=_s + self.separators[0]
            else: s+=_s
            i+=1
        return s+'}'
    
    def _byte_array(self, value: list):
        """byte array (ordered list of 8bit int) [B; 1b, 2b, 3b]"""
        s = '[B;'
        i=0
        for _s in value:
            if i<len(value)-1: s+=self._byte(_s) + self.separators[0]
            else: s+=self._byte(_s)
            i+=1
        return s+']'
    
    def _integer_array(self, value: list):
        """int array (orderd list of 32-bit int) [I; 1,2,3]"""
        s = '[I;'
        i=0
        for _s in value:
            if i<len(value)-1: s+=self._integer(_s) + self.separators[0]
            else: s+=self._integer(_s)
            i+=1
        return s+']'
    
    def _long_array(self, value: list):
        """long array (ordered list of 64 bit int) [L; 1l, 2l, 3l]"""
        s = '[L;'
        i=0
        for _s in value:
            if i<len(value)-1: s+=self._long(_s) + self.separators[0]
            else: s+=self._long(_s)
            i+=1
        return s+']'

    def encode(self, value, key=None):
        if value==None: return ''
        elif isinstance(value, dict): return self._compound(value)
        elif isinstance(value, bool): return self._boolean(value)
        elif isinstance(value, int):
            if value in range(-128, 128): return self._byte(value)
            elif value in range(-32768, 32768): return self._short(value)
            elif value in range(-2147483648, 2147483648): return self._integer(value)
            elif value in range(-9223372036854775808, 9223372036854775808): return self._long(value)
            else: raise ValueError(value)

        elif isinstance(value, float): # TODO
            # if value in range(-3.4e+38, 3.4e+38): return self._float(value)
            # elif value in range(-1.7e308, 1.7e+308): return self._double(value)
            return self._float(value)

        elif isinstance(value, str): return self._string(value, key)
        elif isinstance(value, list): return self._list(value, key)
        else: raise TypeError(f'Object of type {value.__class__.__name__} is not NBT serializable')
        
def loads(s: str):
    return 'worked'

def dumps(obj: dict, separators=(', ', ': ')):
    """nbt -> string"""
    return NBTEncoder(separators).encode(value=obj)

if __name__ == '__main__':
    import json
    obj = {
            'object': {
                'string': "hello world",
                'byte': 127,
                'short': 32767,
                'integer': 2147483647,
                'long': 9223372036854775807,
                'float': 3.4,
                'double': 1.7,
                'boolean': True
            },
            'array': [
                'item 1',
                'item 2',
                'item 3'
            ],
        }
    d = json.dumps(obj)
    l = json.loads(d)
    print(l, d)

    d = dumps(obj)
    l = loads(d)
    print(l, d)