
# coding: utf-8

# This notebook is part of the $\omega radlib$ documentation: http://wradlib.org/wradlib-docs.
# 
# Copyright (c) 2016, $\omega radlib$ developers.
# Distributed under the MIT License. See LICENSE.txt for more info.

# # Supported radar data formats

# The binary encoding of many radar products is a major obstacle for many potential radar users. Often, decoder software is not easily available. In case formats are documented, the implementation of decoders is a major programming effort. This tutorial provides an overview of the data formats currently supported by $\omega radlib$. We seek to continuously enhance the range of supported formats, so this document is only a snapshot. If you need a specific file format to be supported by $\omega radlib$, please [raise an issue](https://github.com/wradlib/wradlib/issues/new) of type *enhancement*. You can provide support by adding documents which help to decode the format, e.g. format reference documents or software code in other languages for decoding the format.
# 
# At the moment, *supported format* means that the radar format can be read and further processed by wradlib. Normally, wradlib will return an array of data values and a dictionary of metadata - if the file contains any. wradlib does not support encoding to any specific file formats, yet! This might change in the future, but it is not a priority. However, you can use Python's netCDF4 or h5py packages to encode the results of your analysis to standard self-describing file formats such as netCDF or hdf5. 

# In the following, we will provide an overview of file formats which can be currently read by $\omega radlib$. Reading weather radar files is done via the [wradlib.io](http://wradlib.org/wradlib-docs/latest/io.html) module. There you will find a complete function reference. 

# In[ ]:

import wradlib as wrl
import matplotlib.pyplot as pl
import matplotlib as mpl
import warnings
warnings.filterwarnings('ignore')
try:
    get_ipython().magic("matplotlib inline")
except:
    pl.ion()
import numpy as np


# ## German Weather Service: DX format

# The German Weather Service uses the DX file format to encode local radar sweeps. DX data are in polar coordinates. The naming convention is as follows: <pre>raa00-dx_&lt;location-id&gt;-&lt;YYMMDDHHMM&gt;-&lt;location-abreviation&gt;---bin</pre> or <pre>raa00-dx_&lt;location-id&gt;-&lt;YYYYMMDDHHMM&gt;-&lt;location-abreviation&gt;---bin</pre>
# [Read and plot DX radar data from DWD](wradlib_reading_dx.ipynb) provides an extensive introduction into working with DX data. For now, we would just like to know how to read the data:

# In[ ]:

filename = wrl.util.get_wradlib_data_file('dx/raa00-dx_10908-0806021655-fbg---bin.gz')
data, metadata = wrl.io.readDX(filename)


# Here, ``data`` is a two dimensional array of shape (number of azimuth angles, number of range gates). This means that the number of rows of the array corresponds to the number of azimuth angles of the radar sweep while the number of columns corresponds to the number of range gates per ray.

# In[ ]:

print(data.shape)
print(metadata.keys())


# In[ ]:

fig = pl.figure(figsize=(10,8))
im = wrl.vis.plot_cg_ppi(data, fig=fig)


# ## German Weather Service: RADOLAN (quantitative) composit

# The quantitative composite format of the DWD (German Weather Service) was established in the course of the [RADOLAN project](https://www.dwd.de/RADOLAN). Most quantitative composite products from the DWD are distributed in this format, e.g. the R-series (RX, RY, RH, RW, ...), the S-series (SQ, SH, SF, ...), and the E-series (European quantitative composite, e.g. EZ, EH, EB). Please see the [composite format description](https://www.dwd.de/DE/leistungen/radolan/radolan_info/radolan_radvor_op_komposit_format_pdf.pdf?__blob=publicationFile&v=5) for a full reference and a full table of products (unfortunately only in German language). An extensive section covering many RADOLAN aspects is here: [RADOLAN](../radolan.ipynb)
# 
# Currently, the RADOLAN composites have a spatial resolution of 1km x 1km, with the national composits (R- and S-series) being 900 x 900 grids, and the European composits 1500 x 1400 grids. The projection is [polar-stereographic](../radolan/radolan-grid.ipynb#Polar-Stereographic-Projection). The products can be read by the following function:

# In[ ]:

filename = wrl.util.get_wradlib_data_file('radolan/misc/raa01-rw_10000-1408102050-dwd---bin.gz')
data, metadata = wrl.io.read_RADOLAN_composite(filename)


