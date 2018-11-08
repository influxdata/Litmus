import sys
import traceback


BUCKETS_URL = '/api/v2/buckets'


# Create a bucket
def create_bucket(test_class_instance, url, bucket_name, retention_rules=None, organization_id=None):
    """
    create_bucket() function creates buckets for a specific organization
    :param test_class_instance: instance of the test class
    :param url: gateway url,for example: http://localhost:9999
    :param bucket_name: name of the bucket to create
    :param retention_rules (int>=1): rules to expire ot retain data.No rules means data never expires
    :param organization_id: id of the organization
    :return: dictionary
    """
    test_class_instance.mylog.info('buckets_util.create_bucket() function is being called')
    test_class_instance.mylog.info('-----------------------------------------------------')
    test_class_instance.mylog.info('')
    test_class_instance.mylog.info('buckets_util.create_function() :'
                                   'Creating Bucket with \'%s\' name, \'%s\' retention rules and \'%s\' org id'
                                   % (bucket_name, retention_rules, organization_id))
    if retention_rules is None:  # data never expires
        data = '{"name":"%s", "organizationID": "%s"}' % (bucket_name, organization_id)
    # organization is required, for a negative case
    elif organization_id is None:
        data = '{"name":"%s", "retentionRules": [{"type":"expire","everySeconds":%d}]}' % (bucket_name, retention_rules)
    else:
        data = '{"name":"%s", "retentionRules": [{"type":"expire","everySeconds":%d}], "organizationID": "%s"}' \
               % (bucket_name, retention_rules, organization_id)

    organization_id, organization, created_bucket_id, created_bucket_name, error_message = '', '', '', '', ''
    retention_period = 0
    response = test_class_instance.rl.post(base_url=url, path=BUCKETS_URL, data=data)
    try:
        organization_id = response.json().get('organizationID')
        created_bucket_name = response.json().get('name')
        created_bucket_id = response.json().get('id')
        organization = response.json().get('organization')
        if retention_rules:
            retention_period = response.json().get('retentionRules')[0].get('everySeconds')
        org_link = response.json().get('links').get('org')
        log_link = response.json().get('links').get('log')
        if created_bucket_id is not None and created_bucket_name is not None:
            test_class_instance.mylog.info('buckets_util.create_bucket() BUCKET_ID=' + str(created_bucket_id))
            test_class_instance.mylog.info('buckets_util.create_bucket() BUCKET_NAME=' + str(created_bucket_name))
            test_class_instance.mylog.info('buckets_util.create_bucket() ORG_ID=' + str(organization_id))
            test_class_instance.mylog.info('buckets_util.create_bucket() ORG=' + str(organization))
            test_class_instance.mylog.info('buckets_util.create_bucket() RETENTION_PERIOD=' + str(retention_period))
            test_class_instance.mylog.info('buckets_util.create_bucket() ORG_LINK=' + str(org_link))
            test_class_instance.mylog.info('buckets_util.create_bucket() LOG_LINK=' + str(log_link))
        else:
            test_class_instance.mylog.info('buckets_util.create_bucket() '
                                           'REQUESTED_BUCKET_ID AND REQUESTED_BUCKET_NAME ARE NONE')
            error_message = response.headers['X-Influx-Error']
            test_class_instance.mylog.info('buckets_util.create_bucket() ERROR=' + error_message)
    except:
        test_class_instance.mylog.info('buckets_util.create_bucket() Exception:')
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(traceback.extract_tb(clt_error_traceback)))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
        error_message = response.headers['X-Influx-Error']
    test_class_instance.mylog.info('buckets_util.create_bucket() function returned : status = \'%s\', '
                                   'bucket_id = \'%s\', bucket_name = \'%s\', org_id = \'%s\', rp = \'%s\', '
                                   'error_message = \'%s\'' % (response.status_code, created_bucket_id,
                                                               created_bucket_name, organization_id, retention_period,
                                                               error_message))
    test_class_instance.mylog.info('buckets_util.create_bucket() function is done')
    test_class_instance.mylog.info('')
    return {'status':response.status_code, 'bucket_id':created_bucket_id, 'bucket_name':created_bucket_name,
            'org_id':organization_id, 'org':organization, 'every_seconds':retention_period,
            'error_message':error_message}


