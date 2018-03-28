#!/bin/sh
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

# script variables for InfluxDB cluster setup
# number of data nodes to deploy
DATANODES=
# number of meta nodes to deploy
METANODES=
# cluster configuration
CLUSTER_ENVIRONMENT=
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
	if [[ `pcl list -c $CLUSTER_NAME | awk '{ if ($1 != "ID") print $1 }'` != ''  ]]
	then
		catchFail "pcl destroy -c $CLUSTER_NAME"
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
    catchFail  "pcl create -c $CLUSTER_NAME $DATANODES $METANODES
                    $CLUSTER_ENV $INFLUX_DB_VERSION $TELEGRAF_VERSION
                      --license-key $LICENSE_KEY"
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
			CLUSTER_ENVIRONMENT=$1
			CLUSTER_ENV=${CLUSTER_ENVIRONMENT//,/ --env }
			CLUSTER_ENV="--env $CLUSTER_ENV";;
		--cluster-name)
			shift
			CLUSTER_NAME=$1;;
		--pkg-data)
			shift
			LOCAL_PKG_DATA="--local-pkg-data $1";;
		--pkg-meta)
			shift
			LOCAL_PKG_META="--local-pkg-meta $1";;
		--telegraf-version)
			shif
			TELEGRAF_VERSION="--telegraf-version $1";;
		--influxdb-version)
			shift
			INFLUX_DB_VERSION="--influxdb-version $1";;

	esac
	shift
done


#-------------------------------------
# main()
#------------------------------------

main() {
    uninstall
    installCluster
}

main
