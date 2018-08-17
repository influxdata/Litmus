
import sys
import traceback
import ast
import json
from src.util import litmus_utils

BUCKETS_URL='/v1/buckets'
TASKS_URL='/v1/tasks'
ORG_URL='/v1/orgs'
USERS_URL='/v1/users'

#=================================================== TASKS =============================================================

def create_task(test_class_instance, url, org_id, task_name, flux, status='enabled', owners=None, last=None):
    '''
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
    '''
    test_class_instance.mylog.info('gateway_util.create_task() function is being called')
    test_class_instance.mylog.info('---------------------------------------------------')
    test_class_instance.mylog.info('')
    test_class_instance.mylog.info('gateway_util.create_task() Creating Task with Organization ID : \'%s\','
                                   ' Task Name : \'%s\', Flux Script: \'%s\', Status : \'%s\', owners : \'%s\' '
                                   'and Last : \'%s\'') % (org_id, task_name, flux, status, owners, last)
    data='{"organization":"%s", "name":"%s", "flux":"%s", "status":"%s", "owners":"%s", "last":"%s"}' % org_id, \
         task_name, flux, status, owners, last
    task_id, org_id, task_name, task_status, task_owners, flux, every, cron, last=None, None, None, None, None, \
                                                                                  None, None, None, None
    response=test_class_instance.rl.post(base_url=url, path=TASKS_URL, data=data)
    try:
        task_id=response.json().get('id')
        org_id=response.json().get('organization')
        task_name=response.json().get('name')
        task_status=response.json().get('status')
        task_owners=response.json().get('owners')
        flux=response.json().get('flux')
        every=response.json().get('every')
        cron=response.json().get('cron')
        last=response.json().get('last')
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

#=================================================== ORGANIZATIONS =====================================================

def create_organization(test_class_instance, url, org_name):
    '''
    :param test_class_instance: instance of the test class
    :param url: gateway url,for example: http://localhost:9999
    :param org_name: name of the organization to create
    :return: status_code, org_id, created_org_name, error_message
    '''
    test_class_instance.mylog.info('gateway_util.create_organization() function is being called')
    test_class_instance.mylog.info('-----------------------------------------------------------')
    test_class_instance.mylog.info('')
    test_class_instance.mylog.info('gateway_util.create_organization() '
                                   'Creating Organization with \'%s\' name' % org_name)
    data='{"name":"%s"}' % org_name
    org_id, created_org_name, error_message=None, None, None
    response=test_class_instance.rl.post(base_url=url, path=ORG_URL, data=data)
    try:
        org_id=response.json().get('id')
        created_org_name=response.json().get('name')
        if org_id is not None and created_org_name is not None:
            test_class_instance.mylog.info('gateway_util.create_organization() ORG_ID=' + str(org_id))
            test_class_instance.mylog.info('gateway_util.create_organization() ORG_NAME=' + str(created_org_name))
        else:
            test_class_instance.mylog.info('gateway_util.create_organization() '
                                           'REQUESTED_ORG_ID AND REQUESTED_ORG_NAME ARE NONE')
            error_message=response.json()['message']
            test_class_instance.mylog.info('gateway_util.create_organization() ERROR=' + error_message)
    except:
        test_class_instance.mylog.info('gateway_util.create_organization() Exception:')
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(traceback.extract_tb(clt_error_traceback)))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
    test_class_instance.mylog.info('gateway_util.create_organization() function is done')
    test_class_instance.mylog.info('')
    return response.status_code, org_id, created_org_name, error_message

