import nose.tools
from tests.common import WpsTestClient

def test_caps():
    wps = WpsTestClient()
    resp = wps.get(service='wps', request='getcapabilities')
    names = resp.xpath_text('/wps:Capabilities'
                            '/wps:ProcessOfferings'
                            '/wps:Process'
                            '/ows:Identifier')
    sorted_names = sorted(names.split())
    expected_names = ['cdo_operation', 'cdo_sinfo', 'cfchecker', 'ensembles', 'ioos_cchecker', 'ncmeta', 'qa_cfchecker', 'qa_checker', 'simple_plot', 'tika']
    nose.tools.ok_(sorted_names == expected_names, sorted_names)

