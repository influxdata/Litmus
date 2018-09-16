
import pytest

import src.util.gateway_util as gateway_util
import src.util.login_util as lu
from src.chronograf.lib import chronograf_rest_lib as crl
from src.cloud.rest_api.conftest import _assert

@pytest.mark.usefixtures('remove_orgs', 'gateway')
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

    def test_write_data_to_storage(self):
        """
        1. Create an organization. Verify organization was created successfully.
        2. Create a bucket for the organization created in step 1. Verify org was created successfully.
        3. Create a user. Verify user was created sucessfully.
        4. Give user permissions to write data to buckets and read data from the same buckets. Verify authentication is
           successful.
        5. Write data points
           5.1. Verify data got to kafka
           5.2. Verify data ended up in storage
        6. Query data using using queryd.
        7. Query data using transpilerde.
        """
        test_name = 'test_write_data_to_storage '
        org_name = 'org_smoke_test'
        bucket_name = 'bucket_smoke_test'

        self.header(test_name)
        self.mylog.info(test_name + 'STEP 1: Create Organization')
        status_code, org_id, created_org_name, error_message = \
            gateway_util.create_organization(self, self.gateway, org_name)
        _assert(self, 201, status_code, 'Create Organization Status Code')


        self.mylog.info(test_name + 'STEP 2: Create Bucket')
        status_code, created_bucket_id, created_bucket_name, organization_id, retention_period, error_message = \
            gateway_util.create_bucket(self, self.gateway, bucket_name, retentionPeriod=0, organizationID=org_id)
        _assert(self, 201, status_code, 'CReate Bucket Status Code')
