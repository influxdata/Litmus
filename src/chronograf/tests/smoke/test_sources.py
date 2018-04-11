
import pytest
import src.util.login_util as lu
import src.util.sources_util as su
import src.util.kapacitor_util as ku
from src.chronograf.lib import rest_lib
from random import choice

# before running test suite make sure there are no sources.
@pytest.mark.usefixtures('chronograf', 'kapacitor',  'data_nodes', 'meta_nodes',
                                        'delete_created_sources', 'get_source_path',
                                        'http_auth', 'admin_user', 'admin_pass')
class TestSources():
    '''
    chronograf fixture - to get the chronograf URL
    kapacitor fixture  - to get kapacitor URL
    data_nodes - to get the list of data nodes URLs
    meta_nodes - to get the list of meta nodes URLs
    delete_created_source - to delete sources that were created by test(s) suites
    get_source_path - to get chronograf's source path, e.g./chronograf/v1/sources
    http_auth - where basic password authentication is available or not
    admin_user - admin user username
    admin_pass - admin user password
    '''

    mylog=lu.log(lu.get_log_path(), 'w', __name__)
    rl=rest_lib.RestLib(mylog)

    CUSTOM_NAME='Test Create Source User Options'
    UPDATE_NAME='Test Update Source Name'
    UPDATED_NAME='Updated Name Of The Source'
    DELETE_NAME='Delete source name'

    ##########################################################
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
        type = su.get_source_type(self, source_id, source)
        self.mylog.info('ASSERT ACTUAL type=' + str(type) + ' EQUALS '\
                        'EXPECTED type=' + str(expected['TYPE']))
        su.verify_data(self, expected['TYPE'], type)
        users = su.get_source_users_link(self, source_id, source)
        self.mylog.info('ASSERT ACTUAL users=' + str(users) + ' EQUALS EXPECTED '\
                        'users=' + str(expected['USERS']))
        su.verify_data(self, expected['USERS'], users)

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

    def test_get_default_sources_count(self):
        '''
        1. Get all of the default data sources
        2. Verify the number of data sources equals the number of data nodes.
        '''
        self.header('test_get_default_sources_count')
        self.mylog.info('test_get_default_sources_count - STEP 1: Get all default sources')
        sources=self.rl.get_sources(self.chronograf, self.get_source_path)
        # by default pcl will create data sources one per data node
        assert len(sources) == len(self.data_nodes), \
            self.mylog.info('test_get_default_sources_count() ASSERTION '
                            'FAILURE expected ' + str(len(sources)) + ', actual ' +
                            str(len(self.data_nodes)))
        self.footer('test_get_default_sources_count')

    def test_create_source_url_only(self):
        '''
        1. Creates source by using only one required param in request body - url of the data node.
        2. Asserts that ID of the source is not None
        3. Get data for the created source
        4. Verify expected response data equals actula response data from get source request.
        '''
        # choose a data node from a list of existing data nodes. For now use the first one
        source_url=self.get_source_path
        DATA_URL=choice(self.data_nodes)
        if self.http_auth:
            JSON_URL_ONLY = {'url': DATA_URL,'username':self.admin_user, 'password':self.admin_pass}
            USERNAME=self.admin_user
        else:
            JSON_URL_ONLY = {'url': DATA_URL}
            USERNAME=''

        self.header('test_create_source_url_only')
        self.mylog.info('test_create_source_url_only - STEP 1: CALL RestLib.create_source()')
        (status,message,source_id)=self.rl.create_source(self.chronograf, source_url, JSON_URL_ONLY)
        assert source_id is not None, self.mylog.info('test_create_source_url_only : ASSERTION FAILED, source_id is None')
        self.mylog.info('test_create_source_url_only - STEP 1: DONE SOURCE_ID=' + str(source_id))
        # Expected dictionary
        expected = {'NAME':'', 'INSECURE_SKIP_VERIFY':False, 'DATA_URL':DATA_URL,
                    'USERNAME': USERNAME,
                    'ROLES':'', 'DEFAULT':0, 'TELEGRAF_DB':'telegraf',
                    'SHARED_SECRET':'', 'META_URL':'',
                    'KAPACITOR':'/chronograf/v1/sources/%s/kapacitors' % source_id,
                    'WRITE':'/chronograf/v1/sources/%s/write' % source_id,
                    'PROXY':'/chronograf/v1/sources/%s/proxy' % source_id,
                    'PERMISSIONS':'/chronograf/v1/sources/%s/permissions' % source_id,
                    'QUERY':'/chronograf/v1/sources/%s/queries' % source_id,
                    'TYPE':'influx-enterprise', 'USERS':'/chronograf/v1/sources/%s/users' % source_id}

        self.mylog.info('test_create_source_url_only - STEP 2: CALL RestLib.get_source()')
        source=self.rl.get_source(self.chronograf, source_url, source_id)
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
        JSON_BAD_URL = {'url':'http://255.0.0.0:8087'}
        error_message='Error contacting source'
        source_url = self.get_source_path

        self.header('test_create_source_incorrect_url')
        self.mylog.info('test_create_source_incorrect_url - STEP 1: CALL RestLib.create_source()')
        (status, message, source_id) = self.rl.create_source(self.chronograf, source_url, JSON_BAD_URL)
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
        DATA_URL=choice(self.data_nodes)
        META_URL=choice(self.meta_nodes)
        if self.http_auth:
            JSON_USER_OPTIONS={'url':DATA_URL, 'metaUrl':META_URL, 'name':self.CUSTOM_NAME, 'telegraf':'telegraf',
                           'default':True, 'username':self.admin_user, 'password':self.admin_pass}
            USERNAME=self.admin_user
        else:
            JSON_USER_OPTIONS={'url':DATA_URL, 'metaUrl':META_URL, 'name':self.CUSTOM_NAME, 'telegraf':'telegraf',
                           'default':True}
            USERNAME=''

        self.header('test_create_source_user_options')
        self.mylog.info('test_create_user_options - STEP 1: CALL RestLib.create_source()')
        (status, message, source_id) = self.rl.create_source(self.chronograf, source_url, JSON_USER_OPTIONS)
        assert source_id is not None, self.mylog.info(
            'test_create_source_user_options : ASSERTION FAILED, source_id is None')
        self.mylog.info('test_create_user_options - STEP 1: DONE SOURCE_ID=' + str(source_id))
        # Expected dictionary
        expected = {'USERNAME':USERNAME, 'INSECURE_SKIP_VERIFY':False, 'DATA_URL':DATA_URL, 'NAME':self.CUSTOM_NAME,
                    'ROLES':'/chronograf/v1/sources/%s/roles' % source_id, 'DEFAULT':True, 'TELEGRAF_DB':'telegraf',
                    'SHARED_SECRET':'', 'META_URL':META_URL,
                    'KAPACITOR':'/chronograf/v1/sources/%s/kapacitors' % source_id,
                    'WRITE':'/chronograf/v1/sources/%s/write' % source_id,
                    'PROXY':'/chronograf/v1/sources/%s/proxy' % source_id,
                    'PERMISSIONS':'/chronograf/v1/sources/%s/permissions' % source_id,
                    'QUERY': '/chronograf/v1/sources/%s/queries' % source_id,
                    'TYPE':'influx-enterprise', 'USERS':'/chronograf/v1/sources/%s/users' % source_id}

        self.mylog.info('test_create_source_user_options - STEP 2: CALL RestLib.get_source()')
        source = self.rl.get_source(self.chronograf, source_url, source_id)
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
        DATA_URL=choice(self.data_nodes)
        META_URL=choice(self.meta_nodes)
        if self.http_auth:
            JSON_UPDATE_NAME = {'url': DATA_URL, 'metaUrl': META_URL, 'name': self.UPDATE_NAME, 'telegraf': 'telegraf',
                            'default': True, 'username':self.admin_user, 'password':self.admin_pass}
            JSON_UPDATED_NAME = {'url': DATA_URL, 'metaUrl': META_URL, 'name': self.UPDATED_NAME, 'telegraf': 'telegraf',
                             'default': True, 'username':self.admin_user, 'password':self.admin_pass}
            USERNAME=self.admin_user
        else:
            JSON_UPDATE_NAME = {'url': DATA_URL, 'metaUrl': META_URL, 'name': self.UPDATE_NAME, 'telegraf': 'telegraf',
                            'default': True}
            JSON_UPDATED_NAME = {'url': DATA_URL, 'metaUrl': META_URL, 'name': self.UPDATED_NAME, 'telegraf': 'telegraf',
                             'default': True}
            USERNAME=''

        self.header('test_update_source_name_field')
        self.mylog.info('test_update_source_name_field - STEP 1: CALL RestLib.create_source()')
        (status, message, source_id) = self.rl.create_source(self.chronograf, source_url, JSON_UPDATE_NAME)
        assert source_id is not None, self.mylog.info(
            'test_update_source_name_field : ASSERTION FAILED, source_id is None')
        self.mylog.info('test_update_source_name_field - STEP 1: DONE SOURCE_ID=' + str(source_id))
        # Expected dictionary
        expected={'USERNAME':USERNAME, 'INSECURE_SKIP_VERIFY':False, 'DATA_URL':DATA_URL, 'NAME':self.UPDATE_NAME,
                    'ROLES':'/chronograf/v1/sources/%s/roles' % source_id, 'DEFAULT':1, 'TELEGRAF_DB':'telegraf',
                    'SHARED_SECRET':'', 'META_URL':META_URL,
                    'KAPACITOR':'/chronograf/v1/sources/%s/kapacitors' % source_id,
                    'WRITE':'/chronograf/v1/sources/%s/write' % source_id,
                    'PROXY':'/chronograf/v1/sources/%s/proxy' % source_id,
                    'PERMISSIONS':'/chronograf/v1/sources/%s/permissions' % source_id,
                    'QUERY':'/chronograf/v1/sources/%s/queries' % source_id,
                    'TYPE':'influx-enterprise','USERS':'/chronograf/v1/sources/%s/users' % source_id}
        expected_updated={'USERNAME':USERNAME, 'INSECURE_SKIP_VERIFY':False,
                    'DATA_URL':DATA_URL, 'NAME':self.UPDATED_NAME,
                    'ROLES':'/chronograf/v1/sources/%s/roles' % source_id, 'DEFAULT': 1,
                    'TELEGRAF_DB': 'telegraf', 'SHARED_SECRET': '', 'META_URL': META_URL,
                    'KAPACITOR':'/chronograf/v1/sources/%s/kapacitors' % source_id,
                    'WRITE':'/chronograf/v1/sources/%s/write' % source_id,
                    'PROXY':'/chronograf/v1/sources/%s/proxy' % source_id,
                    'PERMISSIONS':'/chronograf/v1/sources/%s/permissions' % source_id,
                    'QUERY':'/chronograf/v1/sources/%s/queries' % source_id,
                    'TYPE':'influx-enterprise', 'USERS':'/chronograf/v1/sources/%s/users' % source_id}
        self.mylog.info('test_update_source_name_field - STEP 2: CALL RestLib.get_source()')
        source=self.rl.get_source(self.chronograf, source_url, source_id)
        self.mylog.info('test_update_source_name_field - STEP 2: DONE')
        self.verify_source(expected, source_id, source)
        self.mylog.info('test_update_source_name_field - STEP 3: CALL RestLib.patch_source()')
        self.rl.patch_source(self.chronograf, source_url, JSON_UPDATED_NAME, source_id)
        self.mylog.info('test_update_source_name_field - STEP 3: DONE')
        self.mylog.info('test_update_source_name_field - STEP 4: CALL RestLib.get_source()')
        source = self.rl.get_source(self.chronograf, source_url, source_id)
        self.mylog.info('test_update_source_name_field - STEP 4: DONE')
        self.verify_source(expected_updated, source_id, source)
        self.footer('test_update_source_name_field')

    def test_delete_source(self):
        '''
         1. Create source using data that user would be able to enter via UI, i.e:
             URL of data node, Name of the source, metaURL and telegraf database (All values are correct)
             Username and Password won't be used (requires different cluster configuration)
        2. Assert that ID of the source is not None
        3. Delete Created Source
        '''
        source_url = self.get_source_path
        DATA_URL=choice(self.data_nodes)
        META_URL=choice(self.meta_nodes)
        if self.http_auth:
            JSON_USER_OPTIONS={'url':DATA_URL, 'metaUrl':META_URL, 'name':self.DELETE_NAME, 'telegraf':'telegraf',
                           'default':True, 'username':self.admin_user, 'password':self.admin_pass}
        else:
            JSON_USER_OPTIONS={'url':DATA_URL, 'metaUrl':META_URL, 'name':self.DELETE_NAME, 'telegraf':'telegraf',
                           'default':True}
        self.header('test_delete_source')
        self.mylog.info('test_delete_source - STEP 1: CALL RestLib.create_source()')
        (status, message, source_id) = self.rl.create_source(self.chronograf, source_url, JSON_USER_OPTIONS)
        assert source_id is not None, self.mylog.info(
            'test_create_source_user_options : ASSERTION FAILED, source_id is None')
        self.mylog.info('test_create_user_options - STEP 1: DONE SOURCE_ID=' + str(source_id))
        self.mylog.info('test_delete_source - STEP 2 : DELETING SOURCE FOR source_id=' + str(source_id))
        self.rl.delete_source(self.chronograf, source_url, source_id)












