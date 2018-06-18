

from subprocess import Popen
from subprocess import PIPE
import time
import sys
import traceback


def execCmd(test_class_instance, cmd, status='EXIT_STATUS', timeout=600):
    '''
    :param test_class_instance:
    :param cmd: (str) command to execute
    :param status (str): by default return EXIST STATUS, or SDTOUT, or STDERR
    :param timeout: (int) time in sec to wait for command to exit (default 10 min)
    :return: exit status, stdout or sdterr
    '''
    EXIT_STATUS=1
    OUT_STATUS=None
    ERR_STATUS=None

    test_class_instance.mylog.info('litmus_util.execCmd - status=' + str(status))
    test_class_instance.mylog.info('litmus_util.execCmd Executing \'%s\' command' % cmd)
    test_class_instance.mylog.info('litmus_util.execCmd timeout is %s' % str(timeout))
    time_end=time.time() + timeout
    try:
        result = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        while time.time() <= time_end:
            # Wait for command to complete
            if result.poll() == None:
                test_class_instance.mylog.info('litmus_util.execCmd - sleeping for 1 sec')
                time.sleep(1)
                continue
            else:
                break
        # TODO handle timeouts
        EXIT_STATUS=result.poll()
        test_class_instance.mylog.info('litmus_util.execCmd - EXIT_STATUS=' + str(EXIT_STATUS))
        OUT_STATUS, ERR_STATUS=result.communicate()
        test_class_instance.mylog.info('litmus_util.execCmd - OUT_STATUS=' + str(OUT_STATUS))
        test_class_instance.mylog.info('litmus_util.execCmd - ERR_STATUS=' + str(ERR_STATUS))
    except:
        clt_error_type, clt_error_message, clt_error_traceback = sys.exc_info()
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(traceback.extract_tb(clt_error_traceback)))
        test_class_instance.mylog.info('litmus_util.execCmd:' + str(clt_error_message))
    if status == 'EXIT_STATUS':
        return EXIT_STATUS
    else:
        return (OUT_STATUS, ERR_STATUS)

def shard_layout(test_class_instance, privatekey, install_dir, database_name, retention_policy, shards_id, user, host):
    '''
    :param test_class_instance:
    :param database_name:
    :param retention_policy:
    :param shards_id:
    :return:
    '''
    test_class_instance.mylog.info('litmus_util.shard_layout() function is called')
    test_class_instance.mylog.info('---------------------------------------------')
    test_class_instance.mylog.info('')
    test_class_instance.mylog.info('litmus_util.shard_layout - argumets: privatekey \'%s\', installation dir \'%s\', '
                                   'database name \'%s\', retention policy \'%s\', shard_id \'%s\', user \'%s\' and'
                                   ' host \'%s\'' % (privatekey, install_dir, database_name, retention_policy,
                                                     shards_id, user, host))
    # build up the path to a shard
    path_to_shard=install_dir+'/'+database_name+'/'+retention_policy+'/'+shards_id
    test_class_instance.mylog.info('litmus_util.shard_layout - path \'%s\'' % path_to_shard )
    cmd='ssh -i %s -o StrictHostKeyChecking=no %s@%s \'sudo ls -l %s\'' % (privatekey, user, host, path_to_shard )
    output=execCmd(test_class_instance, cmd, status='OUT_STATUS')
    return output
