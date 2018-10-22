#!/bin/bash
set -x

KUBE_CONFIG=result/config
export KUBECONFIG=$KUBE_CONFIG
ETCD_HOST=$ETCD_HOST
GATEWAY_HOST=$GATEWAY_HOST
QUERYD_HOST=$QUERYD_HOST
TRANSPILERDE_HOST=$TRANSPILERDE_HOST
NAMESPACE=$NAMESPACE
STORAGE_HOST=$STORAGE_HOST
TEST_LIST=$TEST_LIST
ONE_TEST=$ONE_TEST


if [ "X$TEST_LIST" != "X" ] && [ "X$ONE_TEST" != "X" ]; then
	echo "SHOULD ONLY PROVIDE ONE OF THE TWO OPTIONS. EITHER TEST_LIST OR ONE_TEST TO RUN"
	exit 1
fi
if [ "X$TEST_LIST" != "X" ]; then
	echo ""
	echo "RUNNING python litmus_run_master.py --no-chronograf --etcd $ETCD_HOST --gateway $GATEWAY_HOST --flux $QUERYD_HOST --transpilerde $TRANSPILERDE_HOST --namespace $NAMESPACE --storage $STORAGE_HOST--tests-list $TEST_LIST --product-version 2"
	echo ""
	python litmus_run_master.py --no-chronograf --etcd $ETCD_HOST --gateway $GATEWAY_HOST --flux $QUERYD_HOST --transpilerde $TRANSPILERDE_HOST --namespace $NAMESPACE --storage $STORAGE_HOST --tests-list $TEST_LIST --product-version 2
elif [ "X$ONE_TEST" != "X" ]; then
	echo ""
	echo "RUNNING python litmus_run_master.py --no-chronograf --etcd $ETCD_HOST --gateway $GATEWAY_HOST --flux $QUERYD_HOST --transpilerde $TRANSPILERDE_HOST --namespace $NAMESPACE --storage $STORAGE_HOST --tests $ONE_TEST --product-version 2"
	echo ""
	python litmus_run_master.py --no-chronograf --etcd $ETCD_HOST --gateway $GATEWAY_HOST --flux $QUERYD_HOST --transpilerde $TRANSPILERDE_HOST --namespace $NAMESPACE --storage $STORAGE_HOST --tests $ONE_TEST --product-version 2
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
