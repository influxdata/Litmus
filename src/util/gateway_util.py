import ast
import json
import sys
import traceback
import csv
import subprocess

from src.util import litmus_utils
from StringIO import StringIO


TASKS_URL = '/api/v2/tasks'
USERS_URL = '/api/v2/users'
AUTHORIZATION_URL = '/api/v2/authorizations'
FLUX_QUERY = '/api/v2/query'
GATEWAY_QUERY = '/api/v2/query'
QUERYD = '/api/v2/querysvc'


# =================================================== TASKS ============================================================

def create_task(test_class_instance, url, org_id, task_name, flux, status='enabled', owners=None, last=None):
    """
    Wrapper function to create a new task, i.e. Flux script that runs in background
    :param test_class_instance: instance of the test calss,i.e. self
    :param url: (string) Gateway URL, e.g. http://localhost:9999
    :param org_id: ID of the organization that owns this task
    :param task_name: name of the task
    :param flux: The Flux script to run for the task
    :param status: current status of the task (enabled/disabled), default is enabled
    :param owners: ???
    :param last: ???
    :return: returns status_code, task_id, org_id, task_name, task_status, task_owners, flux, every, cron, last tuple
    """
    test_class_instance.mylog.info('gateway_util.create_task() function is being called')
    test_class_instance.mylog.info('---------------------------------------------------')
    test_class_instance.mylog.info('')
    test_class_instance.mylog.info('gateway_util.create_task() Creating Task with Organization ID : \'%s\','
                                   ' Task Name : \'%s\', Flux Script: \'%s\', Status : \'%s\', owners : \'%s\' '
                                   'and Last : \'%s\'') % (org_id, task_name, flux, status, owners, last)
    data = '{"organization":"%s", "name":"%s", "flux":"%s", "status":"%s", "owners":"%s", "last":"%s"}' % org_id, \
           task_name, flux, status, owners, last
    task_id, org_id, task_name, task_status, task_owners, flux, every, cron, last = None, None, None, None, None, \
                                                                                    None, None, None, None
    response = test_class_instance.rl.post(base_url=url, path=TASKS_URL, data=data)
    try:
        task_id = response.json().get('id')
        org_id = response.json().get('organization')
        task_name = response.json().get('name')
        task_status = response.json().get('status')
        task_owners = response.json().get('owners')
        flux = response.json().get('flux')
        every = response.json().get('every')
        cron = response.json().get('cron')
        last = response.json().get('last')
        # based on current swagger doc the required keys in response schema are: organization, name and flux
        # may change!!!!
        if task_id and org_id and task_name and task_status and flux:
            test_class_instance.mylog.info('gateway_util.create_task() : TASK_ID=' + str(task_id))
            test_class_instance.mylog.info('gateway_util.create_task() : ORG_ID=' + str(org_id))
            test_class_instance.mylog.info('gateway_util.create_task() : TASK_NAME=' + str(task_name))
            test_class_instance.mylog.info('gateway_util.create_task() : TASK_STATUS=' + str(task_status))
            test_class_instance.mylog.info('gateway_util.create_task() : TASK_OWNER=' + str(task_owners))
            test_class_instance.mylog.info('gateway_util.create_task() : FLUX_SCRIPT=' + str(flux))
            test_class_instance.mylog.info('gateway_util.create_task() : EVERY=' + str(every))
            test_class_instance.mylog.info('gateway_util.create_task() : CRON=' + str(cron))
            test_class_instance.mylog.info('gateway_util.create_task() : LAST=' + str(last))
        else:
            test_class_instance.mylog.info('gateway_util.create_task() : One of the requested params are None: '
                                           'TASK_ID=\'%s\', ORG_ID=\'%s\', TASK_NAME=\'%s\', FLUX=\'%s\'')
            error_message = response.json()['message']
            test_class_instance.mylog.info('gateway_util.create_task() ERROR=' + error_message)
    except:
        test_class_instance.mylog.info('gateway_util.create_task() Exception:')
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(traceback.extract_tb(clt_error_traceback)))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
    test_class_instance.mylog.info('gateway_util.create_task() function is done')
    test_class_instance.mylog.info('')
    return response.status_code, task_id, org_id, task_name, task_status, task_owners, flux, every, cron, last


# ================================================== USERS =============================================================

