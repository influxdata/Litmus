import pytest

def pytest_addoption(parser):
    parser.addoption('--clustername', action='store')
    parser.addoption('--chronograf', action='store')
    parser.addoption('--datanodes', action='store')
    parser.addoption('--metanodes', action='store')
    parser.addoption('--nodemap', action='store')
    parser.addoption('--kapacitor', action='store')
    parser.addoption('--adminuser', action='store')
    parser.addoption('--adminpass', action='store')
    parser.addoption('--httpauth', action='store')
    parser.addoption('--ldapauth', action='store')
    parser.addoption('--metaauth', action='store')
    parser.addoption('--clusteros', action='store')

def get_clusteros(request):
    return request.config.getoption('--clusteros')

def get_clustername(request):
    return request.config.getoption('--clustername')

def get_chronograf(request):
    return request.config.getoption('--chronograf')

def get_data_nodes(request):
    return request.config.getoption('--datanodes')

def get_meta_nodes(request):
    return request.config.getoption('--metanodes')

def get_all_nodes(request):
    return request.config.getoption('--nodemap')

def get_kapacitor(request):
    return request.config.getoption('--kapacitor')

def get_admin_user(request):
    return request.config.getoption('--adminuser')

def get_admin_pass(request):
    return request.config.getoption('--adminpass')

def get_http_auth(request):
    return request.config.getoption('--httpauth')

def get_ldap_auth(request):
    return request.config.getoption('--ldapauth')

def get_meta_auth(request):
    return request.config.getoption('--metaauth')

@pytest.fixture(scope='class')
def clusteros(request):
    '''
    :param request:
    :return:
    '''
    request.cls.mylog.info('clusteros() fixture is being called')
    request.cls.mylog.info('-----------------------------------')
    clusteros=get_clusteros(request)
    request.cls.mylog.info('clusteros() fixture : clusteros=' + str(clusteros))
    request.cls.clusteros=clusteros
    request.cls.mylog.info('clusteros() fixture - done')
    request.cls.mylog.info('----------------------------')
    request.cls.mylog.info('')
    return request.cls.clusteros

@pytest.fixture(scope='class')
def clustername(request):
    '''
    :param request:
    :return:
    '''
    request.cls.mylog.info('clustername() fixture is being called')
    request.cls.mylog.info('-------------------------------------')
    clustername=get_clustername(request)
    request.cls.mylog.info('clustername() fixture : clustername=' + str(clustername))
    request.cls.clustername=clustername
    request.cls.mylog.info('clustername() fixture - done')
    request.cls.mylog.info('----------------------------')
    request.cls.mylog.info('')
    return request.cls.clustername

@pytest.fixture(scope='class')
def chronograf(request):
    '''
    :param request:
    :return:
    '''
    http='http://'
    port=':8888'
    try:
        request.cls.mylog.info('chronograf() fixture is beig called')
        request.cls.mylog.info('-----------------------------------------------------------')
        chronograf=get_chronograf(request)
        request.cls.mylog.info('chronograf() fixture : chronograf=' + str(chronograf))
    except:
        chronograf=None
    assert chronograf is not None, request.cls.mylog.info('chronograf() fixture returned None')
    request.cls.mylog.info('chronograf() fixture : chronograf url=' + str(http+chronograf+port))
    request.cls.chronograf=http+chronograf+port
    request.cls.mylog.info('chronograf() fixture - done')
    request.cls.mylog.info('-----------------------------------------------')
    request.cls.mylog.info('')
    return request.cls.chronograf

@pytest.fixture(scope='class')
def data_nodes(request):
    '''
    :param request:
    :return:
    '''
    http='http://'
    port=':8086'
    try:
        request.cls.mylog.info('data_nodes() fixture is being called')
        request.cls.mylog.info('--------------------------------------------------------------')
        data_nodes=get_data_nodes(request)
        request.cls.mylog.info('data_nodes() fixture : data_nodes=' + str(data_nodes))
    except:
        data_nodes=None
    assert data_nodes is not None, request.cls.mylog.info('data_nodes() fixture returned None')
    request.cls.data_nodes=[http+node+port for node in data_nodes.split(',')]
    request.cls.mylog.info('data_nodes() fixture - done')
    request.cls.mylog.info('------------------------------------------------')
    request.cls.mylog.info('')
    return request.cls.data_nodes

@pytest.fixture(scope='class')
def data_nodes_ips(request):
    '''
    :param request:
    :return:
    '''
    try:
        request.cls.mylog.info('FIXTURE data_nodes_ips(): GETTING DATA NODES')
        data_nodes=get_data_nodes(request)
        request.cls.mylog.info('FIXTURE data_nodes_ips(): data_nodes=' + str(data_nodes))
    except:
        data_nodes=None
    assert data_nodes is not None, request.cls.mylog.info('FIXTURE data_nodes_ips() returned None')
    request.cls.data_nodes_ips=[node for node in data_nodes.split(',')]
    return request.cls.data_nodes_ips

