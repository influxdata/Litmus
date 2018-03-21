#!/bin/sh -x

DATANODES=
METANODES=
CLUSTER_ENVIRONMENT=
CLUSTER_NAME="litmus"
LICENSE_KEY="d69c9a41-6800-4419-ae5b-1df5aec449df"
LOCAL_PKG_DATA=
LOCAL_PKG_META=
TELEGRAF_VERSION=
INSTALL_DB_VERSION=

while [ $# -gt 0 ]
do
	case $1 in
		--d|--num-data)
			shift
			DATANODES="-d $1";;
		--m|--num-meta)
			shift
			METANODES="-m $1";;
		--e|--env)
			shift
			CLUSTER_ENVIRONMENT=$1;;
		--c|--cluster)
			shift
			CLUSTER_NAME=$1;;
		--pkg-data)
			shift
			LOCAL_PKG_DATA="--local-pkg-data $1";;
		--pkg-meta)
			shift
			LOCAL_PKG_META="--local-pkg-meta $1";;
		--no-telegraf)
			TELEGRAF_VERSION="--telegraf-version \"\"";;
		--telegraf-version)
			shif
			TELEGRAF_VERSION="--telegraf-version $1";;
		--db-version)
			shift
			INSTALL_DB_VERSION="--version $1";;
				
	esac
	shift
done
if [[ $CLUSTER_ENVIRONMENT != "" ]]; then
	CLUSTER_ENV=${CLUSTER_ENVIRONMENT//,/ --env }
	CLUSTER_ENV="--env $CLUSTER_ENV"
else 
	CLUSTER_ENV=""
fi

echo "pcl create -c $CLUSTER_NAME $DATANODES $METANODES $CLUSTER_ENV $INSTALL_DB_VERSION $TELEGRAF_VERSION"
pcl create -c $CLUSTER_NAME $DATANODES $METANODES $CLUSTER_ENV $INSTALL_DB_VERSION $TELEGRAF_VERSION
echo $? 
