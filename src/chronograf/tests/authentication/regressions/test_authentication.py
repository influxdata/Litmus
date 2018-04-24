
import pytest
import src.util.login_util as lu
from src.chronograf.lib import rest_lib
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
    rl=rest_lib.RestLib(mylog)

    # CreateDatabase permissions is good for Creating databases, create RP, alter RP and View RP
    create_db_params=[('user_ViewAdmin', False), ('user_ViewChronograf', False), ('user_CreateDatabase', True),
                  ('user_CreateUserAndRole', False), ('user_AddRemoveNode', False), ('user_DropDatabase', False),
                  ('user_DropData', False), ('user_ReadData', False), ('user_WriteData', False), ('user_Rebalance', False), ('user_ManageShard', False),
                  ('user_ManageContinuousQuery', False), ('user_ManageQuery', False), ('user_ManageSubscription', False),
                  ('user_Monitor', False), ('user_CopyShard', False), ('user_KapacitorAPI', False), ('user_KapacitorConfigAPI', False)]
    # DropDatabase permission is good for Dropping databases and Retention Policies
    drop_db_params=[('user_ViewAdmin', False), ('user_ViewChronograf', False), ('user_CreateDatabase', False),
                  ('user_CreateUserAndRole', False), ('user_AddRemoveNode', False), ('user_DropDatabase', True),
                  ('user_DropData', False), ('user_ReadData', False), ('user_WriteData', False), ('user_Rebalance', False), ('user_ManageShard', False),
                  ('user_ManageContinuousQuery', False), ('user_ManageQuery', False), ('user_ManageSubscription', False),
                  ('user_Monitor', False), ('user_CopyShard', False), ('user_KapacitorAPI', False), ('user_KapacitorConfigAPI', False)]
    # ReadData and CreateDatabase are good for viewing retention policies
    show_rp_params=[('user_ViewAdmin', False), ('user_ViewChronograf', False), ('user_CreateDatabase', True),
                  ('user_CreateUserAndRole', False), ('user_AddRemoveNode', False), ('user_DropDatabase', False),
                  ('user_DropData', False), ('user_ReadData', True), ('user_WriteData', False), ('user_Rebalance', False), ('user_ManageShard', False),
                  ('user_ManageContinuousQuery', False), ('user_ManageQuery', False), ('user_ManageSubscription', False),
                  ('user_Monitor', False), ('user_CopyShard', False), ('user_KapacitorAPI', False), ('user_KapacitorConfigAPI', False)]
    # CreateUserAndRole permission is good for CreatingUserStatement, DroppingUserStatement, GrantAdminStatement, GrantStatement, RevokeAdminStatement,
    # RevokeStatement, SetPasswordUserStatement, ShowGrantsForUserStatement, ShowUsersStatement.
    user_params=[('user_ViewAdmin', False), ('user_ViewChronograf', False), ('user_CreateDatabase', False),
                  ('user_CreateUserAndRole', True), ('user_AddRemoveNode', False), ('user_DropDatabase', False),
                  ('user_DropData', False), ('user_ReadData', False), ('user_WriteData', False), ('user_Rebalance', False), ('user_ManageShard', False),
                  ('user_ManageContinuousQuery', False), ('user_ManageQuery', False), ('user_ManageSubscription', False),
                  ('user_Monitor', False), ('user_CopyShard', False), ('user_KapacitorAPI', False), ('user_KapacitorConfigAPI', False)]

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
    @pytest.mark.parametrize('permission, action', create_db_params)
    def test_user_create_database(self, permission, action):
        '''
        :param permission:
        :param action:
        :return:
        '''
        # create source with a specific user
        test_name='test_user_create_database'
        actual_action=False
        self.header(test_name)
        self.mylog.info(test_name + str(permission))
        (name, source_db_url)=self.source_url(permission, 'DB')
        response=self.rl.create_database(self.chronograf, source_db_url, {'name':name})
        if response.status_code == 201:
            actual_action=True
        elif response.json().get('code') is not None and response.json().get('code') == 400:
            actual_action = False
        assert actual_action == action, self.mylog.info('test_user_create_database : Assertion Error')
        self.footer('test_user_create_database')

    # user with DropDatabase permission should be able to drop database
    @pytest.mark.parametrize('permission, action', drop_db_params)
    def test_user_drop_database(self, permission, action):
        '''
        :param permission:
        :param action:
        :return:
        '''
        test_name='test_user_drop_database '
        actual_action=False
        self.header(test_name)
        (name, source_db_url)=self.source_url(permission,'DB')
        response=self.rl.delete_database(self.chronograf, source_db_url, 'drop_test_db')
        if response.status_code == 204:
            actual_action = True
        elif response.json().get('code') is not None and response.json().get('code') == 400:
            actual_action = False
        assert actual_action == action, self.mylog.info('test_user_create_database : Assertion Error')
        self.footer(test_name)

    # user with CreateDatabase permission should be able to create RP
    # https://github.com/influxdata/influxdb/issues/9727
    @pytest.mark.parametrize('permission, action', create_db_params)
    def test_user_create_rp(self, permission, action):
        '''
        :param permission:
        :param action:
        :return:
        '''
        test_name='test_user_create_rp '
        actual_action=False
        self.header(test_name)
        data={'name':test_name, 'duration':'1d', 'replication':2, 'shardDuration':'2h', 'isDefault':False}
        self.mylog.info(test_name + str(permission))
        (name, source_db_url)=self.source_url(permission, 'DB')
        source_rp_url=source_db_url + '/_internal/rps'
        response=self.rl.create_retention_policy_for_database(self.chronograf, source_rp_url,  data)
        if response.status_code == 201:
            actual_action=True
        elif response.json().get('code') is not None and response.json().get('code') == 400:
            actual_action = False
        assert actual_action == action, self.mylog.info(test_name + ' : Assertion Error')
        self.footer(test_name)

    # user with ReadData and CreateDatabase should be able to view RP
    # https://github.com/influxdata/influxdb/issues/9727
    @pytest.mark.parametrize('permission, action', show_rp_params)
    def test_user_show_rp(self, permission, action):
        '''
        :param permission:
        :param action:
        :return:
        '''
        test_name='test_user_show_rp '
        actual_action=False
        self.header(test_name)
        self.mylog.info(test_name + str(permission))
        (name, source_db_url)=self.source_url(permission, 'DB')
        source_rp_url=source_db_url + '/_internal/rps'
        response=self.rl.get_retention_policies_for_database(self.chronograf, source_rp_url)
        if response.status_code == 200:
            actual_action=True
        elif response.json().get('code') is not None and response.json().get('code') == 400:
            actual_action = False
        assert actual_action == action, self.mylog.info(test_name + ' : Assertion Error')
        self.footer(test_name)

    # user with CreateDatabase permission should be able to alter RP
    # https://github.com/influxdata/influxdb/issues/9727
    @pytest.mark.parametrize('permission, action', create_db_params)
    def test_user_alter_rp(self, permission, action):
        '''
        :param permission:
        :param action:
        :return:
        '''
        test_name='test_user_alter_rp '
        actual_action=False
        rp_to_update='monitor'
        data={'name':rp_to_update, 'duration':'3d', 'replication':2, 'shardDuration':'2h', 'isDefault':False}
        self.header(test_name)
        self.mylog.info(test_name + str(permission))
        (name, source_db_url)=self.source_url(permission, 'DB')
        source_rp_url=source_db_url + '/_internal/rps'
        response=self.rl.patch_retention_policy_for_database(self.chronograf, source_rp_url, rp_to_update, data)
        if response.status_code == 201:
            actual_action=True
        elif response.json().get('code') is not None and response.json().get('code') == 400:
            actual_action = False
        assert actual_action == action, self.mylog.info(test_name + ' : Assertion Error')
        self.footer(test_name)

    # user with DropDatabase permission should be able to drop RP
    @pytest.mark.parametrize('permission, action', drop_db_params)
    def test_user_delete_rp(self, permission, action):
        '''
        :param permission:
        :param action:
        :return:
        '''
        test_name = 'test_user_delete_rp '
        actual_action = False
        # creating the same RP multiple time won't create multiple RP or ERROR's out
        rp_to_create = 'DELETE_RP'
        duration='3d'
        default=False
        replication='2'
        database='_internal'
        data_node=choice(self.data_nodes_ips)

        self.header(test_name)
        self.mylog.info(test_name + str(permission))
        # need to create retention policy as admin_user, admin_pass if auth is enabled
        username, password='',''
        if self.http_auth:
            username=self.admin_user
            password=self.admin_pass
        client=InfluxDBClient(host=data_node,username=username, password=password)
        success=du.create_rp(self, client, rp_to_create, duration, replication, database, default)
        assert success, self.mylog.info(test_name + ' Assertion Error, was not able to create RP')
        (name, source_db_url) = self.source_url(permission, 'DB')
        source_rp_url = source_db_url + '/_internal/rps'
        response = self.rl.delete_retention_policy_for_database(self.chronograf, source_rp_url, rp_to_create)
        if response.status_code == 204:
            # make sure that retention policy was actually dropped.
            ret_policies = client.get_list_retention_policies(database)
            if rp_to_create not in [item['name'] for item in ret_policies]:
                actual_action = True
        elif response.json().get('code') is not None and response.json().get('code') == 400:
            actual_action = False
        assert actual_action == action, self.mylog.info(test_name + ' : Assertion Error')
        self.footer(test_name)

    @pytest.mark.parametrize('permission, action', user_params)
    def test_user_createuser(self, permission, action):
        '''
        :param permission:
        :param action:
        :return:
        '''
        test_name = 'test_user_createuser '
        actual_action = False

        self.header(test_name)
        self.mylog.info(test_name + str(permission))
        (name, source_users_url) = self.source_url(permission, 'USERS')
        data = {'name': name+'_createuser', 'password': name+'_createuser'}
        response = self.rl.create_user(self.chronograf, source_users_url, data)
        if response.status_code == 201:
            actual_action = True
        elif response.json().get('code') is not None and response.json().get('code') == 400:
            actual_action = False
        assert actual_action == action, self.mylog.info(test_name + ' : Assertion Error')
        self.footer(test_name)

    @pytest.mark.parametrize('permission, action', user_params)
    def test_user_deleteuser(self, permission, action):
        '''
        :param permission:
        :param action:
        :return:
        '''
        test_name = 'test_user_deleteuser '
        data_node = choice(self.data_nodes_ips)
        actual_action = False

        self.header(test_name)
        self.mylog.info(test_name + str(permission))
        user_name, user_password=permission+'_deleteuser', permission+'_deleteuser'
        username, password = '', ''
        if self.http_auth:
            username = self.admin_user
            password = self.admin_pass
        client = InfluxDBClient(host=data_node, username=username, password=password)
        (name, source_users_url) = self.source_url(permission, 'USERS')
        success=uu.create_user(self, client, user_name, user_password, False)
        assert success, self.mylog.info(test_name + ' : Assertion Error')
        response=self.rl.delete_user(self.chronograf, source_users_url, user_name)
        if response.status_code == 204:
            # TODO add verification that user indeed was deleted
            actual_action = True
        elif response.json().get('code') is not None and response.json().get('code') == 400:
            actual_action = False
        assert actual_action == action, self.mylog.info(test_name + ' : Assertion Error')
        self.footer(test_name)