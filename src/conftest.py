import pytest

def pytest_addoption(parser):
    parser.addoption('--clustername', action='store')
    parser.addoption('--chronograf', action='store')
    parser.addoption('--datanodes', action='store')
    parser.addoption('--metanodes', action='store')
    parser.addoption('--kapacitor', action='store')
    parser.addoption('--adminuser', action='store')
    parser.addoption('--adminpass', action='store')
    parser.addoption('--httpauth',action='store')

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

def get_admin_user(request):
    return request.config.getoption('--adminuser')

def get_admin_pass(request):
    return request.config.getoption('--adminpass')

def http_auth(request):
    return request.config.getoption('--httpauth')

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
def data_nodes_ips(request):
    try:
        request.cls.mylog.info('FIXTURE data_nodes_ips(): GETTING DATA NODES')
        data_nodes=get_data_nodes(request)
        request.cls.mylog.info('FIXTURE data_nodes_ips(): data_nodes=' + str(data_nodes))
    except:
        data_nodes=None
    assert data_nodes is not None, request.cls.mylog.info('FIXTURE data_nodes_ips() returned None')
    request.cls.data_nodes_ips=data_nodes
    return request.cls.data_nodes_ips

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
        request.cls.mylog.info('FIXTURE kapacitor(): kapacitor=' + str(kapacitor))
    except:
        kapacitor=None
    assert kapacitor is not None, request.cls.mylog.info('FIXTURE kapacitor() returned None')
    kapacitor=http+kapacitor+port
    request.cls.mylog.info('FIXTURE kapacitor() kapacitor url=' + str(kapacitor))
    request.cls.kapacitor=kapacitor
    return request.cls.kapacitor

@pytest.fixture(scope='class')
def admin_user(request):
    try:
        request.cls.mylog.info('FIXTURE admin_user(): GETTING ADMIN_USER ')
        admin_user=get_admin_pass(request)
        request.cls.mylog.info('FIXTURE admin_user() admin_user=' + str(admin_user))
    except:
        admin_user=None
    #assert admin_user is not None, request.cls.mylog.info('FIXTURE admin_user() returned None')
    request.cls.admin_user=admin_user
    return request.cls.admin_user

@pytest.fixture(scope='class')
def admin_pass(request):
    try:
        request.cls.mylog.info('FIXTURE admin_pass(): GETTING ADMIN_PASS')
        admin_pass=get_admin_pass(request)
        request.cls.mylog.info('FIXTURE admin_pass() admin_pass=' + str(admin_pass))
    except:
        admin_pass=None
    #assert admin_pass is not None, request.cls.mylog.info('FIXTURE admin_user() returned None')
    request.cls.admin_pass=admin_pass
    return request.cls.admin_pass

@pytest.fixture(scope='class')
def http_auth(request):
    try:
        request.cls.mylog.info('FIXTURE http_auth(): GETTING HTTPAUTH')
        httpauth=http_auth(request)
        request.cls.mylog.info('FIXTURE http_auth() httpauth=' + str(httpauth))
    except:
        httpauth=None
    assert http_auth is not None, request.cls.mylog.info('FIXTURE http_auth() returned None')
    request.cls.http_auth=httpauth
    return request.cls.http-auth
