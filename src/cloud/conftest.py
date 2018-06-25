

import pytest
import src.util.litmus_utils as litmus_utils

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
