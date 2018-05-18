import requests
from src.chronograf.lib.base_lib import BaseLib


class InfluxDBInfluxDBRestLib(BaseLib):
    '''
    defines generic - post, get, delete and patch methods (built on top of requests library)
    '''


    ############################################# GENERIC HTTP methods #################################################

    def post(self, base_url, path, json=None, data=None, headers=None, auth=None):
        '''
        :param base_url:meta node url, e.g http://<metanode>:<8091>
        :param path:path to post url
        :param json:JSON object containiong post data
        :param data:dictionary containing post data
        :param headers: any custom headers for post request
        :return:response object
        '''
        self.log.info('InfluxDBRestLib.post() is called with parameters: base_url=' + str(base_url) + ', path=' + str(path)
                      + ', json=' + str(json) + ', auth=' + str(auth))
        try:
            response = requests.post(base_url + path, json=json, data=data, headers=headers, auth=auth)
            self.log.info('InfluxDBRestLib.post() response code=' + str(response.status_code))
            # TODO add more logging
        except requests.ConnectionError, e:
            self.log.info('InfluxDBRestLib.post() - ConnectionError : ' + str(e.message))
            response = None
        except requests.RequestException, e:
            self.log.info('InfluxDBRestLib.post() - RequestsException : ' + str(e.message))
            response = None
        assert response is not None, self.log.info('SOME ERROR MESSAGE FOR POST')
        return response

    def get(self, base_url, path, params=None, headers=None, auth=None):
        '''
        :param base_url:Chronograf URL, e.g. http://<IP>:<PORT>, where PORT=8888 (default)
        :param path:path to get url
        :param params: (optional) Dictionary to be sent in the query string for the request
        :param headers
        :param auth
        :return: response object
        '''
        self.log.info('InfluxDBRestLib.get() is called with parameters: base_url = '
                      + str(base_url) + ', path = ' + str(path) + ', params = '
                      + str(params) + ', headers= ' + str(headers) + ', auth=' + str(auth))
        try:
            response = requests.get(base_url + path, params=params, headers=headers, auth=auth)
            self.log.info('InfluxDBRestLib.get() - response status_code = ' + str(response.status_code))
            self.log.info('InfluxDBRestLib.get() - response headers = ' + str(response.headers))
            self.log.info('InfluxDBRestLib.get() - response url = ' + str(response.url))
        except requests.ConnectionError, e:
            self.log.info('InfluxDBRestLib.get() - ConnectionError : ' + str(e.message))
            response = None
        except requests.RequestException, e:
            self.log.info('InfluxDBRestLib.get() - RequestsException : ' + str(e.message))
            response = None
        except requests.exceptions, e:
            self.log.info('InfluxDBRestLib.get() - RequestsException : ' + str(e.message))
            response = None
        assert response is not None, self.log.info('InfluxDBRestLib.get() - ASSERTION ERROR')
        return response

    def delete(self, base_url, path, auth=None):
        '''
        :param base_url:meta node url, e.g. http://<IP>:<PORT>, where PORT=8091 (default)
        :param path: path to delete url
        :param auth
        :return:response object
        '''
        self.log.info('InfluxDBRestLib.delete() is called with parameters: base_url=' +
                      str(base_url) + ', path=' + str(path))
        try:
            response = requests.delete(base_url + path, auth=auth)
            self.log.info('InfluxDBRestLib.delete() - status_code=' + str(response.status_code))
        except requests.ConnectionError, e:
            self.log.info('InfluxDBRestLib.delete() - ConnectionError : ' + str(e.message))
            response = None
        except requests.RequestException, e:
            self.log.info('InfluxDBRestLib.delete() - RequestsException : ' + str(e.message))
            response = None
        assert response is not None, self.log.info('InfluxDBRestLib.delete() - ASSERTION ERROR')
        return response

    def patch(self, base_url, path, json=None, data=None, headers=None, auth=None):
        '''
        :param base_url:chronograf URL, e.g. http://<IP>:<PORT>, where PORT=8888
        :param path:path to patch url
        :param json: data that needs to be updated in json format
        :param data: data that needs to be updated in dictionary format
        :param headers: optional
        :param auth
        :return: response object
        '''
        self.log.info('InfluxDBRestLib.patch() is called with parameters: base_url='
                      + str(base_url) + ', path=' + str(path) + ', json=' + str(json) +
                      ', data=' + str(data) + ', headers=' + str(headers) + ', auth=' + str(auth))
        try:
            response = requests.patch(base_url + path, json=json, data=data, headers=headers)
            self.log.info('InfluxDBRestLib.patch() response code=' + str(response.status_code))
        except requests.ConnectionError, e:
            self.log.info('InfluxDBRestLib.patch() - ConnectionError : ' + str(e.message))
            response = None
        except requests.RequestException, e:
            self.log.info('InfluxDBRestLib.patch() - ConnectionError : ' + str(e.message))
            response = None
        assert response is not None, self.log.info('InfluxDBRestLib.patch() response is none')
        return response

    ####################################################################################################################

    def get_leader_meta_url(self, meta_url, auth=None):
        '''
        :param meta_url:
        :param auth:
        :return:
        '''
        self.log.info('InfluxDBInfluxDBRestLib.get_leader_meta_url() FUNCTION IS CALLED')
        self.log.info('================================================================')
        success=False
        message=''
        meta_leader_node=''
        response=self.get(meta_url, '/status', auth=auth)
        if response.status_code == 200:
            success=True
            meta_leader_node=response.json()['leader']
            self.log.info('InfluxDBInfluxDBRestLib.get_leader_meta_url() meta_leader_node=' + str(meta_leader_node))
        else:
            message=response.text
        self.log.info('InfluxDBInfluxDBRestLib.get_leader_meta_url() success=' + str(success))
        self.log.info('InfluxDBInfluxDBRestLib.get_leader_meta_url() FUNCTION IS DONE')
        self.log.info('==============================================================')
        return (success, meta_leader_node, message)

    def create_role(self, meta_leader_url, role_name, auth=None):
        '''
        :param meta_url:
        :param role_name:
        :param auth:
        :return:
        '''
        self.log.info('InfluxDBInfluxDBRestLib.create_role() FUNCTION IS CALLED')
        self.log.info('========================================================')
        success=False
        message=''
        data={'action':'create', 'role':{'name':role_name}}
        response=self.post(meta_leader_url, '/role', json=data, auth=auth)
        if response.status_code == 200:
            success=True
        else:
            message=response.json()
        self.log.info('InfluxDBInfluxDBRestLib.create_role() success=' + str(success))
        self.log.info('InfluxDBInfluxDBRestLib.create_role() FUNCTION IS DONE')
        self.log.info('======================================================')
        return (success, message)

    def delete_role(self, meta_leader_url, role_name, auth=None):
        '''
        :param meta_url:
        :param role_name:
        :return:
        '''
        self.log.info('InfluxDBInfluxDBRestLib.delete_role() FUNCTION IS CALLED')
        self.log.info('========================================================')
        success = False
        message = ''
        data = {'action': 'delete', 'role': {'name': role_name}}
        response = self.post(meta_leader_url, '/role', json=data, auth=auth)
        if response.status_code == 200:
            success = True
        else:
            message = response.json()
        self.log.info('InfluxDBInfluxDBRestLib.delete_role() success=' + str(success))
        self.log.info('InfluxDBInfluxDBRestLib.delete_role() FUNCTION IS DONE')
        self.log.info('======================================================')
        return (success, message)

    def get_roles(self):
        pass

    def get_role(self):
        pass

    def add_role_permissions(self, meta_leader_url, role_name, scope, permissions, auth=None):
        '''
        :param meta_url: URL of the meta node
        :param role_name: name of the role (str)
        :param scope: 'database' or 'all', if scope=database, then scope=<name of the database>
                      if scope=all, then scope=''
        :param permissions: list of cluster permissions
        :return:
        '''
        self.log.info('InfluxDBInfluxDBRestLib.add_role_permissions() FUNCTION IS CALLED')
        self.log.info('=================================================================')
        success = False
        message = ''
        data = {'action': 'add-permissions', 'role': {'name': role_name, 'permissions':{scope:permissions}}}
        response = self.post(meta_leader_url, '/role', json=data, auth=auth)
        if response.status_code == 200:
            success = True
        else:
            message = response.json()
        self.log.info('InfluxDBInfluxDBRestLib.add_role_permissions() success=' + str(success))
        self.log.info('InfluxDBInfluxDBRestLib.add_role_permissions() FUNCTION IS DONE')
        self.log.info('===============================================================')
        return (success, message)

    ############################################### SUBSCRIPTIONS ######################################################

    def create_subscription(self, data_url, subscription_name, database, retention_policy,
                            subscription_mode, destinations, auth=None):
        '''
        :param data_url:
        :param subscription_name:
        :param database:
        :param retention_policy:
        :param subscription_mode:
        :param destinations:
        :param auth:
        :return:
        '''
        success=False
        message=None
        self.log.info('InfluxDBInfluxDBRestLib.create_subscription() FUNCTION IS CALLED')
        self.log.info('================================================================')
        create_subscription_stmt='CREATE SUBSCRIPTION "%s" ON "%s"."%s" DESTINATIONS %s %s' \
                        % (subscription_name, database, retention_policy, subscription_mode, destinations)
        self.log.info('InfluxDBInfluxDBRestLib.create_subscription() CREATE SUBSCRIPTION STATEMENT : '
                        + str(create_subscription_stmt))
        path='/query?q=%s' % create_subscription_stmt
        response=self.post(data_url, path, auth=auth)
        if response.status_code == 200:
            result=response.json()['results'][0]
            if result.get('error') is None:
                success=True
            else:
                message=result.get('error')
        else:
            message=response.text
            self.log.info('InfluxDBInfluxDBRestLib.create_subscription() error message=' + str(message))
            self.log.info('============================================================')
        self.log.info('InfluxDBInfluxDBRestLib.create_subscription() FUNCTION IS DONE')
        self.log.info('==============================================================')
        return (success, message)

    def show_subscriptions(self, data_url, auth=None):
        '''
        :param data_url:
        :return:
        '''
        success=False
        message=''
        subscriptions_d={}
        subscrpiton_values_d={}
        self.log.info('InfluxDBInfluxDBRestLib.show_subscriptions() FUNCTION IS CALLED')
        self.log.info('==============================================================')
        response=self.get(data_url,'/query?q=SHOW SUBSCRIPTIONS', auth=auth)
        if response.status_code == 200:
            success=True
        else:
            message=response.text
            return (success, message, subscriptions_d)
        results_l=response.json().get('results') # returns list of dictionary(is)
        self.log.info('InfluxDBInfluxDBRestLib.show_subscriptions() - '
                      'GET RESULTS ' + str(results_l))
        for result in results_l:
            subscriptions_l=result.get('series')
            self.log.info('InfluxDBInfluxDBRestLib.show_subscriptions() - '
                          'GET SUBSCRIPTION LIST ' + str(subscriptions_l))
            for subscrpiton in subscriptions_l:
                subscription_db_name=subscrpiton.get('name')
                self.log.info('InfluxDBInfluxDBRestLib.show_subscriptions() - '
                              'DB SUBSCRIPTION NAME=' + subscription_db_name)
                values=subscrpiton.get('values') # list of lists
                self.log.info('InfluxDBInfluxDBRestLib.show_subscriptions() - GET SUBSCRIPTION VALUES=' + str(values))
                # [
                #   [u'autogen', u'kapacitor-0e733c36-6c13-469a-87b1-c3a51f8b78cd', u'ANY', [u'http://10.0.173.74:9092']],
                #   [u'autogen', u'test', u'ALL', [u'http://10.0.173.74:9092']],
                #   [u'autogen', u'test_1', u'ALL', [u'http://1.2.3.4:9092']]
                # ]
                for value in values: #value is a list
                    retention_policy=value[0]
                    self.log.info('InfluxDBInfluxDBRestLib.show_subscriptions() RETENTION POLICY = '
                                  + str(retention_policy))
                    subscription_name=value[1]
                    self.log.info('InfluxDBInfluxDBRestLib.show_subscriptions() SUBSCRIPTION NAME = '
                                  + str(subscription_name))
                    subscription_mode=value[2]
                    self.log.info('InfluxDBInfluxDBRestLib.show_subscriptions() SUBSCRIPTION MODE = '
                                  + str(subscription_mode))
                    subscription_destination=value[3] # list of IPs of kapacitor
                    self.log.info('InfluxDBInfluxDBRestLib.show_subscriptions() SUBSCRIPTION DESTINATIONS = '
                                  + str(subscription_destination))
                    subscrpiton_values_d[subscription_name]={'rp':retention_policy, 'mode':subscription_mode,
                                                             'destination':subscription_destination}
                    self.log.info('InfluxDBInfluxDBRestLib.show_subscriptions() SUBSCRIPTION VALUES = '
                                  + str(subscrpiton_values_d))
                subscriptions_d[subscription_db_name]=subscrpiton_values_d
                self.log.info('InfluxDBInfluxDBRestLib.show_subscriptions() SUBSCRIPTIONS FOR DB = '
                              + str(subscriptions_d))
        self.log.info('InfluxDBInfluxDBRestLib.show_subscriptions() FUNCTION IS DONE')
        self.log.info('=============================================================')
        return(success, subscriptions_d, message)

    def drop_subscription(self, data_url, subscription_name, database, retention_policy, auth=None):
        '''
        :param data_url:
        :param subscription_name:
        :param database:
        :param retention_policy:
        :param auth:
        :return:
        '''
        success=False
        message=''
        self.log.info('InfluxDBInfluxDBRestLib.drop_subscription() FUNCTION IS CALLED')
        self.log.info('==============================================================')
        drop_subscription_stmt = 'DROP SUBSCRIPTION "%s" ON "%s"."%s"' % (subscription_name, database, retention_policy)
        self.log.info('InfluxDBInfluxDBRestLib.drop_subscription() DROP SUBSCRIPTION STATEMENT : '
                      + str(drop_subscription_stmt))
        path='/query?q=%s' % drop_subscription_stmt
        response = self.post(data_url, path, auth=auth)
        if response.status_code == 200:
            result = response.json()['results'][0]
            if result.get('error') is None:
                success=True
            else:
                message=result.get('error')
        else:
            message=response.text
            self.log.info('InfluxDBInfluxDBRestLib.create_subscription() error message=' + str(message))
            self.log.info('============================================================')
        self.log.info('InfluxDBInfluxDBRestLib.create_subscription() FUNCTION IS DONE')
        self.log.info('==============================================================')
        return (success, message)

    ############################################### CONTINUOUS QUERIES #################################################

    def create_continuos_query(self, data_url, cq_name, database, cq_query,
                               interval=None, every=None, duration=None, auth=None):
        '''
        CQ will run periodically and automatically on real time data and store query result in a specific measurement
        :param test_class_instance:
        :param client:
        :param cq_name:
        :param database:
        :param cq_query:
        :param interval:
        :return:
        '''
        success=False
        message=''
        self.log.info('InfluxDBInfluxDBRestLib.create_continuos_query() FUNCTION IS CALLED WITH ARGUMENTS: DATA_URL='
                      + str(data_url) + 'CQ NAME=' + str(cq_name) + ', DATABASE=' + str(database) + ', cq_query=' + str(cq_query)
                      + ', interval=' + str(interval) + ', EVERY=' + str(every) + ', DURATIION=' + str(duration))
        self.log.info('===============================================================================================')
        query='CREATE CONTINUOUS QUERY "%s" ON "%s" ' % (cq_name, database)
        if interval:
            if every is None and duration is None:
                return (False, None, 'Either \'FOR\' or \'EVERY\' should be specified')
            if every:
                query=query + 'RESAMPLE EVERY %s ' % every
                if duration:
                    query=query + 'FOR %s ' % duration
            else:
                query=query + 'RESAMPLE FOR %s ' % duration
        query=query + 'BEGIN %s END' % cq_query
        self.log.info('database_util.create_continuos_query() - FINAL QUERY = ' + str(query))
        path='/query?q=%s' % query
        response=self.post(data_url, path, auth=auth)
        if response.status_code == 200:
            result=response.json()['results'][0]
            if result.get('error') is None:
                success=True
            else:
                message=result.get('error')
        else:
            message=response.text
            self.log.info('InfluxDBInfluxDBRestLib.create_continuous_query() error message=' + str(message))
            self.log.info('================================================================================')
        self.log.info('InfluxDBInfluxDBRestLib.create_continuous_query() FUNCTION IS DONE')
        self.log.info('==================================================================')
        return (success, message)


        ################################################## FGA #############################################################

    def drop_continuos_query(self, data_url, cq_name, database, auth=None):
        '''
        CQ will run periodically and automatically on real time data and store query result in a specific measurement
        :param test_class_instance:
        :param client:
        :param cq_name:
        :param database:
        :return:
        '''
        success=False
        message=''
        self.log.info('InfluxDBInfluxDBRestLib.drop_continuos_query() FUNCTION IS CALLED WITH ARGUMENTS: DATA_URL='
                      + str(data_url) + 'CQ NAME=' + str(cq_name) + ', DATABASE=' + str(database))
        self.log.info('=============================================================================================')
        query='DROP CONTINUOUS QUERY "%s" ON "%s" ' % (cq_name, database)
        self.log.info('database_util.create_continuos_query() - FINAL QUERY = ' + str(query))
        path='/query?q=%s' % query
        response=self.post(data_url, path, auth=auth)
        if response.status_code == 200:
            result=response.json()['results'][0]
            if result.get('error') is None:
                success=True
            else:
                message=result.get('error')
        else:
            message=response.text
            self.log.info('InfluxDBInfluxDBRestLib.drop_continuous_query() error message=' + str(message))
            self.log.info('=============================================================================')
        self.log.info('InfluxDBInfluxDBRestLib.drop_continuous_query() FUNCTION IS DONE')
        self.log.info('================================================================')
        return (success, message)

        ################################################## FGA #############################################################

    def list_continuos_queries(self, data_url, auth=None):
        '''
        List every CQ on an InfluxDB instance
        :param test_class_instance:
        :param client:
        :return:
        '''
        success=False
        message=''
        cq_dict={}
        self.log.info('InfluxDBInfluxDBRestLib.list_continuos_queries() FUNCTION IS CALLED')
        self.log.info('===================================================================')
        query='SHOW CONTINUOUS QUERIES'
        self.log.info('database_util.list_continuos_query() - QUERY = ' + str(query))
        path='/query?q=%s' % query
        response=self.post(data_url, path, auth=auth)
        if response.status_code == 200:
            success=True
            # result: [ {u'name': u'_internal', u'columns': [u'name', u'query']},
            #           {u'name': u'telegraf', u'columns': [u'name', u'query']},
            #           {u'name': u'testdb', u'columns': [u'name', u'query'],
            #               u'values':
            #               [
            #                   [u'test_1',
            #                       u'CREATE CONTINUOUS QUERY test_1 ON testdb BEGIN SELECT mean(value) INTO testdb.autogen.test_1
            #                       FROM testdb.autogen.foobar GROUP BY time(5s) END'
            #                   ]
            #               ]
            #           }
            #         ]
            # result is a list of dictionaries
            result=response.json()['results'][0].get('series')
            for entry in result:
                self.log.info('database_util.list_continuos_query() PARSING ENTRY ' + str(entry))
                self.log.info('================================================================')
                # if key 'values' is present then we have one or more CQ
                cq_values=entry.get('values') # returns list of lists.
                db_name=entry.get('name') # returns database name as a str.
                self.log.info('database_util.list_continuos_query() DATABASE NAME=' + str(db_name))
                if cq_values is not None:
                    for cq in cq_values:
                        cq_name=cq[0]
                        self.log.info('database_util.list_continuos_query() CQ NAME=' + str(cq_name))
                        cq_query=cq[1]
                        self.log.info('database_util.list_continuos_query() CQ QUERY=' + str(cq_query))
                        cq_dict[cq_name]={'QUERY':cq_query, 'DB_NAME':db_name}
                    self.log.info('database_util.list_continuos_query() - INTERM CQ DICT=' + str(cq_dict))
                self.log.info('database_util.list_continuos_query() - DONE PARSING ENTRY')
                self.log.info('=========================================================')
            self.log.info('database_util.list_continuos_queries() - FINAL CQ DICT=' + str(cq_dict))
        else:
            self.log.info('database_util.list_continuos_queries() - RESPONSE CODE = ' + str(response.status_code))
            message=response.json().get('error')
        self.log.info('InfluxDBInfluxDBRestLib.list_continuous_queries() FUNCTION IS DONE')
        self.log.info('==================================================================')
        return (success, cq_dict, message)

        ################################################## FGA #############################################################

    #TODO define methods for FGA for roles (as it applicable to ldap)
