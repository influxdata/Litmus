
import pytest
from src.chronograf.lib import rest_lib

@pytest.fixture(scope='class')
def get_all_paths(request, chronograf):
    '''
    :param request:request object to introspect the rtequesting test function, class or module context
    :param chronograf:Chronograf URL, e.g. http://<ID>:<PORT>, where port is 8888
    :return:all of the paths:
            me --> /chronograf/v1/me
            organizations --> /chronograf/v1/organizations
            users --> /chronograf/v1/organizations/default/users
            allUsers --> /chronograf/v1/users
            dashboards --> /chronograf/v1/dashboards
            auth --> []
            environment --> /chronograf/v1/env
            sources --> /chronograf/v1/sources
            layouts --> /chronograf/v1/layouts
            external --> {u'statusFeed': u'https://www.influxdata.com/feed/json'}
            config --> {u'self': u'/chronograf/v1/config', u'auth': u'/chronograf/v1/config/auth'}
            mappings --> /chronograf/v1/mappings
    '''
    rl=rest_lib.RestLib(request.cls.mylog)
    request.cls.mylog.info('get_all_paths() FIXTURE IS CALLED')
    response=rl.get_chronograf_paths(chronograf)
    request.cls.get_all_paths=response
    request.cls.mylog.info('get_all_paths() FIXTURE IS DONE')
    return request.cls.get_all_paths

@pytest.fixture(scope='class')
def get_source_path(request, chronograf):
    '''
    :param request:request object to introspect the rtequesting test function, class or module context
    :param chronograf:Chronograf URL, e.g. http://<ID>:<PORT>, where port is 8888
    :return:source path, e.g. ['sources':'/chronograf/v1/sources']
    '''
    request.cls.mylog.info('get_source_path() FIXTURE IS CALLED')
    request.cls.mylog.info('get_source_path() CALL get_all_paths() FIXTURE')
    source_path=get_all_paths(request, chronograf)['sources']
    assert source_path is not None, request.cls.mylog.info('get_source_path() ASSERTION ERROR')
    request.cls.mylog.info('get_source_path() source_path=' + str(source_path))
    request.cls.get_source_path=source_path
    request.cls.mylog.info('get_source_path() FIXTURE IS DONE')
    return request.cls.get_source_path

@pytest.fixture(scope='class')
def delete_sources(request,chronograf):
    '''
    :param request:request object to introspect the rtequesting test function, class or module context
    :param base_url:Chronograf URL, e.g. http://<ID>:<PORT>, where port is 8888
    :return:
    '''
    rl=rest_lib.RestLib(request.cls.mylog)
    request.cls.mylog.info('delete_sources() FIXTURE IS CALLED')
    request.cls.mylog.info('delete_sources() : GET ALL OF THE SOURCES')
    source_path=get_source_path(request, chronograf)
    sources=rl.get_sources(chronograf, source_path)
    for source in sources.keys():
        request.cls.mylog.info('delete_sources() : DELETING SOURCE ID=' + str(source))
        rl.delete_source(chronograf, source_path, source)
    request.cls.mylog.info('delete_sources() IS DONE')


