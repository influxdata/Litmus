import ast
import json
import sys
import traceback
import csv

from src.util import litmus_utils
from StringIO import StringIO

BUCKETS_URL = '/api/v2/buckets'
TASKS_URL = '/api/v2/tasks'
ORG_URL = '/api/v2/orgs'
USERS_URL = '/api/v2/users'
AUTHORIZATION_URL = '/api/v2/authorizations'
FLUX_QUERY = '/api/v2/query'
GATEWAY_QUERY = '/api/v2/query'
QUERYD = '/api/v2/querysvc'


# =================================================== TASKS =============================================================

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


# =================================================== ORGANIZATIONS =====================================================

def create_organization(test_class_instance, url, org_name):
    """
    create_organization() function creates an organization
    :param test_class_instance: instance of the test class
    :param url: gateway url,for example: http://localhost:9999
    :param org_name: name of the organization to create
    :return: status_code, org_id, created_org_name, error_message
    """
    test_class_instance.mylog.info('gateway_util.create_organization() function is being called')
    test_class_instance.mylog.info('-----------------------------------------------------------')
    test_class_instance.mylog.info('')
    test_class_instance.mylog.info('gateway_util.create_organization() '
                                   'Creating Organization with \'%s\' name' % org_name)
    data = '{"name":"%s"}' % org_name
    org_id, created_org_name, error_message = None, None, None
    response = test_class_instance.rl.post(base_url=url, path=ORG_URL, data=data)
    try:
        org_id = response.json().get('id')
        created_org_name = response.json().get('name')
        if org_id is not None and created_org_name is not None:
            test_class_instance.mylog.info('gateway_util.create_organization() ORG_ID=' + str(org_id))
            test_class_instance.mylog.info('gateway_util.create_organization() ORG_NAME=' + str(created_org_name))
        else:
            test_class_instance.mylog.info('gateway_util.create_organization() '
                                           'REQUESTED_ORG_ID AND REQUESTED_ORG_NAME ARE NONE')
            error_message = response.headers['X-Influx-Error']
            test_class_instance.mylog.info('gateway_util.create_organization() ERROR=' + error_message)
    except:
        test_class_instance.mylog.info('gateway_util.create_organization() Exception:')
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(traceback.extract_tb(clt_error_traceback)))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
        error_message = response.headers['X-Influx-Error']
        test_class_instance.mylog.info('gateway_util.create_organization() ERROR=' + error_message)
    test_class_instance.mylog.info('gateway_util.create_organization() function is done')
    test_class_instance.mylog.info('')
    return response.status_code, org_id, created_org_name, error_message


def update_organization(test_class_instance, url, org_id, new_org_name):
    """
    :param test_class_instance:
    :param url:
    :param org_id:
    :param new_org_name:
    :return:
    """
    test_class_instance.mylog.info('gateway_util.update_organization() function is being called')
    test_class_instance.mylog.info('-----------------------------------------------------------')
    test_class_instance.mylog.info('')
    data = '{"name":"%s"}' % new_org_name
    updated_org_name, new_org_id, error_message = None, None, None
    response = test_class_instance.rl.patch(base_url=url, path=ORG_URL + '/' + str(org_id), data=data)
    try:
        new_org_id = response.json().get('id')
        updated_org_name = response.json().get('name')
        if org_id is not None and updated_org_name is not None:
            test_class_instance.mylog.info('gateway_util.update_organization() ORG_ID=' + str(new_org_id))
            test_class_instance.mylog.info('gateway_util.update_organization() ORG_NAME=' + str(updated_org_name))
        else:
            test_class_instance.mylog.info('gateway_util.update_organization() '
                                           'REQUESTED_ORG_ID AND REQUESTED_ORG_NAME ARE NONE')
            error_message = response.json()['message']
            test_class_instance.mylog.info('gateway_util.create_organization() ERROR=' + error_message)
    except:
        test_class_instance.mylog.info('gateway_util.update_organization() Exception:')
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(traceback.extract_tb(clt_error_traceback)))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
    test_class_instance.mylog.info('gateway_util.update_organization() function is done')
    test_class_instance.mylog.info('')
    return response.status_code, new_org_id, updated_org_name, error_message


