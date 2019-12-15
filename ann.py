from keras import models
from keras import layers
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from keras import regularizers
#数据准备
train_data = pd.read_csv(r'C:\test\2010pop.csv',usecols=['slope','poi','dem','ndvi','dmsp'])
train_targets = pd.read_csv(r'C:\test\2010pop.csv',usecols=['log_pop'])
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
    model.add(layers.Dropout(0.3))
    model.add(layers.Dense(4,activation='relu'))
    model.add(layers.Dense(2,activation='relu'))
    model.add(layers.Dense(1))
    model.compile(optimizer='rmsprop',
                  loss='mse',
                  metrics=['mae'])
    return model
#10折交叉验证
k = 10
num_val_samples = len(train_data) // k
num_epochs = 200
all_mae_histories = []

for i in range(k):
    print('processing fold #',i)
    val_data = train_data[i*num_val_samples:(i+1)*num_val_samples]
    val_targets = train_targets[i*num_val_samples:(i+1)*num_val_samples]

    partial_train_data = np.concatenate([train_data[:i*num_val_samples],train_data[(i+1)*num_val_samples:]],axis=0)
    partial_train_targets = np.concatenate([train_targets[:i*num_val_samples],train_targets[(i+1)*num_val_samples:]],axis=0)

    model = build_model()
    history = model.fit(partial_train_data,partial_train_targets,
                        validation_data=(val_data,val_targets),
                        epochs=num_epochs,batch_size=2,verbose=0)
    mae_history = history.history['val_mean_absolute_error']
    all_mae_histories.append(mae_history)


#绘制验证分数，查找适合的epochs
average_mae_history = [np.mean([x[i] for x in all_mae_histories]) for i in range(num_epochs)]

def smooth_curve(points,factor=0.9):
    smoothed_points = []
    for point in points:
        if smoothed_points:
            previous = smoothed_points[-1]
            smoothed_points.append(previous*factor+point*(1-factor))
        else:
            smoothed_points.append(point)
    return smoothed_points

smooth_mae_history = smooth_curve(average_mae_history)
plt.plot(range(1,len(smooth_mae_history)+1),smooth_mae_history)
plt.xlabel('Epochs')
plt.ylabel('Validation MAE')
plt.show()



#layer1 = 64, layer2 = 64, num_epochs = 250,  batch_size=4:   Validation MAE = 0.261,  epochs = 150?

#layer1 = 64, layer2 = 64, num_epochs = 350,  batch_size=2:   Validation MAE = 0.261 ,  epochs = 100

#layer1 = 32, layer2 = 32, num_epochs = 500,  batch_size=2:   Validation MAE =  0.26,  epochs = 150

#layer1 = 32, layer2 = 32, 加了dropout num_epochs = 500,  batch_size=2:   Validation MAE =  0.32,  epochs = 150

#layer1 = 16, layer2 = 16, num_epochs = 300,  batch_size=2:   Validation MAE =  0.26,  epochs = 110

#layer1 = 16, layer2 = 16, layer3 = 16, num_epochs = 600,  batch_size=2:   Validation MAE =  0.257,  epochs = 230

#layer1 = 8, layer2 = 8, num_epochs = 500,  batch_size=2:   Validation MAE =  0.26,  epochs = 240
