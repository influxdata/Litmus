

import pytest
import src.util.litmus_utils as litmus_utils
from src.util import gateway_util
from random import sample
from string import ascii_lowercase

# organization names will have 5 letters length and will be of ascii type
org_names=[''.join(sample(ascii_lowercase, 5)) for i in range(5)]

@pytest.fixture(scope='class')
def remove_orgs(request, etcd):
    '''
    :param request:
    :param etcd:
    :return:
    '''
    request.cls.mylog.info('remove_orgs() fixture is being called')
    request.cls.mylog.info('-------------------------------------')
    etcdctl='ETCDCTL_API=3 /usr/local/bin/etcdctl'
    cmd='%s --endpoints %s del --prefix "Organizationv1"' % (etcdctl, etcd)
    exit=litmus_utils.execCmd(request.cls, cmd)
    request.cls.mylog.info('remove_orgs() fixture is done')
    request.cls.mylog.info('-----------------------------')
    request.cls.mylog.info('')
    assert exit == 0, request.cls.mylog('remove_orgs() fixture exit status is not 0')

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
        (status, org_id, name) = gateway_util.create_organization(request.cls, gateway, org_name)
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
