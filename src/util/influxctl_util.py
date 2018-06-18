
def show_cluster_meta_nodes(test_class_instance, list_of_meta_nodes):
    '''
    Shows cluster meta node members
    :param test_class_instance: instance of a test class - self
    :param list_of_meta_nodes: (list of dictionaries) - list of meta nodes dictionaries:
            [{u'httpScheme': u'http', u'tcpAddr': u'10.0.150.167:8089', u'id': 2, u'version': u'meta-node version', u'addr': u'10.0.150.167:8091'},
            {u'httpScheme': u'http', u'tcpAddr': u'10.0.248.195:8089', u'id': 1, u'version': u'meta-node version', u'addr': u'10.0.248.195:8091'},
            {u'httpScheme': u'http', u'tcpAddr': u'10.0.51.86:8089',   u'id': 3, u'version': u'meta-node version', u'addr': u'10.0.51.86:8091'}]
    :return: dictionary of meta nodes: meta_node_id:{httpScheme, tcpAddr, version, addr}
    '''
    meta_node_dict={}
    test_class_instance.mylog.info('influxctl_util.show_cluster_meta_nodes() function is called')
    test_class_instance.mylog.info('===========================================================')
    meta_nodes_info=list_of_meta_nodes['meta']
    test_class_instance.mylog.info('influxctl_util.show_cluster_meta_nodes() - meta nodes ' + str(meta_nodes_info))
    for meta_node in meta_nodes_info:
        test_class_instance.mylog.info('influxctl_util.show_cluster_meta_nodes() - parsing meta_node : '
                                       + str(meta_node))
        meta_node_id=meta_node.get('id') # result dict key
        assert meta_node_id is not None, test_class_instance.mylog.info('influxctl_util.show_cluster_meta_nodes()'
                                                                        ' - meta_node_id is None')
        test_class_instance.mylog.info('influxctl_util.show_cluster_meta_nodes() - meta_node_id = ' + str(meta_node_id))
        meta_node_version=meta_node.get('version')
        assert meta_node_version is not None, test_class_instance.mylog.info('influxctl_util.show_cluster_meta_nodes()'
                                                                        ' - meta_node_version is None')
        test_class_instance.mylog.info('influxctl_util.show_cluster_meta_nodes() - meta_node_version = '
                                       + str(meta_node_version))
        meta_node_tcp_addr=meta_node.get('tcpAddr')
        assert meta_node_tcp_addr is not None, test_class_instance.mylog.info('influxctl_util.show_cluster_meta_nodes()'
                                                                        ' - meta_node_tcp_addr is None')
        test_class_instance.mylog.info('influxctl_util.show_cluster_meta_nodes() - meta_node_tcp_addr = '
                                       + str(meta_node_tcp_addr))
        meta_node_addr=meta_node.get('addr')
        assert meta_node_addr is not None, test_class_instance.mylog.info('influxctl_util.show_cluster_meta_nodes()'
                                                                        ' - meta_node_addr is None')
        test_class_instance.mylog.info('influxctl_util.show_cluster_meta_nodes() - meta_node_addr = '
                                       + str(meta_node_addr))
        meta_node_http_scheme=meta_node.get('httpScheme')
        assert meta_node_http_scheme is not None, \
            test_class_instance.mylog.info('influxctl_util.show_cluster_meta_nodes() - meta_node_http_scheme is None')
        test_class_instance.mylog.info('influxctl_util.show_cluster_meta_nodes() - meta_node_http_scheme = '
                                       + str(meta_node_http_scheme))
        meta_node_dict[meta_node_id]={'version':meta_node_version, 'tcpAddr':meta_node_tcp_addr, 'addr':meta_node_addr,
                                      'httpScheme':meta_node_http_scheme}
        test_class_instance.mylog.info('influxctl_util.show_cluster_meta_nodes()- interm dict : ' + str(meta_node_dict))
        test_class_instance.mylog.info('==============================================================================')
        test_class_instance.mylog.info('')
    test_class_instance.mylog.info('influxctl_util.show_cluster_meta_nodes() FINAL DICTIONARY = ' + str(meta_node_dict))
    test_class_instance.mylog.info('influxctl_util.show_cluster_meta_nodes() function is done')
    test_class_instance.mylog.info('=========================================================')
    test_class_instance.mylog.info('')
    return meta_node_dict

def meta_nodes_count(test_class_instance, meta_node_dict):
    '''
    :param test_class_instance: instance of the test class
    :param meta_node_dict: dictionary of meta nodes (output of show_cluster_meta_nodes function)
    :return: count of meta nodes
    '''
    test_class_instance.mylog.info('influxctl_util.meta_nodes_count() function is called')
    test_class_instance.mylog.info('====================================================')
    test_class_instance.mylog.info('influxctl_util.meta_nodes_count() - count of meta nodes = '
                                   + str(len(meta_node_dict)))
    return len(meta_node_dict)

