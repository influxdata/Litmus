
import src.util.sources_util as su
from influxdb.resultset import ResultSet
from influxdb import exceptions as e

######################## using influxDBClient ####################

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
    try:
        test_class_instance.mylog.info('database_util.create_database() '
                                       '- Creating database ' + db_name)
        #client=influxDbClient(host, port, user, password)
        client.create_database(db_name)
    except e.InfluxDBServerError:
        test_class_instance.mylog.info('InfluxDBServerError:' + str(e.InfluxDBServerError.message))
    except e.InfluxDBClientError:
        test_class_instance.mylog.info('InfluxDBClientError:' + str(e.InfluxDBClientError.message))

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
    try:
        test_class_instance.mylog.info('database_util.run_query() is called '
                                       'with query=%s, params=%s, epoch=%s, '
                                       'expected_response_code=%d, database=%s'
                                       % (query, params, epoch, expected_response_code,
                                          database))
        result=client.query(query=query, params=params, epoch=epoch,
                            expected_response_code=expected_response_code,
                            database=database)
    except e.InfluxDBServerError:
        test_class_instance.mylog.info('InfluxDBServerError:' + str(e.InfluxDBServerError.message))
    except e.InfluxDBClientError:
        test_class_instance.mylog.info('InfluxDBClientError:' + str(e.InfluxDBClientError.message))
    return result

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
    except e.InfluxDBServerError:
        test_class_instance.mylog.info('InfluxDBServerError:' + str(e.InfluxDBServerError.message))
    except e.InfluxDBClientError:
        test_class_instance.mylog.info('InfluxDBClientError:' + str(e.InfluxDBClientError.message))
    return return_value

############################################################
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

