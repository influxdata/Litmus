
import pytest
import src.util.login_util as lu
from src.chronograf.lib import rest_lib
from src.util import sources_util


@pytest.mark.parametrize('create_source', ['user_permissions'], ids=[''], indirect=True)
@pytest.mark.usefixtures( 'delete_created_sources', 'create_source',
                          'cleanup_users', 'setup_users' ,'create_sources_for_test_users')
class TestUserPermissions(object):
    '''
    delete_created_sources - delete all of the sources created by the tests,
                                            with the exception of ones created by pcl installer
    create_source - to create a source for admin_user
    cleanup_users - delete created for the test(s) users
    setup_users - create test users
    '''
    mylog=lu.log(lu.get_log_path(), 'w', __name__)
    rl=rest_lib.RestLib(mylog)

    # CreateDatabase permissions is good for Creating databases, create RP, alter RP and View RP
    create_db_params=[('user_ViewAdmin', False), ('user_ViewChronograf', False), ('user_CreateDatabase', True),
                  ('user_CreateUserAndRole', False), ('user_AddRemoveNode', False), ('user_DropDatabase', False),
                  ('user_DropData', False), ('user_ReadData', False), ('user_WriteData', False), ('user_Rebalance', False), ('user_ManageShard', False),
                  ('user_ManageContinuousQuery', False), ('user_ManageQuery', False), ('user_ManageSubscription', False),
                  ('user_Monitor', False), ('user_CopyShard', False), ('user_KapacitorAPI', False), ('user_KapacitorConfigAPI', False)]

    drop_db_params=[('user_ViewAdmin', False), ('user_ViewChronograf', False), ('user_CreateDatabase', False),
                  ('user_CreateUserAndRole', False), ('user_AddRemoveNode', False), ('user_DropDatabase', True),
                  ('user_DropData', False), ('user_ReadData', False), ('user_WriteData', False), ('user_Rebalance', False), ('user_ManageShard', False),
                  ('user_ManageContinuousQuery', False), ('user_ManageQuery', False), ('user_ManageSubscription', False),
                  ('user_Monitor', False), ('user_CopyShard', False), ('user_KapacitorAPI', False), ('user_KapacitorConfigAPI', False)]

    params=[('user_ViewAdmin', False), ('user_ViewChronograf', False), ('user_CreateDatabase', False),
                  ('user_CreateUserAndRole', False), ('user_AddRemoveNode', False), ('user_DropDatabase', True),
                  ('user_DropData', False), ('user_ReadData', False), ('user_WriteData', False), ('user_Rebalance', False), ('user_ManageShard', False),
                  ('user_ManageContinuousQuery', False), ('user_ManageQuery', False), ('user_ManageSubscription', False),
                  ('user_Monitor', False), ('user_CopyShard', False), ('user_KapacitorAPI', False), ('user_KapacitorConfigAPI', False)]

    ################## Helper methods ##########################
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
        (name, source_db_url)=self.source_url(permission, 'DB')
        response=self.rl.create_database(self.chronograf, source_db_url, {'name':name})
        if response.status_code == 201:
            actual_action=True
        elif response.json().get('code') is not None and response.json().get('code') == 400:
            actual_action = False
        assert actual_action == action, self.mylog.info('test_user_create_database : Assertion Error')
        self.footer('test_user_create_database')

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
        data={'name':'test_user_create_rp', 'duration':'1d', 'replication':2, 'shardDuration':'2h', 'isDefault':False}
        (name, source_db_url)=self.source_url(permission, 'DB')
        source_rp_url=source_db_url + '/_internal/rps'
        response=self.rl.create_retention_policy_for_database(self.chronograf, source_rp_url,  data)
        if response.status_code == 201:
            actual_action=True
        elif response.json().get('code') is not None and response.json().get('code') == 400:
            actual_action = False
        assert actual_action == action, self.mylog.info('test_user_create_database : Assertion Error')
        self.footer('test_user_create_rp')

    @pytest.mark.skip
    def test_user_show_rp(self):
        self.header('test_user_show_rp')
        self.footer('test_user_show_rp')

    @pytest.mark.skip
    def test_user_alter_rp(self):
        self.header('test_user_alter_rp')
        self.footer('test_user_alter_rp')

