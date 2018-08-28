from string import ascii_lowercase
from string import ascii_uppercase
from string import digits

import pytest

import src.util.gateway_util as gateway_util
import src.util.login_util as lu
from src.chronograf.lib import chronograf_rest_lib as crl
from src.cloud.rest_api.conftest import ten_char_lc, twenty_char_lc, twenty_char_uc, ten_char_uc, \
    ten_char_numbers, five_char_numbers, nonalphanumeric, ten_char_nonalphanumeric, \
    twenty_char_nonalphanumeric, twenty_char_names_list, forty_char_names_list, \
    four_hundred_char_name_list, two_hundred_char_name_list, special_char, _assert, verify_org_etcd_entries


@pytest.mark.usefixtures('remove_orgs', 'gateway')
class TestUpdateOrganizationsAPI(object):
    """
    Test suite to test rest api endpoint for updating organizations
    removes created by tests organizations
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

    def run_tests(self, name_of_the_test_to_run, org_name):
        """
        :param name_of_the_test_to_run: test to run
        :param org_name:
        :return: pass/fail
        """
        test_name = name_of_the_test_to_run + org_name + ' '
        org_name_to_assert = ''
        if org_name == 'DoubleQuotes\\"':
            org_name_to_assert = 'DoubleQuotes"_updated_name'
        new_org_name = org_name + '_updated_name'
        self.header(test_name)

        self.mylog.info(test_name + ' STEP 1: Create Organization')
        status, created_org_id, created_org_name, error_message = \
            gateway_util.create_organization(self, self.gateway, org_name)
        if org_name == '':
            _assert(self, status, 201, 'status_code', xfail=True,
                    reason='https://github.com/influxdata/platform/issues/188')
        elif org_name == 'BackSlash\\':
            _assert(self, status, 201, 'status_code', xfail=True,
                    reason='https://github.com/influxdata/platform/issues/163')
        else:
            _assert(self, status, 201, 'status_code')

        self.mylog.info(test_name + ' STEP 2: Update created org with the \'%s\' name' % new_org_name)
        status, new_org_id, updated_org_name, error_message = \
            gateway_util.update_organization(self, self.gateway, created_org_id, new_org_name)
        self.mylog.info(test_name + 'Assert actual status \'%s\' equals to expected status 200' % status)
        _assert(self, status, 200, 'status_code')
        self.mylog.info(test_name + 'Assert actual org_id \'%s\' equals to expected org_id \'%s\''
                        % (new_org_id, created_org_id))
        _assert(self, new_org_id, created_org_id, 'org_id')
        if org_name == 'DoubleQuotes\\"':
            self.mylog.info(test_name + 'Assert actual org_name \'%s\' equals to expected org_name \'%s\''
                            % (updated_org_name, org_name_to_assert))
            _assert(self, updated_org_name, org_name_to_assert, 'org_name')
        else:
            self.mylog.info(test_name + 'Assert actual org_name \'%s\' equals to expected org_name \'%s\''
                            % (updated_org_name, new_org_name))
            _assert(self, updated_org_name, new_org_name, 'org_name')

        self.mylog.info(test_name + 'STEP 3: Verify updated name was persisted in the etcd store')
        verify_org_etcd_entries(self, test_name, created_org_id=new_org_id, created_org_name=updated_org_name, error='')
        self.footer(test_name)

    ############################################
    #       Lower Case Character Org Names     #
    ############################################
    @pytest.mark.parametrize('one_char', ascii_lowercase)
    def test_update_orgs_single_char_lower_case(self, one_char):
        """
        REST API: http://<gateway>/v1/orgs
        METHOD: PATCH
        tests org name containing single character lower case letters can be updated and persisted in the etcd store.
        """
        self.run_tests('test_update_orgs_single_char_lower_case ', one_char)

    @pytest.mark.parametrize('ten_char_lc', ten_char_lc)
    def test_update_orgs_10_char_lower_case(self, ten_char_lc):
        """
        TEST API: http://<gateway>/v1/orgs
        METHOD: PATCH
        tests org name containing random 10 lower case letters can be updated and persisted in the etcd store.
        """
        self.run_tests('test_update_orgs_10_char_lower_case ', ten_char_lc)

    @pytest.mark.parametrize('twenty_char_lc', twenty_char_lc)
    def test_update_orgs_20_char_lower_case(self, twenty_char_lc):
        """
        TEST API: http://<gateway>/v1/orgs
        METHOD: PATCH
        tests org name containing random 20 lower case letters can be updated and persisted in the etcd store.
        """
        self.run_tests('test_update_orgs_20_char_lower_case ', twenty_char_lc)

    ###################################################
    #          Upper Case Character Org Names         #
    ###################################################
    @pytest.mark.parametrize('one_char', ascii_uppercase)
    def test_update_orgs_single_char_upper_case(self, one_char):
        """
        TEST API: http://<gateway>/v1/orgs
        METHOD: PATCH
        tests org name containing single upper case letters can be updated and persisted in the etcd store.
        """
        self.run_tests('test_update_orgs_single_char_upper_case ', one_char)

    @pytest.mark.parametrize('ten_char_uc', ten_char_uc)
    def test_update_orgs_10_char_upper_case(self, ten_char_uc):
        """
        TEST API: http://<gateway>/v1/orgs
        METHOD: PATCH
        tests org name containing random 10 upper case letters can be updated and persisted in the etcd store.
        """
        self.run_tests('test_update_orgs_10_char_upper_case ', ten_char_uc)

    @pytest.mark.parametrize('twenty_char_uc', twenty_char_uc)
    def test_update_orgs_20_char_upper_case(self, twenty_char_uc):
        """
        TEST API: http://<gateway>/v1/orgs
        METHOD: PATCH
        tests org name containing random 20 upper case letters can be updated and persisted in the etcd store.
        """
        self.run_tests('test_update_orgs_20_char_upper_case ', twenty_char_uc)

    #########################################################
    #          Non-alphanumeric Character Org Names         #
    #########################################################
    @pytest.mark.parametrize('one_char', nonalphanumeric)
    def test_update_orgs_single_char_nonalphanumeric_case(self, one_char):
        """
        TEST API: http://<gateway>/v1/orgs
        METHOD: PATCH
        tests org name containing single non-alphanumeric character can be updated and persisted in the etcd store.
        """
        self.run_tests('test_update_orgs_single_char_nonalphanumeric_case ', one_char)

    @pytest.mark.parametrize('ten_char_nonalphanumeric', ten_char_nonalphanumeric)
    def test_update_orgs_10_char_nonalphanumeric_case(self, ten_char_nonalphanumeric):
        """
        TEST API: http://<gateway>/v1/orgs
        METHOD: PATCH
        tests org name containing random 10 non-alphanumeric characters can be updated and persisted in the etcd store.
        """
        self.run_tests('test_update_orgs_10_char_nonalphanumeric_case ', ten_char_nonalphanumeric)

    @pytest.mark.parametrize('twenty_char_nonalphanumeric', twenty_char_nonalphanumeric)
    def test_update_orgs_20_char_nonalphanumeric_case(self, twenty_char_nonalphanumeric):
        """
        TEST API: http://<gateway>/v1/orgs
        METHOD: PATCH
        tests org name containing random 20 non-alphanumeric characters can be updated and persisted in the etcd store.
        """
        self.run_tests('test_update_orgs_20_char_nonalphanumeric_case ', twenty_char_nonalphanumeric)

    #################################################
    #          Number Characters Org Names          #
    #################################################
    @pytest.mark.parametrize('one_char', digits)
    def test_update_orgs_single_char_numbers(self, one_char):
        """
        REST API: http://<gateway>/v1/orgs
        METHOD: PATCH
        tests org name containing single digits can be updated and persisted in the etcd store.
        """
        self.run_tests('test_update_orgs_single_char_numbers ', one_char)

    @pytest.mark.parametrize('ten_char_numbers', ten_char_numbers)
    def test_update_orgs_10_char_numbers(self, ten_char_numbers):
        """
        REST API: http://<gateway>/v1/orgs
        METHOD: PATCH
        tests org name containing random 10 digits can be updated and persisted in the etcd store.
        """
        self.run_tests('test_update_orgs_10_char_numbers ', ten_char_numbers)

    @pytest.mark.parametrize('five_char_numbers', five_char_numbers)
    def test_update_orgs_5_char_numbers(self, five_char_numbers):
        """
        REST API: http://<gateway>/v1/orgs
        METHOD: PATCH
        tests org name containing random 5 digits can be updated and persisted in the etcd store.
        """
        self.run_tests('test_update_orgs_5_char_numbers ', five_char_numbers)

    ####################################
    #     Mix Characters Org Names     #
    ####################################
    @pytest.mark.parametrize('twenty_char_names', twenty_char_names_list)
    def test_update_orgs_20_char_mix(self, twenty_char_names):
        """
        REST API: http://<gateway>/v1/orgs
        METHOD: PATCH
        tests org name containing 20 mix characters can be updated and persisted in the etcd store.
        """
        self.run_tests('test_update_orgs_20_char_mix ', twenty_char_names)

    @pytest.mark.parametrize('forty_char_names', forty_char_names_list)
    def test_update_orgs_40_char_mix(self, forty_char_names):
        """
        REST API: http://<gateway>/v1/orgs
        METHOD: PATCH
        tests org name containing 40 mix characters can be updated and persisted in the etcd store.
        """
        self.run_tests('test_update_orgs_40_char_mix ', forty_char_names)

    @pytest.mark.parametrize('two_hundred_char_name', two_hundred_char_name_list)
    def test_update_orgs_200_char_mix(self, two_hundred_char_name):
        """
        REST API: http://<gateway>/v1/orgs
        METHOD: PATCH
        tests org name containing 200 mix characters can be updated and persisted in the etcd store.
        """
        self.run_tests('test_update_orgs_200_char_mix ', two_hundred_char_name)

    @pytest.mark.parametrize('four_hundred_char_name', four_hundred_char_name_list)
    def test_update_orgs_400_char_mix(self, four_hundred_char_name):
        """
        REST API: http://<gateway>/v1/orgs
        METHOD: PATCH
        tests org name containing 400 mix characters can be updated and persisted in the etcd store.
        """
        self.run_tests('test_update_orgs_400_char_mix ', four_hundred_char_name)

    @pytest.mark.parametrize('special_char', special_char)
    def test_update_orgs_special_chars(self, special_char):
        """
        REST API: http://<gateway>/v1/orgs
        METHOD: PATCH
        tests orgs name containing special characters can be updated and persisted in the etcd store.
        """
        self.run_tests('test_update_orgs_special_chars ', special_char)

    def test_update_orgs_already_exist(self):
        """
        REST API: http://<gateway>/v1/users
        METHOD: PATCH
        tests org name can be updated and persisted in the etcd store if name already exists.
        """
        test_name = 'test_update_org`_already_exist'
        org_name = 'existing_org'
        self.header(test_name)
        self.mylog.info(test_name + ' STEP 1: Create Organization')
        status, created_org_id, created_org_name, error_message = \
            gateway_util.create_organization(self, self.gateway, org_name)
        self.mylog.info(test_name + 'Assert actual status code \'%s\' equals to expected status code 201' % status)
        _assert(self, status, 201, 'status_code')

        self.mylog.info(test_name + ' STEP 2: Update created org with the \'%s\' name' % org_name)
        status, updated_org_id, updated_org_name, error_message = \
            gateway_util.update_organization(self, self.gateway, created_org_id, org_name)
        self.mylog.info(test_name + 'Assert actual status code \'%s\' equals to expected status code 201' % status)
        _assert(self, status, 200, 'status_code')
        self.mylog.info(test_name + 'Assert updated org_id \'%s\' equals to expected org_id \'%s\''
                        % (updated_org_id, created_org_id))
        _assert(self, updated_org_id, created_org_id, 'org_id')
        self.mylog.info(test_name + 'Assert updated org_name \'%s\' equals to expected org_name \'%s\'' % (updated_org_name, org_name))
        _assert(self, updated_org_name, org_name, 'org_name')

        self.mylog.info(test_name + 'STEP 3: Verify created user was persisted in the etcd store')
        verify_org_etcd_entries(self, test_name, updated_org_id, updated_org_name, '')
        self.footer(test_name)

    def test_update_orgs_empty_name(self):
        """
        REST API: http://<gateway>/v1/orgs
        METHOD: PATCH
        tests org name can be updated and persisted in the etcd store if name is empty
        """
        test_name = 'test_update_orgs_empty_name'
        org_name = 'org_to_be_updated'
        org_name_to_update = ''
        self.header(test_name)
        self.mylog.info(test_name + ' STEP 1: Create Organization')
        status, created_org_id, created_org_name, error_message = \
            gateway_util.create_organization(self, self.gateway, org_name)
        self.mylog.info(test_name + 'Assert actual status code \'%s\' equals to expected status code 201' % status)
        _assert(self, status, 201, 'status_code')

        self.mylog.info(test_name + 'STEP 2: Verify created organization was persisted in the etcd store')
        verify_org_etcd_entries(self, test_name, created_org_id, created_org_name, error='')

        self.mylog.info(test_name + ' STEP 3: Update created org with the \'%s\' name' % org_name_to_update)
        status, updated_org_id, updated_org_name, error_message = \
            gateway_util.update_organization(self, self.gateway, created_org_id, org_name_to_update)
        self.mylog.info(test_name + 'Assert actual status code \'%s\' equals to expected status code 200' % status)
        _assert(self, status, 200, 'status_code')
        self.mylog.info(test_name + 'Assert updated org_id \'%s\' equals to expected org_id \'%s\''
                        % (updated_org_id, created_org_id))
        _assert(self, updated_org_id, created_org_id, 'org_id')
        self.mylog.info(test_name + 'Assert updated org_name \'%s\' equals to expected org_name \'%s\''
                        % (updated_org_name, ''))
        _assert(self, updated_org_name, '', 'org_name')
        self.footer(test_name)
