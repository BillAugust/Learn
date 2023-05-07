import matplotlib.pyplot as plt
import numpy as np
import math
from sys import getsizeof
fig,ax = plt.subplots()
#ax.plot([1, 2, 3, 4],[1, 4, 2, 3])
#plt.show())
l = list()
m = list()
n = 0
while n <= 100:
    
    if(n == 30 or n == 90):
        l.append(17)
    else:
        l.append(2.0 * math.sqrt(n))
    m.append(n)
    n += 5
    
#x = np.arange(0,100,5)
#y = 2.0 * np.sqrt(x)

y = np.array(l)
x = np.array(m)
print(getsizeof(x), getsizeof(y))

ax.plot(x,y)
plt.show()




