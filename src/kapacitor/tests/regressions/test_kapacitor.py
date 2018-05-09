import pytest
import src.util.login_util as lu
import src.util.database_util as du
import time
from src.chronograf.lib import chronograf_rest_lib
from src.kapacitor.lib import kapacitor_rest_lib
from random import choice
from influxdb import InfluxDBClient as influxDBClient
from src.influxdb.lib import influxdb_rest_lib


@pytest.mark.usefixtures('delete_created_db','delete_kapacitors_tasks')
class TestKapacitorRegressions(object):
    '''
    kapacitor fixture returns the URL of kapacitor, such as http://<ip>:<port>
                (currently only supports http protoco)
    data_nodes_ips fixture returns the list of ip addresses of the data nodes
    delete_created_db fixture - deletes all of the databases with the exception
    of _internal and telegraf
    delete_kapacitor_tasks fixture- delete all of the existing kapacitor's tasks
     '''
    mylog=lu.log(lu.get_log_path(), 'w', __name__)
    rl=chronograf_rest_lib.RestLib(mylog)
    krl=kapacitor_rest_lib.KapacitorRestLib(mylog)
    irl=influxdb_rest_lib.InfluxDBInfluxDBRestLib(mylog)

    # need to move this method into library eventually
    def show_subscripitons(self, data_url, db_name, auth=None):
        subscriptions=False
        time_end = time.time() + 15
        while time.time() < time_end:
            (success, subscription_d, error)=self.irl.show_subscriptions(data_url, auth=auth)
            assert success, self.mylog.info('test_del_db_sending_data_to_kapacitor : Assertion Error ' + str(error))
            if db_name in subscription_d.keys():
                subscriptions=True
                self.mylog.info('test_del_db_sending_data_to_kapacitor : FOUND SUBSCRIPITON')
                break
            else:
                self.mylog.info('test_del_db_sending_data_to_kapacitor : SLEEPING FOR 1 SEC')
                time.sleep(1)
                continue
        return subscriptions

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
    def test_del_db_sending_data_to_kapacitor(self):
        """
        1. Update config file to set subscription-sync-interval to 5 seconds
        2. Create a task
        3. Create database using python client APIs
        """
        test_name='test_del_db_sending_data_to_kapacitor'
        data_node_to_connect=choice(self.data_nodes_ips)
        db_name='tddsdtk_db'
        task_name='tddsdtk'
        field_value_1='This is a first data to write'
        field_value_final= 'This is a final data to write'
        # eventually move 'set' to the the set_value method in kapacitor rest lib
        #data_to_set={'set':{'subscriptions-sync-interval':'5s'}}
        data_to_set={'subscriptions-sync-interval':'5s'}
        task_to_create={'id':task_name, 'type':'stream',
                        'dbrps':[{'db':'tddsdtk_db','rp':'autogen'}],
                        'script':'stream\n |from()\n .measurement(\'test\')\n |httpOut(\'test\')\n',
                        'status':'enabled'}
        first_data_to_write= [{'measurement': 'test','tags':
            {'host': 'server01','region': 'us-west'},
            'fields': {'f1':field_value_1,}}]
        final_data_to_write= [{'measurement': 'test','tags':
            {'host': 'server01','region': 'us-west'},
            'fields': {'f1':  field_value_final,}}]
        if self.http_auth:
            username=self.admin_user
            password=self.admin_pass
            auth=(username,password)
        else:
            username=''
            password=''
            auth=None
        client=influxDBClient(data_node_to_connect, 8086,
                              username=username, password=password)
        self.mylog.info(test_name + ' : STEP 1 - update subscription-sync-interval in kapacitor config '
                                    'file to be 5second instead of 1 min')
        self.krl.set_value(self.kapacitor, 'influxdb', data_to_set)
        self.krl.verify_set_value(self.kapacitor, 'influxdb', json=data_to_set)
        # create a task that will print a received point from a test database
        self.mylog.info(test_name + ' : STEP 2 Creating Task')
        self.krl.create_task(self.kapacitor, json=task_to_create)
        # create a database with RP=autogen
        self.mylog.info(test_name + ' : STEP 3 Creating Database')
        du.create_database(self, client, db_name)
        # wait for up to 10 seconds and check if subscription to the database was created
        self.mylog.info(test_name + ' : STEP 4 Verifying Kapacitor created a subscription to a DB')
        subscriptions=self.show_subscripitons('http://'+data_node_to_connect+':8086', db_name, auth=auth)
        assert subscriptions, self.mylog.info(test_name + ' Did not find any subscriptions')
        self.mylog.info(test_name + ' : STEP 5 Send Test Data')
        assert du.write_points(self, client, points=first_data_to_write,
                               database=db_name)
        self.mylog.info(test_name + ' : STEP 6 Verify Kapacitor receieved the data')
        path_to_hhtpout=self.krl.KAPACITOR_TASKS + '/' + task_name + '/test'
        result=self.rl.get(self.kapacitor, path_to_hhtpout)
        assert result.status_code == 200, \
            self.mylog.info(test_name + ' Assertion Failure status code=' + str(result.status_code))
        value=result.json()['series']
        # getting the field value of first_data_to_wrtie
        self.mylog.info(test_name + ' - data recieved by kapacitor :' + str(value))
        assert field_value_1 in value[0]['values'][0], \
            self.mylog.info('Assertion Failure field_value_1 ' + field_value_1
                            + ' cannot be found in the last record written : '
                            + str(value[0]['values']))
        self.mylog.info(test_name + ' : STEP 7 Drop Database %s that is sending data to kapacitor ' % db_name)
        client.drop_database(db_name)
        self.mylog.info(test_name + ' : STEP 8 SHOW SUBSCRIPTIONS')
        subscriptions=self.show_subscripitons('http://'+data_node_to_connect+':8086', db_name, auth=auth)
        assert subscriptions == False, self.mylog.info(test_name + ' Found a subscription')
        self.mylog.info(test_name + ' : STEP 9 Recreating Database')
        du.create_database(self, client, db_name)
        # wait for up to 10 seconds and check if subscription to the database was created
        self.mylog.info(test_name + ' : STEP 10 Verifying Kapacitor created a subscription to a DB')
        subscriptions=self.show_subscripitons('http://'+data_node_to_connect+':8086', db_name, auth=auth)
        assert subscriptions, \
            self.mylog.info(test_name +  ' Did not find any subscriptions')
        self.mylog.info(test_name + ' : STEP 11 Send Test Data')
        assert du.write_points(self, client, points=final_data_to_write,
                               database=db_name)
        self.mylog.info(test_name + ' : STEP 12 Verify Kapacitor receieved the data')
        path_to_hhtpout=self.krl.KAPACITOR_TASKS + '/' + task_name + '/test'
        result=self.rl.get(self.kapacitor, path_to_hhtpout)
        assert result.status_code == 200, \
            self.mylog.info('Assertion Failure status code=' + str(result.status_code))
        value=result.json()['series']
        # getting the field value of first_data_to_wrtie
        self.mylog.info(test_name + ' - data recieved by kapacitor :' + str(value))
        assert field_value_final in value[0]['values'][0], \
            self.mylog.info('Assertion Failure field_value_final ' + field_value_final
                            + ' cannot be found in the last record written : '
                            + str(value[0]['values']))