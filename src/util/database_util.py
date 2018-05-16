
import src.util.sources_util as su
import traceback
import sys
from influxdb.resultset import ResultSet


################################################ using influxDBClient ##################################################

def run_query(test_class_instance, client, query, params=None, epoch=None,
              expected_response_code=200, database=None):
    """
    :param test_class_instance: instance of the test class
    :param client: instance of influxDBClient
    :param query: query string
    :param params(dict):additional parameters for the request, defaults to empty dict
    :param epoch(str): response timestamps ,defaults to None which is RFC3339
                UTC format with nanosecond precision
    :param expected_response_code(int):the expected status code of response,
                defaults to 200
    :param database (str):database to query, defaults to None
    :return: ResultSet of queried data
    """
    result=ResultSet
    success=False
    error=''
    try:
        test_class_instance.mylog.info('database_util.run_query() is called '
                                       'with query=%s, params=%s, epoch=%s, '
                                       'expected_response_code=%d, database=%s'
                                       % (query, params, epoch, expected_response_code,
                                          database))
        result=client.query(query=query, params=params, epoch=epoch,
                            expected_response_code=expected_response_code,
                            database=database)
        client.close()
        success=True
    except:
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('InfluxDBError:' + str(clt_error_message))
        test_class_instance.mylog.info('InfluxDBError:' + str(traceback.extract_tb(clt_error_traceback)))
        if client is not None:
            client.close()
        error=clt_error_message
    return (success, result, error)

def write_points(test_class_instance, client, points, time_precision=None,
                 database=None, retention_policy=None, tags=None):
    """
    Write to multiple time series names.
    It is wrapper to InfluxDBClient.write_points method
    http://influxdb-python.readthedocs.io/en/latest/api-documentation.html
    :param test_class_instance:instance of the test class
    :param client:instance of InfluxDBClient
    :param points: the list of points to be written in the database
                (list of dictionaries, each dictionary represents a point)
    :param time_precision:(str) defaults to None
    :param database:(str) The database to write point to.
    :param retention_policy:retention policy for the points
    :param tags:set of key-value pairs associated with each point
    :return: True - success, False -failure
    """
    return_value=False
    try:
        test_class_instance.mylog.info('database_util.write_points() is called '
                                    'with json=%s, time_precision=%s, database=%s, '
                                    'retention_policy=%s, tags=%s'
                                    % (points, time_precision, database,retention_policy,tags))
        return_value=client.write_points(points=points, time_precision=time_precision,
                                         database=database, retention_policy=retention_policy,
                                         tags=tags)
        client.close()
    except:
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('InfluxDBError:' + str(clt_error_message))
        test_class_instance.mylog.info('InfluxDBError:' + str(traceback.extract_tb(clt_error_traceback)))
        if client is not None:
            client.close()
    return return_value

#-------------------------------------------------- DATABASES ---------------------------------------------------------#
def create_database(test_class_instance, client, db_name):
    '''
    create database using InfluxDBClient
    :param test_class_instance:
    :param host:
    :param port:
    :param user:
    :param password:
    :return:
    '''
    success=False
    error_message=''
    try:
        test_class_instance.mylog.info('database_util.create_database() '
                                       '- Creating database ' + db_name)
        client.create_database(db_name)
        client.close()
        success=True
    except:
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('InfluxDBError:' + str(clt_error_message))
        test_class_instance.mylog.info('InfluxDBError:' + str(traceback.extract_tb(clt_error_traceback)))
        error_message=str(clt_error_message)
        if client is not None:
            client.close()
    test_class_instance.mylog.info('database_util.create_database() success=' + str(success))
    return (success, error_message)

def drop_database(test_class_instance, client, db_name):
    '''
    :param test_class_instance:
    :param client:
    :param db_name:
    :return:
    '''
    success = False
    error_message = ''
    try:
        test_class_instance.mylog.info('database_util.drop_database() '
                                       '- Dropping database ' + db_name)
        client.drop_database(db_name)
        client.close()
        success = True
    except:
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('InfluxDBError:' + str(clt_error_message))
        test_class_instance.mylog.info('InfluxDBError:' + str(traceback.extract_tb(clt_error_traceback)))
        error_message=str(clt_error_message)
        if client is not None:
            client.close()
    return (success, error_message)

