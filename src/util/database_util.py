
import src.util.sources_util as su

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
