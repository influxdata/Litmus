import sys
import traceback

ORG_URL = '/api/v2/orgs'


# Create Organization
def create_organization(test_class_instance, url, org_name, status='active'):
    """
    create_organization() function creates an organization
    :param test_class_instance: instance of the test class
    :param url: gateway url,for example: http://localhost:9999
    :param org_name: name of the organization to create
    :param status: status of the org, default is active, available values are active/inactive
    :return: dictionary
    """
    test_class_instance.mylog.info('org_util.create_organization() function is being called')
    test_class_instance.mylog.info('-------------------------------------------------------')
    test_class_instance.mylog.info('')

    test_class_instance.mylog.info('org_util.create_organization() Creating Organization with \'%s\' name '
                                   'and status \'%s\'' % (org_name, status))
    data = '{"name":"%s","status:":"%s"}' % (org_name, status)
    org_id, created_org_name, error_message, tasks, log, dashboards, members, buckets \
        = None, None, None, None, None, None, None, None
    response = test_class_instance.rl.post(base_url=url, path=ORG_URL, data=data)
    """
    {   u'id': u'02e54dc99c0dc000', 
        u'links': 
           {u'tasks': u'/api/v2/tasks?org=test_org_1', 
            u'log': u'/api/v2/orgs/02e54dc99c0dc000/log', 
            u'self': u'/api/v2/orgs/02e54dc99c0dc000', 
            u'dashboards': u'/api/v2/dashboards?org=test_org_1', 
            u'members': u'/api/v2/orgs/02e54dc99c0dc000/members', 
            u'buckets': u'/api/v2/buckets?org=test_org_1'}, 
        u'name': u'test_org_1'}

    """
    try:
        org_id = response.json().get('id')
        created_org_name = response.json().get('name')
        tasks = response.json().get('links').get('tasks')
        log = response.json().get('links').get('log')
        dashboards = response.json().get('links').get('dashboards')
        members = response.json().get('links').get('members')
        buckets = response.json().get('links').get('buckets')
        if org_id is not None and created_org_name is not None:
            test_class_instance.mylog.info('org_util.create_organization() ORG_ID=' + str(org_id))
            test_class_instance.mylog.info('org_util.create_organization() ORG_NAME=' + str(created_org_name))
            test_class_instance.mylog.info('org_util.create_organization() TASKS_LINK=' + str(tasks))
            test_class_instance.mylog.info('org_util.create_organization() LOG_LINK=' + str(log))
            test_class_instance.mylog.info('org_util.create_organization() DASHBOARD_LINK=' + str(dashboards))
            test_class_instance.mylog.info('org_util.create_organization() MEMBERS_LINK=' + str(members))
            test_class_instance.mylog.info('org_util.create_organization() BUCKETS_LINK=' + str(buckets))
        else:
            test_class_instance.mylog.info('org_util.create_organization() '
                                           'REQUESTED_ORG_ID AND REQUESTED_ORG_NAME ARE NONE')
            error_message = response.headers['X-Influx-Error']
            test_class_instance.mylog.info('org_util.create_organization() ERROR=' + error_message)
    except:
        test_class_instance.mylog.info('org_util.create_organization() Exception:')
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(traceback.extract_tb(clt_error_traceback)))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
        error_message = response.headers['X-Influx-Error']
        test_class_instance.mylog.info('org_util.create_organization() ERROR=' + error_message)
    test_class_instance.mylog.info('org_util.create_organization() function is done')
    test_class_instance.mylog.info('')
    return {'status':response.status_code, 'org_id':org_id, 'org_name':created_org_name, 'tasks_link':tasks,
            'log_link':log, 'dashboards_link':dashboards, 'members_link': members, 'buckets_link':buckets,
            'error_message':error_message}


