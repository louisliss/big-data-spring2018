x = range(10)

for i in x:
    if ((i*2) > 5) :
        break
    print(i)

my_list = ['This','is','Python']
for i in my_list:
    print(i)
    print(my_list.index(i))

x = 0
for i in range(100):
    x = x + i
print(x)

def forsum(x,y):
    for i in range(y):
        x =+ i
    return x

forsum(0,100)

#VECTORIZATION

import numpy as np

a = [1,2,3,4,5]
b = [6,7,8,9,10]
c = []

for i,j in zip(a, b):
    c.append(i + j)
print(c)
