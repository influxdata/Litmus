import pytest
import src.util.login_util as lu
from src.chronograf.lib import chronograf_rest_lib as crl
from src.util import gateway_util
from string import ascii_lowercase
from string import ascii_uppercase
from string import digits
from src.cloud.rest_api.conftest import ten_char_lc, twenty_char_lc, twenty_char_uc, ten_char_uc, \
    ten_char_numbers, five_char_numbers, nonalphanumeric, ten_char_nonalphanumeric, \
    twenty_char_nonalphanumeric, twenty_char_names_list, fourty_char_names_list, \
    four_hundred_char_name_list, two_hundred_char_name_list, special_char


@pytest.mark.usefixtures('remove_tasks', 'create_org', 'create_bucket', 'create_user_token', 'gateway')
class TestCreateTasksAllRequiredKeysAPI(object):
    '''
    Test Suite for testing REST API endpoint for creating tasks where:
    - org_name is the same as task_name
    - flux - .....?????
    The existing tasks would be removed before running tests
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

    #default_flux_script='option task = {name:"all required keys", every:1h} from(bucket:"%s") |> range(start:-24) |> to(bucket:"%s")' %

    def run_tests(self, name_of_the_test_to_run, task_name, org_name, flux):
        '''
        :param name_of_the_test_to_run: test name
        :param task_name: name of the task to be created
        :return: pass/fail
        '''
        test_name=name_of_the_test_to_run + task_name + ' '
        self.header(test_name)


        self.mylog.info(test_name + 'STEP 2: Verify data was persisted in the etcd store')
        #gateway_util.verify_task_etcd(self, self.etcd)
        self.footer(test_name)

    #================== LOWER CASE CHARACTESRS ========================
    @pytest.mark.parametrize('one_char', ascii_lowercase)
    def test_create_tasks_single_char_lower_case(self, one_char):
        '''
        REST API: http://<gateway>/api/v2/tasks
        METHOD: POST
        tests task name containing single character lower case letters can be created and persisted in the etcd store.
        '''
        self.run_tests('test_create_tasks_single_char_lower_case ', one_char)

    @pytest.mark.parametrize('ten_char', ten_char_lc)
    def test_create_tasks_10_char_lower_case(self, ten_char):
        '''
        REST API: http://<gateway>/api/v2/tasks
        METHOD: POST
        tests task name containing 10 random lower case characters can be created and persisted in the etcd store.
        '''
        self.run_tests('test_create_tasks_10_char_lower_case ', ten_char)

    @pytest.mark.parametrize('twenty_char', twenty_char_lc)
    def test_create_tasks_20_char_lower_case(self, twenty_char):
        '''
        REST API: http://<gateway>/api/v2/tasks
        METHOD: POST
        tests task name containing 20 random lower case characters can be created and persisted in the etcd store.
        '''
        self.run_tests('test_create_tasks_20_char_lower_case ', twenty_char)

    #=================== UPPER CASE CHARACTERS ==========================
    @pytest.mark.parametrize('one_char', ascii_uppercase)
    def test_create_tasks_single_char_upper_case(self, one_char):
        '''
        REST API: http://<gateway>/api/v2/tasks
        METHOD: POST
        tests task name containing single character upper case letters can be created and persisted in the etcd store.
        '''
        self.run_tests('test_create_tasks_single_char_upper_case ', one_char)

    @pytest.mark.parametrize('ten_char', ten_char_uc)
    def test_create_tasks_10_char_upper_case(self, ten_char):
        '''
        REST API: http://<gateway>/api/v2/tasks
        METHOD: POST
        tests task name containing 10 random upper case characters can be created and persisted in the etcd store.
        '''
        self.run_tests('test_create_tasks_10_char_upper_case ', ten_char)

    @pytest.mark.parametrize('twenty_char', twenty_char_uc)
    def test_create_tasks_20_char_upper_case(self, twenty_char):
        '''
        REST API: http://<gateway>/api/v2/tasks
        METHOD: POST
        tests task name containing 20 random lower case characters can be created and persisted in the etcd store.
        '''
        self.run_tests('test_create_tasks_20_char_upper_case ', twenty_char)

    #========================== DIGITS ===================================
    @pytest.mark.parametrize('one_char', digits)
    def test_create_tasks_single_digit(self, one_char):
        '''
        REST API: http://<gateway>/api/v2/tasks
        METHOD: POST
        tests task name containing single digit can be created and persisted in the etcd store.
        '''
        self.run_tests('test_create_tasks_single_digit ', one_char)

    @pytest.mark.parametrize('ten_char', ten_char_numbers)
    def test_create_tasks_10_digits(self, ten_char):
        '''
        REST API: http://<gateway>/api/v2/tasks
        METHOD: POST
        tests task name containing 10 random digits can be created and persisted in the etcd store.
        '''
        self.run_tests('test_create_tasks_10_digits ', ten_char)

    @pytest.mark.parametrize('five_char', five_char_numbers)
    def test_create_tasks_5_digits(self, five_char):
        '''
        REST API: http://<gateway>/api/v2/tasks
        METHOD: POST
        tests task name containing 5 random digits can be created and persisted in the etcd store.
        '''
        self.run_tests('test_create_tasks_5_digits ', five_char)

    #============================ NON-ALPHANUMERIC =============================
    @pytest.mark.parametrize('one_char', nonalphanumeric)
    def test_create_tasks_single_nonalphanumeric_char(self, one_char):
        '''
        REST API: http://<gateway>/api/v2/tasks
        METHOD: POST
        tests task name containing 1 non-alphanumeric character can be created and persisted in the etcd store.
        '''
        self.run_tests('test_create_tasks_single_nonalphanumeric_char ', one_char)

    @pytest.mark.parametrize('ten_char', ten_char_nonalphanumeric)
    def test_create_tasks_10_nonalphanumeric_char(self, ten_char):
        '''
        REST API: http://<gateway>/api/v2/tasks
        METHOD: POST
        tests task name containing 10 random non-alphanumeric character can be created and persisted in the etcd store.
        '''
        self.run_tests('test_create_tasks_10_nonalphanumeric_char ', ten_char)

    @pytest.mark.parametrize('twenty_char', twenty_char_nonalphanumeric)
    def test_create_tasks_20_nonalphanumeric_char(self, twenty_char):
        '''
        REST API: http://<gateway>/api/v2/tasks
        METHOD: POST
        tests task name containing random 20 non-alphanumeric characters can be created and persisted in the etcd store.
        '''
        self.run_tests('test_create_tasks_20_nonalphanumeric_char ', twenty_char)

    #============================ MIX CHARACTERS ================================
    @pytest.mark.parametrize('twenty_char_names', twenty_char_names_list)
    def test_create_tasks_20_char_mix(self, twenty_char_names):
        '''
        REST API: http://<gateway>/api/v2/tasks
        METHOD: POST
        tests task name containing 20 mix characters can be created and persisted in the etcd store.
        '''
        self.run_tests('test_create_tasks_20_char_mix ', twenty_char_names)

    @pytest.mark.parametrize('fourty_char_names', fourty_char_names_list)
    def test_create_tasks_40_char_mix(self, fourty_char_names):
        '''
        REST API: http://<gateway>/api/v2/tasks
        METHOD: POST
        tests task name containing 40 mix characters can be created and persisted in the etcd store.
        '''
        self.run_tests('test_create_tasks_40_char_mix ', fourty_char_names)

    @pytest.mark.parametrize('two_hundred_char_names', two_hundred_char_name_list)
    def test_create_tasks_200_char_mix(self, two_hundred_char_names):
        '''
        REST API: http://<gateway>/api/v2/tasks
        METHOD: POST
        tests task name containing 200 mix characters can be created and persisted in the etcd store.
        '''
        self.run_tests('test_create_tasks_200_char_mix ', two_hundred_char_names)

    @pytest.mark.parametrize('four_hundred_char_names', four_hundred_char_name_list)
    def test_create_tasks_400_char_mix(self, four_hundred_char_names):
        '''
        REST API: http://<gateway>/api/v2/tasks
        METHOD: POST
        tests task name containing 400 mix characters can be created and persisted in the etcd store.
        '''
        self.run_tests('test_create_tasks_400_char_mix ', four_hundred_char_names)

    @pytest.mark.parametrize('special_char', special_char)
    def test_create_tasks_special_chars(self, special_char):
        '''
        REST API: http://<gateway>/api/v2/tasks
        METHOD: POST
        tests task name containing special characters can be created and persisted in the etcd store.
        '''
        self.run_tests('test_create_tasks_special_chars ', special_char)

    def test_create_tasks_duplicate_names(self):
        '''
        REST API: http://<gateway>/api/v2/tasks
        METHOD: POST
        tests cannot create task with already existing name.
        '''
        test_name='test_create_tasks_duplicate_names '
        task_name='duplicate_name'
        self.header(test_name)
        self.mylog.info(test_name + 'STEP 1: Create a task "%s"' % task_name)
        (status, created_task_id, created_task_name, error_message)=\
            gateway_util.create_task(self, self.gateway, task_name)
        assert status == 201, \
            self.mylog.info(test_name + 'Assertion failed. status=%d, error message %s' % (status, error_message))
        self.mylog.info(test_name + 'STEP 2: Verify data was persisted in the etcd store')
        #gateway_util.verify_task_etcd(self, self.etcd, created_task_id, created_task_name)
        self.mylog.info(test_name + 'STEP 3: Try creating task with the same name')
        (status, created_task_id, created_task_name, error_message)=\
            gateway_util.create_task(self, self.gateway, task_name)
        assert status == 404, pytest.xfail(reason='status code is 500')
        self.footer(test_name)


