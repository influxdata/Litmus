import pytest
import re
from influxdb import InfluxDBClient as InfluxDbClient
from influxdb import exceptions as e
from random import choice
from src.kapacitor.lib import kapacitor_rest_lib
from src.chronograf.lib import rest_lib
import src.util.database_util as du

'''
 need to remove the created databases, all with the exception of 
 internal and telegraf by using InfluxDBClient. This woudl be different
 from dropping databases using chronograf APIs
'''

@pytest.fixture(scope='class')
def delete_created_db(request, data_nodes_ips, http_auth, admin_user,
                      admin_pass):
    '''
    :param request:request object to introspect the requesting test function,
                class or module context
    :param data_nodes_ips: ip addresses of the all of the data nodes
    :return: nothing
    '''
    default_db=['_internal','telegraf']
    host=choice(data_nodes_ips)
    client=None
    request.cls.mylog.info('FIXTURE delete_created_db IS CALLED')
    request.cls.mylog.info('FIXTURE delete_created_db - set up influxdb'
                           ' connection using host=' + str(host))
    try:
        if http_auth:
            username=admin_user
            password=admin_pass
        else:
            username=''
            password=''
        client=InfluxDbClient(host, 8086, username=username, password=password)
        #  [{u'name': u'_internal'}, {u'name': u'telegraf'}, {u'name': u'test_db'}]
        request.cls.mylog.info('FIXTURE delete_created_db. Deleting all '
                               'created databases that not in the default '
                               'databases list ' + str(default_db))
        for db in client.get_list_database():
            if db['name'] not in default_db:
                request.cls.mylog.info('FIXTURE delete_created_db. '
                                       'Dropping ' + db['name'] + ' database')
                client.drop_database(db['name'])
        client.close()
    except e.InfluxDBClientError:
        request.cls.mylog.info('ClientError message=' + e.InfluxDBClientError.message)
        if client is not None:
            client.close()
    except e.InfluxDBServerError:
        request.cls.mylog.info('ServerError message=' + e.InfluxDBServerError.message)
        if client is not None:
            client.close()
    request.cls.mylog.info('FIXTURE delete_created_db IS DONE')

@pytest.fixture(scope='class')
def delete_kapacitors_tasks(request, kapacitor):
    """
    :param request:
    :param kapacitor:
    :return:
    """
    '''
    1. Need to get the list of all tasks 
    2. iterated over the list of task and delete them
    '''
    krl=kapacitor_rest_lib.KapacitorRestLib(request.cls.mylog)

    request.cls.mylog.info('FIXTURE delete_kapacitors_tasks IS CALLED')
    request.cls.mylog.info('FIXTURE delete_kapacitors_tasks - '
                           'Get all of the tasks names')
    tasks_names=krl.get_tasks_data(kapacitor).keys()
    request.cls.mylog.info('FIXTURE delete_kapacitors_tasks - '
                           'task  names : ' + str(tasks_names))
    for name in tasks_names:
        request.cls.mylog.info('FIXTURE delete_kapacitors_tasks - '
                               'Deleting task ' + str(name))
        krl.delete_task(kapacitor, name)
    request.cls.mylog.info('FIXTURE delete_kapacitor_tasks IS DONE')
