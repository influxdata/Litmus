
import pytest
from src.influxdb.lib import influxdb_rest_lib
from random import choice
from src.util import database_util as du
from influxdb import InfluxDBClient as InfluxDBClient

first_roles={'a_first':['CreateDatabase'], 'b_first':['DropDatabase'], 'c_first':['CreateUserAndRole'], 'd_first':['ManageSubscription'],
       'e_first':['ManageContinuousQuery'], 'f_first':['DropData'], 'g_first':['ManageShard'], 'h_first':['ManageQuery'],
       'i_first':['Monitor'], 'j_first':['ReadData'], 'k_first':['WriteData'], 'l_first':''}

last_roles={'a_last':['CreateDatabase'], 'b_last':['DropDatabase'], 'c_last':['CreateUserAndRole'], 'd_last':['ManageSubscription'],
       'e_last':['ManageContinuousQuery'], 'f_last':['DropData'], 'g_last':['ManageShard'], 'h_last':['ManageQuery'],
       'i_last':['Monitor'], 'j_last':['ReadData'], 'k_last':['WriteData'], 'l_last':''}

# create a role (key in the roles dic) and assign permission (value in roles dic)
# meta nodes are using authenticaiton by default
AD_ADMIN_USER='sal.xu'
AD_ADMIN_PASS='p@ssw0rd'

@pytest.fixture(scope='class')
def meta_leader(request, private_public_ip_mapps, meta_nodes):
    '''
    :param request:
    :param private_public_ip_mapps:
    :param meta_nodes
    :return: leader meta node, e.g. http://<ip>:8091
    '''
    meta_leader_node=None
    irl = influxdb_rest_lib.InfluxDBInfluxDBRestLib(request.cls.mylog)
    request.cls.mylog.info('meta_leader fixture is being called')
    request.cls.mylog.info('-----------------------------------')
    meta_url=choice(meta_nodes)
    prv_pub_dic=private_public_ip_mapps
    (success, meta_leader_url, message)=irl.get_leader_meta_url(meta_url, auth=(AD_ADMIN_USER, AD_ADMIN_PASS))
    assert success and meta_leader_url != '', \
        request.cls.mylog.info('meta_leader fixture - failed to get leader meta url: ' + str(message))
    private_addresses=prv_pub_dic.keys() # getting private addresses of all of the meta nodes
    for prv_address in private_addresses:
        if prv_address in meta_leader_url:
            meta_leader_node='http://'+prv_pub_dic[prv_address]+':8091'
            request.cls.mylog.info('meta_leader fixture - meta_leader_url=' + str(meta_leader_node))
            break
    assert meta_leader_node is not None, \
        request.cls.mylog.info('meta_leader fixture - failed to get meta leader node')
    request.cls.meta_leader=meta_leader_node
    request.cls.mylog.info('meta_leader fixture is done')
    request.cls.mylog.info('---------------------------')
    request.cls.mylog.info('')
    return request.cls.meta_leader

@pytest.fixture(scope='class')
def setup_roles_permissions(request, meta_leader):
    '''
    :param request:
    :return:
    '''
    irl=influxdb_rest_lib.InfluxDBInfluxDBRestLib(request.cls.mylog)
    request.cls.mylog.info('setup_roles_permissions fixture is being called')
    request.cls.mylog.info('-----------------------------------------------')
    for role, permission in first_roles.items():
        (success, message)=irl.create_role(meta_leader, role, auth=(AD_ADMIN_USER, AD_ADMIN_PASS))
        assert success, \
            request.cls.mylog.info('setup_roles_permissions fixture, error setting first name roles '
                              + str(role) + ', error:' + str(message))
        (success, message)=irl.add_role_permissions(meta_leader, role, '', permission, auth=(AD_ADMIN_USER,AD_ADMIN_PASS))
        if permission != '':
            assert success, request.cls.mylog.info('setup_roles_permissions fixture, error setting first name permission '
                                                   + str(permission) + ', error:' + str(message))
    for role, permission in last_roles.items():
        (success, message)=irl.create_role(meta_leader, role, auth=(AD_ADMIN_USER, AD_ADMIN_PASS))
        assert success, \
            request.cls.mylog.info('setup_roles_permissions fixture, error setting last names roles '
                               + str(role) + ', error:' + str(message))
        (success, message)=irl.add_role_permissions(meta_leader, role, '', permission, auth=(AD_ADMIN_USER, AD_ADMIN_PASS))
        if permission != '':
            assert success, request.cls.mylog.info('setup_roles_permissions fixture, error setting last name permission '
                                               + str(permission) + ', error:' + str(message))
    request.cls.mylog.info('setup_roles_permissions fixture is done')
    request.cls.mylog.info('---------------------------------------')
    request.cls.mylog.info('')