# Update bucket
def update_bucket(test_class_instance, url, bucket_id, original_bucket_name, original_retention, new_bucket_name=None,
                  new_retention=None):
    """
    update_bucket() function updates bucket with new bucket name or/and new retention rule
    :param test_class_instance: instance of the test class
    :param url: gateway url,for example: http://localhost:9999
    :param bucket_id: id of the bucket to update
    :param original_bucket_name: original name of the bucket
    :param original_retention: original retention period (int)
    :param new_bucket_name: new bucket name
    :param new_retention: new retention rule (int)
    :return: dictionary
    """
    test_class_instance.mylog.info('buckets_util.update_bucket() function is being called')
    test_class_instance.mylog.info('-----------------------------------------------------')
    test_class_instance.mylog.info('')
    # neither bucket name nor retention rule are being updated
    if new_retention is None and new_bucket_name is None:
        data = '{"name":"%s", "retentionRules": [{"type":"expire","everySeconds":%d}]}' \
               % (original_bucket_name, original_retention)
    # only update retention rule
    elif new_bucket_name is None and new_retention is not None:
        data = '{"name":"%s", "retentionRules": [{"type":"expire","everySeconds":%d}]}' \
               % (original_bucket_name, new_retention)
    # only update bucket name
    elif new_retention is None and new_bucket_name is not None:
        data = '{"name":"%s", "retentionRules": [{"type":"expire","everySeconds":%d}]}' \
               % (new_bucket_name, original_retention)
    # update bucket name and retention rule
    else:
        data = '{"name":"%s", "retentionRules": [{"type":"expire","everySeconds":%d}]}' \
               % (new_bucket_name, new_retention)
    updated_bucket_name, updated_bucket_id, org_id, org_name, error_message = \
        None, None, None, None, None
    updated_retention = 0
    response = test_class_instance.rl.patch(base_url=url, path=BUCKETS_URL + '/' + str(bucket_id), data=data)
    try:
        updated_bucket_id = response.json().get('id')
        updated_bucket_name = response.json().get('name')
        if new_retention != []:
            updated_retention = response.json().get('retentionRules')[0].get('everySeconds')
        org_id = response.json().get('organizationID')
        org_name = response.json().get('organization')
        org_link = response.json().get('links').get('org')
        log_link = response.json().get('links').get('log')
        if updated_bucket_id is not None and updated_bucket_name is not None and updated_retention is not None \
                and org_id is not None and org_name is not None:
            test_class_instance.mylog.info('buckets_util.update_bucket() UPDATED_BUCKET_ID=' + str(updated_bucket_id))
            test_class_instance.mylog.info('buckets_util.update_bucket() UPDATED_BUCKET_NAME=' + str(updated_bucket_name))
            test_class_instance.mylog.info('buckets_util.update_bucket() UPDATED_RETENTION=' + str(updated_retention))
            test_class_instance.mylog.info('buckets_util.update_bucket() ORG_ID=' + str(org_id))
            test_class_instance.mylog.info('buckets_util.update_bucket() ORG_NAME=' + str(org_name))
            test_class_instance.mylog.info('buckets_util.update_bucket() ORG_LINK=' + str(org_link))
            test_class_instance.mylog.info('buckets_util.update_bucket() LOG_LINK=' + str(log_link))
        else:
            test_class_instance.mylog.info('buckets_util.update_bucket() SOME OF THE VALUES ARE NONE')
            error_message = response.headers['X-Influx-Error']
            test_class_instance.mylog.info('buckets_util.create_bucket() ERROR=' + error_message)
    except:
        test_class_instance.mylog.info('buckets_util.update_bucket() Exception:')
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(traceback.extract_tb(clt_error_traceback)))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
        error_message = response.headers['X-Influx-Error']
    test_class_instance.mylog.info('buckets_util.update_bucket() function is done')
    test_class_instance.mylog.info('')
    return {'status':response.status_code, 'bucket_id':updated_bucket_id, 'bucket_name':updated_bucket_name,
            'org_id':org_id, 'org':org_name, 'every_seconds':updated_retention, 'error_message':error_message}


# Get information about a bucket using its ID
def get_bucket_by_id(test_class_instance, url, bucket_id):
    """
    get_bucket_by_id() function returns information about bucket using its id
    :param test_class_instance: instance of the test class
    :param url: gateway url,for example: http://localhost:9999
    :param bucket_id: get information of the bucket using bucket id
    :return: dictionary
    """
    test_class_instance.mylog.info('buckets_util.get_bucket_by_id() function is being called')
    test_class_instance.mylog.info('--------------------------------------------------------')
    test_class_instance.mylog.info('')
    test_class_instance.mylog.info('buckets_util.get_bucket_by_id() '
                                   'Getting Bucket with \'%s\' id' % bucket_id)
    requested_bucket_id, requested_bucket_name, error_message, org_id, org_name = None, None, None, None, None
    retention_period = 0
    response = test_class_instance.rl.get(base_url=url, path=BUCKETS_URL + '/' + str(bucket_id))
    try:
        org_id = response.json().get('organizationID')
        org_name = response.json().get('organization')
        org_link = response.json().get('links').get('org')
        log_link = response.json().get('links').get('log')
        if response.json().get('retentionRules') != []:
            retention_period = response.json().get('retentionRules')[0].get('everySeconds')
        requested_bucket_id = response.json().get('id')
        requested_bucket_name = response.json().get('name')
        if requested_bucket_id is not None and requested_bucket_name is not None:
            test_class_instance.mylog.info('buckets_util.get_bucket_by_id() BUCKET_ID=' + str(requested_bucket_id))
            test_class_instance.mylog.info('buckets_util.get_bucket_by_id() BUCKET_NAME=' + str(requested_bucket_name))
            test_class_instance.mylog.info('buckets_util.update_bucket() RETENTION=' + str(retention_period))
            test_class_instance.mylog.info('buckets_util.update_bucket() ORG_ID=' + str(org_id))
            test_class_instance.mylog.info('buckets_util.update_bucket() ORG_NAME=' + str(org_name))
            test_class_instance.mylog.info('buckets_util.update_bucket() ORG_LINK=' + str(org_link))
            test_class_instance.mylog.info('buckets_util.update_bucket() LOG_LINK=' + str(log_link))
        else:
            test_class_instance.mylog.info('buckets_util.get_bucket_by_id() '
                                           'REQUESTED_BUCKET_ID AND REQUESTED_BUCKET_NAME ARE NONE')
            error_message = response.headers['X-Influx-Error']
            test_class_instance.mylog.info('gateway_util.get_bucket_by_id() ERROR=' + error_message)
    except:
        test_class_instance.mylog.info('buckets_util.get_bucket_by_id() Exception:')
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(traceback.extract_tb(clt_error_traceback)))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
        error_message = response.headers['X-Influx-Error']
    test_class_instance.mylog.info('buckets_util.get_bucket_by_id() function is done')
    test_class_instance.mylog.info('')
    return {'status':response.status_code, 'bucket_id':requested_bucket_id, 'bucket_name':requested_bucket_name,
            'org_id':org_id, 'org':org_name, 'every_seconds':retention_period, 'error_message':error_message}


