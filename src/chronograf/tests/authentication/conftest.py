import pytest
from src.chronograf.lib import chronograf_rest_lib
import src.util.sources_util as su
from random import choice

# create users with different permissions
# all valid cluster permissions
cluster_permissions = ['ViewAdmin', 'ViewChronograf', 'CreateDatabase',
                       'CreateUserAndRole', 'AddRemoveNode', 'DropDatabase',
                       'DropData', 'ReadData', 'WriteData', 'Rebalance', 'ManageShard',
                       'ManageContinuousQuery', 'ManageQuery', 'ManageSubscription',
                       'Monitor', 'CopyShard', 'KapacitorAPI', 'KapacitorConfigAPI']
 # scope of permissions
scope = ['all', 'database']

@pytest.fixture(scope='class')
def _get_users_url(request, create_source):
    '''
    :param create_source:
    :return: users_url, e.g. /chronograf/v1/source/{id}/users
    '''
    request.cls.mylog.info('_get_users_url is being called')
    request.cls.mylog.info('------------------------------')
    request.cls.mylog.info('')
    (source_id, result_dic)=create_source
    users_url=result_dic[source_id].get('USERS')
    request.cls.mylog.info('_get_users_url() fixture - users_url=' + str(users_url))
    request.cls.mylog.info('_get_users_url - done')
    request.cls.mylog.info('---------------------')
    request.cls.mylog.info('')
    return users_url

@pytest.fixture(scope='class')
def setup_users(request, chronograf, _get_users_url):
    '''
    :param request:
    :param create_source:
    :param chronograf:
    :return:
    '''
    rl=chronograf_rest_lib.RestLib(request.cls.mylog)
    request.cls.mylog.info('setup_users() fixture is being called')
    request.cls.mylog.info('-------------------------------------')
    request.cls.mylog.info('')
    users_url=_get_users_url
    assert users_url is not None, request.cls.log.info('Assertion Error: users_url is None')
    for permission in cluster_permissions:
        # create a user per permission
        name='user_%s' % permission
        request.cls.mylog.info('setup_users fixture - create user \''
                               + str(name) + '\'')
        data={'name':name, 'password':name, 'permissions':[{'scope':'all', 'allowed':[permission]}]}
        response=rl.create_user(chronograf=chronograf, users_url=users_url, json=data)
        assert response.status_code == 201, \
            request.cls.mylog.info('Assert Error ' + str(response.json()))
    request.cls.mylog.info('setup_users fixture - done')
    request.cls.mylog.info('--------------------------')
    request.cls.mylog.info('')

@pytest.fixture(scope='class')
def cleanup_users(request, chronograf, _get_users_url):
    '''
    :param request:
    :return:
    '''
    rl= chronograf_rest_lib.RestLib(request.cls.mylog)
    request.cls.mylog.info('cleanup_users() fixture is being called')
    request.cls.mylog.info('---------------------------------------')
    request.cls.mylog.info('')
    users_url=_get_users_url
    assert users_url is not None, request.cls.log.info('Assertion Error: users_url is None')
    for permission in cluster_permissions:
        # delete users
        name='user_%s' % permission
        request.cls.mylog.info('cleanup_users fixture - deleting user \''
                               + str(name) + '\'')
        response=rl.delete_user(chronograf=chronograf, users_url=users_url, user_name=name)
        assert response.status_code == 204, \
            request.cls.mylog.info('cleanup_users() fixture Assertion Error '
                                   + str(response.json()))
    for permission in cluster_permissions:
        # delete users
        name='user_%s_createuser' % permission
        request.cls.mylog.info('cleanup_users fixture - deleting user \''
                               + str(name) + '\'')
        rl.delete_user(chronograf=chronograf, users_url=users_url, user_name=name)
        # do not assert, because user might not exist
    request.cls.mylog.info('cleanup_users() fixture - done')
    request.cls.mylog.info('------------------------------')
    request.cls.mylog.info('')

# create source for each created user
@pytest.fixture(scope='class')
def create_sources_for_test_users(request, chronograf,data_nodes, meta_nodes):
    '''
    :param request:
    :return:
    '368': {'USERNAME': u'user_CreateUserAndRole', 'INSECURE_SKIP_VERIFY': False, 'DATA_URL': u'http://52.88.145.203:8086',
    'NAME': u'user_CreateUserAndRole', 'ROLES': u'/chronograf/v1/sources/368/roles', 'DEFAULT': False, 'TELEGRAF_DB': u'telegraf',
    'META_URL': u'http://34.217.86.218:8091', 'KAPACITOR': u'/chronograf/v1/sources/368/kapacitors',
    'WRITE': u'/chronograf/v1/sources/368/write', 'PROXY': u'/chronograf/v1/sources/368/proxy', 'SHARED_SECRET': '',
    'QUERY': u'/chronograf/v1/sources/368/queries', 'DBS': u'/chronograf/v1/sources/368/dbs', 'PERMISSIONS': u'/chronograf/v1/sources/368/permissions',
     'TYPE': u'influx-enterprise', 'USERS': u'/chronograf/v1/sources/368/users'}
    '''
    new_sources={}
    data_node=choice(data_nodes)
    meta_node=choice(meta_nodes)
    sources_url='/chronograf/v1/sources'
    rl=chronograf_rest_lib.RestLib(request.cls.mylog)
    request.cls.mylog.info('create_sources_for_test_users() fixture is being called')
    request.cls.mylog.info('-------------------------------------------------------')
    request.cls.mylog.info('')
    for permission in cluster_permissions:
        name='user_%s' % permission
        request.cls.mylog.info('create_sources_for_test_users() fixture - '
                               'create data source for  \'' + str(name) + '\' user')
        data={'name':name, 'username':name, 'password':name,
              'metaUrl':meta_node, 'url':data_node}
        (status, source_data, source_id)=rl.create_source(chronograf, sources_url, json=data)
        assert status == 201, request.cls.mylog.info('create_sources_for_test_users '
                                                 'status=' + str(status))
        assert source_id is not None, \
            request.cls.mylog.info('create_sources_for_test_users source_id=' + str(source_id))
    # get all sources
    sources=rl.get_sources(chronograf, sources_url)
    # need to convert result dictionary so keys are the names of the datasources
    for key in sources:
        source_name=su.get_source_name(request.cls, key, sources)
        users_url=su.get_source_users_link(request.cls, key, sources)
        db_url=su.get_source_dbs_link(request.cls, key, sources)
        new_sources[source_name]={'SOURCE_ID':key, 'USERS':users_url, 'DB':db_url}
    request.cls.mylog.info('create_sources_for_test_users() fixture '
                           '-new sources dict : ' + str(new_sources))
    request.cls.create_sources_for_test_users=new_sources
    request.cls.mylog.info('create_sources_for_test_users() fixture is done')
    request.cls.mylog.info('-----------------------------------------------')
    request.cls.mylog.info('')
    return request.cls.create_sources_for_test_users



