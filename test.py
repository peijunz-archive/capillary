from capillary import edge, fitting
from numpy import array, empty, save, savetxt
a=empty([73, 4])
for i in range(73):
    print(i)
    pts=edge.get(i+1)
    a[i]=fitting.position(pts)
save('dynamics.npy', a)
savetxt('dynamics.txt', a)