def update_organization(test_class_instance, url, org_id, new_org_name):
    '''
    :param test_class_instance:
    :param url:
    :param org_id:
    :param new_org_name:
    :return:
    '''
    test_class_instance.mylog.info('gateway_util.update_organization() function is being called')
    test_class_instance.mylog.info('-----------------------------------------------------------')
    test_class_instance.mylog.info('')
    data = '{"name":"%s"}' % new_org_name
    updated_org_name, new_org_id, error_message=None, None, None
    response=test_class_instance.rl.patch(base_url=url, path=ORG_URL+'/'+ str(org_id), data=data)
    try:
        new_org_id=response.json().get('id')
        updated_org_name=response.json().get('name')
        if org_id is not None and updated_org_name is not None:
            test_class_instance.mylog.info('gateway_util.update_organization() ORG_ID=' + str(new_org_id))
            test_class_instance.mylog.info('gateway_util.update_organization() ORG_NAME=' + str(updated_org_name))
        else:
            test_class_instance.mylog.info('gateway_util.update_organization() '
                                           'REQUESTED_ORG_ID AND REQUESTED_ORG_NAME ARE NONE')
            error_message=response.json()['message']
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
    '''
    :param test_class_instance:
    :param url:
    :param org_id:
    :return: status_code, requested_org_id, requested__org_name
    '''
    test_class_instance.mylog.info('gateway_util.get_organization_by_id() function is being called')
    test_class_instance.mylog.info('--------------------------------------------------------------')
    test_class_instance.mylog.info('')
    test_class_instance.mylog.info('gateway_util.get_organization_by_id() '
                                   'Getting Organization with \'%s\' id' % org_id)
    requested_org_id, requested_org_name, error_message=None, None, None
    response=test_class_instance.rl.get(base_url=url, path=ORG_URL+'/'+str(org_id))
    try:
        requested_org_id=response.json().get('id')
        requested_org_name=response.json().get('name')
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
    '''
    Gets all of the created organizations.
    :param test_class_instance:
    :param url:
    :return: status_code, list of organization's dictionaries:
            {u'id': u'0255285f6ef3c000', u'name': u'n_same_bucket_name'},
            {u'id': u'0255286dae73c000', u'name': u'u_same_bucket_name'}
    '''
    test_class_instance.mylog.info('gateway_util.get_all_organizations() function is being called')
    test_class_instance.mylog.info('-------------------------------------------------------------')
    test_class_instance.mylog.info('')
    list_of_organizations=[]
    response=test_class_instance.rl.get(base_url=url, path=ORG_URL)
    try:
        list_of_organizations=response.json()
        if type(list_of_organizations) == list:
            test_class_instance.mylog.info('gateway_util.get_all_organizations() LIST OF OGRANIZATIONS=' +
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

def find_org_by_name(test_class_instance, org_name_to_find, list_of_organizations):
    '''
    :param test_class_instance:
    :param org_name_to_find:
    :return: org name, id
    '''
    test_class_instance.mylog.info('gateway_util.find_org_by_name() function is being called')
    test_class_instance.mylog.info('--------------------------------------------------------')
    test_class_instance.mylog.info('')
    test_class_instance.mylog.info('gateway_util.find_org_by_name() '
                                   'Finding Organization with \'%s\' name' % org_name_to_find)
    result=filter(lambda org: org['name'] == org_name_to_find, list_of_organizations)
    orgname=result[0].get('name')
    test_class_instance.mylog.info('gateway_util.find_org_by_name() : ORG_NAME=' + str(orgname))
    orgid=result[0].get('id')
    test_class_instance.mylog.info('gateway_util.find_org_by_name() : ORG_ID=' + str(orgid))
    return orgname, orgid

def find_org_by_id(test_class_instance, org_id_to_find, list_of_organizations):
    '''
    :param test_class_instance:
    :param org_id_to_find:
    :return: org name, id
    '''
    test_class_instance.mylog.info('gateway_util.find_org_by_id() function is being called')
    test_class_instance.mylog.info('------------------------------------------------------')
    test_class_instance.mylog.info('')
    test_class_instance.mylog.info('gateway_util.find_org_by_id() '
                                   'Finding Organization with \'%s\' id' % org_id_to_find)
    result=filter(lambda org: org['id'] == org_id_to_find, list_of_organizations)
    orgname=result[0].get('name')
    test_class_instance.mylog.info('gateway_util.find_org_by_name() : ORG_NAME=' + str(orgname))
    orgid=result[0].get('id')
    test_class_instance.mylog.info('gateway_util.find_org_by_name() : ORG_ID=' + str(orgid))
    return orgname, orgid

def get_count_of_orgs(test_class_instance, list_of_organizations):
    '''
    :param test_class_instance:
    :param list_of_organizations:
    :return: count of corganizations
    '''
    test_class_instance.mylog.info('gateway_util.get_count_of_orgs() function is being called')
    test_class_instance.mylog.info('---------------------------------------------------------')
    test_class_instance.mylog.info('')
    count=len(list_of_organizations)
    test_class_instance.mylog.info('gateway_util.get_count_of_orgs() : COUNT=' + str(count))
    return count

#================================================== USERS ==============================================================

def create_user(test_class_instance, url, user_name):
    '''
    :param test_class_instance:
    :param url:
    :param user_name:
    :return:
    '''
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
    '''
    :param test_class_instance:
    :param url:
    :param user_id:
    :param new_user_name:
    :return:
    '''
    test_class_instance.mylog.info('gateway_util.update_user() function is being called')
    test_class_instance.mylog.info('----------------------------------------------------')
    test_class_instance.mylog.info('')
    data='{"name":"%s"}' % new_user_name
    updated_user_name, new_user_id, error_message = None, None, None
    response=test_class_instance.rl.patch(base_url=url, path=USERS_URL + '/' + str(user_id), data=data)
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
    return (response.status_code, new_user_id, updated_user_name, error_message)

# THIS IS NOT WORKING YET FROM API STAND POINT. INFLUX TOOL WORKS
def get_user_by_name(test_class_instance, url, user_name):
    '''
    :param test_class_instance:
    :param url:
    :param user_name:
    :return: status_code, requested_user_id, requested_user_name
    '''
    test_class_instance.mylog.info('gateway_util.get_user_by_name() function is being called')
    test_class_instance.mylog.info('-----------------------------------------------------------')
    test_class_instance.mylog.info('')
    test_class_instance.mylog.info('gateway_util.get_user_by_name() '
                                   'Getting User with \'%s\' name' % user_name)
    requested_user_id, requested_user_name, error_message=None, None, None
    response=test_class_instance.rl.get(base_url=url, path=USERS_URL+'/'+str(user_name))
    try:
        requested_user_id=response.json().get('id')
        requested_user_name=response.json().get('name')
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
    '''
    :param test_class_instance:
    :param url:
    :param user_id:
    :return: status_code, requested_user_id, requested_user_name
    '''
    test_class_instance.mylog.info('gateway_util.get_user_by_id() function is being called')
    test_class_instance.mylog.info('------------------------------------------------------')
    test_class_instance.mylog.info('')
    test_class_instance.mylog.info('gateway_util.get_user_by_id() '
                                   'Getting User with \'%s\' id' % user_id)
    requested_user_id, requested_user_name, error_message=None, None, None
    response=test_class_instance.rl.get(base_url=url, path=USERS_URL+'/'+str(user_id))
    try:
        requested_user_id=response.json().get('id')
        requested_user_name=response.json().get('name')
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
    '''
    Gets all of the created users.
    :param test_class_instance: instance of the test class
    :param url: gateway url
    :return: status code and list of all of the users's dictionaries:
             {u'id': u'025e2102a017d000', u'name': u'test-user'}
    '''
    test_class_instance.mylog.info('gateway_util.get_all_users() function is being called')
    test_class_instance.mylog.info('-----------------------------------------------------')
    test_class_instance.mylog.info('')
    list_of_users=[]
    response=test_class_instance.rl.get(base_url=url, path=USERS_URL)
    try:
        list_of_users=response.json()
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
    '''
    :param test_class_instance:
    :param list_of_users:
    :return: count of users
    '''
    test_class_instance.mylog.info('gateway_util.get_count_of_users() function is being called')
    test_class_instance.mylog.info('----------------------------------------------------------')
    test_class_instance.mylog.info('')
    count=len(list_of_users)
    test_class_instance.mylog.info('gateway_util.get_count_of_users() : COUNT=' + str(count))
    return count

def find_user_by_name(test_class_instance, user_name, list_of_users):
    '''
    :param test_class_instance:
    :param list_of_buckets:
    :param user_name:
    :return: true/false
    '''
    success=False
    test_class_instance.mylog.info('gateway_util.find_user_by_name() function is being called')
    test_class_instance.mylog.info('---------------------------------------------------------')
    test_class_instance.mylog.info('')
    for user_info in list_of_users:
        test_class_instance.mylog.info('gateway_util.find_user_by_name() Finding User with \'%s\' name' % user_name)
        if user_info['name'] == user_name:
            success=True
            break
    return success

#=================================================== BUCKETS ===========================================================

# Currently retention periods are only numbers and not durations:
# https://github.com/influxdata/platform/issues/144
def create_bucket(test_class_instance, url, bucket_name, retentionPeriod=None, organizationID=None):
    '''
    Create a bucket for an organization with a certain retention period
    :param test_class_instance: instance of the test class
    :param url (str): gateway url
    :param bucket_name (str): name of the bucket to be created
    :param retentionPeriod (str): retention Period of the bucket, one of h,m,s,m,ns
    :param organizationID (str): ID of the organization this bucket would belong to
    :return:
    '''
    # do not use retention period for now, use a hardcoded value:
    test_class_instance.mylog.info('gateway_util.create_bucket() function is being called')
    test_class_instance.mylog.info('-----------------------------------------------------')
    test_class_instance.mylog.info('')
    test_class_instance.mylog.info('gateway_util.create_function() :'
                                   'Creating Bucket with \'%s\' name' % bucket_name)
    # hardcoding retention period to 1, anything below 1h, will default to 1h,
    # https://github.com/influxdata/platform/issues/143
    if retentionPeriod is None:
        data = '{"name":"%s", "organizationID": "%s"}' % (bucket_name, organizationID)
    elif organizationID is None:
        data = '{"name":"%s", "retentionPeriod": %d}' % (bucket_name, retentionPeriod)
    else:
        data = '{"name":"%s", "retentionPeriod": %d, "organizationID": "%s"}' \
               % (bucket_name, retentionPeriod, organizationID)

    organization_id, created_bucket_id, created_bucket_name, \
    retention_period, error_message=None, None, None, None, None
    response=test_class_instance.rl.post(base_url=url, path=BUCKETS_URL, data=data)
    try:
        organization_id=response.json().get('organizationID')
        created_bucket_name=response.json().get('name')
        created_bucket_id=response.json().get('id')
        retention_period=response.json().get('retentionPeriod')
        if created_bucket_id is not None and created_bucket_name is not None:
            test_class_instance.mylog.info('gateway_util.create_bucket() BUCKET_ID=' + str(created_bucket_id))
            test_class_instance.mylog.info('gateway_util.create_user() BUCKET_NAME=' + str(created_bucket_name))
        else:
            test_class_instance.mylog.info('gateway_util.create_bucket() '
                                           'REQUESTED_BUCKET_ID AND REQUESTED_BUCKET_NAME ARE NONE')
            error_message=response.json()['message']
            test_class_instance.mylog.info('gateway_util.create_bucket() ERROR=' + error_message)
    except:
        test_class_instance.mylog.info('gateway_util.create_bucket() Exception:')
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(traceback.extract_tb(clt_error_traceback)))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
    test_class_instance.mylog.info('gateway_util.create_organization() function is done')
    test_class_instance.mylog.info('')
    return response.status_code, created_bucket_id, created_bucket_name, \
           organization_id, retention_period, error_message

