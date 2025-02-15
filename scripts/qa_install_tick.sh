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
meta_auth=false
ldap_auth=false
install=true
SCP="/usr/bin/scp"
SSH="/usr/bin/ssh"
PRIVATE_KEY=
INFLUXD_CTL="/usr/bin/influxd-ctl"
PCL="$HOME/go/bin/pcl"

# script variables for InfluxDB cluster setup
# number of data nodes/pcl to deploy
DATANODES_NUM=
DATANODES=
# number of meta nodes to deploy
METANODES_NUM=
METANODES=
META_CONFIG="/etc/influxdb/influxdb-meta.conf"
META_LDAP_ALLOWED=
META_AUTH=
# cluster configuration
INTERNAL_SHARED_SECRET="long shared secret"
CLUSTER_ENV=
# name of the cluster, default name is 'litmus'
CLUSTER_NAME="litmus"
LDAP_CONFIG="sample-ldap-config.toml"
# data node config
DATA_CONFIG="/etc/influxdb/influxdb.conf"
# license key for an enterprise deployments
LICENSE_KEY="d69c9a41-6800-4419-ae5b-1df5aec449df"
# the latest meta node build (from plutonium build)
LOCAL_PKG_DATA=
# the latest data node build (from plutonium build)
LOCAL_PKG_META=
# telegraf version to install, pass latest released one
TELEGRAF_VERSION=
TELEGRAF_CONFIG="/etc/telegraf/telegraf.d/output.conf"
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
KAPACITOR_CONFIG="/etc/kapacitor/kapacitor.conf"

# script variables for data nodes authentication
# use ENVIRONMENT VAR INFLUXDB_HTTP_AUTH_ENABLED=true
# set it as adifferent env in order to be able to 
# switch between auth and no auth for data nodes???
# *** do the same for INDEX tsi1 vs inmem???? *** #
HTTP_AUTH_ENABLED=
ADMIN_USER=
ADMIN_PASSWORD=
LDAP_ADMIN="sal.xu"
LDAP_PASSWORD="p@ssw0rd"

# Cluster LOG environment Vars to be always used (data node)
# Meta logging toggles the logging of messages from the meta service
META_LOG=",INFLUXDB_META_LOGGING_ENABLED=true,"
# Cluster tracing toggles the logging of Raft logs on Raft nodes
META_CLUSTER_TRACING="INFLUXDB_META_CLUSTER_TRACING=true,"
# Toggles logging of additional debug information within the TSM engine and WAL
DATA_TRACE_LOG="INFLUXDB_DATA_TRACE_LOGGING_ENABLED=true,"
# The query log enabled setting toggles the logging of parsed queries before execution
DATA_QUERY_LOG="INFLUXDB_DATA_QUERY_LOG_ENABLED=true,"
# Determines whether HTTP request logging is enabled
HTTP_LOG="INFLUXDB_HTTP_LOG_ENABLED=true,"
# Determines whether detailed write logging is enabled.
HTTP_WRITE="INFLUXDB_HTTP_WRITE_TRACING=true,"
# to enable logging of cluster communications, to verify connectivity issues between data nodes
CLUSTER_TRACING="INFLUXDB_CLUSTER_CLUSTER_TRACING=true"

CLUSTER_LOG_ENV=$META_LOG$META_CLUSTER_TRACING$DATA_TRACE_LOG$DATA_QUERY_LOG$HTTP_LOG$HTTP_WRITE$CLUSTER_TRACING

# index version either inmem or tsi1 (by default tsi1)
INDEX_VERSION=

if [ "X"$CLUSTER_OS == "X" ]; then
    OS="ubuntu"
else
    OS=$CLUSTER_OS
fi

if [ "$PRIVATE_KEY" == "X" ]; then
    PRIVATE_KEY="litmus-pcl"
else
    PRIVATE_KEY=$PRIVATE_KEY
fi
#-------------------------------------------------------------------------
# catchFail()
#-------------------------------------------------------------------------
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

#-------------------------------------------
# runCmd()
#-------------------------------------------
# Output the command that is being launched.
runCmd () {
	echo "RUNNING: $@"
	eval "$@"
}

#-----------------------------------------------------------------
# uninstall()
#-----------------------------------------------------------------
# Uninstall an existing TICK stack.
# If $PCL list -cluster <cluster name> returns nothing, do nothing

