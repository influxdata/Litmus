
import pytest
import src.util.login_util as lu
from src.chronograf.lib import chronograf_rest_lib as crl
from src.util import gateway_util
from src.cloud.rest_api.conftest import org_names
from string import ascii_uppercase

@pytest.mark.usefixtures('remove_buckets', 'remove_orgs', 'get_all_setup_buckets')
class TestGetAllBucketsAPI(object):
    '''
    Test Suite for testing of REST API endpoint to get all of the buckets
    - Removes all of the created by the tests buckets, orgs
    - Creates 26 buckets (single upper case letters) per each of the 5 orgs (5 lower case letters each)
    '''

    mylog=lu.log(lu.get_log_path(), 'w', __name__)
    rl=crl.RestLib(mylog)

    def header(self, test_name):
        self.mylog.info('#' * (11+len(test_name)+17))
        self.mylog.info('<--------- %s START --------->' % test_name)
        self.mylog.info('#' * (11+len(test_name)+17))

    def footer(self, test_name):
        self.mylog.info('#' * (11+len(test_name)+15))
        self.mylog.info('<--------- %s END --------->' % test_name)
        self.mylog.info('#' * (11 + len(test_name) + 15))
        self.mylog.info('')

    def test_get_all_buckets_count(self):
        '''
        REST API: http://<gateway>/v1/buckets
        METHOD: GET
        tests that the count of the created buckets equals to expected
        '''
        test_name='test_get_all_buckets_count '
        expected_buckets_count=130
        self.header(test_name)
        self.mylog.info(test_name + 'STEP 1: Get count of all buckets')
        actual_count=gateway_util.get_count_of_buckets(self, self.get_all_setup_buckets)
        self.mylog.info(test_name + 'Actual count of created buckets is ' + str(actual_count))
        self.mylog.info(test_name + 'Assert expected_count ' + str(expected_buckets_count) +
                        ' equals to actual count ' + str(actual_count))
        assert expected_buckets_count == actual_count, self.mylog.info(test_name + 'Assertion failed')
        self.footer(test_name)

    def test_verify_created_buckets(self):
        '''
        REST API: http://<gateway>/v1/buckets
        METHOD: GET
        tests that created bucket can be found in the list of all buckets returned by the 'get all buckets' endpoint
        '''
        test_name='test_verify_created_buckets '
        self.header(test_name)
        self.mylog.info(test_name + 'STEP 1: find bucket per org')
        for org_name in org_names:
            for bucket_name in ascii_uppercase:
                success=gateway_util.find_bucket_by_name(self, self.get_all_setup_buckets, bucket_name, org_name)
                assert success, \
                    self.mylog.info(test_name + 'Assertion failed: bucket \'%s\' could not be found in \'%s\''
                                    % (bucket_name, org_name))
        self.footer(test_name)