def update_bucket(test_class_instance, url, bucket_id, new_bucket_name=None, new_retention=None):
    '''
    :param test_class_instance:
    :param url: gateway
    :param bucket_id:
    :param new_bucket_name:
    :param new_retention:
    :return:
    '''
    test_class_instance.mylog.info('gateway_util.update_bucket() function is being called')
    test_class_instance.mylog.info('-----------------------------------------------------')
    test_class_instance.mylog.info('')
    if new_retention is None and new_bucket_name is None:
        data='{}'
    elif new_retention is None:
        data='{"name":"%s"}' % new_bucket_name
    elif new_bucket_name is None:
        data='{"retentionPeriod":"%d"}' % new_retention
    else:
        data='{"name":"%s", "retentionPeriod":"%d"}' % (new_bucket_name, new_retention)
    updated_bucket_name, updated_bucket_id, updated_retention, org_id, org_name, error_message=\
        None, None, None, None, None, None
    response=test_class_instance.rl.patch(base_url=url, path=BUCKETS_URL+'/'+ str(bucket_id), data=data)
    try:
        updated_bucket_id=response.json().get('id')
        updated_bucket_name=response.json().get('name')
        updated_retention=response.json().get('retentionPeriod')
        org_id=response.json().get('organizationID')
        org_name=response.json().get('organization')
        if updated_bucket_id is not None and updated_bucket_name is not None and updated_retention is not None \
                and org_id is not None and org_name is not None:
            test_class_instance.mylog.info('gateway_util.update_bucket() UPDATED_BUCKET_ID=' + str(updated_bucket_id))
            test_class_instance.mylog.info('gateway_util.update_bucket() UPDATED_BUCKET_NAME=' + str(updated_bucket_name))
            test_class_instance.mylog.info('gateway_util.update_bucket() UPDATED_RETENTION=' + str(updated_retention))
            test_class_instance.mylog.info('gateway_util.update_bucket() ORG_ID=' + str(org_id))
            test_class_instance.mylog.info('gateway_util.update_bucket() ORG_NAME=' + str(org_name))
        else:
            test_class_instance.mylog.info('gateway_util.update_bucket() SOME OF THE VALUES ARE NONE')
            error_message=response.json()['message']
            test_class_instance.mylog.info('gateway_util.create_bucket() ERROR=' + error_message)
    except:
        test_class_instance.mylog.info('gateway_util.update_bucket() Exception:')
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(traceback.extract_tb(clt_error_traceback)))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
    test_class_instance.mylog.info('gateway_util.update_obucket() function is done')
    test_class_instance.mylog.info('')
    return response.status_code, updated_bucket_id, updated_bucket_name, updated_retention, org_id, \
           org_name, error_message

