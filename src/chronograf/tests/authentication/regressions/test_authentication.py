
import pytest
import src.util.login_util as lu
from src.chronograf.lib import chronograf_rest_lib
from influxdb import InfluxDBClient
from random import choice
from src.util import database_util as du
from src.util import users_util as uu


@pytest.mark.parametrize('create_source', ['user_permissions'], ids=[''], indirect=True)
@pytest.mark.usefixtures( 'delete_created_sources', 'create_source',
                          'cleanup_users', 'setup_users' ,'create_sources_for_test_users',
                          'data_nodes_ips')
class TestUserPermissions(object):
    '''
    delete_created_sources - delete all of the sources created by the tests,
                                            with the exception of ones created by pcl installer
    create_source - to create a source for admin_user
    cleanup_users - delete created for the test(s) users
    setup_users - create test users
    data_node_ips - to be used in InfluxDBCLient
    '''
    mylog=lu.log(lu.get_log_path(), 'w', __name__)
    rl= chronograf_rest_lib.RestLib(mylog)

    users=['user_ViewAdmin', 'user_ViewChronograf', 'user_CreateDatabase','user_CreateUserAndRole', 'user_AddRemoveNode',
           'user_DropDatabase', 'user_DropData', 'user_ReadData', 'user_WriteData', 'user_Rebalance', 'user_ManageShard',
           'user_ManageContinuousQuery', 'user_ManageQuery', 'user_ManageSubscription', 'user_Monitor', 'user_CopyShard',
           'user_KapacitorAPI', 'user_KapacitorConfigAPI']

    ################## Helper methods ########################
    def source_url(self, permission, Key):
        source_name=permission
        source_url=self.create_sources_for_test_users[source_name].get(Key)
        return (source_name, source_url)

    ##########################################################
    def header(self, test_name):
        self.mylog.info('#######################################################')
        self.mylog.info('<--------------- %s START --------------->' % test_name)
        self.mylog.info('#######################################################')

    def footer(self, test_name):
        self.mylog.info('#######################################################')
        self.mylog.info('<--------------- %s END --------------->' % test_name)
        self.mylog.info('#######################################################')
        self.mylog.info('')
    ##########################################################

    # user with CreateDatabase permission should be able to create database:
    # https://github.com/influxdata/influxdb/issues/9727
    @pytest.mark.parametrize('user', users)
    def test_user_create_database(self, user):
        '''
        :param user:
        :return:
        '''
        # create source with a specific user
        test_name='test_user_create_database_' + user
        self.header(test_name)
        (name, source_db_url)=self.source_url(user, 'DB')
        self.mylog.info(test_name + ' name=%s, source_db_url=%s' % (name, source_db_url))
        response=self.rl.create_database(self.chronograf, source_db_url, {'name':name})
        if user == 'user_CreateDatabase':
            assert response.status_code == 201, \
                pytest.xfail(reason='https://github.com/influxdata/influxdb/issues/9727')
            #self.mylog.info(test_name + ' Error Message' + response.json().get('message') )
        else:
            self.mylog.info(test_name + ' Error message: ' + response.json().get('message'))
            assert response.json().get('code') == 400
        self.footer('test_user_create_database')

    # user with DropDatabase permission should be able to drop database
    @pytest.mark.parametrize('user', users)
    def test_user_drop_database(self, user):
        '''
        :param user:
        :return:
        '''
        test_name='test_user_drop_database_' + user
        self.header(test_name)
        (name, source_db_url)=self.source_url(user,'DB')
        self.mylog.info(test_name + ' name=%s, source_db_url=%s' % (name, source_db_url))
        # drop_test_db is not existing database, but deleting non-exisitng database does not return an error
        # this just tests correct authorization(s)
        response=self.rl.delete_database(self.chronograf, source_db_url, 'drop_test_db')
        if user == 'user_DropDatabase':
            assert response.status_code == 204, \
                self.mylog.info(test_name + ' Error message ' + response.json().get('message'))
        else:
            self.mylog.info(test_name + ' Error message: ' + response.json().get('message'))
            assert response.json().get('code') == 400
        self.footer(test_name)

    # user with CreateDatabase permission should be able to create RP
    # https://github.com/influxdata/influxdb/issues/9727
    @pytest.mark.parametrize('user', users)
    def test_user_create_rp(self, user):
        '''
        :param user:
        :return:
        '''
        test_name='test_user_create_rp_' + user
        self.header(test_name)
        data={'name':test_name, 'duration':'3d', 'replication':2, 'shardDuration':'2h', 'isDefault':False}
        (name, source_db_url)=self.source_url(user, 'DB')
        self.mylog.info(test_name + ' name=%s, source_db_url=%s' % (name, source_db_url))
        source_rp_url=source_db_url + '/_internal/rps'
        response=self.rl.create_retention_policy_for_database(self.chronograf, source_rp_url, data)
        if user == 'user_CreateDatabase':
            assert response.status_code == 201, \
                pytest.xfail(reason='https://github.com/influxdata/influxdb/issues/9727')
            #self.mylog.info(test_name + ' Error Message' + response.json().get('message') )
        else:
            self.mylog.info(test_name + ' Error message: ' + response.json().get('message'))
            assert response.json().get('code') == 400
        self.footer(test_name)

    # user with ReadData and CreateDatabase should be able to view RP
    # https://github.com/influxdata/influxdb/issues/9727
    @pytest.mark.parametrize('user', users)
    def test_user_show_rp(self, user):
        '''
        :param user:
        :return:
        '''
        test_name='test_user_show_rp_' + user
        self.header(test_name)
        (name, source_db_url) = self.source_url(user, 'DB')
        self.mylog.info(test_name + ' name=%s, source_db_url=%s' % (name, source_db_url))
        source_rp_url=source_db_url + '/_internal/rps'
        response=self.rl.get_retention_policies_for_database(self.chronograf, source_rp_url)
        if user == 'user_CreateDatabase' or user == 'user_ReadData':
            assert response.status_code == 200, \
                pytest.xfail(reason='https://github.com/influxdata/influxdb/issues/9727')
        else:
            self.mylog.info(test_name + ' Error message: ' + response.json().get('message'))
            assert response.json().get('code') == 400
        self.footer(test_name)

    # user with CreateDatabase permission should be able to alter RP
    # https://github.com/influxdata/influxdb/issues/9727
    @pytest.mark.parametrize('user', users)
    def test_user_alter_rp(self, user):
        '''
        :param user:
        :return:
        '''
        data_node = choice(self.data_nodes_ips)
        rp_to_create = 'ALTER_RP'
        duration = '3d'
        default = False
        replication = '2'
        database = '_internal'
        rp_to_update='ALTER_RP'
        data={'name':rp_to_update, 'duration':'4d', 'replication':2, 'shardDuration':'1h', 'isDefault':False}
        test_name='test_user_alter_rp_' + user

        self.header(test_name)
        username, password = '', ''
        if self.http_auth:
            username = self.admin_user
            password = self.admin_pass
        client = InfluxDBClient(host=data_node, username=username, password=password)
        success = du.create_retention_policy(self, client, rp_to_create, duration, replication, database, default)
        assert success, self.mylog.info(test_name + ' Assertion Error, was not able to create RP')

        (name, source_db_url) = self.source_url(user, 'DB')
        self.mylog.info(test_name + ' name=%s, source_db_url=%s' % (name, source_db_url))
        source_rp_url=source_db_url + '/_internal/rps'
        response=self.rl.patch_retention_policy_for_database(self.chronograf, source_rp_url, rp_to_update, data)
        if user == 'user_CreateDatabase':
            assert response.status_code == 201, \
                pytest.xfail(reason='https://github.com/influxdata/influxdb/issues/9727')
            #self.mylog.info(test_name + ' Error Message' + response.json().get('message') )
        else:
            self.mylog.info(test_name + ' Error message: ' + response.json().get('message'))
            assert response.json().get('code') == 400
        self.footer(test_name)

    # user with DropDatabase permission should be able to drop RP
    @pytest.mark.parametrize('user', users)
    def test_user_delete_rp(self, user):
        '''
        :param user:
        :return:
        '''
        test_name = 'test_user_delete_rp_' + user
        # creating the same RP multiple time won't create multiple RP or ERROR's out
        rp_to_create= 'DELETE_RP'
        duration='3d'
        default=False
        replication='2'
        database='_internal'
        data_node=choice(self.data_nodes_ips)

        self.header(test_name)
        # need to create retention policy as admin_user, admin_pass if auth is enabled
        username, password='',''
        if self.http_auth:
            username=self.admin_user
            password=self.admin_pass
        client=InfluxDBClient(host=data_node,username=username, password=password)
        success=du.create_retention_policy(self, client, rp_to_create, duration, replication, database, default)
        assert success, self.mylog.info(test_name + ' Assertion Error, was not able to create RP')
        (name, source_db_url) = self.source_url(user, 'DB')
        self.mylog.info(test_name + ' name=%s, source_db_url=%s' % (name, source_db_url))
        source_rp_url=source_db_url + '/_internal/rps'
        response=self.rl.delete_retention_policy_for_database(self.chronograf, source_rp_url, rp_to_create)
        if user == 'user_DropDatabase':
            assert response.status_code == 204, \
                self.mylog.info(test_name + ' Error message ' + response.json().get('message'))
            # make sure that retention policy was actually dropped.
            ret_policies=client.get_list_retention_policies(database)
            assert rp_to_create not in [item['name'] for item in ret_policies], \
                self.mylog.info(test_name + ' Retention Policy was not dropped')
        else:
            self.mylog.info(test_name + ' Error message: ' + response.json().get('message'))
            assert response.json().get('code') == 400
        self.footer(test_name)

    @pytest.mark.parametrize('user', users)
    def test_user_createuser(self, user):
        '''
        :param user:
        :return:
        '''
        test_name = 'test_user_createuser_' + user

        self.header(test_name)
        (name, source_users_url)=self.source_url(user, 'USERS')
        self.mylog.info(test_name + ' name=%s, source_users_url=%s' % (name, source_users_url))
        data = {'name': name+'_createuser', 'password': name+'_createuser'}
        response=self.rl.create_user(self.chronograf, source_users_url, data)
        if user == 'user_CreateUserAndRole':
            assert response.status_code == 201, \
                self.mylog.info(test_name + ' Error message ' + response.json().get('message'))
        else:
            self.mylog.info(test_name + ' Error message: ' + response.json().get('message'))
            assert response.json().get('code') == 400
        self.footer(test_name)

    @pytest.mark.parametrize('user', users)
    def test_user_deleteuser(self, user):
        '''
        :param user:
        :return:
        '''
        test_name='test_user_deleteuser_' + user
        data_node=choice(self.data_nodes_ips)

        self.header(test_name)
        user_name, user_password=user+'_deleteuser', user+'_deleteuser'
        username, password = '', ''
        if self.http_auth:
            username = self.admin_user
            password = self.admin_pass
        client=InfluxDBClient(host=data_node, username=username, password=password)
        (name, source_users_url) = self.source_url(user, 'USERS')
        (success,message)=uu.create_user(self, client, user_name, user_password, False)
        assert success, self.mylog.info(test_name + ' : Assertion Error')
        response=self.rl.delete_user(self.chronograf, source_users_url, user_name)
        if user == 'user_CreateUserAndRole':
            assert response.status_code == 204, \
                self.mylog.info(test_name + ' Error message ' + response.json().get('message'))
                # TODO add verification that user indeed was deleted
        else:
            self.mylog.info(test_name + ' Error message: ' + response.json().get('message'))
            assert response.json().get('code') == 400
        self.footer(test_name)