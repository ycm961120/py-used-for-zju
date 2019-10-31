library(sp)
library(raster)
library(randomForest)
rdata<-read.csv("d:/2010gdp_1_1.csv")
ydata<-rdata[,5]
xdata<-rdata[,c(6:10)]
View(xdata)

#?????????
n = c('5','6','7','8','9')
#????????????
way = 'C:/test/test'

###################################################
#??????
set.seed(105)
rf<-randomForest(x=xdata,y=ydata,mtry=2,importance = TRUE,plot=TRUE)
rf
importance(rf)

rm(rdata)
rm(xdata)
rm(ydata)
#??????
for (i in n){
  way_new = paste('C:/test/test/brightness',i,'.tif',sep='')
  bright<-raster(way_new,layer=1,values=TRUE)
  way_new = paste('C:/test/test/farm',i,'.tif',sep='')
  farm<-raster(way_new,layer=1,values=TRUE)
  way_new = paste('C:/test/test/lst',i,'.tif',sep='')
  lst<-raster(way_new,layer=1,values=TRUE)
  way_new = paste('C:/test/test/ndvi',i,'.tif',sep='')
  ndvi<-raster(way_new,layer=1,values=TRUE)
  way_new = paste('C:/test/test/slope',i,'.tif',sep='')
  slope<-raster(way_new,layer=1,values=TRUE)
  
  x_min = xmin(extent(bright))
  x_max = xmax(extent(bright))
  y_min = ymin(extent(bright))
  y_max = ymax(extent(bright))
  
  mbright<-as.matrix(bright)
  rm(bright)
  mfarm<-as.matrix(farm)
  rm(farm)
  mlst<-as.matrix(lst)
  rm(lst)
  mndvi<-as.matrix(ndvi)
  rm(ndvi)
  mslope<-as.matrix(slope)
  rm(slope)
  
  vbright<-as.vector(mbright)
  vbright[is.na(vbright)]<-0
  rm(mbright)
  vfarm<-as.vector(mfarm)
  vfarm[is.na(vfarm)]<-0
  rm(mfarm)
  vlst<-as.vector(mlst)
  vlst[is.na(vlst)]<-0
  rm(mlst)
  vndvi<-as.vector(mndvi)
  vndvi[is.na(vndvi)]<-0
  rm(mndvi)
  vslope<-as.vector(mslope)
  vslope[is.na(vslope)]<-0
  rm(mslope)
  
  my<-data.frame(farm=c(vfarm),ndvi=c(vndvi),bright=c(vbright),slope=c(vslope),lst_day=c(vlst))
  head(my)
  
  rm(vfarm)
  rm(vndvi)
  rm(vbright)
  rm(vslope)
  rm(vlst)
  
  pre<-predict(rf,my)
  
  mpre<-matrix(pre,nrow=3325,ncol=3652)
  rpre<-raster(mpre,xmin<-x_min,xmax<-x_max,ymin<-y_min,ymax<-y_max,crs<-crs("+proj=aea +lat_1=25 +lat_2=47 +lat_0=0 +lon_0=105 +x_0=0 +y_0=0 +ellps=krass +units=m +no_defs"))
  way_out = paste('C:/test/pre/pre',i,'.tif',sep='')
  writeRaster(rpre,way_out,format="GTiff")
  
  rm(pre)
  rm(mpre)
  rm(rpre)
}



