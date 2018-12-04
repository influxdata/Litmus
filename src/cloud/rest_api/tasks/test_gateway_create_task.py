import pytest
import src.util.login_util as lu


from src.chronograf.lib import chronograf_rest_lib as crl


@pytest.mark.usefixtures('remove_auth', 'remove_users', 'remove_buckets', 'remove_orgs', 'remove_tasks',
                         'gateway', 'etcd_tasks', 'kubecluster', 'namespace', 'kubeconf')
class TestCreateTasks(object):
    """
    Test Suite for testing REST API endpoint for creating tasks where:
    - org_name is the same as task_name
    - flux
    The existing tasks would be removed before running tests
    """


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

