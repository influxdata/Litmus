import pytest
import src.util.litmus_utils as litmus_utils
from src.util import gateway_util
from src.util.twodotoh import org_util
from src.util.twodotoh import buckets_util
from random import sample, shuffle
from string import ascii_lowercase
from string import ascii_uppercase
from string import digits

# organization names will have 5 letters length and will be of ascii type
org_names = [''.join(sample(ascii_lowercase, 5)) for i in range(5)]
# user names will have 5 letters length
# noinspection PyRedeclaration
user_names = [''.join(sample(ascii_uppercase, 5)) for i in range(10)]

special_char = ["", "\'", 'DoubleQuotes\\"', 'BackSlash\\']
# noinspection PyRedeclaration
ten_char_lc = [''.join(sample(ascii_lowercase, 10)) for i in range(10)]
# noinspection PyRedeclaration
twenty_char_lc = [''.join(sample(ascii_lowercase, 20)) for i in range(10)]
# noinspection PyRedeclaration
ten_char_uc = [''.join(sample(ascii_uppercase, 10)) for i in range(10)]
# noinspection PyRedeclaration
twenty_char_uc = [''.join(sample(ascii_uppercase, 20)) for i in range(10)]
# noinspection PyRedeclaration
ten_char_numbers = [''.join(sample(digits, 10)) for i in range(10)]
# noinspection PyRedeclaration
five_char_numbers = [''.join(sample(digits, 5)) for i in range(10)]
nonalphanumeric = '!@#$%^*><&()_+{}[]|,.~/`?'  # removed \, ' and " character
# noinspection PyRedeclaration
ten_char_nonalphanumeric = [''.join(sample(nonalphanumeric, 10)) for i in range(10)]
# noinspection PyRedeclaration
twenty_char_nonalphanumeric = [''.join(sample(nonalphanumeric, 20)) for i in range(10)]
twenty_char_names_list = []
two_hundred_char_name_list = []
# noinspection PyRedeclaration
for i in range(10):
    twenty_char_names = sample(nonalphanumeric, 5) + sample(ascii_lowercase, 5) + \
                        sample(ascii_uppercase, 5) + sample(digits, 5)
    two_hundred_char_names = twenty_char_names * 10
    shuffle(twenty_char_names)
    shuffle(two_hundred_char_names)
    twenty_char_names_list.append(''.join(twenty_char_names))
    two_hundred_char_name_list.append(''.join(two_hundred_char_names))
forty_char_names_list = []
four_hundred_char_name_list = []
# noinspection PyRedeclaration
for i in range(10):
    forty_char_names = sample(nonalphanumeric, 10) + sample(ascii_lowercase, 10) + \
                       sample(ascii_uppercase, 10) + sample(digits, 10)
    four_hundred_char_name = forty_char_names * 10
    shuffle(forty_char_names)
    shuffle(four_hundred_char_name)
    forty_char_names_list.append(''.join(forty_char_names))
    four_hundred_char_name_list.append(''.join(four_hundred_char_name))


def _assert(request, actual, expected, expected_var, xfail=False, reason=''):
    """
    :param request: (object): request object, e.g. 'self'
    :param actual (str): actual value
    :param expected (str): expected value
    :param expected_var (str): kind of value, e.g. 'status code'
    :return: Pass/Fail/XFail
    """
    try:
        if xfail:
            assert actual == expected, pytest.xfail(reason=reason)
        else:
            assert actual == expected, \
                'Actual \'%s\' \'%s\' does not equal to expected \'%s\' \'%s\'' \
                % (actual, expected_var, expected, expected_var)
    except AssertionError, e:
        request.mylog.info(e)
        raise