def drop_series(test_class_instance, client, database, measurement=None, tags=None):
    '''
    DROP SERIES deletes all points from a series in a databases, and it drops the series from the index
    DROP SERIES does not support TIME INTERVALS
    DROP SERIES FROM <measurement_name[,measurement_name]> WHERE <tag_key>='<tag_value>'
    Either measurement or tags must be specified
    :param test_class_instance:
    :param client:
    :param database: (str) - the database from which the series shoudl be deleted.
    :param measurement: (str) - Delete All series from a measurements.
    :param tags: (dict) - Delete all series that match the given tags.
    :return:
    '''
    success=False
    error_message=''
    # check for measurement/tags
    if measurement is None and measurement is None:
        test_class_instance.mylog.info('database_util.drop_series() - must specify either measurement or tags')
        return (success, 'must specify either measurement or tags')
    try:
        test_class_instance.mylog.info('database_util.drop_series() - Dropping Series for database %s, '
                                       'measurement %s and tags %s' % (database, measurement, tags))
        # the function's name is delete_series, but it should have been named drop_series
        client.delete_series(database, measurement=measurement, tags=tags)
        client.close()
        success=True
    except:
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('InfluxDBError:' + str(clt_error_message))
        test_class_instance.mylog.info('InfluxDBError:' + str(traceback.extract_tb(clt_error_traceback)))
        error_message=str(clt_error_message)
        if client is not None:
            client.close()
    return (success, error_message)

def delete_series(test_class_instance, client, database, measurement=None, tags=None, time=None):
    '''
    DELETE SERIES query deletes all points from a series in database. It does not drop the series from the index,
    and it supports time intervals in the WHERE clause
    :param test_class_instance:
    :param client:
    :param database: (str)
    :param measurement: (str)
    :param tags: (dict)
    :param time: (str)
    :return:
    '''

    if measurement is None and time is None:
        return (False, None, 'Either measurement or time values should be supplied')
    if measurement is not None:
        query='DELETE FROM %s' % measurement
        if tags is not None:
            query=query+' WHERE %s = \'%s\'' % (''.join(tags.keys()),''.join(tags.values()))
    else:
        query='DELETE WHERE time < \'%s\'' % time
    test_class_instance.mylog.info('database_util.delete_series() - QUERY : %s' % (query))
    return run_query(test_class_instance, client, query, database=database)

def list_series(test_class_instance, client, database):
    '''
    :param test_class_instance:
    :param client:
    :param query:
    :param database:
    :return:
    '''
    series=[]
    success=False
    query='SHOW SERIES'
    error_message=''
    try:
        test_class_instance.mylog.info('database_util.list_series()- '
                                       'Geting all of the series for database %s' % database)
        (success, query_result, error)=run_query(test_class_instance, client, query, database=database)
        assert success, \
            test_class_instance.mylog.info('database_util.list_series()- Failed to SHOW SERIES' + str(error))
        # get the list of lists : [[u'foobar,id=0'], [u'foobar,id=1'], [u'foobar,id=10'], [u'foobar,id=11']]
        list_of_series=query_result._get_series()[0].get('values')
        test_class_instance.mylog.info('database_util.list_series()- series : ' + str(list_of_series))
        # convert the above list of lists to the list of strings
        for item in list_of_series:
            series.append(''.join(item))
        test_class_instance.mylog.info('database_util.list_series()- final series ' + str(series))
        success=True
    except:
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('SHOW SERIES Error:' + str(clt_error_message))
        test_class_instance.mylog.info('SHOW SERIES Error:' + str(traceback.extract_tb(clt_error_traceback)))
        error_message=str(clt_error_message)
    return (success, series, error_message)

def drop_measurement(test_class_instance, client, measurement):
    '''
    :param test_class_instance:
    :param client:
    :param measurement: (str) - the name of measurement to drop
    :return:
    '''
    success=False
    error_message=''
    try:
        test_class_instance.mylog.info('database_util.drop_database()- Dropping measurement %s' % measurement)
        client.drop_measurement(measurement)
        client.close()
        success=True
    except:
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('InfluxDBError:' + str(clt_error_message))
        test_class_instance.mylog.info('InfluxDBError:' + str(traceback.extract_tb(clt_error_traceback)))
        error_message=str(clt_error_message)
        if client is not None:
            client.close()
    return (success, error_message)

