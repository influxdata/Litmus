
import os, logging, sys, inspect

def log(filename, mode, name):
    '''
    :param filename: name of the log file, i.e. name of the test file + .log
    :param mode: write
    :param name: name of the test
    :return: log object
    '''

    mylog=logging.getLogger(name)
    mylog.setLevel(logging.INFO)
    fh=logging.FileHandler(filename=filename, mode=mode)
    formatter=logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')
    fh.setFormatter(formatter)
    mylog.addHandler(fh)
    return mylog

def get_log_path():
    '''
    :return: path to the log file
    '''

    dir_path=os.path.dirname(os.path.realpath(inspect.getfile(sys._getframe(1))))
    # convert string to list
    dir_path_list=dir_path.split(os.path.sep)
    # find starting point, 'src' directory, and truncate everything after it
    index=dir_path_list.index('src')
    dir_path_list=dir_path_list[0:index]
    dir_path='/'.join(dir_path_list)
    log_name=os.path.splitext(os.path.basename(inspect.getfile(sys._getframe(1))))[0] + '.log'
    log_path=dir_path + os.path.sep + 'result' + os.path.sep + log_name
    return log_path