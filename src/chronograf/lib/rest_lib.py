
import requests, os
from src.chronograf.lib.base_lib import BaseLib



class RestLib(BaseLib):
    '''
    TODO
    '''

    CHRONOGRAF_PATH = '/chronograf/v1'

    def post(self, base_url, path, json, data=None, headers=None):
        '''
        :param base_url:
        :param path:
        :param json:
        :param data:
        :param kwargs:
        :return:
        '''
        self.log.info('RestLib.post() is called with parameters: base_url=' + str(base_url) + ', path=' + str(path)
                      + ', json=' + str(json))
        try:
            response=requests.post(base_url + path, json=json, data=data, headers=headers)
            self.log.info('RestLib.post() response code=' + str(response.status_code))
            # TODO add more logging
        except requests.ConnectionError, e:
            self.log.info('RestLib.post() - ConnectionError : ' + str(e.message))
            response=None
        except requests.RequestException, e:
            self.log.info('RestLib.post() - RequestsException : ' + str(e.message))
            response=None
        assert response is not None, self.log.info('SOME ERROR MESSAGE FOR POST')
        return response

    def get(self, base_url, path, params=None, headers=None):
        '''
        :param base_url:
        :param path:
        :param params: (optional) Dictionary to be sent in the query string for the request
        :param kwargs: optional arguments that request takes (for example custom headers, cookies, etc)
        :return: response object
        '''
        self.log.info('RestLib.get() is called with parameters: base_url = '\
                      + str(base_url) + ', path = ' + str(path) + ', params = '\
                      + str(params) + ', headers= ' + str(headers))
        try:
            response=requests.get(base_url + path, params=params, headers=headers)
            self.log.info('RestLib.get() - response status_code = ' + str(response.status_code))
            self.log.info('RestLib.get() - response headers = ' + str(response.headers))
            self.log.info('RestLib.get() - response url = ' + str(response.url))
        except requests.ConnectionError, e:
            self.log.info('RestLib.get() - ConnectionError : ' + str(e.message))
            response=None
        except requests.RequestException, e:
            self.log.info('RestLib.get() - RequestsException : ' + str(e.message))
            response=None
        assert response is not None, self.log.info('RestLib.get() - ASSERTION ERROR')
        return response

    def delete(self, base_url):
        '''
        :param base_url:
        :param kwargs:
        :return:
        '''
        self.log.info('RestLib.delete() is called with parameters: base_url=' + str(base_url))
        try:
            response=requests.delete(base_url)
            self.log.info('RestLib.delete() - status_code=' + str(response.status_code))
        except requests.ConnectionError, e:
            self.log.info('RestLib.delete() - ConnectionError : ' + str(e.message))
            response=None
        except requests.RequestException, e:
            self.log.info('RestLib.delete() - RequestsException : ' + str(e.message))
            response=None
        assert response is not None, self.log.info('RestLib.delete() - ASSERTION ERROR')
        return response

    def delete_source(self, base_url, source_url, source_id):
        '''
        :param base_url:
        :param source_url:
        :param source_id:
        :return: does not return anything
        '''
        #self.log.info('RestLib.delete_source() - sources path : get_chronograf_paths()')
        #path=self.get_chronograf_paths(base_url).get('sources')
        #assert path is not None, self.log.info('RestLib.delete_source() CANNOT GET sources path')
        self.log.info('RestLib.delete_source() is called with parameters: base_url='
                      + str(base_url) + ', path=' + str(source_url) + ', source id='
                      + str(source_id))
        url_to_delete=(base_url + source_url + os.path.sep + source_id)
        self.log.info('RestLib.delete_source() - URL=' + str(url_to_delete))
        response=self.delete(url_to_delete)
        assert response.status_code == 204, self.log.info('RestLib.delete_source() status_code='
                                                          + str(response.status_code) + ' message='
                                                          + str(response.json()))

    def patch(self, url, json, data=None, headers=None):
        '''
        :param url: endpoint url
        :param json: data that needs to be updated in json format
        :param data: optional
        :param headers: optional
        :return: response object
        '''
        self.log.info('RestLib.patch() is called with parameters: base_url=' + str(url) + ', json=' + str(json) +
                      ', data=' + str(data) + ', headers=' + str(headers))
        try:
            response=requests.patch(url, json=json, data=data, headers=headers)
            self.log.info('RestLib.patch() response code=' + str(response.status_code))
        except requests.ConnectionError, e:
            self.log.info('RestLib.patch() - ConnectionError : ' + str(e.message))
            response=None
        except requests.RequestException, e:
            self.log.info('RestLib.patch() - ConnectionError : ' + str(e.message))
            response=None
        assert response is not None, self.log.info('RestLib.patch() response is none')
        return response

    def patch_source(self, base_url, source_url, json, source_id, data=None, headers=None):
        '''
        :param base_url:
        :param source_url:
        :param json:
        :param source_id:
        :param data:
        :param headers:
        :return: response object
        '''
        #self.log.info('RestLib.patch_source() - sources path : get_chronograf_paths()')
        #path = self.get_chronograf_paths(base_url).get('sources')
        #assert path is not None, self.log.info('RestLib.patch_source() CANNOT GET sources path')
        self.log.info('RestLib.patch_source() is called with parameters: base_url='
                      + str(base_url) + ', path=' + str(source_url) + ', source id='
                      + str(source_id) + ', data=' + str(data) + ', headers=' + str(headers))
        url_to_update=(base_url + source_url + os.path.sep + source_id)
        response=self.patch(url_to_update, json, data=data, headers=headers)
        assert response.status_code == 200, self.log.info('RestLib.patch_source() status code='
                                                          + str(response.status_code) + ' message='
                                                          + str(response.json()))
        return response.json()

    def get_chronograf_paths(self, base_url):
        '''
        :param base_url:
        :return:
        '''

        chronograf_path = {}

        response = self.get(base_url, self.CHRONOGRAF_PATH)
        result = response.json()
        '''
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
        for key, value in result.items():
            self.log.info('RestLib.get_chronograf_paths() - add key/value ' + str(key) + '/' + str(value))
            chronograf_path[str(key)]= str(value)
        return chronograf_path

    def get_source_data(self, source, function):
        '''
        :param source: response body of the source (get/post)
        :param function: the calling function name
        :return: dictionary of source data
        '''
        # final sources dictionary
        sources={}
        # user facing name of the source
        source_name=source.get('name')
        # Chronograf UI requires NAME, but API is not (ask Chris Goller)
        if source_name is None:
            source_name=''
        self.log.info('RestLib.%s() NAME=' % function + str(source_name))
        # URL for the time series data source backend
        data_url=source.get('url')
        assert data_url is not None
        self.log.info('RestLib.%s() DATA NODE URL=' % function + str(data_url))
        # URL for the influxdb meta node
        meta_url=source.get('metaUrl')
        if meta_url is None:
            meta_url=''
        self.log.info('RestLib.%s() META NODE URL=' % function + str(meta_url))
        # Unique identifier representing a specific data source
        source_id=source.get('id')
        assert source_id is not None
        self.log.info('RestLib.%s() SOURCE ID=' % function + str(source_id))
        # Format of the data source - influx, influx-enterprise or influx-relay
        type=source.get('type')
        assert type in ['influx', 'influx-enterprise', 'influx-relay']
        self.log.info('RestLib.%s() FORMAT OF THE DATA SOURCE=' % function + str(type))
        default_source=source.get('default')
        assert default_source is not None
        self.log.info('RestLib.%s() IS SOURCE DEFAULT=' % function + str(default_source))
        # User Name for authenticating to data source
        username=source.get('username')
        if username is None:
            username=''
        self.log.info('RestLib.%s() USERNAME=' % function + str(username))
        # Password
        password=source.get('password')
        if password is None:
            password=''
        self.log.info('RestLib.%s() PASSWORD=' % function + str(password))
        # JWT signing secret for optional Authorization: Bearer to InfluxDB
        shared_secret=source.get('sharedSecret')
        if shared_secret is None:
            shared_secret=''
        self.log.info('RestLib.%s() SHARED SECRET=' % function + str(shared_secret))
        telegraf_db=source.get('telegraf')
        assert telegraf_db is not None
        self.log.info('RestLib.%s() TELEGRAF DB=' % function + str(telegraf_db))
        # Used for self-signed certificates. True or False (default is False)
        insecure_skip_verify=source.get('insecureSkipVerify')
        if insecure_skip_verify is None:
            insecure_skip_verify=False
        self.log.info('RestLib.%s() INSECURE SKIP VERIFY=' % function + str(insecure_skip_verify))
        # LINKS SECTION
        kapacitors_link=source.get('links')['kapacitors']
        assert kapacitors_link is not None
        self.log.info('RestLib.%s() KAPACITORS LINK=' % function + str(kapacitors_link))
        proxy_link=source.get('links')['proxy']
        assert proxy_link is not None
        self.log.info('RestLib.%s() PROXY LINK=' % function + str(proxy_link))
        write_link=source.get('links')['write']
        assert write_link is not None
        self.log.info('RestLib.%s() WRITE LINK=' % function + str(write_link))
        queries_link=source.get('links')['queries']
        assert queries_link is not None
        self.log.info('RestLib.%s() QUERIES LINK=' % function + str(queries_link))
        users_link=source.get('links')['users']
        assert users_link is not None
        self.log.info('RestLib.%s() USERS LINK=' % function + str(users_link))
        permissions_link=source.get('links')['permissions']
        assert permissions_link is not None
        self.log.info('RestLib.%s() PERMISSIONS LINK=' % function + str(permissions_link))
        roles_link=source.get('links')['roles']
        assert roles_link is not None
        self.log.info('RestLib.%s() ROLES LINK=' % function + str(roles_link))
        db_link=source.get('links')['databases']
        self.log.info('RestLib.%s() DATABASE LINK=' % function + str(db_link))
        assert db_link is not None
        sources[source_id]={'NAME': source_name, 'DATA_URL': data_url, 'META_URL': meta_url, 'TYPE': type,
                              'DEFAULT': default_source, 'USERNAME': username, 'PASSWORD': password,
                              'TELEGRAF_DB': telegraf_db, 'KAPACITOR': kapacitors_link, 'PROXY': proxy_link,
                              "WRITE": write_link, 'QUERY': queries_link, 'USERS': users_link,
                              'PERMISSIONS': permissions_link, 'ROLES': roles_link, 'SHARED_SECRET': shared_secret,
                              'INSECURE_SKIP_VERIFY': insecure_skip_verify, 'DBS': db_link}
        self.log.info('RestLib.%s FINAL SOURCE DICTIONARY FOR SOURCE ID=' % function + str(source_id) + ': ' +\
                      str(sources))
        return sources

    def get_kapacitor_data(self, kapacitor, function):
        '''
        :param kapacitor:
        :param function:
        :return:
        '''
        kapacitor_result={}
        # user facing name of kapacitor instance
        name=kapacitor.get('name')
        assert name is not None, self.log.info('RestLib.%s NAME IS NONE' % function)
        self.log.info('RestLib.%s NAME=' % function + name)
        username=kapacitor.get('username')
        if username is None: username=''
        self.log.info('RestLib.%s USERNAME=' % function + username)
        password=kapacitor.get('password')
        if password is None: password=''
        self.log.info('RestLib.%s PASSWORD=' % function + password)
        url=kapacitor.get('url')
        assert url is not None, self.log.info('RestLib.%s URL IS NONE' % function)
        self.log.info('RestLib.%s URL=' % function + url)
        active=kapacitor.get('active')
        assert active is not None, self.log.info('RestLib.%s ACTIVE IS NONE' % function)
        self.log.info('RestLib.%s ACTIVE=' % function + str(active))
        kapacitor_id=kapacitor.get('id')
        assert kapacitor_id is not None, self.log.info('RestLib.%s ID IS NONE' % function)
        self.log.info('RestLib.%s ID=' % function + kapacitor_id)
        rules_link=kapacitor.get('links').get('rules')
        self.log.info('RestLib.%s RULES_LINK=' % function + rules_link)
        tasks_link=kapacitor.get('links').get('tasks')
        self.log.info('RestLib.%s TASKS_LINK=' % function + tasks_link)
        ping_link=kapacitor.get('links').get('ping')
        self.log.info('RestLib.%s PING_LINK=' % function + ping_link)
        proxy_link=kapacitor.get('links').get('proxy')
        self.log.info('RestLib.%s PROXY_LINK=' % function + proxy_link)
        kapacitor_result[kapacitor_id]={'NAME':name, 'USERNAME':username, 'PASSWORD':password, 'URL':url,
                                        'ACTIVE':active, 'RULES':rules_link, 'TASKS':tasks_link,
                                        'PING':ping_link, 'PROXY':proxy_link}
        self.log.info('RestLib.%s RESULT KAPACITOR =' % function + str(kapacitor_result))
        return kapacitor_result

    def create_source(self, base_url, source_url, json):
        '''
        :param base_url: the URL of chronograf, e.g. http://12.34.56.78:8888
        :param source_url: the URL of the source
        :param json: request body in JSON format, e.g.:
                     '{"url":"http://54.149.168.44:8086"}' - URL is required
                      Other options for data sources creation
        :return: (response.status_code, result['message], source_id) if source was created successfully then
                 result['message'] will be empty and status code and source_id won't and if source was not created
                 successfully then status code and result['message'] won't be ampty and source_id will be.
        '''
        #chronograf_path = self.get_chronograf_paths(base_url)
        #source_path = chronograf_path.get('sources')
        #self.log.info('RestLib.create_source() - source_path=' + str(source_path))
        #assert source_path is not None, self.log.info('RestLib.create_source() - source path is None')
        response=self.post(base_url, source_url, json)
        try:
            source_id = response.json().get('id')
            if source_id is not None:
                self.log.info('RestLib.create_source() - Source ID = ' + str(source_id))
                return (response.status_code, '', source_id)
            else:
                self.log.info('RestLib.create_source() - Source ID is None')
                return (response.status_code, response.json()['message'], source_id)
        # if JSON object cannot be decoded, the Value Error is raised.
        except ValueError, e:
            self.log.info('RestLib.create_source() - Value Error :' + str(e.message))
            return (response.status_code, response.json()['message'], None)

    def get_sources(self, base_url, source_url):
        '''
        :param base_url:
        :param source_url:
        :return:
        '''
        sources ={}

        # get list of sources (one source example):
        '''
        telegraf --> telegraf
        name --> data1
        links --> {u'users': u'/chronograf/v1/sources/7/users', u'roles': u'/chronograf/v1/sources/7/roles', 
            u'self': u'/chronograf/v1/sources/7', u'databases': u'/chronograf/v1/sources/7/dbs', 
            u'write': u'/chronograf/v1/sources/7/write', u'proxy': u'/chronograf/v1/sources/7/proxy', 
            u'kapacitors': u'/chronograf/v1/sources/7/kapacitors', u'queries': u'/chronograf/v1/sources/7/queries', 
            u'permissions': u'/chronograf/v1/sources/7/permissions'}
        url --> http://34.211.191.81:8086 -- connection data node
        metaUrl --> http://52.10.58.119:8091 --connection meta node
        default --> True
        type --> influx-enterprise
        id --> 7
        '''
        #chronograf_path=self.get_chronograf_paths(base_url)
        #source_path = chronograf_path.get('sources')
        #assert source_path is not None, self.log.info('RestLib.get_sources() - source path is None')
        response = self.get(base_url, source_url)
        # get the list of all existing sources
        result = response.json()['sources']
        if len(result) == 0:
            return sources
        elif len(result) == 1:
            sources=self.get_source_data(result[0], 'get_sources')
        else:
            for source in result:
                temp_source=self.get_source_data(source, 'get_sources')
                key=''.join(temp_source.keys())
                values=temp_source[key]
                sources[key]=values
        self.log.info('RestLib.get_sources() FINAL SOURCES : ' + str(sources))
        return sources

    def get_source(self, base_url, source_url, source_id):
        '''
        :param base_url: Chronograf URL
        :param source_url: path to a source URL
        :param source_id: id of the created source
        :return:
        '''
        self.log.info('rest_lib.RestLib:get_source() START')
        #source_result = {}
        #self.log.info('rest_lib.RestLib:get_source() : STEP 1 - GET CHRONOGRAF PATHS')
        #chronograf_path = self.get_chronograf_paths(base_url)
        #source_path = chronograf_path.get('sources')
        #self.log.info('rest_lib.RestLib:get_source() : STEP 2 - GET SOURCE PATH = ' + str(source_path))
        #assert source_path is not None, self.log.info('RestLib.get_sources() - source path is None')
        source_path=source_url + os.path.sep + source_id
        self.log.info('rest_lib.RestLib:get_source() : STEP 1 - GET ' + str(base_url) + str(source_path) + ' URL')
        response = self.get(base_url, source_path)
        # get the list of a source eith id = source_id
        source = response.json()
        self.log.info('rest_lib.RestLib:get_source() : STEP 2 - GET ALL OF THE RESPONSE DATA')
        return self.get_source_data(source, 'get_source')

    def create_kapacitor(self, base_url, kapacitor_url, json):
        '''
        :param base_url: url of the chronograf
        :param source_url: path to a source url
        :param json: request body in JSON format
        :return: tuple of (status, message, kapacitor_id), where status is a status of the request, message -
                 if any error return message, id of the kapacitor if it was created successfully, otherwise - None
        '''

        self.log.info('RestLib.create_kapacitor() - create a POST requests with following params: base_url=' + str(base_url)
                      + ', kapacitor_url=' + str(kapacitor_url) + ', json=' + str(json))
        response=self.post(base_url, kapacitor_url, json)
        try:
            kapacitor_id=response.json().get('id')
            if kapacitor_id is not None:
                self.log.info('RestLib.create_kapacitor() Kapacitor ID=' + str(kapacitor_id))
                return (response.status_code, '', kapacitor_id)
            else:
                self.log.info('RestLib.create_kapacitor() Kapacitor ID is None')
                return (response.status_code, response.json()['message'], None)
        except ValueError, e:
            self.log.info('RestLib.create_kapacitor() ValueError = ' + str(e.message))
            return (response.status_code, response.json()['message'], None)

    def get_kapacitor(self, base_url, kapacitor_url, kapacitor_id):
        '''
        :param base_url: URL of the chronograf
        :param kapacitor_url: path to a kapacitor URL for a specific source
        :param kapacitor_id: id of the created kapacitor
        :return: dictionary of the response data
        '''
        self.log.info('RestLib.get_kapacitor() METHOD IS BEING CALLED')
        kapacitor_path=kapacitor_url + os.path.sep + kapacitor_id
        self.log.info('rest_lib.RestLib:get_source() : STEP 1 - GET ' + str(base_url) + str(kapacitor_path) + ' URL')
        response=self.get(base_url, kapacitor_path)
        # get the list of a kapacitor with id = kapacitor_id
        kapacitor_result=response.json()
        self.log.info('rest_lib.RestLib:get_source() : STEP 2 - GET ALL OF THE RESPONSE DATA')
        return self.get_kapacitor_data(kapacitor_result, 'get_kapacitor')



