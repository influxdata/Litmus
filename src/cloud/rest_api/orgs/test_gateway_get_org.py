
import pytest
import src.util.login_util as lu
from src.chronograf.lib import chronograf_rest_lib as crl
from src.util import gateway_util
from string import ascii_lowercase
from string import ascii_uppercase
from string import digits
from src.cloud.rest_api.conftest import ten_char_lc, twenty_char_lc, twenty_char_uc, ten_char_uc, \
    ten_char_numbers, five_char_numbers, nonalphanumeric, ten_char_nonalphanumeric, \
    twenty_char_nonalphanumeric, twenty_char_names_list, fourty_char_names_list, \
    four_hundred_char_name_list, two_hundred_char_name_list, special_char

@pytest.mark.usefixtures('remove_orgs','gateway')
class TestGetOrganizationsAPI(object):
    '''
    Test Suite for testing REST API endpoint for getting single organization
    Removes created by tests organizations before running tests
    '''

    mylog=lu.log(lu.get_log_path(), 'w', __name__)
    rl=crl.RestLib(mylog)

    def header(self, test_name):
        self.mylog.info('#' * (11+len(test_name)+17))
        self.mylog.info('<--------- %s START --------->' % test_name)
        self.mylog.info('#' * (11+len(test_name)+17))

    def footer(self, test_name):
        self.mylog.info('#' * (11+len(test_name)+15))
        self.mylog.info('<--------- %s END --------->' % test_name)
        self.mylog.info('#' * (11 + len(test_name) + 15))
        self.mylog.info('')

    def run_tests(self, name_of_the_test_to_run, org_name):
        '''
        :param name_of_the_test_to_run: test name to run
        :param org_name: name of the organization
        :return: pass/fail
        '''
        test_name=name_of_the_test_to_run + org_name + ' '
        self.header(test_name)
        self.mylog.info(test_name + ' STEP 1: Create Organization "%s"' % org_name)
        (status, created_org_id, created_org_name, error_message)=gateway_util.create_organization(self, self.gateway, org_name)
        if org_name == '':
            assert status == 404, \
                pytest.xfail(reason='https://github.com/influxdata/platform/issues/188')
        elif org_name == 'BackSlash\\':
            assert status == 201, \
                pytest.xfail(reason='https://github.com/influxdata/platform/issues/163')
        else:
            assert status == 201,\
                self.mylog.info(test_name + 'Assertion Failed, status=%s' % status)
        assert status == 201, \
            self.mylog.info(test_name + 'Assertion failed. status=%d, error message %s' % (status, error_message))

        self.mylog.info(test_name + ' STEP 2: Check the organization data was persisted in etcd')
        gateway_util.verify_org_etcd(self, self.etcd, created_org_id, created_org_name)

        self.mylog.info(test_name + ' STEP 3: Get Created Organization')
        (status, actual_org_id, actual_org_name, error_message)=\
            gateway_util.get_organization_by_id(self, self.gateway, created_org_id)
        assert status == 200, \
            self.mylog.info(test_name + 'Assertion failed. status=%d, error message %s' % (status, error_message))
        self.mylog.info(test_name + 'Assert expected org_id ' + str(created_org_id) +
                        ' equals actual org_id ' + str(actual_org_id))
        assert created_org_id == actual_org_id, \
            self.mylog.info(test_name + ' Expected user id is not equal to actual user id' + str(error_message))
        self.mylog.info(test_name + 'Assert expected user_name ' + str(org_name) + ' equals actual user name '
                        + str(actual_org_name))
        assert created_org_name == actual_org_name, \
            self.mylog.info(test_name + ' Expected user name is not equal to actual user name' + str(error_message))
        self.footer(test_name)

    ############################################
    #       Lower Case Character Org Names     #
    ############################################
    @pytest.mark.parametrize('one_char', ascii_lowercase)
    def test_get_orgs_single_char_lower_case(self, one_char):
        '''
        REST API: http://<gateway>/v1/orgs
        METHOD: GET
        tests created user using single lower case characters can be returned by using "get org by id endpoint".
        '''
        self.run_tests('test_get_orgs_single_char_lower_case ', one_char)

    @pytest.mark.parametrize('ten_char_lc', ten_char_lc    )
    def test_get_orgs_10_char_lower_case(self, ten_char_lc):
        '''
        REST API: http://<gateway>/v1/orgs
        METHOD: GET
        tests created org using 10 random lower case characters can be returned by using "get org by id" endpoint.
        '''
        self.run_tests('test_get_orgs_10_char_lower_case ', ten_char_lc)

    @pytest.mark.parametrize('twenty_char_lc', twenty_char_lc)
    def test_get_orgs_20_char_lower_case(self, twenty_char_lc):
        '''
        REST API: http://<gateway>/v1/orgs
        METHOD: GET
        tests created org using 20 random lower case characters can be returned by using "get org by id" endpoint.
        '''
        self.run_tests('test_get_orgs_20_char_lower_case ', twenty_char_lc)

    ###################################################
    #          Upper Case Character Org Names         #
    ###################################################
    @pytest.mark.parametrize('one_char', ascii_uppercase)
    def test_get_orgs_single_char_upper_case(self, one_char):
        '''
        REST API: http://<gateway>/v1/orgs
        METHOD: GET
        tests created org using single UPPER case characters can be returned by using "get org by id endpoint".
        '''
        self.run_tests('test_get_orgs_single_char_upper_case ', one_char)

    @pytest.mark.parametrize('ten_char_uc', ten_char_uc)
    def test_get_orgs_10_char_upper_case(self, ten_char_uc):
        '''
        REST API: http://<gateway>/v1/orgs
        METHOD: GET
        tests created org using 10 random UPPER case characters can be returned by using "get org by id endpoint".
        '''
        self.run_tests('test_get_orgs_10_char_upper_case ', ten_char_uc)

    @pytest.mark.parametrize('twenty_char_uc', twenty_char_uc)
    def test_get_orgs_20_char_upper_case(self, twenty_char_uc):
        '''
        REST API: http://<gateway>/v1/orgs
        METHOD: GET
        tests created org using 20 random UPPER case characters can be returned by using "get org by id endpoint".
        '''
        self.run_tests('test_get_orgs_20_char_upper_case ', twenty_char_uc)

    #########################################################
    #          Non-alphanumeric Character Org Names         #
    #########################################################
    @pytest.mark.parametrize('one_char', nonalphanumeric)
    def test_get_orgs_single_char_nonalphanumeric(self, one_char):
        '''
        REST API: http://<gateway>/v1/orgs
        METHOD: GET
        tests created org using non-alphanumeric characters can be returned by using "get org by id endpoint".
        '''
        self.run_tests('test_get_orgs_single_char_nonalphanumeric ', one_char)

    @pytest.mark.parametrize('ten_char_nonalphanumeric', ten_char_nonalphanumeric)
    def test_get_orgs_10_char_nonalphanumeric(self, ten_char_nonalphanumeric):
        '''
        REST API: http://<gateway>/v1/orgs
        METHOD: GET
        tests created org using 10 random non-alphanumeric characters can be returned by using "get org by id endpoint".
        '''
        self.run_tests('test_get_orgs_10_char_nonalphanumeric ', ten_char_nonalphanumeric)

    @pytest.mark.parametrize('twenty_char_nonalphanumeric', twenty_char_nonalphanumeric)
    def test_get_orgs_20_char_nonalphanumeric(self, twenty_char_nonalphanumeric):
        '''
        REST API: http://<gateway>/v1/orgs
        METHOD: GET
        tests created org using 20 random non-alphanumeric characters can be returned by using "get org by id endpoint".
        '''
        self.run_tests('test_get_orgs_20_char_nonalphanumeric', twenty_char_nonalphanumeric)


    #################################################
    #          Number Characters Org Names          #
    #################################################
    @pytest.mark.parametrize('one_char', digits)
    def test_get_orgs_single_char_numbers(self, one_char):
        '''
        REST API: http://<gateway>/v1/orgs
        METHOD: GET
        tests created org using single digits can be returned by using "get org by id endpoint"
        '''
        self.run_tests('test_get_orgs_single_char_numbers', one_char)

    @pytest.mark.parametrize('ten_char_numbers', ten_char_numbers)
    def test_get_orgs_10_char_numbers(self, ten_char_numbers):
        '''
        REST API: http://<gateway>/v1/orgs
        METHOD: GET
        tests created org using 10 random digits can be returned by using "get org by id endpoint"
        '''
        self.run_tests('test_get_orgs_10_char_numbers ', ten_char_numbers)

    @pytest.mark.parametrize('five_char_numbers', five_char_numbers)
    def test_get_orgs_5_char_numbers(self, five_char_numbers):
        '''
        REST API: http://<gateway>/v1/orgs
        METHOD: GET
        tests created org using 5 random digits can be returned by using "get org by id endpoint"
        '''
        self.run_tests('test_get_orgs_5_char_numbers ', five_char_numbers)

    ####################################
    #     Mix Characters Org Names     #
    ####################################
    @pytest.mark.parametrize('twenty_char', twenty_char_names_list)
    def test_get_orgs_20_char_name_mix(self, twenty_char):
        '''
        REST API: http://<gateway>/v1/orgs
        METHOD: GET
        tests created org using 20 mixed characters can be returned by using "get org by id endpoint"
        '''
        self.run_tests('test_get_orgs_20_char_name_mix ', twenty_char)

    @pytest.mark.parametrize('fourty_char', fourty_char_names_list)
    def test_get_orgs_40_char_name_mix(self, fourty_char):
        '''
        REST API: http://<gateway>/v1/orgs
        METHOD: GET
        tests created org using 40 mixed characters can be returned by using "get org by id endpoint"
        '''
        self.run_tests('test_get_orgs_40_char_name_mix ', fourty_char)

    @pytest.mark.parametrize('two_hundred_char_name', two_hundred_char_name_list)
    def test_get_orgs_200_char_mix(self, two_hundred_char_name):
        '''
        REST API: http://<gateway>/v1/orgs
        METHOD: GET
        tests created org using 200 mixed characters can be returned by using "get org by id endpoint"
        '''
        self.run_tests('test_get_orgs_200_char_mix ', two_hundred_char_name)

    @pytest.mark.parametrize('four_hundred_char_name', four_hundred_char_name_list)
    def test_get_orgs_400_char_mix(self, four_hundred_char_name):
        '''
        REST API: http://<gateway>/v1/orgs
        METHOD: GET
        tests created org using 400 mixed characters can be returned by using "get org by id endpoint"
        '''
        self.run_tests('test_get_orgs_400_char_mix ', four_hundred_char_name)

    @pytest.mark.parametrize('special_char', special_char)
    def test_get_orgs_special_chars(self, special_char):
        '''
        REST API: http://<gateway>/v1/orgs
        METHOD: GET
        tests created org using special characters can be returned by using "get org by id endpoint"
        '''
        self.run_tests('test_get_orgs_special_chars ', special_char)

    def test_get_non_existent_org_id(self):
        '''
        REST API: http://<gateway>/v1/orgs
        METHOD: GET
        tests getting non-existent org returns an error.
        '''
        test_name='test_get_non_existent_org_id '
        org_id='doesnotexist'
        expected_status=404
        expected_error_message='organization not found'
        self.header(test_name)
        self.mylog.info(test_name + 'STEP 1: Get non-existent org id')
        (status, id, name, error_message)=gateway_util.get_organization_by_id(self, self.gateway, org_id)
        self.mylog.info(test_name + 'Assert expected status %s is equal to actual status %s' % (expected_status, status))
        assert expected_status == status, pytest.xfail(reason='https://github.com/influxdata/platform/issues/163')
        self.mylog.info(test_name + 'Assert expected error message %s equals actual error message %s'
                        % (expected_error_message, error_message))
        assert expected_error_message == error_message, self.mylog.info(test_name + 'Assertion failed')
