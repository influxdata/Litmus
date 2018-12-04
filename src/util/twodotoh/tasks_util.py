import sys
import traceback
import json


TASKS_URL = '/api/v2/tasks'

# do not use every and cron in the request body: https://github.com/influxdata/idpe/issues/1995
# Create a new task
def create_task(test_class_instance, url, org_id, task_description, token, status='active', flux=None, task_name=None,
                every=None, cron=None, delay=None, query=None, owners=None):
    """
    Wrapper function to create a new task, i.e. Flux script that runs in background
    :param test_class_instance: instance of the test class, i.e. self.
    :param url: (str) Gateway URL, e.g. http://localhost:9999.
    :param org_id: (str) ID of the organization that owns this task. (request body)
    :param task_description: (str) description of the task (request body)
    :param token: (str) token than defines ability to create, delete and modify tasks. (request body)
    :param status: (str) current status of the task (active/inactive), default is active. (request body)
    :param flux: (str) The Flux script to run for the task. (request body)
    :param task_name: (str) name of the task. (used in Flux script)
    :param every: (duration) this task should be run at this interval. minimum interval is 1s, max interval is 24h.
    :param cron: (str) A task repetition schedule, more sophisticated way to schedule. every and cron are mutually exclusive.
    :param delay: (duration) delaying scheduling the task. (Flux script)
    :param query: (str) flux query (used in flux script)
    :param owners: ???
    :return: dictionary: 'status':response_create.status_code, 'task_id':task_id, 'org_id':org_id,
                        'task_name':task_name, 'task_status':task_status, 'task_owner':task_owners, 'flux_script':flux,
                        'every':every, 'cron':cron
    """
    test_class_instance.mylog.info('tasks_util.create_task() function is being called')
    test_class_instance.mylog.info('-------------------------------------------------\n')
    test_class_instance.mylog.info('tasks_util.create_task() - Creating Task with:\n'
                                   'Organization ID : \'%s\'\n'
                                   'Task Description : \'%s\'\n'
                                   'Task Name : \'%s\'\n'
                                   'Flux Script: \'%s\'\n'
                                   'Status : \'%s\'\n'
                                   'every: \'%s\'\n'
                                   'Token : \'%s\'\n'
                                   'Cron : \'%s\'\n'
                                   'Delay : \'%s\'\n'
                                   'Query : \'%s\'\n'
                                   'Owners : \'%s\''\
                                    % (org_id, task_description, task_name, flux, status, every, token, cron, delay,
                                       query, owners))
    flux_script = ''

    headers = {"Authorization": "Token %s" % token}
    # check if flux param is not None, then it should be used as a value for a flux element in the request body
    # otherwise build up a flux script based on every, cron, delay and name
    if flux:
        data = '{"organizationID":"%s", "name":"%s", "flux":%s, "status":"%s"}' \
               % (org_id, task_description, json.dumps(flux), status)
    else:
        # build flux script
        if every and not cron:
                if delay:
                    flux_script = 'option task = (name:"%s", every:%s, delay:%s} %s' \
                                  % (task_name, every, delay, query)
                else:
                    flux_script = 'option task = {name:"%s", every:%s} %s'\
                                  % (task_name, every, query)
        elif cron and not every:
                if delay:
                    flux_script = 'option task = {name:"%s", cron:%s, delay:%s} %s' \
                                  % (task_name, cron, delay, query)
                else:
                    flux_script = 'option task = {name:"%s", cron:%s} %s' % (task_name, cron, query)
        test_class_instance.mylog.info('tasks_util.create_task() : flux_script = \'%s\'' % flux_script)

        data = '{"organizationID":"%s", "name":"%s", "status":"%s", "flux":%s}' \
               % (org_id, task_description, status,json.dumps(flux_script))
    test_class_instance.mylog.info('tasks_util.create_task() : Request Body - \'%s\'' % data)
    task_id, org_id, task_description, task_status, task_owners, every, cron, flux \
        = None, None, None, None, None, None, None, None
    response_create = test_class_instance.rl.post(base_url=url, path=TASKS_URL, data=data, headers=headers)
    # response object returns:
    # {u'task':
    #   {   u'status': u'',
    #       u'name': u'task_request_body',
    #       u'organizationId': u'02f0e76fe2c69000',
    #       u'flux': u'option task  = {name:"task_1", every:20m}',
    #       u'every': u'20m0s',
    #       u'owner': {u'id': u'02f0e8def7469000', u'name': u''},
    #       u'id': u'02f120ab7352c000'
    #   },
    #   u'links':
    #       {
    #           u'owners': u'/api/v2/tasks/02f120ab7352c000/owners',
    #           u'runs': u'/api/v2/tasks/02f120ab7352c000/runs',
    #           u'members': u'/api/v2/tasks/02f120ab7352c000/members',
    #           u'self': u'/api/v2/tasks/02f120ab7352c000'
    #       }
    # }
    # getting task response object
    response = response_create.json() #.get('task')
    # TODO get the links
    try:
        task_id = response.get('id')
        org_id = response.get('organizationId')
        task_description = response.get('name')
        task_status = response.get('status')
        task_owners = response.get('owner')
        flux = response.get('flux')
        every = response.get('every')
        cron = response.get('cron')
        if task_id and org_id and task_description and flux and task_status:
            test_class_instance.mylog.info('tasks_util.create_task() : TASK_ID=' + str(task_id))
            test_class_instance.mylog.info('tasks_util.create_task() : ORG_ID=' + str(org_id))
            test_class_instance.mylog.info('tasks_util.create_task() : TASK_DESCRIPTION=' + str(task_description))
            test_class_instance.mylog.info('tasks_util.create_task() : TASK_STATUS=' + str(task_status))
            test_class_instance.mylog.info('tasks_util.create_task() : TASK_OWNER=' + str(task_owners))
            test_class_instance.mylog.info('tasks_util.create_task() : FLUX_SCRIPT=' + str(flux))
            test_class_instance.mylog.info('tasks_util.create_task() : EVERY=' + str(every))
            test_class_instance.mylog.info('tasks_util.create_task() : CRON=' + str(cron))
        else:
            test_class_instance.mylog.info('tasks_util.create_task() : One of the required params is None: '
                                           'TASK_ID=\'%s\', ORG_ID=\'%s\', TASK_DESCRIPTION=\'%s\', FLUX=\'%s\''
                                           % (task_id, org_id, task_description, flux))
            #error_message = response.json()['message']
            error_message = response_create.headers['X-Influx-Error']
            test_class_instance.mylog.info('tasks_util.create_task() ERROR=' + error_message)
    except:
        test_class_instance.mylog.info('tasks_util.create_task() Exception:')
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(traceback.extract_tb(clt_error_traceback)))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
    test_class_instance.mylog.info('tasks_util.create_task() function is done')
    test_class_instance.mylog.info('')
    return {'status':response_create.status_code, 'task_id':task_id, 'org_id':org_id,
            'task_description':task_description, 'task_status':task_status, 'task_owner':task_owners,
            'flux_script':flux, 'every':every, 'cron':cron}


