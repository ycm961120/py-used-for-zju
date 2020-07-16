library(raster)
library(doParallel)
#re-set the path to your folder where your data were saved
setwd("C:/Users/pc/Desktop/QQ big data/QQ")
#make sure there are no the other csv files in the folder
file_list<-list.files(path=".",pattern = "*.csv")
df_raw <-read.table( file_list[1], header=T, sep=",")
long<-df_raw$lon_84
lat<-df_raw$lat_84
df_raw$lon_84<-NULL
df_raw$lat_84<-NULL
ave<-rowSums(df_raw)
df<-data.frame(long,lat,ave)
for(i in 2:length(file_list)){
  df_raw <-read.table( file_list[i], header=T, sep=",")
  long<-df_raw$lon_84
  lat<-df_raw$lat_84
  df_raw$lon_84<-NULL
  df_raw$lat_84<-NULL
  ave<-rowSums(df_raw)
  df_tem<-data.frame(long,lat,ave)
  df<-rbind(df,df_tem)
}
#0.0012333 is the resolution of the Luojia nighttime lights image product
#0.0012333*7 is about 1 km
Res<-0.0012333*14
#Res<-0.0041666667 #this resolution is for NPP-VIIRS nighttime lights image products
maxLat<-53.5608961597
minLong<-73.4469604492
maxLong<-135.088626869
minLat<-18.1608963013
row<-(maxLat-minLat)%/%Res+1
Column_v<-seq(minLong,maxLong,by=Res)
Weight<-c()
#########
CPU<-parallel::detectCores()
cl<-makeCluster(CPU-1)
registerDoParallel(cl)
Weight<-foreach(i=1:row,.combine=c) %dopar%{
  a=maxLat-Res*(i-1)
  b=maxLat-Res*i
  sub_df<-subset(df,lat<=a &lat>b)
  Dfun <- function(x){
    p=x
    q=x+Res
    ss_df<-subset(sub_df,long>=p & long<q)
    return(sum(ss_df$ave))
  }
  w<-sapply(Column_v,FUN=Dfun)
}
stopImplicitCluster()
############
#convert the vector to a raster file
Matrix<-matrix(Weight, row, byrow=TRUE)
Raster<-raster(Matrix)
MaxLong<-minLong+Res*length(Column_v)
MinLat<-maxLat-Res*row
extent(Raster)<-c(minLong,MaxLong,MinLat,maxLat)
res(Raster) <- Res
projection(Raster)<- CRS("+proj=longlat +datum=WGS84 +no_defs +ellps=WGS84 +towgs84=0,0,0")
#give your output raster a name. 
writeRaster(Raster, filename="QQmap.tif", format="GTiff", datatype="INT4U", overwrite=TRUE)