def get_organization_by_id(test_class_instance, url, org_id):
    """
    :param test_class_instance:
    :param url:
    :param org_id:
    :return: status_code, requested_org_id, requested__org_name
    """
    test_class_instance.mylog.info('gateway_util.get_organization_by_id() function is being called')
    test_class_instance.mylog.info('--------------------------------------------------------------')
    test_class_instance.mylog.info('')
    test_class_instance.mylog.info('gateway_util.get_organization_by_id() '
                                   'Getting Organization with \'%s\' id' % org_id)
    requested_org_id, requested_org_name, error_message = None, None, None
    response = test_class_instance.rl.get(base_url=url, path=ORG_URL + '/' + str(org_id))
    try:
        requested_org_id = response.json().get('id')
        requested_org_name = response.json().get('name')
        if requested_org_id is not None and requested_org_name is not None:
            test_class_instance.mylog.info('gateway_util.get_organization_by_id() REQUESTED_ORG_ID=' +
                                           str(requested_org_id))
            test_class_instance.mylog.info('gateway_util.get_organization_by_id() REQUESTED_ORG_NAME=' +
                                           str(requested_org_name))
        else:
            test_class_instance.mylog.info('gateway_util.get_organization_by_id() '
                                           'REQUESTED_ORG_ID AND REQUESTED_ORG_NAME ARE NONE')
            error_message = response.json()['message']
            test_class_instance.mylog.info('gateway_util.get_organization_by_id() ERROR=' + error_message)
    except:
        test_class_instance.mylog.info('gateway_util.get_organization_by_id() Exception:')
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(traceback.extract_tb(clt_error_traceback)))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
    test_class_instance.mylog.info('gateway_util.get_organization_by_id() function is done')
    test_class_instance.mylog.info('')
    return response.status_code, requested_org_id, requested_org_name, error_message


def get_all_organizations(test_class_instance, url):
    """
    Gets all of the created organizations.
    :param test_class_instance:
    :param url:
    :return: status_code, list of organization's dictionaries:
            {u'id': u'02a51e4f52a22000',
             u'links': {
                u'users': u'/api/v2/orgs/02a51e4f52a22000/users',
                u'buckets': u'/api/v2/buckets?org=gxfrp',
                u'tasks': u'/api/v2/tasks?org=gxfrp',
                u'dashboards': u'/api/v2/dashboards?org=gxfrp',
                u'self': u'/api/v2/orgs/02a51e4f52a22000'},
             u'name': u'gxfrp'}
    """
    test_class_instance.mylog.info('gateway_util.get_all_organizations() function is being called')
    test_class_instance.mylog.info('-------------------------------------------------------------')
    test_class_instance.mylog.info('')
    list_of_organizations = []
    response = test_class_instance.rl.get(base_url=url, path=ORG_URL)
    try:
        # response.json() returns dictionary:
        # {
        #  u'orgs':
        #   [{u'id': u'02a51e4f52a22000',
        #     u'links': {
        #                   u'users': u'/api/v2/orgs/02a51e4f52a22000/users',
        #                   u'buckets': u'/api/v2/buckets?org=gxfrp',
        #                   u'tasks': u'/api/v2/tasks?org=gxfrp',
        #                   u'dashboards': u'/api/v2/dashboards?org=gxfrp',
        #                   u'self': u'/api/v2/orgs/02a51e4f52a22000'},
        #    u'name': u'gxfrp'}
        #    ],
        # u'links': {u'self': u'/api/v2/orgs'}
        # }
        list_of_organizations = response.json()['orgs']
        if type(list_of_organizations) == list:
            test_class_instance.mylog.info('gateway_util.get_all_organizations() LIST OF ORGANIZATIONS=' +
                                           str(list_of_organizations))
        else:
            test_class_instance.mylog.info('gateway_util.get_all_organizations() ERROR=' + response.json()['message'])
    except:
        test_class_instance.mylog.info('gateway_util.get_all_organizations() Exception:')
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(traceback.extract_tb(clt_error_traceback)))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
    test_class_instance.mylog.info('gateway_util.get_all_organizations() function is done')
    test_class_instance.mylog.info('')
    return response.status_code, list_of_organizations


