import sys
import traceback
from influxdb import exceptions as e
from influxdb import InfluxDBClient


################################################### influxDBClient #####################################################

def create_user(test_class_instance, client, username, password, admin):
    '''
    :param test_class_instance:
    :param client:
    :param username:
    :param password:
    :param admin:
    :return:
    '''
    success=False
    error_message=''
    try:
        test_class_instance.mylog.info('users_util.create_user() - '
                                       'Creating User %s:%s Admin %s' % (username, password, admin))
        client.create_user(username, password, admin)
        client.close()
        success=True
    except:
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('InfluxDBClientError:' + str(clt_error_message))
        test_class_instance.mylog.info('InfluxDBClientError:' + str(traceback.extract_tb(clt_error_traceback)))
        error_message = str(clt_error_message)
        if client is not None:
            client.close()
    return (success, error_message)

def delete_user(test_class_instance, client, username):
    '''
    :param test_class_instance:
    :param client:
    :param username:
    :param password:
    :param admin:
    :return:
    '''
    success=False
    error_message=''
    try:
        test_class_instance.mylog.info('users_util.delete_user() - '
                                       'Deleting User %s' % (username))
        client.drop_user(username)
        client.close()
        success=True
    except:
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('InfluxDBClientError:' + str(clt_error_message))
        test_class_instance.mylog.info('InfluxDBClientError:' + str(traceback.extract_tb(clt_error_traceback)))
        error_message = str(clt_error_message)
        if client is not None:
            client.close()
    return (success, error_message)

def grant_privilege(test_class_instance, client, privilege, database, username):
    '''
    :param test_class_instance:
    :param client:
    :param provilege:
    :param database:
    :param username:
    :return:
    '''
    success=False
    error_message=''
    try:
        test_class_instance.mylog.info('users_util.grant_privilege() - '
                                       'GRANT %s ON %s TO %s' % (privilege, database, username))
        client.grant_privilege(privilege, database, username)
        client.close()
        success=True
    except:
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('InfluxDBClientError:' + str(clt_error_message))
        test_class_instance.mylog.info('InfluxDBClientError:' + str(traceback.extract_tb(clt_error_traceback)))
        error_message = str(clt_error_message)
        if client is not None:
            client.close()
    return (success, error_message)

def grant_admin_privileges(test_class_instance, client, username):
    '''
    :param test_class_instance:
    :param client:
    :param username:
    :return:
    '''
    success=False
    error_message=''
    try:
        test_class_instance.mylog.info('users_util.grant_admin_privileges() - '
                                       'GRANT ALL PRIVILEGES TO %s' % (username))
        client.grant_admin_privileges(username)
        client.close()
        success=True
    except:
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('InfluxDBClientError:' + str(clt_error_message))
        test_class_instance.mylog.info('InfluxDBClientError:' + str(traceback.extract_tb(clt_error_traceback)))
        error_message = str(clt_error_message)
        if client is not None:
            client.close()
    return (success, error_message)

def revoke_privilege(test_class_instance, client, privilege, database, username):
    '''
    :param test_class_instance:
    :param client:
    :param privilege:
    :param database:
    :param username:
    :return:
    '''
    success=False
    error_message=''
    try:
        test_class_instance.mylog.info('users_util.revoke_privilege() - '
                                       'REVOKE %s ON %s FROM %s' % (privilege, database, username))
        client.revoke_privilege(privilege, database, username)
        client.close()
        success=True
    except:
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('InfluxDBClientError:' + str(clt_error_message))
        test_class_instance.mylog.info('InfluxDBClientError:' + str(traceback.extract_tb(clt_error_traceback)))
        error_message = str(clt_error_message)
        if client is not None:
            client.close()
    return (success, error_message)

def revoke_admin_privileges(test_class_instance, client, username):
    '''
    :param test_class_instance:
    :param client:
    :param username:
    :return:
    '''
    success=False
    error_message=''
    try:
        test_class_instance.mylog.info('users_util.revoke_admin_privileges() - '
                                       'REVOKE ALL PRIVILEGES FROM %s' % (username))
        client.revoke_admin_privileges(username)
        client.close()
        success=True
    except:
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('InfluxDBClientError:' + str(clt_error_message))
        test_class_instance.mylog.info('InfluxDBClientError:' + str(traceback.extract_tb(clt_error_traceback)))
        error_message = str(clt_error_message)
        if client is not None:
            client.close()
    return (success, error_message)

def set_user_password(test_class_instance, client, username, password):
    '''
    :param test_class_instance:
    :param client:
    :param user:
    :param password:
    :return:
    '''
    success=False
    error_message=''
    try:
        test_class_instance.mylog.info('users_util.set_user_pasword() - '
                                       'SET PASSWORD FOR %s = %s' % (username, password))
        client.set_user_password(username, password)
        client.close()
        success=True
    except:
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('InfluxDBClientError:' + str(clt_error_message))
        test_class_instance.mylog.info('InfluxDBClientError:' + str(traceback.extract_tb(clt_error_traceback)))
        error_message = str(clt_error_message)
        if client is not None:
            client.close()
    return (success, error_message)

def show_users(test_class_instance, client):
    '''
    :param test_class_instance:
    :param client:
    :return:
    '''
    success=False
    users=[]
    try:
        test_class_instance.mylog.info('users_util.show_users() - SHOW USERS')
        users=client.get_list_users()
        client.close()
        success=True
    except:
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('InfluxDBError:' + str(clt_error_message))
        test_class_instance.mylog.info('InfluxDBError:' + str(traceback.extract_tb(clt_error_traceback)))
        if client is not None:
            client.close()
    return (success, users)

def show_grants(test_class_instance, client, username):
    '''
    :param test_class_instance:
    :param client:
    :param username:
    :return:
    '''
    success=False
    user_grants=[]
    try:
        test_class_instance.mylog.info('users_util.show_grabs() - SHOW GRANTS FOR %s' + username)
        user_grants=client.get_list_privileges(username)
        client.close()
        success=True
    except:
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('InfluxDBError:' + str(clt_error_message))
        test_class_instance.mylog.info('InfluxDBError:' + str(traceback.extract_tb(clt_error_traceback)))
        if client is not None:
            client.close()
    return (success, user_grants)