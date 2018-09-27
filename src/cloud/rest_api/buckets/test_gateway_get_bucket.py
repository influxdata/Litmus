import pytest
import src.util.login_util as lu
from src.chronograf.lib import chronograf_rest_lib as crl
import src.util.gateway_util as gateway_util
from string import ascii_lowercase
from string import ascii_uppercase
from string import digits
from src.cloud.rest_api.conftest import ten_char_lc, twenty_char_lc, twenty_char_uc, ten_char_uc, \
    ten_char_numbers, five_char_numbers, nonalphanumeric, ten_char_nonalphanumeric, \
    twenty_char_nonalphanumeric, twenty_char_names_list, forty_char_names_list, \
    four_hundred_char_name_list, two_hundred_char_name_list, special_char, _assert, verify_org_etcd_entries, \
    verify_bucket_etcd_entries


@pytest.mark.usefixtures('remove_buckets', 'remove_orgs', 'gateway')
class TestGetBucketsAPI(object):
    """
    Test Suite for testing REST API endpoint for getting single bucket by id
    removes created by tests buckets and organizations
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

    def run_tests(self, name_of_the_test_to_run, org_name, bucket_name, retentionperiod):
        """
        :param name_of_the_test_to_run: test to be run
        :param org_name: name of the organization to be created
        :param bucket_name: name of the bucket to be created
        :param retentionperiod: retention period of the bucket
        :return: pass/fail
        """
        test_name = name_of_the_test_to_run + org_name + ' '
        self.header(test_name)
        self.mylog.info(test_name + ' STEP 1: Create Organization "%s"' % org_name)
        status, created_org_id, created_org_name, error_message = \
            gateway_util.create_organization(self, self.gateway, org_name)
        if org_name == '':
            _assert(self, status, 201, 'status code', xfail=True,
                    reason='https://github.com/influxdata/platform/issues/162')
        elif org_name == 'BackSlash\\':
            _assert(self, status, 201, 'status code', xfail=True,
                    reason='https://github.com/influxdata/platform/issues/163')
        else:
            _assert(self, status, 201, '')

        self.mylog.info(test_name + 'STEP 2: Verify org data was persisted in the etcd store')
        verify_org_etcd_entries(self, test_name, created_org_id, created_org_name, error='', get_index_values=True,
                                id_by_index_name=created_org_id, error_by_index_name='')

        self.mylog.info(test_name + 'STEP 3: Create Bucket "%s"' % bucket_name)
        status, created_bucket_id, created_bucket_name, organization_id, retention_period, error_message = \
            gateway_util.create_bucket(self, self.gateway, bucket_name, retentionperiod, created_org_id)
        if bucket_name == '':
            _assert(self, status, 201, 'status code', xfail=True,
                    reason='https://github.com/influxdata/platform/issues/162')
        elif bucket_name == 'BackSlash\\':
            _assert(self, status, 201, 'status code', xfail=True,
                    reason='https://github.com/influxdata/platform/issues/163')
        else:
            _assert(self, status, 201, 'status code')

        self.mylog.info(test_name + 'STEP 4: Verify bucket data was persisted in the etcd store')
        # since RP is stored in nanoseconds, need to convert PR that is passed to method (1h, 1m, 1s, etc) into int by
        # removing the last character that indicates the duration in our case - h (hour)
        exp_retention_period = int(retention_period[:-1]) * 3600000000000
        verify_bucket_etcd_entries(self, test_name, created_bucket_id, created_bucket_name, expected_error='',
                                   expected_retention_period=exp_retention_period)

        self.mylog.info(test_name + ' STEP 5: Get Created Bucket')
        status, actual_bucket_id, actual_bucket_name, error_message = \
            gateway_util.get_bucket_by_id(self, self.gateway, created_bucket_id)
        self.mylog.info(test_name + 'Assert actual status \'%s\'equals to expected status \'%s\'' % (status, 200))
        _assert(self, status, 200, '')
        self.mylog.info(test_name + 'Assert actual bucket_id \'%s\' equals to expected bucket id \'%s\''
                        % (actual_bucket_name, created_bucket_id))
        _assert(self, actual_bucket_id, created_bucket_id, '')
        self.mylog.info(test_name + 'Assert actual bucket_name \'%s\' equals to expected bucket_name \'%s\''
                        % (actual_bucket_name, created_bucket_name))
        _assert(self, actual_bucket_name, created_bucket_name, '')
        self.footer(test_name)

    ##############################################
    #   Lower Case Character Get bucket Name     #
    ##############################################
    @pytest.mark.parametrize('one_char', ascii_lowercase)
    def test_get_buckets_single_char_lower_case(self, one_char):
        """
        REST API: http://<gateway>/v1/buckets
        METHOD: GET
        tests created bucket using single lower case characters can be returned by using get bucket by id endpoint.
        """
        self.run_tests('test_get_buckets_single_char_lower_case_', one_char, one_char, '1h')

    @pytest.mark.parametrize('ten_char_lc', ten_char_lc)
    def test_get_buckets_10_char_lower_case(self, ten_char_lc):
        """
        REST API: http://<gateway>/v1/buckets
        METHOD: GET
        tests created bucket using 10 random lower case characters can be returned by using get bucket by id endpoint.
        """
        self.run_tests('test_get_buckets_10_char_lower_case_', ten_char_lc, ten_char_lc, '1h')

    @pytest.mark.parametrize('twenty_char_lc', twenty_char_lc)
    def test_get_buckets_20_char_lower_case(self, twenty_char_lc):
        """
        REST API: http://<gateway>/v1/buckets
        METHOD: GET
        tests created bucket using 20 random lower case characters can be returned by using get bucket by id endpoint.
        """
        self.run_tests('test_get_buckets_20_char_lower_case_', twenty_char_lc, twenty_char_lc, '1h')

    #####################################################
    #     Upper Case Character Get bucket Name          #
    #####################################################
    @pytest.mark.parametrize('one_char', ascii_uppercase)
    def test_get_buckets_single_char_upper_case(self, one_char):
        """
        REST API: http://<gateway>/v1/buckets
        METHOD: GET
        tests created bucket using single upper case characters can be returned by using get bucket by id endpoint.
        """
        self.run_tests('test_get_buckets_single_char_upper_case_', one_char, one_char, '1h')

    @pytest.mark.parametrize('ten_char_uc', ten_char_uc)
    def test_get_buckets_10_char_upper_case(self, ten_char_uc):
        """
        REST API: http://<gateway>/v1/buckets
        METHOD: GET
        tests created bucket using 10 random upper case characters can be returned by using get bucket by id endpoint.
        """
        self.run_tests('est_get_buckets_10_char_upper_case_', ten_char_uc, ten_char_uc, '1h')

    @pytest.mark.parametrize('twenty_char_uc', twenty_char_uc)
    def test_get_orgs_20_char_upper_case(self, twenty_char_uc):
        """
        REST API: http://<gateway>/v1/buckets
        METHOD: GET
        tests created bucket using 20 random upper case characters can be returned by using get bucket by id endpoint.
                """
        self.run_tests('test_get_orgs_20_char_upper_case_', twenty_char_uc, twenty_char_uc, '1h')

    ###########################################################
    #      Non-alphanumeric Character Get bucket Name         #
    ###########################################################
    @pytest.mark.parametrize('one_char', nonalphanumeric)
    def test_get_buckets_single_char_nonalphanumeric(self, one_char):
        """
        REST API: http://<gateway>/v1/buckets
        METHOD: GET
        tests created bucket using single non-alphanumeric characters can be returned by using get bucket by id endpoint.
        """
        self.run_tests('test_get_buckets_single_char_nonalphanumeric_', one_char, one_char, '1h')

    @pytest.mark.parametrize('ten_char_nonalphanumeric', ten_char_nonalphanumeric)
    def test_get_buckets_10_char_nonalphanumeric(self, ten_char_nonalphanumeric):
        """
        REST API: http://<gateway>/v1/buckets
        METHOD: GET
        tests created bucket using 10 random non-alphanumeric characters can be returned by using get bucket by id endpoint.
        """
        self.run_tests('test_get_orgs_10_char_nonalphanumeric_', ten_char_nonalphanumeric,
                       ten_char_nonalphanumeric, '1h')

    @pytest.mark.parametrize('twenty_char_nonalphanumeric', twenty_char_nonalphanumeric)
    def test_get_buckets_20_char_nonalphanumeric(self, twenty_char_nonalphanumeric):
        """
        REST API: http://<gateway>/v1/buckets
        METHOD: GET
        tests created bucket using 20 random non-alphanumeric characters can be returned by using get bucket by id endpoint.
        """
        self.run_tests('test_get_orgs_20_char_nonalphanumeric_',
                       twenty_char_nonalphanumeric, twenty_char_nonalphanumeric, '1h')

    ###################################################
    #      Number Characters Get bucket Name          #
    ###################################################
    @pytest.mark.parametrize('one_char', digits)
    def test_get_buckets_single_char_numbers(self, one_char):
        """
        REST API: http://<gateway>/v1/buckets
        METHOD: GET
        tests created bucket using single digits can be returned by using get bucket by id endpoint.
        """
        self.run_tests('test_get_buckets_single_char_numbers_', one_char, one_char, '1h')

    @pytest.mark.parametrize('ten_char_numbers', ten_char_numbers)
    def test_get_buckets_10_char_numbers(self, ten_char_numbers):
        """
        REST API: http://<gateway>/v1/buckets
        METHOD: GET
        tests created bucket using 10 random digits can be returned by using get bucket by id endpoint.
        """
        self.run_tests('test_get_buckets_10_char_numbers_', ten_char_numbers, ten_char_numbers, '1h')

    @pytest.mark.parametrize('five_char_numbers', five_char_numbers)
    def test_get_buckets_5_char_numbers(self, five_char_numbers):
        """
        REST API: http://<gateway>/v1/buckets
        METHOD: GET
        tests created bucket using 5 random digits can be returned by using get bucket by id endpoint.
        """
        self.run_tests('test_get_buckets_5_char_numbers_', five_char_numbers, five_char_numbers, '1h')

    ######################################
    #     Mix Characters Get bucket Name #
    ######################################
    @pytest.mark.parametrize('twenty_char', twenty_char_names_list)
    def test_get_buckets_20_char_name_mix(self, twenty_char):
        """
        REST API: http://<gateway>/v1/buckets
        METHOD: GET
        tests created bucket using 20 mix characters can be returned by using get bucket by id endpoint.
        """
        self.run_tests('test_get_buckets_20_char_name_mix_', twenty_char, twenty_char, '1h')

    @pytest.mark.parametrize('forty_char', forty_char_names_list)
    def test_get_buckets_40_char_name_mix(self, forty_char):
        """
        REST API: http://<gateway>/v1/buckets
        METHOD: GET
        tests created bucket using 40 mix characters can be returned by using get bucket by id endpoint.
                """
        self.run_tests('test_get_buckets_40_char_name_mix_', forty_char, forty_char, '1h')

    @pytest.mark.parametrize('two_hundred_char_names', two_hundred_char_name_list)
    def test_get_buckets_200_char_mix(self, two_hundred_char_names):
        """
        REST API: http://<gateway>/v1/buckets
        METHOD: GET
        tests created bucket using 200 mix characters can be returned by using get bucket by id endpoint.
        """
        self.run_tests('test_get_buckets_200_char_name_mix_', two_hundred_char_names, two_hundred_char_names, '1h')

    @pytest.mark.parametrize('four_hundred_char_names', four_hundred_char_name_list)
    def test_get_buckets_400_char_mix(self, four_hundred_char_names):
        """
        REST API: http://<gateway>/v1/buckets
        METHOD: GET
        tests created bucket using 400 mix characters can be returned by using get bucket by id endpoint.
                """
        self.run_tests('test_get_buckets_400_char_name_mix_', four_hundred_char_names, four_hundred_char_names, '1h')

    @pytest.mark.parametrize('special_char', special_char)
    def test_get_buckets_special_chars(self, special_char):
        """
        REST API: http://<gateway>/v1/buckets
        METHOD: GET
        tests created bucket using special characters can be returned by using get bucket by id endpoint.
        """
        self.run_tests('test_get_buckets_special_chars_', special_char, special_char, '1h')

    def test_get_non_existent_bucket_id(self):
        """
        REST API: http://<gateway>/v1/buckets
        METHOD: GET
        tests getting non-existent bucket returns an error.
        """
        test_name = 'test_get_non_existent_bucket_id '
        bucket_id = 'doesnotexist'
        expected_status = 404
        expected_error_message = 'bucket not found'
        self.header(test_name)
        self.mylog.info(test_name + 'STEP 1: Get non-existent bucket id')
        status, actual_bucket_id, actual_bucket_name, error_message = \
            gateway_util.get_bucket_by_id(self, self.gateway, bucket_id)
        self.mylog.info(test_name + 'Assert actual status \'%s\' equals to expected status \'%s\'' % (status, expected_status))
        _assert(self, status, expected_status, 'status code', xfail=True,
                 reason='status code is \'%s\'' % status)
        self.mylog.info(test_name + 'Assert actual error message \'%s\' equals to expected error message \'%s\''
                        % (error_message, expected_error_message))
        _assert(self, error_message, expected_error_message, '')
