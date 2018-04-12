
#1. Install necessary modules if they are missing
#2. add option parser for parsing options to pytest, pcl (installer), for running REST tests.
    #(in the future more options will be added, e.g. for influxDB CLI)
#3. Collect all relevant product logs (if any)
#4. Call pytest to run tests

import pkgutil
import subprocess

PIP_CMD = 'sudo -H pip install --no-cache-dir'
MODULES = ['pytest','requests','python-dateutil','pytest-html','pytest-metadata']
for module in MODULES:
    if None == pkgutil.find_loader(module):
        if module == 'requests':
            proc = subprocess.call('%s %s[security]==2.17.3' % (PIP_CMD, module), shell=True)
            assert proc == 0, 'FAILED TO INSTALL %s' % module
        elif module == 'pytest':
            proc = subprocess.call('%s %s==3.0.7' % (PIP_CMD, module), shell=True)
            assert proc == 0, 'FAILED TO INSTALL %s' % module
        elif module == 'python-dateutil':
            proc = subprocess.call('%s %s==2.6.1' % (PIP_CMD, module), shell=True)
            assert proc == 0, 'FAILED TO INSTALL %s' % module
        elif module == 'pytest-html':
            proc = subprocess.call('%s %s==1.16.0' % (PIP_CMD, module), shell=True)
            assert proc == 0, 'FAILED TO INSTALL %s' % module
        elif module == 'pytest-metadata':
            proc = subprocess.call('%s %s==1.5.0' % (PIP_CMD, module), shell=True)
            assert proc == 0, 'FAILED TO INSTALL %s' % module

import os, sys

MasterScriptDir=os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(MasterScriptDir, 'src'))

print 'SYSTEM PATH : ' + str(sys.path)

import optparse,  pytest
# add script options
usage='%prog[options]'
parser=optparse.OptionParser(usage=usage)

# pytest options
parser.add_option('--testsubset', action='store', dest='testsubset', help='LET\'S YOU ONLY RU NTHE TESTS MARKED WITH MARKER')

# options for running REST tests (By default these options will be derived from the output o the pcl list command
parser.add_option('--chronograf', action='store', help='CHRONOGRAF BASE URL, e.g. http://localhost:8888')
parser.add_option('--datanodes', action='store', help='URL OF THE DATA NODE, e.g. http://datanode:8086')
parser.add_option('--metanodes', action='store', help='URL OF THE META NODE, e.g. http://metanode:8091')
parser.add_option('--kapacitor', action='store', help='KAPACITOR URL, e.g. http://kapacitor:9092:')

# install options for cluster
parser.add_option('--cluster-name', action='store', dest='clustername', help='NAME OF THE CLUSTER')
parser.add_option('--cluster-env', action='store', dest='clusterenv', help='ENVIRONMENT VARS TO PASS TO INSTALL SCRIPT')
parser.add_option('--pkg-data', action='store', dest='localpkgdata', help='LOCAL DATA PACKAGE TO INSTALL')
parser.add_option('--index-version', action='store', dest='indexversion', help='tsi1 OR inmem INDEX')
parser.add_option('--pkg-meta', action='store', dest='localpkgmeta', help='LOCAL META PACKAGE TO INSTALL')
parser.add_option('--http-auth', action='store_true', dest='httpauth', default=False, help='ENABLE AUTHENTICATION')
parser.add_option('--admin-user', action='store', dest='adminuser', help='NAME OF THE ADMIN USER')
parser.add_option('--admin-pass', action='store', dest='adminpass', help='PASSWORD OF THE ADMIN USER')
parser.add_option('--influxdb-version', action='store', dest='dbversion',help='INFLUXDB VERSION TO INSTALL')
parser.add_option('--num-data', action='store', dest='num_datanodes', help='NUMBER OF DATA NODES')
parser.add_option('--num-meta', action='store', dest='num_metanodes', help='NUMBEROF META NODES')
parser.add_option('--telegraf-version', action='store', dest='telegrafversion', help='INSTALL VERSION OF TELEGRAF')
parser.add_option('--cluster-os', action='store', dest='clusteros', help='OS TO INSTALL THE CLUSTER ON')
parser.add_option('--no-install', action='store_true', dest='noinstall', default=False, help='DO NOT INSTALL TH ETICK STACK')

