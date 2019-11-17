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
          epochs=300,batch_size=2,verbose=0)



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
for i in ls:
    way = 'C:\\test\\test-pre\\slope'  + i + '.tif'
    slope = cv2.imread(way,-1)
    slope_na = pd.isnull(slope)
    slope[slope_na] = 0
    slope = slope.reshape(5940*4548)

    way = 'C:\\test\\test-pre\\poi' + i + '.tif'
    poi = cv2.imread(way, -1)
    poi_na = pd.isnull(poi)
    poi[poi_na] = 0
    poi = poi.reshape(5940 * 4548)

    way = 'C:\\test\\test-pre\\dem' + i + '.tif'
    dem = cv2.imread(way, -1)
    dem_na = pd.isnull(dem)
    dem[dem_na] = 0
    dem = dem.reshape(5940 * 4548)

    way = 'C:\\test\\test-pre\\ndvi' + i + '.tif'
    ndvi = cv2.imread(way, -1)
    ndvi_na = pd.isnull(ndvi)
    ndvi[ndvi_na] = 0
    ndvi = ndvi.reshape(5940 * 4548)

    way = 'C:\\test\\test-pre\\dmsp' + i + '.tif'
    dmsp = cv2.imread(way, -1)
    dmsp_na = pd.isnull(dmsp)
    dmsp[dmsp_na] = 0
    dmsp = dmsp.reshape(5940 * 4548)

    test = np.vstack((slope,poi,dem,ndvi,dmsp))
    test = test.T
    test -= mean
    #for x in range(27015120):
    #    for y in range(5):
    #        if test[x][y] < -1000000:
    #            test[x][y] = 0
    test /= std
    del slope, poi, dem, ndvi, dmsp

    pre = model.predict(test)
    pre = pre.reshape(5940,4548)
    way = 'C:\\test\\test-pre\\slope'  + i + '.tif'
    arr = gdal_array.LoadFile(way)
    for x in range(5940):
        for y in range(4548):
            arr[x][y] = pre[x][y]
    output = gdal_array.SaveArray(arr, 'C:\\test\\test-pre\\pre'+'sb'+'.tif', format="GTiff",prototype=way)
    output = None
    del pre,arr
        
    
    
    
    
    
    
  
