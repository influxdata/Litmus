
import pytest
import src.util.login_util as lu
from src.chronograf.lib import chronograf_rest_lib as crl
from random import sample
from random import shuffle
import src.util.litmus_utils as litmus_utils
import ast # for converting string of dictionary into dictionary
import json
from string import digits as numbers # 0123456789
from string import ascii_lowercase  as lc #abcdefghijklmnopqrstuvwxyz
from string import ascii_uppercase as uc #ABCDEFGHIJKLMNOPQRSTUVWXYZ
from string import hexdigits
import src.util.gateway_util as gateway_util

@pytest.mark.usefixtures('remove_orgs','gateway')
class TestUpdateOrganizationsAPI(object):
    '''
    '''
    mylog=lu.log(lu.get_log_path(), 'w', __name__)
    rl=crl.RestLib(mylog)
    create_org_path='/v1/orgs'
    # to install etcdctl tool on mac we need to install etcd : brew install etcd
    # for ubuntu run :
    # 1. curl -L  https://github.com/coreos/etcd/releases/download/v2.1.0-rc.0/etcd-v2.1.0-rc.0-linux-amd64.tar.gz -o etcd-v2.1.0-rc.0-linux-amd64.tar.gz
    # 2. tar xzvf etcd-v2.1.0-rc.0-linux-amd64.tar.gz
    # 3. etcdctl could be found in /tmp/etcd-v2.1.0-rc.0-linux-amd64, copy to /usr/local/bin
    etcdctl='ETCDCTL_API=3 /usr/local/bin/etcdctl'

    nonalphanumeric='!@#$%^*><&()_+{}[]|,.~/`? ' # removed \, ' and " character

    # lower case characters
    ten_char_lc=[''.join(sample(lc, 10)) for i in range(10)]
    twenty_char_lc=[''.join(sample(lc, 20)) for i in range(10)]
    # upper case characters
    ten_char_uc=[''.join(sample(uc, 10)) for i in range(10)]
    twenty_char_uc=[''.join(sample(uc, 20)) for i in range(10)]
    # non-alphanumeric characters
    ten_char_nonalphanumeric=[''.join(sample(nonalphanumeric, 10)) for i in range(10)]
    twenty_char_nonalphanumeric=[''.join(sample(nonalphanumeric, 15)) for i in range(10)]
    # numbers
    ten_char_numbers=[''.join(sample(numbers,10)) for i in range(10)]
    twenty_char_numbers=[''.join(sample(numbers, 5)) for i in range(10)]

    twenty_char_names_list=[]
    for i in range(10):
        twenty_char_names=sample(nonalphanumeric,5)+sample(lc,5)+sample(uc,5)+sample(numbers,5)
        shuffle(twenty_char_names)
        twenty_char_names_list.append(''.join(twenty_char_names))
    fourty_char_names_list = []
    for i in range(10):
        fourty_char_names = sample(nonalphanumeric, 10) + sample(lc, 10) + sample(uc, 10) + sample(numbers, 10)
        shuffle(fourty_char_names)
        fourty_char_names_list.append(''.join(fourty_char_names))

    def header(self, test_name):
        self.mylog.info('#######################################################')
        self.mylog.info('<--------------- %s START --------------->' % test_name)
        self.mylog.info('#######################################################')

    def footer(self, test_name):
        self.mylog.info('#######################################################')
        self.mylog.info('<--------------- %s END --------------->' % test_name)
        self.mylog.info('#######################################################')
        self.mylog.info('')

    ############################################
    #       Lower Case Character Org Names     #
    ############################################
    #@pytest.mark.skip
    @pytest.mark.parametrize('one_char', lc)
    def test_update_orgs_single_char_lower_case(self, one_char):
        '''

        '''
        test_name='test_create_org_single_char_lower_case_' + one_char + ' '
        new_name=one_char+'_updated_name'
        self.header(test_name)
        self.mylog.info(test_name + ' STEP 1: Create Organization')
        (status, id, name)=gateway_util.create_organization(self, self.gateway, one_char)
        assert status == 201, self.mylog.info(test_name + ' Assertion Failed. Status code is not 201')

        self.mylog.info(test_name + ' STEP 2: Update created Organization with the \'%s\' name' % new_name)
        (status, new_id, updated_name) = gateway_util.update_organization(self, self.gateway, id, new_name)
        assert status == 200, self.mylog.info(test_name + 'Assertion Failed. Status code is not 200')
        assert new_id == id, self.mylog.info(test_name + 'Assertion Failed. New id is not equal original id')
        assert updated_name == new_name, self.mylog.info(
            test_name + 'Assertion Failed. Updated name is not equal expected name')

        self.mylog.info(test_name + ' STEP 3: Check the organization data was persisted in etcd')
        cmd='%s --endpoints %s get --prefix "Organizationv1/%s" --print-value-only' % (self.etcdctl, self.etcd, id)
        out=litmus_utils.execCmd(self, cmd, status='OUT_STATUS')
        actual_org_id=ast.literal_eval(out[0]).get('id')
        self.mylog.info(test_name + 'Assert expected org_id ' + str(new_id) + ' equals actual org id ' + str(actual_org_id))
        assert new_id == actual_org_id, self.mylog.info(test_name + ' Expected org id is not equal to actual org id')
        actual_org_name=ast.literal_eval(out[0]).get('name')
        self.mylog.info(test_name + 'Assert expected org_name ' + str(updated_name) + ' equals actual org name '
                        + str(actual_org_name))
        assert updated_name == actual_org_name, \
            self.mylog.info(test_name + ' Expected org name is not equal to actual org name')
        self.footer(test_name)

    #@pytest.mark.skip
    @pytest.mark.parametrize('ten_char_lc', ten_char_lc)
    def test_update_orgs_10_char_lower_case(self, ten_char_lc):
        '''

        '''
        test_name = 'test_update_org_10_char_lower_case_' + ten_char_lc + ' '
        new_name = ten_char_lc + '_updated_name'
        self.header(test_name)
        self.mylog.info(test_name + ' STEP 1: Create Organization')
        (status, id, name) = gateway_util.create_organization(self, self.gateway, ten_char_lc)
        assert status == 201, self.mylog.info(test_name + ' Assertion Failed. Status code is not 201')

        self.mylog.info(test_name + ' STEP 2: Update created Organization with the \'%s\' name' % new_name)
        (status, new_id, updated_name) = gateway_util.update_organization(self, self.gateway, id, new_name)
        assert status == 200, self.mylog.info(test_name + 'Assertion Failed. Status code is not 200')
        assert new_id == id, self.mylog.info(test_name + 'Assertion Failed. New id is not equal original id')
        assert updated_name == new_name, self.mylog.info(
            test_name + 'Assertion Failed. Updated name is not equal expected name')

        self.mylog.info(test_name + ' STEP 3: Check the organization data was persisted in etcd')
        cmd = '%s --endpoints %s get --prefix "Organizationv1/%s" --print-value-only' % (self.etcdctl, self.etcd, id)
        out = litmus_utils.execCmd(self, cmd, status='OUT_STATUS')
        actual_org_id = ast.literal_eval(out[0]).get('id')
        self.mylog.info(
            test_name + 'Assert expected org_id ' + str(new_id) + ' equals actual org id ' + str(actual_org_id))
        assert new_id == actual_org_id, self.mylog.info(test_name + ' Expected org id is not equal to actual org id')
        actual_org_name = ast.literal_eval(out[0]).get('name')
        self.mylog.info(test_name + 'Assert expected org_name ' + str(updated_name) + ' equals actual org name '
                        + str(actual_org_name))
        assert updated_name == actual_org_name, \
            self.mylog.info(test_name + ' Expected org name is not equal to actual org name')
        self.footer(test_name)

    #@pytest.mark.skip
    @pytest.mark.parametrize('twenty_char_lc', twenty_char_lc)
    def test_update_orgs_20_char_lower_case(self, twenty_char_lc):
        '''
        :param ten_char_lc:
        :return:
        '''
        test_name = 'test_update_org_20_char_lower_case_' + twenty_char_lc + ' '
        new_name = twenty_char_lc + '_updated_name'
        self.header(test_name)
        self.mylog.info(test_name + ' STEP 1: Create Organization')
        (status, id, name) = gateway_util.create_organization(self, self.gateway, twenty_char_lc)
        assert status == 201, self.mylog.info(test_name + ' Assertion Failed. Status code is not 201')

        self.mylog.info(test_name + ' STEP 2: Update created Organization with the \'%s\' name' % new_name)
        (status, new_id, updated_name) = gateway_util.update_organization(self, self.gateway, id, new_name)
        assert status == 200, self.mylog.info(test_name + 'Assertion Failed. Status code is not 200')
        assert new_id == id, self.mylog.info(test_name + 'Assertion Failed. New id is not equal original id')
        assert updated_name == new_name, self.mylog.info(
            test_name + 'Assertion Failed. Updated name is not equal expected name')

        self.mylog.info(test_name + ' STEP 3: Check the organization data was persisted in etcd')
        cmd = '%s --endpoints %s get --prefix "Organizationv1/%s" --print-value-only' % (self.etcdctl, self.etcd, id)
        out = litmus_utils.execCmd(self, cmd, status='OUT_STATUS')
        actual_org_id = ast.literal_eval(out[0]).get('id')
        self.mylog.info(
            test_name + 'Assert expected org_id ' + str(new_id) + ' equals actual org id ' + str(actual_org_id))
        assert new_id == actual_org_id, self.mylog.info(test_name + ' Expected org id is not equal to actual org id')
        actual_org_name = ast.literal_eval(out[0]).get('name')
        self.mylog.info(test_name + 'Assert expected org_name ' + str(updated_name) + ' equals actual org name '
                        + str(actual_org_name))
        assert updated_name == actual_org_name, \
            self.mylog.info(test_name + ' Expected org name is not equal to actual org name')
        self.footer(test_name)
        self.footer(test_name)

    ###################################################
    #          Upper Case Character Org Names         #
    ###################################################
    #@pytest.mark.skip
    @pytest.mark.parametrize('one_char', uc)
    def test_update_orgs_single_char_upper_case(self, one_char):
        '''
        :return:
        '''
        test_name = 'test_update_org_single_char_upper_case_' + one_char + ' '
        new_name = one_char + '_updated_name'
        self.header(test_name)
        self.mylog.info(test_name + ' STEP 1: Create Organization')
        (status, id, name) = gateway_util.create_organization(self, self.gateway, one_char)
        assert status == 201, self.mylog.info(test_name + ' Assertion Failed. Status code is not 201')

        self.mylog.info(test_name + ' STEP 2: Update created Organization with the \'%s\' name' % new_name)
        (status, new_id, updated_name) = gateway_util.update_organization(self, self.gateway, id, new_name)
        assert status == 200, self.mylog.info(test_name + 'Assertion Failed. Status code is not 200')
        assert new_id == id, self.mylog.info(test_name + 'Assertion Failed. New id is not equal original id')
        assert updated_name == new_name, self.mylog.info(
            test_name + 'Assertion Failed. Updated name is not equal expected name')

        self.mylog.info(test_name + ' STEP 3: Check the organization data was persisted in etcd')
        cmd = '%s --endpoints %s get --prefix "Organizationv1/%s" --print-value-only' % (self.etcdctl, self.etcd, id)
        out = litmus_utils.execCmd(self, cmd, status='OUT_STATUS')
        actual_org_id = ast.literal_eval(out[0]).get('id')
        self.mylog.info(
            test_name + 'Assert expected org_id ' + str(new_id) + ' equals actual org id ' + str(actual_org_id))
        assert new_id == actual_org_id, self.mylog.info(test_name + ' Expected org id is not equal to actual org id')
        actual_org_name = ast.literal_eval(out[0]).get('name')
        self.mylog.info(test_name + 'Assert expected org_name ' + str(updated_name) + ' equals actual org name '
                        + str(actual_org_name))
        assert updated_name == actual_org_name, \
            self.mylog.info(test_name + ' Expected org name is not equal to actual org name')
        self.footer(test_name)

    #@pytest.mark.skip
    @pytest.mark.parametrize('ten_char_uc', ten_char_uc)
    def test_update_orgs_10_char_upper_case(self, ten_char_uc):
        '''
        :param ten_char_lc:
        :return:
        '''
        test_name = 'test_update_orgs_10_char_upper_case_' + ten_char_uc + ' '
        new_name = ten_char_uc + '_updated_name'
        self.header(test_name)
        self.mylog.info(test_name + ' STEP 1: Create Organization')
        (status, id, name) = gateway_util.create_organization(self, self.gateway, ten_char_uc)
        assert status == 201, self.mylog.info(test_name + ' Assertion Failed. Status code is not 201')

        self.mylog.info(test_name + ' STEP 2: Update created Organization with the \'%s\' name' % new_name)
        (status, new_id, updated_name) = gateway_util.update_organization(self, self.gateway, id, new_name)
        assert status == 200, self.mylog.info(test_name + 'Assertion Failed. Status code is not 200')
        assert new_id == id, self.mylog.info(test_name + 'Assertion Failed. New id is not equal original id')
        assert updated_name == new_name, self.mylog.info(
            test_name + 'Assertion Failed. Updated name is not equal expected name')

        self.mylog.info(test_name + ' STEP 3: Check the organization data was persisted in etcd')
        cmd = '%s --endpoints %s get --prefix "Organizationv1/%s" --print-value-only' % (self.etcdctl, self.etcd, id)
        out = litmus_utils.execCmd(self, cmd, status='OUT_STATUS')
        actual_org_id = ast.literal_eval(out[0]).get('id')
        self.mylog.info(
            test_name + 'Assert expected org_id ' + str(new_id) + ' equals actual org id ' + str(actual_org_id))
        assert new_id == actual_org_id, self.mylog.info(test_name + ' Expected org id is not equal to actual org id')
        actual_org_name = ast.literal_eval(out[0]).get('name')
        self.mylog.info(test_name + 'Assert expected org_name ' + str(updated_name) + ' equals actual org name '
                        + str(actual_org_name))
        assert updated_name == actual_org_name, \
            self.mylog.info(test_name + ' Expected org name is not equal to actual org name')
        self.footer(test_name)

    #@pytest.mark.skip
    @pytest.mark.parametrize('twenty_char_uc', twenty_char_uc)
    def test_update_orgs_20_char_upper_case(self, twenty_char_uc):
        '''
        :param ten_char_lc:
        :return:
        '''
        test_name = 'test_update_org_single_char_upper_case_' + twenty_char_uc + ' '
        new_name = twenty_char_uc + '_updated_name'
        self.header(test_name)
        self.mylog.info(test_name + ' STEP 1: Create Organization')
        (status, id, name) = gateway_util.create_organization(self, self.gateway, twenty_char_uc)
        assert status == 201, self.mylog.info(test_name + ' Assertion Failed. Status code is not 201')

        self.mylog.info(test_name + ' STEP 2: Update created Organization with the \'%s\' name' % new_name)
        (status, new_id, updated_name) = gateway_util.update_organization(self, self.gateway, id, new_name)
        assert status == 200, self.mylog.info(test_name + 'Assertion Failed. Status code is not 200')
        assert new_id == id, self.mylog.info(test_name + 'Assertion Failed. New id is not equal original id')
        assert updated_name == new_name, self.mylog.info(
            test_name + 'Assertion Failed. Updated name is not equal expected name')

        self.mylog.info(test_name + ' STEP 3: Check the organization data was persisted in etcd')
        cmd = '%s --endpoints %s get --prefix "Organizationv1/%s" --print-value-only' % (self.etcdctl, self.etcd, id)
        out = litmus_utils.execCmd(self, cmd, status='OUT_STATUS')
        actual_org_id = ast.literal_eval(out[0]).get('id')
        self.mylog.info(
            test_name + 'Assert expected org_id ' + str(new_id) + ' equals actual org id ' + str(actual_org_id))
        assert new_id == actual_org_id, self.mylog.info(test_name + ' Expected org id is not equal to actual org id')
        actual_org_name = ast.literal_eval(out[0]).get('name')
        self.mylog.info(test_name + 'Assert expected org_name ' + str(updated_name) + ' equals actual org name '
                        + str(actual_org_name))
        assert updated_name == actual_org_name, \
            self.mylog.info(test_name + ' Expected org name is not equal to actual org name')
        self.footer(test_name)

    #########################################################
    #          Non-alphanumeric Character Org Names         #
    #########################################################
    #@pytest.mark.skip
    @pytest.mark.parametrize('one_char', nonalphanumeric)
    def test_update_orgs_single_char_nonalphanumeric_case(self, one_char):
        '''
        :return:
        '''
        test_name = 'test_update_orgs_single_nonalphanumeric_case_' + one_char + ' '
        new_name = one_char + '_updated_name'
        self.header(test_name)
        self.mylog.info(test_name + ' STEP 1: Create Organization')
        (status, id, name) = gateway_util.create_organization(self, self.gateway, one_char)
        assert status == 201, self.mylog.info(test_name + ' Assertion Failed. Status code is not 201')

        self.mylog.info(test_name + ' STEP 2: Update created Organization with the \'%s\' name' % new_name)
        (status, new_id, updated_name) = gateway_util.update_organization(self, self.gateway, id, new_name)
        assert status == 200, self.mylog.info(test_name + 'Assertion Failed. Status code is not 200')
        assert new_id == id, self.mylog.info(test_name + 'Assertion Failed. New id is not equal original id')
        assert updated_name == new_name, self.mylog.info(
            test_name + 'Assertion Failed. Updated name is not equal expected name')

        self.mylog.info(test_name + ' STEP 3: Check the organization data was persisted in etcd')
        cmd = '%s --endpoints %s get --prefix "Organizationv1/%s" --print-value-only' % (self.etcdctl, self.etcd, id)
        out = litmus_utils.execCmd(self, cmd, status='OUT_STATUS')
        actual_org_id = ast.literal_eval(out[0]).get('id')
        self.mylog.info(
            test_name + 'Assert expected org_id ' + str(new_id) + ' equals actual org id ' + str(actual_org_id))
        assert new_id == actual_org_id, self.mylog.info(test_name + ' Expected org id is not equal to actual org id')
        if one_char in ['<', '>', '&']:
            actual_org_name=ast.literal_eval(out[0]).get('name')
            self.mylog.info(test_name + 'org name before decosing = ' + str(actual_org_name))
            actual_org_name=json.loads("\"" + actual_org_name + "\"")
            self.mylog.info(test_name + 'org name after decoding = ' + str(actual_org_name))
        else:
            actual_org_name=ast.literal_eval(out[0]).get('name')
        self.mylog.info(test_name + 'Assert expected org_name ' + str(updated_name) +
                        ' equals actual org name ' + str(actual_org_name))
        assert updated_name == actual_org_name, self.mylog.info(test_name + ' Expected org name is not equal to actual org name')
        self.footer(test_name)

    #@pytest.mark.skip
    @pytest.mark.parametrize('ten_char_nonalphanumeric', ten_char_nonalphanumeric)
    def test_update_orgs_10_char_nonalphanumeric_case(self, ten_char_nonalphanumeric):
        '''
        :return:
        '''
        test_name = 'test_update_orgs_10_char_nonalphanumeric_case_' + ten_char_nonalphanumeric + ' '
        new_name = ten_char_nonalphanumeric + '_updated_name'
        self.header(test_name)
        self.mylog.info(test_name + ' STEP 1: Create Organization')
        (status, id, name) = gateway_util.create_organization(self, self.gateway, ten_char_nonalphanumeric)
        assert status == 201, self.mylog.info(test_name + ' Assertion Failed. Status code is not 201')

        self.mylog.info(test_name + ' STEP 2: Update created Organization with the \'%s\' name' % new_name)
        (status, new_id, updated_name) = gateway_util.update_organization(self, self.gateway, id, new_name)
        assert status == 200, self.mylog.info(test_name + 'Assertion Failed. Status code is not 200')
        assert new_id == id, self.mylog.info(test_name + 'Assertion Failed. New id is not equal original id')
        assert updated_name == new_name, self.mylog.info(
            test_name + 'Assertion Failed. Updated name is not equal expected name')

        self.mylog.info(test_name + ' STEP 3: Check the organization data was persisted in etcd')
        cmd = '%s --endpoints %s get --prefix "Organizationv1/%s" --print-value-only' % (self.etcdctl, self.etcd, id)
        out = litmus_utils.execCmd(self, cmd, status='OUT_STATUS')
        actual_org_id = ast.literal_eval(out[0]).get('id')
        self.mylog.info(
            test_name + 'Assert expected org_id ' + str(new_id) + ' equals actual org id ' + str(actual_org_id))
        assert new_id == actual_org_id, self.mylog.info(test_name + ' Expected org id is not equal to actual org id')
        actual_org_name = ast.literal_eval(out[0]).get('name')
        self.mylog.info(test_name + 'org name before decosing = ' + str(actual_org_name))
        actual_org_name = json.loads("\"" + actual_org_name + "\"")
        self.mylog.info(test_name + 'org name after decoding = ' + str(actual_org_name))
        self.mylog.info(test_name + 'Assert expected org_name ' + str(updated_name) +
                        ' equals actual org name ' + str(actual_org_name))
        assert updated_name == actual_org_name, self.mylog.info(
            test_name + ' Expected org name is not equal to actual org name')
        self.footer(test_name)

    #@pytest.mark.skip
    @pytest.mark.parametrize('twenty_char_nonalphanumeric', twenty_char_nonalphanumeric)
    def test_update_orgs_15_char_nonalphanumeric_case(self, twenty_char_nonalphanumeric):
        '''
        :return:
        '''
        test_name = 'test_update_orgs_15_char_nonalphanumeric_case_' + twenty_char_nonalphanumeric + ' '
        new_name = twenty_char_nonalphanumeric + '_updated_name'
        self.header(test_name)
        self.mylog.info(test_name + ' STEP 1: Create Organization')
        (status, id, name) = gateway_util.create_organization(self, self.gateway, twenty_char_nonalphanumeric)
        assert status == 201, self.mylog.info(test_name + ' Assertion Failed. Status code is not 201')

        self.mylog.info(test_name + ' STEP 2: Update created Organization with the \'%s\' name' % new_name)
        (status, new_id, updated_name) = gateway_util.update_organization(self, self.gateway, id, new_name)
        assert status == 200, self.mylog.info(test_name + 'Assertion Failed. Status code is not 200')
        assert new_id == id, self.mylog.info(test_name + 'Assertion Failed. New id is not equal original id')
        assert updated_name == new_name, self.mylog.info(
            test_name + 'Assertion Failed. Updated name is not equal expected name')

        self.mylog.info(test_name + ' STEP 3: Check the organization data was persisted in etcd')
        cmd = '%s --endpoints %s get --prefix "Organizationv1/%s" --print-value-only' % (self.etcdctl, self.etcd, id)
        out = litmus_utils.execCmd(self, cmd, status='OUT_STATUS')
        actual_org_id = ast.literal_eval(out[0]).get('id')
        self.mylog.info(
            test_name + 'Assert expected org_id ' + str(new_id) + ' equals actual org id ' + str(actual_org_id))
        assert new_id == actual_org_id, self.mylog.info(test_name + ' Expected org id is not equal to actual org id')
        actual_org_name = ast.literal_eval(out[0]).get('name')
        self.mylog.info(test_name + 'org name before decosing = ' + str(actual_org_name))
        actual_org_name = json.loads("\"" + actual_org_name + "\"")
        self.mylog.info(test_name + 'org name after decoding = ' + str(actual_org_name))
        self.mylog.info(test_name + 'Assert expected org_name ' + str(updated_name) +
                        ' equals actual org name ' + str(actual_org_name))
        assert updated_name == actual_org_name, self.mylog.info(
            test_name + ' Expected org name is not equal to actual org name')
        self.footer(test_name)

    #################################################
    #          Number Characters Org Names          #
    #################################################
    #@pytest.mark.skip
    @pytest.mark.parametrize('one_char', numbers)
    def test_update_orgs_single_char_numbers(self, one_char):
        '''
        :return:
        '''
        test_name = 'test_update_org_single_char_numbers_' + one_char + ' '
        new_name = one_char + '_updated_name'
        self.header(test_name)
        self.mylog.info(test_name + ' STEP 1: Create Organization')
        (status, id, name) = gateway_util.create_organization(self, self.gateway, one_char)
        assert status == 201, self.mylog.info(test_name + ' Assertion Failed. Status code is not 201')

        self.mylog.info(test_name + ' STEP 2: Update created Organization with the \'%s\' name' % new_name)
        (status, new_id, updated_name) = gateway_util.update_organization(self, self.gateway, id, new_name)
        assert status == 200, self.mylog.info(test_name + 'Assertion Failed. Status code is not 200')
        assert new_id == id, self.mylog.info(test_name + 'Assertion Failed. New id is not equal original id')
        assert updated_name == new_name, self.mylog.info(
            test_name + 'Assertion Failed. Updated name is not equal expected name')

        self.mylog.info(test_name + ' STEP 3: Check the organization data was persisted in etcd')
        cmd = '%s --endpoints %s get --prefix "Organizationv1/%s" --print-value-only' % (self.etcdctl, self.etcd, id)
        out = litmus_utils.execCmd(self, cmd, status='OUT_STATUS')
        actual_org_id = ast.literal_eval(out[0]).get('id')
        self.mylog.info(
            test_name + 'Assert expected org_id ' + str(new_id) + ' equals actual org id ' + str(actual_org_id))
        assert new_id == actual_org_id, self.mylog.info(test_name + ' Expected org id is not equal to actual org id')
        actual_org_name = ast.literal_eval(out[0]).get('name')
        self.mylog.info(test_name + 'Assert expected org_name ' + str(updated_name) + ' equals actual org name '
                        + str(actual_org_name))
        assert updated_name == actual_org_name, \
            self.mylog.info(test_name + ' Expected org name is not equal to actual org name')
        self.footer(test_name)

    #@pytest.mark.skip
    @pytest.mark.parametrize('ten_char_numbers', ten_char_numbers)
    def test_update_orgs_10_char_numbers(self, ten_char_numbers):
        '''
        :param ten_char_numbers:
        :return:
        '''
        test_name = 'test_update_org_single_char_lower_case_' + ten_char_numbers + ' '
        new_name = ten_char_numbers + '_updated_name'
        self.header(test_name)
        self.mylog.info(test_name + ' STEP 1: Create Organization')
        (status, id, name) = gateway_util.create_organization(self, self.gateway, ten_char_numbers)
        assert status == 201, self.mylog.info(test_name + ' Assertion Failed. Status code is not 201')

        self.mylog.info(test_name + ' STEP 2: Update created Organization with the \'%s\' name' % new_name)
        (status, new_id, updated_name) = gateway_util.update_organization(self, self.gateway, id, new_name)
        assert status == 200, self.mylog.info(test_name + 'Assertion Failed. Status code is not 200')
        assert new_id == id, self.mylog.info(test_name + 'Assertion Failed. New id is not equal original id')
        assert updated_name == new_name, self.mylog.info(
            test_name + 'Assertion Failed. Updated name is not equal expected name')

        self.mylog.info(test_name + ' STEP 3: Check the organization data was persisted in etcd')
        cmd = '%s --endpoints %s get --prefix "Organizationv1/%s" --print-value-only' % (self.etcdctl, self.etcd, id)
        out = litmus_utils.execCmd(self, cmd, status='OUT_STATUS')
        actual_org_id = ast.literal_eval(out[0]).get('id')
        self.mylog.info(
            test_name + 'Assert expected org_id ' + str(new_id) + ' equals actual org id ' + str(actual_org_id))
        assert new_id == actual_org_id, self.mylog.info(test_name + ' Expected org id is not equal to actual org id')
        actual_org_name = ast.literal_eval(out[0]).get('name')
        self.mylog.info(test_name + 'Assert expected org_name ' + str(updated_name) + ' equals actual org name '
                        + str(actual_org_name))
        assert updated_name == actual_org_name, \
            self.mylog.info(test_name + ' Expected org name is not equal to actual org name')
        self.footer(test_name)
        self.footer(test_name)

    #@pytest.mark.skip
    @pytest.mark.parametrize('twenty_char_numbers', twenty_char_numbers)
    def test_update_orgs_5_char_numbers(self, twenty_char_numbers):
        '''
        :param twenty_char_numbers:
        :return:
        '''
        test_name = 'test_update_org_single_char_lower_case_' + twenty_char_numbers + ' '
        new_name = twenty_char_numbers + '_updated_name'
        self.header(test_name)
        self.mylog.info(test_name + ' STEP 1: Create Organization')
        (status, id, name) = gateway_util.create_organization(self, self.gateway, twenty_char_numbers)
        assert status == 201, self.mylog.info(test_name + ' Assertion Failed. Status code is not 201')

        self.mylog.info(test_name + ' STEP 2: Update created Organization with the \'%s\' name' % new_name)
        (status, new_id, updated_name) = gateway_util.update_organization(self, self.gateway, id, new_name)
        assert status == 200, self.mylog.info(test_name + 'Assertion Failed. Status code is not 200')
        assert new_id == id, self.mylog.info(test_name + 'Assertion Failed. New id is not equal original id')
        assert updated_name == new_name, self.mylog.info(
            test_name + 'Assertion Failed. Updated name is not equal expected name')

        self.mylog.info(test_name + ' STEP 3: Check the organization data was persisted in etcd')
        cmd = '%s --endpoints %s get --prefix "Organizationv1/%s" --print-value-only' % (self.etcdctl, self.etcd, id)
        out = litmus_utils.execCmd(self, cmd, status='OUT_STATUS')
        actual_org_id = ast.literal_eval(out[0]).get('id')
        self.mylog.info(
            test_name + 'Assert expected org_id ' + str(new_id) + ' equals actual org id ' + str(actual_org_id))
        assert new_id == actual_org_id, self.mylog.info(test_name + ' Expected org id is not equal to actual org id')
        actual_org_name = ast.literal_eval(out[0]).get('name')
        self.mylog.info(test_name + 'Assert expected org_name ' + str(updated_name) + ' equals actual org name '
                        + str(actual_org_name))
        assert updated_name == actual_org_name, \
            self.mylog.info(test_name + ' Expected org name is not equal to actual org name')
        self.footer(test_name)

    ####################################
    #     Mix Characters Org Names     #
    ####################################
    #@pytest.mark.skip
    @pytest.mark.parametrize('twenty_char_names', twenty_char_names_list)
    def test_update_orgs_20_char_mix(self, twenty_char_names):
        '''
        :param twenty_char_mix:
        :return:
        '''
        test_name = 'test_update_orgs_20_char_mix_' + twenty_char_names + ' '
        new_name = twenty_char_names + '_updated_name'
        self.header(test_name)
        self.mylog.info(test_name + ' STEP 1: Create Organization')
        (status, id, name) = gateway_util.create_organization(self, self.gateway, twenty_char_names)
        assert status == 201, self.mylog.info(test_name + ' Assertion Failed. Status code is not 201')

        self.mylog.info(test_name + ' STEP 2: Update created Organization with the \'%s\' name' % new_name)
        (status, new_id, updated_name) = gateway_util.update_organization(self, self.gateway, id, new_name)
        assert status == 200, self.mylog.info(test_name + 'Assertion Failed. Status code is not 200')
        assert new_id == id, self.mylog.info(test_name + 'Assertion Failed. New id is not equal original id')
        assert updated_name == new_name, self.mylog.info(
            test_name + 'Assertion Failed. Updated name is not equal expected name')

        self.mylog.info(test_name + ' STEP 3: Check the organization data was persisted in etcd')
        cmd = '%s --endpoints %s get --prefix "Organizationv1/%s" --print-value-only' % (self.etcdctl, self.etcd, id)
        out = litmus_utils.execCmd(self, cmd, status='OUT_STATUS')
        actual_org_id = ast.literal_eval(out[0]).get('id')
        self.mylog.info(
            test_name + 'Assert expected org_id ' + str(new_id) + ' equals actual org id ' + str(actual_org_id))
        assert new_id == actual_org_id, self.mylog.info(test_name + ' Expected org id is not equal to actual org id')
        actual_org_name = ast.literal_eval(out[0]).get('name')
        self.mylog.info(test_name + 'org name before decosing = ' + str(actual_org_name))
        actual_org_name = json.loads("\"" + actual_org_name + "\"")
        self.mylog.info(test_name + 'org name after decoding = ' + str(actual_org_name))
        self.mylog.info(test_name + 'Assert expected org_name ' + str(updated_name) +
                        ' equals actual org name ' + str(actual_org_name))
        assert updated_name == actual_org_name, self.mylog.info(
            test_name + ' Expected org name is not equal to actual org name')
        self.footer(test_name)

    #@pytest.mark.skip
    @pytest.mark.parametrize('fourty_char_names', fourty_char_names_list)
    def test_update_orgs_40_char_mix(self, fourty_char_names):
        '''
        :param twenty_char_mix:
        :return:
        '''
        test_name = 'test_update_orgs_40_char_mix_' + fourty_char_names + ' '
        new_name = fourty_char_names + '_updated_name'
        self.header(test_name)
        self.mylog.info(test_name + ' STEP 1: Create Organization')
        (status, id, name) = gateway_util.create_organization(self, self.gateway, fourty_char_names)
        assert status == 201, self.mylog.info(test_name + ' Assertion Failed. Status code is not 201')

        self.mylog.info(test_name + ' STEP 2: Update created Organization with the \'%s\' name' % new_name)
        (status, new_id, updated_name) = gateway_util.update_organization(self, self.gateway, id, new_name)
        assert status == 200, self.mylog.info(test_name + 'Assertion Failed. Status code is not 200')
        assert new_id == id, self.mylog.info(test_name + 'Assertion Failed. New id is not equal original id')
        assert updated_name == new_name, self.mylog.info(
            test_name + 'Assertion Failed. Updated name is not equal expected name')

        self.mylog.info(test_name + ' STEP 3: Check the organization data was persisted in etcd')
        cmd = '%s --endpoints %s get --prefix "Organizationv1/%s" --print-value-only' % (self.etcdctl, self.etcd, id)
        out = litmus_utils.execCmd(self, cmd, status='OUT_STATUS')
        actual_org_id = ast.literal_eval(out[0]).get('id')
        self.mylog.info(
            test_name + 'Assert expected org_id ' + str(new_id) + ' equals actual org id ' + str(actual_org_id))
        assert new_id == actual_org_id, self.mylog.info(test_name + ' Expected org id is not equal to actual org id')
        actual_org_name = ast.literal_eval(out[0]).get('name')
        self.mylog.info(test_name + 'org name before decosing = ' + str(actual_org_name))
        actual_org_name = json.loads("\"" + actual_org_name + "\"")
        self.mylog.info(test_name + 'org name after decoding = ' + str(actual_org_name))
        self.mylog.info(test_name + 'Assert expected org_name ' + str(updated_name) +
                        ' equals actual org name ' + str(actual_org_name))
        assert updated_name == actual_org_name, self.mylog.info(
            test_name + ' Expected org name is not equal to actual org name')
        self.footer(test_name)

    #@pytest.mark.skip
    def test_update_orgs_200_char_mix(self):
        '''
        :param twenty_char_mix:
        :return:
        '''
        test_name = 'test_update_orgs_200_char_mix_'
        new_name = str((hexdigits * 10)) + '_updated_name'
        self.header(test_name)
        self.mylog.info(test_name + ' STEP 1: Create Organization')
        (status, id, name) = gateway_util.create_organization(self, self.gateway, str(hexdigits * 10))
        assert status == 201, self.mylog.info(test_name + ' Assertion Failed. Status code is not 201')

        self.mylog.info(test_name + ' STEP 2: Update created Organization with the \'%s\' name' % new_name)
        (status, new_id, updated_name) = gateway_util.update_organization(self, self.gateway, id, new_name)
        assert status == 200, self.mylog.info(test_name + 'Assertion Failed. Status code is not 200')
        assert new_id == id, self.mylog.info(test_name + 'Assertion Failed. New id is not equal original id')
        assert updated_name == new_name, self.mylog.info(
            test_name + 'Assertion Failed. Updated name is not equal expected name')

        self.mylog.info(test_name + ' STEP 3: Check the organization data was persisted in etcd')
        cmd = '%s --endpoints %s get --prefix "Organizationv1/%s" --print-value-only' % (self.etcdctl, self.etcd, id)
        out = litmus_utils.execCmd(self, cmd, status='OUT_STATUS')
        actual_org_id = ast.literal_eval(out[0]).get('id')
        self.mylog.info(
            test_name + 'Assert expected org_id ' + str(new_id) + ' equals actual org id ' + str(actual_org_id))
        assert new_id == actual_org_id, self.mylog.info(test_name + ' Expected org id is not equal to actual org id')
        actual_org_name = ast.literal_eval(out[0]).get('name')
        self.mylog.info(test_name + 'Assert expected org_name ' + str(updated_name) +
                        ' equals actual org name ' + str(actual_org_name))
        assert updated_name == actual_org_name, self.mylog.info(
            test_name + ' Expected org name is not equal to actual org name')
        self.footer(test_name)

    #@pytest.mark.skip
    def test_update_orgs_400_char_mix(self):
        '''
        '''
        test_name = 'test_update_orgs_400_char_mix_'
        new_name = str((hexdigits * 20)) + '_updated_name'
        self.header(test_name)
        self.mylog.info(test_name + ' STEP 1: Create Organization')
        (status, id, name) = gateway_util.create_organization(self, self.gateway, str(hexdigits * 20))
        assert status == 201, self.mylog.info(test_name + ' Assertion Failed. Status code is not 201')

        self.mylog.info(test_name + ' STEP 2: Update created Organization with the \'%s\' name' % new_name)
        (status, new_id, updated_name) = gateway_util.update_organization(self, self.gateway, id, new_name)
        assert status == 200, self.mylog.info(test_name + 'Assertion Failed. Status code is not 200')
        assert new_id == id, self.mylog.info(test_name + 'Assertion Failed. New id is not equal original id')
        assert updated_name == new_name, self.mylog.info(
            test_name + 'Assertion Failed. Updated name is not equal expected name')

        self.mylog.info(test_name + ' STEP 3: Check the organization data was persisted in etcd')
        cmd = '%s --endpoints %s get --prefix "Organizationv1/%s" --print-value-only' % (self.etcdctl, self.etcd, id)
        out = litmus_utils.execCmd(self, cmd, status='OUT_STATUS')
        actual_org_id = ast.literal_eval(out[0]).get('id')
        self.mylog.info(
            test_name + 'Assert expected org_id ' + str(new_id) + ' equals actual org id ' + str(actual_org_id))
        assert new_id == actual_org_id, self.mylog.info(test_name + ' Expected org id is not equal to actual org id')
        actual_org_name = ast.literal_eval(out[0]).get('name')
        self.mylog.info(test_name + 'Assert expected org_name ' + str(updated_name) +
                        ' equals actual org name ' + str(actual_org_name))
        assert updated_name == actual_org_name, self.mylog.info(
            test_name + ' Expected org name is not equal to actual org name')
        self.footer(test_name)

    #@pytest.mark.skip
    def test_update_orgs_single_quote_char(self):
        '''

        '''
        test_name = 'test_update_orgs_ingle_quote_char_case_'
        name_orig="\'"
        new_name = name_orig + "_updated_name"
        self.header(test_name)
        self.mylog.info(test_name + ' STEP 1: Create Organization')
        (status, id, name) = gateway_util.create_organization(self, self.gateway, name_orig)
        assert status == 201, self.mylog.info(test_name + ' Assertion Failed. Status code is not 201')

        self.mylog.info(test_name + ' STEP 2: Update created Organization with the \'%s\' name' % new_name)
        (status, new_id, updated_name) = gateway_util.update_organization(self, self.gateway, id, new_name)
        assert status == 200, self.mylog.info(test_name + 'Assertion Failed. Status code is not 200')
        assert new_id == id, self.mylog.info(test_name + 'Assertion Failed. New id is not equal original id')
        assert updated_name == new_name, self.mylog.info(
            test_name + 'Assertion Failed. Updated name is not equal expected name')

        self.mylog.info(test_name + ' STEP 3: Check the organization data was persisted in etcd')
        cmd = '%s --endpoints %s get --prefix "Organizationv1/%s" --print-value-only' % (self.etcdctl, self.etcd, id)
        out = litmus_utils.execCmd(self, cmd, status='OUT_STATUS')
        actual_org_id = ast.literal_eval(out[0]).get('id')
        self.mylog.info(
            test_name + 'Assert expected org_id ' + str(new_id) + ' equals actual org id ' + str(actual_org_id))
        assert new_id == actual_org_id, self.mylog.info(test_name + ' Expected org id is not equal to actual org id')
        actual_org_name = ast.literal_eval(out[0]).get('name')
        self.mylog.info(test_name + 'org name before decosing = ' + str(actual_org_name))
        actual_org_name = json.loads("\"" + actual_org_name + "\"")
        self.mylog.info(test_name + 'org name after decoding = ' + str(actual_org_name))
        self.mylog.info(test_name + 'Assert expected org_name ' + str(updated_name) +
                        ' equals actual org name ' + str(actual_org_name))
        assert updated_name == actual_org_name, self.mylog.info(
            test_name + ' Expected org name is not equal to actual org name')
        self.footer(test_name)

    #@pytest.mark.skip
    def test_update_orgs_double_quote_char(self):
        '''

        '''
        test_name = 'test_update_orgs_double_quote_char_'
        name_orig = "HelloWorld\\\""""
        new_name = 'HelloWorld#_updated_name'
        self.header(test_name)
        self.mylog.info(test_name + ' STEP 1: Create Organization')
        (status, id, name) = gateway_util.create_organization(self, self.gateway, name_orig)
        assert status == 201, self.mylog.info(test_name + ' Assertion Failed. Status code is not 201')

        self.mylog.info(test_name + ' STEP 2: Update created Organization with the \'%s\' name' % new_name)
        (status, new_id, updated_name) = gateway_util.update_organization(self, self.gateway, id, new_name)
        assert status == 200, self.mylog.info(test_name + 'Assertion Failed. Status code is not 200')
        assert new_id == id, self.mylog.info(test_name + 'Assertion Failed. New id is not equal original id')
        self.mylog.info(test_name + 'Assert updated_name ' + str(updated_name) + ' equals new_name' + str(new_name))
        assert updated_name == new_name, self.mylog.info(
            test_name + 'Assertion Failed. Updated name is not equal expected name')

        self.mylog.info(test_name + ' STEP 3: Check the organization data was persisted in etcd')
        cmd = '%s --endpoints %s get --prefix "Organizationv1/%s" --print-value-only' % (self.etcdctl, self.etcd, id)
        out = litmus_utils.execCmd(self, cmd, status='OUT_STATUS')
        actual_org_id = ast.literal_eval(out[0]).get('id')
        self.mylog.info(
            test_name + 'Assert expected org_id ' + str(new_id) + ' equals actual org id ' + str(actual_org_id))
        assert new_id == actual_org_id, self.mylog.info(test_name + ' Expected org id is not equal to actual org id')
        actual_org_name = ast.literal_eval(out[0]).get('name')
        self.mylog.info(test_name + 'org name before decosing = ' + str(actual_org_name))
        actual_org_name = json.loads("\"" + actual_org_name + "\"")
        self.mylog.info(test_name + 'org name after decoding = ' + str(actual_org_name))
        self.mylog.info(test_name + 'Assert expected org_name ' + str(updated_name) +
                        ' equals actual org name ' + str(actual_org_name))
        assert updated_name == actual_org_name, self.mylog.info(
            test_name + ' Expected org name is not equal to actual org name')
        self.footer(test_name)

    #@pytest.mark.skip
    def test_update_orgs_back_slash_char(self):
        '''
        '''
        test_name = 'test_create_orgs_back_slash_char_'
        name_orig = "HelloWorld\\"""
        new_name = name_orig + "_updated_name"
        self.header(test_name)
        self.mylog.info(test_name + ' STEP 1: Create Organization')
        (status, id, name) = gateway_util.create_organization(self, self.gateway, name_orig)
        assert status == 201, pytest.xfail(reason='https://github.com/influxdata/platform/issues/163')

        self.mylog.info(test_name + ' STEP 2: Update created Organization with the \'%s\' name' % new_name)
        (status, new_id, updated_name) = gateway_util.update_organization(self, self.gateway, id, new_name)
        assert status == 200, self.mylog.info(test_name + 'Assertion Failed. Status code is not 200')
        assert new_id == id, self.mylog.info(test_name + 'Assertion Failed. New id is not equal original id')
        assert updated_name == new_name, self.mylog.info(
            test_name + 'Assertion Failed. Updated name is not equal expected name')

        self.mylog.info(test_name + ' STEP 3: Check the organization data was persisted in etcd')
        cmd = '%s --endpoints %s get --prefix "Organizationv1/%s" --print-value-only' % (self.etcdctl, self.etcd, id)
        out = litmus_utils.execCmd(self, cmd, status='OUT_STATUS')
        actual_org_id = ast.literal_eval(out[0]).get('id')
        self.mylog.info(
            test_name + 'Assert expected org_id ' + str(new_id) + ' equals actual org id ' + str(actual_org_id))
        assert new_id == actual_org_id, self.mylog.info(test_name + ' Expected org id is not equal to actual org id')
        actual_org_name = ast.literal_eval(out[0]).get('name')
        self.mylog.info(test_name + 'org name before decosing = ' + str(actual_org_name))
        actual_org_name = json.loads("\"" + actual_org_name + "\"")
        self.mylog.info(test_name + 'org name after decoding = ' + str(actual_org_name))
        self.mylog.info(test_name + 'Assert expected org_name ' + str(updated_name) +
                        ' equals actual org name ' + str(actual_org_name))
        assert updated_name == actual_org_name, self.mylog.info(
            test_name + ' Expected org name is not equal to actual org name')
        self.footer(test_name)

    def test_update_org_already_exists(self):
        '''
        '''
        #TODO Update to already existing name. Should fail.


