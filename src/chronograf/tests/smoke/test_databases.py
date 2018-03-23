
import pytest
import src.util.login_util as lu
import src.util.database_util as du
from src.chronograf.lib import rest_lib
from random import choice
from influxdb import InfluxDBClient as db_client
import re

@pytest.mark.usefixtures('delete_created_sources',
                         'delete_created_databases', 'default_sources',
                         'chronograf', 'data_nodes', 'all_sources', 'get_source_path')
class TestDefaultDatabases():
    '''
    '''
    mylog=lu.log(lu.get_log_path(), 'w', __name__)
    rl=rest_lib.RestLib(mylog)

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
        2. For every database verify retention policy duration, retention policy shard group duration,
            if retention policy is default one and default policy replication
        '''
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
        dbs_links=du.get_default_databases_links(self, default_sources=self.default_sources)
        for db in dbs_links:
            dictionary_of_dbs=self.rl.get_databases(self.chronograf, db)
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
                    # if policy is default one
                    assert telegraf_expected['rp_default'] == \
                           du.get_rp_default(self, retention_policies, telegraf_expected['rp_name'])
        self.footer('test_default_databases')

    def test_create_database_default_values(self):
        '''
        1. Get All Sources from the all_sources fixture
        2. Randomly choose one of the sources to create a database
        '''
        database_name='test create database default values'
        # database will be created with all default params
        data={'name':database_name}

        self.header('test_create_database_default_values')
        self.mylog.info('test_create_database_default_values() - '
                        'STEP 1: CHOOSE A SOURCE')
        if (len(self.all_sources) == 0): # we do not have any sources
            # create one
            data_node=choice(self.data_nodes)
            (status, body,source_id)=self.rl.create_source(self.chronograf,
                                                           self.get_source_path, {'url':data_node})
            assert source_id is not None
        else:
            source_id=choice(self.all_sources.keys())
        self.mylog.info('test_create_database_default_values() - STEP 2: '
                        'GET DBS URL FOR SOURCE ID=' + str(source_id))
        dbs_url=self.all_sources[source_id].get('DBS')
        self.mylog.info('test_create_database_default_values dbs_url=' + str(dbs_url))
        self.mylog.info('test_create_database_default_values() - '
                        'STEP 3: CREATE DATABASE ' + database_name)
        response=self.rl.create_database(self.chronograf, dbs_url, json=data)
        self.mylog.info('test_create_database_default_values :' + str(response))
        assert response.get('name') == database_name
        assert response.get('retentionPolicies')[0].get('name') == 'autogen'
        assert response.get('retentionPolicies')[0].get('replication') == 2
        assert response.get('retentionPolicies')[0].get('duration') == '0s'
        assert response.get('retentionPolicies')[0].get('shardDuration') == '168h0m0s'
        self.footer('test_create_database_default_values')

    def test_delete_databse_default_values(self):
        '''

        '''
        database_name='test delete database default values'
        # database will be created with all default params
        data={'name':database_name}

        self.header('test_delete_database_default_values')
        self.mylog.info('test_delete_database_default_values() - '
                        'STEP 1: CHOOSE A SOURCE')
        if (len(self.all_sources) == 0): # we do not have any sources
            # create one
            data_node=choice(self.data_nodes)
            (status, body,source_id)=self.rl.create_source(self.chronograf,
                                                           self.get_source_path, {'url':data_node})
            assert source_id is not None
        else:
            source_id=choice(self.all_sources.keys())
        self.mylog.info('test_delete_database_default_values() - STEP 2: '
                        'GET DBS URL FOR SOURCE ID=' + str(source_id))
        dbs_url=self.all_sources[source_id].get('DBS')
        self.mylog.info('test_delete_database_default_values dbs_url=' + str(dbs_url))
        self.mylog.info('test_delete_database_default_values() - '
                        'STEP 3: CREATE DATABASE ' + database_name)
        response=self.rl.create_database(self.chronograf, dbs_url, json=data)
        db_name=response.get('name')
        self.mylog.info('test_delete_database_default_values() - '
                        'STEP 4: DELETING DATABASE ' + str(db_name))
        self.rl.delete_database(self.chronograf, dbs_url, db_name)

    def test_create_rp(self):
        '''
        1. Create retention policy for a default database (_internal)
        '''
        self.header('test_create_rp')
        rp_name='test_create_rp'
        data={'name':rp_name, 'duration':'1d', 'replication':2, 'shardDuration':'2h', 'isDefault':True}
        # need to get a source to be able to get a link to a database (allows us to get a rp link to create a rp)
        data_node=re.search(r'http://(\d+.\d+.\d+.\d+):[0-9]+',choice(self.data_nodes)).group(1) #http://<IP>:<port>
        client=db_client(data_node)

        self.mylog.info('test_create_rp - STEP 1: CHOOSE SOURCE_ID')
        source_id=choice(self.all_sources.keys())
        assert source_id is not None # just a precaution
        self.mylog.info('test_create_rp - STEP 2 : GET THE DATABASE URL FOR A SOURCE_ID ' + str(source_id) )
        dbs_url=self.all_sources[source_id].get("DBS")
        self.mylog.info('test_create_rp - STEP 3: get database info')
        result=self.rl.get_database(self.chronograf, dbs_url, '_internal')
        self.mylog.info('STEP 3 result = ' + str(result))
        self.mylog.info('test_create_rp - STEP4: GET RETENTION POLICY LINK')
        rp_link=result.get('POLICY_LINKS')
        assert rp_link is not None # just a precaution
        self.mylog.info('test_create_rp - STEP 5: CREATE A RETENTION POLICY')
        response=self.rl.create_retention_policy_for_database(self.chronograf, rp_link, json=data)
        # delete created retention policy
        client.drop_retention_policy(rp_name, '_internal')
        assert response['name'] == rp_name
        assert response['duration'] == '24h0m0s'
        assert response['replication'] == 2
        assert response['shardDuration'] == '2h0m0s'
        assert response['isDefault'] is True

    def test_alter_rp(self):
        '''

        '''
        self.header('test_alter_rp')
        rp_name='test_alter_rp'
        data={'name':rp_name, 'duration':'2d', 'replication':1, 'shardDuration':'1h', 'isDefault':False}
        updated_data={'name':rp_name, 'duration':'3d', 'replication':2, 'shardDuration':'2h', 'isDefault':False}
        # need to get a source to be able to get a link to a database (allows us to get a rp link to create a rp)
        data_node=re.search(r'http://(\d+.\d+.\d+.\d+):[0-9]+',choice(self.data_nodes)).group(1) #http://<IP>:<port>
        client=db_client(data_node)

        self.mylog.info('test_alter_rp - STEP 1: CHOOSE SOURCE_ID')
        source_id=choice(self.all_sources.keys())
        assert source_id is not None # just a precaution
        self.mylog.info('test_alter_rp - STEP 2 : GET THE DATABASE URL FOR A SOURCE_ID ' + str(source_id) )
        dbs_url=self.all_sources[source_id].get("DBS")
        self.mylog.info('test_alter_rp - STEP 3: get database info')
        result=self.rl.get_database(self.chronograf, dbs_url, '_internal')
        self.mylog.info('STEP 3 result = ' + str(result))
        self.mylog.info('test_alter_rp - STEP4: GET RETENTION POLICY LINK')
        rp_link=result.get('POLICY_LINKS')
        assert rp_link is not None # just a precaution
        self.mylog.info('test_alter_rp - STEP 5: CREATE A RETENTION POLICY')
        response=self.rl.create_retention_policy_for_database(self.chronograf, rp_link, json=data)
        self.mylog.info('test_alter_rp - STEP 6: ALTER RETENTION POLICY')
        response=self.rl.patch_retention_policy_for_database(self.chronograf, rp_link, rp_name, json=updated_data )
        assert response['name'] == rp_name
        assert response['duration'] == '72h0m0s'
        assert response['replication'] == 2
        assert response['shardDuration'] == '2h0m0s'
        assert response['isDefault'] is False

