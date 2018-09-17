
#1. Install necessary modules if they are missing
#2. add option parser for parsing options to pytest, pcl (installer), for running REST tests.
    #(in the future more options will be added, e.g. for influxDB CLI)
#3. Collect all relevant product logs (if any)
#4. Call pytest to run tests

import pkgutil, subprocess, os, sys, optparse, json, time

MasterScriptDir=os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(MasterScriptDir, 'src'))

print 'SYSTEM PATH : ' + str(sys.path)

# add script options
usage='%prog[options]'
parser=optparse.OptionParser(usage=usage)

# version of the influxdata: 1.x (software), 2.0 (cloud)
parser.add_option('--product-version', dest='productversion' ,action='store', help='VERSION OF THE PRODUCT')

# options for running REST tests on 2.0 platform
parser.add_option('--gateway', action='store', help='GATEWAY URL THAT HANDLES EXTERNAL REQUESTS, e.g. http://localhost:9999')
parser.add_option('--flux', action='store', help='QUERY URL THAT HANDLES FLUX REQUESTS, e.g http://localhost:8093')
parser.add_option('--etcd', action='store', help='ETCD URL FOR DISTRIBUTED KEY-VALUE STORE')
parser.add_option('--transpilerde', action='store', help='TRANSPILERDE URL THAT HANDLES REQUESTS TO TRANSLATE INFLUXQL QUERIES TO FLUX')

# options for running REST tests (By default these options will be derived from the output o the pcl list command
# chronograf is supported on both platforms 1.x and 2.0
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
parser.add_option('--private-key', action='store', dest='privatekey', help='Private key file')
parser.add_option('--no-install', action='store_true', dest='noinstall', default=False, help='DO NOT INSTALL TH ETICK STACK')
parser.add_option('--ldap-auth', action='store_true', dest='ldapauth', default=False, help='Enable LDAP authentication')
parser.add_option('--meta-auth', action='store_true', dest='metaauth', default=False, help='Enable META NODE authentication')

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


parser.add_option('--tests', action='append', dest='tests', help='path to test suite(s) to be run')
parser.add_option('--tests-list', action='store',dest='testslist',help='list containing the test suites to be run')
parser.add_option('--mark-test', action='store', dest='marktest', help='mark a test function with custom metadata')

(options, args)=parser.parse_args()
pytest_parameters=[]

# product version
if options.productversion is None: prod_version='1'
else: prod_version=options.productversion

# cluster install options
if options.clustername is not None: cluster_name='--cluster-name ' + options.clustername
else: cluster_name=''
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
if options.clusteros is not None:
    cluster_os='--cluster-os ' + options.clusteros
    clusteros=options.clusteros
    pytest_parameters.append('--clusteros=' + options.clusteros)
else:
    cluster_os='' # default OS to install the cluster on is ubuntu
    pytest_parameters.append('--clusteros=' + 'ubuntu')
    clusteros='ubuntu'
if options.privatekey is not None:
    private_key='--private-key ' + options.privatekey
    pytest_parameters.append('--privatekey=' + options.privatekey)
    privatekey=options.privatekey
else:
    private_key=''
    pytest_parameters.append('--privatekey=' + 'gershon-pcl')
    privatekey='gershon-pcl'
if options.indexversion is not None: index_version='--index-version ' + options.indexversion
else: index_version=''
if options.ldapauth is not False:
    ldap_auth='--ldap-auth'
    pytest_parameters.append('--ldapauth=' + 'AUTH')
else:
    ldap_auth=''
    pytest_parameters.append('--ldapauth=' + '')
if options.metaauth is not False:
    meta_auth='--meta-auth'
    pytest_parameters.append('--metaauth=' + 'AUTH')
else:
    meta_auth=''
    pytest_parameters.append('--metaauth=' + '')
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

if options.marktest is not None:
    pytest_parameters.append('-m ' + options.marktest)
pytest_parameters.append('-v')
pytest_parameters.append('--junitxml=result.xml')
pytest_parameters.append('-s')
pytest_parameters.append('--tb=short')
pytest_parameters.append('--disable-pytest-warnings')
pytest_parameters.append('-rxfX')
pytest_parameters.append('--html=report.html')

