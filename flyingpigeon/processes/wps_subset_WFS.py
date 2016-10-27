import os

from flyingpigeon.subset import clipping
from pywps.Process import WPSProcess
from owslib.wfs import WebFeatureService
from owslib.fes import *
from owslib.etree import etree

import logging
logger = logging.getLogger(__name__)


class WFSClippingProcess(WPSProcess):
    def __init__(self):
        WPSProcess.__init__(
            self, 
            identifier="subset_WFS",
            title="Subset WFS",
            version="0.1",
            abstract="Fetch a shapefile from a WFS server and clip each input dataset with all the polygons it contains",
            statusSupported=True,
            storeSupported=True
            )

        self.resource = self.addComplexInput(
            identifier="resource",
            title="Resource",
            abstract="NetCDF File",
            minOccurs=1,
            maxOccurs=1000,
            maxmegabites=5000,
            formats=[{"mimeType":"application/x-netcdf"}],
            )
       
        self.typenames = self.addLiteralInput(
            identifier="typenames",
            title="TypeNames",
            abstract="Target layer",
            type=type(''),
            minOccurs=1,
            maxOccurs=1
            )
        
        self.cql = self.addLiteralInput(
            identifier="cql",
            title="CQL filters",
            abstract="The command that selects only a subset of the polygons in the target layer",
            type=type(''),
            minOccurs=1,
            maxOccurs=1
            )

        self.variable = self.addLiteralInput(
            identifier="variable",
            title="Variable",
            abstract="Variable to be expected in the input files (Variable will be detected if not set)",
            default=None,
            type=type(''),
            minOccurs=0,
            maxOccurs=1,
            )

        self.mosaic = self.addLiteralInput(
            identifier="mosaic",
            title="Mosaic",
            abstract="If Mosaic is checked, selected polygons will be merged to one Mosaic for each input file",
            default=False,
            type=type(False),
            minOccurs=0,
            maxOccurs=1,
        )

        # self.output = self.addComplexOutput(
        #     title="Subsets",
        #     abstract="Tar archive containing the netCDF files",
        #     formats=[{"mimeType":"application/x-tar"}],
        #     asReference=True,
        #     identifier="output",
        #     )
        #
        # self.output_netcdf = self.addComplexOutput(
        #     title="Subsets for one dataset",
        #     abstract="NetCDF file with subsets of one dataset.",
        #     formats=[{"mimeType":"application/x-netcdf"}],
        #     asReference=True,
        #     identifier="ncout",
        #     )

    def execute(self):
        urls = self.getInputValues(identifier='resource')
        mosaic = self.mosaic.getValue()
        cql = self.cql.getValue()
        typenames = self.typenames.getValue()

        logger.info('urls = %s', urls)
        logger.info('cql = %s', cql)
        logger.info('mosaic = %s', mosaic)
        logger.info('typenames = %s', typenames)
    
        self.status.set('Arguments set for WPS subset process', 0)
        logger.debug('starting: num_files=%s' % (len(urls)))

        try:
            #results = clipping(
            #    resource = urls,
            #    polygons = regions, # self.region.getValue(),
            #    mosaic = mosaic,
            #    spatial_wrapping='wrap',
            #    variable = variable,
            #    dir_output = os.path.abspath(os.curdir),
            #    )

            #Get the data
            wfs = WebFeatureService("http://132.217.140.48:8080/geoserver/wfs", "1.1.0")
            filterprop = PropertyIsLike(propertyname='STATE_NAME', literal='TEXAS', wildCard='*')
            filterxml = etree.tostring(filterprop.toXML()).decode("utf-8")
            polygons = wfs.getfeature(typename='usa:states', filter=filterxml, outputFormat='shape-zip')

            #Saves the result
            out = open('/mnt/shared/data.zip', 'wb')
            out.write(bytes(polygons.read()))
            out.close()

            results = True
            logger.info('Done')
        except Exception as e:
            msg = 'WPS clipping failed'
            logger.exception(msg)
            raise Exception(msg)

        if not results:
            raise Exception('no results produced.')

        #self.output.setValue("")
        #self.output_netcdf.setValue("")
        self.status.set('done', 100)
