# Litmus
Litmus is an automated regression test framework suitable for testing Kapacitor, InfluxDB components of TICK stack as well as REST API services. Currently the framework is not suitable for testing of UI component (chronograf), but it could be extended if needed to.
LItmus is based on pytest open source framework and uses Python for writing tests and supporting libraries.

## litmus_run_master.py script
 - It will install all required for running tests modules.
 - For Product Version 1.x (TICK stack with separate components):
   - Install all of the components using `pcl` tool (qa_install_tick.sh)
   - Accepts lits of tests or single test(s) to be run
   - Each test suite will produce a log file (useful for debugging)
   - Example of a test run :
     > python litmus_run_master.py --product-version 1 --num-data 2 --num-meta 3 --pkg-data $DATA_NODE --pkg-meta $META_NODE --telegraf-version "1.6.4" --kapacitor-version "1.5.0" --chronograf-version "1.5.0.1" --tests-list=tests_lists/all_tests.list --http-auth --admin-user test_admin --admin-pass test_admin --meta-auth --cluster-name chronograf --private-key litmus-pcl
 - For Product version 2.0 (Cloud):
   - Does not do any deployments or installations, only acceps three parameters (currently):
     - Gateway URL
     - Queryd URL (Flux)
     - Etcd URL (for users/organizations/buckets)
   - Example of a test run:
     > python litmus_run_master.py --no-chronograf --etcd http://localhost:2379 --gateway http://localhost:9999 --flux http://localhost:8093 --tests-list tests_lists/gateway_api_tests.list --product-version 2

## Running in Docker container (Currently is only done for 2.0):
- In order to create an image use Litmus.Dockerfile from Litmus repo:
  - `cd` to a directory where you will clone a Litmus repo
  - git clone git@github.com:influxdata/Litmus.git
  > docker build -f Litmus.Dockerfile -t image_name .
- To run tests from the test list (when 2.0 deployed locally suing skaffold). In the example below all of the test results and 
artifact will be copied to `/Users/gershonshif/Pictures` directory. 
  > docker run --rm -e ETCD_HOST=http://host.docker.internal:2379 -e GATEWAY_HOST=http://host.docker.internal:9999 -e QUERYD_HOST=http://host.docker.internal:8093 -e TEST_LIST=tests_lists/gateway_users_tests.list -v /Users/gershonshif/Pictures:/Litmus/result litmus_tests
- To run a single test:
  > docker run --rm -e ETCD_HOST=http://host.docker.internal:2379 -e GATEWAY_HOST=http://host.docker.internal:9999 -e QUERYD_HOST=http://host.docker.internal:8093 -e ONE_TEST=src/cloud/rest_api/users/test_gateway_get_all_users.py -v /Users/gershonshif/Pictures:/Litmus/result litmus_tests