def list_measurements(test_class_instance, client):
    '''
    :param test_class_instance:
    :param client:
    :return: (list) - all measurements in InfluxDB
            [measurements1','measurements2,'measurements3']
    '''
    measurements_l=[]
    success=False
    error_message=''
    try:
        test_class_instance.mylog.info('database_util.list_measurements()- Geting all of the measurements')
        list_of_measurements=client.get_list_measurements()
        test_class_instance.mylog.info('database_util.list_measurements()- get_list_measurements returned : '
                                       + str(list_of_measurements))
        # list of measurements returns list of dictionaries: [{u'name': u'measurements1'},{u'name': u'measurements2'}]
        if len(list_of_measurements) != 0:
            for measurement in list_of_measurements:
                measurements_l.append(measurement.get('name'))
        client.close()
        success=True
    except:
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('InfluxDBError:' + str(clt_error_message))
        test_class_instance.mylog.info('InfluxDBError:' + str(traceback.extract_tb(clt_error_traceback)))
        error_message = str(clt_error_message)
        if client is not None:
            client.close()
    test_class_instance.mylog.info('database_util.list_measurements() - list of measurements '
                                   + str(measurements_l))
    return (success, measurements_l, error_message)

def use_database(test_class_instance, client, database):
    '''
    Changes the client databse
    :param test_class_instance:
    :param client:
    :param database: (str) the name of the database to switch to
    :return: success=True/False, if False, get the error message as well
    '''
    success=False
    error=''
    try:
        test_class_instance.mylog.info('database_util.use_database() - Switch to %s database' % database)
        client.switch_database(database)
        client.close()
        success=True
    except:
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('InfluxDBError:' + str(clt_error_message))
        test_class_instance.mylog.info('InfluxDBError:' + str(traceback.extract_tb(clt_error_traceback)))
        error=str(clt_error_message)
        if client is not None:
            client.close()
    test_class_instance.mylog.info('database_util.use_database() success=' + str(success))
    return (success, error)

#--------------------------------------------- RETENTION POLICIES -----------------------------------------------------#

def create_retention_policy(test_class_instance, client, rp_name, duration, replication, database, default):
    '''
    :param test_class_instance:
    :param client:
    :param rp_name:
    :param duration:
    :param replication:
    :param database:
    :param default:
    :return:
    '''
    success=False
    error_message=''
    try:
        test_class_instance.mylog.info('database_util.create_retention_policy()- '
                                       'CREATE RETENTION POLICY %s ON %s DURATION %s REPLICATION %s DEFAULT %s'
                                       % (rp_name, database, duration, replication, default))
        # by default SHARD DURATION is defined by POLICY DURATION : < 2d=1 hour, >=2d <= 6m =1day and > 6month=7 days
        client.create_retention_policy(rp_name, duration, replication, database, default)
        client.close()
        success=True
    except:
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('InfluxDBError:' + str(clt_error_message))
        test_class_instance.mylog.info('InfluxDBError:' + str(traceback.extract_tb(clt_error_traceback)))
        error_message = str(clt_error_message)
        if client is not None:
            client.close()
    return (success, error_message)

def drop_retention_policies(test_class_instance, client, database, rp_name):
    '''
    :param test_class_instance:
    :param client:
    :param database:
    :param rp_name:
    :return:
    '''
    success=False
    error_message=''
    try:
        test_class_instance.mylog.info('database_util.drop_retention_policies()- '
                                       'DROP RETENTION POLICY %s ON %s' % (rp_name, database))
        client.drop_retention_policy(rp_name,database)
        client.close()
        success=True
    except:
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('InfluxDBError:' + str(clt_error_message))
        test_class_instance.mylog.info('InfluxDBError:' + str(traceback.extract_tb(clt_error_traceback)))
        error_message = str(clt_error_message)
        if client is not None:
            client.close()
    return (success, error_message)

