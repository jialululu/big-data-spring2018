from osgeo import gdal
import matplotlib.pyplot as plt
import numpy as np
import os
%matplotlib inline

# Mac Users: If you're having issues importing GDAL,
# you may have to add GDAL to your Python path again
# sys.path.insert(0,'/Library/Frameworks/GDAL.framework/Versions/2.2/Python/3.6/site-packages')

DATA = "J:/0 MIT-DUSP life/Academic/11.S941 Big Data/"


from osgeo import gdal
import matplotlib.pyplot as plt
import numpy as np
import os
%matplotlib inline

# Mac Users: If you're having issues importing GDAL,
# you may have to add GDAL to your Python path again
# sys.path.insert(0,'/Library/Frameworks/GDAL.framework/Versions/2.2/Python/3.6/site-packages')

DATA = "J:/0 MIT-DUSP life/Academic/11.S941 Big Data/LC08_L1TP_009047_20130630_20170503_01_T1"

def process_string (st):
    """
    Parses Landsat metadata
    """
    return float(st.split(' = ')[1].strip('\n'))

def ndvi_calc(red, nir):
    """
    Calculate NDVI
    """
    return (nir - red) / (nir + red)

def emissivity_calc (pv, ndvi):
    """
    Calculates an estimate of emissivity
    """
    ndvi_dest = ndvi.copy()
    ndvi_dest[np.where(ndvi < 0)] = 0.991
    ndvi_dest[np.where((0 <= ndvi) & (ndvi < 0.2)) ] = 0.966
    ndvi_dest[np.where((0.2 <= ndvi) & (ndvi < 0.5)) ] = (0.973 * pv[np.where((0.2 <= ndvi) & (ndvi < 0.5)) ]) + (0.966 * (1 - pv[np.where((0.2 <= ndvi) & (ndvi < 0.5)) ]) + 0.005)
    ndvi_dest[np.where(ndvi >= 0.5)] = 0.973
    return ndvi_dest

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


# Your Functions!



def tif2array(location):

    raster_data = gdal.Open (location)
    raster_band = raster_data.GetRasterBand(1)
    raster = raster_band.ReadAsArray()
    raster = raster.astype(np.float32)
    return raster

    """
    Should:
    1. Use gdal.open to open a connection to a file.
    2. Get band 1 of the raster
    3. Read the band as a numpy array
    4. Convert the numpy array to type 'float32'
    5. Return the numpy array.
    """

def retrieve_meta(meta_text):
    """
    Retrieve variables from the Landsat metadata *_MTL.txt file
    Should return a list of length 4.
    'meta_text' should be the location of your metadata file
    Use the process_string function we created in the workshop.
    """

    with open(meta_text) as f:
      meta = f.readlines()
    matchers = ['RADIANCE_MULT_BAND_10', 'RADIANCE_ADD_BAND_10', 'K1_CONSTANT_BAND_10', 'K2_CONSTANT_BAND_10']
    matching = [process_string(s) for s in meta if any(xs in s for xs in matchers)]
    return matching

def rad_calc(tirs, var_list):
    """
    Calculate Top of Atmosphere Spectral Radiance
    Note that you'll have to access the metadata variables by
    their index number in the list, instead of naming them like we did in class.
    """
    rad = var_list[0]*tirs + var_list[1]
    return rad

def bt_calc(rad, var_list):
    """
    Calculate Brightness Temperature
    Again, you'll have to access appropriate metadata variables
    by their index number.
    """
    bt = var_list[3]/np.log((var_list[2])+1)-273.15
    return bt

def pv_calc(ndvi, ndvi_s, ndvi_v):
    """
    Calculate Proportional Vegetation
    """
    pv = (ndvi - ndvi_s) / (ndvi_v - ndvi_s) ** 2
    return pv

def lst_calc(location):
    """
    Calculate Estimate of Land Surface Temperature.
    Your output should
    ---
    Note that this should take as its input ONLY the location
    of a directory in your file system. That means it will have
    to call your other functions. It should:
    1. Define necessary constants
    2. Read in appropriate tifs (using tif2array)
    3. Retrieve needed variables from metadata (retrieve_meta)
    4. Calculate ndvi, rad, bt, pv, emis using appropriate functions
    5. Calculate land surface temperature and return it.
    Your LST function may return strips of low-values around the raster...
    This is a processing artifact that you're not expected to account for.
    Nothing to worry about!
    """
    # define constants
    wave = 10.8E-06
    # PLANCK'S CONSTANT
    h = 6.626e-34
    # SPEED OF LIGHT
    c = 2.998e8
    # BOLTZMANN's CONSTANT
    s = 1.38e-23
    p = h * c / s

    ndvi_s = 0.2
    ndvi_v = 0.5

    # read appropriate tif

    location_red = os.path.join(location, 'LC08_L1TP_009047_20130630_20170503_01_T1_B4.tif')
    location_nir = os.path.join(location, 'LC08_L1TP_009047_20130630_20170503_01_T1_B5.tif')
    location_tirs = os.path.join(location,  'LC08_L1TP_009047_20130630_20170503_01_T1_B10.tif')

    red = tif2array(location_red)
    nir = tif2array(location_nir)
    tirs = tif2array(location_tirs)


    # retrieve variables
    location_meta = os.path.join(DATA, 'LC08_L1TP_009047_20130630_20170503_01_T1_MTL.txt')
    var_list = retrieve_meta(location_meta)


    # calculate Functions
    ndvi = ndvi_calc(red, nir)
    rad = rad_calc(tirs, var_list)
    bt = bt_calc(rad, var_list)
    pv = pv_calc(ndvi, ndvi_s, ndvi_v)
    emis = emissivity_calc (pv, ndvi)


    # calculate land surface Temperature
    lst = bt / (1 + (wave * bt / p) * np.log(emis))
    return lst

lst = lst_calc(DATA)




def cloud_filter(array, bqa):
    """
    Filters out clouds and cloud shadows using values of BQA.
    """
    array_dest = array.copy()
    array_dest[np.where((bqa != 2720) & (bqa != 2724) & (bqa != 2728) & (bqa != 2732)) ] = 'nan'
    return array_dest

cloud_location = os.path.join(DATA, 'LC08_L1TP_009047_20130630_20170503_01_T1_BQA.TIF')
cloud_array = tif2array(cloud_location)
lst_filter = cloud_filter (cloud_array, bqa)

tirs_path = os.path.join(DATA, 'LC08_L1TP_012031_20170716_20170727_01_T1_B10.TIF')
out_path = os.path.join(DATA, 'tan_lst_20130630.tif')
array2tif(tirs_path, out_path, lst_filter)

red_path = os.path.join(DATA, 'LC08_L1TP_009047_20130630_20170503_01_T1_B4.tif')
out_path = os.path.join(DATA, 'tan_ndvi_20130630.tif')
array2tif(tirs_path, out_path, new_ndvi)
