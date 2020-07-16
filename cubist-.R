library(sp)
library(raster)
library(lattice)
library(stringi)
library(ggplot2)
library(Cubist)
library(caret)

rdata<-read.csv("G:/pre/pre.csv")
y_data<-rdata[,6]
x_data<-rdata[,c(7,8,9,10,11,12,13)]
View(x_data)

cTune<-train(x=x_data,y=y_data,"cubist",
             tuneGrid=expand.grid(committees=seq(1,100,5),neighbors=c(0:9)),
             trControl=trainControl(method="cv"))
modeltree<-cubist(x=x_data,y=y_data,
                  committees = cTune$bestTune$committees,
                  neighbors=cTune$bestTune$neighbors)
#summary(modeltree)

dem<-raster("G:/pre1/dem/dem1.tif",layer=1,values=TRUE)
slope<-raster("G:/pre1/slope/slope1.tif",layer=1,values=TRUE)
ndvi<-raster("G:/pre1/ndvi/ndvi1.tif",layer=1,values=TRUE)
ntl<-raster("G:/pre1/ntl/ols1.tif",layer=1,values=TRUE)
road<-raster("G:/pre1/road/road1.tif",layer=1,values=TRUE)
poidens<-raster("G:/pre1/poidens/pdens1.tif",layer=1,values=TRUE)
poidst<-raster("G:/pre1/poidst/pdst1.tif",layer=1,values=TRUE)
mdem<-as.matrix(dem)
rm(dem)
mslope<-as.matrix(slope)
rm(slope)
mndvi<-as.matrix(ndvi)
rm(ndvi)
mntl<-as.matrix(ntl)
rm(ntl)
mroad<-as.matrix(road)
rm(road)
mpoidens<-as.matrix(poidens)
rm(poidens)
mpoidst<-as.matrix(poidst)
rm(poidst)
vdem<-as.vector(mdem)
vdem[is.na(vdem)]<-0
rm(mdem)
vslope<-as.vector(mslope)
vslope[is.na(vslope)]<-0
rm(mslope)
vndvi<-as.vector(mndvi)
vndvi[is.na(vndvi)]<-0
rm(mndvi)
vntl<-as.vector(mntl)
vntl[is.na(vntl)]<-0
rm(mntl)
vroad<-as.vector(mroad)
vroad[is.na(vroad)]<-0
rm(mroad)
vpoidens<-as.vector(mpoidens)
vpoidens[is.na(vpoidens)]<-0
rm(mpoidens)
vpoidst<-as.vector(mpoidst)
vpoidst[is.na(vpoidst)]<-0
rm(mpoidst)
newdf<-data.frame(ndvi=c(vndvi),ntl=c(vntl),poidens=c(vpoidens),poidst=c(vpoidst),road=c(vroad),slope=c(vslope),dem=c(vdem))
head(newdf)
rm(vdem)
rm(vslope)
rm(vndvi)
rm(vntl)
rm(vpoidens)
rm(vpoidst)
rm(vroad)
rm(rdata)
rm(x_data)
rm(y_data)
pre<-predict(modeltree,newdf,neighbors = cTune$bestTune$neighbors)
mpre1<-matrix(pre,nrow=3287,ncol=4406)
rpre1<-raster(mpre1,xmin<-384626.5,xmax<-825226.5,ymin<-1876727,ymax<-2205427,crs<-crs("+proj=aea +lat_1=25 +lat_2=47 +lat_0=0 +lon_0=105 +x_0=0 +y_0=0 +ellps=krass +units=m +no_defs"))
writeRaster(rpre1,"G:/pre1.tif",format="GTiff")
rm(pre)
rm(mpre1)
rm(rpre1)


