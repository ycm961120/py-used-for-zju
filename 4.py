import numpy as np
import cv2
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import math





ls = ['0','1','2','4','5','6','7','10','11','13','14','15','17','18','19']
result= []
for i in ls:
    print('------' + i + '--------')
    way = 'C:\\test\\test-pre\\poi' + i + '.tif'
    poi = cv2.imread(way, -1)
    poi[poi<-30000] = -10
    poi = poi.reshape(5940 * 4548)
    poi = poi.tolist()
    t1 = datetime.datetime.now()
    for j in poi:
        if j > -1:
            result.append(j)
    t2 = datetime.datetime.now()
    print(len(result))
    print(t2-t1)
del poi

y = []
for k,num in enumerate(result):
    if k % 1000 == 0:
        y.append(num)
del result


y.sort()


######画后%
x = [i for i in range(130059,131403)]


train_data = pd.read_csv(r'c:\test\2010pop-.csv',usecols=['poi'])
train_data = np.array(train_data)
train_data = train_data.tolist()
train_data.sort()
L2 = len(train_data)
x2 = [131403-(978-i)*131403/978 for i in range(int(L2*0.99),979)]
plt.plot(x2,train_data[-11:])


plt.scatter(x,y[130059:])
plt.show()



######画前%
x = [i for i in range(78600)]


train_data = pd.read_csv(r'c:\test\2010pop-.csv',usecols=['poi'])
train_data = np.array(train_data)
train_data = train_data.tolist()
train_data.sort()
L2 = len(train_data)
x2 = [i*131403/978 for i in range(int(L2*0.6))]
plt.plot(x2,train_data[:586])


plt.scatter(x,y[:78600])
plt.show()