def show_cluster_data_nodes(test_class_instance, list_of_data_nodes):
    '''
    Shows cluster data node members
    :param test_class_instance: instance of a test class - self
    :param list_of_data_nodes: list of dictionaries of data nodes:
            [{u'status': u'joined', u'tcpAddr': u'10.0.114.209:8088', u'httpAddr': u'10.0.114.209:8086', u'version': u'data node version', u'httpScheme': u'http', u'id': 5},
            {u'status': u'joined', u'tcpAddr': u'10.0.92.185:8088', u'httpAddr': u'10.0.92.185:8086', u'version': u'data node version', u'httpScheme': u'http', u'id': 4}]}
    :return: dicrionary of data nodes
    '''
    data_node_dict = {}
    test_class_instance.mylog.info('influxctl_util.show_cluster_data_nodes() function is called')
    test_class_instance.mylog.info('===========================================================')
    test_class_instance.mylog.info('')
    data_nodes_info=list_of_data_nodes['data']
    test_class_instance.mylog.info('influxctl_util.show_cluster_data_nodes() - data nodes ' + str(data_nodes_info))
    for data_node in data_nodes_info:
        test_class_instance.mylog.info('influxctl_util.show_cluster_data_nodes() - parsing data_node : '
                                       + str(data_node))
        data_node_id = data_node.get('id')  # result dict key
        assert data_node_id is not None, test_class_instance.mylog.info('influxctl_util.show_cluster_data_nodes()'
                                                                        ' - data_node_id is None')
        test_class_instance.mylog.info('influxctl_util.show_cluster_data_nodes() - data_node_id = ' + str(data_node_id))
        data_node_version = data_node.get('version')
        assert data_node_version is not None, test_class_instance.mylog.info('influxctl_util.show_cluster_data_nodes()'
                                                                             ' - data_node_version is None')
        test_class_instance.mylog.info('influxctl_util.show_cluster_data_nodes() - data_node_version = '
                                       + str(data_node_version))
        data_node_tcp_addr = data_node.get('tcpAddr')
        assert data_node_tcp_addr is not None, test_class_instance.mylog.info('influxctl_util.show_cluster_data_nodes()'
                                                                              ' - data_node_tcp_addr is None')
        test_class_instance.mylog.info('influxctl_util.show_cluster_data_nodes() - data_node_tcp_addr = '
                                       + str(data_node_tcp_addr))
        data_node_http_addr = data_node.get('httpAddr')
        assert data_node_http_addr is not None, test_class_instance.mylog.info('influxctl_util.show_cluster_data_nodes()'
                                                                          ' - data_node_http_addr is None')
        test_class_instance.mylog.info('influxctl_util.show_cluster_data_nodes() - data_node_http_addr = '
                                       + str(data_node_http_addr))
        data_node_http_scheme = data_node.get('httpScheme')
        assert data_node_http_scheme is not None, \
            test_class_instance.mylog.info('influxctl_util.show_cluster_data_nodes() - data_node_http_scheme is None')
        test_class_instance.mylog.info('influxctl_util.show_cluster_data_nodes() - data_node_http_scheme = '
                                       + str(data_node_http_scheme))
        data_node_status=data_node.get('status')
        assert data_node_status is not None, test_class_instance.mylog.info('influxctl_util.show_cluster_data_nodes()'
                                                                            ' - data_node_status is None')
        test_class_instance.mylog.info('influxctl_util.show_cluster_data_nodes() - data_node_status = '
                                       + str(data_node_status))
        data_node_dict[data_node_id] = {'version': data_node_version, 'tcpAddr': data_node_tcp_addr,
                                        'httpAddr': data_node_http_addr, 'status':data_node_status,
                                        'httpScheme': data_node_http_scheme}
        test_class_instance.mylog.info('influxctl_util.show_cluster_data_nodes()- interm dict : ' + str(data_node_dict))
        test_class_instance.mylog.info('==============================================================================')
        test_class_instance.mylog.info('')
    test_class_instance.mylog.info('influxctl_util.show_cluster_data_nodes() FINAL DICTIONARY = ' + str(data_node_dict))
    test_class_instance.mylog.info('influxctl_util.show_cluster_data_nodes() function is done')
    test_class_instance.mylog.info('=========================================================')
    test_class_instance.mylog.info('')
    return data_node_dict

