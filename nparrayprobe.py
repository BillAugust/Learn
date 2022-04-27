import numpy as np
corTable = np.array([[5,0],[20,1],[50,2],[100,3],[320,101]],np.int32)
def correct(offset):
    absOff = abs(offset)
    sign = 1
    if absOff > offset:
        sign = -1
    ret = 101
    for i in range(len(corTable)):
        if (absOff <= corTable[i,0]):
            ret = corTable[i,1]
            break
    return sign * ret

print("wtf")
foo = np.array([[1,2],[6,7],[3,4]],np.int32)
print(foo[2,1])
print(correct(3)," ",correct(20)," ",correct(33)," ",
      correct(500)," ",correct(5)," ",correct(99)," ")