if prod_version == '1':
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
    print r'./qa_install_tick.sh %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s' % (cluster_name, data_nodes_number,
                                                        meta_nodes_number, cluster_env, db_version, data_pkg, meta_pkg, telegraf_version,
                                                        cluster_os, chronograf_version, num_chronografs, chronograf_os, no_chronograf,
                                                        kapacitor_version, num_kapacitor, kapacitor_os, no_kapacitor, http_auth, admin_user,
                                                        admin_pass, no_install, ldap_auth, meta_auth, private_key)
    return_code=subprocess.call('./qa_install_tick.sh %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s' % (cluster_name,
                                                        data_nodes_number, meta_nodes_number, cluster_env, db_version, data_pkg, meta_pkg,
                                                        telegraf_version, cluster_os,  chronograf_version, num_chronografs, chronograf_os,
                                                        no_chronograf, kapacitor_version, num_kapacitor, kapacitor_os, no_kapacitor, http_auth,
                                                        admin_user, admin_pass, no_install, ldap_auth, meta_auth, private_key),shell=True, stdout=File, stderr=File)
    if return_code!=0:
        print 'INSTALLATION OF TICK STACK FAILED. SEE qa_install_tick.out FOR DETAILS'
        exit(1)

if options.clustername is not None:
    cluster_name=options.clustername
else: cluster_name='litmus'

################
# CLUSTER NAME #
################
if options.clustername is not None:
    pytest_parameters.append('--clustername=' + options.clustername)
else:
    pytest_parameters.append('--clustername=litmus')

######################
# CHRONOGRAF NODE(S) #
######################
if options.chronograf is not None:
    pytest_parameters.append('--chronograf=' + options.chronograf)
    print 'CHRONOGRAF IP : ' + options.chronograf
elif options.nochronograf is not False:
    if prod_version == 1:
        print 'NOT INSTALLING CHRONOGRAF'
        print '-------------------------'
        print ''
    else:
        print 'NOT USING CHRONOGRAF URL'
        print '------------------------'
        print ''
else:
    p=subprocess.Popen('pcl host chronograf-0 -c %s' % cluster_name, shell=True, stdout=subprocess.PIPE,
                      stderr=subprocess.PIPE)
    if p.wait() != 0:
        print 'FAILED TO GET CHRONOGRAF NODE. EXITING'
        print p.communicate()
        exit(1)
    chronograf_name = (p.communicate()[0]).strip('\n')
    print '---------------------------------------'
    print 'CHRONOGRAF IP : ' + str(chronograf_name)
    pytest_parameters.append('--chronograf=' + chronograf_name)


