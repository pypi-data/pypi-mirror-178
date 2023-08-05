import numpy
import netCDF4
import isodate
import re

from datetime import datetime
from pyproj import CRS

from cfunits import Units
from lxml import etree

from ._ncml_comments import UNITS_WARNING, STANDARD_NAME_WARNING, TEMPORAL_UNITS_WARNING, \
    OPENDAP_RESERVED_KEYWORDS_WARNING, MISSING_VALUES_ERROR, MONOTONIC_VALUES_ERROR, \
    CANT_GET_VALUES_WARNING, MULTIDIMENSIONAL_WARNING, VALID_RANGE_WARNING, FILL_VALUE_WARNING, \
    MISSING_VALUE_WARNING, VARIABLE_NAME_WARNING, BOUNDARY_VARIABLE_ATTRIBUTES_WARNING
from ._constants import CONVENTION_VERSIONS, WARNING_MESSAGE, GLOBAL_ATTRIBUTES, UNITS, \
    OPENDAP_RESERVED_KEYWORDS, VARIABLE_TYPE_INDICATORS, COORDINATE_VARIABLE_LIST
from ._ncml_comments import ADD_GRID_MAPPING_VARIABLE


def _check_variable(variable, variable_values):
    list_of_warnings = []
    rename_variable = False

    if variable.name in OPENDAP_RESERVED_KEYWORDS:
        list_of_warnings.append(OPENDAP_RESERVED_KEYWORDS_WARNING)
        rename_variable = True

    if variable.variable_type in COORDINATE_VARIABLE_LIST:
        warning = _check_coordinate_variables(variable, variable_values)
        for warning_str in warning:
            list_of_warnings.append(warning_str)

    if not bool(re.match('^[A-Za-z0-9_]*$', variable.name)) and variable.name[0].isalpha():
        list_of_warnings.append(VARIABLE_NAME_WARNING)
        rename_variable = True

    if variable.variable_type == VARIABLE_TYPE_INDICATORS['B']:
        if len(variable.attributes) > 0:
            list_of_warnings.append(BOUNDARY_VARIABLE_ATTRIBUTES_WARNING)

    return list_of_warnings, rename_variable


