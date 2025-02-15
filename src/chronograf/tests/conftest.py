
import pytest
import src.util.database_util as du
from influxdb import InfluxDBClient as influxDbClient
from influxdb import exceptions as e
from random import choice
from src.chronograf.lib import chronograf_rest_lib


@pytest.fixture(scope='class')
def get_all_paths(request, chronograf):
    '''
    Returns all of the chronograf paths
    :param request:request object to introspect the requesting test function, class or module context
    :param chronograf:Chronograf URL, e.g. http://<ID>:<PORT>, where port is 8888
    :return:all of the paths:
            me --> /chronograf/v1/me
            organizations --> /chronograf/v1/organizations
            users --> /chronograf/v1/organizations/default/users
            allUsers --> /chronograf/v1/users
            dashboards --> /chronograf/v1/dashboards
            auth --> []
            environment --> /chronograf/v1/env
            sources --> /chronograf/v1/sources
            layouts --> /chronograf/v1/layouts
            external --> {u'statusFeed': u'https://www.influxdata.com/feed/json'}
            config --> {u'self': u'/chronograf/v1/config', u'auth': u'/chronograf/v1/config/auth'}
            mappings --> /chronograf/v1/mappings
    '''
    rl=chronograf_rest_lib.RestLib(request.cls.mylog)
    request.cls.mylog.info('get_all_paths() fixture is being called')
    request.cls.mylog.info('---------------------------------------')
    request.cls.mylog.info('')
    response=rl.get_chronograf_paths(chronograf)
    request.cls.get_all_paths=response
    request.cls.mylog.info('get_all_paths() fixture - done')
    request.cls.mylog.info('------------------------------')
    request.cls.mylog.info('')
    return request.cls.get_all_paths

@pytest.fixture(scope='class')
def get_source_path(request, chronograf):
    '''
    :param request:request object to introspect the rtequesting test function, class or module context
    :param chronograf:Chronograf URL, e.g. http://<ID>:<PORT>, where port is 8888
    :return:source path, e.g. ['sources':'/chronograf/v1/sources']
    '''
    request.cls.mylog.info('get_source_path() fixture is being called')
    request.cls.mylog.info('-----------------------------------------')
    request.cls.mylog.info('')
    request.cls.mylog.info('get_source_path() call get_all_paths() fixture')
    source_path=get_all_paths(request, chronograf)['sources']
    assert source_path is not None, request.cls.mylog.info('get_source_path() ASSERTION ERROR')
    request.cls.mylog.info('get_source_path() fixture source_path=' + str(source_path))
    request.cls.get_source_path=source_path
    request.cls.mylog.info('get_source_path() - done')
    request.cls.mylog.info('------------------------')
    request.cls.mylog.info('')
    return request.cls.get_source_path

@pytest.fixture(scope='class')
def create_source(request, chronograf, data_nodes, meta_nodes, http_auth, admin_user, admin_pass):
    '''
    Creates source and returns the data for the created source as dictionary
    :param request:request object to introspect the rtequesting test function, class or module context
    :param chronograf: Chronograf URL, e.g. http://<ID>:<PORT>, where port is 8888
    :param data_nodes: list of data nodes passed or returned by pcl installer
    :param meta_nodes: list of meta nodes passed or returned by pcl installer
    :return: tuple of source_id and source response object
    '''
    request.cls.mylog.info('create_source() fixture is being called')
    request.cls.mylog.info('---------------------------------------')
    request.cls.mylog.info('')
    rl= chronograf_rest_lib.RestLib(request.cls.mylog)
    source_name=request.param
    # assert lists of data and meta nodes are not empty
    assert len(data_nodes) != 0 and len(meta_nodes) != 0, \
        request.cls.mylog.info('create_source() ASSERTION ERROR, meta nodes are ' + str(len(meta_nodes))
                               + ', data nodes are' + str(len(data_nodes)))
    # randomly select data node and meta node from the list of nodes
    datanode=choice(data_nodes)
    request.cls.mylog.info('create_source() fixture : datanode=' + str(datanode))
    metanode=choice(meta_nodes)
    request.cls.mylog.info('create_source() fixture : metanode=' + str(metanode))
    # create source
    source_path=get_source_path(request, chronograf)
    username, password ='', ''
    if http_auth:
        username=admin_user
        password=admin_pass
    data={'url':datanode, 'metaUrl':metanode, 'name':source_name, 'username':username, 'password':password}
    (status, source_data, source_id)=rl.create_source(chronograf, source_url=source_path, json=data)
    assert status == 201, request.cls.mylog.info('create_source. create_source() status=' + str(status))
    assert source_id is not None, request.cls.mylog.info('create_source. create_source() source_id=' + str(source_id))
    # get created source data
    result_dic=rl.get_source(chronograf, source_path, source_id)
    request.cls.create_source=(source_id, result_dic)
    request.cls.mylog.info('create_source() fixture - done')
    request.cls.mylog.info('------------------------------')
    request.cls.mylog.info('')
    return request.cls.create_source