def delete_organization(test_class_instance, url, org_id):
    """
    delete_organization() function removes an organization from etcd store, from index/org/id, index/org/name and
    removes the key Organizationv1
    :param test_class_instance: instance of the test class
    :param url: gateway url,for example: http://localhost:9999
    :param org_id: id of the organization to delete
    :return: status_code, org_id, created_org_name, error_message
    """
    test_class_instance.mylog.info('gateway_util.delete_organization() function is being called')
    test_class_instance.mylog.info('-----------------------------------------------------------')
    test_class_instance.mylog.info('')
    test_class_instance.mylog.info('gateway_util.delete_organization() '
                                   'Deleting Organization with \'%s\' id' % org_id)
    # TODO This error is coming from headers,
    # TODO I would need to handle it differently when both JSON error and headers errors are in place.
    error = ''
    if org_id == '':  # org id is missing:
        path = ORG_URL + '/'
    else:
        path = ORG_URL + '/' + org_id
    response = test_class_instance.rl.delete(base_url=url, path=path)
    # TODO Currently status for successful deletion is 202, but needs to be 204,
    # TODO 404 will be returned if org id is missing.
    if response.status_code in range(405, 501):
        error = response.headers['X-Influx-Error']
    if error != '':
        test_class_instance.mylog.info('gateway_util.delete_organization() ERROR: ' + error)
    test_class_instance.mylog.info('gateway_util.delete_organization() function is done')
    test_class_instance.mylog.info('')
    return response.status_code, error


def find_org_by_name(test_class_instance, org_name_to_find, list_of_organizations):
    """
    :param list_of_organizations:
    :param test_class_instance:
    :param org_name_to_find:
    :return: org name, id
    """
    test_class_instance.mylog.info('gateway_util.find_org_by_name() function is being called')
    test_class_instance.mylog.info('--------------------------------------------------------')
    test_class_instance.mylog.info('')
    test_class_instance.mylog.info('gateway_util.find_org_by_name() '
                                   'Finding Organization with \'%s\' name' % org_name_to_find)
    result = filter(lambda org: org['name'] == org_name_to_find, list_of_organizations)
    orgname = result[0].get('name')
    test_class_instance.mylog.info('gateway_util.find_org_by_name() : ORG_NAME=' + str(orgname))
    orgid = result[0].get('id')
    test_class_instance.mylog.info('gateway_util.find_org_by_name() : ORG_ID=' + str(orgid))
    return orgname, orgid


def find_org_by_id(test_class_instance, org_id_to_find, list_of_organizations):
    """
    :param list_of_organizations:
    :param test_class_instance:
    :param org_id_to_find:
    :return: org name, id
    """
    test_class_instance.mylog.info('gateway_util.find_org_by_id() function is being called')
    test_class_instance.mylog.info('------------------------------------------------------')
    test_class_instance.mylog.info('')
    test_class_instance.mylog.info('gateway_util.find_org_by_id() '
                                   'Finding Organization with \'%s\' id' % org_id_to_find)
    result = filter(lambda org: org['id'] == org_id_to_find, list_of_organizations)
    orgname = result[0].get('name')
    test_class_instance.mylog.info('gateway_util.find_org_by_name() : ORG_NAME=' + str(orgname))
    orgid = result[0].get('id')
    test_class_instance.mylog.info('gateway_util.find_org_by_name() : ORG_ID=' + str(orgid))
    return orgname, orgid


def get_count_of_orgs(test_class_instance, list_of_organizations):
    """
    :param test_class_instance:
    :param list_of_organizations:
    :return: count of organizations
    """
    test_class_instance.mylog.info('gateway_util.get_count_of_orgs() function is being called')
    test_class_instance.mylog.info('---------------------------------------------------------')
    test_class_instance.mylog.info('')
    count = len(list_of_organizations)
    test_class_instance.mylog.info('gateway_util.get_count_of_orgs() : COUNT=' + str(count))
    return count


# ================================================== USERS ==============================================================

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


# =================================================== BUCKETS ===========================================================

