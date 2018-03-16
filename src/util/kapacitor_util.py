

def get_key(test_class_instance, kapacitor_id, kapacitor_dictionary, key):
    '''
    :param test_class_instance:
    :param kapacitor_id:
    :param kapacitor_dictionary:
    :param key:
    :return:
    '''
    test_class_instance.mylog.info('kapacitor_util.get_key() - Getting value for ' + str(key) + ' key')
    try:
        key_value=(kapacitor_dictionary.get(kapacitor_id)).get(key)
        test_class_instance.mylog.info('kapacitor_util.get_key() - Value = ' + str(key_value))
    except AttributeError, e:
        test_class_instance.mylog.info('skapacitor_util.get_key() - AttributeError: ' + str(e.message))
        key_value=None
    return key_value

def get_kapacitor_name(test_class_instance, kapacitor_id, kapacitor_dictionary):
    '''
    :param test_class_instance:
    :param kapacitor_id:
    :param kapacitor_dictionary:
    :return:
    '''
    test_class_instance.mylog.info('kapacitor_util.get_kapacitor_name() - '
                                   'Getting NAME of the kapacitor for ID ' + str(kapacitor_id))
    return get_key(test_class_instance, kapacitor_id, kapacitor_dictionary, 'NAME')

def get_kapacitor_url(test_class_instance, kapacitor_id, kapacitor_dictionary):
    '''
    :param test_class_instance:
    :param kapacitor_id:
    :param kapacitor_dictionary:
    :return:
    '''
    test_class_instance.mylog.info('kapacitor_util.get_kapacitor_url() - '
                                   'Getting URL of the kapacitor for ID ' + str(kapacitor_id))
    return get_key(test_class_instance, kapacitor_id, kapacitor_dictionary, 'URL')

def get_kapacitor_username(test_class_instance, kapacitor_id, kapacitor_dictionary):
    '''
    :param test_class_instance:
    :param kapacitor_id:
    :param kapacitor_dictionary:
    :return:
    '''
    test_class_instance.mylog.info('kapacitor_util.get_kapacitor_username() - '
                                   'Getting USERNAME of the kapacitor for ID ' + str(kapacitor_id))
    return get_key(test_class_instance, kapacitor_id, kapacitor_dictionary, 'USERNAME')

def get_kapacitor_password(test_class_instance, kapacitor_id, kapacitor_dictionary):
    '''
    :param test_class_instance:
    :param kapacitor_id:
    :param kapacitor_dictionary:
    :return:
    '''
    test_class_instance.mylog.info('kapacitor_util.get_kapacitor_password() - '
                                   'Getting PASSWORD of the kapacitor for ID ' + str(kapacitor_id))
    return get_key(test_class_instance, kapacitor_id, kapacitor_dictionary, 'PASSWORD')

def get_kapacitor_active(test_class_instance, kapacitor_id, kapacitor_dictionary):
    '''
    :param test_class_instance:
    :param kapacitor_id:
    :param kapacitor_dictionary:
    :return:
    '''
    test_class_instance.mylog.info('kapacitor_util.get_kapacitor_active() - '
                                   'Getting ACTIVE of the kapacitor for ID ' + str(kapacitor_id))
    return get_key(test_class_instance, kapacitor_id, kapacitor_dictionary, 'ACTIVE')

def get_kapacitor_rules(test_class_instance, kapacitor_id, kapacitor_dictionary):
    '''
    :param test_class_instance:
    :param kapacitor_id:
    :param kapacitor_dictionary:
    :return:
    '''
    test_class_instance.mylog.info('kapacitor_util.get_kapacitor_rules() - '
                                   'Getting RULES LINK of the kapacitor for ID ' + str(kapacitor_id))
    return get_key(test_class_instance, kapacitor_id, kapacitor_dictionary, 'RULES')

def get_kapacitor_proxy(test_class_instance, kapacitor_id, kapacitor_dictionary):
    '''
    :param test_class_instance:
    :param kapacitor_id:
    :param kapacitor_dictionary:
    :return:
    '''
    test_class_instance.mylog.info('kapacitor_util.get_kapacitor_proxy() - '
                                   'Getting PROXY LINK of the kapacitor for ID ' + str(kapacitor_id))
    return get_key(test_class_instance, kapacitor_id, kapacitor_dictionary, 'PROXY')

def get_kapacitor_ping(test_class_instance, kapacitor_id, kapacitor_dictionary):
    '''
    :param test_class_instance:
    :param kapacitor_id:
    :param kapacitor_dictionary:
    :return:
    '''
    test_class_instance.mylog.info('kapacitor_util.get_kapacitor_ping() - '
                                   'Getting PING LINK of the kapacitor for ID ' + str(kapacitor_id))
    return get_key(test_class_instance, kapacitor_id, kapacitor_dictionary, 'PING')

def get_kapacitor_tasks(test_class_instance, kapacitor_id, kapacitor_dictionary):
    '''
    :param test_class_instance:
    :param kapacitor_id:
    :param kapacitor_dictionary:
    :return:
    '''
    test_class_instance.mylog.info('kapacitor_util.get_kapacitor_tasks() - '
                                   'Getting TASKS LINK of the kapacitor for ID ' + str(kapacitor_id))
    return get_key(test_class_instance, kapacitor_id, kapacitor_dictionary, 'TASKS')