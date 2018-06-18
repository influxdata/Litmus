import pytest
import src.util.login_util as lu
import src.util.database_util as du
import src.util.influxctl_util as iu
import src.util.litmus_utils as litmus_utils
from src.influxdb.lib import influxdb_rest_lib
from influxdb import InfluxDBClient as InfluxDBClient
from random import choice
import datetime
import time

# There are two plutonium tests for AE service:
# 1. Replace one data node with another (data should be copied from old node to the new node)
# 2. Add an extra data node and remove one of the previously existing data nodes (All the data from removed node
#    should be copied to the newly added node.

@pytest.mark.usefixtures('data_nodes_ips', 'meta_leader', 'clusteros', 'privatekey', 'data_nodes')
class TestAEService(object):
    '''
    '''
    mylog=lu.log(lu.get_log_path(), 'w', __name__)
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
    ####################################################################################################################

    @pytest.mark.parametrize('drop_database', ['test_tsm_db'], ids=[''], indirect=True)
    @pytest.mark.usefixtures('drop_database')
    def test_tsm_diffs(self):
        '''
        '''
        time_minus_3_days_ms=int(10800000)
        test_name='test_tsm_diffs '
        database_name='test_tsm_db'
        rp='tsm_diff'
        user=self.clusteros
        host=(self.meta_leader).split('//')[1][:-5]
        privatekey=self.privatekey
        data_node=choice(self.data_nodes_ips)
        username, password='',''
        current_time_sec=int((datetime.datetime.utcnow()-datetime.datetime(1970,1,1)).total_seconds())
        point_time_sec=current_time_sec -10800 -1
        current_time_ms=current_time_sec * 1000
        point_time=current_time_ms-time_minus_3_days_ms
        if self.http_auth: # it is not supported by the writenode tool
            username=self.admin_user
            password=self.admin_pass
        point=[{'measurement': 'test_tsm',
                'time':point_time,
                'fields':{'value':1},
                'tags':{'t':1}
                }]
        cmd_chmod='ssh -i %s -o StrictHostKeyChecking=no %s@%s \'cd /tmp; sudo chmod +x writenode_lin\'' \
                  % (privatekey, user, host)
        shard_id=None

        self.header(test_name)
        self.mylog.info(test_name + 'STEP 1: Create InfluxDBClient')
        client=InfluxDBClient(data_node, username=username, password=password)
        self.mylog.info(test_name + 'STEP 2: Create database')
        (success, error)=du.create_database(self, client, database_name)
        assert success, self.mylog.info(test_name + 'Failure to create database :' + str(error))
        self.mylog.info(test_name + 'STEP 3: Create retention policy with Replicaiton Factor 2')
        (success, error)=du.create_retention_policy(self, client, rp_name=rp, duration='36h',
                                                    replication='2', database=database_name, default=True)
        assert success, self.mylog.info(test_name + 'Failure to create retention policy :' + str(error))
        # every 5 seconds if there are no writes the data from WAL will be written to TSM file
        # (INFLUXDB_DATA_CACHE_SNAPSHOT_WRITE_COLD_DURATION="5s" - setting in data section, provided through installer
        self.mylog.info(test_name + 'STEP 4: Write a point into %s database' % database_name)
        self.mylog.info(test_name + 'POINT_TIME_SEC=' + str(point_time_sec))
        result=du.write_points(self, client, points=point, time_precision='ms', database=database_name)
        assert result, self.mylog.info(test_name + 'Failure to write a point first time')
        self.mylog.info(test_name + 'STEP 5: Wait for 7sec(CACHE_SNAPSHOT_WRITE_COLD_DURATION=5sec) before writing '
                                    'a second point to create a second tsm file')
        time.sleep(7)
        # at this time we should have one tsm file (the same shard group) on two of the data nodes
        self.mylog.info(test_name + 'STEP 6: Load extra data into randomly chosen data node to cause entropy')
        status, result, error=self.irl._show_cluster(self.meta_leader)
        assert status, self.mylog.info(test_name + 'Failed to show cluster info :' + str(error))
        data_node_id=choice(iu.show_cluster_data_nodes(self, result).keys())
        self.mylog.info(test_name + 'Write extra data to \'%s\' node' % str(data_node_id))
        status, result, error=self.irl._show_shards(self.meta_leader)
        assert status, self.mylog.info(test_name + 'Failed to show shards info :' + str(error))
        shards=iu.show_shards(self, result)
        # get the shard id the extra data should be written to
        for key, value in shards.items():
            if value['database'] == database_name:
                shard_id=key
                self.mylog.info(test_name + 'SHARD_ID=' + str(shard_id))
                break
        assert 0 == litmus_utils.execCmd(self, cmd_chmod), \
            self.mylog.info(test_name + 'Failied to execute \'%s\'' % cmd_chmod)
        cmd='ssh -i %s -o StrictHostKeyChecking=no %s@%s \'cd /tmp; ./writenode_lin -node %d -points 100 -shards %s' \
            ' -starttime %d\'' % (privatekey, user, host, data_node_id, shard_id, point_time_sec)
        assert 0 == litmus_utils.execCmd(self, cmd), \
            self.mylog.info(test_name + 'Failied to execute \'%s\'' % cmd)
        self.mylog.info(test_name + 'Wait for 10 sec (INFLUXDB_DATA_COMPACT_FULL_WRITE_COLD_DURATION=10s) '
                                    'for compaction to complete')
        time.sleep(15)
        self.mylog.info(test_name + 'GET SHARD STRUCTURE OF DATANODES')
        for datanode in self.data_nodes_ips:
            litmus_utils.shard_layout(self, privatekey, '/var/lib/influxdb/data', database_name, rp,
                                          shard_id, user, datanode)
        self.mylog.info(test_name + 'STEP 7: Verify entropy was detected')
        success, result, message=self.irl._show_entropy(choice(self.data_nodes))
        assert success, self.mylog.info(test_name + 'Failure to run \'show entropy\' :' + str(error))
        entropy_shard=iu.show_entropy_shards(self, result)
        self.mylog.info(test_name + 'Assert expected status=diff equals to ' + entropy_shard[shard_id].get('status'))
        assert entropy_shard[shard_id].get('status') == 'diff', self.mylog.info('Assertion Error')
        # TODO: add retentin policy and database assertions.
        self.mylog.info(test_name + 'STEP 8: Fix entropy')
        (success,message)=self.irl.shard_repair(choice(self.data_nodes),shard_id)
        assert success, self.mylog.info(test_name + 'Failed to repair shard %s, message=%s' % (shard_id, message))
        self.mylog.info(test_name + 'GET SHARD STRUCTURE OF DATANODES AFTER SHARD REPAIR')
        for datanode in self.data_nodes_ips:
            litmus_utils.shard_layout(self, privatekey, '/var/lib/influxdb/data', database_name, rp,
                                      shard_id, user, datanode)
        time.sleep(10)
        success, result, message = self.irl._show_entropy(choice(self.data_nodes))
        assert success, self.mylog.info(test_name + 'Failure to run \'show entropy\' :' + str(error))
        entropy_shard=iu.show_entropy_shards(self, result)
        assert entropy_shard == {}
        self.footer(test_name)