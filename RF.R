
library(sp)
library(raster)
library(randomForest)
rdata<-read.csv("c:/test/2010pop.csv")
ydata<-rdata[,4]
xdata<-rdata[,c(5:9)]
View(xdata)

set.seed(105)
rf<-randomForest(x=xdata,y=ydata,mtry=2,importance = TRUE,plot=TRUE)
rf
importance(rf)

#'--------------------------------------------------------'
namelist <- colnames(rdata)


x1 <- raster(paste("C:/test/test/",namelist[5],".tif",sep=""),layer=1,values=TRUE)
x2 <- raster(paste("C:/test/test/",namelist[6],".tif",sep=""),layer=1,values=TRUE)
x3 <- raster(paste("C:/test/test/",namelist[7],".tif",sep=""),layer=1,values=TRUE)
x4 <- raster(paste("C:/test/test/",namelist[8],".tif",sep=""),layer=1,values=TRUE)

class(x1)
a <- "my first list"
b <- "1:3"
c <- matrix(0, ncol=3,nrow=4)
mylist <- NULL
mylist[[1]] <- a
mylist[[2]] <- b
mylist[[3]] <- c


dem<-raster("C:/test/trash/dem0.tif",layer=1,values=TRUE)
slope<-raster("F:/2010slope0.tif",layer=1,values=TRUE)
ndvi<-raster("F:/2010ndvi0.tif",layer=1,values=TRUE)
dmsp<-raster("F:/2010dmsp0.tif",layer=1,values=TRUE)
ghsl<-raster("F:/2010ghsl0.tif",layer=1,values=TRUE)
poi<-raster("F:/poipca0.tif",layer=1,values=TRUE)
mdem<-as.matrix(dem)
rm(dem)
mslope<-as.matrix(slope)
rm(slope)
mndvi<-as.matrix(ndvi)
rm(ndvi)
mdmsp<-as.matrix(dmsp)
rm(dmsp)
mghsl<-as.matrix(ghsl)
rm(ghsl)
mpoi<-as.matrix(poi)
rm(poi)
vdem<-as.vector(mdem)
vdem[is.na(vdem)]<-0
rm(mdem)
vslope<-as.vector(mslope)
vslope[is.na(vslope)]<-0
rm(mslope)
vndvi<-as.vector(mndvi)
vndvi[is.na(vndvi)]<-0
rm(mndvi)
vdmsp<-as.vector(mdmsp)
vdmsp[is.na(vdmsp)]<-0
rm(mdmsp)
vghsl<-as.vector(mghsl)
vghsl[is.na(vghsl)]<-0
rm(mghsl)
vpoi<-as.vector(mpoi)
vpoi[is.na(vpoi)]<-0
rm(mpoi)
my<-data.frame(dem1=c(vdem),slope1=c(vslope),ndvi1=c(vndvi),dmsp1=c(vdmsp),ghsl1=c(vghsl))
head(my)
rm(vdem)
rm(vslope)
rm(vndvi)
rm(vdmsp)
rm(vghsl)
rm(vpoi)
rm(rdata)
rm(xdata)
rm(ydata)
pre<-predict(rf,my)
mpre0<-matrix(pre,nrow=7425,ncol=18192)
rpre0<-raster(mpre0,xmin<-447416.7,xmax<-2266617,ymin<-2020300,ymax<-2762800,crs<-crs("+proj=utm +zone=48 +datum=WGS84 +units=m +no_defs +ellps=WGS84 +towgs84=0,0,0"))
writeRaster(rpre0,"F:/pre0.tif",format="GTiff")

















dem<-raster("F:/2010dem1.tif",layer=1,values=TRUE)
slope<-raster("F:/2010slope1.tif",layer=1,values=TRUE)
ndvi<-raster("F:/2010ndvi1.tif",layer=1,values=TRUE)
dmsp<-raster("F:/2010dmsp1.tif",layer=1,values=TRUE)
ghsl<-raster("F:/2010ghsl1.tif",layer=1,values=TRUE)
#poi<-raster("F:/poipca1.tif",layer=1,values=TRUE)

mdem<-as.matrix(dem)
rm(dem)
mslope<-as.matrix(slope)
rm(slope)
mndvi<-as.matrix(ndvi)
rm(ndvi)
mdmsp<-as.matrix(dmsp)
rm(dmsp)
mghsl<-as.matrix(ghsl)
rm(ghsl)
#mpoi<-as.matrix(poi)
#rm(poi)


vdem<-as.vector(mdem)
vdem[is.na(vdem)]<-0
rm(mdem)
vslope<-as.vector(mslope)
vslope[is.na(vslope)]<-0
rm(mslope)
vndvi<-as.vector(mndvi)
vndvi[is.na(vndvi)]<-0
rm(mndvi)
vdmsp<-as.vector(mdmsp)
vdmsp[is.na(vdmsp)]<-0
rm(mdmsp)
vghsl<-as.vector(mghsl)
vghsl[is.na(vghsl)]<-0
rm(mghsl)
#vpoi<-as.vector(mpoi)
#vpoi[is.na(vpoi)]<-0
#rm(mpoi)

my<-data.frame(dem1=c(vdem),slope1=c(vslope),ndvi1=c(vndvi),dmsp1=c(vdmsp),ghsl1=c(vghsl))
head(my)

