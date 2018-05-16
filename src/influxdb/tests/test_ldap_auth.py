
from random import choice
from src.util import users_util as uu
from src.util import database_util as du
from influxdb import InfluxDBClient as InfluxDBClient
from src.influxdb.lib import influxdb_rest_lib
import src.util.login_util as lu
import pytest
import math
import datetime

# any user that belongs to X_lastnames AD group is an admin user
LDAP_ADMIN_USERS='sal.xu'
LDAP_ADMIN_PASS='p@ssw0rd'

ADMIN_USER='ione.xander'
NON_ADMIN_USER='bill.culleton'

users=['non_existing_user', ADMIN_USER, NON_ADMIN_USER]
permissions=['READ', 'WRITE', 'ALL']
ids=['NON EXISTING USER','ADMIN USER', 'NON ADMIN USER']

single_role_users=[('a_first','annika.sapinski'), # CreateDatabase
                   ('b_first','byron.rons'), # DropDatabase'
                   ('c_first','cythia.udoh'), # CreateUserAndRole
                   ('d_first','dylan.trigueros'), # ManageSubscription
                   ('e_first','ezra.topinka'), # ManageContinuousQuery
                   ('f_first','fumiko.wiss'), # DropData
                   ('g_first','gwyn.wait'), # ManageShard
                   ('h_first','hyun.werley'), # ManageQuery
                   ('i_first','izola.triche'), # Monitor
                   ('j_first','jutta.vicenteno'), # ReadData
                   ('k_first','kyong.nap'), # WriteData
                   ('l_first','lynwood.vanboerum') # No Permissions
]

single_role_users_ids=['CreateDatabase Role-%s' % single_role_users[0][1],
                       'DropDatabase Role-%s' % single_role_users[1][1],
                       'CreateUserAndRole Role-%s' % single_role_users[2][1],
                       'ManageSubscription Role-%s' % single_role_users[3][1],
                       'ManageContinousQuery Role-%s' % single_role_users[4][1],
                       'DropData Role-%s' % single_role_users[5][1],
                       'ManageShard Role-%s' % single_role_users[6][1],
                       'ManageQuery Role-%s' % single_role_users[7][1],
                       'Monitor Role-%s' % single_role_users[8][1],
                       'ReadData Role-%s' % single_role_users[9][1],
                       'WriteData Role-%s' % single_role_users[10][1],
                       'No Permissions-%s' % single_role_users[11][1]
]

# generate test data
def gen_test_data(measurement):
    '''
    :return:
    '''
    points=[]
    for entry in range(0, 100):
        y = 10 + math.sin(math.radians(entry)) * 10
        point = {
            "measurement": measurement,
            "time": int(datetime.datetime.now().strftime('%s')) + entry,
            "fields": {
                "value": y
            },
            "tags": {
                "id": entry,
            }
        }
        points.append(point)
    return points

