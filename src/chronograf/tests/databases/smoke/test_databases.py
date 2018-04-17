import pytest
import src.util.login_util as lu
import src.util.database_util as du
from src.chronograf.lib import rest_lib
from random import choice


@pytest.mark.usefixtures('chronograf', 'data_nodes', 'get_source_path',
                         'delete_created_databases', 'delete_created_rp',
                         'delete_created_sources', 'default_sources',
                         'http_auth', 'admin_user', 'admin_pass')
class TestDefaultDatabases(object):
    '''
    delete_created_databases - deletes all of the databases created by tests
    delete_created_rp - removes all of the created, non-default retention policies
    delete_created_sources - deletes all of the non-default data sources
    default_sources - gets all of the default sources
    chronograf - returns chronograf URL
    data_nodes - returns the list of data nodes URLS
    get_source_path - returns path to a 'source' URL
     '''
    mylog=lu.log(lu.get_log_path(), 'w', __name__)
    rl=rest_lib.RestLib(mylog)

    create_rp_name='test_create_rp'
    alter_rp_name='test_alter_rp'
    delete_rp_name='test_delete_rp'
    database_name_rp='_internal'

    # Cannot use setup_class with fixtures since it si being called before fixtures.
    # Have to move clean up using InfluxDBClient into conftest with params, where
    # parameters are created names of the retention policies.

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

    def test_default_databases(self):
        '''
        1. Get default databases (_internal and telegraf)
        2. For every default database verify retention policy duration, retention
            policy shard group duration, if retention policy is default one and
            default policy replication
        '''
        # Default sources cannot be used to get databases
        internal_expected={
            'rp_duration':'168h0m0s',
            'rp_replication':1,
            'rp_default':True,
            'rp_shard_duration':'24h0m0s',
            'rp_name':'monitor'
        }
        telegraf_expected={
            'rp_duration':'0s',
            'rp_replication':2,
            'rp_default':True,
            'rp_shard_duration':'168h0m0s',
            'rp_name':'autogen'
        }
        self.header('test_default_databases')
        self.mylog.info('test_default_databases - STEP 1: GET DBS LINKS')
        # in a 2 data nodes set ups we will end up with 2 default data sources = 2 dbs links
        # dbs_links = [u'/chronograf/v1/sources/1/dbs', u'/chronograf/v1/sources/2/dbs']
        dbs_links=du.get_default_databases_links(self, default_sources=self.default_sources)
        for link in dbs_links:
            self.mylog.info('test_default_databases - STEP 2: GET ALL OF THE DATABASES')
            # get all of the databases per dbs link
            dictionary_of_dbs=self.rl.get_databases(self.chronograf, link)
            # iterate over database names for a specific source
            for db_name in dictionary_of_dbs.keys():
                if db_name == '_internal':
                    retention_policies=du.get_retention_policies(self, dictionary_of_dbs, db_name)
                    # assert retention policy duration
                    assert internal_expected['rp_duration'] == \
                           du.get_rp_duration(self, retention_policies, internal_expected['rp_name'])
                    # assert retention policy replication
                    assert internal_expected['rp_replication'] == \
                            du.get_rp_replication(self, retention_policies, internal_expected['rp_name'])
                    # assert shard duration
                    assert internal_expected['rp_shard_duration'] == \
                            du.get_rp_shardduration(self, retention_policies, internal_expected['rp_name'])
                    # if policy is default
                    #assert internal_expected['rp_default'] == \
                    #        du.get_rp_default(self, retention_policies, internal_expected['rp_name'])
                if db_name == 'telegraf':
                    retention_policies=du.get_retention_policies(self, dictionary_of_dbs, db_name)
                    # assert retention policy duration
                    assert telegraf_expected['rp_duration'] == \
                           du.get_rp_duration(self, retention_policies, telegraf_expected['rp_name'])
                    # assert retention policy replication
                    assert telegraf_expected['rp_replication'] == \
                            du.get_rp_replication(self, retention_policies, telegraf_expected['rp_name'])
                    # assert shard duration
                    assert telegraf_expected['rp_shard_duration'] == \
                            du.get_rp_shardduration(self, retention_policies, telegraf_expected['rp_name'])
        self.footer('test_default_databases')

    def test_create_database_default_values(self):
        '''
        1. Get default Sources from the all_sources fixture
        2. Randomly choose one of the sources to create a database
        '''
        test_name='test_create_database_default_values '
        database_name='test create database default values'
        # database will be created with all default params
        data={'name':database_name}

        self.header(test_name)
        self.mylog.info(test_name + ' - STEP 1: CHOOSE A SOURCE')
        if (len(self.default_sources) == 0): # we do not have any sources
            # create one
            data_node=choice(self.data_nodes)
            (status, body,source_id)=self.rl.create_source(self.chronograf,
                                                           self.get_source_path, {'url':data_node})
            assert source_id is not None
        else:
            source_id=choice(self.default_sources.keys())
        self.mylog.info(test_name + ' - STEP 2: GET DBS URL FOR SOURCE ID='
                        + str(source_id))
        dbs_url=self.default_sources[source_id].get('DBS')
        self.mylog.info(test_name + str(dbs_url))
        self.mylog.info(test_name + 'STEP 3: CREATE DATABASE ' + database_name)
        response=self.rl.create_database(self.chronograf, dbs_url, json=data)
        assert response.status_code == 201, \
            self.mylog.info(test_name + ' Assertion Error' + str(response.text))
        self.mylog.info(test_name + str(response.json()))
        assert response.json().get('name') == database_name
        assert response.json().get('retentionPolicies')[0].get('name') == 'autogen'
        assert response.json().get('retentionPolicies')[0].get('replication') == 2
        assert response.json().get('retentionPolicies')[0].get('duration') == '0s'
        assert response.json().get('retentionPolicies')[0].get('shardDuration') == '168h0m0s'
        self.footer(test_name)

    def test_delete_database_default_values(self):
        '''
        1. Choose a source from available default sources, otherwise create a
            new data source
        2. Get a DB link for a chosen source
        3. Create a database using just a database name as a param
        4. Delete created database
        '''
        test_name='test_delete_database_default_values '
        database_name='test delete database default values'
        # database will be created with all default params
        data={'name':database_name}

        self.header(test_name)
        self.mylog.info(test_name + 'STEP 1: CHOOSE A SOURCE')
        if (len(self.default_sources) == 0): # we do not have any sources
            # create one
            data_node=choice(self.data_nodes)
            (status, body,source_id)=self.rl.create_source(self.chronograf,
                                                           self.get_source_path, {'url':data_node})
            assert source_id is not None
        else:
            source_id=choice(self.default_sources.keys())
        self.mylog.info(test_name + ' - STEP 2: GET DBS URL FOR SOURCE ID='
                        + str(source_id))
        dbs_url=self.all_sources[source_id].get('DBS')
        self.mylog.info(test_name + ' dbs_url=' + str(dbs_url))
        self.mylog.info(test_name +'STEP 3: CREATE DATABASE ' + database_name)
        response=self.rl.create_database(self.chronograf, dbs_url, json=data)
        assert response.status_code == 201, \
            self.mylog.info(test_name + ' Assertion Error' + str(response.text))
        db_name=response.json().get('name')
        self.mylog.info(test_name + 'STEP 4: DELETING DATABASE ' + str(db_name))
        response=self.rl.delete_database(self.chronograf, dbs_url, db_name)
        assert response.status_code == 204, \
            self.mylog.info(test_name + ' Assertion Error' + str(response.text))
        self.footer(test_name)

    def test_create_rp(self):
        '''
        1. Choose a source id from available default sources
        2. Get a Db url for a chosen source
        3. Get a data for an _internal database
        4. Get a link to RP URL
        5. Create a RP and assert the results
        '''
        test_name='test_create_rp '
        self.header(test_name)
        data={'name':self.create_rp_name, 'duration':'1d', 'replication':2,
              'shardDuration':'2h', 'isDefault':False}
        # need to get a source to be able to get a link to a database
        # (allows us to get a rp link to create a rp)
        self.mylog.info(test_name + ' - STEP 1: CHOOSE SOURCE_ID')
        source_id=choice(self.default_sources.keys())
        assert source_id is not None # just a precaution
        self.mylog.info(test_name + '- STEP 2 : GET THE DATABASE URL FOR '
                                    'A SOURCE_ID ' + str(source_id) )
        dbs_url=self.default_sources[source_id].get("DBS")
        self.mylog.info(test_name + ' - STEP 3: get database info')
        result=self.rl.get_database(self.chronograf, dbs_url, self.database_name_rp)
        self.mylog.info(test_name + 'STEP 3 result = ' + str(result))
        self.mylog.info(test_name + ' - STEP4: GET RETENTION POLICY LINK')
        rp_link=result.get('POLICY_LINKS')
        assert rp_link is not None # just a precaution
        self.mylog.info('test_create_rp - STEP 5: CREATE A RETENTION POLICY')
        response=self.rl.create_retention_policy_for_database(self.chronograf, rp_link, json=data)
        assert response.status_code == 201, \
            self.mylog.info(test_name + ' Assertion Error' + str(response.text))
        assert response.json()['name'] == self.create_rp_name
        assert response.json()['duration'] == '24h0m0s'
        assert response.json()['replication'] == 2
        assert response.json()['shardDuration'] == '2h0m0s'
        assert response.json()['isDefault'] is False

    def test_alter_rp(self):
        '''
        1. Choose a source from available default sources
        2. Get DB URL for a chosen source
        3. Get DB info for _internal DB
        4. Get a link to a RP URL
        5. Create RP
        6. Alter created RP
        '''
        test_name='test_alter_rp'
        self.header(test_name)
        data={'name':self.alter_rp_name, 'duration':'2d', 'replication':1, 'shardDuration':'1h', 'isDefault':False}
        updated_data={'name':self.alter_rp_name, 'duration':'3d', 'replication':2, 'shardDuration':'2h', 'isDefault':False}

        self.mylog.info(test_name + '- STEP 1: CHOOSE SOURCE_ID')
        source_id=choice(self.default_sources.keys())
        assert source_id is not None # just a precaution
        self.mylog.info(test_name + ' - STEP 2 : GET THE DATABASE URL FOR A SOURCE_ID ' + str(source_id) )
        dbs_url=self.default_sources[source_id].get("DBS")
        self.mylog.info(test_name + '- STEP 3: get database info')
        result=self.rl.get_database(self.chronograf, dbs_url, self.database_name_rp)
        self.mylog.info(test_name + 'STEP 3 result = ' + str(result))
        self.mylog.info(test_name + '- STEP4: GET RETENTION POLICY LINK')
        rp_link=result.get('POLICY_LINKS')
        assert rp_link is not None # just a precaution
        self.mylog.info(test_name + '- STEP 5: CREATE A RETENTION POLICY')
        self.rl.create_retention_policy_for_database(self.chronograf, rp_link, json=data)
        self.mylog.info(test_name + '- STEP 6: ALTER RETENTION POLICY')
        response_alter=self.rl.patch_retention_policy_for_database(self.chronograf, rp_link, self.alter_rp_name, json=updated_data )
        assert response_alter.status_code == 201, \
            self.mylog.info(test_name + ' Assertion Error' + str(response_alter.text))
        assert response_alter.json()['name'] == self.alter_rp_name
        assert response_alter.json()['duration'] == '72h0m0s'
        assert response_alter.json()['replication'] == 2
        assert response_alter.json()['shardDuration'] == '2h0m0s'
        assert response_alter.json()['isDefault'] is False

    def test_delete_rp(self):
        '''
        1. Choose a source from available default sources
        2. Get a DB URL for a chosen source
        3. Get info for a _internal DB
        4. Get a link to a RP
        5. Create a RP
        6. Delete created RP
        '''
        test_name='test_delete_rp '
        self.header(test_name)
        data={'name':self.delete_rp_name, 'duration':'4d', 'replication':2, 'shardDuration':'2h', 'isDefault':False}

        self.mylog.info(test_name + ' - STEP 1: RANDOMLY CHOOSE SOURCE_ID')
        source_id=choice(self.default_sources.keys())
        assert source_id is not None # just a precaution
        self.mylog.info(test_name + ' - STEP 2 : GET THE DATABASE URL FOR A SOURCE_ID ' + str(source_id) )
        dbs_url=self.default_sources[source_id].get("DBS")
        self.mylog.info(test_name + ' - STEP 3: get database info')
        result=self.rl.get_database(self.chronograf, dbs_url, self.database_name_rp)
        self.mylog.info(test_name + 'STEP 3 result = ' + str(result))
        self.mylog.info(test_name + ' - STEP4: GET RETENTION POLICY LINK')
        rp_link=result.get('POLICY_LINKS')
        assert rp_link is not None # just a precaution
        self.mylog.info(test_name + '- STEP 5: CREATE A RETENTION POLICY')
        self.rl.create_retention_policy_for_database(self.chronograf, rp_link, json=data)
        self.mylog.info(test_name + '- STEP 6: DELETE RETENTION POLICY')
        response=self.rl.delete_retention_policy_for_database(self.chronograf, rp_link, self.delete_rp_name)
        assert response.status_code == 204, \
            self.mylog.info(test_name + ' Assertion Error' + str(response.text))
        self.footer(test_name)
