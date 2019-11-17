import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

#x轴数据
x = [55, 45, 75, 35]
#y轴变量名称
y = ['a','b','c','d']
#字体
family = 'arial'
#x名字
xlabel = 'gdp3'
#题目
title = 'VarImp(%)'
#保存路径
way = r'C:\Users\Yao\Desktop\3.jpg'




#----------------封装---------------------#
#对数据进行排序
d = dict(zip(y,x))
d = sorted(d.items(),key=lambda x:x[1],reverse=False)
x = []
ylabel = []
for i in d:
    x.append(i[1])
    ylabel.append(i[0])
print(x)
print(ylabel)
#画布大小
plt.figure(figsize=(4,5))
#画平行于x的虚线
y = [i for i in range(1,len(x)+1)]
for i in y:
    x1 = np.arange(x[0]-3,x[-1]+3,0.1)
    y1 = np.array(0*x1)+i
    plt.plot(x1,y1,'k--',linewidth=0.5)
mpl.rcParams['font.sans-serif'] = [family]
#画散点
for a,b in zip(y,x):
    plt.text(b-0.003,a+0.1,'%.4f' % b)#添加数值标签
plt.ylim(0,len(x)+1)
plt.xlim(x[0]-3,x[-1]+3)
plt.xlabel(xlabel)
plt.yticks(y,ylabel)
plt.title(title)
plt.scatter(x,y)
plt.savefig(way,dpi=1000,bbox_inches='tight')
plt.show()
