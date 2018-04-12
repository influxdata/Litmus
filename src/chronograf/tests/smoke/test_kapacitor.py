import pytest
import src.util.login_util as lu
import src.util.sources_util as su
import src.util.kapacitor_util as ku
from src.chronograf.lib import rest_lib


# before running test suite make sure there are no sources.
@pytest.mark.usefixtures( 'kapacitor', 'chronograf', 'data_nodes',
                          'meta_nodes', 'get_source_path',
                          'delete_created_sources', 'http_auth',
                          'admin_user', 'admin_pass')
class TestKapacitor():
    '''
    kapacitor fixture - to get kapacitor URL
    chronograf fixture - to get chronograf URL
    data_node and meta_nodes fixtures - to get lists of meta and data nodes
    delete_created_sources - to delete sources created by tests
    http_auth fixture - whether basic authentication is enabled
    admin_user and admin_pass fixtures - to get the username and password
    of the admin user.
    '''

    mylog=lu.log(lu.get_log_path(), 'w', __name__)
    rl=rest_lib.RestLib(mylog)

    ####################################################################################################################
    def verify_source(self, expected, source_id, source):
        '''
        :param expected_data: dictionary of expected values
        :param source_id: ID of the created source
        :param source: dictionaly of actual values
        :return: does not return anything
        '''
        username = su.get_source_username(self, source_id, source)
        self.mylog.info('ASSERT ACTUAL username=' + str(username) + ' EQUALS '\
                        'EXPECTED username=' + str(expected['USERNAME']))
        su.verify_data(self, expected['USERNAME'], username)
        insecure = su.get_source_insecureskipverify(self, source_id, source)
        self.mylog.info('ASSERT ACTUAL insecure=' + str(insecure) + ' EQUALS '\
                        'EXPECTED insecure=' + str(expected['INSECURE_SKIP_VERIFY']))
        su.verify_data(self, expected['INSECURE_SKIP_VERIFY'], insecure)
        url = su.get_source_url(self, source_id, source)
        self.mylog.info('ASSERT ACTUAL url=' + str(url) + ' EQUALS EXPECTED '\
                        'url=' + str(expected['DATA_URL']))
        su.verify_data(self, expected['DATA_URL'], url)
        name = su.get_source_name(self, source_id, source)
        self.mylog.info('ASSERT ACTUAL name=' + str(name) + ' EQUALS EXPECTED '\
                        'name' + str(expected['NAME']))
        su.verify_data(self, expected['NAME'], name)
        roles = su.get_source_roles_link(self, source_id, source)
        self.mylog.info('ASSERT ACTUAL roles=' + str(roles) + ' EQUALS '\
                        'EXPECTED roles=' + str(expected['ROLES']))
        su.verify_data(self, expected['ROLES'], roles)
        default = su.get_source_default(self, source_id, source)
        self.mylog.info('ASSERT ACTUAL default=' + str(default) + ' EQUALS '\
                        'EXPECTED default=' + str(expected['DEFAULT']))
        su.verify_data(self, expected['DEFAULT'], default)
        telegrafdb = su.get_source_telegraf(self, source_id, source)
        self.mylog.info('ASSERT ACTUAL telegrafdb=' + str(telegrafdb) + ' EQUALS '\
                        'EXPECTED telegrafdb=' + str(expected['TELEGRAF_DB']))
        su.verify_data(self, expected['TELEGRAF_DB'], telegrafdb)
        shared_secret = su.get_source_sharedsecret(self, source_id, source)
        self.mylog.info('ASSERT ACTUAL shared_secret=' + str(shared_secret) + ' EQUALS '\
                        'EXPECTED shared_secret=' + str(expected['SHARED_SECRET']))
        su.verify_data(self, expected['SHARED_SECRET'], shared_secret)
        meta_url = su.get_source_metaurl(self, source_id, source)
        self.mylog.info('ASSERT ACTUAL meta_url=' + str(meta_url) + ' EQUALS '\
                        'EXPECTED meta_url=' + str(expected['META_URL']))
        su.verify_data(self, expected['META_URL'], meta_url)
        kapacitor = su.get_source_kapacitors_link(self, source_id, source)
        self.mylog.info('ASSERT ACTUAL kapacitor=' + str(kapacitor) + ' EQUALS '\
                        'EXPECTED kapacitor=' + str(expected['KAPACITOR']))
        su.verify_data(self, expected['KAPACITOR'], kapacitor)
        write = su.get_source_write_link(self, source_id, source)
        self.mylog.info('ASSERT ACTUAL write=' + str(write) + ' EQUALS '\
                        'EXPECTED write=' + str(expected['WRITE']))
        su.verify_data(self, expected['WRITE'], write)
        proxy = su.get_source_proxy_link(self, source_id, source)
        self.mylog.info('ASSERT ACTUAL proxy=' + str(proxy) + ' EQUALS '\
                        'EXPECTED proxy=' + str(expected['PROXY']))
        su.verify_data(self, expected['PROXY'], proxy)
        permissions = su.get_source_permissions_link(self, source_id, source)
        self.mylog.info('ASSERT ACTUAL permissions=' + str(permissions) + ' EQUALS '\
                        'EXPECTED permissions=' + str(expected['PERMISSIONS']))
        su.verify_data(self, expected['PERMISSIONS'], permissions)
        query = su.get_source_queries_link(self, source_id, source)
        self.mylog.info('ASSERT ACTUAL query=' + str(query) + ' EQUALS '\
                        'EXPECTED query=' + str(expected['QUERY']))
        su.verify_data(self, expected['QUERY'], query)
        password = su.get_source_password(self, source_id, source)
        self.mylog.info('ASSERT ACTUAL password=' + str(password) + ' EQUALS '\
                        'EXPECTED password=' +expected['PASSWORD'])
        su.verify_data(self, expected['PASSWORD'], password)
        type = su.get_source_type(self, source_id, source)
        self.mylog.info('ASSERT ACTUAL type=' + str(type) + ' EQUALS '\
                        'EXPECTED type=' + str(expected['TYPE']))
        su.verify_data(self, expected['TYPE'], type)
        users = su.get_source_users_link(self, source_id, source)
        self.mylog.info('ASSERT ACTUAL users=' + str(users) + ' EQUALS EXPECTED '\
                        'users=' + str(expected['USERS']))
        su.verify_data(self, expected['USERS'], users)

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


    def test_create_kapacitor(self):
        '''
        1. Create source and verify source_id is not None
        2. Get Kapacitor URL - /chronograf/v1/sources/<source_id>/kapacitors
        3. Create Kapacitor and verify kapacitor_id is not None
        4. Get kapacitor data for the above created kapacitor instance
        5. Assert Kapacitor is ping-able
        '''
        self.header('test_ create_kapacitor')
        source_url=self.get_source_path
        DATA_URL=self.data_nodes[0]
        META_URL=self.meta_nodes[0]
        SOURCE_NAME='CREATE KAPACITOR'
        KAPACITOR_NAME='KAPACITOR 1'
        if self.http_auth:
            JSON_SOURCE={'url':DATA_URL, 'metaUrl':META_URL, 'name':SOURCE_NAME,
                         'telegraf': 'telegraf', 'default': True, 'username':self.admin_user,
                         'password':self.admin_pass}
        else:
            JSON_SOURCE={'url':DATA_URL, 'metaUrl':META_URL, 'name':SOURCE_NAME,
                         'telegraf': 'telegraf', 'default': True}
        JSON_KAPACITOR={'url':self.kapacitor, 'name':KAPACITOR_NAME}

        self.mylog.info('test_create_kapacitor - STEP 1: CREATE SOURCE (RestLib.create_source())')
        (status, message, source_id)=self.rl.create_source(self.chronograf, source_url, JSON_SOURCE)
        assert source_id is not None, self.mylog.info('test_create_kapacitor : ASSERTION FAILED, source_id is None')
        self.mylog.info('test_create_kapacitor - STEP 2: GET KAPACITOR URL')
        source=self.rl.get_source(self.chronograf, source_url, source_id)
        kapacitor_url=su.get_source_kapacitors_link(self, source_id, source)
        self.mylog.info('test_create_kapacitor - STEP 3: CREATE KAPACITOR (RestLib.create_kapacitor)')
        (status, message, kapacitor_id)=self.rl.create_kapacitor(self.chronograf, kapacitor_url, JSON_KAPACITOR)
        assert kapacitor_id is not None, self.mylog.info('test_create_kapacitor : ASSERTION FAILED, kapacitor_id is None')
        self.mylog.info('test_create_kapacitor - STEP 4: GET KAPACITOR DATA(RestLib.get_kapacitor)')
        kapacitor_dictionary=self.rl.get_kapacitor(self.chronograf, kapacitor_url, kapacitor_id)
        self.mylog.info('test_create_kapacitor - STEP 4: GET KAPACITOR PING LINK(util.kpacitor_util.get_kapacitor_ping)')
        ping_link=ku.get_kapacitor_ping(self, kapacitor_id, kapacitor_dictionary)
        self.mylog.info('test_create_kapacitor ping url =' + str(ping_link))
        self.mylog.info('test_create_kapacitor - STEP 5: PING KAPACITOR URL USING=' + str(ping_link))
        response=self.rl.get(self.chronograf, ping_link)
        assert response.status_code == 204, self.mylog.info('test_create_kapacitor ASSERTION ERROR status_code=' +
                                                            str(response.status_code))
        self.footer('test_ create_kapacitor')

    def test_update_kapacitor_name(self):
        '''
        1. Create source and verify source_id is not None
        2. Get Kapacitor URL - /chronograf/v1/sources/<source_id>/kapacitors
        3. Create Kapacitor and verify kapacitor_id is not None
        4. Get kapacitor data for the above created kapacitor instance
        5. Assert Kapacitor is ping-able
        6. Update Kapacitor's name
        7. Get updated Kapacitor's name and assert it has been changed
        '''
        self.header('test_update_kapacitor_name')
        source_url=self.get_source_path
        DATA_URL=self.data_nodes[0]
        META_URL=self.meta_nodes[0]
        SOURCE_NAME='CREATE KAPACITOR 2'
        KAPACITOR_NAME='KAPACITOR 2'
        KAPACITOR_UPDATED_NAME='KAPACITOR NEW NAME'
        if self.http_auth:
            JSON_SOURCE={'url':DATA_URL, 'metaUrl':META_URL, 'name':SOURCE_NAME,
                         'telegraf':'telegraf', 'default':True, 'username':self.admin_user,
                         'password':self.admin_pass}
        else:
            JSON_SOURCE={'url':DATA_URL, 'metaUrl':META_URL, 'name':SOURCE_NAME, 'telegraf':'telegraf', 'default':True}
        JSON_KAPACITOR={'url': self.kapacitor, 'name':KAPACITOR_NAME}
        JSON_UPDATE_KAPACITOR={'url':self.kapacitor, 'name':KAPACITOR_UPDATED_NAME}

        self.mylog.info('test_update_kapacitor_name - STEP 1: CREATE SOURCE (RestLib.create_source())')
        (status, message, source_id)=self.rl.create_source(self.chronograf, source_url, JSON_SOURCE)
        assert source_id is not None, self.mylog.info('test_create_kapacitor_name : ASSERTION FAILED, source_id is None')
        self.mylog.info('test_update_kapacitor_name - STEP 2: GET KAPACITOR URL')
        source=self.rl.get_source(self.chronograf, source_url, source_id)
        kapacitor_url=su.get_source_kapacitors_link(self, source_id, source)
        self.mylog.info('test_update_kapacitor_name - STEP 3: CREATE KAPACITOR (RestLib.create_kapacitor)')
        (status, message, kapacitor_id)=self.rl.create_kapacitor(self.chronograf, kapacitor_url, JSON_KAPACITOR)
        assert kapacitor_id is not None, self.mylog.info(
            'test_update_kapacitor : ASSERTION FAILED, kapacitor_id is None')
        self.mylog.info('test_update_kapacitor_name - STEP 4: GET KAPACITOR DATA(RestLib.get_kapacitor)')
        kapacitor_dictionary=self.rl.get_kapacitor(self.chronograf, kapacitor_url, kapacitor_id)
        self.mylog.info(
            'test_update_kapacitor_name - STEP 4: GET KAPACITOR PING LINK(util.kpacitor_util.get_kapacitor_ping)')
        ping_link = ku.get_kapacitor_ping(self, kapacitor_id, kapacitor_dictionary)
        self.mylog.info('test_update_kapacitor_name ping url =' + str(ping_link))
        self.mylog.info('test_update_kapacitor_name - STEP 5: PING KAPACITOR URL USING=' + str(ping_link))
        response=self.rl.get(self.chronograf, ping_link)
        assert response.status_code == 204, self.mylog.info('test_update_kapacitor_name ASSERTION ERROR status_code=' +
                                                            str(response.status_code))
        self.mylog.info('test_update_kapacitor_name - STEP 6: UPDATE KAPACITOR NAME RestLib.patch_kapacitor)')
        self.rl.patch_kapacitor(self.chronograf, kapacitor_url, kapacitor_id, JSON_UPDATE_KAPACITOR)
        kapacitor_dictionary=self.rl.get_kapacitor(self.chronograf, kapacitor_url, kapacitor_id)
        self.mylog.info('test_update_kapacitor_name - STEP 7: GET UPDATED KAPACITOR NAME')
        new_name=ku.get_kapacitor_name(self, kapacitor_id, kapacitor_dictionary)
        assert new_name == KAPACITOR_UPDATED_NAME, self.mylog.info('test_update_kapacitor_name updated name='
                                                                   + str(new_name) + ', but expected ' + KAPACITOR_UPDATED_NAME)
        self.footer('test_update_kapacitor_name')

    def test_delete_kapacitor(self):
        '''
        1. Create source and verify source_id is not None
        2. Get Kapacitor URL - /chronograf/v1/sources/<source_id>/kapacitors
        3. Create Kapacitor and verify kapacitor_id is not None
        4. Get kapacitor data for the above created kapacitor instance
        5. Assert Kapacitor is ping-able
        6. Delete created kapacitor
        '''
        self.header('test_delete_kapacitor')
        source_url = self.get_source_path
        DATA_URL = self.data_nodes[0]
        META_URL = self.meta_nodes[0]
        SOURCE_NAME = 'CREATE KAPACITOR 3'
        KAPACITOR_NAME = 'KAPACITOR 3'
        if self.http_auth:
            JSON_SOURCE = {'url': DATA_URL, 'metaUrl': META_URL, 'name': SOURCE_NAME, 'telegraf': 'telegraf',
                       'default': True, 'username':self.admin_user, 'password':self.admin_pass}
        else:
            JSON_SOURCE = {'url': DATA_URL, 'metaUrl': META_URL, 'name': SOURCE_NAME, 'telegraf': 'telegraf',
                       'default': True}
        JSON_KAPACITOR = {'url': self.kapacitor, 'name': KAPACITOR_NAME}

        self.mylog.info('test_delete_kapacitor - STEP 1: CREATE SOURCE (RestLib.create_source())')
        (status, source_body, source_id) = self.rl.create_source(self.chronograf, source_url, JSON_SOURCE)
        assert source_id is not None, self.mylog.info('test_delete_kapacitor : ASSERTION FAILED, source_id is None')
        self.mylog.info('test_delete_kapacitor - STEP 2: GET KAPACITOR URL')
        source = self.rl.get_source(self.chronograf, source_url, source_id)
        kapacitor_url = su.get_source_kapacitors_link(self, source_id, source)
        self.mylog.info('test_delete_kapacitor - STEP 3: CREATE KAPACITOR (RestLib.create_kapacitor)')
        (status, kap_body, kapacitor_id) = self.rl.create_kapacitor(self.chronograf, kapacitor_url, JSON_KAPACITOR)
        assert kapacitor_id is not None, self.mylog.info(
            'test_delete_kapacitor : ASSERTION FAILED, kapacitor_id is None')
        self.mylog.info('test_delete_kapacitor - STEP 4: GET KAPACITOR DATA(RestLib.get_kapacitor)')
        kapacitor_dictionary = self.rl.get_kapacitor(self.chronograf, kapacitor_url, kapacitor_id)
        self.mylog.info(
            'test_delete_kapacitor - STEP 4: GET KAPACITOR PING LINK(util.kpacitor_util.get_kapacitor_ping)')
        ping_link = ku.get_kapacitor_ping(self, kapacitor_id, kapacitor_dictionary)
        self.mylog.info('test_delete_kapacitor ping url =' + str(ping_link))
        self.mylog.info('test_delete_kapacitor - STEP 5: PING KAPACITOR URL USING=' + str(ping_link))
        response = self.rl.get(self.chronograf, ping_link)
        assert response.status_code == 204, self.mylog.info('test_delete_kapacitor ASSERTION ERROR status_code=' +
                                                            str(response.status_code))
        self.mylog.info('test_delete_kapacitor - STEP 7: DELETE KAPACITOR ID=' + str(kapacitor_id))
        self.rl.delete_kapacitor(self.chronograf, kapacitor_url, kapacitor_id)
        self.footer('test_delete_kapacitor')