def get_bucket_by_id(test_class_instance, url, bucket_id):
    '''
    :param test_class_instance:
    :param url:
    :param org_id:
    :return: status_code, requested_org_id, requested__org_name
    '''
    test_class_instance.mylog.info('gateway_util.get_bucket_by_id() function is being called')
    test_class_instance.mylog.info('--------------------------------------------------------')
    test_class_instance.mylog.info('')
    test_class_instance.mylog.info('gateway_util.get_bucket_by_id() '
                                   'Getting Bucket with \'%s\' id' % bucket_id)
    requested_bucket_id, requested_bucket_name, error_message=None, None, None
    response=test_class_instance.rl.get(base_url=url, path=BUCKETS_URL+'/'+str(bucket_id))
    try:
        requested_bucket_id=response.json().get('id')
        requested_bucket_name=response.json().get('name')
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

def get_all_buckets(test_class_instance, url):
    '''
    Gets all of the created buckets.
    :param test_class_instance: instance of the test class
    :param url: gateway url
    :return: status code and list of all of the bucket's dictionaries:
             {u'organizationID': u'0255286dae73c000', u'organization': u'u_same_bucket_name', u'id': u'0255286eb833c000',
                    u'retentionPeriod': 1, u'name': u'one_for_all'}
             {u'organizationID': u'0255284939b3c000', u'organization': u'c_same_bucket_name', u'id': u'0255284a3d33c000',
                    u'retentionPeriod': 1, u'name': u'one_for_all'}
    '''
    test_class_instance.mylog.info('gateway_util.get_all_buckets() function is being called')
    test_class_instance.mylog.info('-------------------------------------------------------')
    test_class_instance.mylog.info('')
    list_of_buckets=[]
    response=test_class_instance.rl.get(base_url=url, path=BUCKETS_URL)
    try:
        list_of_buckets=response.json()
        if type(list_of_buckets) == list:
            test_class_instance.mylog.info('gateway_util.get_all_buckets() LIST OF BUCKETS=' +
                                           str(list_of_buckets))
        else:
            test_class_instance.mylog.info('gateway_util.get_all_buckets() ERROR=' + response.json()['message'])
    except:
        test_class_instance.mylog.info('gateway_util.get_all_buckets() Exception:')
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(traceback.extract_tb(clt_error_traceback)))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
    test_class_instance.mylog.info('gateway_util.get_all_buckets() function is done')
    test_class_instance.mylog.info('')
    return response.status_code, list_of_buckets

