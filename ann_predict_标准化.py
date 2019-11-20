from keras import models
from keras import layers
import numpy as np
import pandas as pd
import cv2
from osgeo import gdal_array
#数据准备
train_data = pd.read_csv(r'd:\2010pop.csv',usecols=['slope','poi','dem','ndvi','dmsp'])
train_targets = pd.read_csv(r'd:\2010pop.csv',usecols=['log_pop'])
train_data = np.array(train_data)
train_targets = np.array(train_targets)

#标准化
mean = train_data.mean(axis=0)
std = train_data.std(axis=0)
train_data -= mean
train_data /= std



#生成模型
def build_model():
    model = models.Sequential()
    model.add(layers.Dense(8,activation='relu',input_shape=(train_data.shape[1],)))
    model.add(layers.Dense(8,activation='relu'))
    model.add(layers.Dense(1))
    model.compile(optimizer='rmsprop',
                  loss='mse',
                  metrics=['mae'])
    return model

#训练模型
model = build_model()
model.fit(train_data,train_targets,
          epochs=400,batch_size=2,verbose=0)



#变量重要性
#基于MIV的相关变量检测，MIV（mean impact value）平均影响值算法，主要用于检测哪些输入变量与输出相关
#算法很简单，先训练好网络。再将某个输入减少10%和增加10%（其它输入保持不变），将两组数据都输入到网络中，
#查看该输入的落差会引起网络输出多少的落差。若果引起的落差很少，则说明该输入对输出影响很小，
#否则，则认为对输出影响较大。
#MIV被认为是在神经网络中评价变量相关的最好指标之一，其符号代表相关的方向,increase-decrease
result = []
for i in range(train_data.shape[1]):
    inputdata1 = np.copy(train_data)
    inputdata1[:,i] *=  0.9
    inputdata2 = np.copy(train_data)
    inputdata2[:,i] *= 1.1
    pre1 = model.predict(inputdata1)
    pre2 = model.predict(inputdata2)
    result.append((pre2-pre1).mean(axis=0)[0])
print(result)






#标准化输入数据
ls = ['0','1','2','4','5','6','7','10','11','13','14','15','17','18','19']


#求平均值
count1 = 0
count2 = 0
sum_slope = 0.
sum_poi = 0.
sum_dem = 0.
sum_ndvi = 0.
sum_dmsp = 0.

for i in ls:
    print('#########'+i+'#########')
    
    way = 'C:\\test\\test-pre\\poi' + i + '.tif'
    poi = cv2.imread(way, -1)
    poi = poi.reshape(5940 * 4548)
    poi_na = np.where(poi> -3e+38)
    count1 += len(poi_na[0])
    sum_poi += poi[poi_na].sum()
    
    
    way = 'C:\\test\\test-pre\\slope'  + i + '.tif'
    slope = cv2.imread(way,-1)
    slope = slope.reshape(5940*4548)
    slope_na = np.where(slope> -3e+38)
    count2 += len(slope_na[0])
    sum_slope += slope[slope_na].sum()
    
    way = 'C:\\test\\test-pre\\dem' + i + '.tif'
    dem = cv2.imread(way, -1)
    dem = dem.reshape(5940 * 4548)
    sum_dem += dem[slope_na].sum()

    way = 'C:\\test\\test-pre\\ndvi' + i + '.tif'
    ndvi = cv2.imread(way, -1)
    ndvi = ndvi.reshape(5940 * 4548)
    sum_ndvi += ndvi[slope_na].sum()

    way = 'C:\\test\\test-pre\\dmsp' + i + '.tif'
    dmsp = cv2.imread(way, -1)
    dmsp = dmsp.reshape(5940 * 4548)
    sum_dmsp += dmsp[slope_na].sum()
    
    
    mean_poi = sum_poi / count1
    mean_slope = sum_slope / count2
    mean_dem = sum_dem / count2
    mean_ndvi = sum_ndvi / count2
    mean_dmsp = sum_dmsp / count2
    print(mean_poi,mean_slope,mean_dem,mean_ndvi,mean_dmsp)
    

