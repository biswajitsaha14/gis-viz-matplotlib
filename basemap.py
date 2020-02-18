"""
__author__= Biswajit Saha
extending cartopy
"""


from cartopy.feature import Feature
import cartopy.crs as ccrs
from cartopy.io import shapereader
import shapely.geometry as sgeom
import numpy as np
import shapefile



COLORS = {'openspace': np.array((208, 232, 216)) / 256.,
          'road': np.array((216, 191, 171)) / 256.,
          'water': np.array((152, 183, 226)) / 256.,
          'rail': np.array((78, 78, 78)) / 256.
          }

class Base(Feature):
    root =None
    
    def __init__(self, filename,**kwargs):

        super().__init__(ccrs.PlateCarree(),**kwargs)
        self._path = self.root +"/"+filename
    
    def geometries(self):
        return self.intersecting_geometries(extent = None)

    def _make_simple_line(self,geom):
        line_good=[]
        all =list(geom)[0].coords

        start_pt = all[0]
        for i in range(1,len(all)):
            end_pt = list(all)[i]
            simple_line = (start_pt, end_pt)
            line_good.append(simple_line)
            start_pt = end_pt
            
        return  sgeom.MultiLineString(line_good)

    def intersecting_geometries(self, extent):
        geometries = shapereader.Reader(self._path).geometries()
        shapetype = shapefile.Reader(self._path).shapeType
        if extent is not None:
            extent_geom = sgeom.box(extent[0], extent[2],
                                    extent[1], extent[3])
        for geom in geometries:
            if extent is None or extent_geom.intersects(geom):
                """
                if shapetype==3:
                    geom = self._make_simple_line(geom)
                """
                yield geom
       
       
class SABase(Base):
    root = r"G:\GSC\Projects\BisWorking\kitchen\30MinutesCity\py3\shp\basemap"


RAILWAY = SABase('railway',edgecolor =COLORS['rail'], facecolor = None, linewidth =0.30) #linestyle ='--'
ROAD = SABase('roads',edgecolor =COLORS['road'], facecolor = None, linewidth = 0.5)
ROAD_DETAILS = SABase('roads_details2',edgecolor =COLORS['road'], facecolor = None, linewidth = 0.10,zorder=-1)
OCEAN = SABase('ocean',edgecolor =None, facecolor = COLORS['water'],zorder=-1)
WATERFEATURE = SABase('waterfeature',edgecolor =None, facecolor = COLORS['water'],zorder=-1)
OPENSPACE = SABase('openspace',edgecolor =None, facecolor = COLORS['openspace'],zorder=-1)