@pytest.mark.usefixtures('data_nodes_ips','kapacitor')
class TestLdapAdminUser(object):
    '''
    :param delete_roles fixture:
    :param setup_roles_permissions fixture:
    :param data_nodes_ips fixture:
    '''
    mylog = lu.log(lu.get_log_path(), 'w', __name__)
    irl=influxdb_rest_lib.InfluxDBInfluxDBRestLib(mylog)

    ####################################################################################################################

    def header(self, test_name):
        self.mylog.info('#######################################################')
        self.mylog.info('<--------------- %s START --------------->' % test_name)
        self.mylog.info('#######################################################')

    def footer(self, test_name):
        self.mylog.info('#######################################################')
        self.mylog.info('<--------------- %s END --------------->' % test_name)
        self.mylog.info('#######################################################')
        self.mylog.info('')

    ########################################### Admin User Permissions Test Cases ######################################

    #***************************************** CreateUserAndRolePermission *********************************************
    def test_admin_create_user(self):
        '''

        '''
        test_name='test_admin_create_user '
        data_node=choice(self.data_nodes_ips)
        client=InfluxDBClient(data_node,username=LDAP_ADMIN_USERS, password=LDAP_ADMIN_PASS, timeout=3, retries=1)
        user_to_create, password_to_create='test_create_user','test_create_password'
        error_message='creating users is disallowed when ldap is enabled'

        self.header(test_name)
        (success, message)=uu.create_user(self, client, user_to_create, password_to_create, admin=False)
        assert success is False, self.mylog.info(test_name + 'Assertion Error CREATE_USER returned True')
        assert message == error_message, \
            self.mylog.info(test_name + ' Expected Error message :' + error_message +
                            ' is different from actual : ' + message)
        self.footer(test_name)

    @pytest.mark.parametrize('user', users, ids=ids)
    def test_admin_delete_users(self, user):
        '''

        '''
        test_name='test_admin_delete_users_' + user + ' '
        data_node=choice(self.data_nodes_ips)
        client=InfluxDBClient(data_node, username=LDAP_ADMIN_USERS, password=LDAP_ADMIN_PASS, timeout=3, retries=1)
        error_message='dropping users is disallowed when ldap is enabled'

        self.header(test_name)
        (success, message)=uu.delete_user(self, client, user)
        assert success is False, self.mylog.info(test_name + 'Assertion Error DELETE_USER returned True')
        assert message == error_message, \
            self.mylog.info(test_name + 'Expected Error message :' + error_message +
                            ' is different from actual : ' + message)
        self.footer(test_name)

    @pytest.mark.parametrize('user', users, ids=ids)
    @pytest.mark.parametrize('permission', permissions)
    def test_admin_grant_privilege(self, user, permission):
        '''

        '''
        test_name='test_admin_grant_privilege_' + user + ' '
        data_node=choice(self.data_nodes_ips)
        database='_internal'
        client=InfluxDBClient(data_node, username=LDAP_ADMIN_USERS, password=LDAP_ADMIN_PASS, timeout=1, retries=1)
        error_message='modifying user privileges is disallowed when ldap is enabled'

        self.header(test_name)
        (success, message)=uu.grant_privilege(self, client, permission, database, user)
        assert success is False, self.mylog.info(test_name + 'Assertion Error GRANT PRIVILEGE returned True')
        assert message == error_message, \
            self.mylog.info(test_name + ' Expected Error message :' + error_message +
                            ' is different from actual : ' + message)
        self.footer(test_name)

    @pytest.mark.parametrize('user', users, ids=ids)
    def test_admin_grant_admin_privileges(self, user):
        '''

        '''
        test_name='test_admin_grant_admin_privileges_' + user + ' '
        data_node=choice(self.data_nodes_ips)
        client=InfluxDBClient(data_node, username=LDAP_ADMIN_USERS, password=LDAP_ADMIN_PASS, timeout=1, retries=1)
        error_message='setting admin privileges is disallowed when ldap is enabled'

        self.header(test_name)
        (success, message)=uu.grant_admin_privileges(self, client, user)
        assert success is False, self.mylog.info(test_name + 'Assertion Error GRANT ADMIN PRIVILEGE returned True')
        assert message == error_message, \
            self.mylog.info(test_name + ' Expected Error message :' + error_message +
                            ' is different from actual : ' + message)
        self.footer(test_name)

    # https://github.com/influxdata/plutonium/issues/2454
    @pytest.mark.parametrize('user', users, ids=ids)
    @pytest.mark.parametrize('permission', permissions)
    def test_admin_revoke_privilege(self, user, permission):
        '''

        '''
        test_name='test_admin_revoke_privilege_' + user + ' '
        data_node=choice(self.data_nodes_ips)
        database='_internal'
        client=InfluxDBClient(data_node, username=LDAP_ADMIN_USERS, password=LDAP_ADMIN_PASS, timeout=1, retries=1)
        error_message='modifying user privileges is disallowed when ldap is enabled'
        error_message_user_doesnot_exist='user not found'
        self.header(test_name)
        (success, message)=uu.revoke_privilege(self, client, permission, database, user)
        assert success is False, self.mylog.info(test_name + 'Assertion Error REVOKE PRIVILEGE returned True')
        if user == 'non_existing_user':
            assert message == error_message_user_doesnot_exist, pytest.xfail(reason='LDAP error message should overwrite user does not exist message')
        else:
            assert message == error_message, self.mylog.info(test_name + ' Expected Error message :' + error_message +
                                                        ' is different from actual : ' + message)
        self.footer(test_name)

    # https://github.com/influxdata/plutonium/issues/2454
    @pytest.mark.parametrize('user', users, ids=ids)
    def test_admin_revoke_admin_privileges(self, user):
        '''

        '''
        test_name='test_admin_revoke_admin_privileges_' + user + ' '
        data_node=choice(self.data_nodes_ips)
        client=InfluxDBClient(data_node, username=LDAP_ADMIN_USERS, password=LDAP_ADMIN_PASS, timeout=1, retries=1)
        error_message='revoking admin privileges is disallowed when ldap is enabled'

        self.header(test_name)
        (success, message)=uu.revoke_admin_privileges(self, client, user)
        assert success is False, self.mylog.info(test_name + 'Assertion Error REVOKE ADMIN PRIVILEGE returned True')
        assert message == error_message, pytest.xfail(reason='Wrong Error Message: setting instead of revoking')
            #self.mylog.info(test_name + ' Expected Error message :' + error_message +
            #                ' is different from actual : ' + message)
        self.footer(test_name)

    @pytest.mark.parametrize('user', users, ids=ids)
    def test_admin_set_password(self, user):
        '''

        '''
        test_name='test_admin_set_password_' + user + ' '
        password='p@ssw0rd'
        data_node=choice(self.data_nodes_ips)
        client=InfluxDBClient(data_node, username=LDAP_ADMIN_USERS, password=LDAP_ADMIN_PASS, timeout=3, retries=1)
        error_message='updating users is disallowed when ldap is enabled'

        self.header(test_name)
        (success, message)=uu.set_user_password(self, client, user, password)
        assert success is False, self.mylog.info(test_name + 'Assertion Error SET PASSWORD FOR USER returned True')
        assert message == error_message, \
            self.mylog.info(test_name + ' Expected Error message :' + error_message +
                            ' is different from actual : ' + message)
        self.footer(test_name)

    def test_admin_show_users(self):
        '''

        '''
        test_name = 'test_admin_show_users '
        expected_number_of_users=5000
        data_node = choice(self.data_nodes_ips)
        client = InfluxDBClient(data_node, username=LDAP_ADMIN_USERS, password=LDAP_ADMIN_PASS, timeout=3, retries=1)

        self.header(test_name)
        (success, list_of_users)=uu.show_users(self, client)
        assert success is True, self.mylog.info(test_name + 'Assertion Error getting users')
        assert expected_number_of_users == len(list_of_users), pytest.xfail(reason='SHOW USERS does not work with LDAP')
            #self.mylog.info(test_name + ' Expected number of users :' + str(expected_number_of_users) +
            #                ' is different from actual : ' + str(len(list_of_users)))
        self.footer(test_name)

    @pytest.mark.parametrize('user', users, ids=ids)
    def test_admin_show_grants(self, user):
        '''
        :param user:
        :return:
        '''
        test_name='test_admin_show_grants_' + user + ' '
        data_node=choice(self.data_nodes_ips)
        client=InfluxDBClient(data_node, username=LDAP_ADMIN_USERS, password=LDAP_ADMIN_PASS, timeout=1, retries=1)
        self.header(test_name)
        (success, user_grants)=uu.show_grants(self, client, user)
        if user == ADMIN_USER:
            assert success, test_name + 'Assertion Error SHOW GRANTS FOR %s' % user
            assert len(user_grants) == 2, test_name + 'Assertion Error for %s user' % user
        elif user == NON_ADMIN_USER:
            assert success, test_name + 'Assertion Error SHOW GRANTS FOR %s' % user
            assert len(user_grants) == 0, test_name + 'Assertion Error for %s user' % user
        elif user == 'non_existing_user':
            assert success == False, test_name + 'Assertion Error SHOW GRANTS FOR %s' % user
            assert len(user_grants) == 0, test_name + 'Assertion Error for %s user' % user
        self.footer(test_name)

    #******************************************* CreateDatabase Permission *********************************************
    @pytest.mark.parametrize('drop_database', ['test_admin_create_db'], ids=[''], indirect=True)
    @pytest.mark.usefixtures('drop_database')
    def test_admin_create_database(self):
        '''
        '''
        test_name = 'test_admin_create_database '
        data_node = choice(self.data_nodes_ips)
        database = 'test_admin_create_db'
        self.header(test_name)
        self.mylog.info(test_name + 'Creating InfluxDBClient data_node=%s, username=%s, password=%s' %
                        (data_node, LDAP_ADMIN_USERS, LDAP_ADMIN_PASS))
        client=InfluxDBClient(data_node, username=LDAP_ADMIN_USERS, password=LDAP_ADMIN_PASS, timeout=3, retries=1)
        (success, error)=du.create_database(self, client, database)
        assert success, test_name + 'Failed to create database for admin user=%s' % LDAP_ADMIN_USERS
        self.footer(test_name)

    @pytest.mark.parametrize('create_database', ['test_admin_creat_retention_policy_db'], ids=[''], indirect=True)
    @pytest.mark.usefixtures('create_database')
    def test_admin_create_retention_policy(self):
        '''
        '''
        test_name = 'test_admin_create_retention_policy '
        data_node = choice(self.data_nodes_ips)
        database = 'test_admin_creat_retention_policy_db'
        self.header(test_name)
        self.mylog.info(test_name + 'Creating InfluxDBClient data_node=%s, username=%s, password=%s' %
                        (data_node, LDAP_ADMIN_USERS, LDAP_ADMIN_PASS))
        client=InfluxDBClient(data_node, username=LDAP_ADMIN_USERS, password=LDAP_ADMIN_PASS, timeout=3, retries=1)
        (success, error)=du.create_retention_policy(self, client, rp_name='%s_policy_name' % LDAP_ADMIN_USERS,
                                                    duration='1h', replication='2', database=database, default=True)
        assert success, test_name + 'Failed to create retention policy for user=%s' % LDAP_ADMIN_USERS
        self.footer(test_name)

    @pytest.mark.parametrize('create_database', ['test_admin_view_retention_policy_db'], ids=[''], indirect=True)
    @pytest.mark.usefixtures('create_database')
    def test_admin_view_retention_policy(self):
        '''
        '''
        test_name='test_admin_view_retention_policy '
        data_node=choice(self.data_nodes_ips)
        database='test_admin_view_retention_policy_db'
        rp_name='admin_view_retention_policy'
        rp_duration='3h0m0s'
        rp_replication='2'
        self.header(test_name)
        self.mylog.info(test_name + 'Creating InfluxDBClient data_node=%s, username=%s, password=%s' %
                        (data_node, LDAP_ADMIN_USERS, LDAP_ADMIN_PASS))
        client_admin=InfluxDBClient(data_node, username=LDAP_ADMIN_USERS, password=LDAP_ADMIN_PASS, timeout=3,
                                      retries=1)
        (success, errormessage)=du.create_retention_policy(self, client_admin, rp_name=rp_name, duration=rp_duration,
                                                        replication=rp_replication, database=database, default=True)
        assert success, test_name + 'unable to create retention policy ' + str(errormessage)
        (success, rp_dic, error) = du.show_retention_policies(self, client_admin, database)
        assert success, 'unable to view retention policies for %s, error=%s' % (database, str(error))
        retention_policy = du.get_retention_policy(self, rp_dic, rp_name)
        self.mylog.info(test_name + 'retention policy = ' + str(retention_policy))
        duration = du.get_retention_policy_duration(self, retention_policy)
        self.mylog.info(test_name + 'assert actual duraiton %s equals to expected duration %s'
                                                                    % (duration, rp_duration))
        assert duration == rp_duration
        replication = du.get_retention_policy_replication(self, retention_policy)
        self.mylog.info(test_name + 'assert actual replication %s equals to expected replicaiton %s'
                                                                    % (replication, rp_replication))
        assert str(replication) == rp_replication
        shard_group_duration = du.get_retention_policy_shard_group_duration(self, retention_policy)
        self.mylog.info(test_name + 'assert actual shard duration %s equals to expected shard duration 1h'
                                                                    % (shard_group_duration))
        assert shard_group_duration == '1h0m0s'
        self.footer(test_name)

    @pytest.mark.parametrize('create_database', ['test_admin_alter_retention_policy_db'], ids=[''], indirect=True)
    @pytest.mark.usefixtures('create_database')
    def test_admin_alter_retention_policy(self):
        '''

        '''
        test_name = 'test_admin_alter_retention_policy '
        data_node = choice(self.data_nodes_ips)
        database = 'test_admin_alter_retention_policy_db'
        rp_name = 'admin_alter_retention_policy'
        rp_duration = '5h0m0s'
        alter_rp_duration = '10h0m0s'
        rp_replication = '2'
        self.header(test_name)
        self.mylog.info(test_name + 'Creating InfluxDBClient data_node=%s, username=%s, password=%s' %
                        (data_node, LDAP_ADMIN_USERS, LDAP_ADMIN_PASS))
        client_admin=InfluxDBClient(data_node, username=LDAP_ADMIN_USERS, password=LDAP_ADMIN_PASS, timeout=3,
                                        retries=1)
        (success, error_message)=du.create_retention_policy(self, client_admin, rp_name=rp_name, duration=rp_duration,
                                        replication=rp_replication, database=database, default=True)
        assert success, test_name + 'unable to create retention policy ' + str(error_message)
        (success, error_message)=du.alter_retention_policy(self, client_admin, rp_name, database,
                                                           duration=alter_rp_duration)
        assert success, test_name + 'unable to alter retention policies for %s, error=%s' \
                        % (database, str(error_message))
        (success, rp_dic, error_message)=du.show_retention_policies(self, client_admin, database)
        assert success, test_name + 'unable to view retention policies for %s, error=%s'\
                        % (database, str(error_message))
        retention_policy=du.get_retention_policy(self, rp_dic, rp_name)
        duration=du.get_retention_policy_duration(self, retention_policy)
        self.mylog.info(test_name + 'assert actual duraiton %s equals to expected duration %s'
                            % (duration, alter_rp_duration))
        assert duration == alter_rp_duration

    #***************************************** DropDatabase Permissions ************************************************
    # DropDatabase permission for AdminUser is covered by using 'drop_database' fixture
    @pytest.mark.parametrize('create_database', ['test_admin_drop_retention_policy_db'], ids=[''], indirect=True)
    @pytest.mark.usefixtures('create_database')
    def test_admin_drop_retention_policy(self):
        '''
        STEP 1: Creating InfluxDBClient
        STEP 2: Creating retention policy
        STEP 3: Dropping retention
        STEP 4: Show retention policies for database
        STEP 5: Verify database does not have the retention policy
        '''
        test_name='test_admin_drop_retention_policy '
        data_node=choice(self.data_nodes_ips)
        database='test_admin_drop_retention_policy_db'
        rp_name='admin_drop_retention_policy'
        rp_duration='3h0m0s'
        rp_replication='2'
        self.header(test_name)
        self.mylog.info(test_name + 'STEP 1: Creating InfluxDBClient data_node=%s, username=%s, password=%s' %
                        (data_node, LDAP_ADMIN_USERS, LDAP_ADMIN_PASS))
        client_admin=InfluxDBClient(data_node, username=LDAP_ADMIN_USERS, password=LDAP_ADMIN_PASS, timeout=3,
                                      retries=1)
        self.mylog.info(test_name + 'STEP 2: Creating retention policy %s with duration %s and replication %s'
                        % (rp_name, rp_duration, rp_replication))
        (success, errormessage)=du.create_retention_policy(self, client_admin, rp_name=rp_name, duration=rp_duration,
                                                           replication=rp_replication, database=database, default=True)
        assert success, self.mylog.info(test_name + 'unable to create retention policy ' + str(errormessage))
        self.mylog.info(test_name + 'STEP 3: Dropping retention policy %s' % rp_name)
        (success, errormessage)=du.drop_retention_policies(self, client_admin, database, rp_name)
        assert success, self.mylog.info(test_name + 'unable to drop retention policy ' + str(errormessage))
        self.mylog.info(test_name + 'STEP 4: Show retention policies for database %s' % database)
        (success, retention_policies_d, error_message)=du.show_retention_policies(self, client_admin, database)
        assert success, self.mylog.info(test_name + 'unable to get retention policies for database %s' % database)
        self.mylog.info(test_name + 'STEP 5: Verify database does not have the retention policy %s' % rp_name)
        result=du.get_retention_policy(self, retention_policies_d, rp_name)
        assert result == None, self.mylog.info(test_name + ' retention policy %s still could be found' % rp_name)
        self.footer(test_name)

    #****************************************** ManageSubscription Permission ******************************************
    @pytest.mark.parametrize('create_database', ['test_admin_create_subscription_db'], ids=[''], indirect=True)
    @pytest.mark.usefixtures('create_database')
    def test_admin_create_subscription(self):
        '''

        '''
        test_name='test_admin_create_subscription '
        database='test_admin_create_subscription_db'
        retention_policy='autogen'
        mode='ALL'
        destinations='\''+self.kapacitor+'\''
        data_node='http://'+choice(self.data_nodes_ips)+':8086'
        self.header(test_name)
        (success, message)=self.irl.create_subscription(data_node, test_name, database,
                                        retention_policy, mode, destinations, auth=(LDAP_ADMIN_USERS, LDAP_ADMIN_PASS))
        assert success, self.mylog.info(test_name + 'unable to create subscription, error=%s' % message)
        self.footer(test_name)

    @pytest.mark.parametrize('create_database', ['test_admin_drop_subscription_db'], ids=[''], indirect=True)
    @pytest.mark.usefixtures('create_database')
    def test_admin_drop_subscription(self):
        '''

        '''
        test_name='test_admin_drop_subscription'
        database='test_admin_drop_subscription_db'
        retention_policy='autogen'
        mode='ALL'
        destinations = '\'' + self.kapacitor + '\''
        data_node='http://'+choice(self.data_nodes_ips)+':8086'
        self.header(test_name)
        (success, message)=self.irl.create_subscription(data_node, test_name, database,
                                        retention_policy, mode, destinations, auth=(LDAP_ADMIN_USERS, LDAP_ADMIN_PASS))
        assert success, self.mylog.info(test_name + ' unable to create subscription, error=%s' % message)
        (success, message)=self.irl.drop_subscription(data_node, test_name, database, retention_policy,
                                                      auth=(LDAP_ADMIN_USERS, LDAP_ADMIN_PASS))
        assert success, self.mylog.info(test_name + ' unable to drop subscription, error=%s' % message)
        self.footer(test_name)

    @pytest.mark.parametrize('create_database', ['test_admin_show_subscriptions_db'], ids=[''], indirect=True)
    @pytest.mark.usefixtures('create_database')
    def test_admin_show_subscriptions(self):
        '''

        '''
        test_name='test_admin_show_subscriptions '
        database='test_admin_show_subscriptions_db'
        retention_policy='autogen'
        mode='ALL'
        destinations=self.kapacitor
        data_node='http://'+choice(self.data_nodes_ips)+':8086'
        self.header(test_name)
        (success, message)=self.irl.create_subscription(data_node, test_name, database,
                                        retention_policy, mode, '\''+destinations+'\'', auth=(LDAP_ADMIN_USERS, LDAP_ADMIN_PASS))
        assert success, self.mylog.info(test_name + 'unable to create subscription, error=%s' % message)
        (success, subscriptions, message)=self.irl.show_subscriptions(data_node,
                                                                      auth=(LDAP_ADMIN_USERS, LDAP_ADMIN_PASS))
        assert success, self.mylog.info(test_name + 'unable to view subscriptions, error=%s' % message)
        actual_destination=subscriptions.get(database).get(test_name)['destination'][0]
        self.mylog.info(test_name + 'assert actual destination \'' + str(actual_destination) + '\' equals '
                        + str(destinations))
        assert actual_destination == destinations
        actual_rp=subscriptions.get(database).get(test_name)['rp']
        self.mylog.info(test_name + 'assert actual retention policy \'' + str(actual_rp) + '\' equals '
                        + str(retention_policy))
        assert actual_rp == retention_policy
        actual_mode=subscriptions.get(database).get(test_name)['mode']
        self.mylog.info(test_name + 'assert actual mode \'' + str(actual_mode) + '\' equals '
                        + str(mode))
        assert actual_mode == mode
        self.footer(test_name)

    #*************************************** DropData Parmissions ******************************************************
    @pytest.mark.parametrize('create_database', ['test_admin_drop_measurement_db'], ids=[''], indirect=True)
    @pytest.mark.usefixtures('create_database')
    def test_admin_drop_measurement(self):
        '''

        '''
        test_name='test_admin_drop_measurement '
        database='test_admin_drop_measurement_db'
        data_node = choice(self.data_nodes_ips)
        measurement='testm'
        self.header(test_name)
        self.mylog.info(test_name + 'STEP 1: Creating InfluxDBClient data_node=%s, username=%s, password=%s' %
                        (data_node, LDAP_ADMIN_USERS, LDAP_ADMIN_PASS))
        client_admin = InfluxDBClient(data_node, username=LDAP_ADMIN_USERS, password=LDAP_ADMIN_PASS,
                                      database=database, timeout=3, retries=1)
        self.mylog.info(test_name + 'STEP 2: Generate test data')
        points=gen_test_data(measurement)
        self.mylog.info(test_name + 'STEP 3: Write points to the database')
        result=du.write_points(self, client_admin, points=points, time_precision='s', database=database)
        assert result, self.mylog.info(test_name + 'Failed to write points into database')
        self.mylog.info(test_name + 'STEP 4: get created measurement')
        (success, result, error)=du.list_measurements(self, client_admin)
        assert success, self.mylog.info(test_name + 'Failed to get measurements ' + str(error))
        assert measurement in result, self.mylog.info(test_name + 'Created measurement was not found')
        self.mylog.info(test_name + 'STEP 5: drop_measurement %s' % measurement)
        (success, error_measurement)=du.drop_measurement(self, client_admin, measurement)
        assert success, self.mylog.info(test_name + 'Failed to drop measurement' + str(error_measurement))
        self.mylog.info(test_name + 'STEP 6: get measurements')
        (success, result, error) = du.list_measurements(self, client_admin)
        assert success, self.mylog.info(test_name + 'Failed to get measurements ' + str(error))
        self.mylog.info(test_name + 'STEP 7: Assert measurement was deleted')
        assert measurement not in result, self.mylog.info(test_name + 'Measurement still can be found')
        self.footer(test_name)

    @pytest.mark.parametrize('create_database', ['test_admin_drop_series_db'], ids=[''], indirect=True)
    @pytest.mark.usefixtures('create_database')
    def test_admin_drop_series(self):
        '''

        '''
        test_name='test_admin_drop_series '
        database='test_admin_drop_series_db'
        data_node=choice(self.data_nodes_ips)
        measurement='test_drop_series'
        series_to_delete=measurement+',id=17'
        self.header(test_name)
        self.mylog.info(test_name + 'STEP 1: Creating InfluxDBClient data_node=%s, username=%s, password=%s' %
                        (data_node, LDAP_ADMIN_USERS, LDAP_ADMIN_PASS))
        client_admin=InfluxDBClient(data_node, username=LDAP_ADMIN_USERS, password=LDAP_ADMIN_PASS,
                                      database=database, timeout=3, retries=1)
        self.mylog.info(test_name + 'STEP 2: Generate test data')
        points=gen_test_data(measurement)
        self.mylog.info(test_name + 'STEP 3: Write points to the database')
        result=du.write_points(self, client_admin, points=points, time_precision='s', database=database)
        assert result, self.mylog.info(test_name + 'Failed to write points into database')
        self.mylog.info(test_name + 'STEP 4: get series for the %s' % database)
        (success, series, error)=du.list_series(self, client_admin, database)
        assert success, self.mylog.info(test_name + 'Failed to get series ' + str(error))
        assert series_to_delete in series, self.mylog.info(test_name + 'Series was not found')
        self.mylog.info(test_name + 'STEP 5: drop series %s' % series_to_delete)
        # only one measurement is in the database, so deleting one series
        (success, error_series)=du.drop_series(self, client_admin, database=database,
                                                 measurement=measurement, tags={'id':'17'})
        assert success, self.mylog.info(test_name + 'Failed to drop series' + str(error_series))
        self.mylog.info(test_name + 'STEP 6: get series')
        (success, series, error)=du.list_series(self, client_admin, database)
        assert success, self.mylog.info(test_name + 'Failed to get series ' + str(error))
        self.mylog.info(test_name + 'STEP 7: Assert series were dropped')
        assert series_to_delete not in series, self.mylog.info(test_name + 'Series still can be found')
        self.footer(test_name)

    @pytest.mark.parametrize('create_database', ['test_admin_delete_series_db'], ids=[''], indirect=True)
    @pytest.mark.usefixtures('create_database')
    def test_admin_delete_series(self):
        '''

        '''
        test_name = 'test_admin_delete_series '
        database = 'test_admin_delete_series_db'
        data_node = choice(self.data_nodes_ips)
        measurement = 'test_delete_series'
        series_to_delete = measurement + ',id=27'
        self.header(test_name)
        self.mylog.info(test_name + 'STEP 1: Creating InfluxDBClient data_node=%s, username=%s, password=%s' %
                        (data_node, LDAP_ADMIN_USERS, LDAP_ADMIN_PASS))
        client_admin=InfluxDBClient(data_node, username=LDAP_ADMIN_USERS, password=LDAP_ADMIN_PASS,
                                      database=database, timeout=3, retries=1)
        self.mylog.info(test_name + 'STEP 2: Generate test data')
        points=gen_test_data(measurement)
        self.mylog.info(test_name + 'STEP 3: Write points to the database')
        result=du.write_points(self, client_admin, points=points, time_precision='s', database=database)
        assert result, self.mylog.info(test_name + 'Failed to write points into database')
        self.mylog.info(test_name + 'STEP 4: get series for the %s' % database)
        (success, series, error)=du.list_series(self, client_admin, database)
        assert success, self.mylog.info(test_name + 'Failed to get series ' + str(error))
        assert series_to_delete in series, self.mylog.info(test_name + 'Series was not found')
        self.mylog.info(test_name + 'STEP 5: delete series %s' % series_to_delete)
        # only one measurement is in the database, so deleting one series
        (success, result, error)=du.delete_series(self, client_admin, database=database,
                                                  measurement=measurement, tags={'id': '27'})
        assert success, self.mylog.info(test_name + 'Failed to delete series ' + str(error))
        assert len(result.items()) == 0, \
            self.mylog.info(test_name + 'Failed to delete series ' + str(error))
        self.mylog.info(test_name + 'STEP 6: get series')
        (success, series, error)=du.list_series(self, client_admin, database)
        assert success, self.mylog.info(test_name + 'Failed to get series ' + str(error))
        self.mylog.info(test_name + 'STEP 7: Assert series was deleted')
        assert series_to_delete not in series, self.mylog.info(test_name + 'Series still can be found')
        self.footer(test_name)

