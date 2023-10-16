#!/usr/bin/env python
# coding: utf-8
import OpenGeoSys
import numpy as np
import rasterio

file_name = 'Recharge2013_2019_FIXED_domesticWaterCons.tif'
with rasterio.open(file_name) as src:
    band1 = src.read(1)
    height = band1.shape[0]
    width = band1.shape[1]
    cols, rows = np.meshgrid(np.arange(width), np.arange(height))
    xs, ys = rasterio.transform.xy(src.transform, rows, cols)
    lons= np.array(xs)[0]
    lats = np.array(ys).T[0]
band2 = 1*band1/1242399685

def find_nearest(array, value):
    if type(value) == float:
        idx = (np.abs(array - value)).argmin()
    else:
        idx = np.zeros(len(value))
        array = np.asarray(array)
        for i in range(len(value)):
            idx[i] = (np.abs(array - value[i])).argmin()
    return idx

# source term for the benchmark
class Rain(OpenGeoSys.SourceTerm):
    def getFlux(self, t, coords, primary_vars):
        x, y, z = coords
        idxX = find_nearest(lons , x)
        idxY = find_nearest(lats , y)
        value = 1*band2[idxY,idxX] 
        Jac = [ 0.0 ]
        return (value, Jac)

# instantiate source term object referenced in OpenGeoSys' prj file
rainSourceTerm = Rain()