# install optins for chronograf
parser.add_option('--chronograf-version', action='store', dest='chronografversion', help='VERSION OF CHRONOGRAF TO INSTALL')
parser.add_option('--num-chronografs', action='store', dest='numchronografs', help='NUMBER OF CHRONOGRAF INSTANCES TO INSTALL')
parser.add_option('--chronograf-os', action='store', dest='chronografos', help='OS TO INSTALL CHRONOGRAF ON')
parser.add_option('--no-chronograf', action='store_true', dest='nochronograf', default=False, help='DO NOT INSTALL CHRONOGRAF')

# install options for kapacitor
parser.add_option('--kapacitor-version', action='store', dest='kapacitorversion', help='VERSION OF KAPACITOR TO INSTALL')
parser.add_option('--num-kapacitors', action='store', dest='numkapacitors', help='NUMBER OF KAPACITOR INSTANCES TO INSTALL')
parser.add_option('--kapacitor-os', action='store', dest='kapacitoros', help='OS TO INSTALL KAPACITOR ON')
parser.add_option('--no-kapacitor', action='store_true', dest='nokapacitor', default=False, help='DO NOT INSTALL KAPACITOR')


parser.add_option('--tests', action='append', dest='tests', help='')
# add test lists

(options, args)=parser.parse_args()
pytest_parameters=[]

# cluster install options
cluster_name=options.clustername
if cluster_name is None: cluster_name=''
if options.clusterenv is not None: cluster_env='--cluster-env ' + options.clusterenv
else: cluster_env=''
if options.localpkgdata is not None: data_pkg='--pkg-data ' + options.localpkgdata
else: data_pkg=''
if options.localpkgmeta is not None: meta_pkg='--pkg-meta ' + options.localpkgmeta
else: meta_pkg=''
if options.dbversion is not None: db_version='--influxdb-version ' + options.dbversion
else: db_version=''
# need to get list of all data nodes
num_of_data_nodes=options.num_datanodes
if options.num_datanodes is not None: data_nodes_number='--num-data ' + options.num_datanodes
else: data_nodes_number=''
# need to get a list of meta nodes
num_of_meta_nodes=options.num_metanodes
if options.num_metanodes is not None: meta_nodes_number='--num-meta ' + options.num_metanodes
else: meta_nodes_number=''
if options.telegrafversion is not None: telegraf_version='--telegraf-version ' + options.telegrafversion
else: telegraf_version=''
if options.clusteros is not None: cluster_os='--cluster-os ' + options.clusteros
else: cluster_os=''
if options.indexversion is not None: index_version='--index-version ' + options.indexversion
else: index_version=''
if options.httpauth is not False:
    http_auth='--http-auth'
    pytest_parameters.append('--httpauth=' + 'AUTH')
else:
    http_auth=''
    pytest_parameters.append('--httpauth=' + '')
if options.adminuser is not None:
    admin_user='--admin-user ' + options.adminuser
    pytest_parameters.append('--adminuser=' +  options.adminuser)
else: admin_user=''
if options.adminpass is not None:
    admin_pass='--admin-pass ' + options.adminpass
    pytest_parameters.append('--adminpass=' +  options.adminuser)
else: admin_pass=''
if options.noinstall is not False: no_install='--no-install'
else: no_install=''

# chronograf install options
if options.chronografversion is not None: chronograf_version='--chronograf-version ' + options.chronografversion
else: chronograf_version=''
if options.numchronografs is not None: num_chronografs='--num-chronografs ' + options.numchronografs
else: num_chronografs=''
if options.chronografos is not None: chronograf_os='--chronograf-os ' + options.chronografos
else: chronograf_os=''
if options.nochronograf is not False: no_chronograf='--no-chronograf '
else: no_chronograf=''

# kapacitor install options
if options.kapacitorversion is not None: kapacitor_version='--kapacitor-version ' + options.kapacitorversion
else: kapacitor_version=''
if options.numkapacitors is not None: num_kapacitor='--num-kapacitors ' + options.numkapacitors
else: num_kapacitor=''
if options.kapacitoros is not None: kapacitor_os='--kapacitor-os ' + options.kapacitoros
else: kapacitor_os=''
if options.nokapacitor is not False: no_kapacitor='--no-kapacitor '
else: no_kapacitor=''

pytest_parameters.append('-v')
pytest_parameters.append('--junitxml=result.xml')
if options.testsubset is not None: pytest_parameters.append(options.testsubset)
pytest_parameters.append('-s')
pytest_parameters.append('--tb=short')
pytest_parameters.append('--disable-pytest-warnings')
pytest_parameters.append('-rxfX')
pytest_parameters.append('--html=report.html')

File=None
try:
    File = open('qa_install_tick.out','w')
