import pytest
import src.util.login_util as lu

mylog=lu.log(lu.get_log_path(), 'w', __name__)

def pytest_addoption(parser):
    parser.addoption('--chronograf', action='store')
    parser.addoption('--datanodes', action='store')
    parser.addoption('--metanodes', action='store')

def get_base_url(request):
    return request.config.getoption('--chronograf')

def get_data_nodes(request):
    return request.config.getoption('--datanodes')

def get_meta_nmodes(request):
    return request.config.getoption('--metanodes')

@pytest.fixture(scope='class')
def base_url(request):
    try:
        request.cls.mylog.info('FIXTURE base_url(): getting base URL')
        base_url=get_base_url(request)
        request.cls.mylog.info('FIXTURE base_url(): base_url=' + str(base_url))
    except:
        base_url=None
    request.cls.base_url=base_url
    return request.cls.base_url

@pytest.fixture(scope='class')
def data_nodes(request):
    try:
        request.cls.mylog.info('FIXTURE data_nodes(): getting data nodes')
        data_nodes=get_data_nodes(request)
        request.cls.mylog.info('FIXTURE data_nodes(): data_nodes=' + str(data_nodes))
    except:
        data_nodes=None
    request.cls.data_nodes=data_nodes
    return request.cls.data_nodes

@pytest.fixture(scope='class')
def meta_nodes(request):
    try:
        request.cls.mylog.info('FIXTURE meta_nodes(): getting meta nodes')
        meta_nodes=get_data_nodes(request)
        request.cls.mylog.info('FIXTURE data_nodes(): meta_nodes=' + str(meta_nodes))
    except:
        meta_nodes=None
    request.cls.meta_nodes=meta_nodes
    return request.cls.meta_nodes
