
import pytest
import src.util.login_util as lu
from src.chronograf.lib import chronograf_rest_lib as crl
import src.util.gateway_util as gateway_util
from string import ascii_lowercase
from string import ascii_uppercase
from string import digits
from src.cloud.rest_api.conftest import ten_char_lc, twenty_char_lc, twenty_char_uc, ten_char_uc, \
    ten_char_numbers, five_char_numbers, nonalphanumeric, ten_char_nonalphanumeric, \
    twenty_char_nonalphanumeric, twenty_char_names_list, fourty_char_names_list, \
    four_hundred_char_name_list, two_hundred_char_name_list, special_char

@pytest.mark.usefixtures('remove_buckets', 'remove_orgs', 'gateway')
class TestUpdateBucketsNameAPI(object):
    '''
    Test suite to test rest api endpoint for updating Bucket's Name
    removes created by tests bucketanizations and buckets
    '''
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

    def run_tests(self, name_of_the_test_to_run, org_name, bucket_name, retentionPeriod, new_bucket_name=None,
                  new_retention=None):
        '''
        :param name_of_the_test_to_run: test to be run
        :param org_name: name of the organization to be created
        :param bucket_name: name of the bucket to be created
        :param retentionPeriod: retention period for the bucket
        :param new_bucket_name: name of the bucket to update to
        :param new_retention: retention period to update to
        :return: pass/fail
        '''
        test_name=name_of_the_test_to_run + org_name + ' '
        new_bucket_name_to_assert=''
        if org_name == 'DoubleQuotes\\"':
            new_bucket_name_to_assert = 'DoubleQuotes"_updated'

        self.header(test_name)
        self.mylog.info(test_name + ' STEP 1: Create Organization')
        (status, created_org_id, created_org_name, error_message) = \
            gateway_util.create_organization(self, self.gateway, org_name)
        if org_name == '':
            assert status == 404, \
                pytest.xfail(reason='https://github.com/influxdata/platform/issues/188')
        elif org_name == 'BackSlash\\':
            assert status == 201, \
                pytest.xfail(reason='https://github.com/influxdata/platform/issues/163')
        else:
            assert status == 201, \
                self.mylog.info(test_name + 'Assertion Failed, status=%s' % status)

        self.mylog.info(test_name + 'STEP 2: Verify org data was persisted in the etcd store')
        gateway_util.verify_org_etcd(self, self.etcd, created_org_id, created_org_name)

        self.mylog.info(test_name + 'STEP 3: Create Bucket "%s"' % bucket_name)
        status, created_bucket_id, created_bucket_name, created_organization_id, retention_period, error_message = \
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

        if new_bucket_name is None and new_retention is None:
            self.mylog.info(test_name + 'STEP 5: Bucket info is not getting updated')
            status, bucket_id, updated_bucket_name, retention, organization_id, organization_name, error_message = \
                gateway_util.update_bucket(self, self.gateway, created_bucket_id, new_bucket_name=None,
                                           new_retention=None)
            assert updated_bucket_name == created_bucket_name, \
                self.mylog.info(test_name + 'Assertion Failed. status=%d, error message %s' % (status, error_message))
            assert retention == retention_period, \
                self.mylog.info(test_name + 'Assertion Failed. status=%d, error message %s' % (status, error_message))

        elif new_retention is None:
            self.mylog.info(test_name + 'STEP 5: Update created bucket with \'%s\' name' % new_bucket_name)
            status, bucket_id, updated_bucket_name, retention, organization_id, organization_name, error_message=\
                gateway_util.update_bucket(self, self.gateway, created_bucket_id, new_bucket_name, new_retention=None)
            if org_name == 'DoubleQuotes\\"':
                assert updated_bucket_name == new_bucket_name_to_assert, \
                    self.mylog.info(test_name + 'Assertion Failed. status=%d, error message %s'
                                    % (status, error_message))
            else:
                assert updated_bucket_name == new_bucket_name, \
                    self.mylog.info(test_name + 'Assertion Failed. status=%d, error message %s'
                                    % (status, error_message))
            assert retention == retention_period, \
                self.mylog.info(test_name + 'Assertion Failed. status=%d, error message %s' % (status, error_message))

        elif new_bucket_name is None:
            self.mylog.info(test_name + 'STEP 5: Update created bucket with \'%d\' retention name' % new_retention)
            status, bucket_id, updated_bucket_name, retention, organization_id, organization_name, error_message = \
                gateway_util.update_bucket(self, self.gateway, created_bucket_id, new_bucket_name=None,
                                           new_retention=new_retention)
            assert updated_bucket_name == created_bucket_name, \
                self.mylog.info(test_name + 'Assertion Failed. status=%d, error message %s' % (status, error_message))
            assert retention == new_retention, \
                self.mylog.info(test_name + 'Assertion Failed. status=%d, error message %s' % (status, error_message))

        else:
            self.mylog.info(test_name + 'STEP 5: Update created bucket with \'%s\' bucket name and \'%d\' retention'
                            % (new_bucket_name, new_retention))
            status, bucket_id, updated_bucket_name, retention, organization_id, organization_name, error_message = \
                gateway_util.update_bucket(self, self.gateway, created_bucket_id, new_bucket_name, new_retention)
            assert retention == new_retention, \
                self.mylog.info(test_name + 'Assertion Failed. status=%d, error message %s' % (status, error_message))
            assert updated_bucket_name == new_bucket_name, \
                self.mylog.info(test_name + 'Assertion Failed. status=%d, error message %s' % (status, error_message))

        assert status == 200, \
            self.mylog.info(test_name + 'Assertion Failed. status=%d, error message %s' % (status, error_message))

        assert bucket_id == created_bucket_id, \
            self.mylog.info(test_name + 'Assertion Failed. status=%d, error message %s' % (status, error_message))

        assert organization_id == created_organization_id, \
            self.mylog.info(test_name + 'Assertion Failed. status=%d, error message %s' % (status, error_message))
        self.mylog.info('')
        self.mylog.info(test_name + 'STEP 6: Verify updated bucket info was persisted in the etcd store')
        gateway_util.verify_bucket_etcd(self, self.etcd, bucket_id, updated_bucket_name)
        self.footer(test_name)

    ###############################################
    #       Lower Case Character Bucket Names     #
    ###############################################

    @pytest.mark.parametrize('one_char', ascii_lowercase)
    def test_update_buckets_name_single_char_lower_case(self, one_char):
        '''
        REST API: http://<gateway>/v1/buckets
        METHOD: PATCH
        tests bucket name containing single character lower case letters can be updated and persisted in the etcd store.
        '''
        self.run_tests('test_update_buckets_name_single_char_lower_case ',
                       one_char, one_char, 1, one_char+'_updated', None)

    @pytest.mark.parametrize('ten_char_lc', ten_char_lc)
    def test_update_buckets_name_10_char_lower_case(self, ten_char_lc):
        '''
        TEST API: http://<gateway>/v1/buckets
        METHOD: PATCH
        tests bucket name containing random 10 lower case letters can be updated and persisted in the etcd store.
        '''
        self.run_tests('test_update_buckets_name_10_char_lower_case ', ten_char_lc, ten_char_lc, 1,
                       ten_char_lc+'_updated', None)

    @pytest.mark.parametrize('twenty_char_lc', twenty_char_lc)
    def test_update_buckets_name_20_char_lower_case(self, twenty_char_lc):
        '''
        TEST API: http://<gateway>/v1/buckets
        METHOD: PATCH
        tests bucket name containing random 20 lower case letters can be updated and persisted in the etcd store.
        '''
        self.run_tests('test_update_buckets_name_20_char_lower_case ', twenty_char_lc, twenty_char_lc, 1,
                       twenty_char_lc+'_updated', None)

    ######################################################
    #          Upper Case Character Bucket Names         #
    ######################################################
    @pytest.mark.parametrize('one_char', ascii_uppercase)
    def test_update_buckets_name_single_char_upper_case(self, one_char):
        '''
        TEST API: http://<gateway>/v1/buckets
        METHOD: PATCH
        tests bucket name containing single upper case letters can be updated and persisted in the etcd store.
        '''
        self.run_tests('test_update_buckets_name_single_char_upper_case ', one_char, one_char, 1,
                       one_char+'_updated', None)

    @pytest.mark.parametrize('ten_char_uc', ten_char_uc)
    def test_update_buckets_name_10_char_upper_case(self, ten_char_uc):
        '''
        TEST API: http://<gateway>/v1/buckets
        METHOD: PATCH
        tests bucket name containing random 10 upper case letters can be updated and persisted in the etcd store.
        '''
        self.run_tests('test_update_buckets_name_10_char_upper_case ', ten_char_uc, ten_char_uc, 1,
                       ten_char_uc + '_updated', None)

    @pytest.mark.parametrize('twenty_char_uc', twenty_char_uc)
    def test_update_buckets_name_20_char_upper_case(self, twenty_char_uc):
        '''
        TEST API: http://<gateway>/v1/buckets
        METHOD: PATCH
        tests buckets name containing random 20 upper case letters can be updated and persisted in the etcd store.
        '''
        self.run_tests('test_update_buckets_name_20_char_upper_case ', twenty_char_uc, twenty_char_uc, 1,
                       twenty_char_uc + '_updated', None)

    #############################################################
    #          Non-alphanumeric Character Buckets Names         #
    #############################################################
    @pytest.mark.parametrize('one_char', nonalphanumeric)
    def test_update_buckets_name_single_char_nonalphanumeric_case(self, one_char):
        '''
        TEST API: http://<gateway>/v1/buckets
        METHOD: PATCH
        tests bucket name containing single non-alphanumeric character can be updated and persisted in the etcd store.
        '''
        self.run_tests('test_update_buckets_name_single_char_nonalphanumeric_case ', one_char, one_char, 1,
                       one_char + '_updated', None)

    @pytest.mark.parametrize('ten_char_nonalphanumeric', ten_char_nonalphanumeric)
    def test_update_buckets_name_10_char_nonalphanumeric_case(self, ten_char_nonalphanumeric):
        '''
        TEST API: http://<gateway>/v1/buckets
        METHOD: PATCH
        tests bucket name containing randopm 10 non-alphanumeric characters can be updated and persisted in the etcd store.
        '''
        self.run_tests('test_update_buckets_name_10_char_nonalphanumeric_case ', ten_char_nonalphanumeric,
                       ten_char_nonalphanumeric, 1, ten_char_nonalphanumeric + '_updated', None)

    @pytest.mark.parametrize('twenty_char_nonalphanumeric', twenty_char_nonalphanumeric)
    def test_update_buckets_name_20_char_nonalphanumeric_case(self, twenty_char_nonalphanumeric):
        '''
        TEST API: http://<gateway>/v1/buckets
        METHOD: PATCH
        tests bucket name containing randopm 20 non-alphanumeric characters can be updated and persisted in the etcd store.
        '''
        self.run_tests('test_update_buckets_name_20_char_nonalphanumeric_case ', twenty_char_nonalphanumeric,
                       twenty_char_nonalphanumeric, 1, twenty_char_nonalphanumeric + '_updated', None)


    ####################################################
    #          Number Characters bucket Names          #
    ####################################################
    @pytest.mark.parametrize('one_char', digits)
    def test_update_buckets_name_single_char_numbers(self, one_char):
        '''
        REST API: http://<gateway>/v1/buckets
        METHOD: PATCH
        tests bucket name containing single digits can be updated and persisted in the etcd store.
        '''
        self.run_tests('test_update_buckets_name_single_char_numbers ', one_char, one_char, 1,
                       one_char + '_updated', None)

    @pytest.mark.parametrize('ten_char_numbers', ten_char_numbers)
    def test_update_buckets_name_10_char_numbers(self, ten_char_numbers):
        '''
        REST API: http://<gateway>/v1/buckets
        METHOD: PATCH
        tests bucket name containing randpm 10 digits can be updated and persisted in the etcd store.
        '''
        self.run_tests('test_update_buckets_name_10_char_numbers ', ten_char_numbers, ten_char_numbers, 1,
                       ten_char_numbers + '_updated', None)

    @pytest.mark.parametrize('five_char_numbers', five_char_numbers)
    def test_update_buckets_name_5_char_numbers(self, five_char_numbers):
        '''
        REST API: http://<gateway>/v1/buckets
        METHOD: PATCH
        tests bucket name containing randpm 5 digits can be updated and persisted in the etcd store.
        '''
        self.run_tests('test_update_buckets_name_5_char_numbers ', five_char_numbers, five_char_numbers, 1,
                       five_char_numbers + '_updated', None)

    #######################################
    #     Mix Characters bucket Names     #
    #######################################
    @pytest.mark.parametrize('twenty_char_names', twenty_char_names_list)
    def test_update_buckets_name_20_char_mix(self, twenty_char_names):
        '''
        REST API: http://<gateway>/v1/buckets
        METHOD: PATCH
        tests bucket name containing 20 mix characters can be updated and persisted in the etcd store.
        '''
        self.run_tests('test_update_buckets_name_20_char_mix ', twenty_char_names, twenty_char_names, 1,
                       twenty_char_names + '_updated', None)

    @pytest.mark.parametrize('fourty_char_names', fourty_char_names_list)
    def test_update_buckets_name_40_char_mix(self, fourty_char_names):
        '''
        REST API: http://<gateway>/v1/buckets
        METHOD: PATCH
        tests bucket name containing 40 mix characters can be updated and persisted in the etcd store.
        '''
        self.run_tests('test_update_buckets_name_40_char_mix ', fourty_char_names, fourty_char_names, 1,
                       fourty_char_names + '_updated', None)

    @pytest.mark.parametrize('two_hundred_char_name', two_hundred_char_name_list)
    def test_update_buckets_name_200_char_mix(self, two_hundred_char_name):
        '''
        REST API: http://<gateway>/v1/buckets
        METHOD: PATCH
        tests bucket name containing 200 mix characters can be updated and persisted in the etcd store.
        '''
        self.run_tests('test_update_buckets_name_200_char_mix ', two_hundred_char_name, two_hundred_char_name, 1,
                       two_hundred_char_name + '_updated', None)

    @pytest.mark.parametrize('four_hundred_char_name', four_hundred_char_name_list)
    def test_update_buckets_name_400_char_mix(self, four_hundred_char_name):
        '''
        REST API: http://<gateway>/v1/buckets
        METHOD: PATCH
        tests bucket name containing 400 mix characters can be updated and persisted in the etcd store.
        '''
        self.run_tests('test_update_buckets_name_400_char_mix ', four_hundred_char_name, four_hundred_char_name, 1,
                       four_hundred_char_name + '_updated', None)

    @pytest.mark.parametrize('special_char', special_char)
    def test_update_buckets_name_special_chars(self, special_char):
        '''
        REST API: http://<gateway>/v1/buckets
        METHOD: PATCH
        tests buckets name containing special characters can be updated and persisted in the etcd store.
        '''
        self.run_tests('test_update_buckets_name_special_chars ', special_char, special_char, 1,
                       special_char + '_updated', None)

    def test_update_buckets_name_already_exist(self):
        '''
        REST API: http://<gateway>/v1/buckets
        METHOD: PATCH
        tests buckets name can be updated and persisted in the etcd store if name already exists.
        '''
        org_name='test_org_name_already_exists'
        bucket_name='test_bucket_name_already_exists'
        self.run_tests('test_update_buckets_name_already_exist', org_name, bucket_name, 1, bucket_name, None)

    def test_update_buckets_to_empty_name(self):
        '''
        REST API: http://<gateway>/v1/buckets
        METHOD: PATCH
        tests bucket name can not be updated and persisted in the etcd store if name is empty
        '''
        org_name='test_org_name_empty_name'
        bucket_name='test_bucket_name'
        self.run_tests('test_update_buckets_to_empty_name', org_name, bucket_name, 1, '', None)



