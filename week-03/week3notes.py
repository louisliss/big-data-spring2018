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

##PANDAS Workshop

import pandas as pd
import numpy as np

df = pd.DataFrame()
print(df)

df['name'] = ['Joey', 'Jeremy', 'Jenny']

df.assign(age = [28, 37, 27])

import os
os.chdir('week-03')

df = pd.read_csv('data/skyhook_2017-07.csv', sep=',')

df.head()
df.shape
df.columns
df['cat_name'].unique()
df.cat_name
#we're only intrested in hour 158
onefiveeight = df[df['hour'] == 158]
onefiveeight.shape
#we're only interested in rows with more than 50 GPS pings during hour 158
ofesubset = df[(df['hour'] == 158) & (df['count'] > 50)]

bastille = df[df['date'] == '2017-07-14']
bastille.head()

#greater than average cells--creating a mask
bastille_lovers = bastille[bastille['count'] > bastille['count'].mean()]
bastille_lovers['count'].describe()

import matplotlib
%matplotlib inline

df.groupby('date')['count'].describe()
df['hour'].unique()
jul_second = df[df['date'] == '2017-07-02']
jul_second.groupby('hour')['count'].sum().plot()

df['date_new'] = pd.to_datetime(df['date'],format='%Y-%m-%d')
df['date_new'].unique()

df[df['date_new'] == '2017-07-02']['weekday']

df['weekday'] = df['date_new'].apply(lambda x: x.weekday()+1)
df['weekday'].replace(7, 0, inplace = True)


'''for i in range(0, 168, 24):
    j = range()
    df.drop(df[df['weekday'] == (i/24) &
    (
    (df['hour'] < j | df ['hour'] > j + 18)
    )
    ])''' 