# Here, ``data`` is a two dimensional integer array of shape (number of rows, number of columns). Different product types might need different levels of postprocessing, e.g. if the product contains rain rates or accumulations, you will normally have to divide data by factor 10. ``metadata`` is again a dictionary which provides metadata from the files header section, e.g. using the keys *producttype*, *datetime*, *intervalseconds*, *nodataflag*. 

# In[ ]:

print(data.shape)
print(metadata.keys())


# Masking the NoData (or missing) values can be done by:

# In[ ]:

import numpy as np
maskeddata = np.ma.masked_equal(data, metadata["nodataflag"])


# In[ ]:

fig = pl.figure(figsize=(10,8))
# get coordinates
radolan_grid_xy = wrl.georef.get_radolan_grid(900,900)
x = radolan_grid_xy[:,:,0]
y = radolan_grid_xy[:,:,1]

# create quick plot with colorbar and title
pl.figure(figsize=(10,8))
pl.pcolormesh(x, y, maskeddata)


# ## HDF5

# ### OPERA HDF5 (ODIM_H5)

# [HDF5](https://www.hdfgroup.org/HDF5/) is a data model, library, and file format for storing and managing data. The [OPERA 3 program](http://www.eumetnet.eu/opera) developed a convention (or information model) on how to store and exchange radar data in hdf5 format. It is based on the work of [COST Action 717](http://www.smhi.se/hfa_coord/cost717) and is used e.g. in real-time operations in the Nordic European countries. The OPERA Data and Information Model (ODIM) is documented e.g. in this [report](https://www.eol.ucar.edu/system/files/OPERA_2008_03_WP2.1b_ODIM_H5_v2.1.pdf) and in a [UML representation](http://www.eumetnet.eu/sites/default/files/OPERA_2008_18_WP2.1b_ODIM_UML.pdf). Make use of these documents in order to understand the organization of OPERA hdf5 files!
# 
# The hierarchical nature of HDF5 can be described as being similar to directories, files, and links on a hard-drive. Actual metadata are stored as so-called *attributes*, and these attributes are organized together in so-called *groups*. Binary data are stored as so-called *datasets*. As for ODIM_H5, the ``root`` (or top level) group contains three groups of metadata: these are called ``what`` (object, information model version, and date/time information), ``where`` (geographical information), and ``how`` (quality and optional/recommended metadata). For a very simple product, e.g. a CAPPI, the data is organized in a group called ``dataset1`` which contains another group called ``data1`` where the actual binary data are found in ``data``. In analogy with a file system on a hard-disk, the HDF5 file containing this simple product is organized like this:
# 
# ```
#     /
#     /what
#     /where
#     /how
#     /dataset1
#     /dataset1/data1
#     /dataset1/data1/data
# ```
# 
# The philosophy behind the $\omega radlib$ interface to OPERA's data model is very straightforward: $\omega radlib$ simply translates the complete file structure to *one* dictionary and returns this dictionary to the user. Thus, the potential complexity of the stored data is kept and it is left to the user how to proceed with this data. The keys of the output dictionary are strings that correspond to the "directory trees" shown above. Each key ending with ``/data`` points to a Dataset (i.e. a numpy array of data). Each key ending with ``/what``, ``/where`` or ``/how`` points to another dictionary of metadata. The entire output can be obtained by:

# In[ ]:

filename = wrl.util.get_wradlib_data_file('hdf5/knmi_polar_volume.h5')
fcontent = wrl.io.read_OPERA_hdf5(filename)


# The user should inspect the output obtained from his or her hdf5 file in order to see how access those items which should be further processed. In order to get a readable overview of the output dictionary, one can use the pretty printing module:

# In[ ]:

# which keyswords can be used to access the content?
print(fcontent.keys())
# print the entire content including values of data and metadata
# (numpy arrays will not be entirely printed)
print(fcontent['dataset1/data1/data'])


# Please note that in order to experiment with such datasets, you can download hdf5 sample data from the [Odyssey page](http://www.eumetnet.eu/odyssey-opera-data-centre) of the [OPERA 3 homepage](http://www.eumetnet.eu/opera) or use the example data provided with the [wradlib-data](https://github.com/wradlib/wradlib-data/) repository.