def create_user(test_class_instance, url, user_name):
    """
    :param test_class_instance:
    :param url:
    :param user_name:
    :return:
    """
    test_class_instance.mylog.info('gateway_util.create_user() function is being called')
    test_class_instance.mylog.info('---------------------------------------------------')
    test_class_instance.mylog.info('')
    test_class_instance.mylog.info('gateway_util.create_user() :'
                                   'Creating User with \'%s\' name' % user_name)
    data = '{"name":"%s"}' % user_name
    user_id, created_user_name, error_message = None, None, None
    response = test_class_instance.rl.post(base_url=url, path=USERS_URL, data=data)
    try:
        user_id = response.json().get('id')
        created_user_name = response.json().get('name')
        if user_id is not None and created_user_name is not None:
            test_class_instance.mylog.info('gateway_util.create_user() USER_ID=' + str(user_id))
            test_class_instance.mylog.info('gateway_util.create_user() USER_NAME=' + str(created_user_name))
        else:
            test_class_instance.mylog.info('gateway_util.create_user() '
                                           'REQUESTED_USER_ID AND REQUESTED_USER_NAME ARE NONE')
            error_message = response.json()['message']
            test_class_instance.mylog.info('gateway_util.create_user() ERROR=' + error_message)
    except:
        test_class_instance.mylog.info('gateway_util.create_user() Exception:')
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(traceback.extract_tb(clt_error_traceback)))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
    test_class_instance.mylog.info('gateway_util.create_organization() function is done')
    test_class_instance.mylog.info('')
    return response.status_code, user_id, created_user_name, error_message


def update_user(test_class_instance, url, user_id, new_user_name):
    """
    :param test_class_instance:
    :param url:
    :param user_id:
    :param new_user_name:
    :return:
    """
    test_class_instance.mylog.info('gateway_util.update_user() function is being called')
    test_class_instance.mylog.info('----------------------------------------------------')
    test_class_instance.mylog.info('')
    data = '{"name":"%s"}' % new_user_name
    updated_user_name, new_user_id, error_message = None, None, None
    response = test_class_instance.rl.patch(base_url=url, path=USERS_URL + '/' + str(user_id), data=data)
    try:
        new_user_id = response.json().get('id')
        updated_user_name = response.json().get('name')
        if new_user_id is not None and updated_user_name is not None:
            test_class_instance.mylog.info('gateway_util.update_user() USER_ID=' + str(new_user_id))
            test_class_instance.mylog.info('gateway_util.update_user() USER_NAME=' + str(updated_user_name))
        else:
            test_class_instance.mylog.info('gateway_util.update_user() '
                                           'REQUESTED_USER_ID AND REQUESTED_USER_NAME ARE NONE')
            test_class_instance.mylog.info('gateway_util.update_user() ERROR=' + response.json()['message'])
    except:
        test_class_instance.mylog.info('gateway_util.update_user() Exception:')
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(traceback.extract_tb(clt_error_traceback)))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
    test_class_instance.mylog.info('gateway_util.update_user() function is done')
    test_class_instance.mylog.info('')
    return response.status_code, new_user_id, updated_user_name, error_message


# THIS IS NOT WORKING YET FROM API STAND POINT. INFLUX TOOL WORKS
def get_user_by_name(test_class_instance, url, user_name):
    """
    :param test_class_instance:
    :param url:
    :param user_name:
    :return: status_code, requested_user_id, requested_user_name
    """
    test_class_instance.mylog.info('gateway_util.get_user_by_name() function is being called')
    test_class_instance.mylog.info('-----------------------------------------------------------')
    test_class_instance.mylog.info('')
    test_class_instance.mylog.info('gateway_util.get_user_by_name() '
                                   'Getting User with \'%s\' name' % user_name)
    requested_user_id, requested_user_name, error_message = None, None, None
    response = test_class_instance.rl.get(base_url=url, path=USERS_URL + '/' + str(user_name))
    try:
        requested_user_id = response.json().get('id')
        requested_user_name = response.json().get('name')
        if requested_user_id is not None and requested_user_name is not None:
            test_class_instance.mylog.info('gateway_util.cget_user_by_name() REQUESTED_USER_ID=' +
                                           str(requested_user_id))
            test_class_instance.mylog.info('gateway_util.get_user_by_name() REQUESTED_USER_NAME=' +
                                           str(requested_user_name))
        else:
            test_class_instance.mylog.info('gateway_util.get_user_by_name() '
                                           'REQUESTED_USER_ID AND REQUESTED_USER_NAME ARE NONE')
            error_message = response.json()['message']
            test_class_instance.mylog.info('gateway_util.get_user_by_name() ERROR=' + error_message)
    except:
        test_class_instance.mylog.info('gateway_util.get_user_by_name() Exception:')
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(traceback.extract_tb(clt_error_traceback)))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
    test_class_instance.mylog.info('gateway_util.get_user_by_name() function is done')
    test_class_instance.mylog.info('')
    return response.status_code, requested_user_id, requested_user_name, error_message


