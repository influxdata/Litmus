
from src.chronograf.lib.base_lib import BaseLib
from src.chronograf.lib import rest_lib
import  src.util.login_util as lu

class KapacitorRestLib(BaseLib):
    """

    """

    KAPACITOR_CONFIG_PATH='/kapacitor/v1/config/'
    KAPACITOR_TASKS='/kapacitor/v1/tasks'

    mylog=lu.log(lu.get_log_path(), 'w', __name__)
    rl=rest_lib.RestLib(mylog)

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
        response=self.rl.get(kapacitor_url + self.KAPACITOR_CONFIG_PATH, section)
        assert response.status_code == 200, \
            self.mylog.info('KapacitorRestLib._get_section() return code is '
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
        self.mylog.info('final_dictionary = ' + str(final_dictionary))
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
        self.mylog.info('KapacitorRestLib.set_value. Get values for %s'
                        % section + ' for element name ' + name)
        set_value_dictionary=self._get_section(kapacitor_url, section)
        # we need to make sure (???) it is a default element
        assert set_value_dictionary[name]['default'] == True, \
            self.mylog.info('IT IS NOT A DEFAULT ELEMENT')
        # construct a URL to be used to update the one or more options keys
        path_url=self.KAPACITOR_CONFIG_PATH + section + '/'\
            + name
        self.mylog.info('KapacitorRestLib.set_value POST URL=' + str(path_url) )
        # post changes
        response=self.rl.post(kapacitor_url, path_url, json=json)
        assert response.status_code == 204, \
            self.mylog.info('KapacitorRestLib.set_value could not set ' + str(json))

    def verify_set_value(self, kapacitor_url, section, json, name='pcl'):
        '''
        :param kapacitor_url: URL of the kapacitor, e.g. http://IP:PORT
        :param section: one of the kapacitor config file sections
        :param json: the key/value pair(s) to be validated
        :param name: name of the updated element
        :return: Assertion
        '''
        self.mylog.info('KapacitorRestLib.verify_set_value. Get values for %s'
                        % section + ' for element name ' + name)
        verify_value_dictionary=self._get_section(kapacitor_url, section)
        # our json might have multiple values to verify
        for key in json:
            self.mylog.info('KapacitorRestLib.verify_set_value. '
                            'Asserting expected value : '  + str(json[key]) +
                            ' equals to actual value : ' + str(verify_value_dictionary[name][key]))
            assert verify_value_dictionary[name][key] == json[key], \
                self.mylog.info('Assertion failed')

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
        response=self.rl.post(kapacitor_url, self.KAPACITOR_TASKS, json=json)
        assert response.status_code == 200, \
            self.mylog.info('ERROR status code is ' + str(response.status_code))
        return response.json()

    def modify_task(self):
        '''
        modifies an existing task. The task needs to be disabled in order to be
        modified and then re-enabled for the changes to take effect.
        If any property of the task is missing the task will be left unchanged.
        '''
        pass

    def delete_task(self):
        '''
        Delete a specific task
        '''
        pass

    def get_tasks(self):
        '''
        Return information about all of the tasks
        '''
        pass

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

