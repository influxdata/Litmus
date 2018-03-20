
import requests, os
from src.chronograf.lib.base_lib import BaseLib



class RestLib(BaseLib):
    '''
    TODO
    '''

    CHRONOGRAF_PATH = '/chronograf/v1' # Should we make it as option passed to master script???

    ############################################# GENERIC HTTP methods #################################################

    def post(self, base_url, path, json=None, data=None, headers=None):
        '''
        :param base_url:Chronograf URL, e.g http://<ip>:<port>
        :param path:path to post url
        :param json:JSON object containiong post data
        :param data:dictionary containing post data
        :param headers: any custom headers for post request
        :return:response object
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
        :param base_url:Chronograf URL, e.g. http://<IP>:<PORT>, where PORT=8888 (default)
        :param path:path to get url
        :param params: (optional) Dictionary to be sent in the query string for the request
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

    def delete(self, base_url, path):
        '''
        :param base_url:Chronograf URL, e.g. http://<IP>:<PORT>, where PORT=8888 (default)
        :param path: path to delete url
        :return:response object
        '''
        self.log.info('RestLib.delete() is called with parameters: base_url=' + str(base_url) + ', path=' + str(path))
        try:
            response=requests.delete(base_url + path)
            self.log.info('RestLib.delete() - status_code=' + str(response.status_code))
        except requests.ConnectionError, e:
            self.log.info('RestLib.delete() - ConnectionError : ' + str(e.message))
            response=None
        except requests.RequestException, e:
            self.log.info('RestLib.delete() - RequestsException : ' + str(e.message))
            response=None
        assert response is not None, self.log.info('RestLib.delete() - ASSERTION ERROR')
        return response

    def patch(self, base_url, path, json=None, data=None, headers=None):
        '''
        :param base_url:chronograf URL, e.g. http://<IP>:<PORT>, where PORT=8888
        :param path:path to patch url
        :param json: data that needs to be updated in json format
        :param data: data that needs to be updated in dictionary format
        :param headers: optional
        :return: response object
        '''
        self.log.info('RestLib.patch() is called with parameters: base_url=' + str(base_url) + ', json=' + str(json) +
                      ', data=' + str(data) + ', headers=' + str(headers))
        try:
            response=requests.patch(base_url + path, json=json, data=data, headers=headers)
            self.log.info('RestLib.patch() response code=' + str(response.status_code))
        except requests.ConnectionError, e:
            self.log.info('RestLib.patch() - ConnectionError : ' + str(e.message))
            response=None
        except requests.RequestException, e:
            self.log.info('RestLib.patch() - ConnectionError : ' + str(e.message))
            response=None
        assert response is not None, self.log.info('RestLib.patch() response is none')
        return response

    ####################################################################################################################

    def get_chronograf_paths(self, base_url): # this method is used as a fixure for chronograf regression tests. Should
                                              # it be moved to a root conftest.py so every other method/function has an
                                              # access to it????
        '''
        :param base_url: Chronograf URL, e.g. http://<ip>:<port>, right now using default port 8888
        :return: dictionary of URLS, where key is a name of the url and key is a path
        '''
        chronograf_path = {} # result dictionary

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
            self.log.info('RestLib.get_chronograf_paths() - add key/value : ' + str(key) + '/' + str(value))
            chronograf_path[str(key)]= str(value)
        return chronograf_path

    ################################### SOURCES METHODS (create, get, pathc, delete) ###################################

    def get_source_data(self, source, function):
        '''
        :param source:response body of the source request(get/post)
        :param function:the calling function name
        :return: dictionary of source data response
        '''
        '''
        default:true
        id:"22"
        links:{
            databases:"/chronograf/v1/sources/22/dbs"
            kapacitors:"/chronograf/v1/sources/22/kapacitors"
            permissions:"/chronograf/v1/sources/22/permissions"
            proxy:"/chronograf/v1/sources/22/proxy"
            queries:"/chronograf/v1/sources/22/queries"
            roles:"/chronograf/v1/sources/22/roles"
            self:"/chronograf/v1/sources/22"
            users:"/chronograf/v1/sources/22/users"
            write:"/chronograf/v1/sources/22/write"
            metaUrl:"http://52.39.201.97:8091"
        }
            name:"CREATE KAPACITOR"
            telegraf:"telegraf"
            type:"influx-enterprise"
            url:"http://35.167.39.127:8086"
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
        kapacitors_link=source.get('links').get('kapacitors')
        assert kapacitors_link is not None
        self.log.info('RestLib.%s() KAPACITORS LINK=' % function + str(kapacitors_link))
        proxy_link=source.get('links').get('proxy')
        assert proxy_link is not None
        self.log.info('RestLib.%s() PROXY LINK=' % function + str(proxy_link))
        write_link=source.get('links').get('write')
        assert write_link is not None
        self.log.info('RestLib.%s() WRITE LINK=' % function + str(write_link))
        queries_link=source.get('links').get('queries')
        assert queries_link is not None
        self.log.info('RestLib.%s() QUERIES LINK=' % function + str(queries_link))
        users_link=source.get('links').get('users')
        assert users_link is not None
        self.log.info('RestLib.%s() USERS LINK=' % function + str(users_link))
        permissions_link=source.get('links').get('permissions')
        assert permissions_link is not None
        self.log.info('RestLib.%s() PERMISSIONS LINK=' % function + str(permissions_link))
        roles_link=source.get('links').get('roles')
        if roles_link is None:
            roles_link=None
        self.log.info('RestLib.%s() ROLES LINK=' % function + str(roles_link))
        db_link=source.get('links').get('databases')
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

    def create_source(self, base_url, source_url, json):
        '''
        :param base_url: the URL of chronograf, e.g. http://12.34.56.78:8888
        :param source_url:the URL of the source, e.g. /chronograf/v1/sources
        :param json: request body in JSON format, e.g.:
                     '{"url":"http://54.149.168.44:8086"}' - URL is required
                      Other options for data sources creation
        :return: (response.status_code, result['message], source_id) if source was created successfully then
                 result['message'] will be empty and status code and source_id won't and if source was not created
                 successfully then status code and result['message'] won't be ampty and source_id will be.
        '''
        response=self.post(base_url, source_url, json)
        try:
            source_id = response.json().get('id')
            if source_id is not None:
                self.log.info('RestLib.create_source() - Source ID = ' + str(source_id))
                return (response.status_code, response.json(), source_id)
            else:
                self.log.info('RestLib.create_source() - Source ID is None')
                return (response.status_code, response.json()['message'], source_id)
        # if JSON object cannot be decoded, the Value Error is raised.
        except ValueError, e:
            self.log.info('RestLib.create_source() - Value Error :' + str(e.message))
            return (response.status_code, response.json()['message'], None)

    def get_source(self, base_url, source_url, source_id):
        '''
        :param base_url:Chronograf URL, e.g. http://<IP>:<PORT>
        :param source_url:path to a source URL, e.g. /chronograf/v1/sources
        :param source_id:id of the created source
        :return:dictionary of response data
        '''
        self.log.info('rest_lib.RestLib:get_source() START')
        # http://<chronograf IP>:8888/chronograf/v1/sources/{id}, where /chronograf/v1/sources/{id} is
        # source_url + os.path.sep + source_id
        source_path=source_url + os.path.sep + source_id
        self.log.info('rest_lib.RestLib:get_source() : STEP 1 - GET ' + str(base_url) + str(source_path) + ' URL')
        response = self.get(base_url, source_path)
        # get the list of a source with id = source_id
        source = response.json()
        self.log.info('rest_lib.RestLib:get_source() : STEP 2 - GET ALL OF THE RESPONSE DATA')
        return self.get_source_data(source, 'get_source')

    def get_sources(self, base_url, source_url):
        '''
        :param base_url:Chronograf URL, e.g. http://<IP>:<PORT>
        :param source_url:path to a source URL, e.g. /chronograf/v1/sources
        :return:dictionary of response data for all of the existing sources, where dictionary key is a source ID
        '''
        sources={}
        self.log.info('rest_lib.RestLib:get_sources() START')
        # http://<Chronograf IP>:8888/chronograf/v1/sources
        self.log.info('rest_lib.RestLib:get_sources() : STEP 1 - GET ' + str(base_url) + str(source_url) + ' URL')
        response=self.get(base_url, source_url)
        # get the list of all existing sources
        result=response.json()['sources']
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

    def delete_source(self, base_url, source_url, source_id):
        '''
        :param base_url:Chronograf URL, e.e http://<IP>:<PORT>, where PORT=8888 (default)
        :param source_url:the URL of the source, e.g. /chronograf/v1/sources
        :param source_id:ID of the source to be deleted
        :return:does not return anything, asserts status_code is 204
        '''
        self.log.info('RestLib.delete_source() is called with parameters: base_url='
                      + str(base_url) + ', path=' + str(source_url) + ', source id='
                      + str(source_id))
        # http://34.211.227.112:8888/chronograf/v1/sources/{id}, where 34.211.227.112 IP of chronograf and
        # /chronograf/v1/sources/{id} is source_url + source ID to be deleted
        url_to_delete=(source_url + os.path.sep + source_id)
        self.log.info('rest_lib.RestLib:delete_source() : STEP 1 - DELETE ' + str(base_url) +
                      str(url_to_delete) + ' URL')
        response=self.delete(base_url, url_to_delete)
        assert response.status_code == 204, self.log.info('RestLib.delete_source() status_code='
                                                          + str(response.status_code) + ' message='
                                                          + str(response.json()))

    def patch_source(self, base_url, source_url, json, source_id, data=None, headers=None):
        '''
        :param base_url:chronograf URL, e.g. http://<IP>:<PORT>, where PORT=8888
        :param source_url:path to a source URL, e.g. /chronograf/v1/sources
        :param json:data to be updated in JSON format
        :param source_id:id of the source to be updated
        :param data: =data to be updated as dictionary
        :param headers: optional
        :return: response object
        '''
        self.log.info('RestLib.patch_source() is called with parameters: base_url='
                      + str(base_url) + ', path=' + str(source_url) + ', json=' + str(json) + ', source id='
                      + str(source_id) + ', data=' + str(data) + ', headers=' + str(headers))
        url_to_update=(source_url + os.path.sep + source_id)
        # http://34.211.227.112:8888/chronograf/v1/sources/{id}, where url_to_update is /chronograf/v1/sources/{id}
        response=self.patch(base_url, url_to_update, json, data=data, headers=headers)
        assert response.status_code == 200, self.log.info('RestLib.patch_source() status code='
                                                          + str(response.status_code) + ' message='
                                                          + str(response.json()))
        return response.json()

    def get_kapacitor_data(self, kapacitor, function):
        '''
        :param kapacitor:kapacitor response object
        :param function:the calling function's name
        :return: dictionary of kapacitor response object
        '''
        '''
        active:true
        id:"8"
        links:{
            ping:"/chronograf/v1/sources/22/kapacitors/8/proxy?path=/kapacitor/v1/ping"
            proxy:"/chronograf/v1/sources/22/kapacitors/8/proxy"
            rules:"/chronograf/v1/sources/22/kapacitors/8/rules"
            self:"/chronograf/v1/sources/22/kapacitors/8"
            tasks:"/chronograf/v1/sources/22/kapacitors/8/proxy?path=/kapacitor/v1/tasks"
            name:"My Kapacitor1234"
            url:"http://54.186.88.103:9092"
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

    def create_kapacitor(self, base_url, kapacitor_url, json):
        '''
        :param base_url: url of the chronograf
        :param kapacitro_url: path to a kapacitor url
        :param json: request body in JSON format
        :return: tuple of (status, message, kapacitor_id), where status is a status of the request, message -
                 if any error return message, id of the kapacitor if it was created successfully, otherwise - None
        '''
        '''
        kapacitor response object for successfully created kapacitor
        active:true
        id:"8"
        links:{
            ping:"/chronograf/v1/sources/22/kapacitors/8/proxy?path=/kapacitor/v1/ping"
            proxy:"/chronograf/v1/sources/22/kapacitors/8/proxy"
            rules:"/chronograf/v1/sources/22/kapacitors/8/rules"
            self:"/chronograf/v1/sources/22/kapacitors/8"
            tasks:"/chronograf/v1/sources/22/kapacitors/8/proxy?path=/kapacitor/v1/tasks"
        }
            name:"My Kapacitor1234"
            url:"http://54.186.88.103:9092"
        '''

        self.log.info('RestLib.create_kapacitor() - create a POST requests with following params: base_url=' + str(base_url)
                      + ', kapacitor_url=' + str(kapacitor_url) + ', json=' + str(json))
        response=self.post(base_url, kapacitor_url, json)
        try:
            kapacitor_id=response.json().get('id')
            if kapacitor_id is not None:
                self.log.info('RestLib.create_kapacitor() Kapacitor ID=' + str(kapacitor_id))
                return (response.status_code, response.json(), kapacitor_id)
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
        # http://34.211.227.112:8888/chronograf/v1/sources/{id}/kapacitors/{kapa_id}, where
        # /chronograf/v1/sources/{id}/kapacitors is kapacitor path for a specific source and {kapa_id} is a kapacitor id
        kapacitor_result=response.json()
        self.log.info('rest_lib.RestLib:get_source() : STEP 2 - GET ALL OF THE RESPONSE DATA')
        return self.get_kapacitor_data(kapacitor_result, 'get_kapacitor')

    def get_kapacitors(self, base_url, kapacitor_url):
        '''
        :param base_url:URL of the chronograf
        :param kapacitor_url:path to a kapacitor URL for a specific source
        :return:dictionary of response data for all existing kapacitors for a specific source
        '''
        kapacitors={}
        self.log.info('rest_lib.RestLib.get_kapacitors() START')
        # http://34.211.227.112:8888/chronograf/v1/sources/{id}/kapacitors
        self.log.info('rest_lib.RestLib:get_kapacitors() : STEP 1 - GET ' + str(base_url) + str(kapacitor_url) + ' URL')
        response=self.get(base_url, kapacitor_url)
        # get the list of all of the existing kapacitors
        result = response.json()['kapacitors']
        if len(result) == 0:
            return kapacitors
        elif len(result) == 1:
            kapacitors=self.get_kapacitor_data(result[0], 'get_kapacitors')
        else:
            for kapacitor in result:
                temp_kapacitor=self.get_kapacitor_data(kapacitor, 'get_kapacitors')
                key=''.join(temp_kapacitor.keys())
                values=temp_kapacitor[key]
                kapacitors[key]=values
        self.log.info('RestLib.get_kapacitors() FINAL KAPACITORS : ' + str(kapacitors))
        return kapacitors

    def patch_kapacitor(self, base_url, kapacitor_url, kapacitor_id, json=None, data=None, headers=None):
        '''
        :param base_url:chronograf URL, e.g. http://<IP>:<PORT>, where PORT=8888
        :param kapacitor_url:path to a kapacitor url for a specific source: /chronograf/v1/sources/<source id>/kapacitors
        :param json:data to update in JSON format
        :param kapacitor_id:ID of a kapacitor to be updated
        :param data:data to update in dictionary format
        :param headers:optional
        :return:response object
        '''
        self.log.info('RestLib.patch_kapacitor() is called with parameters: base_url='
                      + str(base_url) + ', path=' + str(kapacitor_url) + ', kapacitor id='
                      + str(kapacitor_id) + ', json=' + str(json) + ', data=' + str(data) + ', headers=' + str(headers))
        url_to_update=(kapacitor_url + os.path.sep + kapacitor_id)
        # http://34.211.227.112:8888/chronograf/v1/sources/{id}, where url_to_update is /chronograf/v1/sources/{id}
        response = self.patch(base_url, url_to_update, json, data=data, headers=headers)
        assert response.status_code == 200, self.log.info('RestLib.patch_kapacitor() status code='
                                                          + str(response.status_code) + ' message='
                                                          + str(response.json()))
        return response.json()

    def delete_kapacitor(self, base_url, kapacitor_url, kapacitor_id):
        '''
        :param base_url:Chronograf URL, e.e http://<IP>:<PORT>, where PORT=8888 (default)
        :param kapacitor_url:url of a kapacitor, e.g. /chronograf/v1/sources/<source id>/kapacitors
        :param kapacitor_id:ID of a kapacitor to be deleted
        :return: does not return anything, asserts status code is 204
        '''
        self.log.info('RestLib.delete_kapacitor() is called with parameters: base_url='
                      + str(base_url) + ', kapacitor_url=' + str(kapacitor_url) + ', kapacitor id='
                      + str(kapacitor_id))
        # http://34.211.227.112:8888/chronograf/v1/kapacitors/{id}, where 34.211.227.112 IP of chronograf and
        # /chronograf/v1/kapacitors/{id} is kapacitor_url + kapacitor ID to be deleted
        url_to_delete = (kapacitor_url + os.path.sep + kapacitor_id)
        self.log.info('rest_lib.RestLib:delete_kapacitor() : STEP 1 - DELETE ' + str(base_url) +
                      str(url_to_delete) + ' URL')
        response = self.delete(base_url, url_to_delete)
        assert response.status_code == 204, self.log.info('RestLib.delete_kapacitor() status_code='
                                                          + str(response.status_code) + ' message='
                                                          + str(response.json()))