mean_poi = sum_poi / count1
mean_slope = sum_slope / count2
mean_dem = sum_dem / count2
mean_ndvi = sum_ndvi / count2
mean_dmsp = sum_dmsp / count2


    
#求标准差
std_poi = 0.
std_slope = 0.
std_dem = 0.
std_ndvi = 0.
std_dmsp = 0.
for i in ls:
    print('$$$$$$$$$$'+i+'$$$$$$$$$$')
    way = 'C:\\test\\test-pre\\poi' + i + '.tif'
    poi = cv2.imread(way, -1)
    poi = poi.reshape(5940 * 4548)
    poi_na = np.where(poi> -3e+38)
    poi[poi_na] -= mean_poi
    poi[poi_na] = poi[poi_na] * poi[poi_na]
    std_poi += poi[poi_na].sum() / count1

    
    way = 'C:\\test\\test-pre\\slope'  + i + '.tif'
    slope = cv2.imread(way,-1)
    slope = slope.reshape(5940*4548)
    slope_na = np.where(slope> -3e+38)
    slope[slope_na] -= mean_slope
    slope[slope_na] = slope[slope_na] * slope[slope_na]
    std_slope += slope[slope_na].sum() / count2
    
    way = 'C:\\test\\test-pre\\dem' + i + '.tif'
    dem = cv2.imread(way, -1)
    dem = dem.reshape(5940 * 4548)
    dem[slope_na] = dem[slope_na] * dem[slope_na]
    std_dem += dem[slope_na].sum() / count2

    way = 'C:\\test\\test-pre\\ndvi' + i + '.tif'
    ndvi = cv2.imread(way, -1)
    ndvi = ndvi.reshape(5940 * 4548)
    ndvi[slope_na] = ndvi[slope_na] * ndvi[slope_na]
    std_ndvi += ndvi[slope_na].sum() / count2

    way = 'C:\\test\\test-pre\\dmsp' + i + '.tif'
    dmsp = cv2.imread(way, -1)
    dmsp = dmsp.reshape(5940 * 4548)
    dmsp[slope_na] = dmsp[slope_na] * dmsp[slope_na]
    std_dmsp += dmsp[slope_na].sum() / count2
    
    print(std_poi,std_slope,std_dem,std_ndvi,std_dmsp)

std_poi = std_poi ** 0.5
std_slope = std_slope ** 0.5
std_dem = std_dem ** 0.5
std_ndvi = std_ndvi ** 0.5
std_dmsp = std_dmsp ** 0.5
   
    
#a.astype('float64')


#标准化
for i in ls:
    way = 'C:\\test\\test-pre\\slope'  + i + '.tif'
    slope = cv2.imread(way,-1)
    slope = slope.reshape(5940*4548)
    slope_na = np.where(slope<-3e+38)
    slope[slope_na] = mean_slope
    slope -= mean_slope
    slope /= std_slope

    way = 'C:\\test\\test-pre\\poi' + i + '.tif'
    poi = cv2.imread(way, -1)
    poi = poi.reshape(5940 * 4548)
    poi_na = np.where(poi<-3e+38)
    poi[poi_na] = 100000
    poi -= mean_poi
    poi /= std_poi

    way = 'C:\\test\\test-pre\\dem' + i + '.tif'
    dem = cv2.imread(way, -1)
    dem = dem.reshape(5940 * 4548).astype('float64')
    dem -= mean_dem
    dem /= std_dem

    way = 'C:\\test\\test-pre\\ndvi' + i + '.tif'
    ndvi = cv2.imread(way, -1)
    ndvi = ndvi.reshape(5940 * 4548).astype('float64')
    ndvi -= mean_ndvi
    ndvi /= std_ndvi

    way = 'C:\\test\\test-pre\\dmsp' + i + '.tif'
    dmsp = cv2.imread(way, -1)
    dmsp = dmsp.reshape(5940 * 4548).astype('float64')
    dmsp -= mean_dmsp
    dmsp /= std_dmsp

    test = np.vstack((slope,poi,dem,ndvi,dmsp))
    test = test.T
    
    del slope,poi,dem,ndvi,dmsp
    
    pre = model.predict(test)
    pre = pre.reshape(5940,4548)
    
    way = 'C:\\test\\test-pre\\slope'  + i + '.tif'
    arr = gdal_array.LoadFile(way)
    for x in range(5940):
        for y in range(4548):
            arr[x][y] = pre[x][y]
    output = gdal_array.SaveArray(arr, 'C:\\test\\test-pre\\pre'+i+'.tif', format="GTiff",prototype=way)
    output = None
    del pre,arr