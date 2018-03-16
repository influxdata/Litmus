

def get_sources_count(test_class_instance, sources_dictionary):
    '''
    :param test_class_instance: instance of test class
    :param sources_dictionary: dictionary of all sources where key is a source id and value is a dictionary of response
                               values
    :return: count of sources
    '''
    test_class_instance.mylog.info('sources_util.get_sources_count() - Sources Count = ' + str(len(sources_dictionary)))
    return len(sources_dictionary)

# When the source is being created, then id of the source is returned as part of the request. Means we always know
# source data we are interested in.

def get_key(test_class_instance, source_id, sources_dictionary, key):
    '''
    :param test_class_instance:
    :param source_id:
    :param sources_dictionary:
    :param key:
    :return:
    '''
    test_class_instance.mylog.info('sources_util.get_key() - Getting value for ' + str(key) + ' key')
    try:
        key_value=(sources_dictionary.get(source_id)).get(key)
        test_class_instance.mylog.info('sources_util.get_key() - Value = ' + str(key_value))
    except AttributeError, e:
        test_class_instance.mylog.info('sources_util.get_key() - AttributeError: ' + str(e.message))
        key_value=None
    return key_value

def get_source_name(test_class_instance, source_id, sources_dictionary):
    '''
    :param test_class_instance: instance of test class
    :param source_id: id of the source
    :param sources_dictionary: dictionary of all sources
    :return: source name
    '''
    test_class_instance.mylog.info('sources_util.get_source_name() - '
                                   'Getting NAME of the source for ID ' + str(source_id))
    return get_key(test_class_instance, source_id, sources_dictionary, 'NAME')

def get_source_type(test_class_instance, source_id, sources_dictionary):
    '''
    :param test_class_instance:
    :param source_id:
    :param sources_dictionary:
    :return:
    '''
    test_class_instance.mylog.info('sources_util.get_source_type() - '
                                   'Getting TYPE of the source for ID ' + str(source_id))
    return get_key(test_class_instance, source_id, sources_dictionary, 'TYPE')

def get_source_username(test_class_instance, source_id, sources_dictionary):
    '''
    :param test_class_instance:
    :param source_id:
    :param sources_dictionary:
    :return:
    '''
    test_class_instance.mylog.info('sources_util.get_source_username() - '
                                   'Getting TYPE of the source for ID ' + str(source_id))
    return get_key(test_class_instance, source_id, sources_dictionary, 'USERNAME')

def get_source_password(test_class_instance, source_id, sources_dictionary):
    '''
    :param test_class_instance:
    :param source_id:
    :param sources_dictionary:
    :return:
    '''
    test_class_instance.mylog.info('sources_util.get_source_password() - '
                                   'Getting PASSWORD of the source for ID ' + str(source_id))
    return get_key(test_class_instance, source_id, sources_dictionary, 'PASSWORD')

def get_source_sharedsecret(test_class_instance, source_id, sources_dictionary):
    '''
    :param test_class_instance:
    :param source_id:
    :param sources_dictionary:
    :return:
    '''
    test_class_instance.mylog.info('sources_util.get_source_sharedsecret() - '
                                   'Getting SHARED_SECRET of the source for ID ' + str(source_id))
    return get_key(test_class_instance, source_id, sources_dictionary, 'SHARED_SECRET')

def get_source_url(test_class_instance, source_id, sources_dictionary):
    '''
    :param test_class_instance:
    :param source_id:
    :param sources_dictionary:
    :return:
    '''
    test_class_instance.mylog.info('sources_util.get_source_url() - '
                                   'Getting DATA URL of the source for ID ' + str(source_id))
    return get_key(test_class_instance, source_id, sources_dictionary, 'DATA_URL')

def get_source_metaurl(test_class_instance, source_id, sources_dictionary):
    '''
    :param test_class_instance:
    :param source_id:
    :param sources_dictionary:
    :return:
    '''
    test_class_instance.mylog.info('sources_util.get_source_metaurl() - '
                                   'Getting META URL of the source for ID ' + str(source_id))
    return get_key(test_class_instance, source_id, sources_dictionary, 'META_URL')

def get_source_insecureskipverify(test_class_instance, source_id, sources_dictionary):
    '''
    :param test_class_instance:
    :param source_id:
    :param sources_dictionary:
    :return:
    '''
    test_class_instance.mylog.info('sources_util.get_source_insecureskipverify() - '
                                   'Getting INSECURE SKIP VERIFY of the source for ID ' + str(source_id))
    return get_key(test_class_instance, source_id, sources_dictionary, 'INSECURE_SKIP_VERIFY')