# Update Organization
def update_organization(test_class_instance, url, org_id, new_org_name, status='active'):
    """
    update_organization() function updates the name of the organization
    :param test_class_instance: instance of the test class
    :param url: gateway url,for example: http://localhost:9999
    :param org_id: id of the organization to update
    :param new_org_name: new organization name
    :param status: status of the org, default is active, availbale values are active/inactive
    :return: dictionary
    """
    test_class_instance.mylog.info('org_util.update_organization() function is being called')
    test_class_instance.mylog.info('-------------------------------------------------------')
    test_class_instance.mylog.info('')
    data = '{"name":"%s", "status":"%s"}' % (new_org_name, status)
    updated_org_name, new_org_id, error_message, tasks, log, dashboards, members, buckets \
        = None, None, None, None, None, None, None, None
    response = test_class_instance.rl.patch(base_url=url, path=ORG_URL + '/' + str(org_id), data=data)
    try:
        new_org_id = response.json().get('id')
        updated_org_name = response.json().get('name')
        tasks = response.json().get('links').get('tasks')
        log = response.json().get('links').get('log')
        dashboards = response.json().get('links').get('dashboards')
        members = response.json().get('links').get('members')
        buckets = response.json().get('links').get('buckets')
        if org_id is not None and updated_org_name is not None:
            test_class_instance.mylog.info('org_util.update_organization() ORG_ID=' + str(new_org_id))
            test_class_instance.mylog.info('org_util.update_organization() ORG_NAME=' + str(updated_org_name))
            test_class_instance.mylog.info('org_util.update_organization() TASKS_LINK=' + str(tasks))
            test_class_instance.mylog.info('org_util.update_organization() LOG_LINK=' + str(log))
            test_class_instance.mylog.info('org_util.update_organization() DASHBOARD_LINK=' + str(dashboards))
            test_class_instance.mylog.info('org_util.update_organization() MEMBERS_LINK=' + str(members))
            test_class_instance.mylog.info('org_util.update_organization() BUCKETS_LINK=' + str(buckets))
        else:
            test_class_instance.mylog.info('org_util.update_organization() '
                                           'REQUESTED_ORG_ID AND REQUESTED_ORG_NAME ARE NONE')
            error_message = response.headers['X-Influx-Error']
            test_class_instance.mylog.info('gateway_util.create_organization() ERROR=' + error_message)
    except:
        test_class_instance.mylog.info('org_util.update_organization() Exception:')
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(traceback.extract_tb(clt_error_traceback)))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
        error_message = response.headers['X-Influx-Error']
    test_class_instance.mylog.info('org_util.update_organization() function is done')
    test_class_instance.mylog.info('')
    return {'status':response.status_code, 'updated_org_id':new_org_id, 'updated_org_name':updated_org_name,
            'tasks_link':tasks, 'log_link':log, 'dashboards_link':dashboards, 'members_link': members,
            'buckets_link':buckets, 'error_message':error_message}