@pytest.fixture(scope='class')
def default_sources(request, clustername, all_sources):
    '''
    Return the dictionary of all of the default sources. Default source is
    base on the number of the data nodes
    :param request:
    :param clustername: name of the cluster
    :param all_sources; dict of all of the existing sources
    :return: default sources (ones that are created by pcl add-chronograf command)
    '''
    default_sources={}
    request.cls.mylog.info('default_sources() FIXTURE IS CALLED')
    request.cls.mylog.info('default_sources() : GET ALL OF THE SOURCES')
    for source_id in all_sources.keys():
        # default source would have a name of the cluster as part of its full name
        if (all_sources[source_id].get('NAME')).find(clustername) != -1:
            request.cls.mylog.info('default_sources() : GETTING SOURCE ID=' + str(source_id))
            default_sources[source_id]=all_sources[source_id]
    request.cls.mylog.info('default_sources(): DEFAULTS SOURCES : '  +str(default_sources))
    request.cls.default_sources=default_sources
    return request.cls.default_sources

@pytest.fixture(scope='class')
def all_sources(request, chronograf, http_auth, admin_user, admin_pass,
                get_source_path ,meta_nodes):

    '''
    Return the dictionary of all of the data sources
    :param request: request object to introspect the requesting test class
    :param chronograf: chronograf URL
    :param http_auth: whether authentication available of not
    :param admin_user : name of the admin user
    :param admin_pass : password of the admin user
    :param meta_nodes: list of meta nodes
    :return: dictionary of all sources where dict key is a data source_id
    '''
    rl=chronograf_rest_lib.RestLib(request.cls.mylog)
    request.cls.mylog.info('all_sources() FIXTURE IS CALLED')
    request.cls.mylog.info('all_sources() : GET ALL OF THE SOURCES')
    sources=rl.get_sources(chronograf, get_source_path)
    if http_auth: # authentication is enabled
        new_sources={}
        for source_id in sources.keys():
            # need to update data sources with admin user and password
            request.cls.mylog.info('all_sources() : Updating source id : '
                                   + str(source_id)  + ' since authentication is enabled')
            source_name=sources[source_id].get('NAME')
            data_url=sources[source_id].get('DATA_URL')
            # need to update meta url in case it is empty
            meta_url=choice(meta_nodes)
            type=sources[source_id].get('TYPE')
            default_source=sources[source_id].get('DEFAULT')
            telegraf_db=sources[source_id].get('TELEGRAF_DB')
            data_for_update={'name': source_name, 'url': data_url,
                             'metaUrl': meta_url, 'type': type, 'default': default_source,
                             'telegraf': telegraf_db, 'username':admin_user,
                             'password':admin_pass}
            rl.patch_source(chronograf, get_source_path, data_for_update, source_id)
            # need to get the updated source data
            source_data=rl.get_source(chronograf, get_source_path, source_id)
            new_sources[source_id]=source_data[source_id]
        request.cls.mylog.info('all_sources(): ALL SOURCES : '  +str(new_sources))
        request.cls.all_sources=new_sources
    else:
        request.cls.mylog.info('all_sources(): ALL SOURCES : '  +str(sources))
        request.cls.all_sources=sources
    return request.cls.all_sources

@pytest.fixture(scope='class')
def delete_sources(request, chronograf):
    '''
    Deletes all of the exisitng sources, including default ones.
    :param request:request object to introspect the rtequesting test function, class or module context
    :param chronograf:Chronograf URL, e.g. http://<ID>:<PORT>, where port is 8888
    :return: assert status code == 204
    '''
    rl= chronograf_rest_lib.RestLib(request.cls.mylog)
    request.cls.mylog.info('delete_sources() FIXTURE IS CALLED')
    request.cls.mylog.info('delete_sources() : GET ALL OF THE SOURCES')
    source_path=get_source_path(request, chronograf)
    sources=rl.get_sources(chronograf, source_path)
    for source in sources.keys():
        request.cls.mylog.info('delete_sources() : DELETING SOURCE ID=' + str(source))
        rl.delete_source(chronograf, source_path, source)
    request.cls.mylog.info('delete_sources() IS DONE')