def get_user_by_id(test_class_instance, url, user_id):
    """
    :param test_class_instance:
    :param url:
    :param user_id:
    :return: status_code, requested_user_id, requested_user_name
    """
    test_class_instance.mylog.info('gateway_util.get_user_by_id() function is being called')
    test_class_instance.mylog.info('------------------------------------------------------')
    test_class_instance.mylog.info('')
    test_class_instance.mylog.info('gateway_util.get_user_by_id() '
                                   'Getting User with \'%s\' id' % user_id)
    requested_user_id, requested_user_name, error_message = None, None, None
    response = test_class_instance.rl.get(base_url=url, path=USERS_URL + '/' + str(user_id))
    try:
        requested_user_id = response.json().get('id')
        requested_user_name = response.json().get('name')
        if requested_user_id is not None and requested_user_name is not None:
            test_class_instance.mylog.info('gateway_util.cget_user_by_id() REQUESTED_USER_ID=' +
                                           str(requested_user_id))
            test_class_instance.mylog.info('gateway_util.get_user_by_id() REQUESTED_USER_NAME=' +
                                           str(requested_user_name))
        else:
            test_class_instance.mylog.info('gateway_util.get_user_by_id() '
                                           'REQUESTED_USER_ID AND REQUESTED_USER_NAME ARE NONE')
            error_message = response.json()['message']
            test_class_instance.mylog.info('gateway_util.get_user_by_id() ERROR=' + error_message)
    except:
        test_class_instance.mylog.info('gateway_util.get_user_by_id() Exception:')
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(traceback.extract_tb(clt_error_traceback)))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
    test_class_instance.mylog.info('gateway_util.get_user_by_id() function is done')
    test_class_instance.mylog.info('')
    return response.status_code, requested_user_id, requested_user_name, error_message


def get_all_users(test_class_instance, url):
    """
    Gets all of the created users.
    :param test_class_instance: instance of the test class
    :param url: gateway url
    :return: status code and list of all of the users's dictionaries:
             {u'id': u'025e2102a017d000', u'name': u'test-user'}
    """
    test_class_instance.mylog.info('gateway_util.get_all_users() function is being called')
    test_class_instance.mylog.info('-----------------------------------------------------')
    test_class_instance.mylog.info('')
    list_of_users = []
    response = test_class_instance.rl.get(base_url=url, path=USERS_URL)
    try:
        # {u'users': [], u'links': {u'self': u'/api/v2/users'}}
        list_of_users = response.json()['users']
        if type(list_of_users) == list:
            test_class_instance.mylog.info('gateway_util.get_all_users() LIST OF USERS=' +
                                           str(list_of_users))
        else:
            test_class_instance.mylog.info('gateway_util.get_all_users() ERROR=' + response.json()['message'])
    except:
        test_class_instance.mylog.info('gateway_util.get_all_users() Exception:')
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(traceback.extract_tb(clt_error_traceback)))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
    test_class_instance.mylog.info('gateway_util.get_all_buckets() function is done')
    test_class_instance.mylog.info('')
    return response.status_code, list_of_users


def get_count_of_users(test_class_instance, list_of_users):
    """
    :param test_class_instance:
    :param list_of_users:
    :return: count of users
    """
    test_class_instance.mylog.info('gateway_util.get_count_of_users() function is being called')
    test_class_instance.mylog.info('----------------------------------------------------------')
    test_class_instance.mylog.info('')
    count = len(list_of_users)
    test_class_instance.mylog.info('gateway_util.get_count_of_users() : COUNT=' + str(count))
    return count


