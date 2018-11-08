from string import ascii_lowercase
from string import ascii_uppercase
from string import digits

import pytest

import src.util.login_util as lu
from src.chronograf.lib import chronograf_rest_lib as crl
# noinspection PyProtectedMember
from src.cloud.rest_api.conftest import ten_char_lc, twenty_char_lc, twenty_char_uc, ten_char_uc, \
    ten_char_numbers, five_char_numbers, nonalphanumeric, ten_char_nonalphanumeric, \
    twenty_char_nonalphanumeric, twenty_char_names_list, forty_char_names_list, \
    four_hundred_char_name_list, two_hundred_char_name_list, special_char, _assert, verify_org_etcd_entries
# from src.util import gateway_util
from src.util.twodotoh import org_util


@pytest.mark.usefixtures('remove_orgs', 'gateway')
class TestCreateOrganizationsAPI(object):
    """
    Test Suite for testing REST API endpoint for creating organizations
    The existing orgs would be removed before running tests
    """

    mylog = lu.log(lu.get_log_path(), 'w', __name__)
    rl = crl.RestLib(mylog)

    def header(self, test_name):
        """
        :param test_name:
        :return:
        """
        self.mylog.info('#' * (11 + len(test_name) + 17))
        self.mylog.info('<--------- %s START --------->' % test_name)
        self.mylog.info('#' * (11 + len(test_name) + 17))

    def footer(self, test_name):
        """
        :param test_name:
        :return:
        """
        self.mylog.info('#' * (11 + len(test_name) + 15))
        self.mylog.info('<--------- %s END --------->' % test_name)
        self.mylog.info('#' * (11 + len(test_name) + 15))
        self.mylog.info('')

    def run_tests(self, name_of_the_test_to_run, org_name):
        """
        :param name_of_the_test_to_run: test to be run
        :param org_name: name of the organization to be created
        :return: pass/fail
        """
        test_name = name_of_the_test_to_run + org_name + ' '
        self.header(test_name)
        self.mylog.info(test_name + ' STEP 1: Create Organization "%s"' % org_name)
        create_result = org_util.create_organization(self, self.gateway, org_name)
        status = create_result['status']
        created_org_id = create_result['org_id']
        created_org_name = create_result['org_name']
        if org_name == '':
            # TODO: According to @goller organization with empty name can be created. Currently there is a bug.
            # TODO: Create a bug (@gshif)
            _assert(self, status, 201, 'status code', xfail=True,
                    reason='Should be able to create an org with empty name')
        elif org_name == 'BackSlash\\':
            _assert(self, status, 201, 'status code', xfail=True,
                    reason='https://github.com/influxdata/platform/issues/163')
        else:
            _assert(self, status, 201, 'status code')

        self.mylog.info(test_name + 'STEP 2: Verify data was persisted in the etcd store')
        verify_org_etcd_entries(self, test_name, created_org_id, created_org_name, error='')
        self.footer(test_name)

    ############################################
    #       Lower Case Character Org Names     #
    ############################################
    @pytest.mark.parametrize('one_char', ascii_lowercase)
    def test_create_orgs_single_char_lower_case(self, one_char):
        """
        REST API: http://<gateway>/api/v2/orgs
        METHOD: POST
        tests org name containing single character lower case letters can be created and persisted in the etcd store.
        """
        self.run_tests('test_create_orgs_single_char_lower_case ', one_char)

    @pytest.mark.parametrize('ten_char_lc', ten_char_lc)
    def test_create_orgs_10_char_lower_case(self, ten_char_lc):
        """
        REST API: http://<gateway>/api/v2/orgs
        METHOD: POST
        tests org name containing random 10 lower case letters can be created and persisted in the etcd store.
        """
        self.run_tests('test_create_orgs_10_char_lower_case ', ten_char_lc)

    @pytest.mark.parametrize('twenty_char_lc', twenty_char_lc)
    def test_create_orgs_20_char_lower_case(self, twenty_char_lc):
        """
        REST API: http://<gateway>/api/v2/orgs
        METHOD: POST
        tests org name containing random 20 lower case letters can be created and persisted in the etcd store.
        """
        self.run_tests('test_create_orgs_20_char_lower_case ', twenty_char_lc)

    ###################################################
    #          Upper Case Character Org Names         #
    ###################################################
    @pytest.mark.parametrize('one_char', ascii_uppercase)
    def test_create_orgs_single_char_upper_case(self, one_char):
        """
        REST API: http://<gateway>/api/v2/orgs
        METHOD: POST
        tests org name containing single character upper case letters can be created and persisted in the etcd store.
        """
        self.run_tests('test_create_orgs_single_char_upper_case ', one_char)

    @pytest.mark.parametrize('ten_char_uc', ten_char_uc)
    def test_create_orgs_10_char_upper_case(self, ten_char_uc):
        """
        REST API: http://<gateway>/api/v2/orgs
        METHOD: POST
        tests org name containing random 10 upper case letters can be created and persisted in the etcd store.
        """
        self.run_tests('test_create_orgs_10_char_upper_case ', ten_char_uc)

    @pytest.mark.parametrize('twenty_char_uc', twenty_char_uc)
    def test_create_orgs_20_char_upper_case(self, twenty_char_uc):
        """
        REST API: http://<gateway>/api/v2/orgs
        METHOD: POST
        tests org name containing random 20 upper case letters can be created and persisted in the etcd store.
        """
        self.run_tests('test_create_orgs_20_char_upper_case ', twenty_char_uc)

    #########################################################
    #          Non-alphanumeric Character Org Names         #
    #########################################################
    @pytest.mark.parametrize('one_char', nonalphanumeric)
    def test_create_orgs_single_char_nonalphanumeric_case(self, one_char):
        """
        REST API: http://<gateway>/api/v2/orgs
        METHOD: POST
        tests org name containing single non-alphanumeric characters can be created and persisted in the etcd store.
        """
        self.run_tests('test_create_orgs_single_char_nonalphanumeric_case ', one_char)

    @pytest.mark.parametrize('ten_char_nonalphanumeric', ten_char_nonalphanumeric)
    def test_create_orgs_10_char_nonalphanumeric_case(self, ten_char_nonalphanumeric):
        """
        REST API: http://<gateway>/api/v2/orgs
        METHOD: POST
        tests org name containing 10 random non-alphanumeric characters can be created and persisted in the etcd store.
        """
        self.run_tests('test_create_orgs_10_char_nonalphanumeric_case ', ten_char_nonalphanumeric)

    @pytest.mark.parametrize('twenty_char_nonalphanumeric', twenty_char_nonalphanumeric)
    def test_create_orgs_20_char_nonalphanumeric_case(self, twenty_char_nonalphanumeric):
        """
        REST API: http://<gateway>/api/v2/orgs
        METHOD: POST
        tests org name containing 20 random non-alphanumeric characters can be created and persisted in the etcd store.
        """
        self.run_tests('test_create_orgs_20_char_nonalphanumeric_case ', twenty_char_nonalphanumeric)

    #################################################
    #          Number Characters Org Names          #
    #################################################
    @pytest.mark.parametrize('one_char', digits)
    def test_create_orgs_single_char_numbers(self, one_char):
        """
        REST API: http://<gateway>/api/v2/orgs
        METHOD: POST
        tests org name containing single digits can be created and persisted in the etcd store
        """
        self.run_tests('test_create_orgs_single_char_numbers ', one_char)

    @pytest.mark.parametrize('ten_char_numbers', ten_char_numbers)
    def test_create_orgs_10_char_numbers(self, ten_char_numbers):
        """
        REST API: http://<gateway>/api/v2/orgs
        METHOD: POST
        tests org name containing 10 random digits can be created and persisted in the etcd store
        """
        self.run_tests('test_create_orgs_10_char_numbers', ten_char_numbers)

    @pytest.mark.parametrize('five_chars', five_char_numbers)
    def test_create_orgs_5_char_numbers(self, five_chars):
        """
        REST API: http://<gateway>/api/v2/orgs
        METHOD: POST
        tests org name containing 5 random digits can be created and persisted in the etcd store
        """
        self.run_tests('test_create_orgs_5_char_numbers', five_chars)

    ####################################
    #     Mix Characters Org Names     #
    ####################################
    @pytest.mark.parametrize('twenty_char_names', twenty_char_names_list)
    def test_create_orgs_20_char_mix(self, twenty_char_names):
        """
        REST API: http://<gateway>/api/v2/orgs
        METHOD: POST
        tests org name containing 20 mix characters can be created and persisted in the etcd store.
        """
        self.run_tests('test_create_orgs_20_char_mix ', twenty_char_names)

    @pytest.mark.parametrize('forty_char_names', forty_char_names_list)
    def test_create_orgs_40_char_mix(self, forty_char_names):
        """
        REST API: http://<gateway>/api/v2/orgs
        METHOD: POST
        tests org name containing 40 mix characters can be created and persisted in the etcd store.
        """
        self.run_tests('test_create_orgs_40_char_mix ', forty_char_names)

    @pytest.mark.parametrize('special_char', special_char)
    def test_create_orgs_special_chars(self, special_char):
        """
        REST API: http://<gateway>/api/v2/orgs
        METHOD: POST
        tests org name containing special characters can be created and persisted in the etcd store.
        """
        self.run_tests('test_create_users_special_chars ', special_char)

    # TODO modify test: should be able to create duplicate org
    def test_create_duplicate_org(self):
        """
        REST API: http://<gateway>/api/v2/orgs
        METHOD: POST
        tests cannot create org with already existing name.
        """
        test_name = 'test_create_duplicate_org '
        org_name = 'duporgname'
        self.header(test_name)
        self.mylog.info(test_name + ' STEP 1: Create Organization %s' % org_name)
        create_result = org_util.create_organization(self, self.gateway, org_name)
        status = create_result['status']
        created_org_id = create_result['org_id']
        created_org_name = create_result['org_name']
        _assert(self, status, 201, 'status code')

        self.mylog.info(test_name + 'STEP 2: Verify data was persisted in the etcd store')
        verify_org_etcd_entries(self, test_name, created_org_id, created_org_name, '')

        self.mylog.info(test_name + 'STEP 3: Creating org with the same name')
        # TODO: According to @goller multiple organizations with the same name could be created,
        # TODO: but with different ids, but currently it does not work
        # TODO: filed a bug(gshif)
        create_result = org_util.create_organization(self, self.gateway, org_name)
        status = create_result['status']
        _assert(self, status, 201, 'status code', xfail=True, reason='cannot create org with the same name')
        self.footer(test_name)

    @pytest.mark.parametrize('two_hundred_char_names', two_hundred_char_name_list)
    def test_create_orgs_200_char_mix(self, two_hundred_char_names):
        """
        REST API: http://<gateway>/api/v2/orgs
        METHOD: POST
        tests org name containing 200 mix characters can be created and persisted in the etcd store.
        """
        self.run_tests('test_create_orgs_200_char_mix ', two_hundred_char_names)

    @pytest.mark.parametrize('four_hundred_char_names', four_hundred_char_name_list)
    def test_create_orgs_400_char_mix(self, four_hundred_char_names):
        """
        REST API: http://<gateway>/api/v2/orgs
        METHOD: POST
        tests org name containing 400 mix characters can be created and persisted in the etcd store.
        """
        self.run_tests('test_create_orgs_400_char_mix ', four_hundred_char_names)
