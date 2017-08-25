import pytest

from pywps import Service
from pywps.tests import assert_response_success

from common import TESTDATA, client_for
from flyingpigeon.processes.wps_ocgis_func import *

def test_wps_FreezeThaw():
    client = client_for(Service(processes=[FreezeThawProcess(),]))
    datainputs = "resource=files@xlink:href={0};grouping={1};threshold={2}".format(
        TESTDATA['cmip3_tas_sresb1_da_nc'], 'yr', 10.)
    #datainputs = "resource=files@xlink:href={0};grouping={1};threshold={2}".format(TESTDATA['cmip5_tasmax_2006_nc'], 'yr', 5)
    resp = client.get(
        service='WPS', request='Execute', version='1.0.0',
        identifier='freezethaw',
        datainputs=datainputs)
    assert_response_success(resp)

def test_wps_ICCLIM_TX():
    client = client_for(Service(processes=[ICCLIM_TXProcess(),]))
    datainputs = "resource=files@xlink:href={0};grouping={1}".format(TESTDATA['cmip3_tas_sresb1_da_nc'], 'yr')
    resp = client.get(
        service='WPS', request='Execute', version='1.0.0',
        identifier='icclim_TX',
        datainputs=datainputs)
    assert_response_success(resp)


#test_wps_FreezeThaw()