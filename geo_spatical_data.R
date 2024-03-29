
install.packages("geosphere")
library(geosphere)
install.packages("bda")
library(bda)

#importing the data#
data<- read.csv('C:/Users/LENOVO/Downloads/Data_geo.csv')
get_geo_distance = function(long1, lat1, long2, lat2, units = "miles") {
  loadNamespace("purrr")
  loadNamespace("geosphere")
  longlat1 = purrr::map2(long1, lat1, function(x,y) c(x,y))
  longlat2 = purrr::map2(long2, lat2, function(x,y) c(x,y))
  distance_list = purrr::map2(longlat1, longlat2, function(x,y) geosphere::distHaversine(x, y))
  distance_m = list_extract(distance_list, position = 1)
  if (units == "km") {
    distance = distance_m / 1000.0;
  }
  else if (units == "miles") {
    distance = distance_m / 1609.344
  }
  else {
    distance = distance_m
    # This will return in meter as same way as distHaversine function. 
  }
  distance
}


#use this loop to get individaul distance 
for (i in 1:data$lat) {
for (j in 1:data$long){
new_data= get_geo_distance(lat,long,i,j,unit='km')}}


#biing the data

  breaks <- c(0,1,2,3,4,5,6)
  # specify interval/bin labels
  tags <- c("[0-1)","[1-2)", "[2-3)", "[3-4)", "[4-5)", "[5-6)")
  # bucketing values into bins

data$bin_tags <- cut(data$new_long, 
                  breaks=breaks, 
                  include.lowest=TRUE, 
                  right=FALSE, 
                  labels=tags)