# Currently retention periods are only numbers and not durations:
# https://github.com/influxdata/platform/issues/144
def create_bucket(test_class_instance, url, bucket_name, retentionPeriod=None, organizationID=None):
    """
    Create a bucket for an organization with a certain retention period
    :param url:
    :param bucket_name:
    :param retentionPeriod:
    :param organizationID:
    :param test_class_instance: instance of the test class
    :return:
    """
    # do not use retention period for now, use a hardcoded value:
    test_class_instance.mylog.info('gateway_util.create_bucket() function is being called')
    test_class_instance.mylog.info('-----------------------------------------------------')
    test_class_instance.mylog.info('')
    test_class_instance.mylog.info('gateway_util.create_function() :'
                                   'Creating Bucket with \'%s\' name' % bucket_name)
    # https://github.com/influxdata/platform/issues/143
    # as of 09/26/18 Chris Goller made a change, retentionPeriod is now a string, i.e. "1h" = 1 hour, or 20m = 20 min, etc
    # https://github.com/influxdata/platform/pull/864. Also retentionPeriod is not optional as of this PR
    if retentionPeriod is None:  # test the negative test
        data = '{"name":"%s", "organizationID": "%s"}' % (bucket_name, organizationID)
    elif organizationID is None:
        data = '{"name":"%s", "retentionPeriod": "%s"}' % (bucket_name, retentionPeriod)
    else:
        data = '{"name":"%s", "retentionPeriod": "%s", "organizationID": "%s"}' \
               % (bucket_name, retentionPeriod, organizationID)

    organization_id, created_bucket_id, created_bucket_name, \
    retention_period, error_message = '', '', '', '', ''
    response = test_class_instance.rl.post(base_url=url, path=BUCKETS_URL, data=data)
    try:
        organization_id = response.json().get('organizationID')
        created_bucket_name = response.json().get('name')
        created_bucket_id = response.json().get('id')
        retention_period = response.json().get('retentionPeriod')
        if created_bucket_id is not None and created_bucket_name is not None:
            test_class_instance.mylog.info('gateway_util.create_bucket() BUCKET_ID=' + str(created_bucket_id))
            test_class_instance.mylog.info('gateway_util.create_user() BUCKET_NAME=' + str(created_bucket_name))
        else:
            test_class_instance.mylog.info('gateway_util.create_bucket() '
                                           'REQUESTED_BUCKET_ID AND REQUESTED_BUCKET_NAME ARE NONE')
            error_message = response.json()['message']
            test_class_instance.mylog.info('gateway_util.create_bucket() ERROR=' + error_message)
    except:
        test_class_instance.mylog.info('gateway_util.create_bucket() Exception:')
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(traceback.extract_tb(clt_error_traceback)))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
        error_message = response.headers['X-Influx-Error']
    test_class_instance.mylog.info('gateway_util.create_bucket() function returned : status = \'%s\', '
                                   'bucket_id = \'%s\', bucket_name = \'%s\', org_id = \'%s\', rp = \'%s\', '
                                   'error_message = \'%s\'' % (response.status_code, created_bucket_id,
                                                               created_bucket_name, organization_id, retention_period,
                                                               error_message))
    test_class_instance.mylog.info('gateway_util.create_bucket() function is done')
    test_class_instance.mylog.info('')
    return response.status_code, created_bucket_id, created_bucket_name, \
           organization_id, retention_period, error_message


def update_bucket(test_class_instance, url, bucket_id, new_bucket_name=None, new_retention=None):
    """
    :param test_class_instance:
    :param url: gateway
    :param bucket_id:
    :param new_bucket_name:
    :param new_retention:
    :return:
    """
    test_class_instance.mylog.info('gateway_util.update_bucket() function is being called')
    test_class_instance.mylog.info('-----------------------------------------------------')
    test_class_instance.mylog.info('')
    if new_retention is None and new_bucket_name is None:
        data = '{}'
    elif new_retention is None:
        data = '{"name":"%s"}' % new_bucket_name
    elif new_bucket_name is None:
        data = '{"retentionPeriod":"%d"}' % new_retention
    else:
        data = '{"name":"%s", "retentionPeriod":"%d"}' % (new_bucket_name, new_retention)
    updated_bucket_name, updated_bucket_id, updated_retention, org_id, org_name, error_message = \
        None, None, None, None, None, None
    response = test_class_instance.rl.patch(base_url=url, path=BUCKETS_URL + '/' + str(bucket_id), data=data)
    try:
        updated_bucket_id = response.json().get('id')
        updated_bucket_name = response.json().get('name')
        updated_retention = response.json().get('retentionPeriod')
        org_id = response.json().get('organizationID')
        org_name = response.json().get('organization')
        if updated_bucket_id is not None and updated_bucket_name is not None and updated_retention is not None \
                and org_id is not None and org_name is not None:
            test_class_instance.mylog.info('gateway_util.update_bucket() UPDATED_BUCKET_ID=' + str(updated_bucket_id))
            test_class_instance.mylog.info(
                'gateway_util.update_bucket() UPDATED_BUCKET_NAME=' + str(updated_bucket_name))
            test_class_instance.mylog.info('gateway_util.update_bucket() UPDATED_RETENTION=' + str(updated_retention))
            test_class_instance.mylog.info('gateway_util.update_bucket() ORG_ID=' + str(org_id))
            test_class_instance.mylog.info('gateway_util.update_bucket() ORG_NAME=' + str(org_name))
        else:
            test_class_instance.mylog.info('gateway_util.update_bucket() SOME OF THE VALUES ARE NONE')
            error_message = response.json()['message']
            test_class_instance.mylog.info('gateway_util.create_bucket() ERROR=' + error_message)
    except:
        test_class_instance.mylog.info('gateway_util.update_bucket() Exception:')
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(traceback.extract_tb(clt_error_traceback)))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
    test_class_instance.mylog.info('gateway_util.update_bucket() function is done')
    test_class_instance.mylog.info('')
    return response.status_code, updated_bucket_id, updated_bucket_name, updated_retention, org_id, \
           org_name, error_message