uninstall() {
	echo
	echo `date` "***************  uninstalling  ***************"
	product=`$PCL list -c $CLUSTER_NAME | awk '{ if ($1 != "ID") print $1 }'`
	if [ X"$product" != X"" ]
	then
		catchFail "echo y | $PCL destroy -c $CLUSTER_NAME"
	else
		echo "Nothing to uninstall"
	fi
}

#-------------------------------------------------------------------------------------
# installCluster()
#-------------------------------------------------------------------------------------
# Creates a cluster of meta and data nodes. The meta nodes will be joined and
# data nodes added to the cluster. Also released version of telegraf will be installed.

installCluster() {
	echo
    	echo `date` "**************** installing cluster ********************"
    # 1. Index to be used: inmem or tsi1
	if [ "X"$INDEX_VERSION == "X" ]; then
		INDEX_VERSION="INFLUXDB_DATA_INDEX_VERSION=tsi1"
	fi
	# 2. check for data nodes authentication availability
	if [ "X"$HTTP_AUTH_ENABLED != "X" ]; then
		# check if admin user and password are provided
		if [ "X"$ADMIN_USER == "X" -a "X"$ADMIN_PASSWORD == "X" ]; then
			echo "ADMIN USER OR/AND PASSWORD IS NOT PROVIDED. EXIT"
			exit 1
		fi
	fi 
	if [ "X"$CLUSTER_ENV == "X" ]; then
	    # meta node authenticatin is enabled
	    if [ "X"$META_AUTH != "X" ]; then
	        # need to make sure if ldap authentication is enabled
	        if [ "X"$META_LDAP_ALLOWED != "X" -a "X"$HTTP_AUTH_ENABLED != "X" ]; then # LDAP authentication is enabled
		        CLUSTER_ENV=$INDEX_VERSION$HTTP_AUTH_ENABLED$META_LDAP_ALLOWED$META_AUTH$CLUSTER_LOG_ENV
		    else
		        CLUSTER_ENV=$INDEX_VERSION$HTTP_AUTH_ENABLED$META_AUTH$CLUSTER_LOG_ENV
		    fi
	    else
	        if [ "X"$META_LDAP_ALLOWED != "X" -a "X"$HTTP_AUTH_ENABLED != "X" ]; then # LDAP authentication is enabled
		        CLUSTER_ENV=$INDEX_VERSION$HTTP_AUTH_ENABLED$META_LDAP_ALLOWED$CLUSTER_LOG_ENV
            else
                CLUSTER_ENV=$INDEX_VERSION$HTTP_AUTH_ENABLED$CLUSTER_LOG_ENV
            fi
        fi
	else
	    # meta node authenticatin is enabled
	    if [ "X"$META_AUTH != "X" ]; then
	        if [ "X"$META_LDAP_ALLOWED != "X" -a "X"$HTTP_AUTH_ENABLED != "X" ]; then # LDAP authentication is enabled
		        CLUSTER_ENV=$INDEX_VERSION$HTTP_AUTH_ENABLED$META_LDAP_ALLOWED$META_AUTH$CLUSTER_LOG_ENV","$CLUSTER_ENV
		    else
		        CLUSTER_ENV=$INDEX_VERSION$HTTP_AUTH_ENABLED$META_AUTH$CLUSTER_LOG_ENV","$CLUSTER_ENV
		    fi
		else
		    if [ "X"$META_LDAP_ALLOWED != "X" -a "X"$HTTP_AUTH_ENABLED != "X" ]; then # LDAP authentication is enabled
		        CLUSTER_ENV=$INDEX_VERSION$HTTP_AUTH_ENABLED$META_LDAP_ALLOWED$CLUSTER_LOG_ENV","$CLUSTER_ENV
		    else
		        CLUSTER_ENV=$INDEX_VERSION$HTTP_AUTH_ENABLED$CLUSTER_LOG_ENV","$CLUSTER_ENV
		    fi
		fi
	fi			
    CLUSTER_ENV=$(echo ${CLUSTER_ENV//,/ --env })
	CLUSTER_ENV="--env $CLUSTER_ENV"
	catchFail  "$PCL create -c $CLUSTER_NAME $DATANODES $METANODES $LOCAL_PKG_DATA $LOCAL_PKG_META $CLUSTER_ENV $INFLUX_DB_VERSION $TELEGRAF_VERSION --license-key $LICENSE_KEY"
	if [ "X"$META_AUTH != "X" ]; then
	    counter=0
        while [ $counter -lt $DATANODES_NUM ]
        do
            # ssh to a datanode, stop influxdb service, update the confing and start influxdb service
            catchFail "$PCL ssh -c $CLUSTER_NAME data-$counter 'sudo service influxdb stop'"
            out=`$PCL ssh -c $CLUSTER_NAME data-$counter "ps axu | grep influxdb| grep -v grep"`
            if [ "X$out" == "X" ]; then
                catchFail "$PCL ssh -c $CLUSTER_NAME data-$counter 'sudo sed -i -e \"s/.*meta-internal-shared-secret =.*/  meta-internal-shared-secret = \\\"$INTERNAL_SHARED_SECRET\\\"/\" $DATA_CONFIG'"
                catchFail "$PCL ssh -c $CLUSTER_NAME data-$counter 'sudo service influxdb start'"
                start=`$PCL ssh -c $CLUSTER_NAME meta-$counter "ps axu | grep influxdb| grep -v grep"`
                if [ "X$start" == "X" ]; then
                    echo "INFLUXDB SERVICE DID NOT START ON data-$counter. EXITING"
                    exit 1
                fi
            else
                echo "COULD NOT STOP INFLUXDB SERVICE. EXISITNG"
                exit 1
            fi
            let counter+=1
        done
    fi
	# create admin user and password
	if [ "X"$HTTP_AUTH_ENABLED != "X" ]; then
		catchFail "curl --fail -XPOST \"http://`$PCL host data-0 -c $CLUSTER_NAME`:8086/query\" --data-urlencode \"q=CREATE USER $ADMIN_USER WITH PASSWORD '$ADMIN_PASSWORD' WITH ALL PRIVILEGES\""
		if [ "X"$META_LDAP_ALLOWED != "X" ]; then
            # copy Ldap config to every meta  and data nodes
            echo `date` "*************** copying ldap config file and private key to meta and data nodes ****************"
            echo ""
            # private key required to create tunneling for ldap server
	        counter=0
		    while [ $counter -lt $METANODES_NUM ]
		    do
		        catchFail "$SCP -i $PRIVATE_KEY -o StrictHostKeyChecking=no $PRIVATE_KEY $OS@`$PCL host meta-$counter -c $CLUSTER_NAME`:/tmp"
		        catchFail "$SCP -i $PRIVATE_KEY -o StrictHostKeyChecking=no $LDAP_CONFIG $OS@`$PCL host meta-$counter -c $CLUSTER_NAME`:/tmp"
		        echo `date` "********* PORT FORWARD FOR LDAP *********"
		        catchFail "$SSH -i $PRIVATE_KEY -f -o StrictHostKeyChecking=no $OS@`$PCL host meta-$counter -c $CLUSTER_NAME` 'sudo $SSH -o StrictHostKeyChecking=no -l tunnel -fN -L 3389:10.0.1.69:389 34.217.54.237 -i /tmp/$PRIVATE_KEY'"
		        echo `date` "********* INSTALL LDAP-UTILS *********"
		        catchFail "$SSH -i $PRIVATE_KEY -f -o StrictHostKeyChecking=no $OS@`$PCL host meta-$counter -c $CLUSTER_NAME` 'sudo apt install ldap-utils'"
		        let counter+=1
		    done
		    counter=0
		    while [ $counter -lt $DATANODES_NUM ]
		    do
		        catchFail "$SCP -i $PRIVATE_KEY -o StrictHostKeyChecking=no $PRIVATE_KEY $OS@`$PCL host data-$counter -c $CLUSTER_NAME`:/tmp"
		        catchFail "$SCP -i $PRIVATE_KEY -o StrictHostKeyChecking=no $LDAP_CONFIG $OS@`$PCL host data-$counter -c $CLUSTER_NAME`:/tmp"
		        echo `date` "********* PORT FORWARD FOR LDAP *********"
		        catchFail "$SSH -i $PRIVATE_KEY -f -o StrictHostKeyChecking=no $OS@`$PCL host data-$counter -c $CLUSTER_NAME` 'sudo $SSH -o StrictHostKeyChecking=no -l tunnel -fN -L 3389:10.0.1.69:389 34.217.54.237 -i /tmp/$PRIVATE_KEY'"
		        catchFail "$SSH -i $PRIVATE_KEY -f -o StrictHostKeyChecking=no $OS@`$PCL host data-$counter -c $CLUSTER_NAME` 'sudo apt install ldap-utils'"
		        let counter+=1
		    done
		fi
		echo
		echo `date` "*************** updating telegraf configuration on each data and meta nodes ******************"
		echo ""
		counter=0
		while [ $counter -lt $DATANODES_NUM ]
		do
			# ssh to a datanode, stop telegraf service, update the confing and start telegraf service
			catchFail "$PCL ssh -c $CLUSTER_NAME data-$counter 'sudo service telegraf stop'"
			out=`$PCL ssh -c $CLUSTER_NAME data-$counter "ps axu | grep telegraf| grep -v grep"`
			if [ "X$out" == "X" ]; then
			    catchFail "$PCL ssh -c $CLUSTER_NAME data-$counter 'sudo sed -i \"/database/ausername = \\\"$ADMIN_USER\\\"\" $TELEGRAF_CONFIG'"
				catchFail "$PCL ssh -c $CLUSTER_NAME data-$counter 'sudo sed -i \"/username/apassword = \\\"$ADMIN_PASSWORD\\\"\" $TELEGRAF_CONFIG'"
				catchFail "$PCL ssh -c $CLUSTER_NAME data-$counter 'sudo service telegraf start'"
                start=`$PCL ssh -c $CLUSTER_NAME data-$counter "ps axu | grep telegraf| grep -v grep"`
                if [ "X$start" == "X" ];then
                    echo "TELEGRAF DID NOT START ON data-$counter. EXITING"
                    exit 1
                fi
			else
			    echo "COULD NOT STOP TELEGRAF. EXITING"
			    exit 1;
			fi
			let counter+=1
		done
		counter=0
		while [ $counter -lt $METANODES_NUM ]
		do
			# ssh to a metanode, stop telegraf service, update the confing and start telegraf service
			catchFail "$PCL ssh -c $CLUSTER_NAME meta-$counter 'sudo service telegraf stop'"
			out=`$PCL ssh -c $CLUSTER_NAME meta-$counter "ps axu | grep telegraf| grep -v grep"`
			if [ "X$out" == "X" ]; then
			    catchFail "$PCL ssh -c $CLUSTER_NAME meta-$counter 'sudo sed -i \"/database/ausername = \\\"$ADMIN_USER\\\"\" $TELEGRAF_CONFIG'"
				catchFail "$PCL ssh -c $CLUSTER_NAME meta-$counter 'sudo sed -i \"/username/apassword = \\\"$ADMIN_PASSWORD\\\"\" $TELEGRAF_CONFIG'"
				catchFail "$PCL ssh -c $CLUSTER_NAME meta-$counter 'sudo service telegraf start'"
                start=`$PCL ssh -c $CLUSTER_NAME meta-$counter "ps axu | grep telegraf| grep -v grep"`
                if [ "X$start" == "X" ];then
                    echo "TELEGRAF DID NOT START ON meta-$counter. EXITING"
                    exit 1
                fi
			else
			    echo "COULD NOT STOP TELEGRAF. EXITING"
			    exit 1;
			fi
			let counter+=1
		done
	fi
}

#-------------------------------------------------
# installChronograf()
#-------------------------------------------------
# adds a Chronograf instance to the given cluster

installChronograf() {

	echo
	echo `date`"**************** installing chronograf *********************"
	echo ""
	catchFail "$PCL add-chronograf -c $CLUSTER_NAME $CHRONOGRAF_VERSION $CHRONOGRAF_INSTANCES $CHRONOGRAF_OS"
}

#----------------------------------------------------------------------------------
# installKapacitor()
#----------------------------------------------------------------------------------
# adds a kapacitor instance to the given cluster
# changes the default configuration file to the one provided 
# by the output of the 'kapacitord config' command
# changes write-tracing value to true, pprof-enabled value to true [http] table
# changes log level to DEBUG [logging] section. The influxdb section's key-values
# would be changed using REST API (runtime)

installKapacitor() {
	echo
	echo `date`"***************** installing kapacitor **********************"
	echo ""
	catchFail "$PCL add-kapacitor -c $CLUSTER_NAME $KAPACITOR_VERSION $KAPACITOR_INSTANCES $KAPACITOR_OS"
	if [ "X"$NUMBER_OF_KAPACITORS == "X" ]; then
		echo 
		echo `date`"*********************** stopping kapacitor-0 ****************************"
		echo ""
		catchFail "$PCL ssh -c $CLUSTER_NAME kapacitor-0 'sudo service kapacitor stop'"
		# check if kapacitor was stopped
		out=`$PCL ssh -c $CLUSTER_NAME kapacitor-0 "ps axu | grep kapacitor| grep -v grep"`
		if [ "X$out" == "X" ]; then
			catchFail "$PCL ssh -c $CLUSTER_NAME kapacitor-0 'kapacitord config > /tmp/test.conf;sudo cp /tmp/test.conf /etc/kapacitor/kapacitor.conf.generated;sudo cp /etc/kapacitor/kapacitor.conf /etc/kapacitor/kapacitor.conf.orig;sudo cp /etc/kapacitor/kapacitor.conf.generated /etc/kapacitor/kapacitor.conf'"
		else
			echo "COULD NOT STOP THE KAPACITOR.EXITING"
			exit 1
		fi	  
		echo "****************** updating the config values ********************"
		echo ""
		echo " SETTING write-tracing = true, pprof-enabled = true, level = \"DEBUG\""
		echo ""
		catchFail "$PCL ssh -c $CLUSTER_NAME kapacitor-0 'sudo sed -i -e \"s/write-tracing = false/write-tracing = true/\" $KAPACITOR_CONFIG'"
		catchFail "$PCL ssh -c $CLUSTER_NAME kapacitor-0 'sudo sed -i -e \"s/pprof-enabled = false/pprof-enabled = true/\" $KAPACITOR_CONFIG'"
		catchFail "$PCL ssh -c $CLUSTER_NAME kapacitor-0 'sudo sed -i -e \"s/level = \\\"INFO\\\"/level = \\\"DEBUG\\\"/\" $KAPACITOR_CONFIG'"
		if [ "X"$HTTP_AUTH_ENABLED != "X" ]; then
            catchFail "$PCL ssh -c $CLUSTER_NAME kapacitor-0 'sudo sed -i -e \"s/username = .*/username = \\\"$ADMIN_USER\\\"/\" $KAPACITOR_CONFIG'"
			catchFail "$PCL ssh -c $CLUSTER_NAME kapacitor-0 'sudo sed -i -e \"s/password = .*/password = \\\"$ADMIN_PASSWORD\\\"/\" $KAPACITOR_CONFIG'"
		fi
		echo "****************** starting kapacitor **************************"
		echo ""
		catchFail "$PCL ssh -c $CLUSTER_NAME kapacitor-0 'sudo service kapacitor start'"
		start=`$PCL ssh -c $CLUSTER_NAME kapacitor-0 "ps axu | grep kapacitor| grep -v grep"`
		if [ "X$start" == "X" ];then
			echo "KAPACITOR DID NOT START. EXITING"
			exit 1
		fi
	else
		echo "WILL BE IMPLEMENTED LATER"
	fi
}

#---------------------------------------------------------------------
# enableMetaAuth()
#---------------------------------------------------------------------
# enables authentication of Meta Nodes.
# Meta nodes support JWT authentication and Basic authentication
# First version of the function will support only Basic Authentication
# The ENV vars cannot be used during installation, pcl installer with
# throw the error: Output from failed meta join: add-meta:
# operation exited with error: must create admin user first

enableMetaAuth() {
    echo `date` "****************** Enable meta nodes authentications *************************"
    echo ""
    counter=0
	while [ $counter -lt $METANODES_NUM ]
	do
		# ssh to a metanode, stop influxdb-meta service, update the confing and start influxdb-meta service
		catchFail "$PCL ssh -c $CLUSTER_NAME meta-$counter 'sudo service influxdb-meta stop'"
		out=`$PCL ssh -c $CLUSTER_NAME meta-$counter "ps axu | grep influxdb| grep -v grep"`
		if [ "X$out" == "X" ]; then
		    catchFail "$PCL ssh -c $CLUSTER_NAME meta-$counter 'sudo sed -i -e \"s/.*auth-enabled = false/  auth-enabled = true/\" $META_CONFIG'"
		    catchFail "$PCL ssh -c $CLUSTER_NAME meta-$counter 'sudo sed -i -e \"s/.*internal-shared-secret =.*/  internal-shared-secret = \\\"$INTERNAL_SHARED_SECRET\\\"/\" $META_CONFIG'"
		    catchFail "$PCL ssh -c $CLUSTER_NAME meta-$counter 'sudo service influxdb-meta start'"
            start=`$PCL ssh -c $CLUSTER_NAME meta-$counter "ps axu | grep influxdb| grep -v grep"`
            if [ "X$start" == "X" ]; then
                echo "INFLUXDB-META SERVICE DID NOT START ON meta-$counter. EXITING"
                exit 1
            fi
        else
            echo "COULD NOT STOP INFLUXDB-META SERVICE. EXISITNG"
            exit 1
        fi
        let counter+=1
    done
}

#---------------------------------------------
# enableLdapAuth()
#---------------------------------------------
# sets ldap config on one of the meta nodes
# and updates telegraf and kapacitor username,
# password to connect to influxdb

enableLdapAuth() {
    # are we using meta authentication
    if $meta_auth; then
        echo `date` "********** META AUTHENTICATION IS ENABLED **********"
        # need to use admin user and password that is passed with --admin-user/--admin-pass
        catchFail "$SSH -i $PRIVATE_KEY -o StrictHostKeyChecking=no $OS@`$PCL host meta-0 -c ldap` '$INFLUXD_CTL -auth-type basic -user $ADMIN_USER -pwd $ADMIN_PASSWORD ldap set-config /tmp/$LDAP_CONFIG'"
    else
        echo `date` "********** META AUTHENTICATION IS NOT ENABLED **********"
        catchFail "$SSH -i $PRIVATE_KEY -o StrictHostKeyChecking=no $OS@`$PCL host meta-0 -c ldap` '$INFLUXD_CTL ldap set-config /tmp/$LDAP_CONFIG'"
    fi
    # verify that ldap config was loded successfully
    if $meta_auth; then
        success=$($SSH -i $PRIVATE_KEY -o StrictHostKeyChecking=no $OS@`$PCL host meta-0 -c ldap` "$INFLUXD_CTL -auth-type basic -user $LDAP_ADMIN -pwd $LDAP_PASSWORD ldap get-config")
    else
        success=$($SSH -i $PRIVATE_KEY -o StrictHostKeyChecking=no $OS@`$PCL host meta-0 -c ldap` "$INFLUXD_CTL ldap get-config")
    fi
    if [ "X"$success == "X" ]; then
        echo "LDAP CONFIG WAS NOT LOADED SUCCESSFULLY. EXISTING"
        exit 1;
    fi
    echo "LDAP CONFIG LOADED SUCCESSFULLY"
    echo `date` "********************* Updating telegraf username/password to work with LDAP on data and meta nodes *********************"
    echo ""
	counter=0
	while [ $counter -lt $DATANODES_NUM ]
	do
	    # ssh to a datanode, stop telegraf service, update the confing and start telegraf service
		catchFail "$PCL ssh -c $CLUSTER_NAME data-$counter 'sudo service telegraf stop'"
		out=`$PCL ssh -c $CLUSTER_NAME data-$counter "ps axu | grep telegraf| grep -v grep"`
		if [ "X$out" == "X" ]; then
		    catchFail "$PCL ssh -c $CLUSTER_NAME data-$counter 'sudo sed -i -e \"s/username = .*/username = \\\"$LDAP_ADMIN\\\"/\" $TELEGRAF_CONFIG'"
			catchFail "$PCL ssh -c $CLUSTER_NAME data-$counter 'sudo sed -i -e \"s/password = .*/password = \\\"$LDAP_PASSWORD\\\"/\" $TELEGRAF_CONFIG'"
			catchFail "$PCL ssh -c $CLUSTER_NAME data-$counter 'sudo service telegraf start'"
            start=`$PCL ssh -c $CLUSTER_NAME data-$counter "ps axu | grep telegraf| grep -v grep"`
                if [ "X$start" == "X" ];then
                    echo "TELEGRAF DID NOT START ON data-$counter. EXITING"
                    exit 1
                fi
		else
		    echo "COULD NOT STOP TELEGRAF. EXITING"
			exit 1;
		fi
		let counter+=1
	done
	counter=0
	while [ $counter -lt $METANODES_NUM ]
	do
		# ssh to a metanode, stop telegraf service, update the confing and start telegraf service
		catchFail "$PCL ssh -c $CLUSTER_NAME meta-$counter 'sudo service telegraf stop'"
		out=`$PCL ssh -c $CLUSTER_NAME meta-$counter "ps axu | grep telegraf| grep -v grep"`
		if [ "X$out" == "X" ]; then
		    catchFail "$PCL ssh -c $CLUSTER_NAME meta-$counter 'sudo sed -i -e \"s/username = .*/username = \\\"$LDAP_ADMIN\\\"/\" $TELEGRAF_CONFIG'"
			catchFail "$PCL ssh -c $CLUSTER_NAME meta-$counter 'sudo sed -i -e \"s/password = .*/password = \\\"$LDAP_PASSWORD\\\"/\" $TELEGRAF_CONFIG'"
			catchFail "$PCL ssh -c $CLUSTER_NAME meta-$counter 'sudo service telegraf start'"
            start=`$PCL ssh -c $CLUSTER_NAME meta-$counter "ps axu | grep telegraf| grep -v grep"`
            if [ "X$start" == "X" ];then
                echo "TELEGRAF DID NOT START ON meta-$counter. EXITING"
                exit 1
            fi
		else
		    echo "COULD NOT STOP TELEGRAF. EXITING"
			exit 1;
		fi
		let counter+=1
	done

    echo `date` "********************* Updating KAPACITOR's username/password to work with LDAP ***************************"
    echo ""
    catchFail "$PCL ssh -c $CLUSTER_NAME kapacitor-0 'sudo service kapacitor stop'"
	out=`$PCL ssh -c $CLUSTER_NAME kapacitor-0 "ps axu | grep kapacitor| grep -v grep"`
	if [ "X$out" == "X" ]; then
        catchFail "$PCL ssh -c $CLUSTER_NAME kapacitor-0 'sudo sed -i -e \"s/username = .*/username = \\\"$LDAP_ADMIN\\\"/\" $KAPACITOR_CONFIG'"
	    catchFail "$PCL ssh -c $CLUSTER_NAME kapacitor-0 'sudo sed -i -e \"s/password = .*/password = \\\"$LDAP_PASSWORD\\\"/\" $KAPACITOR_CONFIG'"
	    catchFail "$SCP -i $PRIVATE_KEY -o StrictHostKeyChecking=no $PRIVATE_KEY $OS@`$PCL host kapacitor-0 -c $CLUSTER_NAME`:/tmp"
	    catchFail "$SSH -i $PRIVATE_KEY -f -o StrictHostKeyChecking=no $OS@`$PCL host kapacitor-0 -c $CLUSTER_NAME` 'sudo $SSH -o StrictHostKeyChecking=no -l tunnel -fN -L 3389:10.0.1.69:389 34.217.54.237 -i /tmp/$PRIVATE_KEY'"
	else
	    echo "COULD NOT STOP THE KAPACITOR.EXITING"
			exit 1
	fi
	catchFail "$PCL ssh -c $CLUSTER_NAME kapacitor-0 'sudo service kapacitor start'"
	start=`$PCL ssh -c $CLUSTER_NAME kapacitor-0 "ps axu | grep kapacitor| grep -v grep"`
	if [ "X$start" == "X" ];then
	    echo "KAPACITOR DID NOT START. EXITING"
		exit 1
	fi
}

while [ $# -gt 0 ]
do
	case $1 in
		--num-data)
            shift
			DATANODES_NUM=$1
			DATANODES="-d $1";;
		--num-meta)
			shift
			METANODES_NUM=$1
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
		--ldap-auth)
		    ldap_auth=true
		    META_LDAP_ALLOWED=",INFLUXDB_META_LDAP_ALLOWED=true";;
		--meta-auth)
		    # for now meta authentication will support basic authentication : username/password
		    # INFLUXDB_META_AUTH_ENABLED=true is equal to auth-enabled = true on meta node - will be set up later.
		    # INFLUXDB_META_META_AUTH_ENABLED=true is equal to meta-auth-enabled = true on data node
		    meta_auth=true
		    META_AUTH=",INFLUXDB_META_META_AUTH_ENABLED=true";;
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
		    NUMBER_OF_KAPACITORS="$1";;
        --kapacitor-os)
            KAPACITOR_OS="--aws-os $";;
        --no-kapacitor)
            install_kapacitor=false;;
        --no-install)
            install=false;;
        --private-key)
            shift
            PRIVATE_KEY="$1";;
	esac
	shift
done


#-------------------------------------
# main()
#------------------------------------

main() {
	if $install; then
        uninstall
        installCluster
	    if $install_chronograf; then
		    installChronograf
	    fi
	    if $install_kapacitor; then
		    installKapacitor
	    fi
        if $meta_auth; then
            enableMetaAuth
        fi
	    if $ldap_auth; then
	        enableLdapAuth
	    fi
	fi
}

main