# if product version is 2.0 ('2'), then we need to skip DATA NODES, META NODES and KAPACITOR sections
if prod_version == '1':
    ##############
    # DATA NODES #
    ##############
    if options.datanodes is not None:
        data_node_str=options.datanodes
    else:
        # get data-node URL from pcl list -c <cluster>s
        list_of_data_nodes = []
        for data_node in range(int(num_of_data_nodes)):
            p = subprocess.Popen('pcl host data-%d -c "%s"' % (data_node, cluster_name), shell=True, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            if p.wait() != 0:
                print 'FAILED TO GET DATA NODE. EXITING'
                print p.communicate()
                exit(1)
            list_of_data_nodes.append((p.communicate()[0]).strip('\n'))
        print '-----------------------------------------------'
        print 'LIST OF DATA NODES : ' + str(list_of_data_nodes)
        data_node_str=','.join(list_of_data_nodes)
    pytest_parameters.append('--datanodes=' + data_node_str)

    ##############
    # META NODES #
    ##############
    if options.metanodes is not None:
        meta_node_str=options.metanodes
    else:
        # get meta-node URL from pcl list -c <cluster>
        list_of_meta_nodes = []
        for meta_node in range(int(num_of_meta_nodes)):
            p = subprocess.Popen('pcl host meta-%d -c "%s"' % (meta_node, cluster_name), shell=True, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            if p.wait() != 0:
                print 'FAILED TO GET META NODE. EXITING'
                print p.communicate()
                exit(1)
            list_of_meta_nodes.append((p.communicate()[0]).strip('\n'))
        print '-----------------------------------------------'
        print 'LIST OF META NODES : ' + str(list_of_meta_nodes)
        meta_node_str=','.join(list_of_meta_nodes)
    # copy writenode_lin to every metanode (for now copy to every meta node, but need to copy to just one - meta node leader)

    for meta_node in meta_node_str.split(','):
        print 'COPYING writenode_lin TO ' + str(meta_node)
        print 'scp -i %s -o StrictHostKeyChecking=no writenode_lin %s@%s:/tmp' % (options.privatekey, clusteros, meta_node)
        w=subprocess.Popen('scp -i %s -o StrictHostKeyChecking=no writenode_lin %s@%s:/tmp' %
                           (options.privatekey, clusteros, meta_node) , shell=True, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
        waiting=w.wait()
        if waiting != 0:
            print 'FAILED TO COPY writenode_lin TO %s NODE' % meta_node
            print w.communicate()
            exit(1)
        w=subprocess.Popen('ssh -i %s -o StrictHostKeyChecking=no %s@%s \'cd /tmp; sudo chmod +x writenode_lin\'' %
                           (options.privatekey, clusteros, meta_node), shell=True, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
        waiting=w.wait()
        if waiting != 0:
            print 'FAILED TO CHMOD FOR writenode_lin ON %s NODE' % meta_node
            print w.communicate()
            exit(1)

    # get a mapping of private IPs and Public IPs to be used to find leader meta node
    m=subprocess.Popen("pcl list -c \"%s\"| awk '{ if ($1 != \"ID\") print $4, $5 }'" % cluster_name, shell=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if m.wait() != 0:
        print 'FAILED TO GET ALL OF THE NODES. EXITING'
        print m.communicate()
        exit(1)
    all_nodes=(m.communicate()[0]).strip('\n') # '52.10.147.183 10.0.207.136\n18.236.77.176 10.0.181.224'
    all_nodes=','.join(['_'.join(ips.split()) for ips in all_nodes.split('\n')])
    print '-------------------------------------------------------'
    print 'LIST OF ALL NODES MAPPINGS : ' + str(all_nodes)
    pytest_parameters.append('--metanodes=' + meta_node_str)
    pytest_parameters.append('--nodemap=' + all_nodes)

    ###### KAPACITOR
    if options.kapacitor is not None:
        pytest_parameters.append('--kapacitor=' + options.kapacitor)
        print '-------------------------------------'
        print 'KAPACITOR IP : ' + options.kapacitor
        print '-------------------------------------\n'
    elif options.nokapacitor is not False:
        print 'NOT INSTALLING KAPACITOR'
    else:
        p = subprocess.Popen('pcl host kapacitor-0 -c %s' % cluster_name, shell=True, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        if p.wait() != 0:
            print 'FAILED TO GET kapacitor NODE. EXITING'
            p.communicate()
            exit(1)
        kapacitor_name = (p.communicate()[0]).strip('\n')
        print '-------------------------------------'
        print 'KAPACITOR IP : ' + str(kapacitor_name)
        print '-------------------------------------\n'
        pytest_parameters.append('--kapacitor=' + kapacitor_name)
else:
    # we are running tests against 2.0 (cloud)
    ################
    # GATESWAY URL #
    ################
    if options.gateway:
        pytest_parameters.append('--gateway=' + options.gateway)
        print 'GATEWAY URL : ' + options.gateway
        print '-----------------------------------\n'
    else:
        print 'GATEWAY URL IS NOT SPECIFIED. EXITING'
        exit(1)

    ############
    # FLUX URL #
    ############
    if options.flux:
        pytest_parameters.append('--flux=' + options.flux)
        print 'FLUX URL : ' + options.flux
        print '--------------------------\n'
    else:
        print 'FLUX URL IS NOT SPECIFIED. EXITING'
        exit(1)

    ############
    # ETCD URL #
    ############
    if options.etcd:
        pytest_parameters.append('--etcd=' + options.etcd)
        print 'ETCD URL : ' + options.etcd
        print '--------------------------\n'
    else:
        print 'ETCD URL IS NOT SPECIFIED. EXITING'
        exit(1)

    ####################
    # TRANSPILERDE URL #
    ####################
    if options.transpilerde:
        pytest_parameters.append('--transpilerde=' + options.transpilerde)
        print 'TRANSPILERDE URL : ' + options.transpilerde
        print '------------------------------------------\n'
    else:
        print 'TRANSPILERDE URL IS NOT SPECIFIED. EXITING'
        exit(1)

    ################
    # HEALTH CHECK #
    ################

    # Need to check the health status of the different services, e.g.
    # get the JSON output of curl -GET http://<gateway>:9999/healthz
    # see https://github.com/influxdata/Litmus/issues/87
    """
    {
      "status": "unhealthy",
      "checks": [
        {
          "name": "internal",
          "status": "healthy"
        },
        {
          "status": "unhealthy",
          "checks": [
            {
              "name": "internal",
              "status": "healthy"
            },
            {
              "name": "kafka",
              "status": "healthy"
            },
            {
              "name": "etcd",
              "status": "unhealthy",
              "message": "dial tcp: lookup etcd on 10.96.0.10:53: no such host"
            }
          ]
        }
      ]
    }
    """
    # gateway checks for etcd, kafka and gateway services,
    # queryd checks for queryd and storage services
    # transpilerde checks for transpilerde service
    # TODO: tasks and etcd-tasks services
    status = {}
    services = {'gateway':options.gateway, 'queryd': options.flux, 'transpilerde': options.transpilerde}
    for service in services:
        general_status, out = 'unhealthy', ''
        # let the whole curl operation to run for no more than 10 seconds
        cmd_command = 'curl -s --max-time 10 -GET %s/healthz' % services[service]
        time_end = time.time() + 20 # wait up to 120 sec for services to start
        if service == 'gateway': print 'GETTING THE HEALTH STATUS OF THE GATEWAY, KAFKA and ETCD SERVICES'
        if service == 'queryd': print 'GETTING THE HEALTH STATUS OF THE QUERYD AND STORAGE SERVICES'
        if service == 'transpilerde': print 'GETTING THE HEALTH STATUS OF THE TRANSPILERDE SERVICE'
        print '-----------------------------------------------------------------\n'
        while time.time() <= time_end:
            print 'RUNNING \'%s\' COMMAND\n' % cmd_command
            # wait for up to a minute for curl command to return
            cmd_time_end = time.time() + 10
            while time.time() <= cmd_time_end:
                g_health = subprocess.Popen(cmd_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                time.sleep(2)
                if g_health.poll() == None:
                    print 'Waiting for \'%s\' command to return' % cmd_command
                    time.sleep(1)
                    continue
                else:
                    break
            if g_health.poll() != 0:
                print 'EXIT STATUS OF \'%s\' COMMAND IS NOT ZERO. TRYING ONCE AGAIN\n' % cmd_command
                time.sleep(1)
                continue
            # get output and error (if any) of the command
            out, err = g_health.communicate()
            if err != '':
                print '\'%s\' command returned an error \'%s\'' % (cmd_command, err)
                time.sleep(1)
                continue
            # remove new line characters from output of the command, which is a JSON string
            out = out.replace('\n','')
            """
            <gateway>:<port>/healthz command returns the health status for gateway, kafka and etcd.
            if status of kafka or/and etcd or/and gateway is 'unhealthy', then the general status is unhealthy
            """
            if out == '':
                print 'OUTPUT OF THE COMMAND IS EMPTY. SLEEPING'
                time.sleep(1)
                continue
            # load JSON string to be able to access it
            out = json.loads(out)
            # get the status
            general_status = out.get('status')
            if general_status != 'healthy':
                print 'Waiting for services to start up'
                time.sleep(1)
                continue
            else:
                print 'SERVICES ARE UP AND RUNNING'
                print '---------------------------\n'
                break
        status[service] = general_status
    print "STATUS OD THE SERVICES : " + str(status)
    if 'unhealthy' in status.values():
        print 'SERVICES ARE NOT UP AND RUNNING. EXITING.'
        exit(1)
# passing a file containing the test suite(s)
if options.tests is not None:
    pytest_parameters.extend(options.tests)
elif options.testslist is not None:
    test_list = []
    # we got a test file that needs to be parsed
    for line in open(options.testslist,'r'):
        if not line.startswith('#'):
            test_list.append(line.rstrip())
    pytest_parameters.extend(test_list)
else:
    print 'There are no tests to run. Exiting', exit(1)

print pytest_parameters

if prod_version == '1':
    PIP_CMD = 'sudo -H pip install --no-cache-dir'
    MODULES = ['pytest', 'requests', 'python-dateutil', 'pytest-html', 'pytest-metadata', 'influxdb']
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
            elif module == 'influxdb':
                proc = subprocess.call('%s %s' % (PIP_CMD, module), shell=True)
                assert proc == 0, 'FAILED TO INSTALL %s' % module
import pytest

print ''
print '#############################'
print '####### RUNNING TESTS #######'
print ''
exit_code=pytest.main(pytest_parameters)
#TODO : get log files
exit(exit_code)