# TODO add an extra param : error, currently hardcoded to an empty string L94-95
def verify_org_etcd_entries(request, test_name, created_org_id, created_org_name, error, get_index_values=False,
                            name_by_index_id=None, error_by_index_id=None, id_by_index_name=None,
                            error_by_index_name=None):
    """
    Function verifies id and name of the organization
    :param request:
    :param test_name:
    :param created_org_id:
    :param created_org_name:
    :param error:
    :param get_index_values:
    :param name_by_index_id:
    :param error_by_index_id:
    :param id_by_index_name:
    :param error_by_index_name:
    :return: Pass/Fail
    """
    # actual_org_id, actual_org_name, error, name_by_index_id, error_by_index_id, id_by_index_name, error_by_index_name
    result = gateway_util.get_org_etcd(request, request.etcd, created_org_id, get_index_values)
    request.mylog.info(test_name + 'Assert actual org_id \'%s\' equals to expected org_id \'%s\''
                       % (result[0], created_org_id))
    _assert(request, result[0], created_org_id, 'org_id')
    request.mylog.info(test_name + 'Assert actual org_name \'%s\' equals to expected org_name \'%s\''
                       % (result[1], created_org_name))
    _assert(request, result[1], created_org_name, 'org_name')
    request.mylog.info(test_name + 'Assert actual error \'%s\' equals to expected \'%s\''
                       % (result[2], error))
    _assert(request, result[2], error, 'error')
    if get_index_values:
        if name_by_index_id:
            request.mylog.info \
                (test_name + 'Assert actual name_by_index_id \'%s\' equals to expected name_by_index_id \'%s\''
                 % (result[3], name_by_index_id))
            _assert(request, result[3], name_by_index_id, 'name_by_index_id')
            request.mylog.info \
                (test_name + 'Assert actual error_by_index_id \'%s\' equals to expected error_by_index_id \'%s\''
                 % (result[4], error_by_index_id))
            _assert(request, result[4], error_by_index_id, 'error_by_index_id')
        if id_by_index_name:
            request.mylog.info \
                (test_name + 'Assert actual id_by_index_name \'%s\' equals to expected id_by_index_name \'%s\''
                 % (result[5], id_by_index_name))
            _assert(request, result[5], id_by_index_name, 'id_by_index_name')
            request.mylog.info \
                (test_name + 'Assert actual error_by_index_name \'%s\' equals to expected error_by_index_name \'%s\''
                 % (result[6], error_by_index_name))
            _assert(request, result[6], error_by_index_name, 'error_by_index_name')


def verify_bucket_etcd_entries(request, test_name, expected_bucket_id, expected_bucket_name, expected_retention_period,
                               expected_error):
    """
    Function verifies bucket id, name and errors, if any
    :param request:
    :param test_name:
    :param expected_bucket_id:
    :param expected_bucket_name:
    :param expected_retention_period:
    :param expected_error:
    :return: Pass/Fail
    """
    request.mylog.info(test_name + 'Parameters: expected_bucket_id = \'%s\', expected_bucket_name = \'%s\', '
                                   'expected_retention_period = \'%s\', expected_error = \'%s\''
                       % (expected_bucket_id, expected_bucket_name, expected_retention_period, expected_error))
    actual_bucket_id, actual_bucket_name, actual_retention_period, actual_error = \
        gateway_util.get_bucket_etcd(request, request.etcd, expected_bucket_id)
    request.mylog.info(test_name + 'Assert actual bucket_id \'%s\' equals to expected bucket_id \'%s\''
                       % (actual_bucket_id, expected_bucket_id))
    _assert(request, actual_bucket_id, expected_bucket_id, 'bucket_id')
    request.mylog.info(test_name + 'Assert actual bucket_name \'%s\' equals to expected bucket_name \'%s\''
                       % (actual_bucket_name, expected_bucket_name))
    _assert(request, actual_bucket_name, expected_bucket_name, 'bucket_name')
    request.mylog.info(test_name + 'Assert actual retention_period \'%s\' equals to expected retention_period \'%s\''
                       % (actual_retention_period, expected_retention_period))
    _assert(request, actual_retention_period, expected_retention_period, 'retention_period')
    request.mylog.info(test_name + 'Assert actual error \'%s\' equals to expected error \'%s\''
                       % (actual_error, expected_error))
    _assert(request, actual_error, expected_error, 'error')