except IOError as e:
    print 'IO ERROR ({0}): {1}'.format(e.errno,e.strerror)
    print 'IO ERROR ({0}): '.format(e.message)
    exit(1)

#Installation of the TICK stack
print 'INSTALLING TICK STACK'
print '---------------------'
print r'./qa_install_tick.sh %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s' % (cluster_name, data_nodes_number,
                                                    meta_nodes_number, cluster_env, db_version, data_pkg, meta_pkg, telegraf_version,
                                                    cluster_os, chronograf_version, num_chronografs, chronograf_os, no_chronograf,
                                                    kapacitor_version, num_kapacitor, kapacitor_os, no_kapacitor, http_auth, admin_user, admin_pass, no_install)
return_code=subprocess.call('./qa_install_tick.sh %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s' % (cluster_name,
                                                    data_nodes_number, meta_nodes_number, cluster_env, db_version, data_pkg, meta_pkg,
                                                    telegraf_version, cluster_os,  chronograf_version, num_chronografs, chronograf_os,
                                                    no_chronograf, kapacitor_version, num_kapacitor, kapacitor_os, no_kapacitor, http_auth,
                                                    admin_user, admin_pass, no_install),shell=True, stdout=File)
if return_code!=0:
    print 'INSTALLATION OF TICK STACK FAILED. SEE qa_install_tick.out FOR DETAILS'
    exit(1)

# get all of the data nodes
list_of_data_nodes=[]
if cluster_name == '': cluster_name='litmus'
for data_node in range(int(num_of_data_nodes)):
    p=subprocess.Popen('pcl host data-%d -c "%s"' %(data_node,cluster_name) ,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if p.wait() != 0:
        print 'FAILED TO GET DATA NODE. EXITING'
        print p.communicate()
        exit (1)
    list_of_data_nodes.append((p.communicate()[0]).strip('\n'))
print '-----------------------------------------------'
print 'LIST OF DATA NODES : ' + str(list_of_data_nodes)
list_of_meta_nodes=[]
for meta_node in range(int(num_of_meta_nodes)):
    p=subprocess.Popen('pcl host meta-%d -c "%s"' %(meta_node,cluster_name) ,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if p.wait() != 0:
        print 'FAILED TO GET META NODE. EXITING'
        print p.communicate()
        exit (1)
    list_of_meta_nodes.append((p.communicate()[0]).strip('\n'))
print '-----------------------------------------------'
print 'LIST OF META NODES : ' + str(list_of_meta_nodes)
p=subprocess.Popen('pcl host chronograf-0 -c %s' %cluster_name, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
if p.wait() != 0:
    print 'FAILED TO GET CHRONOGRAF NODE. EXITING'
    p.communicate()
    exit (1)
chronograf_name=(p.communicate()[0]).strip('\n')
print '---------------------------------------'
print 'CHRONOGRAF IP : ' + str(chronograf_name)
p=subprocess.Popen('pcl host kapacitor-0 -c %s' %cluster_name, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
if p.wait() != 0:
    print 'FAILED TO GET kapacitor NODE. EXITING'
    p.communicate()
    exit (1)
kapacitor_name=(p.communicate()[0]).strip('\n')
print '-------------------------------------'
print 'KAPACITOR IP : ' + str(kapacitor_name)

if options.clustername is not None:
    pytest_parameters.append('--clustername=' + options.clustername)
else:
    pytest_parameters.append('--clustername=litmus')
if options.chronograf is not None:
    pytest_parameters.append('--chronograf=' + options.chronograf)
else:
    pytest_parameters.append('--chronograf=' + chronograf_name)
if options.datanodes is not None:
    data_node_str=options.datanodes
else: 
    # get data-node URL from pcl list -c <cluster>s
	data_node_str=','.join(list_of_data_nodes)
pytest_parameters.append('--datanodes=' + data_node_str)
if options.metanodes is not None:
    meta_node_str=options.metanodes
else: 
    # get meta-node URL from pcl list -c <cluster>
    meta_node_str=','.join(list_of_meta_nodes)
pytest_parameters.append('--metanodes=' + meta_node_str)
if options.kapacitor is not None:
    pytest_parameters.append('--kapacitor=' + options.kapacitor)
else:
    pytest_parameters.append('--kapacitor=' + kapacitor_name)

if options.tests is not None: pytest_parameters.extend(options.tests)
else: print 'There are no tests to run. Exiting', exit(1)

print pytest_parameters

print ''
print '#############################'
print '####### RUNNING TESTS #######'
print ''
exit_code=pytest.main(pytest_parameters)
#get log files
exit(exit_code)