def find_user_by_name(test_class_instance, user_name, list_of_users):
    """
    :param list_of_users:
    :param test_class_instance:
    :param user_name:
    :return: true/false
    """
    success = False
    test_class_instance.mylog.info('gateway_util.find_user_by_name() function is being called')
    test_class_instance.mylog.info('---------------------------------------------------------')
    test_class_instance.mylog.info('')
    for user_info in list_of_users:
        test_class_instance.mylog.info('gateway_util.find_user_by_name() Finding User with \'%s\' name' % user_name)
        if user_info['name'] == user_name:
            success = True
            break
    return success


# ================================================== PERMISSIONS =======================================================

def create_authorization(test_class_instance, url, user, userid, list_of_permission):
    """

    :param test_class_instance:
    :param url:
    :param user:
    :param userid:
    :param list_of_permission:
    :return:
    """
    id, user_name, user_id, token, permissions, error_message = None, None, None, None, None, None
    test_class_instance.mylog.info('gateway_util.create_authorization() function is being called')
    test_class_instance.mylog.info('------------------------------------------------------------\n')
    test_class_instance.mylog.info('gateway_util.create_authorization() :'
                                   'Creating Authorization For User \'%s\' With userID \'%s\' and permissions \'%s\''
                                   % (user, userid, str(list_of_permission)))
    # permissions":[{"action":"create","resource":"user"},{"action":"write","resource":"bucket/022a99c38eede000"},
    # {"action":"read","resource":"bucket/022a99c38eede000"}]
    data = '{"user":"%s", "userID":"%s", "permissions": %s}' % (user, userid, list_of_permission)
    response = test_class_instance.rl.post(base_url=url, path=AUTHORIZATION_URL, data=data)
    r = response.json()
    try:
        id = r.get('id')
        user_name = r.get('user')
        user_id = r.get('userID')
        token = r.get('token')
        permissions = r.get('permissions')
        if id is not None and user_name is not None and user_id is not None and token is not None \
                and permissions is not None:
            test_class_instance.mylog.info('gateway_util.create_authorization() USER_ID=' + str(user_id))
            test_class_instance.mylog.info('gateway_util.create_authorization() USER_NAME=' + str(user_name))
            test_class_instance.mylog.info('gateway_util.create_authorization() ID=' + str(id))
            test_class_instance.mylog.info('gateway_util.create_authorization() TOKEN=' + str(token))
            test_class_instance.mylog.info('gateway_util.create_authorization() PERMISSIONS=' + str(permissions))
        else:
            test_class_instance.mylog.info('gateway_util.create_authorization() '
                                           'REQUESTED PARAMS ARE NONE')
            error_message = response.headers['X-Influxs-Error']
            test_class_instance.mylog.info('gateway_util.create_authorization() ERROR=' + error_message)
    except:
        test_class_instance.mylog.info('gateway_util.create_user() Exception:')
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        error_message = response.headers['X-Influxs-Error']
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(traceback.extract_tb(clt_error_traceback)))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
    test_class_instance.mylog.info('gateway_util.create_organization() function is done')
    test_class_instance.mylog.info('')
    return {'status': response.status_code, 'auth_id': id, 'user_name': user_name, 'user_id': user_id, 'token': token,
            'permissions': permissions, 'error': error_message}


# ============================================== WRITE/QUERY DATA POINTS ===============================================

def write_points(test_class_instance, url, token, organization, bucket, data):
    """
    Write point(s) to a bucket in organization given the correct credentials,=.
    :param test_class_instance:
    :param url: gateway url, e.g. http://localhost:9999
    :param token: Token for a given user, with a read/write permissions for a given user
    :param organization: organization the bucket belongs to
    :param bucket: bucket to write data point(s) to
    :param data:
    :return: dictionary of STATUS_CODE and ERROR_MESSAGE, if status code is 204, then error_message is an empty string,
            if status_code does not equal to 204, then error_message should not be an empty string
    """
    error_message = ''
    write_url = '/api/v2/organizations/%s/buckets/%s/write' % (organization, bucket)
    test_class_instance.mylog.info('gateway_util.write_points() function is being called')
    test_class_instance.mylog.info('-----------------------------------------------------\n')
    test_class_instance.mylog.info('gateway_util.write_points() :'
                                   'Writing Points for \'%s\' org, \'%s\' bucket with \'%s\' token'
                                   % (organization, bucket, token))
    # data could be : 'cpu,t=1 f=1'
    headers = {"Authorization": "Token %s" % token}
    response = test_class_instance.rl.post(base_url=url, path=write_url, data=data, headers=headers)
    # in case if there is an error, then get the error_message
    if response.status_code != 204:
        error_message = response.headers['X-Influx-Error']
    test_class_instance.mylog.info('gateway_util.write_points() function is done\n')
    return {"status": response.status_code, "error": error_message}


