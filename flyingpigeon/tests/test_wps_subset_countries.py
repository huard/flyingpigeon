import pytest

from .common import WpsTestClient, TESTDATA, assert_response_success

@pytest.mark.skip(reason="no way of currently testing this")
def test_wps_subset_countries():
    wps = WpsTestClient()
    datainputs = "[resource={0};region=CAN;mosaic=False]".format(
        TESTDATA['cmip5_tasmax_2006_nc'])
    resp = wps.get(service='wps', request='execute', version='1.0.0',
                   identifier='subset_countries',
                   datainputs=datainputs)
    assert_response_success(resp)