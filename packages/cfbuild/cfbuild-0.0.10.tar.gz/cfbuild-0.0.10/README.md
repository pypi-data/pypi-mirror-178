# CFBUILD

## Building CF Compliant netCDF files
This package is designed to help update or build netCDF datasets so that 
they are compliant with the Attribute Conventions for Data Discovery (ACDD)
and the Climate and Forecast (CF) Conventions. It is built to work with multidimensional
geo-referenced datasets but may be used on any netCDF file. No guarantee is given as to 
the accuracy of the updated datasets and user discretion is advised.

### Installation
To install cfbuild run `pip install cfbuild` in your terminal.

Cfbuild requires the udunits2 library which can be
installed via conda with: `conda install -c conda-forge udunits2`

### Dependencies
* netCDF4
* pyproj
* cfunits
* isodate
* lxml

### Documentation
Read the documentation here: https://cfbuild.readthedocs.io/en/latest/

### Classes and Functions

`cfbuild.Dataset(dataset_or_filepath, conventions)`

>**dataset_or_filepath**: str - An OPeNDAP url or the path to a netCDF file.<br>
>**conventions**: str or list - One or both of ['CF-1.9', 'ACDD-1.3'].

`cfbuild.Dataset.to_ncml(output_filepath)`
>**output_filepath**: str - A filepath where an ncml file will be created which 
>describes the cfbuild dataset

`cfbuild.Dataset.crs(epsg_number)`
>**epsg_number**: str or int - An EPSG number that defines the coordinate reference system for the dataset.

`cfbuild.Dataset.close()`
>Close the dataset.

`cfbuild.Dataset.group(name)`
>**name**: str - The name of the group to be created in the cfbuild dataset.

`cfbuild.Dataset.variable(name, data_type, dimensions, variable_type, values)`
>**name**: str - The name of the variable to be created in the cfbuild dataset.<br>
>**data_type**: str - The data type of the variable.<br>
>**dimensions**: tuple - The dimensions associated with the variable.<br>
>**variable_type**: str - The Climate and Forecast Convention variable type for the variable. One of Coordinate,
>Time Coordinate, X Coordinate, Y Coordinate, Z Coordinate', Auxiliary Coordinate',
>Georeferenced Data Variable, Data Variable, Ancillary Data Variable,
>Scalar Coordinate, Grid Mapping Variable, Domain Variable, Boundary Variable, Cell Measures Variable.<br>
>**values**: numpy.array - An array of values for the variable.

`cfbuild.Dataset.dimension(name, length)`
>**name**: str - The name of the dimension to be created in the cfbuild dataset.<br>
>**length**: int or None - The length of the dimension. Use None for an unlimited dimension.

`cfbuild.Dataset.attribute(name, value)`
>**name**: str - The name of the attribute to be created for dataset.<br>
>**value**: str - The value of the attribute.<br>

`cfbuild.NCML(ncml_filepath, dataset)`
>**ncml_filepath**: str - A path to an ncml file used to configure the new dataset.<br>
>**dataset**: cfbuild.Dataset - A dataset created using cfbild.Dataset().

`cfbuild.NCML.to_nc(nc_filepath, write_mode)`
>**nc_filepath**: str - A path to the new netCDF dataset that will be created.
>**writ_mode**: str - w or clobber. w will write to a new dataset but will raise an error if a dataset with the same name 
>already exists. clobber uses the netCDF4 clobber function.

### Tutorial

#### Build a dataset
Import the necessary packages
```python
import cfbuild
import numpy as np
```

Create a new dataset. Add dimensions and variables to the dataset.
```python
ds = cfbuild.Dataset()

time_dimension = ds.dimension('time', None)
lat_dimension = ds.dimension('lat', 181)
lon_dimension = ds.dimension('lon', 361)

time_variable = ds.variable('time', 'int32', ('time',), values=np.arange(0, 20, 1, dtype='int32'))
lat_variable = ds.variable('lat', 'int32', ('lat',), values=np.arange(-90, 90, 1, dtype='int32'))
lon_variable = ds.variable('lon', 'int32', ('lon',), values=np.arange(-180, 180, 1, dtype='int32'))

data_variable = ds.variable('data', 'float64', ('time', 'lat', 'lon',))
data_variable.values = np.random.rand(20,181,361)
```

Specify the variable type for each variable.
```python
time_variable.variable_type = 'Time Coordinate'
lat_variable.variable_type = 'Y Coordinate'
lon_variable.variable_type = 'X Coordinate'
data_variable.variable_type = 'Georeferenced Data Variable'
```

Convert the dataset to an ncml file and generate the needed metadata.
```python
ncml = ds.to_ncml('foo/foo/path_to_ncml.nc')
```

Open the ncml file and edit the metadata. Once the metadata is edited to your
satisfaction, convert it to a netCDF file.
```python
ncml.to_nc('foo/foo/path_to_netCDF_file.nc')
```

#### Update a dataset
Import the necessary packages
```
import cfbuild
```

Create a new dataset. Add dimensions and variables to the dataset.
```python
ds = cfbuild.Dataset('foo/foo/path_to_netCDF_file.nc')
ncml = ds.to_ncml('foo/foo/path_to_ncml.nc')
```

Open the ncml file and edit the metadata. Once the metadata is edited to your
satisfaction, convert it to a netCDF file.
```python
ncml.to_nc('foo/foo/path_to_netCDF_file.nc')
```

If you have a bunch of datasets with the same data structure that need to be updated:
create and ncml file following the same instructions previously listed, create
a cfbuild.Dataset object from the dataset that needs to be updated, create a
cfbuild.NCML object using the dataset just created and the path to the ncml file, and 
create a new dataset.

```python
ds = cfbuild.Dataset('foo/foo/path_to_netCDF_file.nc')
ncml = cfbuild.NCML('foo/foo/path_to_ncml.nc', ds)
ncml.to_nc('foo/foo/path_to_new_netCDF_file.nc')
```

### Issues and bugs
If you encounter an issue while using this package, please recorde it in the issues
tab of the github repository: https://github.com/jenochjones/cfbuild/issues. 

### Notes
Modify the ncml file to modify the resulting dataset.

Change a variable name:
```xml
<variable name="time" orgName="t" />
```

Replace values in a variable:
```xml
<values start="0" incr="2.25" />
```