def _check_attribute_values(merged_attributes, variable, standard_name_table, variable_values):
    if 'standard_name' in merged_attributes:
        tree = etree.parse(standard_name_table)
        root = tree.getroot()
        standard_name_element = root.findall('entry[@id="' + merged_attributes['standard_name'] + '"]')

        if merged_attributes['standard_name'] == 'latitude':
            if 'units' in merged_attributes:
                merged_attributes['units'] = 'degrees_north'
            if 'long_name' in merged_attributes:
                if WARNING_MESSAGE in str(merged_attributes['long_name']):
                    merged_attributes['long_name'] = 'Latitudinal Axis'

        elif merged_attributes['standard_name'] == 'longitude':
            if 'units' in merged_attributes:
                merged_attributes['units'] = 'degrees_east'
            if 'long_name' in merged_attributes:
                if WARNING_MESSAGE in str(merged_attributes['long_name']):
                    merged_attributes['long_name'] = 'Longitudinal Axis'

        elif merged_attributes['standard_name'] == 'time':
            if 'units' in merged_attributes:
                if WARNING_MESSAGE in str(merged_attributes['units']):
                    merged_attributes['units'] = {'value': '!!!CHANGE ME!!! - (temporal units) since (date)',
                                                  'comment': TEMPORAL_UNITS_WARNING}
            if 'long_name' in merged_attributes:
                if WARNING_MESSAGE in str(merged_attributes['long_name']):
                    merged_attributes['long_name'] = 'Temporal Axis'

        if len(standard_name_element) > 0:
            standard_name_element = standard_name_element[0]
            standard_units = standard_name_element.findall('canonical_units')

            if len(standard_units) > 0:
                standard_units = Units(standard_units[0].text)

                if 'units' in merged_attributes:
                    if not isinstance(merged_attributes['units'], dict):
                        units = Units(merged_attributes['units'])

                        if not standard_units.equivalent(units) and 'since' not in merged_attributes['units']:
                            if WARNING_MESSAGE not in merged_attributes['units']:
                                merged_attributes['units'] = {'value': str(units),
                                                              'comment': UNITS_WARNING[0] + str(units) +
                                                                         UNITS_WARNING[1] + str(standard_units) +
                                                                         UNITS_WARNING[2]}

        else:
            value = merged_attributes['standard_name']
            if WARNING_MESSAGE not in value:
                merged_attributes['standard_name'] = {'value': value,
                                                      'comment': STANDARD_NAME_WARNING[0] + value +
                                                                 STANDARD_NAME_WARNING[1]}


    if '_FillValue' in merged_attributes:
        if not isinstance(variable_values, numpy.ndarray) or len(variable_values.shape) <= 0:
            del merged_attributes['_FillValue']
        else:
            if type(merged_attributes['_FillValue']) == str:
                if not isinstance(variable_values, numpy.ndarray) or len(variable_values.shape) <= 0:
                    del merged_attributes['_FillValue']
                else:
                    if WARNING_MESSAGE in str(merged_attributes['_FillValue']):
                        merged_attributes['_FillValue'] = variable_values.fill_value

    if 'missing_value' in merged_attributes:
        if not isinstance(variable_values, numpy.ndarray) or len(variable_values.shape) <= 0:
            del merged_attributes['missing_value']
        else:
            if type(merged_attributes['missing_value']) == str:
                if WARNING_MESSAGE in str(merged_attributes['missing_value']):
                    if '_FillValue' in merged_attributes:
                        merged_attributes['missing_value'] = merged_attributes['_FillValue']
                    else:
                        merged_attributes['missing_value'] = variable_values.fill_value

    if 'valid_min' in merged_attributes or 'valid_max' in merged_attributes:
        if 'valid_range' in merged_attributes:
            del merged_attributes['valid_range']

    elif 'valid_range' in merged_attributes:
        if not isinstance(variable_values, numpy.ndarray) or len(variable_values.shape) <= 0:
            del merged_attributes['valid_range']
        else:
            if type(merged_attributes['valid_range']) == str:
                if WARNING_MESSAGE in str(merged_attributes['valid_range']):
                    data_type = variable.data_type
                    change_value = True

                    if numpy.issubdtype(data_type, numpy.integer):
                        data_type = 'int'
                    elif numpy.issubdtype(data_type, numpy.float):
                        data_type = 'float'
                    elif numpy.issubdtype(data_type, numpy.str):
                        data_type = 'str'
                    elif numpy.issubdtype(data_type, numpy.bool):
                        data_type = 'bool'
                    elif numpy.issubdtype(data_type, numpy.complex):
                        data_type = 'complex'
                    else:
                        data_type = 'unknown'

                    if '_FillValue' in merged_attributes:
                        fill_value = merged_attributes['_FillValue']
                    else:
                        fill_value = None

                    if data_type == 'int':
                        if isinstance(fill_value, str):
                            fill_value = int(fill_value)
                        if fill_value is None:
                            valid_min = numpy.iinfo(variable.data_type).min
                            valid_max = numpy.iinfo(variable.data_type).max
                        elif fill_value < 0:
                            valid_min = fill_value + 1
                            valid_max = numpy.iinfo(variable.data_type).max
                        elif fill_value >= 0:
                            valid_min = numpy.iinfo(variable.data_type).min
                            valid_max = fill_value - 1
                    elif data_type == 'float':
                        if isinstance(fill_value, str):
                            fill_value = float(fill_value)
                        if fill_value is None:
                            valid_min = numpy.finfo(variable.data_type).min
                            valid_max = numpy.finfo(variable.data_type).max
                        elif fill_value < 0:
                            valid_min = fill_value + 2 * numpy.finfo(variable.data_type).eps
                            valid_max = numpy.finfo(variable.data_type).max
                        elif fill_value >= 0:
                            valid_min = numpy.finfo(variable.data_type).min
                            valid_max = fill_value - 2 * numpy.finfo(variable.data_type).eps
                    else:
                        change_value = False
                        valid_max = None
                        valid_min = None

                    if change_value:
                        valid_range = [valid_min, valid_max]
                        merged_attributes['valid_range'] = valid_range

    if 'actual_range' in merged_attributes:
        if not isinstance(variable_values, numpy.ndarray) or len(variable_values.shape) <= 0:
            del merged_attributes['actual_range']
        else:
            if type(merged_attributes['actual_range']) == str:
                if WARNING_MESSAGE in str(merged_attributes['actual_range']):
                    actual_min = numpy.nanmin(variable_values[:])
                    actual_max = numpy.nanmax(variable_values[:])

                    merged_attributes['actual_range'] = [actual_min, actual_max]

    if 'valid_range' in merged_attributes and 'actual_range' in merged_attributes:
        if not isinstance(merged_attributes['actual_range'], str) and not \
                isinstance(merged_attributes['valid_range'], str):
            if merged_attributes['actual_range'][0] <= merged_attributes['valid_range'][0] or \
                    merged_attributes['actual_range'][1] >= merged_attributes['valid_range'][1]:
                merged_attributes['valid_range'] = {'value': merged_attributes['valid_range'],
                                                    'comment': VALID_RANGE_WARNING}

    if '_FillValue' in merged_attributes and 'actual_range' in merged_attributes:
        if not isinstance(merged_attributes['_FillValue'], str) and not \
                isinstance(merged_attributes['valid_range'], str):
            if merged_attributes['valid_range'][0] <= merged_attributes['_FillValue'] <= \
                    merged_attributes['valid_range'][1]:
                merged_attributes['_FillValue'] = {'value': merged_attributes['_FillValue'],
                                                   'comment': FILL_VALUE_WARNING}

    if 'missing_value' in merged_attributes and 'actual_range' in merged_attributes:
        if not isinstance(merged_attributes['missing_value'], str) and not \
                isinstance(merged_attributes['valid_range'], str):
            if merged_attributes['valid_range'][0] <= merged_attributes['missing_value'] <= merged_attributes['valid_range'][1]:
                merged_attributes['missing_value'] = {'value': merged_attributes['missing_value'],
                                                    'comment': MISSING_VALUE_WARNING}

    return merged_attributes