def get_count_of_buckets(test_class_instance, list_of_buckets):
    '''
    :param test_class_instance:
    :param list_of_buckets:
    :return: count of buckets
    '''
    test_class_instance.mylog.info('gateway_util.get_count_of_buckets() function is being called')
    test_class_instance.mylog.info('------------------------------------------------------------')
    test_class_instance.mylog.info('')
    count=len(list_of_buckets)
    test_class_instance.mylog.info('gateway_util.get_count_of_buckets() : COUNT=' + str(count))
    return count

def find_bucket_by_name(test_class_instance, list_of_buckets, bucket_name, org_name):
    '''
    :param test_class_instance:
    :param list_of_buckets:
    :param bucket_name:
    :param org_name:
    :return: true/false
    '''
    success=False
    test_class_instance.mylog.info('gateway_util.find_bucket_by_name_by_org() function is being called')
    test_class_instance.mylog.info('------------------------------------------------------------------')
    test_class_instance.mylog.info('')
    for buckets_info in list_of_buckets:
        test_class_instance.mylog.info('gateway_util.find_bucket_by_name_by_org() '
                                       'Finding Bucket with \'%s\' name and Org \'%s\' in %s' %
                                       (bucket_name, org_name, str(buckets_info)))
        if buckets_info['organization'] == org_name and buckets_info['name'] == bucket_name:
            success=True
            break
    return success

