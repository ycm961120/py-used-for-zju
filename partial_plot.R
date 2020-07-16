#####looping over variables ranked by importance 按照重要性进行循环######
setwd("H:/stan_ouyang")
library(randomForest)
library(showtext)
qdata<-read.csv("H:/Data_collection/chn_RF/新的结果/qdata66_V3.csv")


alldata<-qdata[,5:12]

set.seed(66)
rf<-randomForest(pd_ln~.,alldata,ntree=400,importance = TRUE,plot=TRUE)
rf
importance(rf)

imp<-importance(rf)
impvar<-rownames(imp)[order(imp[,1],decreasing = TRUE)]

par(omi=c(1,1,1,1),mai=c(1.1,1.1,1.1,0.4))
op<-par(mfrow=c(3,3),cex.lab=2,cex.axis=1.5,cex.main=2,lty=2)
for (i in seq_along(impvar)) {
  
  partialPlot(rf,alldata,impvar[i],xlab=impvar[i],
              main = paste("Partial Dependence on",impvar[i]),
              ylim=c(4.8,6.2),
              ylab = "ln(pop_density)")
  
}
par(op)

op<-par(mfrow=c(1,1))


par(mai=c(0.6,0.7,0.52,0.3))#设置页边距（下，左，上，右）
op<-par(mfrow=c(3,3),cex.lab=2,cex.axis=1.5,cex.main=2,lty=2)
ploy1<- partialPlot(rf,            #随机森林模型
                    alldata,        #预测数据?
                    elevation,       #变量名称
                    plot = TRUE, add = FALSE, ylab = "Ln(population density)",ylim=c(5.25,5.65),
                    xlab= "Elevation (m)",main = paste(" ")
                    
)

ploy2<- partialPlot(rf,            #随机森林模型
                    alldata,        #预测数据?
                    slope,       #变量名称
                    plot = TRUE, add = FALSE,
                    ylim=c(5.25,5.65), 
                    xlab="Slope (%)",main = paste(" ")
)

ploy3<- partialPlot(rf,            #随机森林模型
                    alldata,        #预测数据?
                    NDVI,       #变量名称
                    plot = TRUE, add = FALSE,
                    ylim=c(5.25,5.65),
                    xlab="NDVI",main = paste(" ")
)
ploy4<- partialPlot(rf,            #随机森林模型
                    alldata,        #预测数据?
                    density_of_POIs,       #变量名称
                    plot = TRUE, add = FALSE,omi=c(0,0.1,0,0),
                    ylab = "Ln(population density)",ylim=c(4.5,6.5),
                    xlab = "POI density",main = paste(" ")
)
ploy5<- partialPlot(rf,            #随机森林模型
                    alldata,        #预测数据?
                    DtN_POI,       #变量名称
                    plot = TRUE, add = FALSE,
                    ylim=c(4.5,6.5),
                    xlab = "DtN-POI (km)",main = paste(" ")
)
ploy6<- partialPlot(rf,            #随机森林模型
            alldata,        #预测数据?
            brightness_of_NTL,       #变量名称
            
            plot = TRUE, add = FALSE,
            ylim=c(4.5,6.5),
            xlab = "Brightness of NTL",main = paste(" ")
)

ploy7<- partialPlot(rf,            #随机森林模型
                    alldata,        #预测数据?
                    Dtc_road,       #变量名称
                    plot = TRUE, add = FALSE,
                    ylab = "Ln(population density)",ylim=c(4.5,6.5),
                    xlab = "Dtc-road (km)",main = paste(" ")
)


tiff(file="ploy2.tif",width=100, height=100, units='mm',res=300)

dev.off()