def gateway_query_data(test_class_instance, query, url, token, organization):
    """

    :param test_class_instance:
    :param query: Flux query
    :param url: (str) gateway url
    :param token:
    :param organization:
    :return:
    """
    error = ''
    result_list = []
    test_class_instance.mylog.info('gateway_util.gateway_query_data() function is being called')
    test_class_instance.mylog.info('--------------------------------------------------\n')
    test_class_instance.mylog.info('gateway_util.gateway_query_data() : Query : \'%s\'' % query)
    test_class_instance.mylog.info('gateway_util.gateway_query_data() : Token : \'%s\'' % token)
    test_class_instance.mylog.info('gateway_util.gateway_query_data() : Org : \'%s\'' % organization)

    params = {"organization": "%s" % organization}
    data = '{"query":%s}' % json.dumps(query)
    headers = {"Authorization": "Token %s" % token}

    response = test_class_instance.rl.post(base_url=url, path=GATEWAY_QUERY, params=params, data=data, headers=headers)
    # successful status is 200
    if response.status_code > 200:
        error = response.headers['X-Influx-Error']
    else:
        test_class_instance.mylog.info('gateway_util.gateway_query_data() : content : ' + str(response.content))
        result = '\r\n'.join(response.content.split('\r\n')[:-2])
        test_class_instance.mylog.info('gateway_util.gateway_query_data() : result : ' + str(result))
        # read the query results into buffer
        buffer = StringIO(result)
        reader = csv.DictReader(buffer)
        # iterate over reader object
        for line in reader:
            result_list.append(line)
    test_class_instance.mylog.info('gateway_util.gateway_query_data() : result : ' + str(result_list))
    return {'status': response.status_code, 'error': error, 'result': result_list}


def queryd_query_data(test_class_instance, query, url, organization_id, timeout=None, responsenone=None):
    """

    :param test_class_instance:
    :param query: Flux query
    :param url: queryd url
    :param organization_id:
    :param timeout
    :param responsenone
    :return:
    """
    result_list = []
    error = ''
    status_code = None
    test_class_instance.mylog.info('gateway_util.queryd_query_data() function is being called')
    test_class_instance.mylog.info('--------------------------------------------------\n')
    test_class_instance.mylog.info('gateway_util.queryd_query_data() : Query : \'%s\'' % query)
    test_class_instance.mylog.info('gateway_util.queryd_query_data() : Org_ID : \'%s\'' % organization_id)

    data = '{"organization_id":"%s","compiler":{"query":%s}, "compiler_type":"flux"}' \
           % (organization_id, json.dumps(query))

    response = test_class_instance.rl.post(base_url=url, path=QUERYD, data=data, timeout=timeout,
                                           responsenone=responsenone)
    if not responsenone:
        if response is None:
            status_code = 500
        else:
            if response.status_code > 200:
                error = response.headers['X-Influx-Error']
                status_code = response.status_code
            else:
                status_code = response.status_code
            # the first three lines are not needed (at least for now), they are:
            # datatype,string,long,dateTime:RFC3339,dateTime:RFC3339,dateTime:RFC3339,double,string,string,string
            # group,false,false,true,true,false,false,true,true,true
            # default,_result,,,,,,,,
            """
            What we are interested in is result:
            ,result,table,_start,_stop,_time,_value,_field,_measurement,t
            ,,0,2016-11-09T20:09:47.52299776Z,2018-10-10T20:09:47.52299776Z,2018-10-10T20:09:36.072403525Z,1234,f,test_m,0000
            """
            result = '\r\n'.join(response.content.split('\r\n')[3:])
            # read the query results into buffer
            buffer = StringIO(result)
            reader = csv.DictReader(buffer)
            # iterate over reader object
            for line in reader:
                result_list.append(line)
            test_class_instance.mylog.info('gateway_util.queryd_query_data() : result : ' + str(result_list))
    return {'status': status_code, 'result': result_list, 'error': error}