def verify_user_etcd_entries(request, test_name, expected_user_id, expected_user_name, expected_error):
    """
    Function verifies user id, name and errors, if any
    :param request:
    :param test_name:
    :param expected_user_id:
    :param expected_user_name:
    :param expected_error:
    :return: Pass/Fail
    """
    request.mylog.info(test_name + 'Parameters: expected_user_id = \'%s\', expected_user_name = \'%s\', '
                                   'expected_error = \'%s\''
                       % (expected_user_id, expected_user_name, expected_error))
    actual_user_id, actual_user_name, actual_error = \
        gateway_util.get_user_etcd(request, request.etcd, expected_user_id)
    request.mylog.info(test_name + 'Assert actual user_id \'%s\' equals to expected user_id \'%s\''
                       % (actual_user_id, expected_user_id))
    _assert(request, actual_user_id, expected_user_id, 'user_id')
    request.mylog.info(test_name + 'Assert actual user_name \'%s\' equals to expected user_name \'%s\''
                       % (actual_user_name, expected_user_name))
    _assert(request, actual_user_name, expected_user_name, 'bucket_name')
    request.mylog.info(test_name + 'Assert actual error \'%s\' equals to expected error \'%s\''
                       % (actual_error, expected_error))
    _assert(request, actual_error, expected_error, 'error')


# to install etcdctl tool on mac we need to install etcd : brew install etcd
# for ubuntu run :
# 1. curl -L  https://github.com/coreos/etcd/releases/download/v2.1.0-rc.0/etcd-v2.1.0-rc.0-linux-amd64.tar.gz -o
#     etcd-v2.1.0-rc.0-linux-amd64.tar.gz
# 2. tar xzvf etcd-v2.1.0-rc.0-linux-amd64.tar.gz
# 3. etcdctl could be found in /tmp/etcd-v2.1.0-rc.0-linux-amd64, copy to /usr/local/bin
etcdctl = 'ETCDCTL_API=3 /usr/local/bin/etcdctl'


@pytest.fixture(scope='class')
def remove_tasks(request, etcd_tasks):
    """
    Remove all references for the specific tasks from etcd-tasks store using ETCDCTL command
    https://github.com/influxdata/idpe/blob/49ae6f73546b05e8597d2284a3957c20999c5bdd/task/store/etcd/store.go
    #L1195-L1214
    delTask := clientv3.OpDelete(path.Join(tasksPath, idStr))
    delTaskMeta := clientv3.OpDelete(path.Join(taskMetaPath, idStr)+"/", clientv3.WithPrefix())
    delOrgTask := clientv3.OpDelete(path.Join(orgsPath, org, idStr))

    // Only release the lease task but now the owner. When in a cluster
    // we will most likely not be the owner of this lease.
    delClaimTask := clientv3.OpDelete(path.Join(claimPath, idStr))
    delUserTask := clientv3.OpDelete(path.Join(usersPath, user, idStr))

    where:
    tasksPath     = basePath + "tasks"
    orgsPath      = basePath + "orgs"
    usersPath     = basePath + "users"
    taskMetaPath  = basePath + "task_meta"
    claimPath     = basePath + "claims"
    orgDelPath    = basePath + "org_deletions"
    userDelPath   = basePath + "user_deletions"
    cancelRunPath = basePath + "runs"
    basePath = "/tasks/v1/"

    :param request:
    :param etcd_tasks:
    :return:
    """
    # Should change to remove the above and leave /tasks/v1/claims/02f8d98a004e0000/owner
    #                                               tasks-7dcc47895c-mvpql
    request.cls.mylog.info('remove_tasks() fixture is being called')
    request.cls.mylog.info('--------------------------------------')
    cmd = '%s --endpoints %s del --prefix "/tasks/v1"' % (etcdctl, etcd_tasks)
    exit = litmus_utils.execCmd(request.cls, cmd)
    request.cls.mylog.info('remove_tasks() fixture is done')
    request.cls.mylog.info('------------------------------')
    request.cls.mylog.info('')
    assert exit == 0, request.cls.mylog('remove_tasks() fixture exit status is not 0')


