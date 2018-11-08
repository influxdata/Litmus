import pytest
import time
import src.util.twodotoh.org_util as org_util
import src.util.twodotoh.buckets_util as buckets_util
import src.util.gateway_util as gateway_util
import src.util.login_util as lu
import json
import subprocess

from src.chronograf.lib import chronograf_rest_lib as crl
from src.cloud.rest_api.conftest import _assert


# remove authorization before removing users
@pytest.mark.usefixtures('remove_orgs', 'remove_buckets', 'remove_auth',
                         'remove_users', 'gateway', 'flux', 'namespace',
                         'kubeconf')
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
        query = 'from(bucket:"%s") |> range(start:-1m)' % bucket_name
        result = {}

        self.header(test_name)
        self.mylog.info(test_name + 'STEP 1: Create Organization')
        create_org_result = org_util.create_organization(self, self.gateway, org_name)
        status_code = create_org_result['status']
        org_id = create_org_result['org_id']

        _assert(self, status_code, 201, 'Create Organization Status Code')
        # TODO add more checks that Organization was created OK

        self.mylog.info(test_name + 'STEP 2: Create Bucket')
        create_bucket_result = \
            buckets_util.create_bucket(self, self.gateway, bucket_name, 3600, org_id)
        status_code = create_bucket_result['status']
        created_bucket_id = create_bucket_result['bucket_id']

        _assert(self, status_code, 201, 'Create Bucket Status Code')
        # TODO add more checks that bucket was created OK

        self.mylog.info(test_name + 'STEP 3: Create User')
        status_code, user_id, created_user_name, error_message = \
            gateway_util.create_user(self, self.gateway, user_name)
        _assert(self, status_code, 201, 'Create User Status Code')

        permissions = [{"action": "read", "resource": "bucket/%s" % created_bucket_id},
                       {"action": "write", "resource": "bucket/%s" % created_bucket_id}]
        self.mylog.info(
            test_name + 'STEP 4: Create Authorization Token for \'%s\' to be able to read/write \'%s\' bucket'
            % (user_name, bucket_name))
        r_dic = gateway_util.create_authorization(self, self.gateway, user_name, user_id, json.dumps(permissions))
        _assert(self, r_dic['STATUS_CODE'], 201, 'Create Authorization Status')

        self.mylog.info(test_name + 'STEP 5: Write point to a bucket')
        w_dic = gateway_util.write_points(self, self.gateway, r_dic['TOKEN'], org_name, bucket_name,
                                          data='test_m,t=0000 f=1234')
        _assert(self, w_dic['STATUS_CODE'], 204, 'Write Data Point To A Bucket')

        # TODO need to be able to get the test namespace.
        """
        self.mylog.info(test_name + 'STEP 6: Verify Data Was Written To Kafka')
        kafka_result = \
            subprocess.Popen('kubectl --kubeconfig="%s" --context=influx-internal exec kafka-0 -c k8skafka -n %s -- bash -c '
                             '"(/opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server kafka-svc:9093 '
                             '--topic ingress --from-beginning > /tmp/out.log 2>&1 &) && sleep 2 && egrep -a \"[0]{4}\" '
                             '/tmp/out.log"' % (self.kubeconf, self.namespace),
                             shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        kafka_result.wait()
        out, error = kafka_result.communicate()
        self.mylog.info(test_name + ' KAFKA RESULTS : ' + str(out) + ' ' + str(error))
        self.mylog.info(test_name + '')

        """
        self.mylog.info(test_name + 'STEP 6: Query Data using Queryd')
        # need to give it up to 30 sec to get the results back
        end_time = time.time() + 30
        while time.time() <= end_time:
            result = gateway_util.queryd_query_data(self, query, self.flux, org_id, timeout=5, responsenone=False)
            if result['STATUS_CODE'] == 200 and len(result['RESULT']) == 1:
                break
            else:
                self.mylog.info(test_name + ' SLEEPING 1 sec')
                time.sleep(1)
        _assert(self, result['STATUS_CODE'], 200, ' STATUS CODE')
        _assert(self, len(result['RESULT']), 1, ' NUMBER OF RECORDS')
        _assert(self, result['RESULT'][0]['_measurement'], 'test_m', 'Measurement')
        _assert(self, result['RESULT'][0]['_value'], '1234', 'Field Value')
        _assert(self, result['RESULT'][0]['t'], '0000', 'Tag Value')

        self.mylog.info('')
        self.mylog.info(test_name + 'STEP 7: Query Data using Gateway')
        # need to give it up to 30 sec to get the results back
        end_time = time.time() + 30
        while time.time() <= end_time:
            result = gateway_util.gateway_query_data(self, query, self.gateway, r_dic['TOKEN'], org_name)
            if result['STATUS_CODE'] == 200 and len(result['RESULT']) == 1:
                break
            else:
                self.mylog.info(test_name + ' SLEEPING 1 sec')
                time.sleep(1)
        _assert(self, result['STATUS_CODE'], 200, ' STATUS CODE')
        _assert(self, len(result['RESULT']), 1, ' NUMBER OF RECORDS')
        _assert(self, result['RESULT'][0]['_measurement'], 'test_m', 'Measurement')
        _assert(self, result['RESULT'][0]['_value'], '1234', 'Field Value')
        _assert(self, result['RESULT'][0]['t'], '0000', 'Tag Value')
