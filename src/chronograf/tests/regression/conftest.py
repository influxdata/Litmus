
import pytest
from src.chronograf.lib import rest_lib

@pytest.fixture(scope='class')
def get_all_paths(request, base_url):
    rl=rest_lib.RestLib(request.cls.mylog)
    request.cls.mylog.info('get_all_paths() FIXTURE IS CALLED')
    response=rl.get_chronograf_paths(base_url)
    request.cls.get_all_paths=response
    request.cls.mylog.info('get_all_paths() FIXTURE IS DONE')
    return request.cls.get_all_paths

@pytest.fixture(scope='class')
def get_source_path(request, base_url):
    request.cls.mylog.info('get_source_path() FIXTURE IS CALLED')
    request.cls.mylog.info('get_source_path() CALL get_all_paths() FIXTURE')
    source_path=get_all_paths(request, base_url)['sources']
    assert source_path is not None, request.cls.mylog.info('get_source_path() ASSERTION ERROR')
    request.cls.mylog.info('get_source_path() source_path=' + str(source_path))
    request.cls.get_source_path=source_path
    request.cls.mylog.info('get_source_path() FIXTURE IS DONE')
    return request.cls.get_source_path

@pytest.fixture(scope='class')
def delete_sources(request,base_url):
    rl=rest_lib.RestLib(request.cls.mylog)
    request.cls.mylog.info('delete_sources() FIXTURE IS CALLED')
    request.cls.mylog.info('delete_sources() : GET ALL OF THE SOURCES')
    source_path=get_source_path(request, base_url)
    sources=rl.get_sources(base_url, source_path)
    for source in sources.keys():
        request.cls.mylog.info('delete_sources() : DELETING SOURCE ID=' + str(source))
        rl.delete_source(base_url, source_path, source)
    request.cls.mylog.info('delete_sources() IS DONE')


