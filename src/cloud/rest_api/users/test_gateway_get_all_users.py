import pytest
import src.util.login_util as lu
from src.chronograf.lib import chronograf_rest_lib as crl
from src.util import gateway_util
from src.cloud.rest_api.conftest import user_names, _assert


@pytest.mark.usefixtures('remove_users', 'get_all_setup_users')
class TestGetAllUsersAPI(object):
    """
    Test Suite for testing of REST API endpoint to get all of the users
    - Removes all of the created by the tests users
    - Creates N test users
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

    def test_get_all_users_count(self):
        """
        REST API: http://<gateway>/api/v2/users
        METHOD: GET
        tests that the count of the created users equals to expected
        """
        test_name = 'test_get_all_users_count '
        expected_users_count = 10
        self.header(test_name)
        self.mylog.info(test_name + 'STEP 1: Get count of all users')
        actual_count = gateway_util.get_count_of_users(self, self.get_all_setup_users)
        self.mylog.info(test_name + 'Actual count of created users is ' + str(actual_count))
        self.mylog.info(test_name + 'Assert actual user_count \'%s\' equals to expected user_count \'%s\''
                        % (actual_count, expected_users_count))
        _assert(self, actual_count, expected_users_count, 'user count')
        self.footer(test_name)

    def test_verify_created_users(self):
        """
        REST API: http://<gateway>/api/v2/users
        METHOD: GET
        tests that created user can be found in the list of all users returned by the 'get all users' endpoint
        """
        test_name = 'test_verify_created_users '
        self.header(test_name)
        self.mylog.info(test_name + 'STEP 1: find users by name')
        for name in user_names:
            success = gateway_util.find_user_by_name(self, name, self.get_all_setup_users)
            _assert(self, success, True, 'find user by name')
        self.footer(test_name)
