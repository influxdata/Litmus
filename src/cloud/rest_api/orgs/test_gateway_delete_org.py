
import pytest
import src.util.login_util as lu
from src.chronograf.lib import chronograf_rest_lib as crl
from src.util import gateway_util
from random import choice

from string import ascii_lowercase
from string import ascii_uppercase
from string import digits
from src.cloud.rest_api.conftest import nonalphanumeric, twenty_char_names_list, four_hundred_char_name_list

@pytest.mark.usefixtures('remove_orgs','gateway')
class TestDeleteOrganizationsAPI(object):
    '''
    Test Suite for testing REST API endpoint to delete organizations.
    The existing orgs would be removed before running tests.
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

    def run_tests(self, name_of_the_test_to_run, org_name=None, expected_error='', org_id=None):
        '''

        '''
        if org_name == '':
            test_name = name_of_the_test_to_run + 'empty org name '
        elif org_name == None:
            test_name = name_of_the_test_to_run
        else:
            test_name = name_of_the_test_to_run + org_name + ' '
        self.header(test_name)
        if org_id is None:
            self.mylog.info(test_name + ' STEP 1: Create Organization "%s"' % org_name)
            status, created_org_id, created_org_name, error_message = \
                    gateway_util.create_organization(self, self.gateway, org_name)
            # according to Chris Goller the name of the org can be an empty string, but currently it is returns an error
            if org_name == '':
                assert status == 404, \
                    pytest.xfail(reason='https://github.com/influxdata/platform/issues/162')
            elif org_name == 'BackSlash\\':
                assert status == 201, \
                    pytest.xfail(reason='https://github.com/influxdata/platform/issues/163')
            else:
                assert status == 201, \
                    self.mylog.info(test_name + 'Assertion Failed, status=%s' % status)
            self.mylog.info(test_name + ' STEP 2: Delete Organization with \'%s\' id' % created_org_id)
            status, error = gateway_util.delete_organization(self, self.gateway, created_org_id)
            assert status == 202, self.mylog.info(test_name + 'Assertion Error')
            assert error == '', self.mylog.info(test_name + 'Assertion Error')
        else:
            # Do not create Organization, this is just to pass an org_id to the delete API
            self.mylog.info(test_name + ' STEP 1: Delete Organization with \'%s\' id' % org_id)
            status, error = gateway_util.delete_organization(self, self.gateway, org_id)
            #TODO to change status to the one other then current 500, when it is fixed.
            assert status != 202, self.mylog.info(test_name + 'Assertion Error, status is \'%s\'' % status)
            assert error == expected_error, self.mylog.info(test_name + 'Assertion Error, error message is wrong')
        #TODO need to add a check of etcd store to ensure org records were deleted.
        self.footer(test_name)


    def test_delete_org_id_odd_length(self):
        '''
        REST API: http://<gateway>/v1/orgs/aff
        METHOD: DELETE
        tests API will return an error if org_id has an odd length
        '''
        self.run_tests('test_delete_org_id_odd_length ',
                       expected_error='encoding/hex: odd length hex string', org_id='aff')

    def test_delete_org_id_invalid_byte(self):
        '''
        REST API: http://<gateway>/v1/orgs/aff
        METHOD: DELETE
        tests API will return an error if org_id has an invalid byte
        '''
        self.run_tests('test_delete_org_id_invalid_byte ',
                       expected_error='encoding/hex: invalid byte: U+0073 \'s\'', org_id='assdff')

    def test_delete_org_id_does_not_exist(self):
        '''
        REST API: http://<gateway>/v1/orgs/1234567890
        METHOD: DELETE
        tests API will return an error if org_id does not exist in etcd store, but is valid
        '''
        self.run_tests('test_delete_org_id_does_not_exist ',
                       expected_error='organization not found', org_id='1234567890')

    def test_delete_org_id_missing(self):
        '''
        REST API: http://<gateway>/v1/orgs/
        METHOD: DELETE
        tests API will return an error if org_id is missing
        '''
        self.run_tests('test_delete_org_id_missing ', expected_error='', org_id='')

    @pytest.mark.parametrize('single_char', [choice(ascii_lowercase), choice(ascii_uppercase), choice(digits),
                                             choice(nonalphanumeric)])
    def test_delete_empty_org_single_char_name(self, single_char):
        '''
        REST API: http://<gateway>/v1/orgs/<org_id>
        METHOD: DELETE
        tests API will successfully remove organization records from etcd store
        '''
        self.run_tests('test_delete_empty_org_single_char_name ', org_name=single_char)

    @pytest.mark.parametrize('twenty_mix_chars', twenty_char_names_list)
    def test_delete_empty_org_20_mix_char_name(self, twenty_mix_chars):
        '''
        REST API: http://<gateway>/v1/orgs/<org_id>
        METHOD: DELETE
        tests API will successfully remove organization records from etcd store when org name is 20 characters long
        '''
        self.run_tests('test_delete_empty_org_20_mix_char_name ', org_name=twenty_mix_chars)

    @pytest.mark.parametrize('four_hundred_char_names', four_hundred_char_name_list)
    def test_delete_empty_org_400_mix_char_name(self, four_hundred_char_names):
        '''
        REST API: http://<gateway>/v1/orgs/<org_id>
        METHOD: DELETE
        tests API will successfully remove organization records from etcd store when org name is 400 characters long
        '''
        self.run_tests('test_delete_empty_org_400_mix_char_name ', org_name=four_hundred_char_names)

