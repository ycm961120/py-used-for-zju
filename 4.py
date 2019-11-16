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
          epochs=200,batch_size=2,verbose=0)

del train_data
del train_targets

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
        
    
    
    
    
    
    
  