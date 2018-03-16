
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
parser.add_option('--datanode', action='store', help='URL OF THE DATA NODE, e.g. http://datanode:8086')
parser.add_option('--metanode', action='store', help='URL OF THE META NODE, e.g. http://metanode:8091')
parser.add_option('--kapacitor', action='store', help='KAPACITOR URL, e.g. http://kapacitor9092:')

# tests to run
parser.add_option('--tests', action='append', dest='tests', help='')
# add test lists

(options, args)=parser.parse_args()
pytest_parameters=[]

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

# Installation part goes here
#return_code=subprocess.call('install script goes here', shell=True, stdout=File)

if options.chronograf is not None: pytest_parameters.append('--chronograf=' + options.chronograf)
else: pass # get chronograf URL from pcl list -c <cluster>
if options.datanode is not None: pytest_parameters.append('--datanode=' + options.datanode)
else: pass # get data-node URL from pcl list -c <cluster>
if options.metanode is not None: pytest_parameters.append('--metanode=' + options.metanode)
else: pass # get meta-node URL from pcl list -c <cluster>
if options.kapacitor is not None: pytest_parameters.append('--kapacitor=' + options.kapacitor)
else: pass # get kapacitor URL from pcl list -c <cluster>


data_node=['http://54.190.199.92:8086', 'http://1.2.3.4:8086']
data_node_str=' '.join(data_node)
print data_node_str
pytest_parameters.append('--datanodes=' + data_node_str)
meta_node=['http://34.217.16.7:8091', '1.2.3.4.5']
meta_node_str=' '.join(meta_node)
pytest_parameters.append('--metanodes=' + meta_node_str)

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

