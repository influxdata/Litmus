
import pytest
import src.util.login_util as lu
from src.chronograf.lib import chronograf_rest_lib as crl
import src.util.gateway_util as gateway_util
from string import ascii_lowercase
from string import ascii_uppercase
from string import digits
from conftest import ten_char_lc, twenty_char_lc, twenty_char_uc, ten_char_uc, \
    ten_char_numbers, five_char_numbers, nonalphanumeric, ten_char_nonalphanumeric, \
    twenty_char_nonalphanumeric, twenty_char_names_list, fourty_char_names_list, \
    four_hundred_char_name_list, two_hundred_char_name_list, special_char

@pytest.mark.usefixtures('remove_users','gateway')
class TestUpdateUsersAPI(object):
    '''
    remove created by tests users
    '''
    mylog=lu.log(lu.get_log_path(), 'w', __name__)
    rl=crl.RestLib(mylog)

    def header(self, test_name):
        self.mylog.info('#######################################################')
        self.mylog.info('<--------------- %s START --------------->' % test_name)
        self.mylog.info('#######################################################')

    def footer(self, test_name):
        self.mylog.info('#######################################################')
        self.mylog.info('<--------------- %s END --------------->' % test_name)
        self.mylog.info('#######################################################')
        self.mylog.info('')

    def run_tests(self, name_of_the_test_to_run, user_name):
        '''
        :param name_of_the_test_to_run: name of the test to be run
        :param user_name: name of tuser under the test
        :return: pass/fail
        '''
        test_name=name_of_the_test_to_run + user_name + ' '
        new_name_to_assert=''
        if user_name == 'DoubleQuotes\\"':
            new_name_to_assert='DoubleQuotes"_updated_name'
        new_name=user_name + '_updated_name'
        self.header(test_name)
        self.mylog.info(test_name + ' STEP 1: Create User')
        (status, created_user_id, created_user_name, error_message) = \
            gateway_util.create_user(self, self.gateway, user_name)
        if user_name == '':
            assert status == 404, \
                pytest.xfail(reason='https://github.com/influxdata/platform/issues/188')
        elif user_name == 'BackSlash\\':
            assert status == 201, \
                pytest.xfail(reason='https://github.com/influxdata/platform/issues/163')
        else:
            assert status == 201, \
                self.mylog.info(test_name + 'Assertion Failed, status=%s' % status)

        self.mylog.info(test_name + ' STEP 2: Update created user with the \'%s\' name' % new_name)
        (status, new_user_id, updated_user_name, error_message) = \
            gateway_util.update_user(self, self.gateway, created_user_id, new_name)
        assert status == 200, \
            self.mylog.info(test_name + 'Assertion Failed. status=%d, error message %s' % (status, error_message))
        assert new_user_id == created_user_id, \
            self.mylog.info(test_name + 'Assertion Failed. New user id is not equal original user id')
        if user_name == 'DoubleQuotes\\"':
            assert updated_user_name == new_name_to_assert, self.mylog.info(
                test_name + 'Assertion Failed. Updated name is not equal expected name')
        else:
            assert updated_user_name == new_name, self.mylog.info(
                test_name + 'Assertion Failed. Updated name is not equal expected name')

        self.mylog.info(test_name + 'STEP 3: Verify updated name was persisted in the etcd store')
        gateway_util.verify_user_etcd(self, self.etcd, new_user_id, updated_user_name)
        self.footer(test_name)

    ############################################
    #       Lower Case Character User Names    #
    ############################################
    @pytest.mark.parametrize('one_char', ascii_lowercase)
    def test_update_users_single_char_lower_case(self, one_char):
        '''
        REST API: http://<gateway>/v1/users
        METHOD: PATCH
        tests user name containing single character lower case letters can be updated and persisted in the etcd store.
        '''
        self.run_tests('test_update_users_single_char_lower_case_', one_char)

    @pytest.mark.parametrize('ten_char', ten_char_lc)
    def test_update_users_10_char_lower_case(self, ten_char):
        '''
        REST API: http://<gateway>/v1/users
        METHOD: PATCH
        tests user name containing 10 characters lower case letters can be updated and persisted in the etcd store.
        '''
        self.run_tests('test_update_users_10_char_lower_case_', ten_char)

    @pytest.mark.parametrize('twenty_char', twenty_char_lc)
    def test_update_users_20_char_lower_case(self, twenty_char):
        '''
        REST API: http://<gateway>/v1/users
        METHOD: PATCH
        tests user name containing 20 characters lower case letters can be updated and persisted in the etcd store.
        '''
        self.run_tests('test_update_users_20_char_lower_case_', twenty_char)

    ###################################################
    #          Upper Case Character User Names        #
    ###################################################
    @pytest.mark.parametrize('one_char', ascii_uppercase)
    def test_update_users_single_char_upper_case(self, one_char):
        '''
        REST API: http://<gateway>/v1/users
        METHOD: PATCH
        tests user name containing single upper case character letters can be updated and persisted in the etcd store.
        '''
        self.run_tests('test_update_users_single_char_upper_case_', one_char)

    @pytest.mark.parametrize('ten_char', ten_char_uc)
    def test_update_users_10_char_upper_case(self, ten_char):
        '''
        REST API: http://<gateway>/v1/users
        METHOD: PATCH
        tests user name containing 10 upper case character letters can be updated and persisted in the etcd store.
        '''
        self.run_tests('test_update_users_10_char_upper_case_', ten_char)

    @pytest.mark.parametrize('twenty_char', twenty_char_uc)
    def test_update_users_20_char_upper_case(self, twenty_char):
        '''
        REST API: http://<gateway>/v1/users
        METHOD: PATCH
        tests user name containing 20 upper case character letters can be updated and persisted in the etcd store.
        '''
        self.run_tests('test_update_users_20_char_upper_case_', twenty_char)

    #########################################################
    #          Non-alphanumeric Character User Names        #
    #########################################################
    @pytest.mark.parametrize('one_char', nonalphanumeric)
    def test_update_users_single_char_nonalphanumeric(self, one_char):
        '''
        REST API: http://<gateway>/v1/users
        METHOD: PATCH
        tests user name containing non-alphanumeric character letters can be updated and persisted in the etcd store.
        '''
        self.run_tests('test_update_users_single_char_nonalphanumeric_', one_char)

    @pytest.mark.parametrize('ten_char_nonalphanumeric', ten_char_nonalphanumeric)
    def test_update_users_10_char_nonalphanumeric(self, ten_char_nonalphanumeric):
        '''
        REST API: http://<gateway>/v1/users
        METHOD: PATCH
        tests user name containing 10 non-alphanumeric character letters can be updated and persisted in the etcd store.
        '''
        self.run_tests('test_update_users_10_char_nonalphanumeric_', ten_char_nonalphanumeric)

    @pytest.mark.parametrize('twenty_char_nonalphanumeric', twenty_char_nonalphanumeric)
    def test_update_orgs_20_char_nonalphanumeric_case(self, twenty_char_nonalphanumeric):
        '''
        REST API: http://<gateway>/v1/users
        METHOD: PATCH
        tests user name containing 20 non-alphanumeric character letters can be updated and persisted in the etcd store.
        '''
        self.run_tests('twenty_char_nonalphanumeric_', twenty_char_nonalphanumeric)

    #################################################
    #          Number Characters User Names         #
    #################################################
    @pytest.mark.parametrize('one_char', digits)
    def test_update_users_single_char_numbers(self, one_char):
        '''
        REST API: http://<gateway>/v1/users
        METHOD: PATCH
        tests user name containing single digits can be updated and persisted in the etcd store.
        '''
        self.run_tests('test_update_users_single_char_numbers_', one_char)

    @pytest.mark.parametrize('ten_char_numbers', ten_char_numbers)
    def test_update_users_10_char_numbers(self, ten_char_numbers):
        '''
        REST API: http://<gateway>/v1/users
        METHOD: PATCH
        tests user name containing 10 digits can be updated and persisted in the etcd store.
        '''
        self.run_tests('test_update_users_10_char_numbers_', ten_char_numbers)

    @pytest.mark.parametrize('five_numbers', five_char_numbers)
    def test_update_users_5_char_numbers(self, five_numbers):
        '''
        REST API: http://<gateway>/v1/users
        METHOD: PATCH
        tests user name containing 5 digits can be updated and persisted in the etcd store.
        '''
        self.run_tests('test_update_users_5_char_numbers_', five_numbers)

    ####################################
    #     Mix Characters User Names    #
    ####################################
    @pytest.mark.parametrize('twenty_char_names', twenty_char_names_list)
    def test_update_users_20_char_mix(self, twenty_char_names):
        '''
        REST API: http://<gateway>/v1/users
        METHOD: PATCH
        tests user name containing 20 mix characters can be updated and persisted in the etcd store.
        '''
        self.run_tests('test_update_users_20_char_mix_', twenty_char_names)

    @pytest.mark.parametrize('fourty_char_names', fourty_char_names_list)
    def test_update_users_40_char_mix(self, fourty_char_names):
        '''
        REST API: http://<gateway>/v1/users
        METHOD: PATCH
        tests user name containing 40 mix characters can be updated and persisted in the etcd store.
        '''
        self.run_tests('test_update_users_40_char_mix_', fourty_char_names)

    @pytest.mark.parametrize('two_hundred_char_names', two_hundred_char_name_list)
    def test_update_users_200_char_mix(self, two_hundred_char_names):
        '''
        REST API: http://<gateway>/v1/users
        METHOD: PATCH
        tests user name containing 200 mix characters can be updated and persisted in the etcd store.
        '''
        self.run_tests('test_update_users_200_char_mix_', two_hundred_char_names)

    @pytest.mark.parametrize('four_hundred_char_names', four_hundred_char_name_list)
    def test_update_users_400_char_mix(self, four_hundred_char_names):
        '''
        REST API: http://<gateway>/v1/users
        METHOD: PATCH
        tests user name containing 400 mix characters can be updated and persisted in the etcd store.
        '''
        self.run_tests('test_update_users_400_char_mix_', four_hundred_char_names)

    @pytest.mark.parametrize('special_char', special_char)
    def test_update_users_special_chars(self, special_char):
        '''
        REST API: http://<gateway>/v1/users
        METHOD: PATCH
        tests user name containing special characters can be updated and persisted in the etcd store.
        '''
        self.run_tests('test_update_users_special_chars_', special_char)

    def test_update_users_already_exist(self):
        '''
        REST API: http://<gateway>/v1/users
        METHOD: PATCH
        tests user name can be updated and persisted in the etcd store if name already exists.
        '''
        test_name='test_update_users_already_exist'
        user_name='existing_user'
        self.header(test_name)
        self.mylog.info(test_name + ' STEP 1: Create User')
        (status, created_user_id, created_user_name, error_message) = \
            gateway_util.create_user(self, self.gateway, user_name)
        assert status == 201, \
            self.mylog.info(test_name + 'Assertion failed. status=%d, error message %s' % (status, error_message))

        self.mylog.info(test_name + ' STEP 2: Update created user with the \'%s\' name' % user_name)
        (status, updated_user_id, updated_user_name, error_message) = \
            gateway_util.update_user(self, self.gateway, created_user_id, user_name)
        assert status == 200, \
            self.mylog.info(test_name + 'Assertion Failed. status=%d, error message %s' % (status, error_message))
        assert updated_user_id == created_user_id, \
            self.mylog.info(test_name + 'Assertion Failed. New user id is not equal original user id')
        assert updated_user_name == user_name, self.mylog.info(
            test_name + 'Assertion Failed. Updated name is not equal expected name')

        self.mylog.info(test_name + 'STEP 3: Verify created user was persisted in the etcd store')
        gateway_util.verify_user_etcd(self, self.etcd, updated_user_id, updated_user_name)
        self.footer(test_name)

    def test_update_users_empty_name(self):
        '''
        REST API: http://<gateway>/v1/users
        METHOD: PATCH
        tests user name can not be updated and persisted in the etcd store if name is empty
        '''
        test_name='test_update_users_empy_name'
        user_name='user_to_be_updated'
        user_name_to_update=''
        self.header(test_name)
        self.mylog.info(test_name + ' STEP 1: Create User')
        (status, created_user_id, created_user_name, error_message) = \
            gateway_util.create_user(self, self.gateway, user_name)
        assert status == 201, \
            self.mylog.info(test_name + 'Assertion failed. status=%d, error message %s' % (status, error_message))

        self.mylog.info(test_name + 'STEP 2: Verify created user was persisted in the etcd store')
        gateway_util.verify_user_etcd(self, self.etcd, created_user_id, created_user_name)

        self.mylog.info(test_name + ' STEP 3: Update created user with the \'%s\' name' % user_name_to_update)
        (status, updated_user_id, updated_user_name, error_message) = \
            gateway_util.update_user(self, self.gateway, created_user_id, user_name_to_update)
        assert status == 404, \
            pytest.xfail(reason='https://github.com/influxdata/platform/issues/188')
        self.footer(test_name)



