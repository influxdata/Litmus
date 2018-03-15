
import pytest
from src.chronograf.lib import rest_lib

#base_url='http://34.217.41.106:8888'

@pytest.fixture(scope='class')
def delete_sources(request,base_url):
    rl=rest_lib.RestLib(request.cls.mylog)
    request.cls.mylog.info('fixture.delete_sources() is being called')
    request.cls.mylog.info('fixture.delete_sources() : Get all of the sources')
    sources=rl.get_sources(base_url)
    for source in sources.keys():
        request.cls.mylog.info('fixture.delete_sources() : Deleting Source ID=' + str(source))
        rl.delete_source(base_url, source)
    request.cls.mylog.info('fixture.delete_sources() is done')

@pytest.fixture(scope='class')
def get_all_paths(request, base_url):
    rl=rest_lib.RestLib(request.cls.mylog)
    request.cls.mylog.info('get_all_paths() FIXTURE IS BEING CALLED')
    response=rl.get_chronograf_paths(base_url)
    request.cls.get_all_paths=response
    return request.cls.get_all_paths
