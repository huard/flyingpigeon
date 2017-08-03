
from os import listdir
from os import path

from ocgis import RequestDataset, OcgOperations
from ocgis.constants import DimensionMapKey

p = '/home/nils/birdhouse/var/lib/pywps/cache/malleefowl/esgf1.dkrz.de/thredds/fileServer/cordex/cordex/output/AFR-44/MPI-CSC/MPI-M-MPI-ESM-LR/historical/r1i1p1/MPI-CSC-REMO2009/v1/day/tas/v20160412/'

ncs = [path.join(p, nc) for nc in listdir(p)]
ncs.sort()
rd = RequestDataset(ncs[0])
indice = 'TG'
geom = OcgOperations(rd,
                     calc=[{'func': 'icclim_' + indice, 'name': indice}],
                     calc_grouping=['year', 'month'],
                     prefix='single_file',
                     output_format='nc').execute()
print geom

rd = RequestDataset(ncs)
rd.dimension_map.set_bounds(DimensionMapKey.TIME, None)
indice = 'TG'
geom = OcgOperations(rd,
                     calc=[{'func': 'icclim_' + indice, 'name': indice}],
                     calc_grouping=['year', 'month'],
                     prefix='multi_file',
                     output_format='nc').execute()
print geom

from flyingpigeon.indices import calc_indice_simple

fp_indice = calc_indice_simple(resource=ncs, variable=None, prefix=None, indice='TG',
                               polygons=['CMR'], mosaic=True, grouping='yr', dir_output=None,
                               dimension_map=None, memory_limit=None)

print fp_indice