# Get the list of the buckets that belong to the specific organization or that belong to all of the organizations
def get_all_buckets(test_class_instance, url, org=None):
    """
    Gets all of the created buckets for a specific organization or all of the organizations.
    :param test_class_instance: instance of the test class
    :param url: gateway url,for example: http://localhost:9999
    :param org: organization name we want to get all of the buckets, If org is not specified, then get all of the
                existing buckets for all of the existing organizations
    :return: status code, error and list of all of the bucket's dictionaries:
    """
    test_class_instance.mylog.info('buckets_util.get_all_buckets() function is being called')
    test_class_instance.mylog.info('-------------------------------------------------------')
    test_class_instance.mylog.info('')
    list_of_buckets = []
    error_message = ''
    if org:
        get_all_buckets_per_org_param = {'org': '%s' % org}
        response = test_class_instance.rl.get(base_url=url, path=BUCKETS_URL, params=get_all_buckets_per_org_param)
    else:
        response = test_class_instance.rl.get(base_url=url, path=BUCKETS_URL)
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
            test_class_instance.mylog.info('buckets_util.get_all_buckets() LIST OF BUCKETS=' +
                                           str(list_of_buckets))
        else:
            error_message = response.headers['X-Influx-Error']
            test_class_instance.mylog.info('buckets_util.get_all_buckets() ERROR=' + error_message)
    except:
        test_class_instance.mylog.info('buckets_util.get_all_buckets() Exception:')
        # get an error from the header
        error_message = response.headers['X-Influx-Error']
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(traceback.extract_tb(clt_error_traceback)))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
        error_message = response.headers['X-Influx-Error']
    test_class_instance.mylog.info('buckets_util.get_all_buckets() function is done')
    test_class_instance.mylog.info('')
    return response.status_code, error_message, list_of_buckets


# Get count of all of the existing buckets
def get_count_of_buckets(test_class_instance, list_of_buckets):
    """
    get_count_of_buckets() function returns the count of buckets
    :param test_class_instance: instance of the test class
    :param list_of_buckets: list of buckets that is returned by get_all_buckets() function
    :return: count of buckets
    """
    test_class_instance.mylog.info('buckets_util.get_count_of_buckets() function is being called')
    test_class_instance.mylog.info('------------------------------------------------------------')
    test_class_instance.mylog.info('')
    count = len(list_of_buckets)
    test_class_instance.mylog.info('buckets_util.get_count_of_buckets() : COUNT=' + str(count))
    return count


# Find a bucket in the list of buckets
def find_bucket_by_name(test_class_instance, list_of_buckets, bucket_name, org_name):
    """
    find_bucket_by_name() function return true if bucket is found in the list of buckets
    :param test_class_instance: instance of the test class
    :param list_of_buckets: list of buckets that is returned by get_all_buckets() function
    :param bucket_name: name of the bucket we are looking for
    :param org_name: name of the organization this bucket belongs to
    :return: true/false
    """
    success = False
    test_class_instance.mylog.info('buckets_util.find_bucket_by_name_by_org() function is being called')
    test_class_instance.mylog.info('------------------------------------------------------------------')
    test_class_instance.mylog.info('')
    for buckets_info in list_of_buckets:
        test_class_instance.mylog.info('buckets_util.find_bucket_by_name_by_org() '
                                       'Finding Bucket with \'%s\' name and Org \'%s\' in %s' %
                                       (bucket_name, org_name, str(buckets_info)))
        if buckets_info['organization'] == org_name and buckets_info['name'] == bucket_name:
            success = True
            break
    return success
