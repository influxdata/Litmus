#!/bin/bash -x
: ' Install and configure Enterprise TICK product.
    The script will:
  1. uninstall exisiting TICK system
  2. download and install the latest available plutonium build from  Jenkins
      (or a specific released version can be specified). For now, telefraf will be
      installed by default. (need to figure out how to pass an empty string as
      an argument)
  3. add a chronograf (need to figure out where to get the latest available
      chronograf build). For now, pass a latest released chronograf version,
  4. add a kapacitor(s) (need to figure out where to get the latest available
      kapacitor build). For now, pass a latest released kapacitor version.
'

install_chronograf=true
install_kapacitor=true

# script variables for InfluxDB cluster setup
# number of data nodes to deploy
DATANODES=
# number of meta nodes to deploy
METANODES=
# cluster configuration
CLUSTER_ENV=
# name of the cluster, default name is 'litmus'
CLUSTER_NAME="litmus"
# license key for an enterprise deployments
LICENSE_KEY="d69c9a41-6800-4419-ae5b-1df5aec449df"
# the latest meta node build (from plutonium build)
LOCAL_PKG_DATA=
# the latest data node build (from plutonium build)
LOCAL_PKG_META=
# telegraf version to install, pass latest released one
TELEGRAF_VERSION=
# influxDB released version to install
INSTALL_DB_VERSION=
# OS to install cluster on
CLUSTER_OS=

# script variables for chronograf
# version of chronograf to install
CHRONOGRAF_VERSION=
# number of chronograf instances
CHRONOGRAF_INSTANCES=
# OS to install chronograf on
CHRONOGRAF_OS=

# script variables for kapacitor
# version of kapacitor to install
KAPACITOR_VERSION=
# number of kapacitor instances
KAPACITOR_INSTANCES=
NUMBER_OF_KAPACITORS=
# OS to install kapacitor on
KAPACITOR_OS=

# script variables for data nodes authentication
# use ENVIRONMENT VAR INFLUXDB_HTTP_AUTH_ENABLED=true
# set it as adifferent env in order to be able to 
# switch between auth and no auth for data nodes???
# *** do the same for INDEX tsi1 vs inmem???? *** #
HTTP_AUTH_ENABLED=
ADMIN_USER=
ADMIN_PASSWORD=

# Cluster LOG environment Vars to be always used (data node)
# Meta logging toggles the logging of messages from the meta service
DATA_META_LOG=",INFLUXDB_META_LOGGING_ENABLED=true,"
DATA_TRACE_LOG="INFLUXDB_DATA_TRACE_LOGGING_ENABLED=true,"
DATA_QUERY_LOG="INFLUXDB_DATA_QUERY_LOG_ENABLED=true,"
HTTP_LOG="INFLUXDB_HTTP_LOG_ENABLED=true,"
HTTP_WRITE="INFLUXDB_HTTP_WRITE_TRACING=true,"
CLUSTER_TRACING="INFLUXDB_CLUSTER_CLUSTER_TRACING=true"

CLUSTER_LOG_ENV=$DATA_META_LOG$DATA_TRACE_LOG$DATA_QUERY_LOG$HTTP_LOG$CLUSTER_TRACING

# index version either inmem or tsi1 (by default tsi1)
INDEX_VERSION=

#--------------------------------------
# catchFail()
#--------------------------------------
# Make sure the command succeeded
# If the parameter to this function returns anything but a 0 return value,
# stop the installation and display the failed command.
catchFail () {
	echo "RUNNING: $@"
	eval "$@"

	if [ $? -ne 0 ]; then
		echo "ERROR executing: $@"
		echo "Stopping the install"
		exit 1
	fi
}

#--------------------------------------
# runCmd()
#--------------------------------------
# Output the command that is being launched.
runCmd () {
	echo "RUNNING: $@"
	eval "$@"
}

#--------------------------------------
# uninstall()
#--------------------------------------
# Uninstall an existing TICK stack.
# If pcl list -cluster <cluster name> returns nothing, do nothing

