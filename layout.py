
"""
__author__= Biswajit Saha

this shows an example of visualisation of GIS data in matplotlib subplots using cartopy

"""

import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import pyproj
import cartopy
from shapely.geometry import Point
from matplotlib import rc
import matplotlib as mpl
import matplotlib.cm as cm

#rc('text', usetex=True)

from cartopy.io.shapereader import Reader
from cartopy.io.img_tiles import StamenTerrain, OSM, GoogleTiles

from shapely.ops import cascaded_union
import basemap

plt.rcParams["axes.edgecolor"] = "gray"
plt.rcParams["axes.linewidth"] = 0.20

shp = "shp/sa_harbour_diss_2.shp"

def blank_axes(ax):
    """
    blank_axes:  blank the extraneous spines and tick marks for an axes

    Input:
    ax:  a matplotlib Axes object

    Output: None
    """


    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
#end blank_axes

def create_random_points(num_points, shapelypoly):
    import random
    import numpy as np

    xmin, ymin, xmax, ymax = shapelypoly.bounds
    random_points =[]
    while len(random_points)<=num_points:
        pt_coords = [random.uniform(xmin,xmax),random.uniform(ymin,ymax)]
        pt = Point(*pt_coords)
        if shapelypoly.intersects(pt):
            random_points.append(pt_coords)

    return np.array(random_points)

data = Reader(shp)
data_ccrs = ccrs.PlateCarree()

geoms = data.geometries()
geom_diss = cascaded_union(list(geoms))
bounds = geom_diss.bounds#geom_diss.bounds
x1,y1,x2,y2 = bounds
extent =(x1,x2,y1,y2)
#sr = ccrs.epsg(28356)
nrows =2
ncols =2
fig = plt.figure(figsize=(8,8)) 
records = data.records()

fig.suptitle("Harbour CBD",fontweight='light')
#color settings
pop = [row.attributes["POP_2016"] for row in data.records()]
cmap = cm.get_cmap("YlOrRd")
norm = mpl.colors.Normalize(min(pop)*0.5,max(pop))
color_producer = cm.ScalarMappable(norm = norm, cmap = cmap)

for idx,r in enumerate(records):
    
    
    ax = fig.add_subplot(nrows,ncols,idx+1,projection = ccrs.PlateCarree())
    ax.set_extent(extent, data_ccrs)
    #ax.set_title(r.attributes["SYM_CODE"] +"   "+ r"\textbf{" + str(r.attributes["POP_2016"]) + "}")
    ax.set_title("{} ({})".format(r.attributes["SYM_CODE"], int(r.attributes["POP_2016"]), fontsize =6,fontweight='ultralight'))

    blank_axes(ax)
    ax.patch.set_visible(False)
    ax.patch.set_linewidth(0.10)
    ax.set_frame_on(False)
    ax.outline_patch.set_linewidth(0.2) ##

    # tiler = GoogleTiles()
    # ax.add_image(tiler, 15)

    #ax.add_feature(cartopy.feature.LAND)
    #ax.add_feature(cartopy.feature.OCEAN)
    # ax.add_feature(cartopy.feature.COASTLINE)
    # ax.add_feature(cartopy.feature.BORDERS, linestyle=':')
    # ax.add_feature(cartopy.feature.LAKES, alpha=0.5)
    # ax.add_feature(cartopy.feature.RIVERS)

    rgba= color_producer.to_rgba(r.attributes["POP_2016"])
    
    opacity =0.25
    facecolor = list(rgba)[:-1] +[opacity]
    edgecolor =rgba

    ax.add_geometries([r.geometry], crs=data_ccrs, edgecolor=edgecolor,facecolor=facecolor,linewidth =.30)
    #pts = create_random_points(50, geom_diss)
    #ax.scatter(pts[:,0], pts[:,1],marker ='o',color= 'orange')


    ax.add_feature(basemap.OCEAN)
    ax.add_feature(basemap.WATERFEATURE)
    ax.add_feature(basemap.OPENSPACE)
    ax.add_feature(basemap.RAILWAY)
    ax.add_feature(basemap.ROAD_DETAILS)


#plt.tight_layout()
#plt.subplots_adjust(left= 0.0, right= 1.0, bottom=0.0, wspace = 0.1 ,hspace = 0.5 )
#plt.show()
plt.savefig("out.pdf", pad_inches=0, dpi =600)