# In[ ]:

fig = pl.figure(figsize=(10,8))
im = wrl.vis.plot_cg_ppi(fcontent['dataset1/data1/data'], fig=fig)


# ### GAMIC HDF5

# GAMIC refers to the commercial [GAMIC Enigma MURAN software](https://www.gamic.com) which exports data in hdf5 format. The concept is quite similar to the above [OPERA HDF5 (ODIM_H5)](#OPERA-HDF5-(ODIM_H5%29) format. Such a file (typical ending: *.mvol*) can be read by:

# In[ ]:

filename = wrl.util.get_wradlib_data_file('hdf5/2014-08-10--182000.ppi.mvol')
data, metadata = wrl.io.read_GAMIC_hdf5(filename)


# While metadata represents the usual dictionary of metadata, the data variable is a dictionary which might contain several numpy arrays with the keywords of the dictionary indicating different moments.

# In[ ]:

print(metadata.keys())
print(metadata['VOL'])
print(metadata['SCAN0'].keys())


# In[ ]:

print(data['SCAN0'].keys())
print(data['SCAN0']['PHIDP'].keys())
print(data['SCAN0']['PHIDP']['data'].shape)


# In[ ]:

fig = pl.figure(figsize=(10,8))
im = wrl.vis.plot_cg_ppi(data['SCAN0']['ZH']['data'], fig=fig)


# ### Generic HDF5

# This is a generic hdf5 reader, which will read any hdf5 structure.

# In[ ]:

filename = wrl.util.get_wradlib_data_file('hdf5/2014-08-10--182000.ppi.mvol')
fcontent = wrl.io.read_generic_hdf5(filename)


# In[ ]:

print(fcontent.keys())


# In[ ]:

print(fcontent['where'])
print(fcontent['how'])
print(fcontent['scan0/moment_3'].keys())
print(fcontent['scan0/moment_3']['attrs'])
print(fcontent['scan0/moment_3']['data'].shape)


# In[ ]:

fig = pl.figure(figsize=(10,8))
im = wrl.vis.plot_cg_ppi(fcontent['scan0/moment_3']['data'], fig=fig)


# ## NetCDF

# The NetCDF format also claims to be self-describing. However, as for all such formats, the developers of netCDF also admit that "[...] the mere use of netCDF is not sufficient to make data self-describing and meaningful to both humans and machines [...]" (see [here](http://www.unidata.ucar.edu/software/netcdf/documentation/historic/netcdf/Conventions.html). Different radar operators or data distributors will use different naming conventions and data hierarchies (i.e. "data models") that the reading program might need to know about.
# 
# $\omega radlib$ provides two solutions to address this challenge. The first one ignores the concept of data models and just pulls all data and metadata from a NetCDF file ([wradlib.io.read_generic_netcdf()](http://wradlib.org/wradlib-docs/latest/generated/wradlib.io.read_generic_netcdf.html). The second is designed for a specific data model used by the EDGE software ([wradlib.io.read_EDGE_netcdf()](http://wradlib.org/wradlib-docs/latest/generated/wradlib.io.read_EDGE_netcdf.html)).

# ### Generic NetCDF reader (includes CfRadial)

# $\omega radlib$ provides a function that will virtually read any NetCDF file irrespective of the data model: [wradlib.io.read_generic_netcdf()](http://wradlib.org/wradlib-docs/latest/generated/wradlib.io.read_generic_netcdf.html). It is built upon Python's [netcdf4](https://unidata.github.io/netcdf4-python/) library. [wradlib.io.read_generic_netcdf()](http://wradlib.org/wradlib-docs/latest/generated/wradlib.io.read_generic_netcdf.html) will return only one object, a dictionary, that contains all the contents of the NetCDF file corresponding to the original file structure. This includes all the metadata, as well as the so called "dimensions" (describing the dimensions of the actual data arrays) and the "variables" which will contains the actual data. Users can use this dictionary at will in order to query data and metadata; however, they should make sure to consider the documentation of the corresponding data model. [wradlib.io.read_generic_netcdf()](http://wradlib.org/wradlib-docs/latest/generated/wradlib.io.read_generic_netcdf.html) has been shown to work with a lot of different data models, most notably **CfRadial** (see [here](http://www.ral.ucar.edu/projects/titan/docs/radial_formats/cfradial.html) for details). A typical call to [wradlib.io.read_generic_netcdf()](http://wradlib.org/wradlib-docs/latest/generated/wradlib.io.read_generic_netcdf.html) would look like:

# In[ ]:

filename = wrl.util.get_wradlib_data_file('netcdf/example_cfradial_ppi.nc')
outdict = wrl.io.read_generic_netcdf(filename)
for key in outdict.keys():
    print(key)


# Please see [this example notebook](wradlib_generic_netcdf_example.ipynb) to get started.

# ### EDGE NetCDF

# EDGE is a commercial software for radar control and data analysis provided by the Enterprise Electronics Corporation. It allows for netCDF data export. The resulting files can be read by [wradlib.io.read_generic_netcdf()](http://wradlib.org/wradlib-docs/latest/generated/wradlib.io.read_generic_netcdf.html), but $\omega radlib$ also provides a specific function,  [wradlib.io.read_EDGE_netcdf()](http://wradlib.org/wradlib-docs/latest/generated/wradlib.io.read_EDGE_netcdf.html) to return metadata and data as seperate objects:

# In[ ]:

filename = wrl.util.get_wradlib_data_file('netcdf/edge_netcdf.nc') 
data, metadata = wrl.io.read_EDGE_netcdf(filename)
print(data.shape)
print(metadata.keys())


# ## Gematronik Rainbow

# Rainbow refers to the commercial [RAINBOW®5 APPLICATION SOFTWARE](http://www.de.selex-es.com/capabilities/meteorology/products/components/rainbow5) which exports data in an XML flavour, which due to binary data blobs violates XML standard. Gematronik provided python code for implementing this reader in $\omega radlib$, which is very much appreciated.
# 
# The philosophy behind the $\omega radlib$ interface to Gematroniks data model is very straightforward: $\omega radlib$ simply translates the complete xml file structure to *one* dictionary and returns this dictionary to the user. Thus, the potential complexity of the stored data is kept and it is left to the user how to proceed with this data. The keys of the output dictionary are strings that correspond to the "xml nodes" and "xml attributes". Each ``data`` key points to a Dataset (i.e. a numpy array of data). Such a file (typical ending: *.vol* or *.azi*) can be read by:

# In[ ]:

filename = wrl.util.get_wradlib_data_file('rainbow/2013070308340000dBuZ.azi')
fcontent = wrl.io.read_Rainbow(filename)


# The user should inspect the output obtained from his or her Rainbow file in order to see how access those items which should be further processed. In order to get a readable overview of the output dictionary, one can use the pretty printing module:

# In[ ]:

# which keyswords can be used to access the content?
print(fcontent.keys())
# print the entire content including values of data and metadata
# (numpy arrays will not be entirely printed)
print(fcontent['volume']['sensorinfo'])


# You can check this [example notebook](wradlib_load_rainbow_example.ipynb) for getting a first impression.

# ## OPERA BUFR

# **WARNING** $\omega radlib$ does currently not support the BUFR format!
# 
# The Binary Universal Form for the Representation of meteorological data (BUFR) is a binary data format maintained by the World Meteorological Organization (WMO).
# 
# The BUFR format was adopted by [OPERA](https://www.eumetnet.eu/opera) for the representation of weather radar data.
# A BUFR file consists of a set of *descriptors* which contain all the relevant metadata and a data section. 
# The *descriptors* are identified as a tuple of three integers. The meaning of these tupels is described in the so-called BUFR tables. There are generic BUFR tables provided by the WMO, but it is also possible to define so called *local tables* - which was done by the OPERA consortium for the purpose of radar data representation.
#  
# If you want to use BUFR files together with $\omega radlib$, we recommend that you check out the [OPERA software webpage](http://www.eumetnet.eu/opera-software) where you will find software for BUFR decoding. In particular, you might want to check out [this tool](http://www.eumetnet.eu/sites/default/files/bufr-opera-mf-1.21.tar_.gz) which seems to support the conversion of OPERA BUFR files to ODIM_H5 (which is supported by $\omega radlib$). However, you have to build it yourself.
# 
# It would be great if someone could add a tutorial on how to use OPERA BUFR software together with $\omega radlib$!