def get_source_default(test_class_instance, source_id, sources_dictionary):
    '''
    :param test_class_instance:
    :param source_id:
    :param sources_dictionary:
    :return:
    '''
    test_class_instance.mylog.info('sources_util.get_source_default() - '
                                   'Getting DEFAULT of the source for ID ' + str(source_id))
    return get_key(test_class_instance, source_id, sources_dictionary, 'DEFAULT')

def get_source_telegraf(test_class_instance, source_id, sources_dictionary):
    '''
    :param test_class_instance:
    :param source_id:
    :param sources_dictionary:
    :return:
    '''
    test_class_instance.mylog.info('sources_util.get_source_telegraf() - '
                                   'Getting TELEGRAF DB of the source for ID ' + str(source_id))
    return get_key(test_class_instance, source_id, sources_dictionary, 'TELEGRAF_DB')

def get_source_proxy_link(test_class_instance, source_id, sources_dictionary):
    '''
    :param test_class_instance:
    :param source_id:
    :param sources_dictionary:
    :return:
    '''
    test_class_instance.mylog.info('sources_util.get_source_proxy_link() - '
                                   'Getting PROXY LINK of the source for ID ' + str(source_id))
    return get_key(test_class_instance, source_id, sources_dictionary, 'PROXY')

def get_source_write_link(test_class_instance, source_id, sources_dictionary):
    '''
    :param test_class_instance:
    :param source_id:
    :param sources_dictionary:
    :return:
    '''
    test_class_instance.mylog.info('sources_util.get_source_write_link() - '
                                   'Getting WRITE LINK of the source for ID ' + str(source_id))
    return get_key(test_class_instance, source_id, sources_dictionary, 'WRITE')

def get_source_queries_link(test_class_instance, source_id, sources_dictionary):
    '''
    :param test_class_instance:
    :param source_id:
    :param sources_dictionary:
    :return:
    '''
    test_class_instance.mylog.info('sources_util.get_source_queries_link() - '
                                   'Getting QUERIES LINK of the source for ID ' + str(source_id))
    return get_key(test_class_instance, source_id, sources_dictionary, 'QUERY')

def get_source_kapacitors_link(test_class_instance, source_id, sources_dictionary):
    '''
    :param test_class_instance:
    :param source_id:
    :param sources_dictionary:
    :return:
    '''
    test_class_instance.mylog.info('sources_util.get_source_kapacitors_link() - '
                                   'Getting KAPACITORS LINK of the source for ID ' + str(source_id))
    return get_key(test_class_instance, source_id, sources_dictionary, 'KAPACITOR')

def get_source_users_link(test_class_instance, source_id, sources_dictionary):
    '''
    :param test_class_instance:
    :param source_id:
    :param sources_dictionary:
    :return:
    '''
    test_class_instance.mylog.info('sources_util.get_source_users_link() - '
                                   'Getting USERS LINK of the source for ID ' + str(source_id))
    return get_key(test_class_instance, source_id, sources_dictionary, 'USERS')

def get_source_permissions_link(test_class_instance, source_id, sources_dictionary):
    '''
    :param test_class_instance:
    :param source_id:
    :param source_dictionary:
    :return:
    '''
    test_class_instance.mylog.info('sources_util.get_source_permissions_link() - '
                                   'Getting PERMISSIONS LINK of the source for ID ' + str(source_id))
    return get_key(test_class_instance, source_id, sources_dictionary, 'PERMISSIONS')

def get_source_roles_link(test_class_instance, source_id, sources_dictionary):
    '''
    :param test_class_instance:
    :param source_id:
    :param sources_dictionary:
    :return:
    '''
    test_class_instance.mylog.info('sources_util.get_source_roles_link() - '
                                   'Getting ROLES LINK of the source for ID ' + str(source_id))
    return get_key(test_class_instance, source_id, sources_dictionary, 'ROLES')

def verify_data(test_class_instance ,expected, actual):
    '''
    :param expected: expected value
    :param actual: actual value
    :return: pass or fail
    '''
    assert expected == actual, test_class_instance.mylog.info('sources_util.verify_data() - '
                                                              'ASSERTION FAILED: EXPECTED='+ str(expected) +
                                                              ', ACTUAL=' + str(actual))