def get_bucket_by_id(test_class_instance, url, bucket_id):
    """
    :param bucket_id:
    :param test_class_instance:
    :param url:
    :return: status_code, requested_org_id, requested__org_name
    """
    test_class_instance.mylog.info('gateway_util.get_bucket_by_id() function is being called')
    test_class_instance.mylog.info('--------------------------------------------------------')
    test_class_instance.mylog.info('')
    test_class_instance.mylog.info('gateway_util.get_bucket_by_id() '
                                   'Getting Bucket with \'%s\' id' % bucket_id)
    requested_bucket_id, requested_bucket_name, error_message = None, None, None
    response = test_class_instance.rl.get(base_url=url, path=BUCKETS_URL + '/' + str(bucket_id))
    try:
        requested_bucket_id = response.json().get('id')
        requested_bucket_name = response.json().get('name')
        if requested_bucket_id is not None and requested_bucket_name is not None:
            test_class_instance.mylog.info('gateway_util.get_bucket_by_id() REQUESTED_BUCKET_ID=' +
                                           str(requested_bucket_id))
            test_class_instance.mylog.info('gateway_util.get_bucket_by_id() REQUESTED_BUCKET_NAME=' +
                                           str(requested_bucket_name))
        else:
            test_class_instance.mylog.info('gateway_util.get_bucket_by_id() '
                                           'REQUESTED_BUCKET_ID AND REQUESTED_BUCKET_NAME ARE NONE')
            error_message = response.json()['message']
            test_class_instance.mylog.info('gateway_util.get_bucket_by_id() ERROR=' + error_message)
    except:
        test_class_instance.mylog.info('gateway_util.get_bucket_by_id() Exception:')
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(traceback.extract_tb(clt_error_traceback)))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
    test_class_instance.mylog.info('gateway_util.get_bucket_by_id() function is done')
    test_class_instance.mylog.info('')
    return response.status_code, requested_bucket_id, requested_bucket_name, error_message


def get_all_buckets(test_class_instance, url, org):
    """
    Gets all of the created buckets for a specific organization.
    :param test_class_instance: instance of the test class
    :param url: gateway url
    :param org: organization name for which to get all of the buckets
    :return: status code, error and list of all of the bucket's dictionaries:
             {u'name': u'bucket_1',
              u'links':
                   {u'org': u'/api/v2/orgs/02a5230b19a22000',
                   u'self': u'/api/v2/buckets/02a5231df7a22000'},
               u'organizationID': u'02a5230b19a22000',
               u'retentionPeriod': "1h",
               u'organization': u'org_1',
               u'id': u'02a5231df7a22000'}
    """
    test_class_instance.mylog.info('gateway_util.get_all_buckets() function is being called')
    test_class_instance.mylog.info('-------------------------------------------------------')
    test_class_instance.mylog.info('')
    list_of_buckets = []
    error_message = ''
    get_all_buckets_per_org_param = {'org': '%s' % org}
    response = test_class_instance.rl.get(base_url=url, path=BUCKETS_URL, params=get_all_buckets_per_org_param)
    try:
        # response object returns dictionary:
        # {u'buckets':
        #   [
        #       {u'name': u'bucket_1',
        #       u'links':
        #           {u'org': u'/api/v2/orgs/02a5230b19a22000',
        #           u'self': u'/api/v2/buckets/02a5231df7a22000'},
        #       u'organizationID': u'02a5230b19a22000',
        #       u'retentionPeriod': 0,
        #       u'organization': u'org_1',
        #       u'id': u'02a5231df7a22000'}
        #   ],
        # u'links': {u'self': u'/api/v2/buckets'}
        # }
        list_of_buckets = response.json()['buckets']
        if type(list_of_buckets) == list:
            test_class_instance.mylog.info('gateway_util.get_all_buckets() LIST OF BUCKETS=' +
                                           str(list_of_buckets))
        else:
            test_class_instance.mylog.info('gateway_util.get_all_buckets() ERROR=' + response.json()['message'])
    except:
        test_class_instance.mylog.info('gateway_util.get_all_buckets() Exception:')
        # get an error from the header
        error_message = response.headers['X-Influx-Error']
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(traceback.extract_tb(clt_error_traceback)))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
    test_class_instance.mylog.info('gateway_util.get_all_buckets() function is done')
    test_class_instance.mylog.info('')
    return response.status_code, error_message, list_of_buckets