@pytest.fixture(scope='class')
def delete_roles(request, meta_leader):
    '''
    :param request:
    :param meta_leader:
    :return:
    '''
    irl = influxdb_rest_lib.InfluxDBInfluxDBRestLib(request.cls.mylog)
    request.cls.mylog.info('delete_roles fixture is being called')
    request.cls.mylog.info('------------------------------------')
    for role in first_roles.keys():
        (success, message)=irl.delete_role(meta_leader, role, auth=(AD_ADMIN_USER, AD_ADMIN_PASS))
        assert success, \
            request.cls.mylog.info('delete_roles fixture, error deleting first name roles '
                                   + str(role) + ', error:' + str(message))
    for role in last_roles.keys():
        (success, message)=irl.delete_role(meta_leader, role, auth=(AD_ADMIN_USER, AD_ADMIN_PASS))
        assert success, \
            request.cls.mylog.info('delete_roles fixture, error deleting last name roles '
                               + str(role) + ', error:' + str(message))
    request.cls.mylog.info('delete_roles fixture is done')
    request.cls.mylog.info('----------------------------')

@pytest.fixture(scope='function', autouse=False)
def drop_database(request, data_nodes_ips):
    '''
    :param request:
    :param data_nodes:
    :param database name:
    :return:
    '''
    data_node=choice(data_nodes_ips)
    database=request.param
    request.cls.mylog.info('drop_database fixture is being called')
    request.cls.mylog.info('-------------------------------------')
    client=InfluxDBClient(data_node, username=AD_ADMIN_USER, password=AD_ADMIN_PASS)
    (success, error)=du.drop_database(request.cls, client, database)
    assert success, request.cls.mylog.info('drop_database fixture failed to drop database' + error)
    def drop_database_fin():
        client=InfluxDBClient(data_node, username=AD_ADMIN_USER, password=AD_ADMIN_PASS)
        (success, error)=du.drop_database(request.cls, client, database)
        assert success, request.cls.mylog.info('drop_database fixture failed to drop database' + error)
    request.addfinalizer(drop_database_fin)
    request.cls.mylog.info('drop_database fixture is done')
    request.cls.mylog.info('-----------------------------')
    request.cls.mylog.info('')

@pytest.fixture(scope='function', autouse=False)
def create_database(request, data_nodes_ips):
    '''
    :param request:
    :param data_nodes:
    :param database name:
    :return:
    '''
    data_node=choice(data_nodes_ips)
    database=request.param
    request.cls.mylog.info('create_database fixture is being called')
    request.cls.mylog.info('-------------------------------------')
    client=InfluxDBClient(data_node, username=AD_ADMIN_USER, password=AD_ADMIN_PASS)
    (success, error)=du.create_database(request.cls, client, database)
    assert success, request.cls.mylog.info('create_database fixture failed to create database' + error)
    def create_database_fin():
        client=InfluxDBClient(data_node, username=AD_ADMIN_USER, password=AD_ADMIN_PASS)
        (success, error)=du.drop_database(request.cls, client, database)
        assert success, request.cls.mylog.info('create_database fixture failed to drop database' + error)
    request.addfinalizer(create_database_fin)
    request.cls.mylog.info('create_database fixture is done')
    request.cls.mylog.info('-------------------------------')
    request.cls.mylog.info('')

