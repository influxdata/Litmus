import pytest
import src.util.login_util as lu

mylog=lu.log(lu.get_log_path(), 'w', __name__)

def pytest_addoption(parser):
    parser.addoption('--clustername', action='store')
    parser.addoption('--chronograf', action='store')
    parser.addoption('--datanodes', action='store')
    parser.addoption('--metanodes', action='store')
    parser.addoption('--kapacitor', action='store')

def get_clustername(request):
    return request.config.getoption('--clustername')

def get_chronograf(request):
    return request.config.getoption('--chronograf')

def get_data_nodes(request):
    return request.config.getoption('--datanodes')

def get_meta_nodes(request):
    return request.config.getoption('--metanodes')

def get_kapacitor(request):
    return request.config.getoption('--kapacitor')

@pytest.fixture(scope='class')
def clustername(request):
    request.cls.mylog.info('FIXTURE clustername(): GETTING CLUSTER NAME')
    clustername=get_clustername(request)
    request.cls.mylog.info('FIXTURE clustername(): clustername=' + str(clustername))
    request.cls.clustername=clustername
    return request.cls.clustername

@pytest.fixture(scope='class')
def chronograf(request):
    http='http://'
    port=':8888'
    try:
        request.cls.mylog.info('FIXTURE chronograf(): GETTING CHRONOGRAF URL')
        chronograf=get_chronograf(request)
        request.cls.mylog.info('FIXTURE chronograf(): chronograf=' + str(chronograf))
    except:
        chronograf=None
    assert chronograf is not None, request.cls.mylog.info('FIXTURE chronograf() returned None')
    request.cls.mylog.info('FIXTURE chronograf(): chronograf url=' + str(http+chronograf+port))
    request.cls.chronograf=http+chronograf+port
    return request.cls.chronograf

@pytest.fixture(scope='class')
def data_nodes(request):
    http='http://'
    port=':8086'
    try:
        request.cls.mylog.info('FIXTURE data_nodes(): GETTING DATA NODES')
        data_nodes=get_data_nodes(request)
        request.cls.mylog.info('FIXTURE data_nodes(): data_nodes=' + str(data_nodes))
    except:
        data_nodes=None
    assert data_nodes is not None, request.cls.mylog.info('FIXTURE data_nodes() returned None')
    request.cls.data_nodes=[http+node+port for node in data_nodes.split(',')]
    return request.cls.data_nodes

@pytest.fixture(scope='class')
def meta_nodes(request):
    http='http://'
    port=':8091'
    try:
        request.cls.mylog.info('FIXTURE meta_nodes(): GETTING META NODES')
        meta_nodes=get_meta_nodes(request)
        request.cls.mylog.info('FIXTURE data_nodes(): meta_nodes=' + str(meta_nodes))
    except:
        meta_nodes=None
    assert meta_nodes is not None, request.cls.mylog.info('FIXTURE meta_nodes returned None')
    request.cls.meta_nodes=[http+node+port for node in meta_nodes.split(',')]
    return request.cls.meta_nodes

@pytest.fixture(scope='class')
def kapacitor(request):
    http='http://'
    port=':9092'
    try:
        request.cls.mylog.info('FIXTURE kapacitor(): GETTING KAPACITOR URL ')
        kapacitor=get_kapacitor(request)
        request.cls.mylog.info('FIXTURE data_nodes(): kapacitor=' + str(kapacitor))
    except:
        kapacitor=None
    assert kapacitor is not None, request.cls.mylog.info('FIXTURE kapacitor() returned None')
    kapacitor=http+kapacitor+port
    request.cls.mylog.info('FIXTURE kapacitor() kapacitor url=' + str(kapacitor))
    request.cls.kapacitor=kapacitor
    return request.cls.kapacitor