# Get Organization Info by Organization ID
def get_organization_by_id(test_class_instance, url, org_id):
    """
    get_organization_by_id() function return organization info based on the organization id
    :param test_class_instance: instance of the test class
    :param url: gateway url,for example: http://localhost:9999
    :param org_id: id of the organization to get
    :return: dictionary
    """
    test_class_instance.mylog.info('org_util.get_organization_by_id() function is being called')
    test_class_instance.mylog.info('----------------------------------------------------------')
    test_class_instance.mylog.info('')
    test_class_instance.mylog.info('org_util.get_organization_by_id() '
                                   'Getting Organization with \'%s\' id' % org_id)
    requested_org_id, requested_org_name, error_message, tasks, log, dashboards, members, buckets \
        = None, None, None, None, None, None, None, None
    response = test_class_instance.rl.get(base_url=url, path=ORG_URL + '/' + str(org_id))
    try:
        requested_org_id = response.json().get('id')
        requested_org_name = response.json().get('name')
        tasks = response.json().get('links').get('tasks')
        log = response.json().get('links').get('log')
        dashboards = response.json().get('links').get('dashboards')
        members = response.json().get('links').get('members')
        buckets = response.json().get('links').get('buckets')
        if requested_org_id is not None and requested_org_name is not None:
            test_class_instance.mylog.info('org_util.get_organization_by_id() REQUESTED_ORG_ID=' +
                                           str(requested_org_id))
            test_class_instance.mylog.info('org_util.get_organization_by_id() REQUESTED_ORG_NAME=' +
                                           str(requested_org_name))
            test_class_instance.mylog.info('org_util.get_organization_by_id() TASKS_LINK=' + str(tasks))
            test_class_instance.mylog.info('org_util.get_organization_by_id() LOG_LINK=' + str(log))
            test_class_instance.mylog.info('org_util.get_organization_by_id() DASHBOARD_LINK=' + str(dashboards))
            test_class_instance.mylog.info('org_util.get_organization_by_id() MEMBERS_LINK=' + str(members))
            test_class_instance.mylog.info('org_util.get_organization_by_id() BUCKETS_LINK=' + str(buckets))
        else:
            test_class_instance.mylog.info('org_util.get_organization_by_id() '
                                           'REQUESTED_ORG_ID AND REQUESTED_ORG_NAME ARE NONE')
            error_message = response.headers['X-Influx-Error']
            test_class_instance.mylog.info('org_util.get_organization_by_id() ERROR=' + error_message)
    except:
        test_class_instance.mylog.info('org_util.get_organization_by_id() Exception:')
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(traceback.extract_tb(clt_error_traceback)))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
        error_message = response.headers['X-Influx-Error']
    test_class_instance.mylog.info('org_util.get_organization_by_id() function is done')
    test_class_instance.mylog.info('')
    return {'status':response.status_code, 'requested_org_id':requested_org_id, 'requested_org_name':requested_org_name,
            'tasks_link':tasks, 'log_link':log, 'dashboards_link':dashboards, 'members_link': members,
            'buckets_link':buckets, 'error_message':error_message}


