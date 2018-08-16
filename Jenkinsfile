currentBuild.result = "SUCCESS" // sets the ordinal as 0 and boolean to true
properties([[$class: 'GithubProjectProperty', displayName: '', projectUrlStr: 'https://github.com/influxdata/idpe/'], pipelineTriggers([cron('@midnight')])])
node('dind') {
	container('dind') {
		withCredentials([usernamePassword(credentialsId: 'quay-k8scloud', passwordVariable: 'QUAYPASS', usernameVariable: 'QUAYUSER')]) {
   			stage('Deploy Test Environment') {
	    			try {
                			httpRequest consoleLogResponseBody: true, contentType: 'APPLICATION_JSON', httpMode: 'POST', requestBody: '{"name": "cpg"}', responseHandle: 'NONE', url: 'http://fenvd.fenv.svc.cluster.local/v1/env', validResponseCodes: '100:500'
                			sleep time: 1, unit: 'MINUTES'
	    			} catch (err) {
					currentBuild.result = "FAILURE" // sets the ordinal as 4 and boolean to false
                			throw err
	    			}
        		}
    			stage('Running Integration Tests') {
				try {
					sh '''
        					docker login -u="${QUAYUSER}" -p="${QUAYPASS}" quay.io
                				docker run --rm -e ETCD_HOST=http://etcd.cpg.svc.cluster.local:2379 -e GATEWAY_HOST=http://gateway.cpg.svc.cluster.local:9999 -e QUERYD_HOST=http://queryd.cpg.svc.cluster.local:8093 -e TEST_LIST=tests_lists/gateway_api_tests.list -v $PWD:/Litmus/result quay.io/influxdb/litmus:latest
					'''
    				} catch (err) {
					currentBuild.result = "FAILURE" // sets the ordinal as 4 and boolean to false
                                        throw err
				} finally {
					httpRequest consoleLogResponseBody: true, contentType: 'APPLICATION_JSON', httpMode: 'DELETE', responseHandle: 'NONE', url: 'http://fenvd.fenv.svc.cluster.local/v1/env/cpg', validResponseCodes: '202'
					archiveArtifacts allowEmptyArchive: true, artifacts: '**', defaultExcludes: false
					junit allowEmptyResults: true, testResults: '*.xml'
					step([$class: 'InfluxDbPublisher',
							customData: null,
							customDataMap: null,
							customPrefix: null,
							target: 'monitoring'])
            			}

        
			}
		}
	}
}	