########################################################################################################################
########################################################################################################################


@pytest.mark.usefixtures('delete_roles', 'setup_roles_permissions', 'data_nodes_ips', 'kapacitor')
class TestLdapUser(object):
    '''
    :param delete_roles fixture:
    :param setup_roles_permissions fixture:
    :param data_nodes_ips fixture:
    '''
    mylog = lu.log(lu.get_log_path(), 'w', __name__)
    irl = influxdb_rest_lib.InfluxDBInfluxDBRestLib(mylog)

    ####################################################################################################################

    def header(self, test_name):
        self.mylog.info('#######################################################')
        self.mylog.info('<--------------- %s START --------------->' % test_name)
        self.mylog.info('#######################################################')

    def footer(self, test_name):
        self.mylog.info('#######################################################')
        self.mylog.info('<--------------- %s END --------------->' % test_name)
        self.mylog.info('#######################################################')
        self.mylog.info('')
    ######################################## Non-Admin Users Test Cases ################################################

    #************************************ CreateDatabase permission Test Cases ****************************************#

    @pytest.mark.parametrize('drop_database',['test_create_db'], ids=[''], indirect=True)
    @pytest.mark.usefixtures('drop_database')
    @pytest.mark.parametrize('role, user', single_role_users, ids=single_role_users_ids)
    def test_user_create_database(self, role, user):
        '''

        '''
        test_name = 'test_user_create_database_' + user + ' '
        data_node = choice(self.data_nodes_ips)
        database='test_create_db'
        error_message='error authorizing query: %s not authorized to execute statement \'CREATE DATABASE %s\'' \
                      % (user, database)
        self.header(test_name)
        self.mylog.info(test_name + 'Creating InfluxDBClient data_node=%s, username=%s, password=%s' %
                        (data_node, user, LDAP_ADMIN_PASS))
        client = InfluxDBClient(data_node, username=user, password=LDAP_ADMIN_PASS, timeout=3, retries=1)
        (success, error)=du.create_database(self, client, database)
        if role == 'a_first':
            assert success, \
                self.mylog.info(test_name + 'Failed to create database for user=%s and role=%s' % (user, role))
        else:
            assert success == False, \
                self.mylog.info(test_name + '%s was able to create database, %s' % (user, role))
            assert error_message in error, \
                self.mylog.info(test_name + 'expected error message is different from actual')
        self.footer(test_name)

    @pytest.mark.parametrize('create_database', ['test_creat_retention_policy_db'], ids=[''], indirect=True)
    @pytest.mark.usefixtures('create_database')
    @pytest.mark.parametrize('role, user', single_role_users, ids=single_role_users_ids)
    def test_user_create_retention_policy(self, role, user):
        '''
        :return:
        '''

        test_name='test_user_create_retention_policy_' + user + ' '
        data_node=choice(self.data_nodes_ips)
        database='test_creat_retention_policy_db'
        error_message='error authorizing query: %s not authorized to execute statement ' \
              '\'CREATE RETENTION POLICY \\"%s_policy_name\\" ON %s DURATION 1h REPLICATION 2 DEFAULT\'' \
                      % (user, user, database)
        self.header(test_name)
        self.mylog.info(test_name + 'Creating InfluxDBClient data_node=%s, username=%s, password=%s' %
                        (data_node, user, LDAP_ADMIN_PASS))
        client=InfluxDBClient(data_node, username=user, password=LDAP_ADMIN_PASS, timeout=3, retries=1)
        (success, error)=du.create_retention_policy(self, client, rp_name='%s_policy_name' % user, duration='1h',
                                                    replication='2', database=database, default=True)
        if role == 'a_first':
            assert success, \
                self.mylog.info(test_name + 'Failed to create retention policy for user=%s and role=%s' % (user, role))
        else:
            assert success == False, \
                self.mylog.info(test_name + '%s was able to create retention policy,role=%s' % (user, role))
            assert error_message in error, \
                self.mylog.info(test_name + 'expected error `message is different from actual')
        self.footer(test_name)

    # https://github.com/influxdata/influxdb/issues/9727
    @pytest.mark.parametrize('create_database', ['test_view_retention_policy_db'], ids=[''], indirect=True)
    @pytest.mark.usefixtures('create_database')
    @pytest.mark.parametrize('role, user', single_role_users, ids=single_role_users_ids)
    def test_user_view_retention_policy(self, role, user):
        '''
        :param role:
        :param user:
        :return:
        '''
        test_name='test_user_view_retention_policy_' + user + ' '
        data_node=choice(self.data_nodes_ips)
        database='test_view_retention_policy_db'
        rp_name='view_retention_policy'
        rp_duration='3h0m0s'
        rp_replication='2'
        error_message='error authorizing query: %s not authorized to execute statement \'SHOW RETENTION POLICIES ON %s\'' \
                      % (user, database)
        self.header(test_name)
        self.mylog.info(test_name + 'Creating InfluxDBClient data_node=%s, username=%s, password=%s' %
                        (data_node, LDAP_ADMIN_USERS, LDAP_ADMIN_PASS))
        client_admin=InfluxDBClient(data_node, username=LDAP_ADMIN_USERS, password=LDAP_ADMIN_PASS, timeout=3, retries=1)
        (success, errormessage)=du.create_retention_policy(self, client_admin, rp_name=rp_name, duration=rp_duration,
                                                            replication=rp_replication, database=database, default=True)
        assert success, self.mylog.info(test_name + 'unable to create retention policy ' + str(error_message))
        self.mylog.info(test_name + 'Creating InfluxDBClient data_node=%s, username=%s, password=%s' %
                        (data_node, user, LDAP_ADMIN_PASS))
        client=InfluxDBClient(data_node, username=user, password=LDAP_ADMIN_PASS, timeout=3, retries=1)
        (success, rp_dic, error)=du.show_retention_policies(self, client, database)
        if role == 'a_first' or role == 'j_first':
            assert success, \
                pytest.xfail(reason='User with CreateDatabase permission cannot view retention policy')
            # 'unable to view retention policies for %s, error=%s' % (database, str(error))
            retention_policy=du.get_retention_policy(self, rp_dic, rp_name)
            self.mylog.info(test_name + 'retention policy = ' + str(retention_policy))
            duration=du.get_retention_policy_duration(self, retention_policy)
            self.mylog.info(test_name + 'assert actual duraiton %s equals to expected duration %s'
                            % (duration, rp_duration))
            assert duration == rp_duration
            replication=du.get_retention_policy_replication(self, retention_policy)
            self.mylog.info(test_name + 'assert actual replication %s equals to expected replicaiton %s'
                            % (replication, rp_replication))
            assert str(replication) == rp_replication
            shard_group_duration=du.get_retention_policy_shard_group_duration(self, retention_policy)
            self.mylog.info(test_name + 'assert actual shard duration %s equals to expected shard duration 1h'
                            % (shard_group_duration))
            assert shard_group_duration == '1h0m0s'
        else:
            assert success == False, \
                self.mylog.info(test_name + 'able to view retention policies for %s, error=%s'
                                % (database, str(error)))
            assert error_message in error, \
                self.mylog.info(test_name + 'expected error `message is different from actual')
        self.footer(test_name)

    @pytest.mark.parametrize('create_database', ['test_alter_retention_policy_db'], ids=[''], indirect=True)
    @pytest.mark.usefixtures('create_database')
    @pytest.mark.parametrize('role, user', single_role_users, ids=single_role_users_ids)
    def test_user_alter_retention_policy(self, role, user):
        '''
        :param role:
        :param users:
        :return:
        '''
        test_name = 'test_user_alter_retention_policy_' + user + ' '
        data_node = choice(self.data_nodes_ips)
        database = 'test_alter_retention_policy_db'
        rp_name = 'alter_retention_policy'
        rp_duration = '5h0m0s'
        alter_rp_duration='10h0m0s'
        rp_replication = '2'
        error_message = 'error authorizing query: %s not authorized to execute statement \'SHOW RETENTION POLICIES ON %s\''
        self.header(test_name)
        self.mylog.info(test_name + 'Creating InfluxDBClient data_node=%s, username=%s, password=%s' %
                        (data_node, LDAP_ADMIN_USERS, LDAP_ADMIN_PASS))
        client_admin=InfluxDBClient(data_node, username=LDAP_ADMIN_USERS, password=LDAP_ADMIN_PASS, timeout=3, retries=1)
        (success, error_message)=du.create_retention_policy(self, client_admin, rp_name=rp_name, duration=rp_duration,
                                                              replication=rp_replication, database=database,
                                                              default=True)
        assert success, self.mylog.info(test_name + 'unable to create retention policy ' + str(error_message))
        self.mylog.info(test_name + 'Creating InfluxDBClient data_node=%s, username=%s, password=%s' %
                        (data_node, user, LDAP_ADMIN_PASS))
        client=InfluxDBClient(data_node, username=user, password=LDAP_ADMIN_PASS, timeout=3, retries=1)
        (success, error_message)=du.alter_retention_policy(self, client, rp_name, database, duration=alter_rp_duration)
        if role == 'a_first':
            assert success, self.mylog.info(test_name + 'unable to alter retention policies for %s, error=%s'
                                        % (database, str(error_message)))
            (success, rp_dic, error_message)=du.show_retention_policies(self, client_admin, database)
            assert success, self.mylog.info(test_name + 'unable to view retention policies for %s, error=%s'
                                        % (database, str(error_message)))
            retention_policy = du.get_retention_policy(self, rp_dic, rp_name)
            duration=du.get_retention_policy_duration(self, retention_policy)
            self.mylog.info(test_name + 'assert actual duraiton %s equals to expected duration %s'
                            % (duration, alter_rp_duration))
            assert duration == alter_rp_duration
        else:
            assert success == False, self.mylog.info(test_name + 'able to alter retention policies for %s, error=%s'
                                        % (database, str(error_message)))

    #************************************* DropDatabase Permission Test Cases *****************************************#
    @pytest.mark.parametrize('create_database', ['test_drop_db'], ids=[''], indirect=True)
    @pytest.mark.usefixtures('create_database')
    @pytest.mark.parametrize('role, user', single_role_users, ids=single_role_users_ids)
    def test_user_drop_database(self, role, user):
        '''

        '''
        test_name = 'test_user_drop_database_' + user + ' '
        data_node = choice(self.data_nodes_ips)
        database='test_drop_db'
        error_message='error authorizing query: %s not authorized to execute statement \'DROP DATABASE %s\'' \
                                                                                                                  % (user, database)
        self.header(test_name)
        self.mylog.info(test_name + 'Creating InfluxDBClient data_node=%s, username=%s, password=%s' %
                        (data_node, user, LDAP_ADMIN_PASS))
        client = InfluxDBClient(data_node, username=user, password=LDAP_ADMIN_PASS, timeout=3, retries=1)
        (success, error)=du.drop_database(self, client, database)
        if role == 'b_first':
            assert success, \
                self.mylog.info(test_name + 'Failed to drop database for user=%s and role=%s' % (user, role))
        else:
            assert success == False, \
                self.mylog.info(test_name + '%s was able to drop database, %s' % (user, role))
            assert error_message in error, \
                self.mylog.info(test_name + 'expected error message is different from actual')
        self.footer(test_name)

    @pytest.mark.parametrize('create_database', ['test_user_drop_retention_policy_db'], ids=[''], indirect=True)
    @pytest.mark.usefixtures('create_database')
    @pytest.mark.parametrize('role, user', single_role_users, ids=single_role_users_ids)
    def test_user_drop_retention_policy(self, role, user):
        '''
        STEP 1: Creating InfluxDBClient
        STEP 2: Creating retention policy
        STEP 3: Dropping retention
        STEP 4: Show retention policies for database
        STEP 5: Verify database does not have the retention policy
        '''
        test_name='test_user_drop_retention_policy_' + user + ' '
        data_node=choice(self.data_nodes_ips)
        database='test_user_drop_retention_policy_db'
        rp_name='user_drop_retention_policy'
        rp_duration='3h0m0s'
        rp_replication='2'
        self.header(test_name)
        self.mylog.info(test_name + 'STEP 1: Creating Admin InfluxDBClient data_node=%s, username=%s, password=%s' %
                        (data_node, LDAP_ADMIN_USERS, LDAP_ADMIN_PASS))
        client_admin=InfluxDBClient(data_node, username=LDAP_ADMIN_USERS, password=LDAP_ADMIN_PASS, timeout=3,
                                    retries=1)
        self.mylog.info(test_name + 'STEP 2: Creating retention policy %s with duration %s and replication %s'
                        % (rp_name, rp_duration, rp_replication))
        (success, errormessage)=du.create_retention_policy(self, client_admin, rp_name=rp_name, duration=rp_duration,
                                                           replication=rp_replication, database=database, default=True)
        assert success, self.mylog.info(test_name + 'unable to create retention policy ' + str(errormessage))
        self.mylog.info(test_name + 'STEP 3: Dropping retention policy %s' % rp_name)
        client=InfluxDBClient(data_node, username=user, password=LDAP_ADMIN_PASS, timeout=3, retries=1)
        (success, errormessage)=du.drop_retention_policies(self, client, database, rp_name)
        if role == 'b_first':
            assert success, self.mylog.info(test_name + 'unable to drop retention policy ' + str(errormessage))
            self.mylog.info(test_name + 'STEP 4: Show retention policies for database %s' % database)
            (success, retention_policies_d, error_message) = du.show_retention_policies(self, client_admin, database)
            assert success, self.mylog.info(test_name + 'unable to get retention policies for database %s' % database)
            self.mylog.info(test_name + 'STEP 5: Verify database does not have the retention policy %s' % rp_name)
            result=du.get_retention_policy(self, retention_policies_d, rp_name)
            assert result == None, self.mylog.info(test_name + ' retention policy %s still could be found' % rp_name)
        else:
            assert success == False, self.mylog.info(test_name + 'able to drop retention policy ' + str(errormessage))
        self.footer(test_name)

    # ==================================== ManageSubscription Permission Test Cases ===================================#
    @pytest.mark.parametrize('create_database', ['test_user_create_subscription_db'], ids=[''], indirect=True)
    @pytest.mark.usefixtures('create_database')
    @pytest.mark.parametrize('role, user', single_role_users, ids=single_role_users_ids)
    def test_user_create_subscription(self, role, user):
        '''

        '''
        test_name='test_user_create_subscription_' + user + ' '
        database='test_user_create_subscription_db'
        retention_policy='autogen'
        mode='ALL'
        destinations='\''+self.kapacitor+'\''
        data_node='http://'+choice(self.data_nodes_ips)+':8086'
        self.header(test_name)
        (success, message)=self.irl.create_subscription(data_node, test_name, database,
                                        retention_policy, mode, destinations, auth=(user, LDAP_ADMIN_PASS))
        if role == 'd_first':
            assert success, self.mylog.info(test_name + 'unable to create subscription, error=%s' % message)
        else:
            assert success == False, \
                self.mylog.info(test_name + 'able to create subscription, error=%s' % message)
        self.footer(test_name)

    @pytest.mark.parametrize('create_database', ['test_user_drop_subscription_db'], ids=[''], indirect=True)
    @pytest.mark.usefixtures('create_database')
    @pytest.mark.parametrize('role, user', single_role_users, ids=single_role_users_ids)
    def test_user_drop_subscription(self, role, user):
        '''

        '''
        test_name='test_user_drop_subscription_' + user + ' '
        database='test_user_drop_subscription_db'
        retention_policy='autogen'
        mode='ALL'
        destinations = '\'' + self.kapacitor + '\''
        data_node='http://'+choice(self.data_nodes_ips)+':8086'
        self.header(test_name)
        (success, message)=self.irl.create_subscription(data_node, test_name, database,
                                        retention_policy, mode, destinations, auth=(LDAP_ADMIN_USERS, LDAP_ADMIN_PASS))
        assert success, self.mylog.info(test_name + ' unable to create subscription, error=%s' % message)
        (success, message)=self.irl.drop_subscription(data_node, test_name, database, retention_policy,
                                                      auth=(user, LDAP_ADMIN_PASS))
        if role == 'd_first':
            assert success, self.mylog.info(test_name + ' unable to drop subscription, error=%s' % message)
        else:
            assert success == False, \
                self.mylog.info(test_name + ' able to drop subscription, error=%s' % message)
        self.footer(test_name)

    @pytest.mark.parametrize('create_database', ['test_user_show_subscriptions_db'], ids=[''], indirect=True)
    @pytest.mark.usefixtures('create_database')
    @pytest.mark.parametrize('role, user', single_role_users, ids=single_role_users_ids)
    def test_user_show_subscriptions(self, role, user):
        '''

        '''
        test_name='test_user_show_subscriptions_' + user + ' '
        database='test_user_show_subscriptions_db'
        retention_policy='autogen'
        mode='ALL'
        destinations=self.kapacitor
        data_node='http://'+choice(self.data_nodes_ips)+':8086'
        self.header(test_name)
        (success, message)=self.irl.create_subscription(data_node, test_name, database,
                                        retention_policy, mode, '\''+destinations+'\'', auth=(LDAP_ADMIN_USERS, LDAP_ADMIN_PASS))
        assert success, self.mylog.info(test_name + 'unable to create subscription, error=%s' % message)
        (success, subscriptions, message)=self.irl.show_subscriptions(data_node,
                                                                      auth=(user, LDAP_ADMIN_PASS))
        if role == 'd_first':
            assert success, self.mylog.info(test_name + 'unable to view subscriptions, error=%s' % message)
            actual_destination=subscriptions.get(database).get(test_name)['destination'][0]
            self.mylog.info(test_name + 'assert actual destination \'' + str(actual_destination) + '\' equals '
                        + str(destinations))
            assert actual_destination == destinations
            actual_rp=subscriptions.get(database).get(test_name)['rp']
            self.mylog.info(test_name + 'assert actual retention policy \'' + str(actual_rp) + '\' equals '
                        + str(retention_policy))
            assert actual_rp == retention_policy
            actual_mode=subscriptions.get(database).get(test_name)['mode']
            self.mylog.info(test_name + 'assert actual mode \'' + str(actual_mode) + '\' equals '
                        + str(mode))
            assert actual_mode == mode
        else:
            assert success == False, self.mylog.info(test_name + 'able to view subscriptions, error=%s' % message)
        self.footer(test_name)

    # ================================ CreateUserAndRole Permission Test Cases ========================================#
    @pytest.mark.parametrize('role, user', single_role_users, ids=single_role_users_ids)
    def test_user_create_user(self, role, user):
        '''
        '''
        test_name='test_user_create_user_' + user + ' '
        data_node=choice(self.data_nodes_ips)
        client=InfluxDBClient(data_node,username=user, password=LDAP_ADMIN_PASS, timeout=3, retries=1)
        user_to_create, password_to_create='test_user_create_user','test_user_create_password'
        # error message for users with CreateUserAndRole permissions
        error_message_authorized='creating users is disallowed when ldap is enabled'
        # error message for users without CreateUserAndRole permissions
        error_message_not_authorized='error authorizing query: %s not authorized to execute statement' \
                                     ' \'CREATE USER test_user_create_user WITH PASSWORD [REDACTED]\'' % user

        self.header(test_name)
        (success, message)=uu.create_user(self, client, user_to_create, password_to_create, admin=False)
        assert success is False, self.mylog.info(test_name + 'Assertion Error CREATE_USER returned True')
        if role == 'c_first':
            assert error_message_authorized in message, \
                self.mylog.info(test_name + ' Expected Error message :' + error_message_authorized +
                                ' is different from actual : ' + message)
        else:
            assert error_message_not_authorized in message, \
                self.mylog.info(test_name + ' Expected Error message :' + error_message_not_authorized +
                                ' is different from actual : ' + message)
        self.footer(test_name)

    @pytest.mark.parametrize('role, user', single_role_users, ids=single_role_users_ids)
    def test_user_delete_user(self, role, user):
        '''
        '''
        test_name='test_user_delete_user_' + user + ' '
        data_node=choice(self.data_nodes_ips)
        client=InfluxDBClient(data_node, username=user, password=LDAP_ADMIN_PASS, timeout=3, retries=1)
        error_message_authorized='dropping users is disallowed when ldap is enabled'
        error_message_not_authorized='error authorizing query: %s not authorized to execute statement' % user
        #                                     '\\\'DROP USER' % user

        self.header(test_name)
        (success, message)=uu.delete_user(self, client, LDAP_ADMIN_USERS)
        assert success is False, self.mylog.info(test_name + 'Assertion Error DELETE_USER returned True')
        if role == 'c_first':
            assert error_message_authorized in message, \
                self.mylog.info(test_name + ' Expected Error message :' + error_message_authorized +
                                ' is different from actual : ' + message)
        else:
            assert error_message_not_authorized in message, \
                self.mylog.info(test_name + ' Expected Error message :' + error_message_not_authorized +
                                ' is different from actual : ' + message)
        self.footer(test_name)

    @pytest.mark.parametrize('role, user', single_role_users, ids=single_role_users_ids)
    @pytest.mark.parametrize('permission', permissions)
    def test_user_grant_privilege(self, role, user, permission):
        '''
        '''
        test_name='test_user_grant_privilege_' + user + ' '
        data_node=choice(self.data_nodes_ips)
        database='_internal'
        client=InfluxDBClient(data_node, username=user, password=LDAP_ADMIN_PASS, timeout=1, retries=1)
        error_message_authorized='modifying user privileges is disallowed when ldap is enabled'
        error_message_not_authorized='error authorizing query: %s not authorized to execute statement' % user
        self.header(test_name)
        (success, message)=uu.grant_privilege(self, client, permission, database, LDAP_ADMIN_USERS)
        assert success is False, self.mylog.info(test_name + 'Assertion Error GRANT PRIVILEGE returned True')
        if role == 'c_first':
            assert error_message_authorized in message, \
                self.mylog.info(test_name + ' Expected Error message :' + error_message_authorized +
                            ' is different from actual : ' + message)
        else:
            assert error_message_not_authorized in message, \
                self.mylog.info(test_name + ' Expected Error message :' + error_message_not_authorized +
                                ' is different from actual : ' + message)
        self.footer(test_name)

    @pytest.mark.parametrize('role, user', single_role_users, ids=single_role_users_ids)
    def test_user_grant_admin_privileges(self, role, user):
        '''
        '''
        test_name='test_user_grant_admin_privileges_' + user + ' '
        data_node=choice(self.data_nodes_ips)
        client=InfluxDBClient(data_node, username=user, password=LDAP_ADMIN_PASS, timeout=1, retries=1)
        error_message_authorized='setting admin privileges is disallowed when ldap is enabled'
        error_message_not_authorized='error authorizing query: %s not authorized to execute statement' % user

        self.header(test_name)
        (success, message)=uu.grant_admin_privileges(self, client, LDAP_ADMIN_USERS)
        assert success is False, self.mylog.info(test_name + 'Assertion Error GRANT ADMIN PRIVILEGE returned True')
        if role == 'c_first':
            assert error_message_authorized in message, \
                self.mylog.info(test_name + ' Expected Error message :' + error_message_authorized +
                                ' is different from actual : ' + message)
        else:
            assert error_message_not_authorized in message, \
                self.mylog.info(test_name + ' Expected Error message :' + error_message_not_authorized +
                                ' is different from actual : ' + message)
        self.footer(test_name)

    # https://github.com/influxdata/plutonium/issues/2454
    @pytest.mark.parametrize('role, user', single_role_users, ids=single_role_users_ids)
    @pytest.mark.parametrize('permission', permissions)
    def test_user_revoke_privilege(self, role, user, permission):
        '''
        '''
        test_name='test_user_revoke_privilege_' + user + ' '
        data_node=choice(self.data_nodes_ips)
        database='_internal'
        client=InfluxDBClient(data_node, username=user, password=LDAP_ADMIN_PASS, timeout=1, retries=1)
        error_message_authorized='modifying user privileges is disallowed when ldap is enabled'
        error_message_not_authorized='error authorizing query: %s not authorized to execute statement' % user

        self.header(test_name)
        (success, message)=uu.revoke_privilege(self, client, permission, database, user)
        assert success is False, self.mylog.info(test_name + 'Assertion Error REVOKE PRIVILEGE returned True')
        if role == 'c_first':
            assert error_message_authorized in message, \
                self.mylog.info(test_name + ' Expected Error message :' + error_message_authorized +
                                ' is different from actual : ' + message)
        else:
            assert error_message_not_authorized in message, \
                self.mylog.info(test_name + ' Expected Error message :' + error_message_not_authorized +
                                ' is different from actual : ' + message)
        self.footer(test_name)

    # https://github.com/influxdata/plutonium/issues/2454
    @pytest.mark.parametrize('role, user', single_role_users, ids=single_role_users_ids)
    def test_user_revoke_admin_privileges(self, role, user):
        '''
        '''
        test_name='test_user_revoke_admin_privileges_' + user + ' '
        data_node=choice(self.data_nodes_ips)
        client=InfluxDBClient(data_node, username=user, password=LDAP_ADMIN_PASS, timeout=1, retries=1)
        error_message_authorized='revoking admin privileges is disallowed when ldap is enabled'
        error_message_not_authorized='error authorizing query: %s not authorized to execute statement' % user

        self.header(test_name)
        (success, message)=uu.revoke_admin_privileges(self, client, user)
        assert success is False, self.mylog.info(test_name + 'Assertion Error REVOKE ADMIN PRIVILEGE returned True')
        if role == 'c_first':
            assert error_message_authorized in message, \
                pytest.xfail(reason='Incorrect error message: setting instead of revoking')
                #self.mylog.info(test_name + ' Expected Error message :' + error_message_authorized +
                #                ' is different from actual : ' + message)
        else:
            assert error_message_not_authorized in message, \
                self.mylog.info(test_name + ' Expected Error message :' + error_message_not_authorized +
                                ' is different from actual : ' + message)
        self.footer(test_name)

    @pytest.mark.parametrize('role, user', single_role_users, ids=single_role_users_ids)
    def test_user_set_password(self, role, user):
        '''
        '''
        test_name='test_user_set_password_' + user + ' '
        password='newpassword'
        data_node=choice(self.data_nodes_ips)
        client=InfluxDBClient(data_node, username=user, password=LDAP_ADMIN_PASS, timeout=3, retries=1)
        error_message_authorized='updating users is disallowed when ldap is enabled'
        error_message_not_authorized = 'error authorizing query: %s not authorized to execute statement' % user

        self.header(test_name)
        (success, message)=uu.set_user_password(self, client, LDAP_ADMIN_USERS, password)
        assert success is False, self.mylog.info(test_name + 'Assertion Error SET PASSWORD FOR USER returned True')
        if role == 'c_first':
            assert error_message_authorized in message, \
                self.mylog.info(test_name + ' Expected Error message :' + error_message_authorized +
                                ' is different from actual : ' + message)
        else:
            assert error_message_not_authorized in message, \
                self.mylog.info(test_name + ' Expected Error message :' + error_message_not_authorized +
                                ' is different from actual : ' + message)
        self.footer(test_name)

    @pytest.mark.parametrize('role, user', single_role_users, ids=single_role_users_ids)
    def test_user_show_users(self, role, user):
        '''
        '''
        test_name = 'test_user_show_users_' + user + ' '
        expected_number_of_users=5000
        data_node = choice(self.data_nodes_ips)
        client = InfluxDBClient(data_node, username=user, password=LDAP_ADMIN_PASS, timeout=3, retries=1)

        self.header(test_name)
        (success, list_of_users)=uu.show_users(self, client)
        if role == 'c_first':
            assert success is True, self.mylog.info(test_name + 'Assertion Error not able getting users')
            assert expected_number_of_users == len(list_of_users), \
                pytest.xfail(reason='SHOW USERS is not supported with LDAP auth')
                #self.mylog.info(test_name + ' Expected number of users :' + str(expected_number_of_users) +
                #            ' is different from actual : ' + str(len(list_of_users)))
        else:
            assert success == False, \
                self.mylog.info(test_name + 'Assertion Error able getting users')
        self.footer(test_name)

    @pytest.mark.parametrize('role, user', single_role_users, ids=single_role_users_ids)
    def test_user_show_grants(self, role, user):
        '''
        '''
        test_name='test_user_show_grants_' + user + ' '
        data_node=choice(self.data_nodes_ips)
        client=InfluxDBClient(data_node, username=user, password=LDAP_ADMIN_PASS, timeout=1, retries=1)
        self.header(test_name)
        (success, user_grants)=uu.show_grants(self, client, LDAP_ADMIN_USERS)
        if role == 'c_first':
            assert success, self.mylog.info(test_name + 'Assertion Error SHOW GRANTS FOR %s' % user)
            assert len(user_grants) == 2, self.mylog.info(test_name + 'Assertion Error for %s user' % user)
        else:
            assert success == False, self.mylog.info(test_name + 'Assertion Error SHOW GRANTS FOR %s' % user)
        self.footer(test_name)

    # =================================== DropData Permission Test Cases ==============================================#
    @pytest.mark.parametrize('role, user', single_role_users, ids=single_role_users_ids)
    @pytest.mark.parametrize('create_database', ['test_user_drop_measurement_db'], ids=[''], indirect=True)
    @pytest.mark.usefixtures('create_database')
    def test_user_drop_measurement(self, role, user):
        '''

        '''
        test_name='test_user_drop_measurement_' + user + ' '
        database='test_user_drop_measurement_db'
        data_node=choice(self.data_nodes_ips)
        measurement='testm_user'
        self.header(test_name)
        self.mylog.info(test_name + 'STEP 1: Creating InfluxDBClient data_node=%s, username=%s, password=%s' %
                        (data_node, user, LDAP_ADMIN_PASS))
        client=InfluxDBClient(data_node, username=user, password=LDAP_ADMIN_PASS, database=database, timeout=3,
                                      retries=1)
        client_admin=InfluxDBClient(data_node, username=LDAP_ADMIN_USERS, password=LDAP_ADMIN_PASS, database=database,
                                    timeout=3, retries=1)
        self.mylog.info(test_name + 'STEP 1: Generate test data')
        points=gen_test_data(measurement)
        self.mylog.info(test_name + 'STEP 2: Write points to the database as admin user')
        result=du.write_points(self, client_admin, points=points, time_precision='s', database=database)
        assert result, self.mylog.info(test_name + 'Failed to write points into database')
        self.mylog.info(test_name + 'STEP 4: get created measurement')
        (success, result, error)=du.list_measurements(self, client_admin)
        assert success, self.mylog.info(test_name + 'Failed to get measurements ' + str(error))
        assert measurement in result, self.mylog.info(test_name + 'Created measurement was not found')
        self.mylog.info(test_name + 'STEP 5: drop_measurement %s' % measurement)
        (success, error_measurement)=du.drop_measurement(self, client, measurement)
        if role == 'f_first':
            assert success, self.mylog.info(test_name + 'Failed to drop measurement -' + str(error_measurement))
            self.mylog.info(test_name + 'STEP 6: get measurements')
            (success, result, error) = du.list_measurements(self, client_admin)
            assert success, self.mylog.info(test_name + 'Failed to get measurements ' + str(error))
            self.mylog.info(test_name + 'STEP 7: Assert measurement was deleted')
            assert measurement not in result, self.mylog.info(test_name + 'Measurement still can be found')
        else:
            assert success == False, self.mylog.info(test_name + 'able to drop measurement '
                                                     + str(error_measurement))
        self.footer(test_name)

    @pytest.mark.parametrize('role, user', single_role_users, ids=single_role_users_ids)
    @pytest.mark.parametrize('create_database', ['test_user_drop_series_db'], ids=[''], indirect=True)
    @pytest.mark.usefixtures('create_database')
    def test_user_drop_series(self, role, user):
        '''
        '''
        test_name='test_user_drop_series_' + user + ' '
        database='test_user_drop_series_db'
        data_node=choice(self.data_nodes_ips)
        measurement='test_user_series'
        series_to_delete = measurement+',id=28'
        self.header(test_name)
        self.mylog.info(test_name + 'STEP 1: Creating InfluxDBClient data_node=%s, username=%s, password=%s' %
                        (data_node, LDAP_ADMIN_USERS, LDAP_ADMIN_PASS))
        client_admin=InfluxDBClient(data_node, username=LDAP_ADMIN_USERS, password=LDAP_ADMIN_PASS,
                                database=database, timeout=3, retries=1)
        client=InfluxDBClient(data_node, username=user, password=LDAP_ADMIN_PASS,
                                      database=database, timeout=3, retries=1)
        self.mylog.info(test_name + 'STEP 2: Generate test data')
        points=gen_test_data(measurement)
        self.mylog.info(test_name + 'STEP 3: Write points to the database')
        result=du.write_points(self, client_admin, points=points, time_precision='s', database=database)
        assert result, self.mylog.info(test_name + 'Failed to write points into database')
        self.mylog.info(test_name + 'STEP 4: get series for the %s' % database)
        (success, series, error)=du.list_series(self, client_admin, database)
        assert success, self.mylog.info(test_name + 'Failed to get series ' + str(error))
        assert series_to_delete in series, self.mylog.info(test_name + 'Series was not found')
        self.mylog.info(test_name + 'STEP 5: delete series %s' % series_to_delete)
        # only one measurement is in the database, so deleting one series
        (success, error_series)=du.drop_series(self, client, database=database,
                                               measurement=measurement, tags={'id': '28'})
        if role == 'f_first':
            assert success, self.mylog.info(test_name + 'Failed to delete series' + str(error_series))
            self.mylog.info(test_name + 'STEP 6: get series')
            (success, series, error)=du.list_series(self, client_admin, database)
            assert success, self.mylog.info(test_name + 'Failed to get series ' + str(error))
            self.mylog.info(test_name + 'STEP 7: Assert series was deleted')
            assert series_to_delete not in series, self.mylog.info(test_name + 'Series still can be found')
        else:
            assert success == False, self.mylog.info(test_name + 'able to drop series '
                                                     + str(error))
        self.footer(test_name)

    @pytest.mark.parametrize('role, user', single_role_users, ids=single_role_users_ids)
    @pytest.mark.parametrize('create_database', ['test_user_delete_series_db'], ids=[''], indirect=True)
    @pytest.mark.usefixtures('create_database')
    def test_user_delete_series(self, role, user):
        '''

        '''
        test_name='test_user_delete_series_' + user + ' '
        database='test_user_delete_series_db'
        data_node=choice(self.data_nodes_ips)
        measurement='test_user_delete_series'
        series_to_delete=measurement + ',id=47'
        self.header(test_name)
        self.mylog.info(test_name + 'STEP 1: Creating InfluxDBClient data_node=%s, username=%s, password=%s' %
                        (data_node, LDAP_ADMIN_USERS, LDAP_ADMIN_PASS))
        client_admin=InfluxDBClient(data_node, username=LDAP_ADMIN_USERS, password=LDAP_ADMIN_PASS,
                                    database=database, timeout=3, retries=1)
        self.mylog.info(test_name + 'STEP 1: Creating InfluxDBClient data_node=%s, username=%s, password=%s' %
                        (data_node, user, LDAP_ADMIN_PASS))
        client=InfluxDBClient(data_node, username=user, password=LDAP_ADMIN_PASS,
                              database=database, timeout=3, retries=1)
        self.mylog.info(test_name + 'STEP 2: Generate test data')
        points=gen_test_data(measurement)
        self.mylog.info(test_name + 'STEP 3: Write points to the database')
        result=du.write_points(self, client_admin, points=points, time_precision='s', database=database)
        assert result, self.mylog.info(test_name + 'Failed to write points into database')
        self.mylog.info(test_name + 'STEP 4: get series for the %s' % database)
        (success, series, error)=du.list_series(self, client_admin, database)
        assert success, self.mylog.info(test_name + 'Failed to get series ' + str(error))
        assert series_to_delete in series, self.mylog.info(test_name + 'Series was not found')
        self.mylog.info(test_name + 'STEP 5: delete series %s' % series_to_delete)
        # only one measurement is in the database, so deleting one series
        (success, result, error) = du.delete_series(self, client, database=database,
                                                    measurement=measurement, tags={'id': '47'})
        if role == 'f_first':
            assert success, self.mylog.info(test_name + 'Failed to delete series')
            assert len(result.items()) == 0, self.mylog.info(test_name + 'Failed to delete series ' + str(error))
            self.mylog.info(test_name + 'STEP 6: get series')
            (success, series, error)=du.list_series(self, client_admin, database)
            assert success, self.mylog.info(test_name + 'Failed to get series ' + str(error))
            self.mylog.info(test_name + 'STEP 7: Assert series was deleted')
            assert series_to_delete not in series, self.mylog.info(test_name + 'Series still can be found')
        else:
            assert success == False, self.mylog.info(test_name + ' able to delete series '
                                                     + str(error))
        self.footer(test_name)