
import sys
import traceback
import ast
import json
from src.util import litmus_utils

#=================================================== ORGANIZATIONS =====================================================

ORG_URL='/v1/orgs'

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

USERS_URL='/v1/users'

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

#=================================================== BUCKETS ===========================================================

BUCKETS_URL='/v1/buckets'

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
    :param test_class_instance: instance of the test clas, i.e. self
    :param etcd: url of the etcd service
    :param org_id: organization id
    :param org_name: organization name
    :return: does not return anything
    '''
    test_class_instance.mylog.info('gateway_util.verify_org_etcd() function is being called')
    test_class_instance.mylog.info('-------------------------------------------------------')
    test_class_instance.mylog.info('')
    cmd='ETCDCTL_API=3 /usr/local/bin/etcdctl --endpoints %s get --prefix "Organizationv1/%s" --print-value-only'\
        % (etcd, org_id)
    out=litmus_utils.execCmd(test_class_instance, cmd, status='OUT_STATUS')
    actual_org_id=ast.literal_eval(out[0]).get('id')
    test_class_instance.mylog.info('Assert expected org_id ' + str(org_id) + ' equals to actual org_id '
                                   + str(actual_org_id))
    assert org_id == actual_org_id, test_class_instance.mylog.info('Expected org id is not equal to actual org id')
    actual_org_name = ast.literal_eval(out[0]).get('name')
    if org_name != 'DoubleQuotes\"' and org_name != 'DoubleQuotes\"_updated_name':
        actual_org_name=json.loads("\"" + actual_org_name + "\"")
    test_class_instance.mylog.info('Assert expected user_name ' + str(org_name) + ' equals actual to user_name '
                           + str(actual_org_name))
    assert org_name == actual_org_name, \
        test_class_instance.mylog.info('Expected org name is not equal to actual org name')

def verify_user_etcd(test_class_instance, etcd, user_id, user_name):
    '''
    :param test_class_instance: instance of the test clas, i.e. self
    :param etcd: url of the etcd service
    :param user_id: organization id
    :param user_name: organization name
    :return: does not return anything
    '''
    test_class_instance.mylog.info('gateway_util.verify_user_etcd() function is being called')
    test_class_instance.mylog.info('--------------------------------------------------------')
    test_class_instance.mylog.info('gateway_util.verify_user_etcd(): params: %s and %s' %(user_id, user_name))
    test_class_instance.mylog.info('')
    cmd='ETCDCTL_API=3 /usr/local/bin/etcdctl --endpoints %s get --prefix "userv1/%s" --print-value-only'\
        % (etcd, user_id)
    out=litmus_utils.execCmd(test_class_instance, cmd, status='OUT_STATUS')
    actual_user_id=ast.literal_eval(out[0]).get('id')
    test_class_instance.mylog.info('Assert expected user_id ' + str(user_id) + ' equals to actual user_id '
                                   + str(actual_user_id))
    assert user_id == actual_user_id, test_class_instance.mylog.info('Expected user id is not equal to actual user id')
    actual_user_name=ast.literal_eval(out[0]).get('name')
    if user_name != 'DoubleQuotes\"' and user_name != 'DoubleQuotes\"_updated_name':
        actual_user_name=json.loads("\"" + actual_user_name + "\"")
    test_class_instance.mylog.info('Assert expected user_name ' + str(user_name) + ' equals actual to user_name '
                           + str(actual_user_name))
    assert user_name == actual_user_name, \
        test_class_instance.mylog.info('Expected user name is not equal to actual user name')

def verify_bucket_etcd(test_class_instance, etcd, bucket_id, bucket_name):
    '''
    :param test_class_instance: instance of the test clas, i.e. self
    :param etcd: url of the etcd service
    :param bucket_id: bucket id
    :param bucket_name: bucket name
    :return:
    '''
    test_class_instance.mylog.info('gateway_util.verify_bucket_etcd() function is being called')
    test_class_instance.mylog.info('----------------------------------------------------------')
    test_class_instance.mylog.info('gateway_util.verify_bucket_etcd(): params: %s and %s' %(bucket_id, bucket_name))
    test_class_instance.mylog.info('')
    cmd='ETCDCTL_API=3 /usr/local/bin/etcdctl --endpoints %s get --prefix "bucketv1/%s" --print-value-only'\
        % (etcd, bucket_id)
    out=litmus_utils.execCmd(test_class_instance, cmd, status='OUT_STATUS')
    actual_bucket_id=ast.literal_eval(out[0]).get('id')
    test_class_instance.mylog.info('Assert expected bucket_id ' + str(bucket_id) + ' equals to actual bucket_id '
                                   + str(actual_bucket_id))
    assert bucket_id == actual_bucket_id, \
        test_class_instance.mylog.info('Expected bucket id is not equal to actual bucket id')
    actual_bucket_name=ast.literal_eval(out[0]).get('name')
    if bucket_name != 'DoubleQuotes\"' and bucket_name != 'DoubleQuotes\"_updated_name' \
            and bucket_name != 'DoubleQuotes\"_updated':
        actual_bucket_name=json.loads("\"" + actual_bucket_name + "\"")
    test_class_instance.mylog.info('Assert expected bucket_name ' + str(bucket_name) + ' equals actual to bucket_name '
                           + str(actual_bucket_name))
    assert bucket_name == actual_bucket_name, \
        test_class_instance.mylog.info('Expected bucket name is not equal to actual bucket name')