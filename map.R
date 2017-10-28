library(leaflet)
library(htmlwidgets)
m <- leaflet()
m <- addTiles(m)

# Read CSV into R
MyData <- read.csv(file="geoData.csv", header=TRUE, sep=",")
lat <- MyData[,1]
lng <- MyData[,2]

greenLeafIcon <- makeIcon(
  iconUrl = "http://downloadicons.net/sites/default/files/user-icon-45917.png",
  iconWidth = 20, iconHeight = 50,
  iconAnchorX = 22, iconAnchorY = 94,
)  # OpenStreetMap Base

m <- addMarkers(m,lng,lat,icon = greenLeafIcon,clusterOptions = markerClusterOptions())
saveWidget(m, file="m.html")
