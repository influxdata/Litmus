

import pytest
import src.util.litmus_utils as litmus_utils
from src.util import gateway_util
from random import sample, shuffle
from string import ascii_lowercase
from string import ascii_uppercase
from string import digits

# organization names will have 5 letters length and will be of ascii type
org_names=[''.join(sample(ascii_lowercase, 5)) for i in range(5)]

special_char=["", "\'", 'DoubleQuotes\\"', 'BackSlash\\']
ten_char_lc=[''.join(sample(ascii_lowercase, 10)) for i in range(10)]
twenty_char_lc=[''.join(sample(ascii_lowercase, 20)) for i in range(10)]
ten_char_uc=[''.join(sample(ascii_uppercase, 10)) for i in range(10)]
twenty_char_uc=[''.join(sample(ascii_uppercase, 20)) for i in range(10)]
ten_char_numbers=[''.join(sample(digits,10)) for i in range(10)]
five_char_numbers=[''.join(sample(digits, 5)) for i in range(10)]
nonalphanumeric='!@#$%^*><&()_+{}[]|,.~/`?' # removed \, ' and " character
ten_char_nonalphanumeric=[''.join(sample(nonalphanumeric, 10)) for i in range(10)]
twenty_char_nonalphanumeric=[''.join(sample(nonalphanumeric, 20)) for i in range(10)]
twenty_char_names_list=[]
two_hundred_char_name_list=[]
for i in range(10):
    twenty_char_names=sample(nonalphanumeric, 5) + sample(ascii_lowercase, 5) + \
                      sample(ascii_uppercase, 5) + sample(digits, 5)
    two_hundred_char_names=twenty_char_names * 10
    shuffle(twenty_char_names)
    shuffle(two_hundred_char_names)
    twenty_char_names_list.append(''.join(twenty_char_names))
    two_hundred_char_name_list.append(''.join(two_hundred_char_names))
fourty_char_names_list=[]
four_hundred_char_name_list=[]
for i in range(10):
    fourty_char_names=sample(nonalphanumeric, 10) + sample(ascii_lowercase, 10) + \
                      sample(ascii_uppercase, 10) + sample(digits, 10)
    four_hundred_char_name=fourty_char_names * 10
    shuffle(fourty_char_names)
    shuffle(four_hundred_char_name)
    fourty_char_names_list.append(''.join(fourty_char_names))
    four_hundred_char_name_list.append(''.join(four_hundred_char_name))


# to install etcdctl tool on mac we need to install etcd : brew install etcd
# for ubuntu run :
# 1. curl -L  https://github.com/coreos/etcd/releases/download/v2.1.0-rc.0/etcd-v2.1.0-rc.0-linux-amd64.tar.gz -o etcd-v2.1.0-rc.0-linux-amd64.tar.gz
# 2. tar xzvf etcd-v2.1.0-rc.0-linux-amd64.tar.gz
# 3. etcdctl could be found in /tmp/etcd-v2.1.0-rc.0-linux-amd64, copy to /usr/local/bin
etcdctl='ETCDCTL_API=3 /usr/local/bin/etcdctl'

@pytest.fixture(scope='class')
def remove_users(request, etcd):
    '''
    :param request:
    :param etcd:
    :return:
    '''
    request.cls.mylog.info('remove_users() fixture is being called')
    request.cls.mylog.info('--------------------------------------')
    cmd='%s --endpoints %s del --prefix "userv1"' % (etcdctl, etcd)
    exit=litmus_utils.execCmd(request.cls, cmd)
    request.cls.mylog.info('remove_users() fixture is done')
    request.cls.mylog.info('------------------------------')
    request.cls.mylog.info('')
    assert exit == 0, request.cls.mylog('remove_users() fixture exit status is not 0')

@pytest.fixture(scope='class')
def remove_orgs(request, etcd):
    '''
    :param request:
    :param etcd:
    :return:
    '''
    request.cls.mylog.info('remove_orgs() fixture is being called')
    request.cls.mylog.info('-------------------------------------')
    cmd='%s --endpoints %s del --prefix "Organizationv1"' % (etcdctl, etcd)
    exit=litmus_utils.execCmd(request.cls, cmd)
    request.cls.mylog.info('remove_orgs() fixture is done')
    request.cls.mylog.info('-----------------------------')
    request.cls.mylog.info('')
    assert exit == 0, request.cls.mylog('remove_orgs() fixture exit status is not 0')

@pytest.fixture(scope='class')
def remove_buckets(request, etcd):
    '''
    :param request:
    :param etcd:
    :return:
    '''
    request.cls.mylog.info('remove_buckets() fixture is being called')
    request.cls.mylog.info('----------------------------------------')
    cmd='%s --endpoints %s del --prefix "bucketv1"' % (etcdctl, etcd)
    exit=litmus_utils.execCmd(request.cls, cmd)
    request.cls.mylog.info('remove_buckets() fixture is done')
    request.cls.mylog.info('--------------------------------')
    request.cls.mylog.info('')
    assert exit == 0, request.cls.mylog('remove_buckets() fixture exit status is not 0')

@pytest.fixture(scope='class')
def create_orgs(request, gateway, etcd):
    '''
    :param request:
    :param gateway:
    :param etcd:
    :return:
    '''
    request.cls.mylog.info('create_orgs() fixture is being called')
    request.cls.mylog.info('-------------------------------------')
    for org_name in org_names:
        request.cls.mylog.info('create_orgs() fixture : Creating an org \'%s\''% org_name)
        (status, org_id, name, error) = gateway_util.create_organization(request.cls, gateway, org_name)
        assert status == 201, request.cls.mylog.info('Failed to create an org \'%s\'' % org_name)
        gateway_util.verify_org_etcd(request.cls, etcd, org_id, org_name)
    request.cls.mylog.info('remove_orgs() fixture is done')
    request.cls.mylog.info('-----------------------------')
    request.cls.mylog.info('')

@pytest.fixture(scope='class')
def get_all_setup_orgs(request, create_orgs, gateway):
    '''
    :param request:
    :param create_orgs:
    :return:
    '''
    request.cls.mylog.info('get_all_setup_orgs() fixture is being called')
    request.cls.mylog.info('--------------------------------------------')
    request.cls.mylog.info('get_all_setup_orgs() fixture: Get all of the created organizations')
    (status, created_orgs_list)=gateway_util.get_all_organizations(request.cls, gateway)
    assert status == 200, \
        request.cls.mylog.info('get_all_setup_orgs() fixture: response status is ' + str(status))
    request.cls.get_all_setup_orgs=created_orgs_list
    request.cls.mylog.info('get_all_setup_orgs() fixture is done')
    request.cls.mylog.info('-----------------------------------')
    request.cls.mylog.info('')
    return request.cls.get_all_setup_orgs