#========================================================== ETCD =======================================================

def verify_org_etcd(test_class_instance, etcd, org_id, org_name):
    '''
    Function asserts that organization_id and organization_name exist in etcd store
    :param test_class_instance: instance of the test class, i.e. self
    :param etcd: url of the etcd service
    :param org_id: organization id
    :param org_name: organization name
    :return: does not return a value
    '''
    test_class_instance.mylog.info('gateway_util.verify_org_etcd() function is being called')
    test_class_instance.mylog.info('-------------------------------------------------------')
    test_class_instance.mylog.info('')
    cmd='ETCDCTL_API=3 /usr/local/bin/etcdctl --endpoints %s get --prefix "Organizationv1/%s" --print-value-only'\
        % (etcd, org_id)
    out, error=litmus_utils.execCmd(test_class_instance, cmd, status='OUT_STATUS')
    # make sure there is no error message and output of the command is not empty
    try:
        assert error == '' and out != '', 'Executing command \'%s\' returned an error \'%s\' ' \
                                          'or output of the command is empty' % (cmd, error)
    except AssertionError, e:
        test_class_instance.mylog.info(e)
        raise
    actual_org_id=ast.literal_eval(out).get('id')
    test_class_instance.mylog.info('Assert expected org_id ' + str(org_id) + ' equals to actual org_id '
                                   + str(actual_org_id))
    try:
        assert org_id == actual_org_id, 'Expected org id is not equal to actual org id'
    except AssertionError, e:
        test_class_instance.mylog.info(e)
        raise
    actual_org_name = ast.literal_eval(out).get('name')
    if org_name != 'DoubleQuotes\"' and org_name != 'DoubleQuotes\"_updated_name':
        actual_org_name=json.loads("\"" + actual_org_name + "\"")
    test_class_instance.mylog.info('Assert expected user_name ' + str(org_name) + ' equals actual to user_name '
                           + str(actual_org_name))
    try:
        assert org_name == actual_org_name, 'Expected org name is not equal to actual org name'
    except AssertionError, e:
        test_class_instance.mylog.info(e)
        raise

