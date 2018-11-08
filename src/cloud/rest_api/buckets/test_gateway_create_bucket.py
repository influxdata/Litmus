from string import ascii_lowercase
from string import ascii_uppercase
from string import digits

import pytest

import src.util.login_util as lu
from src.chronograf.lib import chronograf_rest_lib as crl
from src.cloud.rest_api.conftest import ten_char_lc, twenty_char_lc, twenty_char_uc, ten_char_uc, \
    ten_char_numbers, five_char_numbers, nonalphanumeric, ten_char_nonalphanumeric, \
    twenty_char_nonalphanumeric, twenty_char_names_list, forty_char_names_list, \
    four_hundred_char_name_list, two_hundred_char_name_list, special_char, _assert, verify_org_etcd_entries, \
    verify_bucket_etcd_entries
from src.util.twodotoh import buckets_util
from src.util.twodotoh import org_util


@pytest.mark.usefixtures('remove_buckets', 'remove_orgs', 'gateway')
class TestCreateBucketsAPI(object):
    """
    Test Suite for testing REST API endpoint for creating buckets
    The existing buckets and organizations would be removed before running tests
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

    def run_tests(self, name_of_the_test_to_run, org_name, bucket_name, retention_period):
        """
        :param name_of_the_test_to_run: test to be run
        :param org_name: name of the org to be created
        :param bucket_name: name of the bucket to be created
        :param retention_period: retention period of the bucket. how long keep the data for. Default is 0s (forever)
        :return: pass/fail
        """
        test_name = name_of_the_test_to_run + org_name + ' '
        self.header(test_name)
        self.mylog.info(test_name + ' STEP 1: Create Organization \'%s\'' % org_name)
        self.mylog.info('')
        create_org_result = org_util.create_organization(self, self.gateway, org_name)
        status = create_org_result['status']
        created_org_id = create_org_result['org_id']
        created_org_name = create_org_result['org_name']

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
        create_bucket_result = \
            buckets_util.create_bucket(self, self.gateway, bucket_name, retention_period, created_org_id)
        status = create_bucket_result['status']
        created_bucket_id = create_bucket_result['bucket_id']
        created_bucket_name = create_bucket_result['bucket_name']

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
        # exp_retention_period = int(retention_period[:-1]) * 3600000000000
        verify_bucket_etcd_entries(self, test_name, created_bucket_id, created_bucket_name, expected_error='',
                                   expected_retention_period=3600000000000)
        self.footer(test_name)

    ############################################
    #       Lower Case Character Bucket Names  #
    ############################################

    @pytest.mark.parametrize('one_char', ascii_lowercase)
    def test_create_buckets_single_char_lower_case(self, one_char):
        """
        REST API: http://<gateway>/api/v2/buckets
        METHOD: POST
        tests bucket name containing single character lower case letters can be created and persisted in the etcd store.
        Test Steps:
        1. Create an org with the name containing a single lower case ascii character [abcdefghijklmnopqrstuvwxyz] list.
        2. Verify org name and org id persisted in the etcd store.
        3. Create a bucket with the name containing the same lower case ascii character as the organization name.
        4. Verify bucket name and bucket id persisted in the etcd store.
        """
        self.run_tests('test_create_buckets_single_char_lower_case ', one_char, one_char, 3600)

    @pytest.mark.parametrize('ten_char_lc', ten_char_lc)
    def test_create_buckets_10_char_lower_case(self, ten_char_lc):
        """
        REST API: http://<gateway>/api/v2/buckets
        METHOD: POST
        tests bucket name containing random 10 lower case letters can be created and persisted in the etcd store.
        Test Steps:
        1. Create an org with the name containing 10 random lower case ascii characters from the
           [abcdefghijklmnopqrstuvwxyz] list.
        2. Verify org name and org id persisted in the etcd store.
        3. Create a bucket with the name containing the same lower case ascii characters as the organization name.
        4. Verify bucket name and bucket id persisted in the etcd store.
        """
        self.run_tests('test_create_buckets_10_char_lower_case ', ten_char_lc, ten_char_lc, 3600)

    @pytest.mark.parametrize('twenty_char_lc', twenty_char_lc)
    def test_create_buckets_20_char_lower_case(self, twenty_char_lc):
        """
        REST API: http://<gateway>/api/v2/buckets
        METHOD: POST
        tests bucket name containing random 20 lower case letters can be created and persisted in the etcd store.
        Test Steps:
        1. Create an org with the name containing 20 random lower case ascii characters from the
           [abcdefghijklmnopqrstuvwxyz] list.
        2. Verify org name and org id persisted in the etcd store.
        3. Create a bucket with the name containing the same lower case ascii characters as the organization name.
        4. Verify bucket name and bucket id persisted in the etcd store.
        """
        self.run_tests('test_create_buckets_20_char_lower_case ', twenty_char_lc, twenty_char_lc, 3600)

    ######################################################
    #          Upper Case Character Bucket Names         #
    ######################################################
    @pytest.mark.parametrize('one_char', ascii_uppercase)
    def test_create_buckets_single_char_upper_case(self, one_char):
        """
        REST API: http://<gateway>/api/v2/buckets
        METHOD: POST
        tests bucket name containing single character upper case letters can be created and persisted in the etcd store.
        Test Steps:
        1. Create an org with the name containing a single upper case ascii character [ABCDEFGHIJKLMNOPQRSTUVWXYZ] list.
        2. Verify org name and org id persisted in the etcd store.
        3. Create a bucket with the name containing the same upper case ascii character as the organization name.
        4. Verify bucket name and bucket id persisted in the etcd store.
        """

        self.run_tests('test_create_buckets_single_char_upper_case ', one_char, one_char, 3600)

    @pytest.mark.parametrize('ten_char_uc', ten_char_uc)
    def test_create_buckets_10_char_upper_case(self, ten_char_uc):
        """
        REST API: http://<gateway>/api/v2/buckets
        METHOD: POST
        tests bucket name containing random 10 upper case letters can be created and persisted in the etcd store.
        Test Steps:
        1. Create an org with the name containing 10 random upper case ascii characters from the
           [ABCDEFGHIJKLMNOPQRSTUVWXYZ] list.
        2. Verify org name and org id persisted in the etcd store.
        3. Create a bucket with the name containing the same upper case ascii characters as the organization name.
        4. Verify bucket name and bucket id persisted in the etcd store.
        """
        self.run_tests('test_create_buckets_10_char_upper_case ', ten_char_uc, ten_char_uc, 3600)

    @pytest.mark.parametrize('twenty_char_uc', twenty_char_uc)
    def test_create_buckets_20_char_upper_case(self, twenty_char_uc):
        """
        REST API: http://<gateway>/api/v2/buckets
        METHOD: POST
        tests bucket name containing random 20 upper case letters can be created and persisted in the etcd store.
        Test Steps:
        3600. Create an org with the name containing 20 random upper case ascii characters from the
           [ABCDEFGHIJKLMNOPQRSTUVWXYZ] list.
        2. Verify org name and org id persisted in the etcd store.
        3. Create a bucket with the name containing the same upper case ascii characters as the organization name.
        4. Verify bucket name and bucket id persisted in the etcd store.
        """
        self.run_tests('test_create_buckets_20_char_upper_case ', twenty_char_uc, twenty_char_uc, 3600)

    ############################################################
    #          Non-alphanumeric Character Bucket Names         #
    ############################################################
    @pytest.mark.parametrize('one_char', nonalphanumeric)
    def test_create_buckets_single_char_nonalphanumeric_case(self, one_char):
        """
        REST API: http://<gateway>/api/v2/buckets
        METHOD: POST
        tests bucket name containing single non-alphanumeric characters can be created and persisted in the etcd store.
        Test Steps:
        1. Create an org with the name containing single non-alphanumeric character from the
           [!@#$%^*><&()_+{}[]|,.~/`?] list. (",\ and ' is a separate test case)
        2. Verify org name and org id persisted in the etcd store.
        3. Create a bucket with the name containing the same non-alphanumeric character as the organization name.
        4. Verify bucket name and bucket id persisted in the etcd store.
        """
        self.run_tests('test_create_buckets_single_char_nonalphanumeric_case ', one_char, one_char, 3600)

    @pytest.mark.parametrize('ten_char_nonalphanumeric', ten_char_nonalphanumeric)
    def test_create_buckets_10_char_nonalphanumeric_case(self, ten_char_nonalphanumeric):
        """
        REST API: http://<gateway>/api/v2/buckets
        METHOD: POST
        tests bucket name containing 10 random non-alphanumeric characters can be created and persisted in the etcd store.
        Test Steps:
        1. Create an org with the name containing 10 random non-alphanumeric characters from the
           [!@#$%^*><&()_+{}[]|,.~/`?] list. (",\ and ' is a separate test case)
        2. Verify org name and org id persisted in the etcd store.
        3. Create a bucket with the name containing the same non-alphanumeric characters as the organization name.
        4. Verify bucket name and bucket id persisted in the etcd store.
        """
        self.run_tests('test_create_buckets_10_char_nonalphanumeric_case ',
                       ten_char_nonalphanumeric, ten_char_nonalphanumeric, 3600)

    @pytest.mark.parametrize('twenty_char_nonalphanumeric', twenty_char_nonalphanumeric)
    def test_create_buckets_20_char_nonalphanumeric_case(self, twenty_char_nonalphanumeric):
        """
        REST API: http://<gateway>/api/v2/buckets
        METHOD: POST
        tests bucket name containing 20 random non-alphanumeric characters can be created and persisted in the etcd store.
        Test Steps:
        1. Create an org with the name containing 20 random non-alphanumeric characters from the
           [!@#$%^*><&()_+{}[]|,.~/`?] list. (",\ and ' is a separate test case)
        2. Verify org name and org id persisted in the etcd store.
        3. Create a bucket with the name containing the same non-alphanumeric characters as the organization name.
        4. Verify bucket name and bucket id persisted in the etcd store.
        """
        self.run_tests('test_create_buckets_20_char_nonalphanumeric_case ',
                       twenty_char_nonalphanumeric, twenty_char_nonalphanumeric, 3600)

    ####################################################
    #          Number Characters Bucket Names          #
    ####################################################
    @pytest.mark.parametrize('one_char', digits)
    def test_create_buckets_single_char_numbers(self, one_char):
        """
        REST API: http://<gateway>/api/v2/buckets
        METHOD: POST
        tests bucket name containing single digits can be created and persisted in the etcd store
        Test Steps:
        1. Create an org with the name containing single digit from the [0123456789] list.
        2. Verify org name and org id persisted in the etcd store.
        3. Create a bucket with the name containing the same single digit as the organization name.
        4. Verify bucket name and bucket id persisted in the etcd store.
        """
        self.run_tests('test_create_buckets_single_char_numbers ', one_char, one_char, 3600)

    @pytest.mark.parametrize('ten_char_numbers', ten_char_numbers)
    def test_create_buckets_10_char_numbers(self, ten_char_numbers):
        """
        REST API: http://<gateway>/api/v2/buckets
        METHOD: POST
        tests bucket name containing 10 random digits can be created and persisted in the etcd store.
        Test Steps:
        1. Create an org with the name containing 10 random digits from the [0123456789] list.
        2. Verify org name and org id persisted in the etcd store.
        3. Create a bucket with the name containing the same 10 random digits as the organization name.
        4. Verify bucket name and bucket id persisted in the etcd store.
        """
        self.run_tests('test_create_buckets_10_char_numbers', ten_char_numbers, ten_char_numbers, 3600)

    @pytest.mark.parametrize('five_chars', five_char_numbers)
    def test_create_buckets_5_char_numbers(self, five_chars):
        """
        REST API: http://<gateway>/api/v2/buckets
        METHOD: POST
        tests bucket name containing 5 random digits can be created and persisted in the etcd store.
        Test Steps:
        1. Create an org with the name containing 20 random digits from the [0123456789] list.
        2. Verify org name and org id persisted in the etcd store.
        3. Create a bucket with the name containing the same 20 random digits as the organization name.
        4. Verify bucket name and bucket id persisted in the etcd store.
        """
        self.run_tests('test_create_buckets_5_char_numbers', five_chars, five_chars, 3600)

    #######################################
    #     Mix Characters Bucket Names     #
    #######################################
    @pytest.mark.parametrize('twenty_char_names', twenty_char_names_list)
    def test_create_buckets_20_char_mix(self, twenty_char_names):
        """
        REST API: http://<gateway>/api/v2/buckets
        METHOD: POST
        tests bucket name containing 20 mix characters can be created and persisted in the etcd store.
        """
        self.run_tests('test_create_buckets_20_char_mix ', twenty_char_names, twenty_char_names, 3600)

    @pytest.mark.parametrize('forty_char_names', forty_char_names_list)
    def test_create_buckets_40_char_mix(self, forty_char_names):
        """
        REST API: http://<gateway>/api/v2/buckets
        METHOD: POST
        tests bucket name containing 40 mix characters can be created and persisted in the etcd store.
        """
        self.run_tests('test_create_buckets_40_char_mix ', forty_char_names, forty_char_names, 3600)

    @pytest.mark.parametrize('special_char', special_char)
    def test_create_buckets_special_chars(self, special_char):
        """
        REST API: http://<gateway>/api/v2/buckets
        METHOD: POST
        tests bucket name containing special characters can be created and persisted in the etcd store.
        """
        self.run_tests('test_create_buckets_special_chars ', special_char, special_char, 3600)

    @pytest.mark.parametrize('two_hundred_char_names', two_hundred_char_name_list)
    def test_create_buckets_200_char_mix(self, two_hundred_char_names):
        """
        REST API: http://<gateway>/api/v2/buckets
        METHOD: POST
        tests bucket name containing 200 mix characters can be created and persisted in the etcd store.
        """
        self.run_tests('test_create_buckets_200_char_mix ', two_hundred_char_names, two_hundred_char_names, 3600)

    @pytest.mark.parametrize('four_hundred_char_names', four_hundred_char_name_list)
    def test_create_buckets_400_char_mix(self, four_hundred_char_names):
        """
        REST API: http://<gateway>/api/v2/buckets
        METHOD: POST
        tests bucket name containing 400 mix characters can be created and persisted in the etcd store.
        """
        self.run_tests('test_create_buckets_400_char_mix ', four_hundred_char_names, four_hundred_char_names, 3600)

    def test_create_many_buckets_same_org(self):
        """
        REST API: http://<gateway>/api/v2/buckets
        METHOD: POST
        tests many buckets with different names can be created for the same organization.
        """
        org_name = 'one_for_all'
        test_name = 'test_create_many_buckets_same_org '
        self.header(test_name)
        self.mylog.info(test_name + 'STEP 1: Create Organization \'%s\'' % org_name)
        create_org_result = org_util.create_organization(self, self.gateway, org_name)
        status = create_org_result['status']
        created_org_id = create_org_result['org_id']
        created_org_name = create_org_result['org_name']

        self.mylog.info(test_name + 'Assert actual status \'%s\' equals to expected status 201' % status)
        _assert(self, status, 201, '')

        self.mylog.info(test_name + 'STEP 2: Verify org data was persisted in the etcd store')
        verify_org_etcd_entries(self, test_name, created_org_id, created_org_name, error='', get_index_values=True,
                                id_by_index_name=created_org_id, error_by_index_name='')

        self.mylog.info(test_name + 'STEP 3: Create Multiple Buckets for "%s" name' % org_name)
        for bucket_name in ascii_lowercase:
            self.mylog.info(test_name + 'Creating bucket \'%s\' name' % bucket_name)
            create_bucket_result = \
                buckets_util.create_bucket(self, self.gateway, bucket_name, 3600, created_org_id)
            status = create_bucket_result['status']
            created_bucket_id = create_bucket_result['bucket_id']

            self.mylog.info(test_name + 'Assert actual status \'%s\' equals to expected status 201' % status)
            _assert(self, status, 201, '')
            self.mylog.info(test_name + 'Verify bucket data was persisted in the etcd store')
            verify_bucket_etcd_entries(self, test_name, created_bucket_id, bucket_name, expected_error='',
                                       expected_retention_period=3600000000000)
        self.footer(test_name)

    def test_create_same_bucket_different_orgs(self):
        """
        REST API: http://<gateway>/api/v2/buckets
        METHOD: POST
        tests bucket with the same name can be created for different organizations
        """
        bucket_name = 'one_for_all'
        test_name = 'test_create_same_bucket_different_orgs '
        self.header(test_name)
        for org_name in ascii_lowercase:
            org_name = org_name + '_same_bucket_name'

            self.mylog.info(test_name + 'STEP 1: Create Organization \'%s\'' % org_name)
            create_org_result = org_util.create_organization(self, self.gateway, org_name)
            status = create_org_result['status']
            created_org_id = create_org_result['org_id']
            created_org_name = create_org_result['org_name']

            self.mylog.info(test_name + 'Assert actual status \'%s\' equals to expected status 201' % status)
            _assert(self, status, 201, '')

            self.mylog.info(test_name + 'STEP2: Verify org data was persisted in the etcd store')
            verify_org_etcd_entries(self, test_name, created_org_id, created_org_name, error='', get_index_values=True,
                                    id_by_index_name=created_org_id, error_by_index_name='')

            self.mylog.info(test_name + 'STEP 3: Create Bucket \'%s\' name for org \'%s\' name'
                            % (bucket_name, org_name))
            create_bucket_result = \
                buckets_util.create_bucket(self, self.gateway, bucket_name, 3600, created_org_id)
            status = create_bucket_result['status']
            created_bucket_id = create_bucket_result['bucket_id']

            self.mylog.info(test_name + 'Assert actual status \'%s\' equals to expected status 201' % status)
            _assert(self, status, 201, '')

            self.mylog.info(test_name + 'STEP 4: Verify bucket data was persisted in the etcd store')
            verify_bucket_etcd_entries(self, test_name, created_bucket_id, bucket_name, expected_error='',
                                       expected_retention_period=3600000000000)
        self.footer(test_name)

    def test_create_duplicate_bucket(self):
        """
        REST API: http://<gateway>/api/v2/buckets
        METHOD: POST
        tests cannot create bucket with already existing name with the same org.
        """
        test_name = 'test_create_duplicate_bucket '
        org_name = 'orgname'
        bucket_name = 'dupbucketname'
        expected_error_message = 'bucket with name dupbucketname already exists'
        self.header(test_name)
        self.mylog.info(test_name + ' STEP 1: Create Organization \'%s\'' % org_name)
        create_org_result = org_util.create_organization(self, self.gateway, org_name)
        status = create_org_result['status']
        created_org_id = create_org_result['org_id']
        created_org_name = create_org_result['org_name']

        self.mylog.info(test_name + 'Assert actual status \'%s\' equals to expected status 201' % status)
        _assert(self, status, 201, '')

        self.mylog.info(test_name + 'STEP 2: Verify org data was persisted in the etcd store')
        verify_org_etcd_entries(self, test_name, created_org_id, created_org_name, error='', get_index_values=True,
                                id_by_index_name=created_org_id, error_by_index_name='')

        self.mylog.info(test_name + 'STEP 3: Create Bucket \'%s\'' % bucket_name)
        create_bucket_result = \
            buckets_util.create_bucket(self, self.gateway, bucket_name, 3600, created_org_id)
        status = create_bucket_result['status']
        created_bucket_id = create_bucket_result['bucket_id']

        self.mylog.info(test_name + 'Assert actual status \'%s\' equals to expected status 201' % status)
        _assert(self, status, 201, 'status code')

        self.mylog.info(test_name + 'STEP 4: Verify bucket data was persisted in the etcd store')
        verify_bucket_etcd_entries(self, test_name, created_bucket_id, bucket_name, expected_error='',
                                   expected_retention_period=3600000000000)

        self.mylog.info(test_name + 'STEP 5: Create Bucket with already existing name for the same org')
        create_bucket_result = \
            buckets_util.create_bucket(self, self.gateway, bucket_name, 3600, created_org_id)
        error_message = create_bucket_result['error_message']

        _assert(self, error_message, expected_error_message, 'error message')
        self.footer(test_name)

    def test_create_bucket_no_org_id(self):
        """
        REST API: http://<gateway>/api/v2/buckets
        METHOD: POST
        tests cannot create bucket if organization id is not provided
        """
        test_name = 'test_create_bucket_no_org_id'
        bucket_name = 'bucket_no_org_id'
        self.header(test_name)
        self.mylog.info(test_name + 'STEP 1: Create Bucket \'%s\' without ORG ID' % bucket_name)
        create_bucket_result = buckets_util.create_bucket(self, self.gateway, bucket_name, 3600)
        status = create_bucket_result['status']

        _assert(self, status, 404, 'status code', xfail=True, reason='status=%s' % status)

    def test_create_bucket_default_rp(self):
        """
        REST API: http://<gateway>/api/v2/buckets
        METHOD: POST
        tests bucket cannot be created if retention policy is not provided, (was before: default RP is used: 0s))
        """
        test_name = 'test_create_bucket_default_rp'
        org_name = 'org_default_rp'
        bucket_name = 'bucket_default_rp'
        self.header(test_name)
        self.mylog.info(test_name + ' STEP 1: Create Organization "%s"' % org_name)
        create_org_result = org_util.create_organization(self, self.gateway, org_name)
        status = create_org_result['status']
        created_org_id = create_org_result['org_id']
        created_org_name = create_org_result['org_name']

        self.mylog.info(test_name + 'Assert actual status \'%s\' equals to expected status 201' % status)
        _assert(self, status, 201, 'status code')

        self.mylog.info(test_name + 'STEP 2: Verify org data was persisted in the etcd store')
        verify_org_etcd_entries(self, test_name, created_org_id, created_org_name, error='', get_index_values=True,
                                id_by_index_name=created_org_id, error_by_index_name='')

        self.mylog.info(test_name + 'STEP 3: Create Bucket \'%s\'' % bucket_name)
        create_bucket_result = \
            buckets_util.create_bucket(self, self.gateway, bucket_name, retention_rules=None,
                                       organization_id=created_org_id)
        status = create_bucket_result['status']
        created_bucket_id = create_bucket_result['bucket_id']
        retention_period = create_bucket_result['every_seconds']

        self.mylog.info(test_name + 'Assert actual status \'%s\' equals to expected status 201' % status)
        _assert(self, status, 201, 'status code')
        self.mylog.info(test_name + 'Assert actual RP \'%s\' equals to expected RP \'%s\'' % (retention_period, 0))
        _assert(self, retention_period, 0, 'retention policy')
        self.mylog.info(test_name + 'STEP 4: Verify bucket data was persisted in the etcd store')
        verify_bucket_etcd_entries(self, test_name, created_bucket_id, bucket_name, expected_error='',
                                   expected_retention_period=0)
        self.footer(test_name)
