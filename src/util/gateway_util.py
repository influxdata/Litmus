
import sys
import traceback

ORG_URL='/v1/orgs'

def create_organization(test_class_instance, url, org_name):
    '''
    :param test_class_instance:
    :param url:
    :param org_name:
    :return: status_code, org_id, created_org_name
    '''
    test_class_instance.mylog.info('gateway_util.create_organization() function is being called')
    test_class_instance.mylog.info('-----------------------------------------------------------')
    test_class_instance.mylog.info('')
    test_class_instance.mylog.info('gateway_util.create_organization() '
                                   'Creating Organization with \'%s\' name' % org_name)
    data='{"name":"%s"}' % org_name
    org_id, created_org_name=None,None
    response=test_class_instance.rl.post(base_url=url, path=ORG_URL, data=data)
    try:
        org_id=response.json().get('id')
        created_org_name=response.json().get('name')
        if org_id is not None and created_org_name is not None:
            test_class_instance.mylog.info('gateway_util.create_organization() ORG_ID=' + str(org_id))
            test_class_instance.mylog.info('gateway_util.create_organization() ORG_NAME=' + str(created_org_name))
        else:
            test_class_instance.mylog.info('gateway_util.create_organization() ORG_ID=' + str(org_id))
            test_class_instance.mylog.info('gateway_util.create_organization() ORG_NAME=' + str(created_org_name))
            test_class_instance.mylog.info('gateway_util.create_organization() ERROR=' + response.json()['message'])
    except:
        test_class_instance.mylog.info('gateway_util.create_organization() Exception:')
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(traceback.extract_tb(clt_error_traceback)))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
    test_class_instance.mylog.info('gateway_util.create_organization() function is done')
    test_class_instance.mylog.info('')
    return response.status_code, org_id, created_org_name


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
    updated_org_name, new_org_id=None,None
    response=test_class_instance.rl.patch(base_url=url, path=ORG_URL+'/'+ str(org_id), data=data)
    try:
        new_org_id=response.json().get('id')
        updated_org_name=response.json().get('name')
        if org_id is not None and updated_org_name is not None:
            test_class_instance.mylog.info('gateway_util.create_organization() ORG_ID=' + str(new_org_id))
            test_class_instance.mylog.info('gateway_util.create_organization() ORG_NAME=' + str(updated_org_name))
        else:
            test_class_instance.mylog.info('gateway_util.create_organization() ORG_ID=' + str(new_org_id))
            test_class_instance.mylog.info('gateway_util.create_organization() ORG_NAME=' + str(updated_org_name))
            test_class_instance.mylog.info('gateway_util.create_organization() ERROR=' + response.json()['message'])
    except:
        test_class_instance.mylog.info('gateway_util.update_organization() Exception:')
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(traceback.extract_tb(clt_error_traceback)))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
    test_class_instance.mylog.info('gateway_util.update_organization() function is done')
    test_class_instance.mylog.info('')
    return (response.status_code, new_org_id, updated_org_name)

