library(geosphere)
library(bda)
library(Imap)
library(dplyr)
#importing the data#
data<- read.csv('c:/Users/DELL/Desktop/Lat_data.csv')


dists_list <- list()

# iterate through data frame placing calculated distance next to place place names
for (i in 1:nrow(data)) {
  
  dists_list[[i]] <- gdist(lon.1 = data$long[i],
                          lat.1 = data$lat[i],
                          lon.2 = data$new_long,
                          lat.2 = data$new_lat, 
                          units="km")
  
  
}






# unlist results and convert to a "named" matrix format
dist_mat <- sapply(dist_list, unlist)
#mapping the result with the main data
data$new_dist<-dist_mat


#biing the data

breaks <- c(0,1,2,3,4,100)
# specify interval/bin labels
tags <- c("[0-1)","[1-2)","[2-3)","[3-4)","[4-1000)")
# bucketing values into bins

data$bin_tags <- cut(data$new_dist, 
                  breaks=breaks, 
                  include.lowest=TRUE, 
                  right=FALSE, 
                  labels=tags)

#tabling the name
table(data$bin_tags,data$Name)


