
import pytest

import src.util.gateway_util as gateway_util
import src.util.login_util as lu
import json
from src.chronograf.lib import chronograf_rest_lib as crl
from src.cloud.rest_api.conftest import _assert

# remove authorization before removing users
@pytest.mark.usefixtures('remove_orgs', 'remove_buckets', 'remove_auth', 'remove_users', 'gateway')
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
        3. Create a user. Verify user was created sucessfully.
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

        self.header(test_name)
        self.mylog.info(test_name + 'STEP 1: Create Organization')
        status_code, org_id, created_org_name, error_message = \
            gateway_util.create_organization(self, self.gateway, org_name)
        _assert(self, 201, status_code, 'Create Organization Status Code')
        # TODO add more checks that Organization was created OK

        self.mylog.info(test_name + 'STEP 2: Create Bucket')
        status_code, created_bucket_id, created_bucket_name, organization_id, retention_period, error_message = \
            gateway_util.create_bucket(self, self.gateway, bucket_name, retentionPeriod="1h", organizationID=org_id)
        _assert(self, 201, status_code, 'Create Bucket Status Code')
        # TODO add more checks that bucket was created OK

        self.mylog.info(test_name + 'STEP 3: Create User')
        status_code, user_id, created_user_name, error_message = \
            gateway_util.create_user(self, self.gateway, user_name)
        _assert(self, 201, status_code, 'Create User Status Code')

        permissions = [{"action":"read", "resource":"bucket/%s" % created_bucket_id},
                       {"action":"write", "resource":"bucket/%s" % created_bucket_id}]
        self.mylog.info(test_name + 'STEP 4: Create Authorization Token for \'%s\' to be able to read/write \'%s\' bucket'
                        % (user_name, bucket_name))
        r_dic = gateway_util.create_authorization(self, self.gateway, user_name, user_id, json.dumps(permissions))
        _assert(self, 201, r_dic['STATUS_CODE'], 'Create Authorization Status')

        self.mylog.info(test_name + 'STEP 5: Write point to a bucket')
        w_dic = gateway_util.write_points(self, self.gateway, r_dic['TOKEN'], org_name, bucket_name,
                                          data='test_m,t=0000 f=1234')
        _assert(self, 204, w_dic['STATUS_CODE'], 'Write Data Point To A Bucket')

        # TODO need to be able to get the test namespace.
        """
        self.mylog.info(test_name + 'STEP 6: Verify Data Was Written To Kafka')
        kafka_result = subprocess.Popen('kubectl exec kafka-0 -c k8skafka -n <?????NAMESPACE?????> -- bash -c '
                                        '"(/opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server kafka-svc:9093 '
                                        '--topic ingress --from-beginning > /tmp/out.log 2>&1 &) && sleep 2 && egrep '
                                        '-a \"[0]{4}\" /tmp/out.log"',
                                        shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        """

        self.mylog.info(test_name + 'STEP 6: Query Data From Storage using Queryd')