@pytest.fixture(scope='class')
def meta_nodes(request):
    '''
    :param request:
    :return:
    '''
    http='http://'
    port=':8091'
    try:
        request.cls.mylog.info('meta_nodes() fixture is being called')
        request.cls.mylog.info('---------------------------------------------------------------')
        meta_nodes=get_meta_nodes(request)
        request.cls.mylog.info('meta_nodes() fixture : meta_nodes=' + str(meta_nodes))
    except:
        meta_nodes=None
    assert meta_nodes is not None, request.cls.mylog.info('meta_nodes fixture returned None')
    request.cls.meta_nodes=[http+node+port for node in meta_nodes.split(',')]
    request.cls.mylog.info('meta_nodes() fixture - done')
    request.cls.mylog.info('-------------------------------------------------')
    request.cls.mylog.info('')
    return request.cls.meta_nodes

@pytest.fixture(scope='class')
def private_public_ip_mapps(request):
    '''
    :param request:
    :return:
    '''
    private_public_dic={}
    try:
        request.cls.mylog.info('private_public_ip_mapps() fixture is being called')
        request.cls.mylog.info('-------------------------------------------------')
        all_nodes_mappings=get_all_nodes(request)
        request.cls.mylog.info('private_public_ip_mapps() fixture : meta_nodes=' + str(all_nodes_mappings))
    except:
        all_nodes_mappings=None
    assert all_nodes_mappings is not None, request.cls.mylog.info('meta_leader fixture returned None')
    nodes_list=all_nodes_mappings.split(',')
    for nodes in nodes_list:
        private_public_dic[nodes.split('_')[1]]=nodes.split('_')[0]
    request.cls.mylog.info('private_public_ip_mapps fixture private/public IP mappings : ' + str(private_public_dic))
    request.cls.private_public_ip_mapps=private_public_dic
    request.cls.mylog.info('private_public_ip_mapps() fixture - done')
    request.cls.mylog.info('----------------------------------------')
    request.cls.mylog.info('')
    return request.cls.private_public_ip_mapps

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
        request.cls.mylog.info('admin_user() fixture is being called')
        request.cls.mylog.info('--------------------------------------------------------------')
        admin_user=get_admin_pass(request)
        request.cls.mylog.info('admin_user() fixture : admin_user=' + str(admin_user))
    except:
        admin_user=None
    request.cls.admin_user=admin_user
    request.cls.mylog.info('admin_user() fixture - done')
    request.cls.mylog.info('------------------------------------------------')
    request.cls.mylog.info('')
    return request.cls.admin_user

@pytest.fixture(scope='class')
def admin_pass(request):
    try:
        request.cls.mylog.info('admin_pass() fixture is being called')
        request.cls.mylog.info('---------------------------------------------------------------')
        admin_pass=get_admin_pass(request)
        request.cls.mylog.info('admin_pass() fixture : admin_pass=' + str(admin_pass))
    except:
        admin_pass=None
    request.cls.admin_pass=admin_pass
    request.cls.mylog.info('admin_pass() fixture - done')
    request.cls.mylog.info('------------------------------------------------')
    request.cls.mylog.info('')
    return request.cls.admin_pass

@pytest.fixture(scope='class')
def http_auth(request):
    try:
        request.cls.mylog.info('http_auth() fixture is being called')
        request.cls.mylog.info('-------------------------------------------------------------')
        http_auth=get_http_auth(request)
        request.cls.mylog.info('http_auth() fixture : http_auth=' + str(http_auth))
    except:
        http_auth=None
    assert http_auth is not None, request.cls.mylog.info('http_auth() fixture returned None')
    request.cls.http_auth=http_auth
    request.cls.mylog.info('http_auth() fixture - done')
    request.cls.mylog.info('--------------------------------------------')
    request.cls.mylog.info('')
    return request.cls.http_auth

@pytest.fixture(scope='class')
def ldap_auth(request):
    try:
        request.cls.mylog.info('ldap_auth() fixture is being called')
        request.cls.mylog.info('-----------------------------------')
        ldap_auth=get_ldap_auth(request)
        request.cls.mylog.info('ldap_auth() fixture : ldap_auth=' + str(ldap_auth))
    except:
        ldap_auth=None
    assert ldap_auth is not None, request.cls.mylog.info('ldap_auth() fixture returned None')
    request.cls.ldap_auth=ldap_auth
    request.cls.mylog.info('ldap_auth() fixture - done')
    request.cls.mylog.info('--------------------------')
    request.cls.mylog.info('')
    return request.cls.ldap_auth

@pytest.fixture(scope='class')
def meta_auth(request):
    try:
        request.cls.mylog.info('meta_auth() fixture is being called')
        request.cls.mylog.info('-----------------------------------')
        meta_auth=get_meta_auth(request)
        request.cls.mylog.info('meta_auth() fixture : meta_auth=' + str(meta_auth))
    except:
        meta_auth=None
    assert meta_auth is not None, request.cls.mylog.info('meta_auth() fixture returned None')
    request.cls.meta_auth=meta_auth
    request.cls.mylog.info('http_auth() fixture - done')
    request.cls.mylog.info('--------------------------')
    request.cls.mylog.info('')
    return request.cls.meta_auth