def show_shards(test_class_instance, list_of_shards):
    '''
    Shows the shards in a cluster
    :param test_class_instance: instance of the test class - self
    :param list_of_shards: output of influx_rest_lib._show_shards method (list of dict of shard groups)
    :return: dictionary of shards {shard_id:{shard_group_id, shard_group_start_time, shard_group_end_time,
                                             database,replication,retention, retention_duration,
                                             owners}
    '''
    '''
    output of influx_rest_lib._show_shards method:
    ----------------------------------------------
    {u'shard-group-id': u'1', 
     u'end-time': u'2018-05-24T00:00:00Z', 
     u'start-time': u'2018-05-23T00:00:00Z', 
     u'owners': [{u'id': u'5', u'tcpAddr': u'10.0.114.209:8088'}], 
     u'database': u'_internal', 
     u'retention-policy': u'monitor', 
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
    for shard_group in list_of_shards:
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
        test_class_instance.mylog.info('=================================================================')
        test_class_instance.mylog.info('')
    test_class_instance.mylog.info('influxctl_util.show_shards() FINAL DICTIONARY = ' + str(shard_group_dic))
    test_class_instance.mylog.info('influxctl_util.show_shards() function is done')
    test_class_instance.mylog.info('=============================================')
    test_class_instance.mylog.info('')
    return shard_group_dic

def show_entropy_queued_shards():
    pass

def show_entropy_shards(test_class_instance, list_of_entropy_shards):
    '''
    :param test_class_instance:
    :param list_of_entropy_shards: list of dictionaries of outpus of _show_entropy
            {u'queued_shards': [],
             u'shards': [{u'status': u'diff', u'retention_policy': u'tsm_diff', u'database': u'test_tsm_db',
                          u'start_time': u'1528401600000000000', u'expires': u'1528534800000000000',
                          u'end_time': u'1528405200000000000', u'id': u'39'}
                        ],
             u'processing_shards': []}
    :return:
    '''
    entropy_shard_dict={}
    test_class_instance.mylog.info('influxctl_util.show_entropy_shards() function is called')
    test_class_instance.mylog.info('=======================================================')
    entropy_shards=list_of_entropy_shards['shards']
    for entry in entropy_shards:
        status=entry.get('status')
        assert status, test_class_instance.mylog.info('influxctl_util.show_entropy_shards() - status is None')
        test_class_instance.mylog.info('influxctl_util.show_entropy_shards()- status = ' + str(status))
        rp=entry.get('retention_policy')
        assert rp, test_class_instance.mylog.info('influxctl_util.show_entropy_shards() - retention policy is None')
        test_class_instance.mylog.info('influxctl_util.show_entropy_shards() - retention policy = ' + str(rp))
        db=entry.get('database')
        assert db, test_class_instance.mylog.info('influxctl_util.show_entropy_shards() - db is None')
        test_class_instance.mylog.info('influxctl_util.show_entropy_shards() - db = ' + str(db))
        shard_id=entry.get('id')
        assert shard_id, test_class_instance.mylog.info('influxctl_util.show_entropy_shards() - shard id is None')
        test_class_instance.mylog.info('influxctl_util.show_entropy_shards() - shard_id = ' + str(shard_id))
        start_time=entry.get('start_time')
        assert start_time, test_class_instance.mylog.info('influxctl_util.show_entropy_shards() -status is None')
        test_class_instance.mylog.info('influxctl_util.show_entropy_shards() - start_time = ' + str(start_time))
        end_time=entry.get('end_time')
        assert end_time, test_class_instance.mylog.info('influxctl_util.show_entropy_shards() -status is None')
        test_class_instance.mylog.info('influxctl_util.show_entropy_shards() - end_time = ' + str(end_time))
        expires=entry.get('expires')
        assert expires, test_class_instance.mylog.info('influxctl_util.show_entropy_shards() - expires is None')
        test_class_instance.mylog.info('influxctl_util.show_entropy_shards() - expires = ' + str(expires))
        entropy_shard_dict[shard_id]={'status':status, 'rp':rp, 'db':db, 'start_time':start_time, 'end_time':end_time,
                                      'expires': expires}
        test_class_instance.mylog.info('influxctl_util.show_entropy_shards()- interm dict : ' + str(entropy_shard_dict))
        test_class_instance.mylog.info('==============================================================================')
        test_class_instance.mylog.info('')
    test_class_instance.mylog.info('influxctl_util.show_entropy_shards() FINAL DICTIONARY = ' + str(entropy_shard_dict))
    test_class_instance.mylog.info('influxctl_util.show_entropy_shards() function is done')
    test_class_instance.mylog.info('=====================================================')
    test_class_instance.mylog.info('')
    return entropy_shard_dict

def show_entropy_processing_shards():
    pass