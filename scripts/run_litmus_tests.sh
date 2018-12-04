#!/bin/bash
set -x

KUBE_CONFIG=result/config
export KUBECONFIG=$KUBE_CONFIG
if [ "X$KUBE_CLUSTER" == "X" ]; then
    KUBE_CLUSTER=docker-for-desktop
fi

if [ "X$TEST_LIST" != "X" ] && [ "X$ONE_TEST" != "X" ]; then
	echo "SHOULD ONLY PROVIDE ONE OF THE TWO OPTIONS. EITHER TEST_LIST OR ONE_TEST TO RUN"
	exit 1
fi
if [ "X$TEST_LIST" != "X" ]; then
	echo ""
	echo "RUNNING python litmus_run_master.py --no-chronograf --etcd $ETCD_HOST --gateway $GATEWAY_HOST "`\
	                                        `"--flux $QUERYD_HOST --etcd_tasks $ETCD_TASKS_HOST "`\
	                                        `"--transpilerde $TRANSPILERDE_HOST --namespace $NAMESPACE "`\
	                                        `"--storage $STORAGE_HOST --kubeconf $KUBE_CONFIG "`\
	                                        `"--kubecluster $KUBE_CLUSTER --tests-list $TEST_LIST --product-version 2"
	echo ""
	python litmus_run_master.py --no-chronograf \
	                            --etcd $ETCD_HOST \
	                            --gateway $GATEWAY_HOST \
	                            --flux $QUERYD_HOST \
	                            --etcd_tasks $ETCD_TASKS_HOST \
	                            --transpilerde $TRANSPILERDE_HOST \
	                            --namespace $NAMESPACE \
	                            --storage $STORAGE_HOST \
	                            --kubeconf $KUBE_CONFIG \
	                            --tests-list $TEST_LIST \
	                            --kubecluster $KUBE_CLUSTER \
	                            --product-version 2
elif [ "X$ONE_TEST" != "X" ]; then
	echo ""
	echo "RUNNING python litmus_run_master.py --no-chronograf --etcd $ETCD_HOST --gateway $GATEWAY_HOST "`\
	                                        `"--flux $QUERYD_HOST --etcd_tasks $ETCD_TASKS_HOST "`\
	                                        `"--transpilerde $TRANSPILERDE_HOST --namespace $NAMESPACE "`\
	                                        `"--storage $STORAGE_HOST --kubeconf $KUBE_CONFIG "`\
	                                        `"--kubecluster $KUBE_CLUSTER --tests $ONE_TEST --product-version 2"
	echo ""
	python litmus_run_master.py --no-chronograf \
	                            --etcd $ETCD_HOST \
	                            --gateway $GATEWAY_HOST \
	                            --flux $QUERYD_HOST \
	                            --etcd_tasks $ETCD_TASKS_HOST \
	                            --transpilerde $TRANSPILERDE_HOST \
	                            --namespace $NAMESPACE \
	                            --storage $STORAGE_HOST \
	                            --kubeconf $KUBE_CONFIG \
	                            --kubecluster $KUBE_CLUSTER \
	                            --tests $ONE_TEST \
	                            --product-version 2
fi
# Return success or failure ( 0 - success )
EXIT_STATUS=$?

# remove config file so it won't be archived
rm -rf result/config

if [ -f report.html ]; then
	echo "COPYING report.html TO result DIRECTORY"
	cp report.html result
fi
if [ -f result.xml ]; then
	echo "COPYING result.xml TO result DIRECTORY"
	cp result.xml result
fi
if [ -d assets ]; then
	echo "COPYING assets DIRECTORY TO result DIRECTORY"
	cp -r assets result
fi
if [ "$EXIT_STATUS" -eq 0 ]; then
	PASSED=true
else
	PASSED=false
fi
$PASSED
