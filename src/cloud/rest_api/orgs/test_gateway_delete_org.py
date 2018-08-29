from random import choice
from string import ascii_lowercase
from string import ascii_uppercase
from string import digits

import pytest

import src.util.login_util as lu
from src.chronograf.lib import chronograf_rest_lib as crl
from src.cloud.rest_api.conftest import nonalphanumeric, twenty_char_names_list, four_hundred_char_name_list, _assert, \
    verify_org_etcd_entries, verify_bucket_etcd_entries
from src.util import gateway_util


@pytest.mark.usefixtures('remove_orgs', 'gateway')
class TestDeleteOrganizationsAPI(object):
    """
    Test Suite for testing REST API endpoint to delete organizations.
    - The existing orgs would be removed before running tests.
    - The existing buckets would be removed before running tests
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

    def run_tests(self, name_of_the_test_to_run, org_name=None, expected_error='', org_id=None, bucket_name=None,
                  number_of_buckets=1):
        """
        Helper function to run organization deletion tests
        :param name_of_the_test_to_run (str): name of the test
        :param org_name (str): name of the organization
        :param expected_error (str): expected error returned by delete org rest api,  default: empty string
        :param org_id (str): id of the organization, default: None
        :param bucket_name (str): name of the bucket to be created, default: None
        :param number_of_buckets (int): how many buckets to create, default: 1
        :return: Pass/Fail
        """
        bucket_info = {}
        if org_name == '':
            test_name = name_of_the_test_to_run + 'empty org name '
        elif org_name is None:
            test_name = name_of_the_test_to_run
        else:
            test_name = name_of_the_test_to_run + org_name + ' '
        self.header(test_name)
        if org_id is None:
            self.mylog.info('')
            self.mylog.info(test_name + ' STEP 1: Create Organization "%s"' % org_name)
            self.mylog.info('')
            status, created_org_id, created_org_name, error_message = \
                gateway_util.create_organization(self, self.gateway, org_name)
            # TODO according to @goller the name of the org can be an empty string, but currently it returns an error.
            # TODO issues/162 is an old one - update when new issue is filed.
            if org_name == '':
                _assert(self, status, 201, 'status code', xfail=True,
                        reason='https://github.com/influxdata/platform/issues/162')
            elif org_name == 'BackSlash\\':
                _assert(self, status, 201, 'status code', xfail=True,
                        reason='https://github.com/influxdata/platform/issues/163')
            else:
                _assert(self, status, 201, 'status code')
            if bucket_name:
                self.mylog.info('')
                self.mylog.info(test_name + 'STEP 2: Create Bucket "%s"' % bucket_name)
                self.mylog.info('')
                for bucket_num in range(number_of_buckets):
                    name_of_the_bucket = bucket_name + '_' + str(bucket_num)
                    self.mylog.info('')
                    self.mylog.info(test_name + 'STEP 2.1: Create Bucket "%s"' % name_of_the_bucket)
                    self.mylog.info('')
                    status, created_bucket_id, created_bucket_name, organization_id, retention_period, error_message = \
                        gateway_util.create_bucket(self, self.gateway, name_of_the_bucket, retentionPeriod=None,
                                                   organizationID=created_org_id)
                    _assert(self, status, 201, 'status code')
                    _assert(self, created_bucket_name, name_of_the_bucket, 'bucket_name')
                    _assert(self, retention_period, 0, 'retention period')
                    _assert(self, error_message, '', 'error message')
                    bucket_info[created_bucket_id] = created_bucket_name
                self.mylog.info('')
                self.mylog.info(test_name + ' STEP 3: Delete Organization with \'%s\' id' % created_org_id)
                self.mylog.info('')
                status, error = gateway_util.delete_organization(self, self.gateway, created_org_id)
                _assert(self, status, 202, 'status code')
                _assert(self, error, '', 'expected error')
                self.mylog.info('')
                self.mylog.info(test_name + ' STEP 4: Verify all of the org data is removed from etcd store')
                self.mylog.info('')
                verify_org_etcd_entries(self, test_name, created_org_id='', created_org_name='', error='',
                                        get_index_values=True, name_by_index_id='', error_by_index_id='',
                                        id_by_index_name='', error_by_index_name='')
                self.mylog.info('')
                self.mylog.info(test_name + ' STEP 5: Verify bucket data is preseved in the etcd store')
                self.mylog.info('')
                for id in bucket_info.keys():
                    verify_bucket_etcd_entries(self, test_name, id, bucket_info[id], 0, '')
                    self.mylog.info('')
                    self.mylog.info(test_name + ' STEP 6: Verify bucket is not in the list of all buckets')
                    self.mylog.info('')
                    status, list_of_buckets = gateway_util.get_all_buckets(self, self.gateway)
                    _assert(self, status, 200, 'status_code')
                    status = gateway_util.find_bucket_by_name(self, list_of_buckets, bucket_info[id], org_name)
                    _assert(self, status, False, 'find bucket by name')
            else:
                self.mylog.info('')
                self.mylog.info(test_name + ' STEP 2: Delete Organization with \'%s\' id' % created_org_id)
                self.mylog.info('')
                status, error = gateway_util.delete_organization(self, self.gateway, created_org_id)
                _assert(self, status, 202, 'status code')
                _assert(self, error, '', 'expected error')
                self.mylog.info('')
                self.mylog.info(test_name + ' STEP 3: Verify all of the org data is removed from etcd store')
                self.mylog.info('')
                verify_org_etcd_entries(self, test_name, created_org_id='', created_org_name='', error='',
                                        get_index_values=True, name_by_index_id='', error_by_index_id='',
                                        id_by_index_name='', error_by_index_name='')
        # Do not create Organization, this is just to pass an org_id to the delete API
        else:
            self.mylog.info('')
            self.mylog.info(test_name + ' STEP 1: Delete Organization with \'%s\' id' % org_id)
            self.mylog.info('')
            status, error = gateway_util.delete_organization(self, self.gateway, org_id)
            # TODO to change status to the one other then current 500, when it is fixed.
            if org_id == '':
                _assert(self, status, 404, 'status code')
            else:
                _assert(self, status, 500, 'status code')
            _assert(self, error, expected_error, 'expected error')
        self.footer(test_name)

    # =============== DELETE EMPTY ORG ==============

    def test_delete_org_id_odd_length(self):
        """
        REST API: http://<gateway>/v1/orgs/aff
        METHOD: DELETE
        tests API will return an error if org_id has an odd length
        """
        self.run_tests('test_delete_org_id_odd_length ',
                       expected_error='encoding/hex: odd length hex string', org_id='aff')

    def test_delete_org_id_invalid_byte(self):
        """
        REST API: http://<gateway>/v1/orgs/aff
        METHOD: DELETE
        tests API will return an error if org_id has an invalid byte
        """
        self.run_tests('test_delete_org_id_invalid_byte ',
                       expected_error='encoding/hex: invalid byte: U+0073 \'s\'', org_id='assdff')

    def test_delete_org_id_does_not_exist(self):
        """
        REST API: http://<gateway>/v1/orgs/1234567890
        METHOD: DELETE
        tests API will return an error if org_id does not exist in etcd store, but is valid
        """
        self.run_tests('test_delete_org_id_does_not_exist ',
                       expected_error='organization not found', org_id='1234567890')

    def test_delete_org_id_missing(self):
        """
        REST API: http://<gateway>/v1/orgs/
        METHOD: DELETE
        tests API will return an error if org_id is missing
        """
        self.run_tests('test_delete_org_id_missing ', expected_error='', org_id='')

    @pytest.mark.parametrize('single_char', [choice(ascii_lowercase), choice(ascii_uppercase), choice(digits),
                                             choice(nonalphanumeric)])
    def test_delete_empty_org_single_char_name(self, single_char):
        """
        REST API: http://<gateway>/v1/orgs/<org_id>
        METHOD: DELETE
        tests API will successfully remove organization records from etcd store
        """
        self.run_tests('test_delete_empty_org_single_char_name ', org_name=single_char)

    @pytest.mark.parametrize('twenty_mix_chars', twenty_char_names_list)
    def test_delete_empty_org_20_mix_char_name(self, twenty_mix_chars):
        """
        REST API: http://<gateway>/v1/orgs/<org_id>
        METHOD: DELETE
        tests API will successfully remove organization records from etcd store when org name is 20 characters long
        """
        self.run_tests('test_delete_empty_org_20_mix_char_name ', org_name=twenty_mix_chars)

    @pytest.mark.parametrize('four_hundred_char_names', four_hundred_char_name_list)
    def test_delete_empty_org_400_mix_char_name(self, four_hundred_char_names):
        """
        REST API: http://<gateway>/v1/orgs/<org_id>
        METHOD: DELETE
        tests API will successfully remove organization records from etcd store when org name is 400 characters long
        """
        self.run_tests('test_delete_empty_org_400_mix_char_name ', org_name=four_hundred_char_names)

    # =============== DELETE ORG WITH BUCKETS ===============

    def test_delete_org_one_empty_bucket(self):
        """
        REST API: http://<gateway>/v1/orgs/aff
        METHOD: DELETE
        tests org is deleted and bucket's data is preserved.
        1. Create Organization.
        2. Verify Organization data is in etcd store.
        3. Create Bucket that belongs to the created above organization.
        4. Verify Bucket data is in etcd store.
        5. Delete Organization.
        6. Verify organization data completely removed from etcd store.
        7. Verify bucket data is preserved in etcd strore
        8. Verify accessing the bucket for the removed org does not return an error.
        """
        self.run_tests('test_delete_org_one_empty_bucket ', org_name='test_delete_org_one_empty_bucket',
                       expected_error='', org_id=None, bucket_name='test_delete_org_one_empty_bucket')

    def test_delete_org_five_empty_buckets(self):
        """
        REST API: http://<gateway>/v1/orgs/aff
        METHOD: DELETE
        tests org is deleted and bucket's data is preserved.
        1. Create Organization.
        2. Verify Organization data is in etcd store.
        3. Create 5 Buckets that belong to the created above organization.
        4. Verify Buckets data is in etcd store.
        5. Delete Organization.
        6. Verify organization data completely removed from etcd store.
        7. Verify buckets data is preserved in etcd strore
        8. Verify accessing the buckets for the removed org does not return an error.
        """
        self.run_tests('test_delete_org_five_empty_buckets ', org_name='test_delete_org_five_empty_buckets',
                       expected_error='', org_id=None, bucket_name='test_delete_org_five_empty_buckets',
                       number_of_buckets=5)