def kafka_find_data_by_tag(test_class_instance, kube_config, kube_cluster, namespace, tag_value, *args):
    """

    :param test_class_instance: (obj), instance of the test class
    :param kube_config: (str), location of kubernetes config file
    :param kube_cluster: (str), either influx-internal or local
    :param namespace: (str), namespace where test cluster is deployed
    :param tag_value: (str), the tag value that should be stored on one one of the kafka containers
    :param *args, (tuple), kafka pods, e.g."kafka-0","kafka-1" or just one "kafka-0"
    :return:
    """
    err = ''
    topics, data = [], []

    test_class_instance.mylog.info('gateway_util.kafka_find_data_by_tag() function is being called')
    test_class_instance.mylog.info('--------------------------------------------------------------\n')
    test_class_instance.mylog.info('Params: kube_config=%s\nkube_cluster=%s\n'
                                   'namespace=%s\ntag_value=%s\nkafka_pod=%s\n'
                                   % (kube_config, kube_cluster, namespace, tag_value, args))
    for kafka_pod in args:
        cmd = 'kubectl --kubeconfig=%s --context=%s exec %s -c k8skafka -n %s -- bash -c ' \
              '"cd /var/lib/kafka/data/topics;grep -r -a --include=\*.log \"%s\""' \
              % (kube_config, kube_cluster, kafka_pod, namespace, tag_value)
        test_class_instance.mylog.info('Executing Command : %s' % cmd)
        k_result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if k_result.wait() != 0:
            # kubectl failed for some reason, find out
            err = k_result.communicate()[1]
            test_class_instance.mylog.info('Execution of command failed with \'%s\' error, for \'%s\''
                                           % (err, kafka_pod))
            test_class_instance.mylog.info('gateway_util.kafka_find_data_by_tag() function is done\n')
            return topics, data, err
        # get the result
        out = k_result.communicate()[0]
        # there could be potentially more than 1 data point with a tag value we are looking for
        # we are getting a list of strings
        out = out.split('\n')
        # out entry could be:
        # ingress-52/00000000000000000000.log:helloworld(\xde\xe5\xd1\xab\xd3\x05\xb9\x0c\x01fA\x00\t\x01\x10@(\xc3\xfc\xd3
        # \r\x16F\x91\x02\x1860ffed7Ve\x01\x1d\x1d\x92\xcf\x00\x00\x00
        for entry in out:
            if entry != '':
                # get the topic name
                topics.append(entry.split('/')[0])
                # get the data string
                data.append(entry.split(':')[1])
    test_class_instance.mylog.info('TOPICS : ' + str(topics))
    test_class_instance.mylog.info('DATA : ' + str(data))
    test_class_instance.mylog.info('gateway_util.kafka_find_data_by_tag() function is done\n')
    return topics, data, err


