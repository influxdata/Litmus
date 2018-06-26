
import sys
import traceback
import ast
from src.util import litmus_utils

#============================================= ORGANIZATIONS =====================================================

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
            test_class_instance.mylog.info('gateway_util.create_organization() '
                                           'REQUESTED_ORG_ID AND REQUESTED_ORG_NAME ARE NONE')
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
            test_class_instance.mylog.info('gateway_util.create_organization() '
                                           'REQUESTED_ORG_ID AND REQUESTED_ORG_NAME ARE NONE')
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

def delete_organization(test_class_instance, url, org_id_to_delete):
    '''
    :param test_class_instance:
    :param url:
    :param org_id_to_delete:
    :return:
    '''
    test_class_instance.mylog.info('gateway_util.delete_organization() function is being called')
    test_class_instance.mylog.info('-----------------------------------------------------------')
    test_class_instance.mylog.info('')
    test_class_instance.mylog.info('gateway_util.delete_organization() '
                                   'Deleting Organization with \'%s\' id' % org_id_to_delete)
    response=test_class_instance.rl.delete(base_url=url, path=ORG_URL + '/' + str(org_id_to_delete))
    try:
        # for now assuming that delete returns id and org name as in `influx` tool
        deleted_org_id=response.json().get('id')
        deleted_org_name=response.json().get('name')
        if deleted_org_id is not None and deleted_org_name is not None:
            test_class_instance.mylog.info('gateway_util.delete_organization() ORG_ID=' + str(deleted_org_id))
            test_class_instance.mylog.info('gateway_util.delete_organization() ORG_NAME=' + str(deleted_org_name))
        else:
            test_class_instance.mylog.info('gateway_util.delete_organization() '
                                           'REQUESTED_ORG_ID AND REQUESTED_ORG_NAME ARE NONE')
            test_class_instance.mylog.info('gateway_util.create_organization() ERROR=' + response.json()['message'])
    except:
        test_class_instance.mylog.info('gateway_util.create_organization() Exception:')
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(traceback.extract_tb(clt_error_traceback)))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
    test_class_instance.mylog.info('gateway_util.create_organization() function is done')
    test_class_instance.mylog.info('')
    return response.status_code, deleted_org_id, deleted_org_name

def get_organization(test_class_instance, url, org_id):
    '''
    :param test_class_instance:
    :param url:
    :param org_id:
    :return: status_code, org_id, created_org_name
    '''
    test_class_instance.mylog.info('gateway_util.get_organization() function is being called')
    test_class_instance.mylog.info('-----------------------------------------------------------')
    test_class_instance.mylog.info('')
    test_class_instance.mylog.info('gateway_util.get_organization() '
                                   'Getting Organization with \'%s\' id' % org_id)
    requested_org_id, requested_org_name=None,None
    response=test_class_instance.rl.get(base_url=url, path=ORG_URL+'/'+str(org_id))
    try:
        requested_org_id=response.json().get('id')
        requested_org_name=response.json().get('name')
        if requested_org_id is not None and requested_org_name is not None:
            test_class_instance.mylog.info('gateway_util.create_organization() REQUESTED_ORG_ID=' +
                                           str(requested_org_id))
            test_class_instance.mylog.info('gateway_util.create_organization() REQUESTED_ORG_NAME=' +
                                           str(requested_org_name))
        else:
            test_class_instance.mylog.info('gateway_util.create_organization() '
                                           'REQUESTED_ORG_ID AND REQUESTED_ORG_NAME ARE NONE')
            test_class_instance.mylog.info('gateway_util.create_organization() ERROR=' + response.json()['message'])
    except:
        test_class_instance.mylog.info('gateway_util.get_organization() Exception:')
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(traceback.extract_tb(clt_error_traceback)))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
    test_class_instance.mylog.info('gateway_util.get_organization() function is done')
    test_class_instance.mylog.info('')
    return response.status_code, requested_org_id, requested_org_name

def get_all_organizations(test_class_instance, url):
    '''
    :param test_class_instance:
    :param url:
    :return: status_code, org_id, created_org_name
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
            test_class_instance.mylog.info('gateway_util.create_organization() ERROR=' + response.json()['message'])
    except:
        test_class_instance.mylog.info('gateway_util.get_organization() Exception:')
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


#============================================= ETCD =================================================

def verify_org_etcd(test_class_instance, etcd, org_id, org_name):
    '''
    :param test_class_instance: instance of the test clas, i.e. self
    :param etcd: url of the etcd service
    :param org_id: organization id
    :param org_name: organization name
    :return: does not return anything
    '''
    cmd='ETCDCTL_API=3 /usr/local/bin/etcdctl --endpoints %s get --prefix "Organizationv1/%s" --print-value-only'\
        % (etcd, org_id)
    out=litmus_utils.execCmd(test_class_instance, cmd, status='OUT_STATUS')
    actual_org_id=ast.literal_eval(out[0]).get('id')
    test_class_instance.mylog.info('Assert expected org_id ' + str(org_id) + ' equals to actual org_id '
                                   + str(actual_org_id))
    assert org_id == actual_org_id, test_class_instance.mylog.info('Expected org id is not equal to actual org id')
    actual_org_name = ast.literal_eval(out[0]).get('name')
    test_class_instance.mylog.info('Assert expected org_name ' + str(org_name) + ' equals actual to org_name '
                           + str(actual_org_name))
    assert org_name == actual_org_name, \
        test_class_instance.mylog.info('Expected org name is not equal to actual org name')
