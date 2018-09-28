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
    four_hundred_char_name_list, two_hundred_char_name_list, special_char, _assert, verify_user_etcd_entries


@pytest.mark.usefixtures('remove_users', 'gateway')
class TestUpdateUsersAPI(object):
    """
    Test suite to test rest api endpoint for updating users
    removes created by tests users
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

    def run_tests(self, name_of_the_test_to_run, user_name):
        """
        :param name_of_the_test_to_run: name of the test to be run
        :param user_name: name of user under the test
        :return: pass/fail
        """
        test_name = name_of_the_test_to_run + user_name + ' '
        new_name_to_assert = ''
        if user_name == 'DoubleQuotes\\"':
            new_name_to_assert = 'DoubleQuotes"_updated_name'
        new_name = user_name + '_updated_name'
        self.header(test_name)
        self.mylog.info(test_name + ' STEP 1: Create User \'%s\'' % user_name)
        status, created_user_id, created_user_name, error_message = \
            gateway_util.create_user(self, self.gateway, user_name)
        if user_name == '':
            _assert(self, status, 201, 'status code', xfail=True,
                    reason='https://github.com/influxdata/platform/issues/162')
        elif user_name == 'BackSlash\\':
            _assert(self, status, 201, 'status code', xfail=True,
                    reason='https://github.com/influxdata/platform/issues/163')
        else:
            _assert(self, status, 201, 'status code')

        self.mylog.info(test_name + 'STEP 2: Verify data was persisted in the etcd store')
        verify_user_etcd_entries(self, test_name, created_user_id, created_user_name, expected_error='')

        self.mylog.info(test_name + ' STEP 3: Update created user with the \'%s\' name' % new_name)
        status, new_user_id, updated_user_name, error_message = \
            gateway_util.update_user(self, self.gateway, created_user_id, new_name)
        self.mylog.info(test_name + 'Assert actual status \'%s\' equals to expected status \'%s\'' % (status, 200))
        _assert(self, status, 200, 'status code')
        self.mylog.info(test_name + 'Assert updated user_id \'%s\' equals to expected user_id \'%s\''
                        % (new_user_id, created_user_id))
        _assert(self, new_user_id, created_user_id, 'user id')
        if user_name == 'DoubleQuotes\\"':
            self.mylog.info(test_name + 'Assert updated user_name \'%s\' equals to expected user_name \'%s\''
                            % (updated_user_name, new_name_to_assert))
            _assert(self, updated_user_name, new_name_to_assert, 'user name')
        else:
            self.mylog.info(test_name + 'Assert updated user_name \'%s\' equals to expected user_name \'%s\''
                            % (updated_user_name, new_name))
            _assert(self, updated_user_name, new_name, 'user name')

        self.mylog.info(test_name + 'STEP 4: Verify updated name was persisted in the etcd store')
        verify_user_etcd_entries(self, test_name, new_user_id, updated_user_name, expected_error='')
        self.footer(test_name)

    ############################################
    #       Lower Case Character User Names    #
    ############################################
    @pytest.mark.parametrize('one_char', ascii_lowercase)
    def test_update_users_single_char_lower_case(self, one_char):
        """
        REST API: http://<gateway>/api/v2/users
        METHOD: PATCH
        tests user name containing single character lower case letters can be updated and persisted in the etcd store.
        """
        self.run_tests('test_update_users_single_char_lower_case_', one_char)

    @pytest.mark.parametrize('ten_char', ten_char_lc)
    def test_update_users_10_char_lower_case(self, ten_char):
        """
        REST API: http://<gateway>/api/v2/users
        METHOD: PATCH
        tests user name containing 10 random characters lower case letters can be updated and persisted in the etcd store.
        """
        self.run_tests('test_update_users_10_char_lower_case_', ten_char)

    @pytest.mark.parametrize('twenty_char', twenty_char_lc)
    def test_update_users_20_char_lower_case(self, twenty_char):
        """
        REST API: http://<gateway>/api/v2/users
        METHOD: PATCH
        tests user name containing 20 random characters lower case letters can be updated and persisted in the etcd store.
        """
        self.run_tests('test_update_users_20_char_lower_case_', twenty_char)

    ###################################################
    #          Upper Case Character User Names        #
    ###################################################
    @pytest.mark.parametrize('one_char', ascii_uppercase)
    def test_update_users_single_char_upper_case(self, one_char):
        """
        REST API: http://<gateway>/api/v2/users
        METHOD: PATCH
        tests user name containing single upper case character letters can be updated and persisted in the etcd store.
        """
        self.run_tests('test_update_users_single_char_upper_case_', one_char)

    @pytest.mark.parametrize('ten_char', ten_char_uc)
    def test_update_users_10_char_upper_case(self, ten_char):
        """
        REST API: http://<gateway>/api/v2/users
        METHOD: PATCH
        tests user name containing 10 random upper case character letters can be updated and persisted in the etcd store.
        """
        self.run_tests('test_update_users_10_char_upper_case_', ten_char)

    @pytest.mark.parametrize('twenty_char', twenty_char_uc)
    def test_update_users_20_char_upper_case(self, twenty_char):
        """
        REST API: http://<gateway>/api/v2/users
        METHOD: PATCH
        tests user name containing 20 random upper case character letters can be updated and persisted in the etcd store.
        """
        self.run_tests('test_update_users_20_char_upper_case_', twenty_char)

    #########################################################
    #          Non-alphanumeric Character User Names        #
    #########################################################
    @pytest.mark.parametrize('one_char', nonalphanumeric)
    def test_update_users_single_char_nonalphanumeric(self, one_char):
        """
        REST API: http://<gateway>/api/v2/users
        METHOD: PATCH
        tests user name containing non-alphanumeric character letters can be updated and persisted in the etcd store.
        """
        self.run_tests('test_update_users_single_char_nonalphanumeric_', one_char)

    @pytest.mark.parametrize('ten_char_nonalphanumeric', ten_char_nonalphanumeric)
    def test_update_users_10_char_nonalphanumeric(self, ten_char_nonalphanumeric):
        """
        REST API: http://<gateway>/api/v2/users
        METHOD: PATCH
        tests user name containing 10 random non-alphanumeric character letters can be updated and persisted in the etcd store.
        """
        self.run_tests('test_update_users_10_char_nonalphanumeric_', ten_char_nonalphanumeric)

    @pytest.mark.parametrize('twenty_char_nonalphanumeric', twenty_char_nonalphanumeric)
    def test_update_orgs_20_char_nonalphanumeric_case(self, twenty_char_nonalphanumeric):
        """
        REST API: http://<gateway>/api/v2/users
        METHOD: PATCH
        tests user name containing 20 random non-alphanumeric character letters can be updated and persisted in the etcd store.
        """
        self.run_tests('twenty_char_nonalphanumeric_', twenty_char_nonalphanumeric)

    #################################################
    #          Number Characters User Names         #
    #################################################
    @pytest.mark.parametrize('one_char', digits)
    def test_update_users_single_char_numbers(self, one_char):
        """
        REST API: http://<gateway>/api/v2/users
        METHOD: PATCH
        tests user name containing single digits can be updated and persisted in the etcd store.
        """
        self.run_tests('test_update_users_single_char_numbers_', one_char)

    @pytest.mark.parametrize('ten_char_numbers', ten_char_numbers)
    def test_update_users_10_char_numbers(self, ten_char_numbers):
        """
        REST API: http://<gateway>/api/v2/users
        METHOD: PATCH
        tests user name containing 10 random digits can be updated and persisted in the etcd store.
        """
        self.run_tests('test_update_users_10_char_numbers_', ten_char_numbers)

    @pytest.mark.parametrize('five_numbers', five_char_numbers)
    def test_update_users_5_char_numbers(self, five_numbers):
        """
        REST API: http://<gateway>/api/v2/users
        METHOD: PATCH
        tests user name containing 5 random digits can be updated and persisted in the etcd store.
        """
        self.run_tests('test_update_users_5_char_numbers_', five_numbers)

    ####################################
    #     Mix Characters User Names    #
    ####################################
    @pytest.mark.parametrize('twenty_char_names', twenty_char_names_list)
    def test_update_users_20_char_mix(self, twenty_char_names):
        """
        REST API: http://<gateway>/api/v2/users
        METHOD: PATCH
        tests user name containing 20 mix characters can be updated and persisted in the etcd store.
        """
        self.run_tests('test_update_users_20_char_mix_', twenty_char_names)

    @pytest.mark.parametrize('forty_char_names', forty_char_names_list)
    def test_update_users_40_char_mix(self, forty_char_names):
        """
        REST API: http://<gateway>/api/v2/users
        METHOD: PATCH
        tests user name containing 40 mix characters can be updated and persisted in the etcd store.
        """
        self.run_tests('test_update_users_40_char_mix_', forty_char_names)

    @pytest.mark.parametrize('two_hundred_char_names', two_hundred_char_name_list)
    def test_update_users_200_char_mix(self, two_hundred_char_names):
        """
        REST API: http://<gateway>/api/v2/users
        METHOD: PATCH
        tests user name containing 200 mix characters can be updated and persisted in the etcd store.
        """
        self.run_tests('test_update_users_200_char_mix_', two_hundred_char_names)

    @pytest.mark.parametrize('four_hundred_char_names', four_hundred_char_name_list)
    def test_update_users_400_char_mix(self, four_hundred_char_names):
        """
        REST API: http://<gateway>/api/v2/users
        METHOD: PATCH
        tests user name containing 400 mix characters can be updated and persisted in the etcd store.
        """
        self.run_tests('test_update_users_400_char_mix_', four_hundred_char_names)

    @pytest.mark.parametrize('special_char', special_char)
    def test_update_users_special_chars(self, special_char):
        """
        REST API: http://<gateway>/api/v2/users
        METHOD: PATCH
        tests user name containing special characters can be updated and persisted in the etcd store.
        """
        self.run_tests('test_update_users_special_chars_', special_char)

    def test_update_users_already_exist(self):
        """
        REST API: http://<gateway>/api/v2/users
        METHOD: PATCH
        tests user name can be updated and persisted in the etcd store if name already exists.
        """
        test_name = 'test_update_users_already_exist'
        user_name = 'existing_user'
        self.header(test_name)
        self.mylog.info(test_name + ' STEP 1: Create User')
        status, created_user_id, created_user_name, error_message = \
            gateway_util.create_user(self, self.gateway, user_name)
        self.mylog.info(test_name + 'Assert actual status \'%s\' equals to expected status \'%s\'' % (status, 201))
        _assert(self, status, 201, 'status code')

        self.mylog.info(test_name + 'STEP 2: Verify data was persisted in the etcd store')
        verify_user_etcd_entries(self, test_name, created_user_id, created_user_name, expected_error='')

        self.mylog.info(test_name + ' STEP 3: Update created user with the \'%s\' name' % user_name)
        status, updated_user_id, updated_user_name, error_message = \
            gateway_util.update_user(self, self.gateway, created_user_id, user_name)
        self.mylog.info(test_name + 'Assert actual status \'%s\' equals to expected status \'%s\'' % (status, 200))
        _assert(self, status, 200, 'status code')
        self.mylog.info(test_name + 'Assert updated user_id \'%s\' equals to expected user_id \'%s\''
                        % (updated_user_id, created_user_id))
        _assert(self, updated_user_id, created_user_id, 'user id')
        self.mylog.info(test_name + 'Assert updated user_name \'%s\' equals to expected user_name \'%s\''
                        % (updated_user_name, user_name))
        _assert(self, updated_user_name, user_name, 'user name')

        self.mylog.info(test_name + 'STEP 4: Verify data was persisted in the etcd store')
        verify_user_etcd_entries(self, test_name, updated_user_id, updated_user_name, expected_error='')
        self.footer(test_name)

    def test_update_users_empty_name(self):
        """
        REST API: http://<gateway>/api/v2/users
        METHOD: PATCH
        tests user name can be updated and persisted in the etcd store if name is empty
        """
        test_name = 'test_update_users_empy_name'
        user_name = 'user_to_be_updated'
        user_name_to_update = ''
        self.header(test_name)
        self.mylog.info(test_name + ' STEP 1: Create User \'%s\'' % user_name)
        status, created_user_id, created_user_name, error_message = \
            gateway_util.create_user(self, self.gateway, user_name)
        self.mylog.info(test_name + 'Assert actual status \'%s\' equals to expected status \'%s\'' % (status, 201))
        _assert(self, status, 201, 'status code')

        self.mylog.info(test_name + 'STEP 2: Verify data was persisted in the etcd store')
        verify_user_etcd_entries(self, test_name, created_user_id, created_user_name, expected_error='')

        self.mylog.info(test_name + ' STEP 3: Update created user with the \'%s\' name' % user_name_to_update)
        status, updated_user_id, updated_user_name, error_message = \
            gateway_util.update_user(self, self.gateway, created_user_id, user_name_to_update)
        self.mylog.info(test_name + 'Assert actual status \'%s\' equals to expected status \'%s\'' % (status, 200))
        _assert(self, status, 200, 'status code')
        self.mylog.info(test_name + 'Assert updated user_id \'%s\' equals to expected user_id \'%s\''
                        % (updated_user_id, created_user_id))
        _assert(self, updated_user_id, created_user_id, 'user id')
        self.mylog.info(test_name + 'Assert updated user_name \'%s\' equals to expected user_name \'%s\''
                       % (updated_user_name, user_name_to_update))
        _assert(self, updated_user_name, user_name_to_update, 'user name')

        self.mylog.info(test_name + 'STEP 4: Verify data was persisted in the etcd store')
        verify_user_etcd_entries(self, test_name, updated_user_id, updated_user_name, expected_error='')
        self.footer(test_name)