@pytest.fixture(scope='class')
def remove_auth(request, etcd):
    """

    :param request:
    :param etcd:
    :return:
    """
    request.cls.mylog.info('remove_auth() fixture is being called')
    request.cls.mylog.info('-------------------------------------')
    cmd = '%s --endpoints %s del --prefix "authorizationv1"' % (etcdctl, etcd)
    exit = litmus_utils.execCmd(request.cls, cmd)
    request.cls.mylog.info('remove_auth() fixture is done')
    request.cls.mylog.info('-----------------------------')
    request.cls.mylog.info('')
    assert exit == 0, request.cls.mylog('remove_auth() fixture exit status is not 0')


@pytest.fixture(scope='class')
def remove_users(request, etcd):
    """
    :param request:
    :param etcd:
    :return:
    """
    request.cls.mylog.info('remove_users() fixture is being called')
    request.cls.mylog.info('--------------------------------------')
    cmd = '%s --endpoints %s del --prefix "userv1"' % (etcdctl, etcd)
    exit = litmus_utils.execCmd(request.cls, cmd)
    request.cls.mylog.info('remove_users() fixture is done')
    request.cls.mylog.info('------------------------------')
    request.cls.mylog.info('')
    assert exit == 0, request.cls.mylog('remove_users() fixture exit status is not 0')


@pytest.fixture(scope='class')
def remove_orgs(request, etcd):
    """
    :param request:
    :param etcd:
    :return:
    """
    request.cls.mylog.info('remove_orgs() fixture is being called')
    request.cls.mylog.info('-------------------------------------')
    cmd_remove_org_id = '%s --endpoints %s del --prefix "indexv1/org/id"' % (etcdctl, etcd)
    cmd_remove_org_name = '%s --endpoints %s del --prefix "indexv1/org/name"' % (etcdctl, etcd)
    cmd = '%s --endpoints %s del --prefix "Organizationv1"' % (etcdctl, etcd)
    request.cls.mylog.info('remove_orgs() removing index org id')
    exit_org_id = litmus_utils.execCmd(request.cls, cmd_remove_org_id)
    request.cls.mylog.info('remove_orgs() removing index org name')
    exit_org_name = litmus_utils.execCmd(request.cls, cmd_remove_org_name)
    request.cls.mylog.info('remove_orgs() removing Organization')
    exit = litmus_utils.execCmd(request.cls, cmd)
    request.cls.mylog.info('remove_orgs() fixture is done')
    request.cls.mylog.info('-----------------------------')
    request.cls.mylog.info('')
    assert exit_org_id == 0, request.cls.mylog('remove_orgs() fixture exit_org_id status is not 0')
    assert exit_org_name == 0, request.cls.mylog('remove_orgs() fixture exit_org_name status is not 0')
    assert exit == 0, request.cls.mylog('remove_orgs() fixture exit status is not 0')


@pytest.fixture(scope='class')
def remove_buckets(request, etcd):
    """
    :param request:
    :param etcd:
    :return:
    """
    request.cls.mylog.info('remove_buckets() fixture is being called')
    request.cls.mylog.info('----------------------------------------')
    cmd = '%s --endpoints %s del --prefix "bucketv1"' % (etcdctl, etcd)
    exit = litmus_utils.execCmd(request.cls, cmd)
    request.cls.mylog.info('remove_buckets() fixture is done')
    request.cls.mylog.info('--------------------------------')
    request.cls.mylog.info('')
    assert exit == 0, request.cls.mylog('remove_buckets() fixture exit status is not 0')