def _check_coordinate_variables(variable, variable_values):
    warning_list = []
    if variable_values is not None:
        if len(variable_values.shape) == 1:
            array_sum = numpy.sum(variable_values)
            if numpy.isnan(array_sum) or numpy.ma.is_masked(variable_values):
                warning_list.append(f'{MISSING_VALUES_ERROR[0]}{variable.name}{MISSING_VALUES_ERROR[1]}')
            if not numpy.all(variable_values[1:] > variable_values[:-1], axis=0) and not numpy.all(variable_values[1:] < variable_values[:-1], axis=0):
                warning_list.append(f'{MONOTONIC_VALUES_ERROR[0]}{variable.name}{MONOTONIC_VALUES_ERROR[1]}')
        else:
            warning_list.append(f'{MULTIDIMENSIONAL_WARNING}')
    else:
        warning_list.append(f'{CANT_GET_VALUES_WARNING[0]}{variable.name}{CANT_GET_VALUES_WARNING[1]}')
    return warning_list


def _check_spatial_variables(variable_ordered_dictionary):
    spatial_list = []
    georeferenced_dict = {}
    warning_list = []
    list_of_domains = []
    named_variable_dict = {}

    for variable in variable_ordered_dictionary:
        named_variable_dict[variable.name] = variable
        condition_y = variable.variable_type == VARIABLE_TYPE_INDICATORS['Y']
        condition_x = variable.variable_type == VARIABLE_TYPE_INDICATORS['X']
        condition_g = variable.variable_type == VARIABLE_TYPE_INDICATORS['G']
        condition_gd = variable.variable_type == VARIABLE_TYPE_INDICATORS['GD']

        if condition_y or condition_x or condition_g or condition_gd:
            if condition_y or condition_x or condition_g:
                spatial_list.append(variable.name)
            elif condition_gd:
                georeferenced_dict[variable.name] = variable

    for variable_name in georeferenced_dict:
        variable = georeferenced_dict[variable_name]
        new_domain_list = []
        for dimension in variable.dimensions:
            if dimension in spatial_list:
                new_domain_list.append(dimension)
        if 'coordinates' in variable.attributes:
            for coordinate in variable.attributes['coordinates'].split(' '):
                if coordinate != '':
                    if coordinate in spatial_list:
                        if coordinate not in new_domain_list:
                            new_domain_list.append(coordinate)
        if 'grid_mapping' in variable.attributes:
            if variable.attributes['grid_mapping'] != '':
                if variable.attributes['grid_mapping'] in spatial_list:
                    if variable.attributes['grid_mapping'] not in new_domain_list:
                        new_domain_list.append(variable.attributes['grid_mapping'])

        if len(new_domain_list) > 0:
            new_domain_list.sort()
            if len(list_of_domains) == 0:
                list_of_domains.append(new_domain_list)
            else:
                if new_domain_list not in list_of_domains:
                    list_of_domains.append(new_domain_list)

    for domain in list_of_domains:
        has_lat = False
        has_lon = False
        has_grid_mapping = False
        has_proj_x = False
        has_proj_y = False

        for variable_name in domain:
            variable = named_variable_dict[variable_name]
            if variable.variable_type == VARIABLE_TYPE_INDICATORS['Y']:
                if 'standard_name' in variable.attributes:
                    if variable.attributes['standard_name'] == 'latitude' or variable.attributes[
                        'standard_name'] == 'grid_latitude':
                        has_lat = True
                    elif variable.attributes['standard_name'] == 'projection_y_coordinate' or variable.attributes[
                        'standard_name'] == 'projection_y_angular_coordinate':
                        has_proj_y = True
                elif 'units' in variable.attributes:
                    if variable.attributes['units'] in UNITS:
                        has_lat = True
                else:
                    has_proj_y = True
            elif variable.variable_type == VARIABLE_TYPE_INDICATORS['X']:
                if 'standard_name' in variable.attributes:
                    if variable.attributes['standard_name'] == 'longitude' or variable.attributes[
                        'standard_name'] == 'grid_longitude':
                        has_lon = True
                    elif variable.attributes['standard_name'] == 'projection_x_coordinate' or variable.attributes[
                        'standard_name'] == 'projection_x_angular_coordinate':
                        has_proj_x = True
                elif 'units' in variable.attributes:
                    if variable.attributes['units'] in UNITS:
                        has_lon = True
                else:
                    has_proj_x = True
            elif variable.variable_type == VARIABLE_TYPE_INDICATORS['G']:
                has_grid_mapping = True

        condition_1 = has_proj_y and has_proj_x
        condition_2 = not has_grid_mapping
        condition_3 = not has_lat and not has_lon
        if condition_1 and condition_2 and condition_3:
            warning_list.append(ADD_GRID_MAPPING_VARIABLE)

    return warning_list


