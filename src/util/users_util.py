import src.util.sources_util as su
from influxdb.resultset import ResultSet
from influxdb import exceptions as e

def create_user(test_class_instance, client, user_name, password, admin):
    '''
    :param test_class_instance:
    :param client:
    :param user_name:
    :param password:
    :param admin:
    :return:
    '''
    success = False
    try:
        test_class_instance.mylog.info('users_util.create_user() - '
                                       'Creating User %s:%s Admin %s' % (user_name, password, admin))
        client.create_user(user_name, password, admin)
        client.close()
        success = True
    except e.InfluxDBServerError:
        test_class_instance.mylog.info('InfluxDBServerError:' + str(e.InfluxDBServerError.message))
        if client is not None:
            client.close()
    except e.InfluxDBClientError:
        test_class_instance.mylog.info('InfluxDBClientError:' + str(e.InfluxDBClientError.message))
        if client is not None:
            client.close()
    return success