def storage_find_data(test_class_instance, kube_config, kube_cluster, namespace, search_value, *args):
    """
    storage_find_data() function looking for a data on all of the storage nodes
    :param test_class_instance: (obj), instance of the test class
    :param kube_config: (str), location of kubernetes config file
    :param kube_cluster: (str), either influx-internal or local
    :param namespace: (str), namespace where test cluster is deployed
    :param search_value: (str), the value that should be stored on one one of the storage containers
    :param *args : (tuple), storage pods, e.g."storage-0","storage-1" or just one "storage-0"
    :return: (tuple), list of absolute path to the file name or empty, list of data stored or empty,
                        error string or empty
    """
    err = ''
    engine, data = [], []

    test_class_instance.mylog.info('gateway_util.storage_find_data() function is being called')
    test_class_instance.mylog.info('---------------------------------------------------------\n')
    test_class_instance.mylog.info('Params: kube_config=%s\nkube_cluster=%s\nnamespace=%s\nsearch_value=%s\nargs=%s\n'
                                   % (kube_config, kube_cluster, namespace, search_value, args))
    # if we have more than one storage pod, e.g. storage-0, storage-1, then we need to iterate over stirage containers
    # in each pod
    for storage_pod in args:
        cmd = 'kubectl --kubeconfig=%s --context=%s exec %s -c storage -n %s -- bash -c ' \
              '"cd /data;find . -name \"*.tsm\" -print | xargs grep -a \"%s\""' \
              % (kube_config, kube_cluster, storage_pod, namespace, search_value)
        test_class_instance.mylog.info('Executing Command : %s' % cmd)
        k_result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if k_result.wait() != 0:
            # kubectl failed for some reason, find out
            err = k_result.communicate()[1]
            test_class_instance.mylog.info('Execution of command failed with \'%s\' error for \%s\''
                                           % (err, storage_pod))
            test_class_instance.mylog.info('gateway_util.storage_find_data() function is done\n')
            return engine, data, err
        # get the result
        out = k_result.communicate()[0]
        # there could be potentially more than 1 data point with a tag value we are looking for
        # we are getting a list of strings
        out = out.split('\n')
        # out entry could be:
        # # the output of the command could be :
        # ./17/engine/data/000000000-000000001.tsm:,_f=f,_m=test_m,t=hello\ world#!~#f
        for entry in out:
            test_class_instance.mylog.info('gateway_util.storage_find_data() Entry = ' + str(entry))
            if entry != '':
                entry = entry.split(':')
                if len(entry) > 1:
                    # get the engine name
                    engine.append(entry[0])
                    # get the data string
                    data.append(entry[1])
                elif len(entry) == 1:
                    data.append(entry[0])
    test_class_instance.mylog.info('ENGINE : ' + str(engine))
    test_class_instance.mylog.info('DATA : ' + str(data))
    test_class_instance.mylog.info('gateway_util.storage_find_data() function is done\n')
    return engine, data, err


# ========================================================== ETCD ======================================================

def get_org_etcd(test_class_instance, etcd, org_id, get_index_values=False):
    """
    Function gets org ids and org name (hashed name) from etcd store and reports any errors.
    :param etcd:
    :param org_id:
    :param test_class_instance: instance of the test class, i.e. self
    :param get_index_values (bool), if set to True then get the org id and org name values from etcd index,
                                    default value is False
    :return: actual_org_id =>
             actual_org_name =>
             error =>
             name_by_index_id =>
             error_by_index_id =>
             id_by_index_name =>
             error_by_index_name =>
    """
    actual_org_id, actual_org_name, error, name_by_index_id, error_by_index_id, id_by_index_name, error_by_index_name = \
        '', '', '', '', '', '', ''
    test_class_instance.mylog.info('gateway_util.get_org_etcd() function is being called')
    test_class_instance.mylog.info('----------------------------------------------------')
    test_class_instance.mylog.info('')
    cmd = 'ETCDCTL_API=3 /usr/local/bin/etcdctl --endpoints %s get --prefix "Organizationv1/%s" --print-value-only' \
          % (etcd, org_id)
    out, error = litmus_utils.execCmd(test_class_instance, cmd, status='OUT_STATUS')
    # if we want to get values from indexv1/org/id and indexv1/org/name from etcd store
    if get_index_values:
        test_class_instance.mylog.info('gateway_util.get_org_etcd() : Getting hashed name by index by id prefix')
        cmd_index_by_id = 'ETCDCTL_API=3 /usr/local/bin/etcdctl --endpoints %s get --prefix "indexv1/org/id/%s" ' \
                          '--print-value-only' % (etcd, org_id)
        name_by_index_id, error_by_index_id = \
            litmus_utils.execCmd(test_class_instance, cmd_index_by_id, status='OUT_STATUS')
        # get first 64 characters
        name_by_index_id = name_by_index_id[:64]
        test_class_instance.mylog.info('gateway_util.get_org_etcd() : Getting index by index by name prefix')
        cmd_index_by_name = 'ETCDCTL_API=3 /usr/local/bin/etcdctl --endpoints %s get --prefix "indexv1/org/name/%s" ' \
                            '--print-value-only' % (etcd, name_by_index_id)
        id_by_index_name, error_by_index_name = \
            litmus_utils.execCmd(test_class_instance, cmd_index_by_name, status='OUT_STATUS')
        name_by_index_id = name_by_index_id.strip()
        id_by_index_name = id_by_index_name.strip()
    # If organization id and name exist (assuming no error)
    if out != '':
        actual_org_id = ast.literal_eval(out).get('id')
        test_class_instance.mylog.info('gateway_util.get_org_etcd() : actual_org_id = \'%s\'' % actual_org_id)
        actual_org_name = ast.literal_eval(out).get('name')
        # need to handle double quotes for now separately
        if actual_org_name != 'DoubleQuotes\"' and actual_org_name != 'DoubleQuotes\"_updated_name':
            actual_org_name = json.loads("\"" + actual_org_name + "\"")
        test_class_instance.mylog.info('gateway_util.get_org_etcd() : actual_org_name = \'%s\'' % actual_org_name)
    return actual_org_id, actual_org_name, error, name_by_index_id, error_by_index_id, id_by_index_name, \
           error_by_index_name


