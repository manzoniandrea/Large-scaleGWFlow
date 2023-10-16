import OpenGeoSys
import numpy as np
import rasterio

file_name = 'DEM_clip.tif'
with rasterio.open(file_name) as src:
    band1 = src.read(1)
    height = band1.shape[0]
    width = band1.shape[1]
    cols, rows = np.meshgrid(np.arange(width), np.arange(height))
    xs, ys = rasterio.transform.xy(src.transform, rows, cols)
    lons= np.array(xs)[0]
    lats = np.array(ys).T[0]
band2 = 0.1*band1/1242399685

def find_nearest(array, value):
    if type(value) == float:
        idx = (np.abs(array - value)).argmin()
    else:
        idx = np.zeros(len(value))
        array = np.asarray(array)
        for i in range(len(value)):
            idx[i] = (np.abs(array - value[i])).argmin()
    return idx


# Source Terms
## Pressure
class BC_p_D(OpenGeoSys.BoundaryCondition):
    def getDirichletBCValue(self, t, coords, node_id, primary_vars):
        p = primary_vars[0]
        x, y, z = coords
        idxX = find_nearest(lons , x)
        idxY = find_nearest(lats , y)
        z_g = band2[idxY,idxX]
        if p/9810+z>z_g:
            p_0 = z_g*9810
        else:
            p_0 = p 



            
        return (True, p_0)


bc_p_D = BC_p_D()
