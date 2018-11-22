from ctypes import *

res = cdll.LoadLibrary("C:\\Users\\xieji\\CLionProjects\\untitled\\main.dll")
a = (c_int * 36)()
a[2*6+2]=1
a[2*6+3]=-1
a[3*6+2]=-1
a[3*6+3]=1
res.make_move(a, 1)
for i in range(6):
    for j in range(6):
        print(a[i*6+j],' ',end='')
    print()