def _fill_global_attributes(required_attributes, dataset):
    crs = None
    x_dim = None
    y_dim = None
    z_dim = None
    t_dim = None

    if 'date_metadata_modified' in required_attributes:
        if WARNING_MESSAGE in str(required_attributes['date_metadata_modified']):
            required_attributes['date_metadata_modified'] = datetime.utcnow().replace(microsecond=0).isoformat()

    if 'history' in required_attributes:
        date = datetime.utcnow().replace(microsecond=0).isoformat()
        if WARNING_MESSAGE in str(required_attributes['history']):
            required_attributes['history'] = f'{date}, Metadata updated using cfbuild python package'
        else:
            required_attributes['history'] += f'; {date}, Metadata updated using cfbuild python package'

    if 'geospatial_bounds_crs' in required_attributes:
        if dataset.crs is not None and dataset.crs != '':
            if str(dataset.crs).isdigit():
                if len(str(dataset.crs)) == 4 or len(str(dataset.crs)) == 5:
                    crs = f'EPSG:{dataset.crs}'
                else:
                    crs = None
            elif str(dataset.crs)[:4].upper() == 'EPSG':
                crs = dataset.crs.upper()
            else:
                crs = None

            if crs is not None:
                required_attributes['geospatial_bounds_crs'] = crs

        elif WARNING_MESSAGE in str(required_attributes['geospatial_bounds_crs']):
            grid_mapping_variable = None

            for variable in dataset.variables:
                if dataset.variables[variable].variable_type == VARIABLE_TYPE_INDICATORS['G']:
                    grid_mapping_variable = dataset.variables[variable]

            if grid_mapping_variable is not None:
                attributes = grid_mapping_variable.attributes

                for attribute in attributes:
                    if attributes[attribute].isdigit():
                        attributes[attribute] = int(attributes[attribute])
                    else:
                        try:
                            attributes[attribute] = float(attributes[attribute])
                        except:
                            attributes[attribute] = attributes[attribute]

                if 'grid_mapping_name' in attributes:
                    if attributes['grid_mapping_name'] == 'latitude_longitude':
                        crs = 'EPSG:4326'
                    else:
                        crs = CRS.from_cf(attributes).to_epsg()
                else:
                    crs = 'EPSG:4326'

            if crs is None:
                required_attributes['geospatial_bounds_crs'] = 'EPSG:4326'
            else:
                required_attributes['geospatial_bounds_crs'] = crs

    if 'geospatial_bounds' in required_attributes:
        if WARNING_MESSAGE in str(required_attributes['geospatial_bounds']):

            for variable in dataset.variables:
                if dataset.variables[variable].variable_type == VARIABLE_TYPE_INDICATORS['X']:
                    x_dim = dataset.variables[variable]
                elif dataset.variables[variable].variable_type == VARIABLE_TYPE_INDICATORS['Y']:
                    y_dim = dataset.variables[variable]

            if x_dim is not None and y_dim is not None:
                try:
                    if x_dim.values is None:
                        x_values = dataset.dataset.variables[x_dim.name][:]
                    else:
                        x_values = x_dim.values

                    if y_dim.values is None:
                        y_values = dataset.dataset.variables[y_dim.name][:]
                    else:
                        y_values = y_dim.values

                    x_min = numpy.nanmin(x_values)
                    x_max = numpy.nanmax(x_values)
                    y_min = numpy.nanmin(y_values)
                    y_max = numpy.nanmax(y_values)
                    x_resolution = abs(numpy.mean(x_values[1:] - x_values[:-1]))
                    y_resolution = abs(numpy.mean(y_values[1:] - y_values[:-1]))

                    if crs == 'EPSG:4326':
                        if x_max > 180:
                            x_max = x_max - 360
                        if x_min > 180:
                            x_min = x_min - 360
                        if y_max > 90:
                            y_max = x_max - 180
                        if y_min > 90:
                            y_min = x_min - 180

                    wkt_string = f'POLYGON (({y_min} {x_min}, {y_max} {x_min}, {y_max} {x_max}, {y_min} {x_max}, ' \
                                 f'{y_min} {x_min}))'

                    required_attributes['geospatial_bounds'] = wkt_string

                    if 'geospatial_lon_min' in required_attributes:
                        if WARNING_MESSAGE in str(required_attributes['geospatial_lon_min']):
                            required_attributes['geospatial_lon_min'] = x_min
                    if 'geospatial_lat_min' in required_attributes:
                        if WARNING_MESSAGE in str(required_attributes['geospatial_lat_min']):
                            required_attributes['geospatial_lat_min'] = y_min
                    if 'geospatial_lon_max' in required_attributes:
                        if WARNING_MESSAGE in str(required_attributes['geospatial_lon_max']):
                            required_attributes['geospatial_lon_max'] = x_max
                    if 'geospatial_lat_max' in required_attributes:
                        if WARNING_MESSAGE in str(required_attributes['geospatial_lat_max']):
                            required_attributes['geospatial_lat_max'] = y_max
                    if 'geospatial_lon_resolution' in required_attributes:
                        if WARNING_MESSAGE in str(required_attributes['geospatial_lon_resolution']):
                            required_attributes['geospatial_lon_resolution'] = x_resolution
                    if 'geospatial_lat_resolution' in required_attributes:
                        if WARNING_MESSAGE in str(required_attributes['geospatial_lat_resolution']):
                            required_attributes['geospatial_lat_resolution'] = y_resolution
                    if 'units' in x_dim.attributes:
                        if 'geospatial_lon_units' in required_attributes:
                            if WARNING_MESSAGE in str(required_attributes['geospatial_lon_units']):
                                required_attributes['geospatial_lon_units'] = x_dim.attributes['units']
                    if 'units' in y_dim.attributes:
                        if 'geospatial_lat_units' in required_attributes:
                            if WARNING_MESSAGE in str(required_attributes['geospatial_lat_units']):
                                required_attributes['geospatial_lat_units'] = y_dim.attributes['units']

                except Exception:
                    pass

            else:
                if 'geospatial_lat_max' in required_attributes:
                    required_attributes.pop('geospatial_lat_max')
                if 'geospatial_lon_max' in required_attributes:
                    required_attributes.pop('geospatial_lon_max')
                if 'geospatial_lat_units' in required_attributes:
                    required_attributes.pop('geospatial_lat_units')
                if 'geospatial_lon_units' in required_attributes:
                    required_attributes.pop('geospatial_lon_units')
                if 'geospatial_lat_resolution' in required_attributes:
                    required_attributes.pop('geospatial_lat_resolution')
                if 'geospatial_lon_resolution' in required_attributes:
                    required_attributes.pop('geospatial_lon_resolution')
                if 'geospatial_bounds' in required_attributes:
                    required_attributes.pop('geospatial_bounds')
                if 'geospatial_bounds_crs' in required_attributes:
                    required_attributes.pop('geospatial_bounds_crs')

    for variable in dataset.variables:
        if dataset.variables[variable].variable_type == VARIABLE_TYPE_INDICATORS['Z']:
            z_dim = dataset.variables[variable]

    if z_dim is not None:
        try:
            if z_dim.values is None:
                z_values = dataset.dataset.variables[z_dim.name][:]
            else:
                z_values = z_dim.values

            z_max = numpy.nanmax(z_values)
            z_min = numpy.nanmin(z_values)
            z_resolution = abs(numpy.mean(z_values[1:] - z_values[:-1]))

            if 'positive' in z_dim.attributes:
                if 'geospatial_vertical_positive' in required_attributes:
                    if WARNING_MESSAGE in str(required_attributes['geospatial_vertical_positive']):
                        required_attributes['geospatial_vertical_positive'] = z_dim.attributes['positive']

            if 'units' in z_dim.attributes:
                if 'geospatial_vertical_units' in required_attributes:
                    if WARNING_MESSAGE in str(required_attributes['geospatial_vertical_units']):
                        required_attributes['geospatial_vertical_units'] = z_dim.attributes['units']

            if 'geospatial_vertical_min' in required_attributes:
                if WARNING_MESSAGE in str(required_attributes['geospatial_vertical_min']):
                    required_attributes['geospatial_vertical_min'] = z_min

            if 'geospatial_vertical_max' in required_attributes:
                if WARNING_MESSAGE in str(required_attributes['geospatial_vertical_max']):
                    required_attributes['geospatial_vertical_max'] = z_max

            if 'geospatial_vertical_resolution' in required_attributes:
                if WARNING_MESSAGE in str(required_attributes['geospatial_vertical_resolution']):
                    required_attributes['geospatial_vertical_resolution'] = z_resolution

        except Exception:
            pass

    else:
        if 'geospatial_vertical_max' in required_attributes:
            required_attributes.pop('geospatial_vertical_max')
        if 'geospatial_vertical_min' in required_attributes:
            required_attributes.pop('geospatial_vertical_min')
        if 'geospatial_vertical_positive' in required_attributes:
            required_attributes.pop('geospatial_vertical_positive')
        if 'geospatial_bounds_vertical_crs' in required_attributes:
            required_attributes.pop('geospatial_bounds_vertical_crs')
        if 'geospatial_vertical_units' in required_attributes:
            required_attributes.pop('geospatial_vertical_units')
        if 'geospatial_vertical_resolution' in required_attributes:
            required_attributes.pop('geospatial_vertical_resolution')

    for variable in dataset.variables:
        if dataset.variables[variable].variable_type == VARIABLE_TYPE_INDICATORS['T']:
            t_dim = dataset.variables[variable]

    if t_dim is not None:
        try:
            if t_dim.values is None:
                t_values = dataset.dataset.variables[t_dim.name][:]
            else:
                t_values = t_dim.values

            if 'units' in t_dim.attributes:
                t_units = t_dim.attributes['units']
            else:
                t_units = None
            if 'calendar' in t_dim.attributes:
                t_calendar = t_dim.attributes['calendar']
            else:
                t_calendar = 'standard'

            if t_units is not None:
                t_max_num = numpy.nanmax(t_values)
                t_min_num = numpy.nanmin(t_values)
                t_difference_num = abs(numpy.mean(t_values[1:] - t_values[:-1]))

                t_max_date = netCDF4.num2date(t_max_num, t_units, t_calendar)
                t_min_date = netCDF4.num2date(t_min_num, t_units, t_calendar)
                t_difference_date = netCDF4.num2date(t_difference_num, t_units, t_calendar)

                t_max_string = t_max_date.replace(microsecond=0).isoformat()
                t_min_string = t_min_date.replace(microsecond=0).isoformat()
                t_duration_string = isodate.duration_isoformat(t_max_date - t_min_date)
                t_resolution_string = isodate.duration_isoformat(t_difference_date - t_min_date)

                if 'time_coverage_start' in required_attributes:
                    if WARNING_MESSAGE in str(required_attributes['time_coverage_start']):
                        required_attributes['time_coverage_start'] = t_min_string

                if 'time_coverage_end' in required_attributes:
                    if WARNING_MESSAGE in str(required_attributes['time_coverage_end']):
                        required_attributes['time_coverage_end'] = t_max_string

                if 'time_coverage_duration' in required_attributes:
                    if WARNING_MESSAGE in str(required_attributes['time_coverage_duration']):
                        required_attributes['time_coverage_duration'] = t_duration_string

                if 'time_coverage_resolution' in required_attributes:
                    if WARNING_MESSAGE in str(required_attributes['time_coverage_resolution']):
                        required_attributes['time_coverage_resolution'] = t_resolution_string

        except Exception:
            pass

    else:
        if 'time_coverage_start' in required_attributes:
            required_attributes.pop('time_coverage_start')
        if 'time_coverage_end' in required_attributes:
            required_attributes.pop('time_coverage_end')
        if 'time_coverage_duration' in required_attributes:
            required_attributes.pop('time_coverage_duration')
        if 'time_coverage_resolution' in required_attributes:
            required_attributes.pop('time_coverage_resolution')

    return required_attributes


