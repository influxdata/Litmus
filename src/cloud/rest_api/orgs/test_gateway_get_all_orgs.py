import pytest
import src.util.login_util as lu
from src.chronograf.lib import chronograf_rest_lib as crl
from src.util.twodotoh import org_util
from src.cloud.rest_api.conftest import org_names, _assert


@pytest.mark.usefixtures('remove_orgs', 'remove_buckets', 'get_all_setup_orgs')
class TestGetAllOrganizationsAPI(object):
    """
    Test Suite for testing of REST API endpoint to get all of the orgs
    - Removes all of the created by the tests orgs
    - Creates 5 test organizations
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

    def test_get_all_orgs_count(self):
        """
        REST API: http://<gateway>/api/v2/orgs
        METHOD: GET
        tests that the count of the created orgs equals to expected
        """
        test_name = 'test_get_all_orgs_count '
        expected_orgs_count = 5
        self.header(test_name)
        self.mylog.info(test_name + 'STEP 1: Get count of all organizations')
        actual_count = org_util.get_count_of_orgs(self, self.get_all_setup_orgs)
        self.mylog.info(test_name + 'Actual count of created organizations is ' + str(actual_count))
        self.mylog.info(test_name + 'Assert expected_count ' + str(expected_orgs_count) +
                        ' equals to actual count ' + str(actual_count))
        _assert(self, actual_count, expected_orgs_count, 'orgs count')
        self.footer(test_name)

    def test_verify_created_orgs(self):
        """
        REST API: http://<gateway>/api/v2/orgs
        METHOD: GET
        tests that created org can be found in the list of all orgs returned by the 'get all orgs' endpoint
        """
        test_name = 'test_verify_created_orgs '
        self.header(test_name)
        self.mylog.info(test_name + 'STEP 1: find organization by name')
        for name in org_names:
            org_name, org_id = org_util.find_org_by_name(self, name, self.get_all_setup_orgs)
            self.mylog.info(test_name + 'Assert expected name ' + str(name) + ' equals to actual name ' + str(org_name))
            _assert(self, org_name, name, 'org name')
        self.footer(test_name)