@pytest.fixture(scope='class')
def delete_created_sources(request, chronograf, clustername):
    '''
    Deletes all of the created by tests sources
    :param request:request object to introspect the rtequesting test function, class or module context
    :param chronograf:Chronograf URL, e.g. http://<ID>:<PORT>, where port is 8888
    :param clustername:Name of the cluster
    :return: does not return, make an assertion status code == 204
    '''
    rl= chronograf_rest_lib.RestLib(request.cls.mylog)
    request.cls.mylog.info('delete_created_sources() fixture is called')
    request.cls.mylog.info('------------------------------------------')
    request.cls.mylog.info('')
    request.cls.mylog.info('delete_created_sources() fixture calls get_source_path fixture')
    source_path=get_source_path(request, chronograf)
    request.cls.mylog.info('delete_created_sources() fixture calls rest_lib.get_sources() method')
    request.cls.mylog.info('--------------------------------------------------------------------')
    request.cls.mylog.info('')
    sources=rl.get_sources(chronograf, source_path)
    for source in sources.keys():
        if (sources[source].get('NAME')).find(clustername) == -1:
            request.cls.mylog.info('delete_created_sources() fixture : deleting source_id=' + str(source))
            rl.delete_source(chronograf, source_path, source)
    request.cls.mylog.info('delete_created_sources() fixture - done')
    request.cls.mylog.info('---------------------------------------')
    request.cls.mylog.info('')

@pytest.fixture(scope='class')
def delete_created_databases(request, chronograf, all_sources):
    '''
    Deleted all of the created databases with the exception of default ones (_internal, telegraf).
    :param request:
    :param chronograf:
    :return: asserts status == 204
    '''
    rl=chronograf_rest_lib.RestLib(request.cls.mylog)
    request.cls.mylog.info('delete_created_databases() FIXTURE IS CALLED')
    request.cls.mylog.info('--------------------------------------------')
    request.cls.mylog.info('')
    dbs_links=du.get_all_databases_links(request.cls, all_sources)
    request.cls.mylog.info('delete_created_databases() dbs_links ' + str(dbs_links))
    db_link=choice(dbs_links)
    response=rl.get_databases(chronograf, db_link)
    for name in response.keys():
        if name not in ['_internal', 'telegraf']:
            request.cls.mylog.info('delete_created_databases() DELETING DATABASE ' + str(name))
            rl.delete_database(chronograf, db_link, name)
    request.cls.mylog.info('delete_created_databases() FIXTURE IS DONE')
    request.cls.mylog.info('------------------------------------------')
    request.cls.mylog.info('')

@pytest.fixture(scope='class')
def delete_created_rp(request, chronograf, data_nodes_ips, default_sources,
                      http_auth, admin_user, admin_pass):
    '''
    Removes all of the created by the tests retention policies using InfluxDBClient library
    for the exception of default policies for default databases
    :param request:
    :param data_nodes_ips: list of data nodes IPs
    :param default_sources: dictionary of default sources with a source_id as a key
    :param chronograf: URL to achronograf, ie. http://<IP>:<port>
    '''
    username, password='', ''
    if http_auth:
        username=admin_user
        password=admin_pass
    rl= chronograf_rest_lib.RestLib(request.cls.mylog)
    request.cls.mylog.info('delete_created_rp() FIXURE IS CALLED')
    request.cls.mylog.info('------------------------------------')
    request.cls.mylog.info('')
    # randomly choose a data_node
    data_node=choice(data_nodes_ips)
    # choose database url from a default data source:
    source_id=choice(default_sources.keys())
    # get a database url from a chosen default data source
    dbs_url=default_sources[source_id]['DBS']
    # get all retention policies for default databases: _internal and telegraf
    telegraf_rp=rl.get_database(chronograf, dbs_url, 'telegraf').get('RETENTION_POLICIES').keys()
    request.cls.mylog.info('delete_created_rp() retention policies for telegraf db=' + str(telegraf_rp))
    internal_rp=rl.get_database(chronograf, dbs_url, '_internal').get('RETENTION_POLICIES').keys()
    request.cls.mylog.info('delete_created_rp() retention policies for _internal db=' + str(internal_rp))
    # define parameter - list of retention policies to be removed
    try:
        client=influxDbClient(host=data_node,port=8086, username=username, password=password)
        for rp in telegraf_rp:
            if rp != 'autogen':
                client.drop_retention_policy(rp, 'telegraf')
        for rp in internal_rp:
            if rp != 'monitor':
                client.drop_retention_policy(rp, '_internal')
        client.close()
    except e.InfluxDBClientError:
        request.cls.mylog.info('ClientError message=' + e.InfluxDBClientError.message)
    except e.InfluxDBServerError:
        request.cls.mylog.info('ServerError message=' + e.InfluxDBServerError.message)
