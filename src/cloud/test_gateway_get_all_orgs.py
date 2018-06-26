
import pytest
import src.util.login_util as lu
from src.chronograf.lib import chronograf_rest_lib as crl
from src.util import gateway_util
from conftest import org_names

@pytest.mark.usefixtures('remove_orgs','get_all_setup_orgs')
class TestGetAllOrganizationsAPI(object):
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


    def test_get_all_orgs_count(self):
        '''
        '''
        test_name='test_get_all_orgs_count '
        expected_orgs_count=5
        self.header(test_name)
        self.mylog.info(test_name + 'STEP 1: Get count of all organizations')
        actual_count=gateway_util.get_count_of_orgs(self, self.get_all_setup_orgs)
        self.mylog.info(test_name + 'Actual count of created organizations is ' + str(actual_count))
        self.mylog.info(test_name + 'Assert expected_count ' + str(expected_orgs_count) +
                        ' equals to actual count ' + str(actual_count))
        assert expected_orgs_count == actual_count, self.mylog.info(test_name + 'Assertion failed')
        self.footer(test_name)

    def test_verify_created_orgs(self):
        '''
        '''
        test_name='test_verify_created_orgs '
        self.header(test_name)
        self.mylog.info(test_name + 'STEP 1: find organization by name')
        for name in org_names:
            (org_name, org_id)=gateway_util.find_org_by_name(self, name, self.get_all_setup_orgs)
            self.mylog.info(test_name + 'Assert expected name ' + str(name) + ' equals to actual name ' + str(org_name))
            assert org_name == name, self.mylog.info(test_name + 'Assertion failed')
        self.footer(test_name)

