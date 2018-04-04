
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
parser.add_option('--verbose', action='store', dest='verbose', help='INCREASE VERBOSITY OF PYTEST')
parser.add_option('--resultxml', action='store', dest='junitXml', help='CREATE junit-xml STYLE REPORT FILE AT A GIVEN PATH')
parser.add_option('--nocapture', action='store', dest='nocapture', help='')
parser.add_option('--traceback', action='store', dest='traceback', help='')
parser.add_option('--testsubset', action='store', dest='testsubset', help='')

# options for running REST tests (By default these options will be derived from the output o the pcl list command
parser.add_option('--chronograf', action='store', help='CHRONOGRAF BASE URL, e.g. http://localhost:8888')
parser.add_option('--datanodes', action='store', help='URL OF THE DATA NODE, e.g. http://datanode:8086')
parser.add_option('--metanodes', action='store', help='URL OF THE META NODE, e.g. http://metanode:8091')
parser.add_option('--kapacitor', action='store', help='KAPACITOR URL, e.g. http://kapacitor:9092:')

# install options for cluster
parser.add_option('--cluster-name', action='store', dest='clustername', help='NAME OF THE CLUSTER')
parser.add_option('--cluster-env', action='store', dest='clusterenv', help='ENVIRONMENT VARS TO PASS TO INSTALL SCRIPT')
parser.add_option('--pkg-data', action='store', dest='localpkgdata', help='LOCAL DATA PACKAGE TO INSTALL')
parser.add_option('--pkg-meta', action='store', dest='localpkgmeta', help='LOCAL META PACKAGE TO INSTALL')
parser.add_option('--influxdb-version', action='store', dest='dbversion',help='INFLUXDB VERSION TO INSTALL')
parser.add_option('--num-data', action='store', dest='num_datanodes', help='NUMBER OF DATA NODES')
parser.add_option('--num-meta', action='store', dest='num_metanodes', help='NUMBEROF META NODES')
parser.add_option('--telegraf-version', action='store', dest='telegrafversion', help='INSTALL VERSION OF TELEGRAF')
parser.add_option('--cluster-os', action='store', dest='clusteros', help='OS TO INSTALL THE CLUSTER ON')

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
cluster_env=options.clusterenv
if cluster_env is not None: cluster_env='--cluster-env ' + options.clusterenv
else: cluster_env=''
data_pkg=options.localpkgdata
if data_pkg is not None: data_pkg='--pkg-data ' + options.localpkgdata
else: data_pkg=''
meta_pkg=options.localpkgmeta
if meta_pkg is not None: meta_pkg='--meta-pkg ' + options.localpkgmeta
else: meta_pkg=''
db_version=options.dbversion
if db_version is not None: db_version='--influxdb-version ' + options.dbversion
else: db_version=''
data_nodes_number=options.num_datanodes
# need to get list of all data nodes
num_of_data_nodes=data_nodes_number
if data_nodes_number is not None: data_nodes_number='--num-data ' + options.num_datanodes
else: data_nodes_number=''
meta_nodes_number=options.num_metanodes
# need to get a list of meta nodes
num_of_meta_nodes=meta_nodes_number
if meta_nodes_number is not None: meta_nodes_number='--num-meta ' + options.num_metanodes
else: meta_nodes_number=''
telegraf_version=options.telegrafversion
if telegraf_version is not None: telegraf_version='--telegraf-version ' + options.telegrafversion
else: telegraf_version=''
cluster_os=options.clusteros
if cluster_os is not None: cluster_os='--cluster-os ' + cluster_os
else: cluster_os=''

# chronograf install options
chronograf_version=options.chronografversion
if chronograf_version is not None: chronograf_version='--chronograf-version ' + chronograf_version
else: chronograf_version=''
num_chronografs=options.numchronografs
if num_chronografs is not None: num_chronografs='--num-instances ' + num_chronografs
else: num_chronografs=''
chronograf_os=options.chronografos
if chronograf_os is not None: chronograf_os='--aws-os ' + chronograf_os
else: chronograf_os=''
no_chronograf=options.nochronograf
if no_chronograf is not False: no_chronograf='--no-chronograf '
else: no_chronograf=''


# kapacitor install options
kapacitor_version=options.kapacitorversion
if kapacitor_version is not None: kapacitor_version='--kapacitor-version ' + kapacitor_version
else: kapacitor_version=''
num_kapacitor=options.numkapacitors
if num_kapacitor is not None: num_kapacitor='--num-instances ' + num_kapacitor
else: num_kapacitor=''
kapacitor_os=options.kapacitoros
if kapacitor_os is not None: kapacitor_os='--aws-os ' + kapacitor_os
else: kapacitor_os=''
no_kapacitor=options.nokapacitor
if no_kapacitor is not False: no_kapacitor='--no-kapacitor '
else: no_kapacitor=''

if options.verbose is not None: pytest_parameters.append(options.verbose)
if options.verbose is None: pytest_parameters.append('-v')
if options.junitXml is not None: pytest_parameters.append(options.junitXml)
if options.junitXml is None: pytest_parameters.append('--junitxml=result.xml')
if options.testsubset is not None: pytest_parameters.append(options.testsubset)
if options.nocapture is not None: pytest_parameters.append(options.nocapture)
if options.nocapture is None: pytest_parameters.append('-s')
if options.traceback is not None: pytest_parameters.append(options.traceback)
if options.traceback is None: pytest_parameters.append('--tb=short')
pytest_parameters.append('--disable-pytest-warnings')
pytest_parameters.append('-rxfX')
pytest_parameters.append('--html=report.html')

File=None
try:
	File = open('qa_install_tick.out','w')
except	IOError as e:
	print 'IO ERROR ({0}): {1}'.format(e.errno,e.strerror)
	print 'IO ERROR ({0}): '.format(e.message)
        exit(1)

#Installation of the TICK stack
print 'INSTALLING TICK STACK'
print '---------------------'
print r'./qa_install_tick.sh %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s' % (cluster_name, data_nodes_number, meta_nodes_number, cluster_env, db_version, data_pkg, meta_pkg, telegraf_version, cluster_os, chronograf_version, num_chronografs, chronograf_os, no_chronograf, kapacitor_version, num_kapacitor, kapacitor_os, no_kapacitor)
return_code=subprocess.call('./qa_install_tick.sh %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s' % (cluster_name, data_nodes_number, meta_nodes_number, cluster_env, db_version, data_pkg, meta_pkg, telegraf_version, cluster_os,  chronograf_version, num_chronografs, chronograf_os, no_chronograf, kapacitor_version, num_kapacitor, kapacitor_os, no_kapacitor),shell=True, stdout=File)
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
