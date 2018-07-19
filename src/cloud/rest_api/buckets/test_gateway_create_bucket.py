
import pytest
import src.util.login_util as lu
from src.chronograf.lib import chronograf_rest_lib as crl
from src.util import gateway_util
from string import ascii_lowercase
from string import ascii_uppercase
from string import digits
from src.cloud.rest_api.conftest import ten_char_lc, twenty_char_lc, twenty_char_uc, ten_char_uc, \
    ten_char_numbers, five_char_numbers, nonalphanumeric, ten_char_nonalphanumeric, \
    twenty_char_nonalphanumeric, twenty_char_names_list, fourty_char_names_list, \
    four_hundred_char_name_list, two_hundred_char_name_list, special_char

@pytest.mark.usefixtures('remove_buckets', 'remove_orgs', 'gateway')
class TestCreateBucketsAPI(object):
    '''
    Test Suite for testing REST API endpoint for creating buckets
    The existing buckets and organizations would be removed before running tests
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

    def run_tests(self, name_of_the_test_to_run, org_name, bucket_name, retentionPeriod):
        '''
        :param name_of_the_test_to_run: test to be run
        :param org_name (str): name of the organization to be created
        :param bucket_name (str): name of the bucket to be created for the org
        :param retentionPeriod(str): retention period for the bucket
        :return: pass/fail
        '''
        test_name=name_of_the_test_to_run + org_name + ' '
        self.header(test_name)
        self.mylog.info(test_name + ' STEP 1: Create Organization "%s"' % org_name)
        (status, created_org_id, created_org_name, error_message)=\
            gateway_util.create_organization(self, self.gateway, org_name)
        if org_name == '':
            assert status == 404, \
                pytest.xfail(reason='https://github.com/influxdata/platform/issues/162')
        elif org_name == 'BackSlash\\':
            assert status == 201, \
                pytest.xfail(reason='https://github.com/influxdata/platform/issues/163')
        else:
            assert status == 201, \
                self.mylog.info(test_name + 'Assertion Failed, status=%s' % status)

        self.mylog.info(test_name + 'STEP 2: Verify org data was persisted in the etcd store')
        gateway_util.verify_org_etcd(self, self.etcd, created_org_id, created_org_name)

        self.mylog.info(test_name + 'STEP 3: Create Bucket "%s"' % bucket_name)
        status, created_bucket_id, created_bucket_name, organization_id, retention_period, error_message=\
            gateway_util.create_bucket(self, self.gateway, bucket_name, retentionPeriod, created_org_id)
        if bucket_name == '':
            assert status == 404, \
                pytest.xfail(reason='https://github.com/influxdata/platform/issues/162')
        elif bucket_name == 'BackSlash\\':
            assert status == 201, \
                pytest.xfail(reason='https://github.com/influxdata/platform/issues/163')
        else:
            assert status == 201, \
                self.mylog.info(test_name + 'Assertion Failed, status=%s' % status)

        self.mylog.info(test_name + 'STEP 4: Verify bucket data was persisted in the etcd store')
        gateway_util.verify_bucket_etcd(self, self.etcd, created_bucket_id, created_bucket_name)
        self.footer(test_name)

    ############################################
    #       Lower Case Character Bucket Names  #
    ############################################
    @pytest.mark.parametrize('one_char', ascii_lowercase)
    def test_create_buckets_single_char_lower_case(self, one_char):
        '''
        REST API: http://<gateway>/v1/buckets
        METHOD: POST
        tests bucket name containing single character lower case letters can be created and persisted in the etcd store.
        '''
        self.run_tests('test_create_bucket_single_char_lower_case ', one_char, one_char, 1)


    @pytest.mark.parametrize('ten_char_lc', ten_char_lc)
    def test_create_buckets_10_char_lower_case(self, ten_char_lc):
        '''
        REST API: http://<gateway>/v1/buckets
        METHOD: POST
        tests bucket name containing random 10 lower case letters can be created and persisted in the etcd store.
        '''
        self.run_tests('test_create_orgs_10_char_lower_case ', ten_char_lc, twenty_char_lc, 1)

    @pytest.mark.parametrize('twenty_char_lc', twenty_char_lc)
    def test_create_buckets_20_char_lower_case(self, twenty_char_lc):
        '''
        REST API: http://<gateway>/v1/buckets
        METHOD: POST
        tests bucket name containing random 20 lower case letters can be created and persisted in the etcd store.
        '''
        self.run_tests('test_create_orgs_20_char_lower_case ', twenty_char_lc, twenty_char_lc, 1)

    ######################################################
    #          Upper Case Character Bucket Names         #
    ######################################################
    @pytest.mark.parametrize('one_char', ascii_uppercase)
    def test_create_buckets_single_char_upper_case(self, one_char):
        '''
        REST API: http://<gateway>/v1/buckets
        METHOD: POST
        tests bucket name containing single character upper case letters can be created and persisted in the etcd store.
        '''
        self.run_tests('test_create_buckets_single_char_upper_case ', one_char, one_char, 1)

    @pytest.mark.parametrize('ten_char_uc', ten_char_uc)
    def test_create_buckets_10_char_upper_case(self, ten_char_uc):
        '''
        REST API: http://<gateway>/v1/buckets
        METHOD: POST
        tests bucket name containing random 10 upper case letters can be created and persisted in the etcd store.
        '''
        self.run_tests('test_create_buckets_10_char_upper_case ', ten_char_uc, ten_char_uc, 1)

    @pytest.mark.parametrize('twenty_char_uc', twenty_char_uc)
    def test_create_buckets_20_char_upper_case(self, twenty_char_uc):
        '''
        REST API: http://<gateway>/v1/buckets
        METHOD: POST
        tests bucket name containing random 20 upper case letters can be created and persisted in the etcd store.
        '''
        self.run_tests('test_create_orgs_20_char_upper_case ', twenty_char_uc, twenty_char_uc, 1)

    ############################################################
    #          Non-alphanumeric Character Bucket Names         #
    ############################################################
    @pytest.mark.parametrize('one_char', nonalphanumeric)
    def test_create_buckets_single_char_nonalphanumeric_case(self, one_char):
        '''
        REST API: http://<gateway>/v1/buckets
        METHOD: POST
        tests bucket name containing single non-alphanumeric characters can be created and persisted in the etcd store.
        '''
        self.run_tests('test_create_buckets_single_char_nonalphanumeric_case ', one_char, one_char, 1)

    @pytest.mark.parametrize('ten_char_nonalphanumeric', ten_char_nonalphanumeric)
    def test_create_buckets_10_char_nonalphanumeric_case(self, ten_char_nonalphanumeric):
        '''
        REST API: http://<gateway>/v1/buckets
        METHOD: POST
        tests bucket name containing 10 random non-alphanumeric charactersd can be created and persisted in the etcd store.
        '''
        self.run_tests('test_create_buckets_10_char_nonalphanumeric_case ',
                       ten_char_nonalphanumeric, ten_char_nonalphanumeric, 1)

    @pytest.mark.parametrize('twenty_char_nonalphanumeric', twenty_char_nonalphanumeric)
    def test_create_buckets_20_char_nonalphanumeric_case(self, twenty_char_nonalphanumeric):
        '''
        REST API: http://<gateway>/v1/buckets
        METHOD: POST
        tests bucket name containing 20 random non-alphanumeric charactersd can be created and persisted in the etcd store.
        '''
        self.run_tests('test_create_buckets_20_char_nonalphanumeric_case ',
                       twenty_char_nonalphanumeric, twenty_char_nonalphanumeric, 1)

    ####################################################
    #          Number Characters Bucket Names          #
    ####################################################
    @pytest.mark.parametrize('one_char', digits)
    def test_create_buckets_single_char_numbers(self, one_char):
        '''
        REST API: http://<gateway>/v1/buckets
        METHOD: POST
        tests bucket name containing single digits can be created and persisted in the etcd store
        '''
        self.run_tests('test_create_buckets_single_char_numbers ', one_char, one_char, 1)

    @pytest.mark.parametrize('ten_char_numbers', ten_char_numbers)
    def test_create_buckets_10_char_numbers(self, ten_char_numbers):
        '''
        REST API: http://<gateway>/v1/buckets
        METHOD: POST
        tests bucket name containing 10 random digits can be created and persisted in the etcd store
        '''
        self.run_tests('test_create_buckets_10_char_numbers', ten_char_numbers, ten_char_numbers, 1)

    @pytest.mark.parametrize('five_chars', five_char_numbers)
    def test_create_buckets_5_char_numbers(self, five_chars):
        '''
        REST API: http://<gateway>/v1/buckets
        METHOD: POST
        tests bucket name containing 5 random digits can be created and persisted in the etcd store
        '''
        self.run_tests('test_create_buckets_5_char_numbers', five_chars, five_chars, 1)

    #######################################
    #     Mix Characters Bucket Names     #
    #######################################
    @pytest.mark.parametrize('twenty_char_names', twenty_char_names_list)
    def test_create_buckets_20_char_mix(self, twenty_char_names):
        '''
        REST API: http://<gateway>/v1/buckets
        METHOD: POST
        tests bucket name containing 20 mix characters can be created and persisted in the etcd store.
        '''
        self.run_tests('test_create_buckets_20_char_mix ', twenty_char_names, twenty_char_names, 1)

    @pytest.mark.parametrize('fourty_char_names', fourty_char_names_list)
    def test_create_buckets_40_char_mix(self, fourty_char_names):
        '''
        REST API: http://<gateway>/v1/buckets
        METHOD: POST
        tests bucket name containing 40 mix characters can be created and persisted in the etcd store.
        '''
        self.run_tests('test_create_buckets_40_char_mix ', fourty_char_names, fourty_char_names, 1)

    @pytest.mark.parametrize('special_char', special_char)
    def test_create_buckets_special_chars(self, special_char):
        '''
        REST API: http://<gateway>/v1/buckets
        METHOD: POST
        tests bucket name containing special characters can be created and persisted in the etcd store.
        '''
        self.run_tests('test_create_buckets_special_chars ', special_char, special_char, 1)

    @pytest.mark.parametrize('two_hundred_char_names', two_hundred_char_name_list)
    def test_create_buckets_200_char_mix(self, two_hundred_char_names):
        '''
        REST API: http://<gateway>/v1/buckets
        METHOD: POST
        tests bucket name containing 200 mix characters can be created and persisted in the etcd store.
        '''
        self.run_tests('test_create_buckets_200_char_mix ', two_hundred_char_names, two_hundred_char_names, 1)

    @pytest.mark.parametrize('four_hundred_char_names', four_hundred_char_name_list)
    def test_create_buckets_400_char_mix(self, four_hundred_char_names):
        '''
        REST API: http://<gateway>/v1/buckets
        METHOD: POST
        tests bucket name containing 400 mix characters can be created and persisted in the etcd store.
        '''
        self.run_tests('test_create_buckets_400_char_mix ', four_hundred_char_names, four_hundred_char_names, 1)

    def test_create_many_buckets_same_org(self):
        '''
        REST API: http://<gateway>/v1/buckets
        METHOD: POST
        tests many buckets with different names can be created for the same organization.
        '''
        org_name='one_for_all'
        test_name='test_create_many_buckets_same_org '
        self.header(test_name)
        self.mylog.info(test_name + ' STEP 1: Create Organization "%s"' % org_name)
        (status, created_org_id, created_org_name, error_message) = \
            gateway_util.create_organization(self, self.gateway, org_name)
        assert status == 201, self.mylog.info(test_name + 'Assertion Failed, status=%s' % status)

        self.mylog.info(test_name + 'STEP 2: Verify org data was persisted in the etcd store')
        gateway_util.verify_org_etcd(self, self.etcd, created_org_id, created_org_name)

        self.mylog.info(test_name + 'STEP 3: Create Multiple Buckets for "%s" name' % org_name)
        for bucket_name in ascii_lowercase:
            self.mylog.info(test_name + 'Creating bucket "%s" name' % bucket_name)
            status, created_bucket_id, created_bucket_name, organization_id, retention_period, error_message=\
                gateway_util.create_bucket(self, self.gateway, bucket_name, 1, created_org_id)
            assert status == 201, self.mylog.info(test_name + 'Assertion Failed, status=%s' % status)
            self.mylog.info(test_name + 'Verify bucket data was persisted in the etcd store')
            gateway_util.verify_bucket_etcd(self, self.etcd, created_bucket_id, created_bucket_name)
        self.footer(test_name)

    def test_create_same_bucket_different_orgs(self):
        '''
        REST API: http://<gateway>/v1/buckets
        METHOD: POST
        tests bucket with the same name can be created for different organizations
        '''
        bucket_name='one_for_all'
        test_name='test_create_same_bucket_different_orgs '
        self.header(test_name)
        for org_name in ascii_lowercase:
            org_name=org_name + '_same_bucket_name'
            self.mylog.info(test_name + 'Create Organization "%s"' % org_name)
            (status, created_org_id, created_org_name, error_message) = \
                gateway_util.create_organization(self, self.gateway, org_name)
            assert status == 201, self.mylog.info(test_name + 'Assertion Failed, status=%s' % status)
            self.mylog.info(test_name + 'Verify org data was persisted in the etcd store')
            gateway_util.verify_org_etcd(self, self.etcd, created_org_id, created_org_name)
            self.mylog.info(test_name + 'Create Bucket "%s" name for "%s" name' % (bucket_name, org_name))
            status, created_bucket_id, created_bucket_name, organization_id, retention_period, error_message = \
                gateway_util.create_bucket(self, self.gateway, bucket_name, 1, created_org_id)
            assert status == 201, self.mylog.info(test_name + 'Assertion Failed, status=%s' % status)
            self.mylog.info(test_name + 'Verify bucket data was persisted in the etcd store')
            gateway_util.verify_bucket_etcd(self, self.etcd, created_bucket_id, created_bucket_name)
        self.footer(test_name)

    def test_create_duplicate_bucket(self):
        '''
        REST API: http://<gateway>/v1/buckets
        METHOD: POST
        tests cannot create bucket with already existing name with the same org.
        '''
        test_name='test_create_duplicate_bucket '
        org_name='orgname'
        bucket_name='dupbucketname'
        retentionPeriod=1
        expected_error_message='bucket with name dupbucketname already exists'
        self.header(test_name)
        self.mylog.info(test_name + ' STEP 1: Create Organization "%s"' % org_name)
        (status, created_org_id, created_org_name, error_message) = \
            gateway_util.create_organization(self, self.gateway, org_name)
        assert status == 201, self.mylog.info(test_name + 'Assertion Failed, status=%s' % status)

        self.mylog.info(test_name + 'STEP 2: Verify org data was persisted in the etcd store')
        gateway_util.verify_org_etcd(self, self.etcd, created_org_id, created_org_name)

        self.mylog.info(test_name + 'STEP 3: Create Bucket "%s"' % bucket_name)
        status, created_bucket_id, created_bucket_name, organization_id, retention_period, error_message = \
            gateway_util.create_bucket(self, self.gateway, bucket_name, retentionPeriod, created_org_id)
        assert status == 201, self.mylog.info(test_name + 'Assertion Failed, status=%s' % status)

        self.mylog.info(test_name + 'STEP 4: Verify bucket data was persisted in the etcd store')
        gateway_util.verify_bucket_etcd(self, self.etcd, created_bucket_id, created_bucket_name)

        self.mylog.info(test_name + 'STEP 5: Create Bucket with already existing name for the same org')
        status, created_bucket_id, created_bucket_name, organization_id, retention_period, error_message = \
            gateway_util.create_bucket(self, self.gateway, bucket_name, retentionPeriod, created_org_id)
        assert error_message == expected_error_message, pytest.xfail(reason='error message is empty')
        self.footer(test_name)

    def test_create_bucket_no_org_id(self):
        '''
        REST API: http://<gateway>/v1/buckets
        METHOD: POST
        tests cannot create bucket if organization id is not provided
        '''
        test_name='test_create_bucket_no_org_id'
        bucket_name='bucket_no_org_id'
        retentionPeriod=1
        self.header(test_name)
        self.mylog.info(test_name + 'STEP 1: Create Bucket "%s" without ORG ID' % bucket_name)
        status, created_bucket_id, created_bucket_name, organization_id, retention_period, error_message = \
            gateway_util.create_bucket(self, self.gateway, bucket_name, retentionPeriod)
        assert status == 404, pytest.xfail(reason='status=%s' % status)

    def test_create_bucket_default_rp(self):
        '''
        REST API: http://<gateway>/v1/buckets
        METHOD: POST
        tests bucket can be created if retention policy is not provided, use default one (what is the default one???)
        '''
        test_name='test_create_bucket_default_rp'
        org_name='org_default_rp'
        bucket_name='bucket_default_rp'
        self.header(test_name)
        self.mylog.info(test_name + ' STEP 1: Create Organization "%s"' % org_name)
        (status, created_org_id, created_org_name, error_message) = \
            gateway_util.create_organization(self, self.gateway, org_name)
        assert status == 201, self.mylog.info(test_name + 'Assertion Failed, status=%s' % status)

        self.mylog.info(test_name + 'STEP 2: Verify org data was persisted in the etcd store')
        gateway_util.verify_org_etcd(self, self.etcd, created_org_id, created_org_name)

        self.mylog.info(test_name + 'STEP 3: Create Bucket "%s"' % bucket_name)
        status, created_bucket_id, created_bucket_name, organization_id, retention_period, error_message = \
            gateway_util.create_bucket(self, self.gateway, bucket_name,
                                       retentionPeriod=None, organizationID=created_org_id)
        assert status == 201, self.mylog.info(test_name + 'Assertion Failed, status=%s' % status)
        assert retention_period == "1h", pytest.xfail(reason='https://github.com/influxdata/platform/issues/419')

        self.mylog.info(test_name + 'STEP 4: Verify bucket data was persisted in the etcd store')
        gateway_util.verify_bucket_etcd(self, self.etcd, created_bucket_id, created_bucket_name)
        self.footer(test_name)