def get_user_etcd(test_class_instance, etcd, user_id):
    """
    Function gets user_id and user_name from etcd store.
    :param user_id:
    :param test_class_instance: instance of the test class, i.e. self
    :param etcd: url of the etcd service
    :return: actual_user_id =>
             actual_user_name =>
             error =>
    """
    actual_user_id, actual_user_name, error = '', '', ''
    test_class_instance.mylog.info('gateway_util.get_user_etcd() function is being called')
    test_class_instance.mylog.info('--------------------------------------------------------')
    test_class_instance.mylog.info('gateway_util.get_user_etcd(): params: user_id \'%s\'' % user_id)
    test_class_instance.mylog.info('')
    cmd = 'ETCDCTL_API=3 /usr/local/bin/etcdctl --endpoints %s get --prefix "userv1/%s" --print-value-only' \
          % (etcd, user_id)
    out, error = litmus_utils.execCmd(test_class_instance, cmd, status='OUT_STATUS')
    if out != '':
        actual_user_id = ast.literal_eval(out).get('id')
        test_class_instance.mylog.info('gateway_util.get_user_etcd() : actual_user_id = \'%s\'' % actual_user_id)
        actual_user_name = ast.literal_eval(out).get('name')
        if actual_user_name != 'DoubleQuotes\"' and actual_user_name != 'DoubleQuotes\"_updated_name':
            actual_user_name = json.loads("\"" + actual_user_name + "\"")
        test_class_instance.mylog.info('gateway_util.get_user_etcd() : actual_user_name = \'%s\'' % actual_user_name)
    return actual_user_id, actual_user_name, error


def get_bucket_etcd(test_class_instance, etcd, bucket_id):
    """
    Function gets
    :param test_class_instance: instance of the test class, i.e. self
    :param etcd: url of the etcd service
    :param bucket_id: id of the bucket
    :return: actual_bucket_id =>
             actual_bucket_name =>
             error =>
    """
    actual_bucket_id, actual_bucket_name, actual_rp, error = '', '', '', ''
    test_class_instance.mylog.info('gateway_util.get_bucket_etcd() function is being called')
    test_class_instance.mylog.info('-------------------------------------------------------')
    test_class_instance.mylog.info('gateway_util.get_bucket_etcd(): params: bucket_id \'%s\'' % bucket_id)
    test_class_instance.mylog.info('')
    cmd = 'ETCDCTL_API=3 /usr/local/bin/etcdctl --endpoints %s get --prefix "bucketv1/%s" --print-value-only' \
          % (etcd, bucket_id)
    out, error = litmus_utils.execCmd(test_class_instance, cmd, status='OUT_STATUS')
    if out != '':
        actual_rp = ast.literal_eval(out).get('retentionPeriod')
        test_class_instance.mylog.info('gateway_util.get_bucket_etcd() : actual_retention_period = \'%s\'' % actual_rp)
        actual_bucket_id = ast.literal_eval(out).get('id')
        test_class_instance.mylog.info('gateway_util.get_bucket_etcd() : actual_bucket_id = \'%s\'' % actual_bucket_id)
        actual_bucket_name = ast.literal_eval(out).get('name')
        if actual_bucket_name != 'DoubleQuotes\"' and actual_bucket_name != 'DoubleQuotes\"_updated_name' \
                and actual_bucket_name != 'DoubleQuotes\"_updated':
            actual_bucket_name = json.loads("\"" + actual_bucket_name + "\"")
        test_class_instance.mylog.info(
            'gateway_util.get_bucket_etcd() : actual_bucket_name = \'%s\'' % actual_bucket_name)
    return actual_bucket_id, actual_bucket_name, actual_rp, error
