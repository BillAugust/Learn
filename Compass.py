from i2clibraries import i2c_hmc5883l
import time
import statistics as stats
hmc5883l =i2c_hmc5883l.i2c_hmc5883l(1)
hmc5883l.setContinuousMode()
hmc5883l.setDeclination(4, 0)
#(x,y,z) = hmc5883l.get_axes()
#print (hmc5883l.getHeading())
sum = 0
num = 10
headings = []
stds = []
for i in range(num):
    (deg, min) = hmc5883l.getHeading()
    toDecimal = int((deg + min/60) * 1000)/1000
    headings.append(toDecimal)
    #print (toDecimal)
    sum += toDecimal
    time.sleep(0.25)
avg = int(sum/num * 1000)/1000
print ("Average: " ,avg)
sdev = stats.stdev(headings)
print("Std: ", sdev)
reject = 0
#print("Deviants:")
for i in range(num):
    deviation = abs(int((headings[i]- avg)*1000)/1000)
    if(deviation > (2 * sdev)):
        #print(deviation, "Deviant")
        reject += 1
    else:
        pass
        #print(deviation)
print("Rejected: ",reject)
        
#    if(abs(headings[] - avg) - std) >  
#pass



      