def _determine_global_attributes_for_given_conventions(conventions, current_conventions, group):
    append_convention = True
    if CONVENTION_VERSIONS[0] in conventions and not CONVENTION_VERSIONS[1] in conventions:
        required_attributes = GLOBAL_ATTRIBUTES['CF_GLOBAL_ATTRIBUTES']

        for convention in current_conventions:

            if 'CF' in convention:
                list_index = current_conventions.index(convention)
                current_conventions = current_conventions[:list_index] + [
                    CONVENTION_VERSIONS[0]] + current_conventions[list_index + 1:]
                append_convention = False

        if append_convention:
            current_conventions.append(CONVENTION_VERSIONS[0])

        group.attributes['Conventions'] = ', '.join(current_conventions)

    elif CONVENTION_VERSIONS[1] in conventions and not CONVENTION_VERSIONS[0] in conventions:
        GLOBAL_ATTRIBUTES['ACDD_ATTRIBUTES']['date_created'] = datetime.now().strftime("%m/%d/%Y")
        required_attributes = GLOBAL_ATTRIBUTES['ACDD_ATTRIBUTES']

        for convention in current_conventions:

            if 'ACDD' in convention:
                list_index = current_conventions.index(convention)
                current_conventions = current_conventions[:list_index] + [
                    CONVENTION_VERSIONS[1]] + current_conventions[list_index + 1:]
                append_convention = False

        if append_convention:
            current_conventions.append(CONVENTION_VERSIONS[1])

        group.attributes['Conventions'] = ', '.join(current_conventions)

    else:
        required_attributes = {**GLOBAL_ATTRIBUTES['CF_GLOBAL_ATTRIBUTES'], **GLOBAL_ATTRIBUTES['ACDD_ATTRIBUTES'],}

        for convention in current_conventions:
            if 'ACDD' in convention or 'CF' in convention:
                if 'ACDD' in convention:
                    list_index = current_conventions.index(convention)
                    current_conventions = current_conventions[:list_index] + [CONVENTION_VERSIONS[1]] + \
                                          current_conventions[list_index + 1:]
                    append_convention = True
                if 'CF' in convention:
                    list_index = current_conventions.index(convention)
                    current_conventions = current_conventions[:list_index] + [CONVENTION_VERSIONS[0]] + \
                                          current_conventions[list_index + 1:]
                    append_convention = True

        if append_convention:
            for convention in CONVENTION_VERSIONS:
                if convention not in current_conventions:
                    current_conventions.append(convention)

        group.attributes['Conventions'] = ', '.join(current_conventions)

    return required_attributes
