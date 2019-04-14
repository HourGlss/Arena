import bitstruct
import sys
def stats(s,i):
    print(s,sys.getsizeof(i),i)


# OUTGOING FROM SERVER
pack_data = 't32u11u11u11u11b1'
"""
u – unsigned integer
s – signed integer
f – floating point number of 16, 32, or 64 bits
b – boolean
t – text (ascii or utf-8)
r – raw, bytes
p – padding with zeros, ignore
P – padding with ones, ignore
"""
data = {'uid':"aabb",'x':1920,'y':1080,'mx':1920,'my':1080,'c':True}
names = [str(e) for e in data.keys()]
packed = bitstruct.pack_dict(pack_data, names, data)
unpacked = bitstruct.unpack_dict(pack_data, names, packed)

stats("raw",data)
stats("packed",packed)
#INCOMING TO SERVER
pack_data = 'u11u11u11u11u10u10f32'
"""
u – unsigned integer
s – signed integer
f – floating point number of 16, 32, or 64 bits
b – boolean
t – text (ascii or utf-8)
r – raw, bytes
p – padding with zeros, ignore
P – padding with ones, ignore
"""
data = {'x': 960, 'y': 540, 'mouse_x': 938, 'mouse_y': 552, 'health': 1000, 'mana': 1000, 'time_made': 1555180007.1687832}
names = [str(e) for e in data.keys()]
packed = bitstruct.pack_dict(pack_data, names, data)
unpacked = bitstruct.unpack_dict(pack_data, names, packed)
stats("raw",data)
stats("packed",packed)