def verify_user_etcd(test_class_instance, etcd, user_id, user_name):
    '''
    Function asserts that user_id and user_name exist in the etcd store.
    :param test_class_instance: instance of the test class, i.e. self
    :param etcd: url of the etcd service
    :param user_id: id of the user
    :param user_name: name of the user
    :return: does not return a value
    '''
    test_class_instance.mylog.info('gateway_util.verify_user_etcd() function is being called')
    test_class_instance.mylog.info('--------------------------------------------------------')
    test_class_instance.mylog.info('gateway_util.verify_user_etcd(): params: %s and %s' %(user_id, user_name))
    test_class_instance.mylog.info('')
    cmd='ETCDCTL_API=3 /usr/local/bin/etcdctl --endpoints %s get --prefix "userv1/%s" --print-value-only'\
        % (etcd, user_id)
    out, error=litmus_utils.execCmd(test_class_instance, cmd, status='OUT_STATUS')
    # make sure there is not error before proceeding further
    try:
        assert error == '' and out != '', 'Executing \'%s\' command returned an error \'%s\'' % (cmd, error)
    except AssertionError, e:
        test_class_instance.mylog.info(e)
        raise
    actual_user_id=ast.literal_eval(out).get('id')
    test_class_instance.mylog.info('Assert expected user_id ' + str(user_id) + ' equals to actual user_id '
                                   + str(actual_user_id))
    try:
        assert user_id == actual_user_id, 'Expected user id is not equal to actual user id'
    except AssertionError, e:
        test_class_instance.mylog.info(e)
        raise
    actual_user_name=ast.literal_eval(out).get('name')
    if user_name != 'DoubleQuotes\"' and user_name != 'DoubleQuotes\"_updated_name':
        actual_user_name=json.loads("\"" + actual_user_name + "\"")
    test_class_instance.mylog.info('Assert expected user_name ' + str(user_name) + ' equals actual to user_name '
                           + str(actual_user_name))
    try:
        assert user_name == actual_user_name, 'Expected user name is not equal to actual user name'
    except AssertionError, e:
        test_class_instance.mylog.info(e)
        raise

def verify_bucket_etcd(test_class_instance, etcd, bucket_id, bucket_name):
    '''
    Function asserts that bucket_id and bucket_name exist in the etcd store.
    :param test_class_instance: instance of the test clas, i.e. self
    :param etcd: url of the etcd service
    :param bucket_id: id of the bucket
    :param bucket_name: name of the bucket
    :return: does not return a value
    '''
    test_class_instance.mylog.info('gateway_util.verify_bucket_etcd() function is being called')
    test_class_instance.mylog.info('----------------------------------------------------------')
    test_class_instance.mylog.info('gateway_util.verify_bucket_etcd(): params: %s and %s' %(bucket_id, bucket_name))
    test_class_instance.mylog.info('')
    cmd='ETCDCTL_API=3 /usr/local/bin/etcdctl --endpoints %s get --prefix "bucketv1/%s" --print-value-only'\
        % (etcd, bucket_id)
    out, error=litmus_utils.execCmd(test_class_instance, cmd, status='OUT_STATUS')
    # make sure there is not error before proceeding further
    try:
        assert error == '' and out != '', 'Executing \'%s\' command returned an error \'%s\'' % (cmd, error)
    except AssertionError, e:
        test_class_instance.mylog.info(e)
        raise
    actual_bucket_id=ast.literal_eval(out).get('id')
    test_class_instance.mylog.info('Assert expected bucket_id ' + str(bucket_id) + ' equals to actual bucket_id '
                                   + str(actual_bucket_id))
    try:
        assert bucket_id == actual_bucket_id, 'Expected bucket id is not equal to actual bucket id'
    except AssertionError, e:
        test_class_instance.mylog.info(e)
        raise
    actual_bucket_name=ast.literal_eval(out).get('name')
    if bucket_name != 'DoubleQuotes\"' and bucket_name != 'DoubleQuotes\"_updated_name' \
            and bucket_name != 'DoubleQuotes\"_updated':
        actual_bucket_name=json.loads("\"" + actual_bucket_name + "\"")
    test_class_instance.mylog.info('Assert expected bucket_name ' + str(bucket_name) + ' equals actual to bucket_name '
                           + str(actual_bucket_name))
    try:
        assert bucket_name == actual_bucket_name, 'Expected bucket name is not equal to actual bucket name'
    except AssertionError, e:
        test_class_instance.mylog.info(e)
        raise