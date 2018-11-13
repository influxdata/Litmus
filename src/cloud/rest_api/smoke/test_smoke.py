import pytest
import time
import src.util.twodotoh.org_util as org_util
import src.util.twodotoh.buckets_util as buckets_util
import src.util.gateway_util as gateway_util
import src.util.login_util as lu
import json

from src.chronograf.lib import chronograf_rest_lib as crl
from src.cloud.rest_api.conftest import _assert


# remove authorization before removing users
@pytest.mark.usefixtures('remove_orgs', 'remove_buckets', 'remove_auth',
                         'remove_users', 'gateway', 'flux', 'namespace',
                         'kubeconf', 'kubecluster')
class TestSmoke(object):
    """
    TODO
    """
    mylog = lu.log(lu.get_log_path(), 'w', __name__)
    rl = crl.RestLib(mylog)

    def header(self, test_name):
        self.mylog.info('#' * (11 + len(test_name) + 17))
        self.mylog.info('<--------- %s START --------->' % test_name)
        self.mylog.info('#' * (11 + len(test_name) + 17))

    def footer(self, test_name):
        self.mylog.info('#' * (11 + len(test_name) + 15))
        self.mylog.info('<--------- %s END --------->' % test_name)
        self.mylog.info('#' * (11 + len(test_name) + 15))
        self.mylog.info('')

    def test_E2E_smoke(self):
        """
        1. Create an organization. Verify organization was created successfully.
        2. Create a bucket for the organization created in step 1. Verify org was created successfully.
        3. Create a user. Verify user was created successfully.
        4. Give user permissions to write data to buckets and read data from the same buckets. Verify authentication is
           successful.
        5. Write data points
           5.1. Verify data got to kafka # TODO (when kubectl is available in containers)
        6. Query data using using queryd. (gateway:9999/api/v2/query)
        7. Query data using transpilerde. (gateway:9999/query)
        """
        test_name = 'test_E2E_smoke '
        org_name = 'test_E2E_smoke_org'
        bucket_name = 'test_E2E_smoke_bucket'
        user_name = 'test_E2E_smoke_user'
        query = 'from(bucket:"%s") |> range(start:-5m)' % bucket_name
        result = {}

        self.header(test_name)
        self.mylog.info(test_name + 'STEP 1: Create Organization')
        self.mylog.info(test_name + '\n')
        create_org_result = org_util.create_organization(self, self.gateway, org_name)
        status_code = create_org_result['status']
        org_id = create_org_result['org_id']

        _assert(self, status_code, 201, 'Create Organization Status Code')
        # TODO add more checks that Organization was created OK

        self.mylog.info(test_name + 'STEP 2: Create Bucket')
        self.mylog.info(test_name + '\n')
        create_bucket_result = \
            buckets_util.create_bucket(self, self.gateway, bucket_name, 3600, org_id)
        status_code = create_bucket_result['status']
        created_bucket_id = create_bucket_result['bucket_id']

        _assert(self, status_code, 201, 'Create Bucket Status Code')
        # TODO add more checks that bucket was created OK

        self.mylog.info(test_name + 'STEP 3: Create User')
        self.mylog.info(test_name + '\n')
        status_code, user_id, created_user_name, error_message = \
            gateway_util.create_user(self, self.gateway, user_name)
        _assert(self, status_code, 201, 'Create User Status Code')

        permissions = [{"action": "read", "resource": "bucket/%s" % created_bucket_id},
                       {"action": "write", "resource": "bucket/%s" % created_bucket_id}]
        self.mylog.info(
            test_name + 'STEP 4: Create Authorization Token for \'%s\' to be able to read/write \'%s\' bucket'
            % (user_name, bucket_name))
        self.mylog.info(test_name + '\n')
        create_auth_result = gateway_util.create_authorization(self, self.gateway, user_name, user_id,
                                                               json.dumps(permissions))
        _assert(self, create_auth_result['status'], 201, 'Create Authorization Status')
        _assert(self, create_auth_result['error'], None, 'Create Authorization Error')

        self.mylog.info(test_name + 'STEP 5: Write point to a bucket')
        self.mylog.info(test_name + '\n')
        write_result = gateway_util.write_points(self, self.gateway, create_auth_result['token'], org_name,
                                                 bucket_name, data='test_m,t=hello\ world f=1234')
        _assert(self, write_result['status'], 204, 'Write Data Point To A Bucket')
        _assert(self, write_result['error'], '', 'Write Data Error Message')

        self.mylog.info(test_name + 'STEP 6: Verify Data Was Written To Kafka')
        self.mylog.info(test_name + '\n')
        # just if there is a latency on writing data to kafka, give it some time
        err = ''
        data = []
        end_time = time.time() + 10
        while time.time() <= end_time:
            topics, data, err = gateway_util.kafka_find_data_by_tag(self, self.kubeconf, self.kubecluster,
                                                                    self.namespace, 'hello world', 'kafka-0')
            if len(data) == 0:
                self.mylog.info(test_name + 'KAFKA DOES NOT HAVE THE DATA YET')
                time.sleep(1)
                continue
            else:
                self.mylog.info(test_name + 'KAFKA GOT THE DATA')
                break
        _assert(self, err, '', 'ERROR GETTING DATA FROM KAFKA')
        _assert(self, len(data), 1, 'SHOULD BE ONLY ONE RECORD')
        _assert(self, 'hello world' in data[0], True, 'DATA SHOULD CONTAIN THE EXPECTED WORD')

        # storage is pulling every 10 seconds from kafka
        self.mylog.info(test_name + 'STEP 7: Verify Data Was Written To Storage')
        self.mylog.info(test_name + '\n')
        end_time = time.time() + 20
        while time.time() <= end_time:
            engine, data, err = gateway_util.storage_find_data(self, self.kubeconf, self.kubecluster, self.namespace,
                                                               'hello world', 'storage-0')
            if len(data) == 0:
                self.mylog.info(test_name + 'STORAGE DOES NOT HAVE THE DATA YET')
                time.sleep(1)
                continue
            else:
                self.mylog.info(test_name + 'STORAGE GOT THE DATA')
                break
        _assert(self, err, '', 'ERROR GETTING DATA FROM STORAGE')
        _assert(self, 'hello\ world' in data[0], True, 'STORAGE SHOULD CONTAIN THE EXPECTED RECORD')

        self.mylog.info(test_name + 'STEP 8: Query Data using Queryd')
        self.mylog.info(test_name + '\n')
        # need to give it up to 30 sec to get the results back
        end_time = time.time() + 30
        result_queryd = None
        while time.time() <= end_time:
            result_queryd = gateway_util.queryd_query_data(self, query, self.flux, org_id, timeout=5, responsenone=False)
            if result_queryd['status'] == 200 and len(result_queryd['result']) == 1:
                break
            else:
                self.mylog.info(test_name + ' SLEEPING 1 sec')
                time.sleep(1)
        _assert(self, result_queryd['status'], 200, ' STATUS CODE')
        _assert(self, len(result_queryd['result']), 1, ' NUMBER OF RECORDS')
        _assert(self, result_queryd['result'][0]['_measurement'], 'test_m', 'Measurement')
        _assert(self, result_queryd['result'][0]['_value'], '1234', 'Field Value')
        _assert(self, result_queryd['result'][0]['t'], 'hello world', 'Tag Value')

        self.mylog.info('')
        self.mylog.info(test_name + 'STEP 9: Query Data using Gateway')
        self.mylog.info(test_name + '\n')
        # need to give it up to 30 sec to get the results back
        end_time = time.time() + 30
        result_gateway = None
        while time.time() <= end_time:
            result_gateway = gateway_util.gateway_query_data(self, query, self.gateway, create_auth_result['token'],
                                                             org_name)
            if result_gateway['status'] == 200 and len(result_gateway['result']) == 1:
                break
            else:
                self.mylog.info(test_name + ' SLEEPING 1 sec')
                time.sleep(1)
        _assert(self, result_gateway['status'], 200, ' STATUS CODE')
        _assert(self, len(result_gateway['result']), 1, ' NUMBER OF RECORDS')
        _assert(self, result_gateway['result'][0]['_measurement'], 'test_m', 'Measurement')
        _assert(self, result_gateway['result'][0]['_value'], '1234', 'Field Value')
        _assert(self, result_gateway['result'][0]['t'], 'hello world', 'Tag Value')