uninstall() {
	echo
	echo `date` "***************  uninstalling  ***************"
	product=`pcl list -c $CLUSTER_NAME | awk '{ if ($1 != "ID") print $1 }'`
	if [ X"$product" != X"" ]
	then
		catchFail "echo y | pcl destroy -c $CLUSTER_NAME"
	else
		echo "Nothing to uninstall"
	fi
}

#----------------------------------------
# installCluster()
#----------------------------------------
# Creates a cluster of meta and data nodes. The meta nodes will be joined and
# data nodes added to the cluster. Also released version of telegraf will be installed.

installCluster() {
	echo
    	echo `date`"**************** installing cluster ********************"
	if [ "X"$INDEX_VERSION == "X" ]; then
		INDEX_VERSION="INFLUXDB_DATA_INDEX_VERSION=tsi1"
	fi
	if [ "X"$HTTP_AUTH_ENABLED != "X" ]; then # data nodes auth enabled
		# check if admin user and password are provided
		if [ "X"$ADMIN_USER == "X" -a "X"$ADMIN_PASSWORD == "X" ]; then
			echo "ADMIN USER OR/AND PASSWORD IS NOT PROVIDED. EXIT"
			exit 1
		fi
	fi 
	if [ "X"$CLUSTER_ENV == "X" ]; then
		CLUSTER_ENV=$INDEX_VERSION$HTTP_AUTH_ENABLED$CLUSTER_LOG_ENV
	else
		CLUSTER_ENV=$INDEX_VERSION$HTTP_AUTH_ENABLED$CLUSTER_LOG_ENV","$CLUSTER_ENV
	fi			
    	CLUSTER_ENV=$(echo ${CLUSTER_ENV//,/ --env })
	CLUSTER_ENV="--env $CLUSTER_ENV"
	catchFail  "pcl create -c $CLUSTER_NAME $DATANODES $METANODES $CLUSTER_ENV $INFLUX_DB_VERSION $TELEGRAF_VERSION --license-key $LICENSE_KEY"
	# create admin user and password
	if [ "X"$HTTP_AUTH_ENABLED != "X" ]; then
		catchFail "curl --fail -XPOST \"http://`pcl host data-0 -c $CLUSTER_NAME`:8086/query\" --data-urlencode \"q=CREATE USER $ADMIN_USER WITH PASSWORD '$ADMIN_PASSWORD' WITH ALL PRIVILEGES\""
	fi
}


#---------------------------------------
# installChronograf()
#---------------------------------------
# adds a Chronograf instance to the given cluster

installChronograf() {

	echo
	echo `date`"**************** installing chronograf *********************"
	catchFail "pcl add-chronograf -c $CLUSTER_NAME $CHRONOGRAF_VERSION $CHRONOGRAF_INSTANCES $CHRONOGRAF_OS"
}

#----------------------------------------
# installKapacitor()
#----------------------------------------
# adds a kapacitor instance to the given cluster
# changes the default configuration file to the one provided 
# by the output of the 'kapacitord config' command
# changes write-tracing value to true, pprof-enabled value to true [http] table
# changes log level to DEBUG [logging] section. The influxdb section's key-values
# would be changed using REST API (runtime)

installKapacitor() {
	echo
	echo `date`"***************** installing kapacitor **********************"
	catchFail "pcl add-kapacitor -c $CLUSTER_NAME $KAPACITOR_VERSION $KAPACITOR_INSTANCES $KAPACITOR_OS"
	if [ "X"$NUMBER_OF_KAPACITORS == "X" ]; then
		echo 
		echo `date`"*********************** stopping kapacitor-0 ****************************"
		catchFail "pcl ssh -c $CLUSTER_NAME kapacitor-0 'sudo service kapacitor stop'"
		# check if kapacitor was stopped
		out=`pcl ssh -c $CLUSTER_NAME kapacitor-0 "ps axu | grep kapacitor| grep -v grep"`
		if [ "X$out" == "X" ]; then
			catchFail "pcl ssh -c $CLUSTER_NAME kapacitor-0 'kapacitord config > /tmp/test.conf;sudo cp /tmp/test.conf /etc/kapacitor/kapacitor.conf.generated;sudo cp /etc/kapacitor/kapacitor.conf /etc/kapacitor/kapacitor.conf.orig;sudo cp /etc/kapacitor/kapacitor.conf.generated /etc/kapacitor/kapacitor.conf'"
		else
			echo "COULD NOT STOP THE KAPACITOR.EXITING"
			exit 1
		fi	  
		echo "****************** updating the config values ********************"		
		echo " SETTING write-tracing = true, pprof-enabled = true, level = \"DEBUG\""
		catchFail "pcl ssh -c $CLUSTER_NAME kapacitor-0 'sudo sed -i -e \"s/write-tracing = false/write-tracing = true/\" /etc/kapacitor/kapacitor.conf'"
		catchFail "pcl ssh -c $CLUSTER_NAME kapacitor-0 'sudo sed -i -e \"s/pprof-enabled = false/pprof-enabled = true/\" /etc/kapacitor/kapacitor.conf'"
		catchFail "pcl ssh -c $CLUSTER_NAME kapacitor-0 'sudo sed -i -e \"s/level = \\\"INFO\\\"/level = \\\"DEBUG\\\"/\" /etc/kapacitor/kapacitor.conf'"
		echo "****************** starting kapacitor **************************"
		catchFail "pcl ssh -c $CLUSTER_NAME kapacitor-0 'sudo service kapacitor start'"
		start=`pcl ssh -c $CLUSTER_NAME kapacitor-0 "ps axu | grep kapacitor| grep -v grep"`
		if [ "X$start" == "X" ];then
			echo "KAPACITOR DID NOT START. EXITING"
			exit 1
		fi
	else
		echo "WILL BE IMPLEMENTED LATER"
	fi
}

while [ $# -gt 0 ]
do
	case $1 in
		--num-data)
            		shift
			DATANODES="-d $1";;
		--num-meta)
			shift
			METANODES="-m $1";;
		--cluster-env)
			shift
			CLUSTER_ENV=$1;;
		--cluster-name)
			shift
			CLUSTER_NAME=$1;;
		--index-version)
			shift
			INDEX_VERSION="INFLUXDB_DATA_INDEX_VERSION=$1";;
		--http-auth)
			HTTP_AUTH_ENABLED=",INFLUXDB_HTTP_AUTH_ENABLED=true";;
		--admin-user)
			shift
			ADMIN_USER=$1;;
		--admin-pass)
			shift
			ADMIN_PASSWORD=$1;;			
		--pkg-data)
			shift
			LOCAL_PKG_DATA="--local-pkg-data $1";;
		--pkg-meta)
			shift
			LOCAL_PKG_META="--local-pkg-meta $1";;
		--telegraf-version)	
			shift
			TELEGRAF_VERSION="--telegraf-version $1";;
		--influxdb-version)
			shift
			INFLUX_DB_VERSION="--version $1";;
		--cluster-os)
			shift
			CLUSTER_OS="--aws-os $1";;
               	--chronograf-version)
                       shift
                       CHRONOGRAF_VERSION="--chronograf-version $1";;
               	--num-chronografs)
                       shift
                       CHRONOGRAF_INSTANCES="--num-instances $1";;
               	--chronograf-os)
                       shift
                       CHRONOGRAF_OS="--aws-os $1";;
               	--no-chronograf)
                       install_chronograf=false;;
               	--kapacitor-version)
                       shift
                       KAPACITOR_VERSION="--kapacitor-version $1";;
               	--num-kapacitors)
                       shift
		       KAPACITOR_INSTANCES="--num-instances $1"
		       NUM_OF_KAPACITORS="$1";;
               --kapacitor-os)
                       KAPACITOR_OS="--aws-os $";;
               --no-kapacitor)
                       install_kapacitor=false;;
	esac
	shift
done


#-------------------------------------
# main()
#------------------------------------

main() {
    	uninstall
    	installCluster
	if $install_chronograf; then
		installChronograf
	fi
	if $install_kapacitor; then
		installKapacitor
	fi
}

main
