
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
class TestGetUsersAPI(object):
    '''
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

    def run_tests(self, name_of_the_test, user_name):
        '''
        :param name_of_the_test: name of the test to run
        :param user_name: user name to get
        :return: pass/fail
        '''
        test_name=name_of_the_test + user_name + ' '
        self.header(test_name)
        self.mylog.info(test_name + ' STEP 1: Create Users')
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
        assert status == 201, \
            self.mylog.info(test_name + 'Assertion failed. status=%d, error message %s' % (status, error_message))

        self.mylog.info(test_name + 'STEP 2: Verify data was persisted in the etcd store')
        gateway_util.verify_user_etcd(self, self.etcd, created_user_id, created_user_name)

        self.mylog.info(test_name + ' STEP 3: Get Created User')
        (status, actual_user_id, actual_user_name, error_message) = \
            gateway_util.get_user_by_id(self, self.gateway, created_user_id)
        assert status == 200, \
            self.mylog.info(test_name + 'Assertion failed. status=%d, error message %s' % (status, error_message))
        self.mylog.info(test_name + 'Assert expected user_id ' + str(created_user_id) +
                        ' equals actual user id ' + str(actual_user_id))
        assert actual_user_id == created_user_id, \
            self.mylog.info(test_name + ' Expected user id is not equal to actual user id' + error_message)
        self.mylog.info(test_name + 'Assert expected user_name ' + str(created_user_name) + ' equals actual user name '
                        + str(actual_user_name))
        assert actual_user_name == created_user_name, \
            self.mylog.info(test_name + ' Expected user name is not equal to actual user name' + error_message)
        self.footer(test_name)


    ############################################
    #   Lower Case Character Get User Name     #
    ############################################
    #@pytest.mark.skip
    @pytest.mark.parametrize('one_char', ascii_lowercase)
    def test_get_users_single_char_lower_case(self, one_char):
        '''
        REST API: http://<gateway>/v1/users
        METHOD: GET
        tests created user using single lower case characters can be returned by using get user by id endpoint.
        '''
        self.run_tests('test_get_users_single_char_lower_case_',one_char)

    #@pytest.mark.skip
    @pytest.mark.parametrize('ten_char_lc', ten_char_lc    )
    def test_get_users_10_char_lower_case(self, ten_char_lc):
        '''
        REST API: http://<gateway>/v1/users
        METHOD: GET
        tests created user using 10 lower case characters can be returned by using get user by id endpoint.
        '''
        self.run_tests('test_get_users_10_char_lower_case_',ten_char_lc)

    #@pytest.mark.skip
    @pytest.mark.parametrize('twenty_char_lc', twenty_char_lc)
    def test_get_users_20_char_lower_case(self, twenty_char_lc):
        '''
        REST API: http://<gateway>/v1/users
        METHOD: GET
        tests created user using 10 lower case characters can be returned by using get user by id endpoint.
        '''
        self.run_tests('test_get_users_20_char_lower_case_', twenty_char_lc)

    ###################################################
    #     Upper Case Character Get User Name          #
    ###################################################
    #@pytest.mark.skip
    @pytest.mark.parametrize('one_char', ascii_uppercase)
    def test_get_users_single_char_upper_case(self, one_char):
        '''
        REST API: http://<gateway>/v1/users
        METHOD: GET
        tests created user using single upper case characters can be returned by using get user by id endpoint.
        '''
        self.run_tests('test_get_users_single_char_upper_case_',one_char)

    #@pytest.mark.skip
    @pytest.mark.parametrize('ten_char_uc', ten_char_uc)
    def test_get_users_10_char_upper_case(self, ten_char_uc):
        '''
        REST API: http://<gateway>/v1/users
        METHOD: GET
        tests created user using 10 upper case characters can be returned by using get user by id endpoint.
        '''
        self.run_tests('est_get_users_10_char_upper_case_',ten_char_uc)


    #@pytest.mark.skip
    @pytest.mark.parametrize('twenty_char_uc', twenty_char_uc)
    def test_get_orgs_20_char_upper_case(self, twenty_char_uc):
        '''
        REST API: http://<gateway>/v1/users
        METHOD: GET
        tests created user using 20 upper case characters can be returned by using get user by id endpoint.
                '''
        self.run_tests('test_get_orgs_20_char_upper_case_', twenty_char_uc)

    #########################################################
    #      Non-alphanumeric Character Get User Name         #
    #########################################################
    #@pytest.mark.skip
    @pytest.mark.parametrize('one_char', nonalphanumeric)
    def test_get_users_single_char_nonalphanumeric(self, one_char):
        '''
        REST API: http://<gateway>/v1/users
        METHOD: GET
        tests created user using single non-alphanumeric characters can be returned by using get user by id endpoint.
        '''
        self.run_tests('test_get_users_single_char_nonalphanumeric_', one_char)

    #@pytest.mark.skip
    @pytest.mark.parametrize('ten_char_alphanumeric', ten_char_nonalphanumeric)
    def test_get_users_10_char_nonalphanumeric(self, ten_char_alphanumeric):
        '''
        REST API: http://<gateway>/v1/users
        METHOD: GET
        tests created user using 10 non-alphanumeric characters can be returned by using get user by id endpoint.
        '''
        self.run_tests('test_get_orgs_10_char_nonalphanumeric_', ten_char_alphanumeric)

    #@pytest.mark.skip
    @pytest.mark.parametrize('twenty_char_alphanumeric', twenty_char_nonalphanumeric)
    def test_get_users_20_char_nonalphanumeric(self, twenty_char_alphanumeric):
        '''
        REST API: http://<gateway>/v1/users
        METHOD: GET
        tests created user using 10 non-alphanumeric characters can be returned by using get user by id endpoint.
        '''
        self.run_tests('test_get_orgs_20_char_nonalphanumeric_', twenty_char_alphanumeric)

    #################################################
    #      Number Characters Get User Name          #
    #################################################
    #@pytest.mark.skip
    @pytest.mark.parametrize('one_char', digits)
    def test_get_users_single_char_numbers(self, one_char):
        '''
        REST API: http://<gateway>/v1/users
        METHOD: GET
        tests created user using single digits can be returned by using get user by id endpoint.
        '''
        self.run_tests('test_get_users_single_char_numbers_', one_char)

    #@pytest.mark.skip
    @pytest.mark.parametrize('ten_char_numbers', ten_char_numbers)
    def test_get_users_10_char_numbers(self, ten_char_numbers):
        '''
        REST API: http://<gateway>/v1/users
        METHOD: GET
        tests created user using 10 digits can be returned by using get user by id endpoint.
        '''
        self.run_tests('test_get_users_10_char_numbers_', ten_char_numbers)

    #@pytest.mark.skip
    @pytest.mark.parametrize('five_char_numbers', five_char_numbers)
    def test_get_users_5_char_numbers(self, five_char_numbers):
        '''
        REST API: http://<gateway>/v1/users
        METHOD: GET
        tests created user using 20 digits can be returned by using get user by id endpoint.
        '''
        self.run_tests('test_get_users_5_char_numbers_', five_char_numbers)

    ####################################
    #     Mix Characters Get User Name #
    ####################################
    #@pytest.mark.skip
    @pytest.mark.parametrize('twenty_char', twenty_char_names_list)
    def test_get_users_20_char_name_mix(self, twenty_char):
        '''
        REST API: http://<gateway>/v1/users
        METHOD: GET
        tests created user using 20 mix characters can be returned by using get user by id endpoint.
        '''
        self.run_tests('test_get_users_20_char_name_mix_', twenty_char)

    #@pytest.mark.skip
    @pytest.mark.parametrize('fourty_char', fourty_char_names_list)
    def test_get_users_40_char_name_mix(self, fourty_char):
        '''
        REST API: http://<gateway>/v1/users
        METHOD: GET
        tests created user using 40 mix characters can be returned by using get user by id endpoint.
                '''
        self.run_tests('test_get_users_40_char_name_mix_', fourty_char)

    #@pytest.mark.skip
    @pytest.mark.parametrize('two_hundred_char_names', two_hundred_char_name_list)
    def test_get_users_200_char_mix(self, two_hundred_char_names):
        '''
        REST API: http://<gateway>/v1/users
        METHOD: GET
        tests created user using 200 mix characters can be returned by using get user by id endpoint.
        '''
        self.run_tests('test_get_users_200_char_name_mix_', two_hundred_char_names)

    #@pytest.mark.skip
    @pytest.mark.parametrize('four_hundred_char_names', four_hundred_char_name_list)
    def test_get_users_400_char_mix(self, four_hundred_char_names):
        '''
        REST API: http://<gateway>/v1/users
        METHOD: GET
        tests created user using 400 mix characters can be returned by using get user by id endpoint.
                '''
        self.run_tests('test_get_users_400_char_name_mix_', four_hundred_char_names)

    #@pytest.mark.skip
    @pytest.mark.parametrize('special_char', special_char)
    def test_get_users_special_chars(self, special_char):
        '''
        REST API: http://<gateway>/v1/users
        METHOD: GET
        tests created user using special characters can be returned by using get user by id endpoint.
        '''
        self.run_tests('test_get_users_special_chars_', special_char)

    #@pytest.mark.skip
    def test_get_non_existent_org_id(self):
        '''
        REST API: http://<gateway>/v1/users
        METHOD: GET
        tests getting non-existent user returns an error.
        '''
        test_name='test_get_non_existent_org_id '
        org_id='doesnotexist'
        expected_status=404
        expected_error_message='organization not found'
        self.header(test_name)
        self.mylog.info(test_name + 'STEP 1: Get non-existent org id')
        (status, id, name, error_message)=gateway_util.get_organization(self, self.gateway, org_id)
        self.mylog.info(test_name + 'Assert expected status %s is equal to actual status %s' % (expected_status, status))
        assert expected_status == status, pytest.xfail(reason='https://github.com/influxdata/platform/issues/163')
        self.mylog.info(test_name + 'Assert expected error message %s equals actual error message %s'
                        % (expected_error_message, error_message))
        assert expected_error_message == error_message, self.mylog.info(test_name + 'Assertion failed')
