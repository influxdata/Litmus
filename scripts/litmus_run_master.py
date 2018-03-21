
#1. Install necessary modules if they are missing
#2. add option parser for parsing options to pytest, pcl (installer), for running REST tests.
    #(in the future more options will be added, e.g. for influxDB CLI)
#3. Collect all relevant product logs (if any)
#4. Call pytest to run tests


import optparse, os, sys, pytest, subprocess

MasterScriptDir=os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(MasterScriptDir, 'src'))

print 'SYSTEM PATH : ' + str(sys.path)

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

parser.add_option('--clustername', action='store', help='NAME OF THE CLUSTER')
parser.add_option('--clusterenv', action='store', help='ENVIRONMENT VARS TO PASS TO INSTALL SCRIPT')
parser.add_option('--localpkgdata', action='store', help='LOCAL DATA PACKAGE TO INSTALL')
parser.add_option('--localpkgmeta', action='store', help='LOCAL META PACKAGE TO INSTALL')
parser.add_option('--dbversion', action='store', help='INFLUXDB VERSION TO INSTALL')
parser.add_option('--num_datanodes', action='store', help='NUMBER OF DATA NODES')
parser.add_option('--num_metanodes', action='store', help='NUMBEROF META NODES')

# tests to run
parser.add_option('--tests', action='append', dest='tests', help='')
# add test lists

(options, args)=parser.parse_args()
pytest_parameters=[]

# install options
cluster_name=options.clustername
cluster_env=options.clusterenv
data_pkg=options.localpkgdata
meta_pkg=options.localpkgmeta
db_version=options.dbversion
data_nodes_number=options.num_datanodes
meta_nodes_number=options.num_metanodes


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

# Installation of the TICK stack
print './qa_install_tick.sh --c %s --d %s --m %s --e %s --db-version %s' % (cluster_name, data_nodes_number, meta_nodes_number, cluster_env, db_version)
return_code=subprocess.call('./qa_install_tick.sh --c %s --d %s --m %s --e %s --db-version %s' % (cluster_name, data_nodes_number, meta_nodes_number, cluster_env, db_version), shell=True)
exit(0)

if options.chronograf is not None:
    pytest_parameters.append('--chronograf=' + options.chronograf)
else:
    pass
if options.datanodes is not None:
    data_node_str=options.datanodes
else: # get data-node URL from pcl list -c <cluster>s
    data_nodes=['34.217.102.209','54.218.122.160']
    data_node_str=','.join(data_nodes)
pytest_parameters.append('--datanodes=' + data_node_str)
if options.metanodes is not None:
    meta_node_str=options.metanodes
else: # get meta-node URL from pcl list -c <cluster>
    meta_nodes = ['54.202.76.159', '54.202.5.229','52.42.51.117']
    meta_node_str = ','.join(meta_nodes)
pytest_parameters.append('--metanodes=' + meta_node_str)
if options.kapacitor is not None:
    kapacitor_str=options.kapacitor
    pytest_parameters.append('--kapacitor=' + options.kapacitor)
else:
    kapacitor=['54.71.255.156']
    kapacitor_str=','.join(kapacitor)
pytest_parameters.append('--kapacitor=' + kapacitor_str)

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

