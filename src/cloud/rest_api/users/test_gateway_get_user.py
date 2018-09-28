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
class TestGetUsersAPI(object):
    """
    Test Suite for testing REST API endpoint for getting single user by id
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

    def run_tests(self, name_of_the_test, user_name):
        """
        :param name_of_the_test: name of the test to run
        :param user_name: user name to get
        :return: pass/fail
        """
        test_name = name_of_the_test + user_name + ' '
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

        self.mylog.info(test_name + ' STEP 3: Get Created User')
        status, actual_user_id, actual_user_name, error_message = \
            gateway_util.get_user_by_id(self, self.gateway, created_user_id)
        self.mylog.info(test_name + 'Assert actual status \'%s\' equals to expected status \'%s\'' % (status, 200))
        _assert(self, status, 200, 'status code')
        self.mylog.info(test_name + 'Assert actual user_id \'%s\' equals expected user_id \'%s\''
                        % (actual_user_id, created_user_id))
        _assert(self, actual_user_id, created_user_id, 'user id')
        self.mylog.info(test_name + 'Assert actual user_name \'%s\' equals expected user_name \'%s\''
                        % (actual_user_name, created_user_name))
        _assert(self, actual_user_name, created_user_name, 'user name')
        self.footer(test_name)

    ############################################
    #   Lower Case Character Get User Name     #
    ############################################
    @pytest.mark.parametrize('one_char', ascii_lowercase)
    def test_get_users_single_char_lower_case(self, one_char):
        """
        REST API: http://<gateway>/api/v2/users
        METHOD: GET
        tests created user using single lower case characters can be returned by using get user by id endpoint.
        """
        self.run_tests('test_get_users_single_char_lower_case_', one_char)

    @pytest.mark.parametrize('ten_char_lc', ten_char_lc)
    def test_get_users_10_char_lower_case(self, ten_char_lc):
        """
        REST API: http://<gateway>/api/v2/users
        METHOD: GET
        tests created user using 10 random lower case characters can be returned by using get user by id endpoint.
        """
        self.run_tests('test_get_users_10_char_lower_case_', ten_char_lc)

    @pytest.mark.parametrize('twenty_char_lc', twenty_char_lc)
    def test_get_users_20_char_lower_case(self, twenty_char_lc):
        """
        REST API: http://<gateway>/api/v2/users
        METHOD: GET
        tests created user using 20 random lower case characters can be returned by using get user by id endpoint.
        """
        self.run_tests('test_get_users_20_char_lower_case_', twenty_char_lc)

    ###################################################
    #     Upper Case Character Get User Name          #
    ###################################################
    @pytest.mark.parametrize('one_char', ascii_uppercase)
    def test_get_users_single_char_upper_case(self, one_char):
        """
        REST API: http://<gateway>/api/v2/users
        METHOD: GET
        tests created user using single upper case characters can be returned by using get user by id endpoint.
        """
        self.run_tests('test_get_users_single_char_upper_case_', one_char)

    @pytest.mark.parametrize('ten_char_uc', ten_char_uc)
    def test_get_users_10_char_upper_case(self, ten_char_uc):
        """
        REST API: http://<gateway>/api/v2/users
        METHOD: GET
        tests created user using 10 random upper case characters can be returned by using get user by id endpoint.
        """
        self.run_tests('est_get_users_10_char_upper_case_', ten_char_uc)

    @pytest.mark.parametrize('twenty_char_uc', twenty_char_uc)
    def test_get_users_20_char_upper_case(self, twenty_char_uc):
        """
        REST API: http://<gateway>/api/v2/users
        METHOD: GET
        tests created user using 20 random upper case characters can be returned by using get user by id endpoint.
                """
        self.run_tests('test_get_orgs_20_char_upper_case_', twenty_char_uc)

    #########################################################
    #      Non-alphanumeric Character Get User Name         #
    #########################################################
    @pytest.mark.parametrize('one_char', nonalphanumeric)
    def test_get_users_single_char_nonalphanumeric(self, one_char):
        """
        REST API: http://<gateway>/api/v2/users
        METHOD: GET
        tests created user using single non-alphanumeric characters can be returned by using get user by id endpoint.
        """
        self.run_tests('test_get_users_single_char_nonalphanumeric_', one_char)

    @pytest.mark.parametrize('ten_char_alphanumeric', ten_char_nonalphanumeric)
    def test_get_users_10_char_nonalphanumeric(self, ten_char_alphanumeric):
        """
        REST API: http://<gateway>/api/v2/users
        METHOD: GET
        tests created user using 10 random non-alphanumeric characters can be returned by using get user by id endpoint.
        """
        self.run_tests('test_get_orgs_10_char_nonalphanumeric_', ten_char_alphanumeric)

    @pytest.mark.parametrize('twenty_char_alphanumeric', twenty_char_nonalphanumeric)
    def test_get_users_20_char_nonalphanumeric(self, twenty_char_alphanumeric):
        """
        REST API: http://<gateway>/api/v2/users
        METHOD: GET
        tests created user using 20 random non-alphanumeric characters can be returned by using get user by id endpoint.
        """
        self.run_tests('test_get_orgs_20_char_nonalphanumeric_', twenty_char_alphanumeric)

    #################################################
    #      Number Characters Get User Name          #
    #################################################
    @pytest.mark.parametrize('one_char', digits)
    def test_get_users_single_char_numbers(self, one_char):
        """
        REST API: http://<gateway>/api/v2/users
        METHOD: GET
        tests created user using single digits can be returned by using get user by id endpoint.
        """
        self.run_tests('test_get_users_single_char_numbers_', one_char)

    @pytest.mark.parametrize('ten_char_numbers', ten_char_numbers)
    def test_get_users_10_char_numbers(self, ten_char_numbers):
        """
        REST API: http://<gateway>/api/v2/users
        METHOD: GET
        tests created user using 10 random digits can be returned by using get user by id endpoint.
        """
        self.run_tests('test_get_users_10_char_numbers_', ten_char_numbers)

    @pytest.mark.parametrize('five_char_numbers', five_char_numbers)
    def test_get_users_5_char_numbers(self, five_char_numbers):
        """
        REST API: http://<gateway>/api/v2/users
        METHOD: GET
        tests created user using 5 random digits can be returned by using get user by id endpoint.
        """
        self.run_tests('test_get_users_5_char_numbers_', five_char_numbers)

    ####################################
    #     Mix Characters Get User Name #
    ####################################
    @pytest.mark.parametrize('twenty_char', twenty_char_names_list)
    def test_get_users_20_char_name_mix(self, twenty_char):
        """
        REST API: http://<gateway>/api/v2/users
        METHOD: GET
        tests created user using 20 mix characters can be returned by using get user by id endpoint.
        """
        self.run_tests('test_get_users_20_char_name_mix_', twenty_char)

    @pytest.mark.parametrize('forty_char', forty_char_names_list)
    def test_get_users_40_char_name_mix(self, forty_char):
        """
        REST API: http://<gateway>/api/v2/users
        METHOD: GET
        tests created user using 40 mix characters can be returned by using get user by id endpoint.
                """
        self.run_tests('test_get_users_40_char_name_mix_', forty_char)

    @pytest.mark.parametrize('two_hundred_char_names', two_hundred_char_name_list)
    def test_get_users_200_char_mix(self, two_hundred_char_names):
        """
        REST API: http://<gateway>/api/v2/users
        METHOD: GET
        tests created user using 200 mix characters can be returned by using get user by id endpoint.
        """
        self.run_tests('test_get_users_200_char_name_mix_', two_hundred_char_names)

    @pytest.mark.parametrize('four_hundred_char_names', four_hundred_char_name_list)
    def test_get_users_400_char_mix(self, four_hundred_char_names):
        """
        REST API: http://<gateway>/api/v2/users
        METHOD: GET
        tests created user using 400 mix characters can be returned by using get user by id endpoint.
                """
        self.run_tests('test_get_users_400_char_name_mix_', four_hundred_char_names)

    @pytest.mark.parametrize('special_char', special_char)
    def test_get_users_special_chars(self, special_char):
        """
        REST API: http://<gateway>/api/v2/users
        METHOD: GET
        tests created user using special characters can be returned by using get user by id endpoint.
        """
        self.run_tests('test_get_users_special_chars_', special_char)

    def test_get_non_existent_user_id(self):
        """
        REST API: http://<gateway>/api/v2/users
        METHOD: GET
        tests getting non-existent user returns an error.
        """
        test_name = 'test_get_non_existent_user_id '
        user_id = 'doesnotexist'
        expected_status = 404
        expected_error_message = 'user not found'
        self.header(test_name)
        self.mylog.info(test_name + 'STEP 1: Get non-existent user id')
        status, actual_user_id, actual_user_name, error_message = \
            gateway_util.get_user_by_id(self, self.gateway, user_id)
        self.mylog.info(test_name + 'Assert actual status \'%s\' equals to expected status \'%s\''
                        % (status, expected_status))
        _assert(self, status, expected_status, 'status code', xfail=True,
                reason='https://github.com/influxdata/platform/issues/163')
        self.mylog.info(test_name + 'Assert actual error message \'%s\' equals to expected error message \'%s\''
                        % (error_message, expected_error_message))
        _assert(self, error_message, expected_error_message, 'error message')