def show_retention_policies(test_class_instance, client, database):
    '''
    :param test_class_instance:
    :param client:
    :param database:
    :return:
    '''
    success = False
    error_message = ''
    retention_policies_d={}
    try:
        test_class_instance.mylog.info('database_util.show_retention_policies()- '
                                       'SHOW RETENTION POLICIES ON %s DATABASE' % database)
        #list of retention policy dictionaries: [{u'default': True,'duration': u'0','name': u'default','replicaN': 1}]
        retention_policies_l=client.get_list_retention_policies(database)
        for policy in retention_policies_l:
            # policy is represented by :{u'duration': u'24h0m0s', u'default': True, u'replicaN': 2,
            # u'name': u'annika.sapinski_retention_policy', u'shardGroupDuration': u'1h0m0s'}
            policy_name=policy.get('name')
            test_class_instance.mylog.info('database_util.show_retention_policies()- policy_name=' + str(policy_name))
            policy_duration=policy.get('duration')
            test_class_instance.mylog.info('database_util.show_retention_policies()- policy duration='
                                           + str(policy_duration))
            policy_default=policy.get('default')
            test_class_instance.mylog.info('database_util.show_retention_policies()- policy default='
                                           + str(policy_default))
            policy_replication=policy.get('replicaN')
            test_class_instance.mylog.info('database_util.show_retention_policies()- policy_replication='
                                           + str(policy_replication))
            policy_shard_group_duration=policy.get('shardGroupDuration')
            test_class_instance.mylog.info('database_util.show_retention_policies()- policy_shard_group_duration='
                                           + str(policy_shard_group_duration))
            retention_policies_d[policy_name]={'duration':policy_duration, 'default':policy_default,
                                               'replication':policy_replication,
                                               'shard_group_duration':policy_shard_group_duration}
        test_class_instance.mylog.info('database_util.show_retention_policies()- returned : '
                                       + str(retention_policies_d))
        client.close()
        success = True
    except:
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('InfluxDBError:' + str(clt_error_message))
        test_class_instance.mylog.info('InfluxDBError:' + str(traceback.extract_tb(clt_error_traceback)))
        error_message = str(clt_error_message)
        if client is not None:
            client.close()
    return (success, retention_policies_d, error_message)

def get_retention_policy(test_class_instance, dictionary_of_retention_policies, retention_policy_name):
    '''
    :param test_class_instance:
    :param dictinary_of_retention_policies:
    :param retention_policy_name:
    :return:
    '''
    test_class_instance.mylog.info('database_util.get_retention_policy()- ' + str(retention_policy_name))
    if retention_policy_name in dictionary_of_retention_policies.keys():
        return dictionary_of_retention_policies[retention_policy_name]
    else:
        return None

def get_retention_policy_duration(test_class_instance, retention_policy_dic):
    '''
    :param test_class_instance:
    :param retention_policy_dic:
    :return:
    '''
    test_class_instance.mylog.info('database_util.get_retention_policy_duration() function is being called')
    test_class_instance.mylog.info('----------------------------------------------------------------------')
    test_class_instance.mylog.info('database_util.get_retention_policy_duraiton() - duration='
                                   + retention_policy_dic['duration'])
    return retention_policy_dic['duration']

def get_retention_policy_is_default(test_class_instance, retention_policy_dic):
    '''
    :param test_class_instance:
    :param retention_policy_dic:
    :return:
    '''
    test_class_instance.mylog.info('database_util.get_retention_policy_is_default() function is being called')
    test_class_instance.mylog.info('------------------------------------------------------------------------')
    test_class_instance.mylog.info('database_util.get_retention_policy_is_default() - default='
                                   + retention_policy_dic['default'])
    return retention_policy_dic['default']

def get_retention_policy_replication(test_class_instance, retention_policy_dic):
    '''
    :param test_class_instance:
    :param retention_policy_dic:
    :return:
    '''
    test_class_instance.mylog.info('database_util.get_retention_policy_replication() function is being called')
    test_class_instance.mylog.info('-------------------------------------------------------------------------')
    test_class_instance.mylog.info('database_util.get_retention_policy_replicaiton() - replicaiton='
                                   + str(retention_policy_dic['replication']))
    return retention_policy_dic['replication']