def get_count_of_buckets(test_class_instance, list_of_buckets):
    """
    :param test_class_instance:
    :param list_of_buckets:
    :return: count of buckets
    """
    test_class_instance.mylog.info('gateway_util.get_count_of_buckets() function is being called')
    test_class_instance.mylog.info('------------------------------------------------------------')
    test_class_instance.mylog.info('')
    count = len(list_of_buckets)
    test_class_instance.mylog.info('gateway_util.get_count_of_buckets() : COUNT=' + str(count))
    return count


def find_bucket_by_name(test_class_instance, list_of_buckets, bucket_name, org_name):
    """
    :param test_class_instance:
    :param list_of_buckets:
    :param bucket_name:
    :param org_name:
    :return: true/false
    """
    success = False
    test_class_instance.mylog.info('gateway_util.find_bucket_by_name_by_org() function is being called')
    test_class_instance.mylog.info('------------------------------------------------------------------')
    test_class_instance.mylog.info('')
    for buckets_info in list_of_buckets:
        test_class_instance.mylog.info('gateway_util.find_bucket_by_name_by_org() '
                                       'Finding Bucket with \'%s\' name and Org \'%s\' in %s' %
                                       (bucket_name, org_name, str(buckets_info)))
        if buckets_info['organization'] == org_name and buckets_info['name'] == bucket_name:
            success = True
            break
    return success


# =================================================== PERMISSIONS =======================================================

def create_authorization(test_class_instance, url, user, userid, list_of_permission):
    """
    :param userid:
    :param test_class_instance:
    :param url:
    :param user:
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
    return {"STATUS_CODE": response.status_code, "ID": id, "USER": user_name, "USER_ID": user_id, "TOKEN": token,
            "PERMISSIONS": permissions, "ERROR_MESSAGE": error_message}


# ============================================== WRITE/QUERY DATA POINTS ================================================

def write_points(test_class_instance, url, token, organization, bucket, data):
    """
    Write point(s) to a bucket in organization given the correct credentials,=.
    :param data:
    :param test_class_instance:
    :param url: gateway url, e.g. http://localhost:9999
    :param token: Token for a given user, with a read/write permissions for a given user
    :param organization: organization the bucket belongs to
    :param bucket: bucket to write data point(s) to
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
    return {"STATUS_CODE": response.status_code, "ERROR_MESSAGE": error_message}


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
    test_class_instance.mylog.info('gateway_util.gateway_query_data() function is being called')
    test_class_instance.mylog.info('--------------------------------------------------\n')
    test_class_instance.mylog.info('gateway_util.gateway_query_data() : Query : \'%s\'' % query)
    test_class_instance.mylog.info('gateway_util.gateway_query_data() : Token : \'%s\'' % token)
    test_class_instance.mylog.info('gateway_util.gateway_query_data() : Org : \'%s\'' % organization)

    params = {"organization": "%s" % organization}
    data = '{"query":"%s}' % json.dumps(query)
    headers = {"Authorization": "Token %s" % token}

    response = test_class_instance.rl.post(base_url=url, path=GATEWAY_QUERY, params=params, data=data, headers=headers)
    # successful status is 200
    if response.status_code > 200:
        error = response.headers['X-Influx-Error']
    return {'STATUS_CODE': response.status_code, 'ERROR': error, 'RESULT': response.content}


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
    return {'STATUS_CODE': status_code, 'RESULT': result_list, 'ERROR': error}


# ========================================================== ETCD =======================================================

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
