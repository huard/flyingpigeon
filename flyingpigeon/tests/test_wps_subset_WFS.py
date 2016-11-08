import pytest

from .common import WpsTestClient, TESTDATA, assert_response_success

def test_wps_subset_WFS():
    wps = WpsTestClient()
    datainputs = "[resource={0};typename=usa:states;featureids=states.11,states.49;mosaic=False]".format(
       TESTDATA['cmip5_tasmax_2006_nc'])
    resp = wps.get(service='wps', request='execute', version='1.0.0',
                   identifier='subset_WFS',
                   datainputs=datainputs)
    assert_response_success(resp)