def get_retention_policy_shard_group_duration(test_class_instance, retention_policy_dic):
    '''
    :param test_class_instance:
    :param retention_policy_dic:
    :return:
    '''
    test_class_instance.mylog.info('database_util.get_retention_policy_shard_group_duration() function is being called')
    test_class_instance.mylog.info('----------------------------------------------------------------------------------')
    test_class_instance.mylog.info('database_util.get_retention_policy_shard_group_duraiton() - shard group duration='
                                   + retention_policy_dic['shard_group_duration'])
    return retention_policy_dic['shard_group_duration']

def alter_retention_policy(test_class_instance, client, rp_name, database, duration=None,
                           replication=None, default=None):
    '''
    :param test_class_instance:
    :param client:
    :param rp_name:
    :param duration:
    :param replicaiton:
    :param database:
    :param default:
    :return:
    '''
    success = False
    error_message = ''
    try:
        test_class_instance.mylog.info('database_util.alter_retention_policy()- '
            'ALTER RETENTION POLICY %s ON %s DURATION %s REPLICATION %s DEFAULT %s'
                                       % (rp_name, database, duration, replication, default))
        client.alter_retention_policy(rp_name, database, duration, replication, default)
        client.close()
        success = True
    except:
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('InfluxDBError:' + str(clt_error_message))
        test_class_instance.mylog.info('InfluxDBError:' + str(traceback.extract_tb(clt_error_traceback)))
        error_message = str(clt_error_message)
        if client is not None:
            client.close()
    return (success, error_message)


######################################## REST API CHRONOGRAF ###########################################################

def get_default_databases_links(test_class_instance, default_sources):
    '''
    :param test_class_instance: instance of test class
    :param default_sources: dictionary of default sources, i.e. sources that
                 were created when chronograf was added to the cluster
    :return: list of links to the dbs, .i.e.[u'/chronograf/v1/sources/1/dbs',
                  u'/chronograf/v1/sources/2/dbs']
    '''
    test_class_instance.mylog.info('database_util.get_default_databases_links() functions is called')
    dbs_link_list=[]
    for source in default_sources.keys():
        dbs_link_list.append(su.get_source_dbs_link(test_class_instance,
                                        source_id=source, sources_dictionary=default_sources))
        test_class_instance.mylog.info('database_util.get_default_databases_links()'
                                       ' - dbs links =' + str(dbs_link_list))
    return dbs_link_list

def get_all_databases_links(test_class_instance, all_sources):
    '''
    :param test_clas_instance:instance of test class
    :param all_sources:dictionary of all sources
    :return: list of links to the dbs, .i.e.[u'/chronograf/v1/sources/1/dbs',
                  u'/chronograf/v1/sources/2/dbs']
    '''
    test_class_instance.mylog.info('database_util.get_all_databases_links() functions is called')
    dbs_link_list=[]
    for source in all_sources.keys():
        dbs_link_list.append(su.get_source_dbs_link(test_class_instance,
                                                    source_id=source, sources_dictionary=all_sources))
        test_class_instance.mylog.info('database_util.get_all_databases_links()'
                                       ' dbs links=' + str(dbs_link_list))
    return dbs_link_list

# /chronograf/v1/sources/2/dbs/_internal/rps
def get_policy_link(test_class_instance, dbs_for_source, db_name=None):
    '''
    :param test_class_instance:instance of the test class
    :param db_name: name of the database for a specific source (optional)
    :param dbs_for_source:dictionary of database(s) for a specific source
    :return: policy link, e.g. /chronograf/v1/sources/2/dbs/_internal/rps
    '''
    # we are dealing with only one database
    if db_name is None:
        policy_link=dbs_for_source.get('POLICY_LINKS')
    # we are dealing with all of the databases for a particular source
    else:
        policy_link=dbs_for_source.get(db_name).get('POLICY_LINKS')
    test_class_instance.mylog.info('database_util.get_policy_link() policy links=' + str(policy_link))
    return policy_link

