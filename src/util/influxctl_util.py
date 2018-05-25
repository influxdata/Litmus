

def show_shards(test_class_instance, list_of_shards):
    '''
    :param test_class_instance:
    :param list_of_shards: output of irl._show_shards method
    :return: dictionary of shards
    '''
    '''
    {u'shard-group-id': u'1', 
     u'end-time': u'2018-05-24T00:00:00Z', 
     u'start-time': u'2018-05-23T00:00:00Z', 
     u'owners': [{u'id': u'5', u'tcpAddr': u'10.0.114.209:8088'}], 
     u'database': u'_internal', 
     u'retention-policy': 
     u'monitor', 
     u'expire-time': u'2018-05-31T00:00:00Z', 
     u'replica-n': 1, 
     u'truncated-at': u'0001-01-01T00:00:00Z', 
     u'id': u'1'
     }
    {u'shard-group-id': u'1', u'end-time': u'2018-05-24T00:00:00Z', u'start-time': u'2018-05-23T00:00:00Z', u'owners': [{u'id': u'4', u'tcpAddr': u'10.0.92.185:8088'}], u'database': u'_internal', u'retention-policy': u'monitor', u'expire-time': u'2018-05-31T00:00:00Z', u'replica-n': 1, u'truncated-at': u'0001-01-01T00:00:00Z', u'id': u'2'}
    {u'shard-group-id': u'2', u'end-time': u'2018-05-28T00:00:00Z', u'start-time': u'2018-05-21T00:00:00Z', u'owners': [{u'id': u'4', u'tcpAddr': u'10.0.92.185:8088'}, {u'id': u'5', u'tcpAddr': u'10.0.114.209:8088'}], u'database': u'telegraf', u'retention-policy': u'autogen', u'expire-time': u'0001-01-01T00:00:00Z', u'replica-n': 2, u'truncated-at': u'0001-01-01T00:00:00Z', u'id': u'3'}
    '''
    shard_group_dic={}
    test_class_instance.mylog.info('influxctl_util.show_shards() function is called')
    test_class_instance.mylog.info('===============================================')
    (success, result, message)=list_of_shards
    if success == False:
        test_class_instance.mylog.info('influxctl_util.show_shards() - list of shards returned error : ' + str(message))
        return shard_group_dic
    for shard_group in result:
        test_class_instance.mylog.info('influxctl_util.show_shards() - parsing shard group : ' + str(shard_group))
        shard_id=shard_group.get('id') # dictionary key
        assert shard_id is not None, test_class_instance.mylog.info('influxctl_util.show_shards() - shard_id is None')
        test_class_instance.mylog.info('influxctl_util.show_shards() - shard_id = ' + str(shard_id))
        shard_group_id=shard_group.get('shard-group-id')
        assert shard_group_id is not None, \
            test_class_instance.mylog.info('influxctl_util.show_shards() - shard_group_id is None')
        test_class_instance.mylog.info('influxctl_util.show_shards() - shard_group_id = ' + str(shard_group_id))
        shard_group_start_time=shard_group.get('start-time')
        assert shard_group_start_time is not None, \
            test_class_instance.mylog.info('influxctl_util.show_shards() - shard_group_start_time is None')
        test_class_instance.mylog.info('influxctl_util.show_shards() - shard_group_start_time = '
                                       + str(shard_group_start_time))
        shard_group_end_time=shard_group.get('end-time')
        assert shard_group_end_time is not None, \
            test_class_instance.mylog.info('influxctl_util.show_shards() - shard_group_end_time is None')
        test_class_instance.mylog.info('influxctl_util.show_shards() - shard_group_end_time = '
                                       + str(shard_group_end_time))
        database=shard_group.get('database')
        assert database is not None, \
            test_class_instance.mylog.info('influxctl_util.show_shards() - database is None')
        test_class_instance.mylog.info('influxctl_util.show_shards() - database = ' + str(database))
        replication=shard_group.get('replica-n')
        assert replication is not None, \
            test_class_instance.mylog.info('influxctl_util.show_shards() - replication is None')
        test_class_instance.mylog.info('influxctl_util.show_shards() - replication = ' + str(replication))
        retention=shard_group.get('retention-policy')
        assert retention is not None, \
            test_class_instance.mylog.info('influxctl_util.show_shards() - retention is None')
        test_class_instance.mylog.info('influxctl_util.show_shards() - retention = ' + str(retention))
        retention_duration=shard_group.get('expire-time')
        assert retention_duration is not None, \
            test_class_instance.mylog.info('influxctl_util.show_shards() - retention_duration is None')
        test_class_instance.mylog.info('influxctl_util.show_shards() - retention_duration = ' + str(retention_duration))
        owners={}
        for node in shard_group.get('owners'): # list of dictionaries of data nodes that own this shard
            data_node_id=node.get('id')
            assert data_node_id is not None, \
                test_class_instance.mylog.info('influxctl_util.show_shards() - data_node_id is None')
            test_class_instance.mylog.info('influxctl_util.show_shards() - data_node_id = ' + str(data_node_id))
            tcp_addr=node.get('tcpAddr')
            assert tcp_addr is not None, \
                test_class_instance.mylog.info('influxctl_util.show_shards() - tcp_addr is None')
            test_class_instance.mylog.info('influxctl_util.show_shards() - tcp_addr = ' + str(tcp_addr))
            owners[tcp_addr]=data_node_id
        shard_group_dic[shard_id]={'shard_group_id':shard_group_id, 'shard_group_start_time':shard_group_start_time,
                                   'shard_group_end_time':shard_group_end_time, 'database':database,
                                   'replication':replication, 'retention':retention,
                                   'retention_duration':retention_duration, 'data_nodes':owners}
        test_class_instance.mylog.info('influxctl_util.show_shards() interm dic = ' + str(shard_group_dic))
    test_class_instance.mylog.info('influxctl_util.show_shards() FINAL DICTIONARY = ' + str(shard_group_dic))
    test_class_instance.mylog.info('influxctl_util.show_shards() function is done')
    test_class_instance.mylog.info('=============================================')
    test_class_instance.mylog.info('')
    return shard_group_dic