# Retrieve the list of run records for a particular task
def get_run_records_for_task(test_class_instance, url, org_id, task_id, token, after=None, limit=20, afterTime=None,
                             beforeTime=None):
    """
    Function to retrieve the run records for a particular task
    :param test_class_instance: instance of the test class, i.e. self.
    :param url: (str) Gateway URL, e.g. http://localhost:9999.
    :param org_id: (str) ID of the organization that owns this task. (param)
    :param task_id: (str) id of the task that runs are being retrieved for.
    :param token: (str) token than defines ability to create, delete and modify tasks.
    :param after: (str) return run records after run id = after, default is None (return all runs) (param)
    :param limit: (int) the number of runs to return, default is 20 (param)
    :param afterTime: (str) filter runs to those scheduled after this time, RFC3339, default is None (return all runs)
    :param beforeTime: (str) filter runs to those scheduled before this time, RFC3339, default is None (return all runs)
    :return: a list of task runs, where task run is a dictionary
    """
    test_class_instance.mylog.info('tasks_util.get_run_records_for_task() function is being called')
    test_class_instance.mylog.info('--------------------------------------------------------------\n')
    # build PATH:
    path = TASKS_URL + '/' + task_id + '/runs'
    test_class_instance.mylog.info('tasks_util.get_run_records_for_task() : Getting runs for :\n'
                                   'Organization ID : \'%s\'\n'
                                   'Task ID : \'%s\'\n'
                                   'Token : \'%s\'\n') % (org_id, task_id, token, url)
    # define headers:
    headers={'Authorization': 'Token %s' % token}
    # define params
    params = {}
    params['orgID'] = '%s' % org_id
    params['limit'] = '%s' % limit
    if after: params['after'] = '%s' % after
    if afterTime: params['afterTime'] = '%s' % afterTime
    if beforeTime: params['beforeTime'] = '%s' % beforeTime

    response = test_class_instance.rl.post(base_url=url, path=path, params=params, headers=headers)
    # TODO: get u'links': {u'self': u'/api/v2/tasks/030324ce2aac1001/runs', u'task': u'/api/v2/tasks/030324ce2aac1001'}
    # get runs response object
    run_records = {}
    runs = response.json().get('runs')
    """
    {   u'status': u'success', u'scheduledFor': u'2018-11-28T23:12:42Z', u'finishedAt':
        u'2018-11-28T23:12:42.561564608Z', u'taskId': u'030324ce2aac1000', u'startedAt':
        u'2018-11-28T23:12:42.357141034Z', u'id': u'0303257dac6c1000', u'log': u''
    }
    {   u'status': u'success', u'scheduledFor': u'2018-11-28T23:13:12Z', u'finishedAt':
        u'2018-11-28T23:13:12.561214894Z', u'taskId': u'030324ce2aac1000', u'startedAt':
        u'2018-11-28T23:13:12.357623097Z', u'id': u'0303259af96c1000', u'log': u''
    }
    """




