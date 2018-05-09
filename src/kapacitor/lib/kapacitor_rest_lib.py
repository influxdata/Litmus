import requests
from src.chronograf.lib.base_lib import BaseLib

class KapacitorRestLib(BaseLib):
    """

    """

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


    KAPACITOR_CONFIG_PATH='/kapacitor/v1/config/'
    KAPACITOR_TASKS='/kapacitor/v1/tasks'


    ################### set/delete/add value ######################

    def _get_section(self, kapacitor_url, section):
        '''
        :param kapacitor_url: URL of the kapacitor, such as http://IP:PORT
                                            from kapacitor fixture
        :param section: one of the sections returned by config:
                    alerta, hipchat,httppost, influxdb,etc. We are interested in influxdb
                    for now
        :return: dictionary of elements of a particular section
        '''
        final_dictionary={}
        response=self.get(kapacitor_url + self.KAPACITOR_CONFIG_PATH, section)
        assert response.status_code == 200, \
            self.log.info('KapacitorRestLib._get_section() return code is '
                            + response.status_code)
        '''
        each section can have multiple elements, for example influxdb section
        can have local, remote, etc database elements.
        basically each element is a dictionary of following key -- values:
        redacted ----> [u'password']
        link ----> {u'href': u'/kapacitor/v1/config/influxdb/pcl', u'rel': u'self'}
        options ----> { u'insecure-skip-verify': False, 
                                u'udp-read-buffer': 0, 
                                u'disable-subscriptions': False, 
                                u'excluded-subscriptions': {u'_kapacitor': [u'autogen']}, 
                                u'subscription-mode': u'cluster', 
                                u'udp-bind': u'', 
                                u'subscription-protocol': u'http', 
                                u'username': u'', 
                                u'urls': [u'http://34.213.133.93:8086', u'http://54.214.86.234:8086'], 
                                u'subscriptions': {}, 
                                u'kapacitor-hostname': u'', 
                                u'startup-timeout': u'5m0s', 
                                u'password': False, 
                                u'ssl-key': u'', 
                                u'name': u'pcl', 
                                u'udp-buffer': 1000, 
                                u'default': True, 
                                u'enabled': True, 
                                u'ssl-ca': u'', 
                                u'timeout': u'0s', 
                                u'http-port': 0, 
                                u'ssl-cert': u'', 
                                u'subscriptions-sync-interval': u'1m0s'}
        
        In order to set/delete/add key:values to the influxdb table of the
        kapacitor config file we need to know link, that is '/kapacitor/v1/config/influxdb/pcl
        Our final dictionary for the section would have key = name and 
        values = options
        '''
        elements=response.json()['elements'] # returns list of dictionary(ies)
        for element in elements:
            key=element['options']['name']
            value=element['options']
            final_dictionary[key]=value
        self.log.info('final_dictionary = ' + str(final_dictionary))
        return final_dictionary

    def set_value(self, kapacitor_url, section, json, name='pcl'):
        '''
        :param kapacitor_url: URL of the kapacitor, e.g. http://IP:PORT
        :param section: one of the kapacitor config file sections
        :param json: data to set in JSON format
        :param name: name of the element to update, if name is not provided,
                                we are assuming we are dealing with influxdb and the
                                name is the pcl, the one set up by pcl installer
        :return:assertion
        '''
        self.log.info('KapacitorRestLib.set_value. Get values for %s'
                        % section + ' for element name ' + name)
        set_value_dictionary=self._get_section(kapacitor_url, section)
        # we need to make sure (???) it is a default element
        assert set_value_dictionary[name]['default'] == True, \
            self.log.info('IT IS NOT A DEFAULT ELEMENT')
        # construct a URL to be used to update the one or more options keys
        path_url=self.KAPACITOR_CONFIG_PATH + section + '/'\
            + name
        self.log.info('KapacitorRestLib.set_value POST URL=' + str(path_url) )
        # post changes
        response=self.post(kapacitor_url, path_url, {'set':json})
        assert response.status_code == 204, \
            self.log.info('KapacitorRestLib.set_value could not set ' + str(json))

    def verify_set_value(self, kapacitor_url, section, json, name='pcl'):
        '''
        :param kapacitor_url: URL of the kapacitor, e.g. http://IP:PORT
        :param section: one of the kapacitor config file sections
        :param json: the key/value pair(s) to be validated
        :param name: name of the updated element
        :return: Assertion
        '''
        self.log.info('KapacitorRestLib.verify_set_value. Get values for %s'
                        % section + ' for element name ' + name)
        verify_value_dictionary=self._get_section(kapacitor_url, section)
        # our json might have multiple values to verify
        for key in json:
            self.log.info('KapacitorRestLib.verify_set_value. '
                            'Asserting expected value : '  + str(json[key]) +
                            ' equals to actual value : ' + str(verify_value_dictionary[name][key]))
            assert verify_value_dictionary[name][key] == json[key], \
                self.log.info('Assertion failed')

    def delete_value(self):
        pass

    def add_value(self):
        pass

    ######################## tasks #############################
    # API:https://docs.influxdata.com/kapacitor/v1.4/working/api/#tasks
    def create_task(self, kapacitor_url, json):
        '''
        Create a new task. Some task maybe created enabled when
        "status" is set to "enabled"
        :param kapacitor_url: URL of a kapacitor, e.g. http://IP:PORT
        :param path: path to a tasks endpoint, see KAPACITOR_TASKS above
        :param json: JSON body of a task
        :return: response object
        '''
        response=self.post(kapacitor_url, self.KAPACITOR_TASKS, json=json)
        assert response.status_code == 200, \
            self.log.info('ERROR message ' + str(response.text))
        return response.json()

    def modify_task(self):
        '''
        modifies an existing task. The task needs to be disabled in order to be
        modified and then re-enabled for the changes to take effect.
        If any property of the task is missing the task will be left unchanged.
        '''
        pass

    def delete_task(self, kapacitor_url, task_id):
        '''
        Delete a specific task
        :param kapacitor url, e.g. http://IP:PORT
        :param task_id name of the task
        :return nothing
        '''
        delete_path=self.KAPACITOR_TASKS + '/' + task_id
        self.log.info('kapacitor_rest_lib.delete_task - delete_path='
                        + str(delete_path))
        response=self.delete(kapacitor_url, delete_path)
        assert response.status_code == 204, \
            self.log.info('Assertion Errr ' + str(response.text))

    def get_tasks_data(self, kapacitor_url):
        '''
        :return:
        '''
        final_dictionary={}
        dict_tasks=self._get_tasks(kapacitor_url)
        #get the list of all of the tasks, each task in the list is a dictionary
        tasks_list=dict_tasks['tasks']
        for task in tasks_list:
            # status = enabled/disabled
            task_status=task.get('status')
            assert task_status is not None, \
                self.log.info('kapacitor_rest_lib.get_tasks_data task '
                                'status is None')
            self.log.info('kapacitor_rest_lib.get_tasks_data task_status='
                            + str(task_status))
            # type either stream or batch
            task_type=task.get('type')
            assert task_type is not None, \
                self.log.info('kapacitor_rest_lib.get_tasks_data task '
                                'type is None')
            self.log.info('kapacitor_rest_lib.get_tasks_data task_type='
                            + str(task_type))
            # script that defines the task
            task_script=task.get('script')
            assert task_script is not None, \
                self.log.info('kapacitor_rest_lib.get_tasks_data task '
                                'script is None')
            self.log.info('kapacitor_rest_lib.get_tasks_data task_script='
                            + str(task_script))
            # name of the task
            task_id=task.get('id')
            assert task_id is not None, \
                self.log.info('kapacitor_rest_lib.get_tasks_data task '
                                'id is None')
            self.log.info('kapacitor_rest_lib.get_tasks_data task_id='
                            + str(task_id))
            # list of database/rp for the task
            dbrps=task.get('dbrps')
            task_db=dbrps[0].get('db')
            assert task_db is not None, \
                self.log.info('kapacitor_rest_lib.get_tasks_data task '
                                'db is None')
            self.log.info('kapacitor_rest_lib.get_tasks_data task_db='
                            + str(task_db))
            task_rp=dbrps[0].get('rp')
            assert task_rp is not None, \
                self.log.info('kapacitor_rest_lib.get_tasks_data task '
                                'rp is None')
            self.log.info('kapacitor_rest_lib.get_tasks_data task_rp='
                            + str(task_rp))
            final_dictionary[task_id]={'task_status':task_status, 'task_type':task_type,
                                       'task_script':task_script, 'task_db':task_db,
                                       'task_rp':task_rp}
        self.log.info('kapacitor_rest_lib.get_tasks_data final_dict=' + str(final_dictionary))
        return final_dictionary

    def _get_tasks(self, kapacitor_url):
        '''
        Return information about all of the tasks
        '''
        response=self.get(kapacitor_url, self.KAPACITOR_TASKS)
        assert response.status_code == 200, \
            self.log.info('ERROR message ' + str(response.text))
        return response.json()

    def get_task(self):
        '''
        Get information about specific task
        '''
        pass

    def enable_task(self):
        '''
        Enable the existing task
        '''
        pass

    def disable_task(self):
        '''
        Disbale the existing task
        '''
        pass