@pytest.fixture(scope='class')
def get_all_setup_users(request, gateway):
    """
    :param request:
    :param gateway
    :return:
    """
    request.cls.mylog.info('get_all_setup_users() fixture is being called')
    request.cls.mylog.info('---------------------------------------------')
    request.cls.mylog.info('')
    for user_name in user_names:
        request.cls.mylog.info('get_all_setup_users() fixture : Creating user \'%s\'' % user_name)
        (status, user_id, name, error) = gateway_util.create_user(request.cls, gateway, user_name)
        assert status == 201, request.cls.mylog.info('Failed to create user \'%s\'' % user_name)
    request.cls.mylog.info('get_all_setup_users() fixture: Get all of the created users')
    (status, created_users_list) = gateway_util.get_all_users(request.cls, gateway)
    assert status == 200, \
        request.cls.mylog.info('get_all_setup_users() fixture: response status is ' + str(status))
    request.cls.get_all_setup_users = created_users_list
    request.cls.mylog.info('get_all_setup_users() fixture is done')
    request.cls.mylog.info('-------------------------------------')
    request.cls.mylog.info('')
    return request.cls.get_all_setup_users


@pytest.fixture(scope='class')
def get_all_setup_orgs(request, gateway):
    """
    :param request:
    :param gateway
    :return:
    """
    request.cls.mylog.info('get_all_setup_orgs() fixture is being called')
    request.cls.mylog.info('--------------------------------------------')
    request.cls.mylog.info('')
    for org_name in org_names:
        request.cls.mylog.info('get_all_setup_orgs() fixture : Creating an org \'%s\'' % org_name)
        create_result = org_util.create_organization(request.cls, gateway, org_name)
        status = create_result['status']
        assert status == 201, request.cls.mylog.info('Failed to create an org \'%s\'' % org_name)
    request.cls.mylog.info('get_all_setup_orgs() fixture: Get all of the created organizations')
    status, created_orgs_list = org_util.get_all_organizations(request.cls, gateway)
    assert status == 200, \
        request.cls.mylog.info('get_all_setup_orgs() fixture: response status is ' + str(status))
    request.cls.get_all_setup_orgs = created_orgs_list
    request.cls.mylog.info('get_all_setup_orgs() fixture is done')
    request.cls.mylog.info('------------------------------------')
    request.cls.mylog.info('')
    return request.cls.get_all_setup_orgs


@pytest.fixture(scope='class')
def get_all_setup_buckets(request, gateway):
    """
    :param request:
    :param gateway
    :return:
    """
    request.cls.mylog.info('get_all_setup_buckets() fixture is being called')
    request.cls.mylog.info('-----------------------------------------------')
    request.cls.mylog.info('')
    for org_name in org_names:
        request.cls.mylog.info('get_all_setup_buckets() fixture : Creating an org \'%s\'' % org_name)
        request.cls.mylog.info('-' * (51 + len(org_name) + 1))
        create_result = org_util.create_organization(request.cls, gateway, org_name)
        status = create_result['status']
        org_id = create_result['org_id']
        assert status == 201, request.cls.mylog.info('Failed to create an org \'%s\'' % org_name)
        for bucket_name in ascii_uppercase:
            request.cls.mylog.info('get_all_setup_buckets() fixture : Creating a bucket \'%s\'' % bucket_name)
            # TODO make retention period a variable param
            create_bucket_result = buckets_util.create_bucket(request.cls, gateway, bucket_name, 3600, org_id)
            assert create_bucket_result['status'] == \
                   201, request.cls.mylog.info('Failed to create a bucket \'%s\'' % bucket_name)
    status, error_message, created_buckets_list = buckets_util.get_all_buckets(request.cls, gateway)
    assert status == 200, \
        request.cls.mylog.info('get_all_setup_buckets() fixture: response status is ' + str(status))
    request.cls.get_all_setup_buckets = created_buckets_list
    request.cls.mylog.info('get_all_setup_buckets() fixture is done')
    request.cls.mylog.info('--------------------------------------')
    request.cls.mylog.info('')
    return request.cls.get_all_setup_buckets