def get_retention_policies(test_class_instance, dbs_for_source, db_name=None):
    '''
    :param test_class_instance:instance of the test class
    :param db_name: optional
    :param dbs_for_source:
    :return: dictionary of retention policies
    '''
    '''
    'RETENTION_POLICIES': 
	    {u'monitor': 
		    {'DURATION': u'168h0m0s', 
		    'REPLICATION': 1, 
			'POLICY_LINK': u'/chronograf/v1/sources/2/dbs/_internal/rps/monitor', 
			'DEFAULT': True, 
			'SHARD_DURATION': u'24h0m0s'}
    '''
    # we are dealing with only one database per source
    if db_name is None:
        retention_policies=dbs_for_source.get('RETENTION_POLICIES')
    else:
        retention_policies=dbs_for_source.get(db_name).get('RETENTION_POLICIES')
    test_class_instance.mylog.info('database_util.get_policy_link() retention policies =' + str(retention_policies))
    return retention_policies

def get_rp_names(test_class_instance, retention_policies):
    '''
    :param test_class_instance:instance of the class
    :param retention_policies: dictionary of retention policies for a specific database
    :return: list of retention policies names
    '''
    rp_names=retention_policies.keys()
    test_class_instance.mylog.info('database_util.get_policy_link() rp names=' + str(rp_names))
    return rp_names

def get_rp_duration(test_class_instance, retention_policies, retention_policy_name):
    '''
    :param test_class_instance:instance of the class
    :param retention_policies: dictionary of retention policies for a specific database
    :param retention_policy_name:name of the retention policy
    :return:retention policy duration
    '''
    rp_duration=retention_policies.get(retention_policy_name).get('DURATION')
    test_class_instance.mylog.info('database_util.get_policy_link() rp duration='
                                   + str(rp_duration) + ' for policy name='
                                   + str(retention_policy_name))
    return rp_duration

def get_rp_replication(test_class_instance, retention_policies, retention_policy_name):
    '''
    :param test_class_instance:instance of the class
    :param retention_policies:dictionary of retention policies for a specific database
    :param retention_policy_name:name of the retention policy
    :return: retention policy replication
    '''
    rp_replication=retention_policies.get(retention_policy_name).get('REPLICATION')
    test_class_instance.mylog.info('database_util.get_policy_link() rp replication='
                                   + str(rp_replication) + ' for policy name='
                                   + str(retention_policy_name))
    return rp_replication

def get_rp_shardduration(test_class_instance, retention_policies, retention_policy_name):
    '''
    :param test_class_instance:instance of the class
    :param retention_policies:dictionary of retention policies for a specific database
    :param retention_policy_name:name of the retention policy
    :return: retention policy shard duration
    '''
    rp_shard_duration=retention_policies.get(retention_policy_name).get('SHARD_DURATION')
    test_class_instance.mylog.info('database_util.get_policy_link() rp shard duration='
                                   + str(rp_shard_duration) + ' for policy name='
                                   + str(retention_policy_name))
    return rp_shard_duration

def get_rp_default(test_class_instance, retention_policies, retention_policy_name):
    '''
    :param test_class_instance:instance of the class
    :param retention_policies:dictionary of retention policies for a specific database
    :param retention_policy_name:name of the retention policy
    :return: retention policy isDefault status
    '''
    rp_default=retention_policies.get(retention_policy_name).get('DEFAULT')
    test_class_instance.mylog.info('database_util.get_policy_link() rp default='
                                   + str(rp_default) + ' for policy name='
                                   + str(retention_policy_name))
    return rp_default

# /chronograf/v1/sources/2/dbs/_internal/rps/monitor
def get_rp_policy_link(test_class_instance, retention_policies, retention_policy_name):
    '''
    :param test_class_instance:instance of the class
    :param retention_policies:dictionary of retention policies for a specific database
    :param retention_policy_name:name of the retention policy
    :return: retention policy link
    '''
    rp_link=retention_policies.get(retention_policy_name).get('POLICY_LINK')
    test_class_instance.mylog.info('database_util.get_policy_link() rp link='
                                   + str(rp_link) + ' for policy name='
                                   + str(retention_policy_name))
    return rp_link