# Return info of all of the created organization
def get_all_organizations(test_class_instance, url):
    """
    get_all_organizations() function returns all of the created organizations.
    :param test_class_instance: instance of the test class
    :param url: gateway url,for example: http://localhost:9999
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
    test_class_instance.mylog.info('org_util.get_all_organizations() function is being called')
    test_class_instance.mylog.info('---------------------------------------------------------')
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
            test_class_instance.mylog.info('org_util.get_all_organizations() LIST OF ORGANIZATIONS=' +
                                           str(list_of_organizations))
        else:
            test_class_instance.mylog.info('gateway_util.get_all_organizations() ERROR='
                                           + response.headers['X-Influx-Error'])
    except:
        test_class_instance.mylog.info('org_util.get_all_organizations() Exception:')
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(traceback.extract_tb(clt_error_traceback)))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
    test_class_instance.mylog.info('org_util.get_all_organizations() function is done')
    test_class_instance.mylog.info('')
    return response.status_code, list_of_organizations


# Delete organization by org id
def delete_organization(test_class_instance, url, org_id):
    """
    delete_organization() function removes an organization from etcd store, from index/org/id, index/org/name and
    removes the key Organizationv1
    :param test_class_instance: instance of the test class
    :param url: gateway url,for example: http://localhost:9999
    :param org_id: id of the organization to delete
    :return: status_code, org_id, created_org_name, error_message
    """
    test_class_instance.mylog.info('org_util.delete_organization() function is being called')
    test_class_instance.mylog.info('-----------------------------------------------------------')
    test_class_instance.mylog.info('')
    test_class_instance.mylog.info('org_util.delete_organization() '
                                   'Deleting Organization with \'%s\' id' % org_id)
    # TODO This error is coming from headers,
    # TODO I would need to handle it differently when both JSON error and headers errors are in place.
    error = ''
    if org_id == '':  # org id is missing:
        path = ORG_URL + '/'
    else:
        path = ORG_URL + '/' + org_id
    response = test_class_instance.rl.delete(base_url=url, path=path)
    # TODO 404 will be returned if org id is missing.
    if response.status_code in range(405, 501):
        error = response.headers['X-Influx-Error']
    if error != '':
        test_class_instance.mylog.info('org_util.delete_organization() ERROR: ' + error)
    test_class_instance.mylog.info('org_util.delete_organization() function is done')
    test_class_instance.mylog.info('')
    return response.status_code, error


# Finding an organization in the list of organizations using org name
def find_org_by_name(test_class_instance, org_name_to_find, list_of_organizations):
    """
    Helper function: find_org_by_name() finds organization by name in the list of all organizations
    :param test_class_instance: instance of the test class
    :param org_name_to_find: name of the organization to find
    :param list_of_organizations: output of get_all_organizations() function
    :return: org name, id
    """
    test_class_instance.mylog.info('org_util.find_org_by_name() function is being called')
    test_class_instance.mylog.info('----------------------------------------------------')
    test_class_instance.mylog.info('')
    test_class_instance.mylog.info('org_util.find_org_by_name() '
                                   'Finding Organization with \'%s\' name' % org_name_to_find)
    # in case the result list is empty we need to handle IndexError exception (list index out of range)
    try:
        result = filter(lambda org: org['name'] == org_name_to_find, list_of_organizations)
        orgname = result[0].get('name')
        test_class_instance.mylog.info('org_util.find_org_by_name() : ORG_NAME=' + str(orgname))
        orgid = result[0].get('id')
        test_class_instance.mylog.info('org_util.find_org_by_name() : ORG_ID=' + str(orgid))
    except IndexError as error:
        test_class_instance.mylog.info('org_util.find_org_by_name() : Exception = ' + str(error))
        orgname, orgid = None, None
    return orgname, orgid


# Finding an organization in the list of organizations using org id
def find_org_by_id(test_class_instance, org_id_to_find, list_of_organizations):
    """
    Helper function: find_org_by_id() finds organization by id in the list of all organizations.
    :param test_class_instance:instance of the test class
    :param org_id_to_find: id of the organization to find
    :param list_of_organizations: output of get_all_organizations() function
    :return: org name, id
    """
    test_class_instance.mylog.info('org_util.find_org_by_id() function is being called')
    test_class_instance.mylog.info('------------------------------------------------------')
    test_class_instance.mylog.info('')
    test_class_instance.mylog.info('org_util.find_org_by_id() '
                                   'Finding Organization with \'%s\' id' % org_id_to_find)
    try:
        result = filter(lambda org: org['id'] == org_id_to_find, list_of_organizations)
        orgname = result[0].get('name')
        test_class_instance.mylog.info('org_util.find_org_by_name() : ORG_NAME=' + str(orgname))
        orgid = result[0].get('id')
        test_class_instance.mylog.info('org_util.find_org_by_name() : ORG_ID=' + str(orgid))
    except IndexError as error:
        test_class_instance.mylog.info('org_util.find_org_by_name() : Exception = ' + str(error))
        orgname, orgid = None, None
    return orgname, orgid


# Returns the count of all of the created organizations.
def get_count_of_orgs(test_class_instance, list_of_organizations):
    """
    Helper function: get_count_of_orgs() returns the count of all created organizations
    :param test_class_instance: instance of the test class
    :param list_of_organizations:output of get_all_organizations() function
    :return: count of organizations
    """
    test_class_instance.mylog.info('org_util.get_count_of_orgs() function is being called')
    test_class_instance.mylog.info('---------------------------------------------------------')
    test_class_instance.mylog.info('')
    count = len(list_of_organizations)
    test_class_instance.mylog.info('org_util.get_count_of_orgs() : COUNT=' + str(count))
    return count
