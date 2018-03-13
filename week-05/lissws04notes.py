from osgeo import gdal
import matplotlib.pyplot as plt
import numpy as np
import os
%matplotlib inline
## make sure you set the DATA path to be to the folder where you downloaded the data at the beginning of class
DATA = "C:/Users/Louis Liss/Downloads/ws04_materials"

b4_raster = os.path.join(DATA, 'b4.tif')
b5_raster = os.path.join(DATA, 'b5.tif')

# Load in Red band
red_data = gdal.Open(b4_raster)
red_band = red_data.GetRasterBand(1)
red = red_band.ReadAsArray()

# Load in Near-infrasred band
nir_data = gdal.Open(b5_raster)
nir_band = nir_data.GetRasterBand(1)
nir = nir_band.ReadAsArray()

type(nir)

# make sure you run these two lines at the same time or the color bar won't show up in your plot
plt.imshow(nir)
plt.colorbar()

def ndvi_calc(red, nir):
    """ Calculate NDVI"""
    return (nir - red) / (nir + red)

# throws an error without changigng data type here we are calling our function within the plot!
plt.imshow(ndvi_calc(red, nir), cmap="YlGn")
plt.colorbar()

#checking and fixing data type
red.dtype
nir.dtype

red = red.astype(np.float32)
nir = nir.astype(np.float32)

#re-plotting (Same as above)


plt.imshow(ndvi_calc(red, nir), cmap="YlGn")
plt.colorbar()

ndvi = ndvi_calc(red, nir)

##surface temperature situation

# Path of TIRS Band
tirs_path = os.path.join(DATA, 'b10.TIF')

# Load in TIRS Band
tirs_data = gdal.Open(tirs_path)
tirs_band = tirs_data.GetRasterBand(1)
tirs = tirs_band.ReadAsArray()
tirs = tirs.astype(np.float32)

#which things we need to pull
# RADIANCE_MULT_BAND_10
# RADIANCE_ADD_BAND_10
# K1_CONSTANT_BAND_10
# K2_CONSTANT_BAND_10

# make this path the local path to your MTL.txt file that you downloaded at the start of the workshop
meta_file = 'C:/Users/Louis Liss/Downloads/ws04_materials/MTL.txt'

with open(meta_file) as f:
    meta = f.readlines()

meta

# Define terms to match
matchers = ['RADIANCE_MULT_BAND_10', 'RADIANCE_ADD_BAND_10', 'K1_CONSTANT_BAND_10', 'K2_CONSTANT_BAND_10']

[s for s in meta if any(xs in s for xs in matchers)]

#cleaning the returned list and assigning to values

def process_string (st):
    return float(st.split(' = ')[1].strip('\n'))

matching = [process_string(s) for s in meta if any(xs in s for xs in matchers)]
matching
rad_mult_b10, rad_add_b10, k1_b10, k2_b10 = matching

#top of atmosphere spectral radiance

rad = rad_mult_b10 * tirs + rad_add_b10
plt.imshow(rad, cmap='RdYlGn')
plt.colorbar()

#brightness temperature

bt = k2_b10 / np.log((k1_b10/rad) + 1) - 273.15
plt.imshow(bt, cmap='RdYlGn')
plt.colorbar()

#normalized difference vegetation index

plt.imshow(ndvi, cmap='YlGn')
plt.colorbar()

# propertional vegetation

pv = (ndvi - 0.2) / (0.5 - 0.2) ** 2
plt.imshow(pv, cmap='RdYlGn')
plt.colorbar()

# land surface emissivity

def emissivity_calc (pv, ndvi):
    ndvi_dest = ndvi.copy()
    ndvi_dest[np.where(ndvi < 0)] = 0.991
    ndvi_dest[np.where((0 <= ndvi) & (ndvi < 0.2)) ] = 0.966
    ndvi_dest[np.where((0.2 <= ndvi) & (ndvi < 0.5)) ] = (0.973 * pv[np.where((0.2 <= ndvi) & (ndvi < 0.5)) ]) + (0.966 * (1 - pv[np.where((0.2 <= ndvi) & (ndvi < 0.5)) ]) + 0.005)
    ndvi_dest[np.where(ndvi >= 0.5)] = 0.973
    return ndvi_dest

emis = emissivity_calc(pv, ndvi)

plt.imshow(emis, cmap='RdYlGn')
plt.colorbar()

#land surface temperature

wave = 10.8E-06
# PLANCK'S CONSTANT
h = 6.626e-34
# SPEED OF LIGHT
c = 2.998e8
# BOLTZMANN's CONSTANT
s = 1.38e-23
p = h * c / s

lst = bt / (1 + (wave * bt / p) * np.log(emis))

plt.imshow(lst, cmap='RdYlGn')
plt.colorbar()

#writing into a tif

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

#exporting

out_path = os.path.join(DATA, 'lst.tif')
array2tif(tirs_path, out_path, lst)
