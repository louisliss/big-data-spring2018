# Problem Set 4: Working With Landsat Data
# My Code

```python

#defining calculations

from osgeo import gdal
import matplotlib.pyplot as plt
import numpy as np
import os
%matplotlib inline

DATA = "C:/Users/Louis Liss/Downloads/pset04_materials/"
location = os.path.join(DATA, 'b4.tif')
meta_text = os.path.join(DATA, 'MTL.txt')
red = tif2array(os.path.join(DATA, 'b4.tif'))
nir = tif2array(os.path.join(DATA, 'b5.tif'))

def tif2array(location):
  data = gdal.Open(location)
  band = data.GetRasterBand(1)
  array = band.ReadAsArray()
  array = array.astype(np.float32)
  return array

def process_string (st):
  return float(st.split(' = ')[1].strip('\n'))

def retrieve_meta(meta_text):
  with open(meta_text) as f:
      meta = f.readlines()
  matchers = ['RADIANCE_MULT_BAND_10', 'RADIANCE_ADD_BAND_10', 'K1_CONSTANT_BAND_10', 'K2_CONSTANT_BAND_10']
  [s for s in meta if any(xs in s for xs in matchers)]
  def process_string (st):
    return float(st.split(' = ')[1].strip('\n'))
  matching = [process_string(s) for s in meta if any(xs in s for xs in matchers)]
  rad_mult_b10, rad_add_b10, k1_b10, k2_b10 = matching
  return matching

def rad_calc(tirs, var_list):
  rad_mult_b10 = var_list[0]
  rad_add_b10 = var_list[1]
  rad = rad_mult_b10 * tirs + rad_add_b10
  return rad

def bt_calc(rad, var_list):
  k2_b10 = var_list[3]
  k1_b10 = var_list[2]
  bt = k2_b10 / np.log((k1_b10/rad) + 1) - 273.15
  return bt

def ndvi_calc(red, nir):
  ndvi = (nir - red) / (nir + red)
  return ndvi

def emissivity_calc (pv, ndvi):
  ndvi_dest = ndvi.copy()
  ndvi_dest[np.where(ndvi < 0)] = 0.991
  ndvi_dest[np.where((0 <= ndvi) & (ndvi < 0.2)) ] = 0.966
  ndvi_dest[np.where((0.2 <= ndvi) & (ndvi < 0.5)) ] = (0.973 * pv[np.where((0.2 <= ndvi) & (ndvi < 0.5)) ]) + (0.966 * (1 - pv[np.where((0.2 <= ndvi) & (ndvi < 0.5)) ]) + 0.005)
  ndvi_dest[np.where(ndvi >= 0.5)] = 0.973
  return ndvi_dest

def pv_calc(ndvi):
  pv = (ndvi - 0.2) / (0.5 - 0.2) ** 2
  return pv

def lst_calc(location):
  wave = 10.8E-06
# PLANCK'S CONSTANT
  h = 6.626e-34
# SPEED OF LIGHT
  c = 2.998e8
# BOLTZMANN's CONSTANT
  s = 1.38e-23
  p = h * c / s
  tirs = tif2array(location)
  var_list = retrieve_meta(meta_text)
  rad = rad_calc(tirs, var_list)
  bt = bt_calc(rad, var_list)
  ndvi = ndvi_calc(red, nir)
  pv = pv_calc(ndvi)
  emis = emissivity_calc(pv, ndvi)
  lst = bt / (1 + (wave * bt / p) * np.log(emis))
  return lst

##Create NDVI and LST Maps

ndvi = ndvi_calc(red,nir)
# plt.imshow(ndvi, cmap='RdYlGn')
# plt.colorbar()

location = os.path.join(DATA, 'b10.tif')
lst = lst_calc(location)
# plt.imshow(lst, cmap='RdYlGn')
# plt.colorbar()

##Cloud filter

def cloud_filter(array, bqa):
    array_dest = array.copy()
    array_dest[np.where((bqa != 2720) & (bqa != 2724) & (bqa != 2728) & (bqa != 2732)) ] = 'nan'
    return array_dest

bqa = tif2array(os.path.join(DATA, 'bqa.tif'))
array = lst
lst_filter = cloud_filter(array, bqa)

array = ndvi
ndvi_filter = cloud_filter(array, bqa)

## Write Your Filtered Arrays as `.tifs`

def array2tif(raster_file, new_raster_file, array):
    """
    Writes 'array' to a new tif, 'new_raster_file',
    whose properties are given by a reference tif,
    here called 'raster_file.'
    """
    # Invoke the GDAL Geotiff driver
    raster = gdal.Open(raster_file)

    driver = gdal.GetDriverByName('GTiff')
    out_raster = driver.Create(new_raster_file,
                        raster.RasterXSize,
                        raster.RasterYSize,
                        1,
                        gdal.GDT_Float32)
    out_raster.SetProjection(raster.GetProjection())
    # Set transformation - same logic as above.
    out_raster.SetGeoTransform(raster.GetGeoTransform())
    # Set up a new band.
    out_band = out_raster.GetRasterBand(1)
    # Set NoData Value
    out_band.SetNoDataValue(-1)
    # Write our Numpy array to the new band!
    out_band.WriteArray(array)

tirs_path = os.path.join(DATA, 'b10.tif')
out_path = os.path.join(DATA, 'liss_lst_20170309.tif')
array2tif(tirs_path, out_path, lst_filter)

tirs_path = os.path.join(DATA, 'b10.tif')
out_path = os.path.join(DATA, 'liss_ndvi_20170309.tif')
array2tif(tirs_path, out_path, ndvi_filter)


```
