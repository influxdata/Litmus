import pytest
import time
import src.util.twodotoh.org_util as org_util
import src.util.twodotoh.buckets_util as buckets_util
import src.util.twodotoh.tasks_util as tasks_util
import src.util.gateway_util as gateway_util
import src.util.login_util as lu
import json

from datetime import datetime
from src.chronograf.lib import chronograf_rest_lib as crl
from src.cloud.rest_api.conftest import _assert
from src.cloud.rest_api.conftest import verify_org_etcd_entries
from src.cloud.rest_api.conftest import verify_bucket_etcd_entries
from src.cloud.rest_api.conftest import verify_user_etcd_entries


# remove authorization before removing users
@pytest.mark.usefixtures('remove_orgs', 'remove_buckets', 'remove_auth', 'remove_users', 'remove_tasks',
                         'gateway', 'etcd_tasks', 'flux', 'namespace', 'kubeconf', 'kubecluster')
class TestSmoke(object):
    """
    TODO
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


    def test_e2e_smoke(self):
        """
        1. Create an organization. Verify organization was created successfully.
        2. Create a bucket for the organization created in step 1. Verify org was created successfully.
        3. Create a user. Verify user was created successfully.
        4. Give user permissions to write data to buckets and read data from the same buckets. Verify authentication is
           successful.
        5. Write data points
           5.1. Verify data got to kafka.
        6. Query data using using queryd. (gateway:9999/api/v2/querysvc)
        7. Query data using gateway. (gateway:9999/api/v2/query)
        """
        test_name = 'test_e2e_smoke '
        org_name = 'test_e2e_smoke_org'
        bucket_name = 'test_e2e_smoke_bucket'
        user_name = 'test_e2e_smoke_user'
        measurement = 'test_m'
        tag = 'hello world'
        tag_storage = 'hello\ world'
        value = '1234'
        query = 'from(bucket:"%s") |> range(start:-5m)' % bucket_name

        err = '' # intial error message is am empty string.
        data = [] # to store the data that made it to kafka, initial value is empty list.
        final_kafka_points = '' # if kafka has a data we are looking for, added to a final_point str.
        final_storage_points = ''

        self.header(test_name)
        self.mylog.info(test_name + 'STEP 1: Create Organization')
        self.mylog.info(test_name + '\n')
        create_org_result = org_util.create_organization(self, self.gateway, org_name)
        status_code = create_org_result.get('status')
        org_id = create_org_result.get('org_id')
        org_name = create_org_result.get('org_name')

        _assert(self, status_code, 201, 'Create Organization Status Code')
        verify_org_etcd_entries(self, test_name, org_id, org_name, error='')

        self.mylog.info(test_name + 'STEP 2: Create Bucket')
        self.mylog.info(test_name + '\n')
        create_bucket_result = \
            buckets_util.create_bucket(self, self.gateway, bucket_name, organization_id=org_id)
        status_code = create_bucket_result['status']
        created_bucket_id = create_bucket_result.get('bucket_id')
        created_bucket_name = create_bucket_result.get('bucket_name')

        _assert(self, status_code, 201, 'Create Bucket Status Code')
        verify_bucket_etcd_entries(self, test_name, created_bucket_id, created_bucket_name, 0, expected_error='')

        self.mylog.info(test_name + 'STEP 3: Create User')
        self.mylog.info(test_name + '\n')
        status_code, user_id, created_user_name, error_message = \
            gateway_util.create_user(self, self.gateway, user_name)
        _assert(self, status_code, 201, 'Create User Status Code')

        permissions = [{"action": "read", "resource": "bucket/%s" % created_bucket_id},
                       {"action": "write", "resource": "bucket/%s" % created_bucket_id}]
        self.mylog.info(
            test_name + 'STEP 4: Create Authorization Token for \'%s\' to be able to read/write \'%s\' bucket'
            % (user_name, bucket_name))
        self.mylog.info(test_name + '\n')
        create_auth_result = gateway_util.create_authorization(self, self.gateway, user_name, user_id,
                                                               json.dumps(permissions))
        token = create_auth_result.get('token')
        _assert(self, create_auth_result.get('status'), 201, 'Create Authorization Status')
        _assert(self, create_auth_result.get('error'), None, 'Create Authorization Error')

        self.mylog.info(test_name + 'STEP 5: Write point to a bucket')
        self.mylog.info(test_name + '\n')
        write_result = gateway_util.write_points(self, self.gateway, token, org_name, bucket_name, data='%s,t=%s f=%s'
                                                                                    % (measurement, tag_storage, value))
        _assert(self, write_result.get('status'), 204, 'Write Data Point To A Bucket')
        _assert(self, write_result.get('error'), '', 'Write Data Error Message')

        self.mylog.info(test_name + 'STEP 6: Verify Data Was Written To Kafka')
        self.mylog.info(test_name + '\n')
        # just if there is a latency on writing data to kafka, give it some time
        end_time = time.time() + 10
        while time.time() <= end_time:
            topics, data, err = gateway_util.kafka_find_data_by_tag(self, self.kubeconf, self.kubecluster,
                                                                    self.namespace, tag, 'kafka-0')
            if len(data) == 0:
                self.mylog.info(test_name + 'KAFKA DOES NOT HAVE THE DATA YET. SLEEPING 1 SECOND.')
                time.sleep(1)
                continue
            else:
                for point in data:
                    if tag in point:
                        final_kafka_points += point
                        self.mylog.info(test_name + 'KAFKA DOES HAVE THE DATA:' + str(point))
                        break
                else:
                    self.mylog.info(test_name + 'KAFKA DOES NOT HAVE THE DATA YET')
                    continue
                break
        _assert(self, err, '', 'ERROR GETTING DATA FROM KAFKA')
        _assert(self, len(data) > 0, True, 'KAFKA DOES NOT HAVE THE DATA')
        _assert(self, tag in final_kafka_points, True, 'KAFKA DOES NOT HAVE THE DATA')

        # storage is pulling every 10 seconds from kafka
        self.mylog.info(test_name + 'STEP 7: Verify Data Was Written To Storage')
        self.mylog.info(test_name + '\n')
        end_time = time.time() + 20
        while time.time() <= end_time:
            engine, data, err = gateway_util.storage_find_data(self, self.kubeconf, self.kubecluster, self.namespace,
                                                               tag, 'storage-0')
            if len(data) == 0:
                self.mylog.info(test_name + 'STORAGE DOES NOT HAVE THE DATA YET. SLEEPING FOR 1 SECOND.')
                time.sleep(1)
                continue
            else:
                for point in data:
                    if tag_storage in point:
                        final_storage_points += point
                        self.mylog.info(test_name + 'STORAGE DOES HAVE THE DATA: ' + str(point))
                        break
                else:  # storage has some data, but data we are looking for is not there yet.
                    self.mylog.info('STORAGE DOES NOT HAVE THE DATA YET')
                    continue
                break
        _assert(self, err, '', 'ERROR GETTING DATA FROM STORAGE')
        _assert(self, len(data) > 0, True, 'STORAGE DOES NOT HAVE THE DATA')
        _assert(self, tag_storage in final_storage_points, True, 'STORAGE DOES NOT HAVE THE DATA')

        self.mylog.info(test_name + 'STEP 8: Query Data using Queryd')
        self.mylog.info(test_name + '\n')
        # need to give it up to 30 sec to get the results back
        end_time = time.time() + 30
        result_queryd = None
        while time.time() <= end_time:
            result_queryd = gateway_util.queryd_query_data(self, query, self.flux, org_id, timeout=5, responsenone=False)
            if result_queryd.get('status') == 200 and len(result_queryd.get('result')) == 1:
                break
            else:
                self.mylog.info(test_name + 'WAITING FOR QUERY RESULTS. SLEEPING FOR 1 SECOND.')
                time.sleep(1)
        _assert(self, result_queryd.get('status'), 200, ' STATUS CODE')
        _assert(self, len(result_queryd.get('result')), 1, ' NUMBER OF RECORDS')
        _assert(self, result_queryd.get('result')[0].get('_measurement'), measurement, 'Measurement')
        _assert(self, result_queryd.get('result')[0].get('_value'), value, 'Field Value')
        _assert(self, result_queryd.get('result')[0].get('t'), tag, 'Tag Value')

        self.mylog.info('')
        self.mylog.info(test_name + 'STEP 9: Query Data using Gateway')
        self.mylog.info(test_name + '\n')
        # need to give it up to 30 sec to get the results back
        end_time = time.time() + 30
        result_gateway = None
        while time.time() <= end_time:
            result_gateway = gateway_util.gateway_query_data(self, query, self.gateway, token, org_name)
            if result_gateway.get('status') == 200 and len(result_gateway.get('result')) == 1:
                break
            else:
                self.mylog.info(test_name + 'WAITING FOR QUERY RESULTS. SLEEPING FOR 1 SECONDS.')
                time.sleep(1)
        _assert(self, result_gateway.get('status'), 200, ' STATUS CODE')
        _assert(self, len(result_gateway.get('result')), 1, ' NUMBER OF RECORDS')
        _assert(self, result_gateway.get('result')[0].get('_measurement'), measurement, 'Measurement')
        _assert(self, result_gateway.get('result')[0].get('_value'), value, 'Field Value')
        _assert(self, result_gateway.get('result')[0].get('t'), tag, 'Tag Value')


    def test_tasks_smoke(self):
        """
        1. Create organization and verify it was created successfully.
        2. Create bucket (source bucket) to read data from and verify it was created successfully.
        3. Create bucket (destination bucket) to write data to and verify it was created successfully.
        4. Create user.
        5. Create an authorization token.
        6. Create task.
        7. Verify created task.
        8. Write a point to a bucket the data is read from.
        9. Verify data was written to kafka.
        10. Verify data was written to storage.
        11. Query written data using gateway endpoint.
        12. Wait for task to be executed.
        13. Verify data was written to kafka.
        14. Verify data was written to a bucket we wrote a data to.
        15. Query the data from a bucket the data was written to.
        """
        test_name = 'test_tasks_smoke '
        org_name = 'test_tasks_smoke_org'
        bucket_name_destination = 'test_tasks_smoke_bucket_dest'
        bucket_name_source = 'test_tasks_smoke_bucket_source'
        user_name = 'test_tasks_smoke_user'
        task_description = 'task_description'
        task_status = 'active'
        task_name = 'test_task_smoke_name'
        task_duration = '30s'

        data = [] # to store the data that made it to kafka, initial value is empty list
        err = '' # initially there is no error
        task_tag = 'taskcreation'
        measurement = 'task_m'
        value = '1234'
        tag = 'qa_great'
        result_gateway = {}
        final_kafka_points = ''
        final_storage_points = ''

        self.header(test_name)
        self.mylog.info(test_name + 'STEP 1: Create Organization')
        self.mylog.info(test_name + '\n')
        create_org = org_util.create_organization(self, self.gateway, org_name)
        status = create_org.get('status')
        _assert(self, status, 201, 'RESPONSE STATUS')
        org_id = create_org.get('org_id')
        org_name = create_org.get('org_name')
        verify_org_etcd_entries(self, test_name, org_id, org_name, error='')

        # create bucket to read data from - source bucket
        self.mylog.info(test_name + 'STEP 2: Create Bucket To Read Data From')
        self.mylog.info(test_name + '\n')
        create_bucket_source = buckets_util.create_bucket(self, self.gateway, bucket_name_source,
                                                          organization_id=org_id)
        status = create_bucket_source.get('status')
        _assert(self, status, 201, 'RESPONSE STATUS')
        bucket_id_created_source = create_bucket_source.get('bucket_id')
        bucket_name_created_source = create_bucket_source.get('bucket_name')
        verify_bucket_etcd_entries(self, test_name, bucket_id_created_source, bucket_name_created_source, 0,
                                   expected_error='')

        # create bucket to write data to
        self.mylog.info(test_name + 'STEP 3: Create Bucket To Write Data To')
        self.mylog.info(test_name + '\n')
        create_bucket_dest = buckets_util.create_bucket(self, self.gateway, bucket_name_destination,
                                                      organization_id=org_id)
        status = create_bucket_dest.get('status')
        _assert(self, status, 201, 'RESPONSE STATUS')
        bucket_id_created_dest = create_bucket_dest.get('bucket_id')
        bucket_name_created_dest = create_bucket_dest.get('bucket_name')
        verify_bucket_etcd_entries(self, test_name, bucket_id_created_dest, bucket_name_created_dest, 0,
                                   expected_error='')

        # create user
        self.mylog.info(test_name + 'STEP 4: Create User')
        self.mylog.info(test_name + '\n')
        create_user = gateway_util.create_user(self, self.gateway, user_name)
        status = create_user[0]
        _assert(self, status, 201, 'RESPONSE STATUS')
        user_id = create_user[1]
        user_name = create_user[2]
        verify_user_etcd_entries(self, test_name, user_id, user_name, expected_error='')

        # give user permissions
        self.mylog.info(test_name + 'STEP 5: Create Authorization Token For Tasks/Write And Read Operations')
        self.mylog.info(test_name + '\n')
        tasks_permissions = [{"action": "create", "resource": "org/%s/task" % org_id},
                             {"action": "read", "resource": "bucket/%s" % bucket_id_created_source},
                             {"action": "write", "resource": "bucket/%s" % bucket_id_created_dest}]

        write_permissions = [{"action": "write", "resource": "bucket/%s" % bucket_id_created_source}]

        read_permissions = [{"action": "write", "resource": "bucket/%s" % bucket_id_created_dest},
                            {"action": "read", "resource": "bucket/%s" % bucket_id_created_source}]

        create_tasks_permissions = \
            gateway_util.create_authorization(self, self.gateway, user_name, user_id, json.dumps(tasks_permissions))
        status = create_tasks_permissions.get('status')
        _assert(self, status, 201, 'RESPONSE STATUS')
        tasks_token = create_tasks_permissions.get('token')

        create_write_permissions = \
            gateway_util.create_authorization(self, self.gateway, user_name, user_id, json.dumps(write_permissions))
        status = create_write_permissions.get('status')
        _assert(self, status, 201, 'RESPONSE STATUS')
        write_token = create_write_permissions.get('token')

        create_read_permissions = \
            gateway_util.create_authorization(self, self.gateway, user_name, user_id, json.dumps(read_permissions))
        status = create_read_permissions.get('status')
        _assert(self, status, 201, 'RESPONSE STATUS')
        read_token = create_read_permissions.get('token')

        self.mylog.info(test_name + 'STEP 6: Create Task')
        self.mylog.info(test_name + '\n')
        flux_script = 'option task = {name:"%s", every:%s} from(bucket:"%s") |> range(start: -1h) ' \
                      '|> map(fn: (r) => ({_time: r._time, _value:r._value, t : "%s"}))' \
                      '|> to(bucket:"%s", orgID:"%s")' % \
                      (task_name, task_duration, bucket_name_source, task_tag, bucket_name_destination, org_id)

        create_task = tasks_util.create_task(self, self.gateway, org_id, task_description, tasks_token, task_status,
                                             flux=flux_script)
        time_task_created = time.time()
        self.mylog.info(test_name + 'TASK WAS CREATED AT : ' + str(datetime.now()))
        status = create_task.get('status')
        _assert(self, status, 201, 'RESPONSE STATUS')
        task_id = create_task.get('task_id')

        # query etcd-tasks
        etcd_tasks = gateway_util.get_tasks_etcd(self, self.etcd_tasks, task_id)
        self.mylog.info(test_name + 'ETCD TASKS RESULT : ' + str(etcd_tasks))

        self.mylog.info(test_name + 'STEP 7: Verify Created Task')
        self.mylog.info(test_name + '\n')
        _assert(self, etcd_tasks.get('flux_script'), flux_script, 'FLUX SCRIPT')
        _assert(self, etcd_tasks.get('task_name'), task_name, 'TASK_NAME')
        _assert(self, etcd_tasks.get('org_id'), org_id, 'ORG ID')
        _assert(self, etcd_tasks.get('user_id'), user_id, 'USER ID')
        _assert(self, etcd_tasks.get('status'), task_status, 'TASK STATUS')
        _assert(self, etcd_tasks.get('schedule'), 'every %s' % task_duration, 'TASK SCHEDULE')

        # write a point
        self.mylog.info(test_name + 'STEP 8: Write a point')
        self.mylog.info(test_name + '\n')
        write_result = gateway_util.write_points(self, self.gateway, write_token, org_name, bucket_name_source,
                                                 data='%s,t=%s f=%s' % (measurement, tag, value))
        _assert(self, write_result.get('status'), 204, 'Write Data Point To A Bucket')
        _assert(self, write_result.get('error'), '', 'Write Data Error Message')

        self.mylog.info(test_name + 'STEP 9: Verify Data Was Written To Kafka')
        self.mylog.info(test_name + '\n')

        end_time = time.time() + 10 # data should be written to kafka right away, but give it up to 10 sec
        while time.time() <= end_time:
            topics, data, err = gateway_util.kafka_find_data_by_tag(self, self.kubeconf, self.kubecluster,
                                                                    self.namespace, tag, 'kafka-0')
            if len(data) == 0: # kafka does not have any data, usually new deployments
                self.mylog.info(test_name + 'KAFKA DOES NOT HAVE THE DATA YET. SLEEPING FOR 1 SECOND')
                time.sleep(1)
                continue
            else:
                for point in data:
                    if tag in point:
                        final_kafka_points += point
                        self.mylog.info(test_name + 'KAFKA DOES HAVE THE DATA: ' + str(point))
                        break
                else: # there is already data in kafka, but the data we are looking for is not there yet.
                    self.mylog.info('KAFKA DOES NOT HAVE THE DATA YET')
                    continue
                break
        _assert(self, err, '', 'ERROR GETTING DATA FROM KAFKA')
        _assert(self, len(data) > 0, True, 'KAFKA DOES NOT HAVE THE DATA')
        _assert(self, tag in final_kafka_points, True, 'KAFKA DOES NOT HAVE THE DATA')

        # storage is pulling every 10 seconds from kafka
        self.mylog.info(test_name + 'STEP 10: Verify Data Was Written To Storage')
        end_time = time.time() + 20
        while time.time() <= end_time:
            engine, data, err = gateway_util.storage_find_data(self, self.kubeconf, self.kubecluster, self.namespace,
                                                               tag, 'storage-0')
            if len(data) == 0: # storage does not have any data yet, new deployments
                self.mylog.info(test_name + 'STORAGE DOES NOT HAVE THE DATA YET. SLEEPING FOR 1 SECOND')
                time.sleep(1)
                continue
            else:
                for point in data:
                    if tag in point:
                        final_storage_points += point
                        self.mylog.info(test_name + 'STORAGE DOES HAVE THE DATA: ' + str(point))
                        break
                else: # storage has some data, but data we are looking for is not there yet.
                    self.mylog.info('STORAGE DOES NOT HAVE THE DATA YET')
                    continue
                break
        _assert(self, err, '', 'ERROR GETTING DATA FROM STORAGE')
        _assert(self, len(data) > 0, True, 'STORAGE DOES NOT HAVE THE DATA')
        _assert(self, tag in final_storage_points, True, 'STORAGE DOES NOT HAVE THE DATA')

        # query the data from a bucket
        self.mylog.info(test_name + 'STEP 11: Query Data using Gateway')
        self.mylog.info(test_name + '\n')
        query_out = 'from(bucket:"%s") |> range(start:-5m)' % bucket_name_source
        end_time = time.time() + 15 # should happen right away, since data is already in storage
        while time.time() <= end_time:
            result_gateway = gateway_util.gateway_query_data(self, query_out, self.gateway, read_token, org_name)
            if result_gateway.get('status') == 200 and len(result_gateway.get('result')) == 1:
                break
            else:
                self.mylog.info(test_name + 'WAITING FOR QUERY RESULTS. SLEEPING 1 SECOND')
                time.sleep(1)
        _assert(self, result_gateway.get('status'), 200, ' STATUS CODE')
        _assert(self, len(result_gateway.get('result')), 1, ' NUMBER OF RECORDS')
        _assert(self, result_gateway.get('result')[0].get('_measurement'), measurement, 'Measurement')
        _assert(self, result_gateway.get('result')[0].get('_value'), value, 'Field Value')
        _assert(self, result_gateway.get('result')[0].get('t'), tag, 'Tag Value')

        # Wait for task service to execute the flux query
        query_in = 'from(bucket:"%s") |> range(start:-5m)' % bucket_name_destination
        # task wil start running at the end of the 'end_time', which is time task was created + 40 sec, since task will
        # start running for the first time after its scheduled time passes, that is 30sec.
        self.mylog.info(test_name + 'STEP 12: Wait For Task To Be Executed')
        self.mylog.info(test_name + '\n')
        end_time = time_task_created + 40
        while time.time() < end_time:
            time.sleep(1)

        self.mylog.info(test_name + 'STEP 13: Verify Data Was Written To Kafka')
        self.mylog.info(test_name + '\n')
        final_kafka_points = ''
        end_time = time.time() + 10
        while time.time() <= end_time:
            topics, data, err = gateway_util.kafka_find_data_by_tag(self, self.kubeconf, self.kubecluster,
                                                                    self.namespace, task_tag, 'kafka-0')
            if len(data) == 0:
                self.mylog.info(test_name + 'KAFKA DOES NOT HAVE THE DATA YET. SLEEPING 1 SECOND.')
                time.sleep(1)
                continue
            else:
                for point in data:
                    if task_tag in point and not 'task-system' in point:
                        final_kafka_points += point
                        self.mylog.info(test_name + 'KAFKA DOES HAVE THE DATA:' + str(point))
                        break
                else:
                    self.mylog.info(test_name + 'KAFKA DOES NOT HAVE THE DATA YET')
                    continue
                break
        _assert(self, err, '', 'ERROR GETTING DATA FROM KAFKA')
        _assert(self, len(data) > 0, True, 'KAFKA DOES NOT HAVE THE DATA')
        _assert(self, task_tag in final_kafka_points, True, 'KAFKA DOES NOT HAVE THE DATA')

        # storage is pulling every 10 seconds from kafka
        self.mylog.info(test_name + 'STEP 14: Verify Data Was Written To Storage')
        self.mylog.info(test_name + '\n')
        final_storage_points = ''
        end_time = time.time() + 20
        while time.time() <= end_time:
            engine, data, err = gateway_util.storage_find_data(self, self.kubeconf, self.kubecluster,
                                                               self.namespace, task_tag, 'storage-0')
            if len(data) == 0:
                self.mylog.info(test_name + 'STORAGE DOES NOT HAVE THE DATA YET. SLEEPING 1 SECOND')
                time.sleep(1)
                continue
            else:
                for point in data:
                    if task_tag in point and not 'task-system' in point:
                        final_storage_points += point
                        self.mylog.info(test_name + 'STORAGE DOES HAVE THE DATA:' + str(point))
                        break
                else:
                    self.mylog.info(test_name + 'STORAGE DOES NOT HAVE THE DATA YET')
                    continue
                break
        _assert(self, err, '', 'ERROR GETTING DATA FROM STORAGE')
        _assert(self, len(data) > 0, True, 'STORAGE DOES NOT HAVE THE DATA')
        _assert(self, task_tag in final_storage_points, True, 'STORAGE DOES NOT HAVE THE DATA')

        self.mylog.info(test_name + 'STEP 15: Query Data Using Gateway')
        self.mylog.info(test_name + '\n')
        end_time = time.time() + 30
        while time.time() <= end_time:
            result_gateway = gateway_util.gateway_query_data(self, query_in, self.gateway, read_token, org_name)
            if result_gateway.get('status') == 200 and len(result_gateway.get('result')) == 1:
                break
            else:
                self.mylog.info(test_name + 'WAITING FOR QUERY RESULTS. SLEEPING 2 SECOND')
                time.sleep(2)
        _assert(self, result_gateway.get('status'), 200, ' STATUS CODE')
        _assert(self, len(result_gateway.get('result')), 1, ' NUMBER OF RECORDS')
        _assert(self, result_gateway.get('result')[0].get('_measurement'), measurement, 'Measurement')
        _assert(self, result_gateway.get('result')[0].get('_value'), value, 'Field Value')
        _assert(self, result_gateway.get('result')[0].get('t'), task_tag, 'Tag Value')