rm(vdem)
rm(vslope)
rm(vndvi)
rm(vdmsp)
rm(vghsl)
rm(vpoi)
rm(rdata)
rm(xdata)
rm(ydata)


pre<-predict(rf,my)


mpre1<-matrix(pre,nrow=7425,ncol=18192)
rpre1<-raster(mpre1,xmin<-447416.7,xmax<-2266617,ymin<-2762800,ymax<-3505300,crs<-crs("+proj=utm +zone=48 +datum=WGS84 +units=m +no_defs +ellps=WGS84 +towgs84=0,0,0"))
writeRaster(rpre1,"F:/pre1.tif",format="GTiff")














dem<-raster("F:/2010dem2.tif",layer=1,values=TRUE)
slope<-raster("F:/2010slope2.tif",layer=1,values=TRUE)
ndvi<-raster("F:/2010ndvi2.tif",layer=1,values=TRUE)
dmsp<-raster("F:/2010dmsp2.tif",layer=1,values=TRUE)
ghsl<-raster("F:/2010ghsl2.tif",layer=1,values=TRUE)
#poi<-raster("F:/poipca2.tif",layer=1,values=TRUE)

mdem<-as.matrix(dem)
rm(dem)
mslope<-as.matrix(slope)
rm(slope)
mndvi<-as.matrix(ndvi)
rm(ndvi)
mdmsp<-as.matrix(dmsp)
rm(dmsp)
mghsl<-as.matrix(ghsl)
rm(ghsl)
#mpoi<-as.matrix(poi)
#rm(poi)


vdem<-as.vector(mdem)
vdem[is.na(vdem)]<-0
rm(mdem)
vslope<-as.vector(mslope)
vslope[is.na(vslope)]<-0
rm(mslope)
vndvi<-as.vector(mndvi)
vndvi[is.na(vndvi)]<-0
rm(mndvi)
vdmsp<-as.vector(mdmsp)
vdmsp[is.na(vdmsp)]<-0
rm(mdmsp)
vghsl<-as.vector(mghsl)
vghsl[is.na(vghsl)]<-0
rm(mghsl)
#vpoi<-as.vector(mpoi)
#vpoi[is.na(vpoi)]<-0
#rm(mpoi)

my<-data.frame(dem1=c(vdem),slope1=c(vslope),ndvi1=c(vndvi),dmsp1=c(vdmsp),ghsl1=c(vghsl))
head(my)

rm(vdem)
rm(vslope)
rm(vndvi)
rm(vdmsp)
rm(vghsl)
rm(vpoi)
rm(rdata)
rm(xdata)
rm(ydata)


pre<-predict(rf,my)


mpre2<-matrix(pre,nrow=7425,ncol=18192)
rpre2<-raster(mpre2,xmin<-447416.7,xmax<-2266617,ymin<-3505300,ymax<-4247800,crs<-crs("+proj=utm +zone=48 +datum=WGS84 +units=m +no_defs +ellps=WGS84 +towgs84=0,0,0"))
writeRaster(rpre2,"F:/pre2.tif",format="GTiff")




















dem<-raster("F:/2010dem3.tif",layer=1,values=TRUE)
slope<-raster("F:/2010slope3.tif",layer=1,values=TRUE)
ndvi<-raster("F:/2010ndvi3.tif",layer=1,values=TRUE)
dmsp<-raster("F:/2010dmsp3.tif",layer=1,values=TRUE)
ghsl<-raster("F:/2010ghsl3.tif",layer=1,values=TRUE)
#poi<-raster("F:/poipca3.tif",layer=1,values=TRUE)

mdem<-as.matrix(dem)
rm(dem)
mslope<-as.matrix(slope)
rm(slope)
mndvi<-as.matrix(ndvi)
rm(ndvi)
mdmsp<-as.matrix(dmsp)
rm(dmsp)
mghsl<-as.matrix(ghsl)
rm(ghsl)
mpoi<-as.matrix(poi)
rm(poi)


vdem<-as.vector(mdem)
vdem[is.na(vdem)]<-0
rm(mdem)
vslope<-as.vector(mslope)
vslope[is.na(vslope)]<-0
rm(mslope)
vndvi<-as.vector(mndvi)
vndvi[is.na(vndvi)]<-0
rm(mndvi)
vdmsp<-as.vector(mdmsp)
vdmsp[is.na(vdmsp)]<-0
rm(mdmsp)
vghsl<-as.vector(mghsl)
vghsl[is.na(vghsl)]<-0
rm(mghsl)
#vpoi<-as.vector(mpoi)
#vpoi[is.na(vpoi)]<-0
#rm(mpoi)

my<-data.frame(dem1=c(vdem),slope1=c(vslope),ndvi1=c(vndvi),dmsp1=c(vdmsp),ghsl1=c(vghsl))
head(my)

rm(vdem)
rm(vslope)
rm(vndvi)
rm(vdmsp)
rm(vghsl)
rm(vpoi)
rm(rdata)
rm(xdata)
rm(ydata)


pre<-predict(rf,my)


mpre3<-matrix(pre,nrow=7425,ncol=18192)
rpre3<-raster(mpre3,xmin<-447416.7,xmax<-2266617,ymin<-4247800,ymax<-4990300,crs<-crs("+proj=utm +zone=48 +datum=WGS84 +units=m +no_defs +ellps=WGS84 +towgs84=0,0,0"))
writeRaster(rpre3,"F:/pre3.tif",format="GTiff")




