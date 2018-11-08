import pytest
import src.util.login_util as lu
import src.util.twodotoh.buckets_util as buckets_util
import src.util.twodotoh.org_util as org_util

from src.chronograf.lib import chronograf_rest_lib as crl
from string import ascii_lowercase
from string import ascii_uppercase
from string import digits
from src.cloud.rest_api.conftest import ten_char_lc, twenty_char_lc, twenty_char_uc, ten_char_uc, \
    ten_char_numbers, five_char_numbers, nonalphanumeric, ten_char_nonalphanumeric, \
    twenty_char_nonalphanumeric, twenty_char_names_list, forty_char_names_list, \
    four_hundred_char_name_list, two_hundred_char_name_list, special_char, _assert, verify_bucket_etcd_entries, \
    verify_org_etcd_entries


@pytest.mark.usefixtures('remove_buckets', 'remove_orgs', 'gateway')
class TestUpdateBucketsNameAPI(object):
    """
    Test suite to test rest api endpoint for updating Bucket's Name
    removes created by tests organizations and buckets
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

    def run_tests(self, name_of_the_test_to_run, org_name, bucket_name, retention_period, new_bucket_name=None,
                  new_retention=None):
        """
        :param name_of_the_test_to_run: test to be run
        :param org_name: name of the organization to be created
        :param bucket_name: name of the bucket to be created
        :param retention_period: retention period for the bucket
        :param new_bucket_name: name of the bucket to update to
        :param new_retention: retention period to update to
        :return: pass/fail
        """
        test_name = name_of_the_test_to_run + org_name + ' '
        new_bucket_name_to_assert = ''
        if org_name == 'DoubleQuotes\\"':
            new_bucket_name_to_assert = 'DoubleQuotes"_updated'

        self.header(test_name)
        self.mylog.info(test_name + ' STEP 1: Create Organization \'%s\'' % org_name)
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
        created_retention = create_bucket_result['every_seconds']
        created_organization_id = create_bucket_result['org_id']

        if bucket_name == '':
            _assert(self, status, 201, 'status code', xfail=True,
                    reason='https://github.com/influxdata/platform/issues/162')
        elif bucket_name == 'BackSlash\\':
            _assert(self, status, 201, 'status code', xfail=True,
                    reason='https://github.com/influxdata/platform/issues/163')
        else:
            _assert(self, status, 201, 'status code')

        self.mylog.info(test_name + 'STEP 4: Verify bucket data was persisted in the etcd store')
        verify_bucket_etcd_entries(self, test_name, created_bucket_id, created_bucket_name, expected_error='',
                                   expected_retention_period=3600000000000)

        # Neither bucket name, nor the retention period are being updated.
        if new_bucket_name is None and new_retention is None:
            self.mylog.info(test_name + 'STEP 5: Bucket info is not getting updated')
            update_bucket_result = \
                buckets_util.update_bucket(self, self.gateway, created_bucket_id, created_bucket_name,
                                           created_retention, new_bucket_name=None, new_retention=None)
            updated_bucket_name = update_bucket_result['bucket_name']
            retention = update_bucket_result['every_seconds']
            status = update_bucket_result['status']
            bucket_id = update_bucket_result['bucket_id']
            organization_id = update_bucket_result['org_id']

            self.mylog.info(test_name + 'Assert updated bucket name \'%s\' equals to expected bucket name \'%s\''
                            % (updated_bucket_name, created_bucket_name))
            _assert(self, updated_bucket_name, created_bucket_name, 'bucket name')
            self.mylog.info(test_name + 'Assert actual retention \'%s\' equals to expected \'%s\' retention'
                            % (retention, created_retention))
            _assert(self, retention, created_retention, 'retention period')
        # only bucket name is being updated
        elif new_bucket_name is not None and new_retention is None:
            self.mylog.info(test_name + 'STEP 5: Update created bucket with \'%s\' name' % new_bucket_name)
            update_bucket_result = \
                buckets_util.update_bucket(self, self.gateway, created_bucket_id, created_bucket_name,
                                           created_retention, new_bucket_name, new_retention=None)
            updated_bucket_name = update_bucket_result['bucket_name']
            retention = update_bucket_result['every_seconds']
            status = update_bucket_result['status']
            bucket_id = update_bucket_result['bucket_id']
            organization_id = update_bucket_result['org_id']

            if org_name == 'DoubleQuotes\\"':
                self.mylog.info(test_name + 'Assert updated bucket_name \'%s\' equals to expected bucket_name \'%s\''
                                % (updated_bucket_name, new_bucket_name_to_assert))
                _assert(self, updated_bucket_name, new_bucket_name_to_assert, 'bucket name')
            else:
                self.mylog.info(test_name + 'Assert updated bucket_name \'%s\' equals to expected bucket_name \'%s\''
                                % (updated_bucket_name, new_bucket_name))
                _assert(self, updated_bucket_name, new_bucket_name, '')
            self.mylog.info(test_name + 'Assert updated retention \'%s\' equals to expected retention \'%s\''
                            % (retention, created_retention))
            _assert(self, retention, created_retention, 'retention period')
        # only retention is being updated
        elif new_bucket_name is None and new_retention is not None:
            self.mylog.info(test_name + 'STEP 5: Update created bucket with \'%d\' retention name' % new_retention)
            update_bucket_result = \
                buckets_util.update_bucket(self, self.gateway, created_bucket_id, created_bucket_name,
                                           created_retention, new_bucket_name=None, new_retention=new_retention)
            updated_bucket_name = update_bucket_result['bucket_name']
            retention = update_bucket_result['every_seconds']
            status = update_bucket_result['status']
            bucket_id = update_bucket_result['bucket_id']
            organization_id = update_bucket_result['org_id']

            self.mylog.info(test_name + 'Assert updated bucket_name \'%s\' equals to expected bucket_name \'%s\''
                            % (updated_bucket_name, created_bucket_name))
            _assert(self, updated_bucket_name, created_bucket_name, 'bucket name')
            self.mylog.info(test_name + 'Assert updated retention \'%s\' equals to expected retention \'%s\''
                            % (retention, new_retention))
            _assert(self, retention, new_retention, 'retention period')
        # bucket name and retention period are being updated
        else:
            self.mylog.info(test_name + 'STEP 5: Update created bucket with \'%s\' bucket name and \'%d\' retention'
                            % (new_bucket_name, new_retention))
            update_bucket_result = \
                buckets_util.update_bucket(self, self.gateway, created_bucket_id, created_bucket_name,
                                           created_retention, new_bucket_name, new_retention)
            retention = update_bucket_result['every_seconds']
            updated_bucket_name = update_bucket_result['bucket_name']
            status = update_bucket_result['status']
            bucket_id = update_bucket_result['bucket_id']
            organization_id = update_bucket_result['org_id']

            self.mylog.info(test_name + 'Assert updated retention \'%s\' equals to expected retention \'%s\''
                            % (retention, new_retention))
            _assert(self, retention, new_retention, 'retention period')
            if org_name == 'DoubleQuotes\\"':
                self.mylog.info(test_name + 'Assert updated bucket_name \'%s\' equals to expected bucket_name \'%s\''
                                % (updated_bucket_name, new_bucket_name_to_assert))
                _assert(self, updated_bucket_name, new_bucket_name_to_assert, 'bucket name')
            else:
                self.mylog.info(test_name + 'Assert updated bucket_name \'%s\' equals to expected bucket_name \'%s\''
                                % (updated_bucket_name, new_bucket_name))
                _assert(self, updated_bucket_name, new_bucket_name, '')
        self.mylog.info(test_name + 'Assert actual status \'%s\' equals to expected status \'%s\'' % (status, 200))
        _assert(self, status, 200, 'status code')
        self.mylog.info(test_name + 'Assert actual bucket_id \'%s\' equals to expected bucket_id \'%s\''
                        % (bucket_id, created_bucket_id))
        _assert(self, bucket_id, created_bucket_id, 'bucket id')
        self.mylog.info(test_name + 'Assert actual org_id \'%s\' equals to expected org_id \'%s\''
                        % (organization_id, created_organization_id))
        _assert(self, organization_id, created_organization_id, 'organization id')
        self.mylog.info('')

        self.mylog.info(test_name + 'STEP 6: Verify updated bucket info was persisted in the etcd store')
        verify_bucket_etcd_entries(self, test_name, bucket_id, updated_bucket_name, expected_error='',
                                   expected_retention_period=3600000000000)
        self.footer(test_name)

    ###############################################
    #       Lower Case Character Bucket Names     #
    ###############################################

    @pytest.mark.parametrize('one_char', ascii_lowercase)
    def test_update_buckets_name_single_char_lower_case(self, one_char):
        """
        REST API: http://<gateway>/api/v2/buckets
        METHOD: PATCH
        tests bucket name containing single character lower case letters can be updated and persisted in the etcd store.
        """
        self.run_tests('test_update_buckets_name_single_char_lower_case ',
                       one_char, one_char, 3600, one_char + '_updated', None)

    @pytest.mark.parametrize('ten_char_lc', ten_char_lc)
    def test_update_buckets_name_10_char_lower_case(self, ten_char_lc):
        """
        TEST API: http://<gateway>/api/v2/buckets
        METHOD: PATCH
        tests bucket name containing random 10 lower case letters can be updated and persisted in the etcd store.
        """
        self.run_tests('test_update_buckets_name_10_char_lower_case ', ten_char_lc, ten_char_lc, 3600,
                       ten_char_lc + '_updated', None)

    @pytest.mark.parametrize('twenty_char_lc', twenty_char_lc)
    def test_update_buckets_name_20_char_lower_case(self, twenty_char_lc):
        """
        TEST API: http://<gateway>/api/v2/buckets
        METHOD: PATCH
        tests bucket name containing random 20 lower case letters can be updated and persisted in the etcd store.
        """
        self.run_tests('test_update_buckets_name_20_char_lower_case ', twenty_char_lc, twenty_char_lc, 3600,
                       twenty_char_lc + '_updated', None)

    ######################################################
    #          Upper Case Character Bucket Names         #
    ######################################################
    @pytest.mark.parametrize('one_char', ascii_uppercase)
    def test_update_buckets_name_single_char_upper_case(self, one_char):
        """
        TEST API: http://<gateway>/api/v2/buckets
        METHOD: PATCH
        tests bucket name containing single upper case letters can be updated and persisted in the etcd store.
        """
        self.run_tests('test_update_buckets_name_single_char_upper_case ', one_char, one_char, 3600,
                       one_char + '_updated', None)

    @pytest.mark.parametrize('ten_char_uc', ten_char_uc)
    def test_update_buckets_name_10_char_upper_case(self, ten_char_uc):
        """
        TEST API: http://<gateway>/api/v2/buckets
        METHOD: PATCH
        tests bucket name containing random 10 upper case letters can be updated and persisted in the etcd store.
        """
        self.run_tests('test_update_buckets_name_10_char_upper_case ', ten_char_uc, ten_char_uc, 3600,
                       ten_char_uc + '_updated', None)

    @pytest.mark.parametrize('twenty_char_uc', twenty_char_uc)
    def test_update_buckets_name_20_char_upper_case(self, twenty_char_uc):
        """
        TEST API: http://<gateway>/api/v2/buckets
        METHOD: PATCH
        tests buckets name containing random 20 upper case letters can be updated and persisted in the etcd store.
        """
        self.run_tests('test_update_buckets_name_20_char_upper_case ', twenty_char_uc, twenty_char_uc, 3600,
                       twenty_char_uc + '_updated', None)

    #############################################################
    #          Non-alphanumeric Character Buckets Names         #
    #############################################################
    @pytest.mark.parametrize('one_char', nonalphanumeric)
    def test_update_buckets_name_single_char_nonalphanumeric_case(self, one_char):
        """
        TEST API: http://<gateway>/api/v2/buckets
        METHOD: PATCH
        tests bucket name containing single non-alphanumeric character can be updated and persisted in the etcd store.
        """
        self.run_tests('test_update_buckets_name_single_char_nonalphanumeric_case ', one_char, one_char, 3600,
                       one_char + '_updated', None)

    @pytest.mark.parametrize('ten_char_nonalphanumeric', ten_char_nonalphanumeric)
    def test_update_buckets_name_10_char_nonalphanumeric_case(self, ten_char_nonalphanumeric):
        """
        TEST API: http://<gateway>/api/v2/buckets
        METHOD: PATCH
        tests bucket name containing random 10 non-alphanumeric characters can be updated and persisted in the etcd store.
        """
        self.run_tests('test_update_buckets_name_10_char_nonalphanumeric_case ', ten_char_nonalphanumeric,
                       ten_char_nonalphanumeric, 3600, ten_char_nonalphanumeric + '_updated', None)

    @pytest.mark.parametrize('twenty_char_nonalphanumeric', twenty_char_nonalphanumeric)
    def test_update_buckets_name_20_char_nonalphanumeric_case(self, twenty_char_nonalphanumeric):
        """
        TEST API: http://<gateway>/api/v2/buckets
        METHOD: PATCH
        tests bucket name containing random 20 non-alphanumeric characters can be updated and persisted in the etcd store.
        """
        self.run_tests('test_update_buckets_name_20_char_nonalphanumeric_case ', twenty_char_nonalphanumeric,
                       twenty_char_nonalphanumeric, 3600, twenty_char_nonalphanumeric + '_updated', None)

    ####################################################
    #          Number Characters bucket Names          #
    ####################################################
    @pytest.mark.parametrize('one_char', digits)
    def test_update_buckets_name_single_char_numbers(self, one_char):
        """
        REST API: http://<gateway>/api/v2/buckets
        METHOD: PATCH
        tests bucket name containing single digits can be updated and persisted in the etcd store.
        """
        self.run_tests('test_update_buckets_name_single_char_numbers ', one_char, one_char, 3600,
                       one_char + '_updated', None)

    @pytest.mark.parametrize('ten_char_numbers', ten_char_numbers)
    def test_update_buckets_name_10_char_numbers(self, ten_char_numbers):
        """
        REST API: http://<gateway>/api/v2/buckets
        METHOD: PATCH
        tests bucket name containing random 10 digits can be updated and persisted in the etcd store.
        """
        self.run_tests('test_update_buckets_name_10_char_numbers ', ten_char_numbers, ten_char_numbers, 3600,
                       ten_char_numbers + '_updated', None)

    @pytest.mark.parametrize('five_char_numbers', five_char_numbers)
    def test_update_buckets_name_5_char_numbers(self, five_char_numbers):
        """
        REST API: http://<gateway>/api/v2/buckets
        METHOD: PATCH
        tests bucket name containing random 5 digits can be updated and persisted in the etcd store.
        """
        self.run_tests('test_update_buckets_name_5_char_numbers ', five_char_numbers, five_char_numbers, 3600,
                       five_char_numbers + '_updated', None)

    #######################################
    #     Mix Characters bucket Names     #
    #######################################
    @pytest.mark.parametrize('twenty_char_names', twenty_char_names_list)
    def test_update_buckets_name_20_char_mix(self, twenty_char_names):
        """
        REST API: http://<gateway>/api/v2/buckets
        METHOD: PATCH
        tests bucket name containing 20 mix characters can be updated and persisted in the etcd store.
        """
        self.run_tests('test_update_buckets_name_20_char_mix ', twenty_char_names, twenty_char_names, 3600,
                       twenty_char_names + '_updated', None)

    @pytest.mark.parametrize('forty_char_names', forty_char_names_list)
    def test_update_buckets_name_40_char_mix(self, forty_char_names):
        """
        REST API: http://<gateway>/api/v2/buckets
        METHOD: PATCH
        tests bucket name containing 40 mix characters can be updated and persisted in the etcd store.
        """
        self.run_tests('test_update_buckets_name_40_char_mix ', forty_char_names, forty_char_names, 3600,
                       forty_char_names + '_updated', None)

    @pytest.mark.parametrize('two_hundred_char_name', two_hundred_char_name_list)
    def test_update_buckets_name_200_char_mix(self, two_hundred_char_name):
        """
        REST API: http://<gateway>/api/v2/buckets
        METHOD: PATCH
        tests bucket name containing 200 mix characters can be updated and persisted in the etcd store.
        """
        self.run_tests('test_update_buckets_name_200_char_mix ', two_hundred_char_name, two_hundred_char_name, 3600,
                       two_hundred_char_name + '_updated', None)

    @pytest.mark.parametrize('four_hundred_char_name', four_hundred_char_name_list)
    def test_update_buckets_name_400_char_mix(self, four_hundred_char_name):
        """
        REST API: http://<gateway>/api/v2/buckets
        METHOD: PATCH
        tests bucket name containing 400 mix characters can be updated and persisted in the etcd store.
        """
        self.run_tests('test_update_buckets_name_400_char_mix ', four_hundred_char_name, four_hundred_char_name, 3600,
                       four_hundred_char_name + '_updated', None)

    @pytest.mark.onetest
    @pytest.mark.parametrize('special_char', special_char)
    def test_update_buckets_name_special_chars(self, special_char):
        """
        REST API: http://<gateway>/api/v2/buckets
        METHOD: PATCH
        tests buckets name containing special characters can be updated and persisted in the etcd store.
        """
        self.run_tests('test_update_buckets_name_special_chars ', special_char, special_char, 3600,
                       special_char + '_updated', None)

    def test_update_buckets_name_already_exist(self):
        """
        REST API: http://<gateway>/api/v2/buckets
        METHOD: PATCH
        tests buckets name can be updated and persisted in the etcd store if name already exists.
        """
        org_name = 'test_org_name_already_exists'
        bucket_name = 'test_bucket_name_already_exists'
        self.run_tests('test_update_buckets_name_already_exist', org_name, bucket_name, 3600, bucket_name, None)

    def test_update_buckets_to_empty_name(self):
        """
        REST API: http://<gateway>/api/v2/buckets
        METHOD: PATCH
        tests bucket name can not be updated and persisted in the etcd store if name is empty
        """
        org_name = 'test_org_name_empty_name'
        bucket_name = 'test_bucket_name'
        self.run_tests('test_update_buckets_to_empty_name', org_name, bucket_name, 3600, '', None)
