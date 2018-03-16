
import pytest
import src.util.login_util as lu
import src.util.sources_util as su
import src.util.kapacitor_util as ku
from src.chronograf.lib import rest_lib

# before running test suite make sure there are no sources.
@pytest.mark.usefixtures('delete_sources', 'base_url', 'data_nodes', 'meta_nodes', 'get_source_path')
class TestSources():
    '''
    TODO
    '''

    mylog=lu.log(lu.get_log_path(), 'w', __name__)
    rl=rest_lib.RestLib(mylog)

    CUSTOM_NAME='Test Create Source User Options'
    UPDATE_NAME='Test Update Source Name'
    UPDATED_NAME='Updated Name Of The Source'

    # Test Data for creating a source(s)
    JSON_BAD_URL={'url':'http://34.211.191.80:8086'}
    JSON_ALL_DATA={}
    JSON_BAD_METAURL={}
    JSON_AUTH_DATA={} # need to use with a auth supported configuration

    ####################################################################################################################
    def verify_source(self, expected, source_id, source):
        '''
        :param expected_data: dictionary of expected values
        :param source_id: ID of the created source
        :param source: dictionaly of actual values
        :return: does not return anything
        '''
        username = su.get_source_username(self, source_id, source)
        self.mylog.info('test_create_source_url_only : ASSERT ACTUAL username=' + str(username) + ' EQUALS '\
                        'EXPECTED username=' + str(expected['USERNAME']))
        su.verify_data(self, expected['USERNAME'], username)
        insecure = su.get_source_insecureskipverify(self, source_id, source)
        self.mylog.info('test_create_source_url_only : ASSERT ACTUAL insecure=' + str(insecure) + ' EQUALS '\
                        'EXPECTED insecure=' + str(expected['INSECURE_SKIP_VERIFY']))
        su.verify_data(self, expected['INSECURE_SKIP_VERIFY'], insecure)
        url = su.get_source_url(self, source_id, source)
        self.mylog.info('test_create_source_url_only : ASSERT ACTUAL url=' + str(url) + ' EQUALS EXPECTED '\
                        'url=' + str(expected['DATA_URL']))
        su.verify_data(self, expected['DATA_URL'], url)
        name = su.get_source_name(self, source_id, source)
        self.mylog.info('test_create_source_url_only : ASSERT ACTUAL name=' + str(name) + ' EQUALS EXPECTED '\
                        'name' + str(expected['NAME']))
        su.verify_data(self, expected['NAME'], name)
        roles = su.get_source_roles_link(self, source_id, source)
        self.mylog.info('test_create_source_url_only : ASSERT ACTUAL roles=' + str(roles) + ' EQUALS '\
                        'EXPECTED roles=' + str(expected['ROLES']))
        su.verify_data(self, expected['ROLES'], roles)
        default = su.get_source_default(self, source_id, source)
        self.mylog.info('test_create_source_url_only : ASSERT ACTUAL default=' + str(default) + ' EQUALS '\
                        'EXPECTED default=' + str(expected['DEFAULT']))
        su.verify_data(self, expected['DEFAULT'], default)
        telegrafdb = su.get_source_telegraf(self, source_id, source)
        self.mylog.info('test_create_source_url_only : ASSERT ACTUAL telegrafdb=' + str(telegrafdb) + ' EQUALS '\
                        'EXPECTED telegrafdb=' + str(expected['TELEGRAF_DB']))
        su.verify_data(self, expected['TELEGRAF_DB'], telegrafdb)
        shared_secret = su.get_source_sharedsecret(self, source_id, source)
        self.mylog.info('test_create_source_url_only : ASSERT ACTUAL shared_secret=' + str(shared_secret) + ' EQUALS '\
                        'EXPECTED shared_secret=' + str(expected['SHARED_SECRET']))
        su.verify_data(self, expected['SHARED_SECRET'], shared_secret)
        meta_url = su.get_source_metaurl(self, source_id, source)
        self.mylog.info('test_create_source_url_only : ASSERT ACTUAL meta_url=' + str(meta_url) + ' EQUALS '\
                        'EXPECTED meta_url=' + str(expected['META_URL']))
        su.verify_data(self, expected['META_URL'], meta_url)
        kapacitor = su.get_source_kapacitors_link(self, source_id, source)
        self.mylog.info('test_create_source_url_only : ASSERT ACTUAL kapacitor=' + str(kapacitor) + ' EQUALS '\
                        'EXPECTED kapacitor=' + str(expected['KAPACITOR']))
        su.verify_data(self, expected['KAPACITOR'], kapacitor)
        write = su.get_source_write_link(self, source_id, source)
        self.mylog.info('test_create_source_url_only : ASSERT ACTUAL write=' + str(write) + ' EQUALS '\
                        'EXPECTED write=' + str(expected['WRITE']))
        su.verify_data(self, expected['WRITE'], write)
        proxy = su.get_source_proxy_link(self, source_id, source)
        self.mylog.info('test_create_source_url_only : ASSERT ACTUAL proxy=' + str(proxy) + ' EQUALS '\
                        'EXPECTED proxy=' + str(expected['PROXY']))
        su.verify_data(self, expected['PROXY'], proxy)
        permissions = su.get_source_permissions_link(self, source_id, source)
        self.mylog.info('test_create_source_url_only : ASSERT ACTUAL permissions=' + str(permissions) + ' EQUALS '\
                        'EXPECTED permissions=' + str(expected['PERMISSIONS']))
        su.verify_data(self, expected['PERMISSIONS'], permissions)
        query = su.get_source_queries_link(self, source_id, source)
        self.mylog.info('test_create_source_url_only : ASSERT ACTUAL query=' + str(query) + ' EQUALS '\
                        'EXPECTED query=' + str(expected['QUERY']))
        su.verify_data(self, expected['QUERY'], query)
        password = su.get_source_password(self, source_id, source)
        self.mylog.info('test_create_source_url_only : ASSERT ACTUAL password=' + str(password) + ' EQUALS '\
                        'EXPECTED password=' +expected['PASSWORD'])
        su.verify_data(self, expected['PASSWORD'], password)
        type = su.get_source_type(self, source_id, source)
        self.mylog.info('test_create_source_url_only : ASSERT ACTUAL type=' + str(type) + ' EQUALS '\
                        'EXPECTED type=' + str(expected['TYPE']))
        su.verify_data(self, expected['TYPE'], type)
        users = su.get_source_users_link(self, source_id, source)
        self.mylog.info('test_create_source_url_only : ASSERT ACTUAL users=' + str(users) + ' EQUALS EXPECTED '\
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

    def test_create_source_url_only(self):
        '''
        1. Creates source by using only one required param in request body - url of the data node.
        2. Asserts that ID of the source is not None
        3. Get data for the created source
        4. Verify expected response data equals actula response data from get source request.
        '''
        # choose a data node from a list of existing data nodes. For now use the first one
        source_url=self.get_source_path
        DATA_URL=self.data_nodes.split()[0]
        JSON_URL_ONLY = {'url': DATA_URL}
        self.header('test_create_source_url_only')
        self.mylog.info('test_create_source_url_only - STEP 1: CALL RestLib.create_source()')
        (status,message,source_id)=self.rl.create_source(self.base_url, source_url, JSON_URL_ONLY)
        assert source_id is not None, self.mylog.info('test_create_source_url_only : ASSERTION FAILED, source_id is None')
        self.mylog.info('test_create_source_url_only - STEP 1: DONE SOURCE_ID=' + str(source_id))
        # Expected dictionary
        expected = {'USERNAME': '', 'INSECURE_SKIP_VERIFY': False, 'DATA_URL': DATA_URL, 'NAME': '',
                    'ROLES': '/chronograf/v1/sources/%s/roles' % source_id, 'DEFAULT': 1, 'TELEGRAF_DB': 'telegraf',
                    'SHARED_SECRET': '', 'META_URL': '',
                    'KAPACITOR': '/chronograf/v1/sources/%s/kapacitors' % source_id,
                    'WRITE': '/chronograf/v1/sources/%s/write' % source_id,
                    'PROXY': '/chronograf/v1/sources/%s/proxy' % source_id,
                    'PERMISSIONS': '/chronograf/v1/sources/%s/permissions' % source_id,
                    'QUERY': '/chronograf/v1/sources/%s/queries' % source_id, 'PASSWORD': '',
                    'TYPE': 'influx-enterprise', 'USERS': '/chronograf/v1/sources/%s/users' % source_id}

        self.mylog.info('test_create_source_url_only - STEP 2: CALL RestLib.get_source()')
        source=self.rl.get_source(self.base_url, source_url, source_id)
        self.mylog.info('test_create_source_url_only - STEP 2: DONE')
        self.verify_source(expected, source_id, source)
        self.footer('test_create_source_url_only')

    @pytest.mark.skip
    def test_create_source_incorrect_url(self):
        '''
        1. Tries to create a source using incorrect url for data node
        2. Asserts request status is 400 and error message is 'Error contacting source'
        NOTE: UI does not return any errors at all. Would be nice to let users know why they cannot create a source
        '''
        error_message='Error contacting source'

        self.header('test_create_source_incorrect_url')
        self.mylog.info('test_create_source_incorrect_url - STEP 1: CALL RestLib.create_source()')
        (status, message, source_id) = self.rl.create_source(self.base_url, self.JSON_BAD_URL)
        self.mylog.info('test_create_source_incorrecturl - STEP 1: DONE')
        self.mylog.info('test_create_source_incorrect_url : ASSERT 400 equals ' + str(status))
        assert 400 == status, self.mylog.info('test_create_source_incorrect_url - ASSERTION ERROR, '
                                              'status=' + str(status))
        self.mylog.info('test_create_source_incorrect_url : ASSERT ' + str(error_message)\
                        + ' equals to ' + str(message))
        assert error_message == message, self.mylog.info('message=' + str(message))

    def test_create_source_user_options(self):
        '''
        1. Create source using data that user would be able to enter via UI, i.e:
           URL of data node, Name of the source, metaURL and telegraf database (All values are correct)
           Username and Password won't be used (requires different cluster configuration)
        2. Assert that ID of the source is not None
        3. Verify expected response data equals actual data from get source request
        '''
        # Choose meta and data node from the list of existing nodes. For now use the first one in the list
        source_url = self.get_source_path
        DATA_URL=self.data_nodes.split()[0]
        META_URL=self.meta_nodes.split()[0]
        JSON_USER_OPTIONS={'url':DATA_URL, 'metaUrl':META_URL, 'name':self.CUSTOM_NAME, 'telegraf':'telegraf',
                           'default':True}

        self.header('test_create_source_user_options')
        self.mylog.info('test_create_user_options - STEP 1: CALL RestLib.create_source()')
        (status, message, source_id) = self.rl.create_source(self.base_url, source_url, JSON_USER_OPTIONS)
        assert source_id is not None, self.mylog.info(
            'test_create_source_user_options : ASSERTION FAILED, source_id is None')
        self.mylog.info('test_create_user_options - STEP 1: DONE SOURCE_ID=' + str(source_id))
        # Expected dictionary
        expected = {'USERNAME': '', 'INSECURE_SKIP_VERIFY': False, 'DATA_URL': DATA_URL, 'NAME':self.CUSTOM_NAME,
                    'ROLES': '/chronograf/v1/sources/%s/roles' % source_id, 'DEFAULT': True, 'TELEGRAF_DB': 'telegraf',
                    'SHARED_SECRET': '', 'META_URL': META_URL,
                    'KAPACITOR': '/chronograf/v1/sources/%s/kapacitors' % source_id,
                    'WRITE': '/chronograf/v1/sources/%s/write' % source_id,
                    'PROXY': '/chronograf/v1/sources/%s/proxy' % source_id,
                    'PERMISSIONS': '/chronograf/v1/sources/%s/permissions' % source_id,
                    'QUERY': '/chronograf/v1/sources/%s/queries' % source_id, 'PASSWORD': '',
                    'TYPE': 'influx-enterprise', 'USERS': '/chronograf/v1/sources/%s/users' % source_id}

        self.mylog.info('test_create_source_user_options - STEP 2: CALL RestLib.get_source()')
        source = self.rl.get_source(self.base_url, source_url, source_id)
        self.mylog.info('test_create_source_user_options - STEP 2: DONE')
        self.verify_source(expected, source_id, source)
        self.footer('test_create_source_user_options')

    def test_update_source_name_field(self):
        '''
        Create source using data that user would be able to enter via UI, i.e:
           URL of data node, Name of the source, metaURL and telegraf database (All values are correct)
           Username and Password won't be used (requires different cluster configuration)
        2. Assert that ID of the source is not None
        3. Verify expected response data equals actual data from get source request

        '''
        source_url = self.get_source_path
        DATA_URL=self.data_nodes.split()[0]
        META_URL=self.meta_nodes.split()[0]
        JSON_UPDATE_NAME = {'url': DATA_URL, 'metaUrl': META_URL, 'name': self.UPDATE_NAME, 'telegraf': 'telegraf',
                            'default': True}
        JSON_UPDATED_NAME = {'url': DATA_URL, 'metaUrl': META_URL, 'name': self.UPDATED_NAME, 'telegraf': 'telegraf',
                             'default': True}

        self.header('test_update_source_name_field')
        self.mylog.info('test_update_source_name_field - STEP 1: CALL RestLib.create_source()')
        (status, message, source_id) = self.rl.create_source(self.base_url, source_url, JSON_UPDATE_NAME)
        assert source_id is not None, self.mylog.info(
            'test_update_source_name_field : ASSERTION FAILED, source_id is None')
        self.mylog.info('test_update_source_name_field - STEP 1: DONE SOURCE_ID=' + str(source_id))
        # Expected dictionary
        expected={'USERNAME':'', 'INSECURE_SKIP_VERIFY':False, 'DATA_URL':DATA_URL, 'NAME':self.UPDATE_NAME,
                    'ROLES':'/chronograf/v1/sources/%s/roles' % source_id, 'DEFAULT':1, 'TELEGRAF_DB':'telegraf',
                    'SHARED_SECRET':'', 'META_URL':META_URL,
                    'KAPACITOR':'/chronograf/v1/sources/%s/kapacitors' % source_id,
                    'WRITE':'/chronograf/v1/sources/%s/write' % source_id,
                    'PROXY':'/chronograf/v1/sources/%s/proxy' % source_id,
                    'PERMISSIONS':'/chronograf/v1/sources/%s/permissions' % source_id,
                    'QUERY':'/chronograf/v1/sources/%s/queries' % source_id, 'PASSWORD':'',
                    'TYPE':'influx-enterprise','USERS':'/chronograf/v1/sources/%s/users' % source_id}
        expected_updated={'USERNAME':'', 'INSECURE_SKIP_VERIFY':False, 'DATA_URL':DATA_URL, 'NAME':self.UPDATED_NAME,
                    'ROLES':'/chronograf/v1/sources/%s/roles' % source_id, 'DEFAULT': 1, 'TELEGRAF_DB': 'telegraf',
                    'SHARED_SECRET': '', 'META_URL': META_URL,
                    'KAPACITOR':'/chronograf/v1/sources/%s/kapacitors' % source_id,
                    'WRITE':'/chronograf/v1/sources/%s/write' % source_id,
                    'PROXY':'/chronograf/v1/sources/%s/proxy' % source_id,
                    'PERMISSIONS':'/chronograf/v1/sources/%s/permissions' % source_id,
                    'QUERY':'/chronograf/v1/sources/%s/queries' % source_id, 'PASSWORD':'',
                    'TYPE':'influx-enterprise', 'USERS':'/chronograf/v1/sources/%s/users' % source_id}
        self.mylog.info('test_update_source_name_field - STEP 2: CALL RestLib.get_source()')
        source=self.rl.get_source(self.base_url, source_url, source_id)
        self.mylog.info('test_update_source_name_field - STEP 2: DONE')
        self.verify_source(expected, source_id, source)
        self.mylog.info('test_update_source_name_field - STEP 3: CALL RestLib.patch_source()')
        self.rl.patch_source(self.base_url, source_url, JSON_UPDATED_NAME, source_id)
        self.mylog.info('test_update_source_name_field - STEP 3: DONE')
        self.mylog.info('test_update_source_name_field - STEP 4: CALL RestLib.get_source()')
        source = self.rl.get_source(self.base_url, source_url, source_id)
        self.mylog.info('test_update_source_name_field - STEP 4: DONE')
        self.verify_source(expected_updated, source_id, source)
        self.footer('test_update_source_name_field')

    def test_create_kapacitor(self):
        '''
        1. Create source and verify source_id is not None
        2. Get Kapacitor URL - /chronograf/v1/sources/<source_id>/kapacitors
        3. Create Kapacitor and verify kapacitor_id is not None
        4. Get kapacitor data for the above created kapacitor instance
        5. Assert Kapacitor is pig-able
        '''
        self.header('test_ create_kapacitor')
        source_url=self.get_source_path
        DATA_URL=self.data_nodes.split()[0]
        META_URL=self.meta_nodes.split()[0]
        KAPACITOR_URL='http://34.217.207.155:9022'
        SOURCE_NAME='CREATE KAPACITOR'
        KAPACITOR_NAME='KAPACITOR 1'
        JSON_SOURCE={'url':DATA_URL, 'metaUrl':META_URL, 'name':SOURCE_NAME, 'telegraf': 'telegraf', 'default': True}
        JSON_KAPACITOR={'url':KAPACITOR_URL, 'name':KAPACITOR_NAME}

        self.mylog.info('test_create_kapacitor - STEP 1: CREATE SOURCE (RestLib.create_source())')
        (status, message, source_id)=self.rl.create_source(self.base_url, source_url, JSON_SOURCE)
        assert source_id is not None, self.mylog.info('test_create_kapacitor : ASSERTION FAILED, source_id is None')
        self.mylog.info('test_create_kapacitor - STEP 2: GET KAPACITOR URL')
        source=self.rl.get_source(self.base_url, source_url, source_id)
        kapacitor_url=su.get_source_kapacitors_link(self, source_id, source)
        self.mylog.info('test_create_kapacitor - STEP 3: CREATE KAPACITOR (RestLib.create_kapacitor)')
        (status, message, kapacitor_id)=self.rl.create_kapacitor(self.base_url, kapacitor_url, JSON_KAPACITOR)
        assert kapacitor_id is not None, self.mylog.info('test_create_kapacitor : ASSERTION FAILED, kapacitor_id is None')
        self.mylog.info('test_create_kapacitor - STEP 4: GET KAPACITOR DATA(RestLib.get_kapacitor)')
        kapacitor_dictionary=self.rl.get_kapacitor(self.base_url, kapacitor_url, kapacitor_id)
        self.mylog.info('test_create_kapacitor - STEP 4: GET KAPACITOR PING LINK(util.kpacitor_util.get_kapacitor_ping)')
        ping_link=ku.get_kapacitor_ping(self, kapacitor_id, kapacitor_dictionary)
        self.mylog.info('test_create_kapacitor ping url =' + str(ping_link))
        self.mylog.info('test_create_kapacitor - STEP 5: PING KAPACITOR URL USING=' + str(ping_link))
        response=self.rl.get(self.base_url, ping_link)
        assert response.status_code == 204, self.mylog.info('test_create_kapacitor ASSERTION ERROR status_code=' +
                                                            str(response.status_code))
        self.footer('test_ create_kapacitor')




