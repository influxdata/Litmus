currentBuild.result = "SUCCESS" // sets the ordinal as 0 and boolean to true
// In case JOB_NAME has a forward slash in its name replace it with dash
env.JOB_NAME = "${JOB_NAME}".replaceAll("/","-")
properties([[$class: 'GithubProjectProperty', displayName: '', projectUrlStr: 'https://github.com/influxdata/idpe/'], pipelineTriggers([cron('@midnight')])])
node('dind') {
	container('dind') {
		withCredentials([usernamePassword(credentialsId: 'quay-k8scloud', passwordVariable: 'QUAYPASS', usernameVariable: 'QUAYUSER')]) {
   			stage('Deploy Test Environment') {
				try {  
					slackSend (channel: "#testing",color: "#FFFF00", message: "STARTED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")	
					sh """
					docker login -u="${QUAYUSER}" -p="${QUAYPASS}" quay.io
					docker run --entrypoint "/ctl/fenvctl" --rm quay.io/influxdb/fenvd --host "http://fenvd.fenv.svc.cluster.local" new "lit-${env.JOB_NAME}-${env.BUILD_ID}"
	    				"""
				} catch (err) {
					currentBuild.result = "FAILURE" // sets the ordinal as 4 and boolean to false
					slackSend (channel: "#testing",color: "#FF0000", message: "FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
                			throw err
	    			}
        		}
    			stage('Running Integration Tests') {
				try {
					timeout(time: 90, unit: "MINUTES"){
						sh "printenv"
						sh """
        					docker login -u="${QUAYUSER}" -p="${QUAYPASS}" quay.io
                				docker run --rm -e ETCD_HOST=http://etcd."lit-${env.JOB_NAME}-${env.BUILD_ID}".svc.cluster.local:2379 -e GATEWAY_HOST=http://gateway."lit-${env.JOB_NAME}-${env.BUILD_ID}".svc.cluster.local:9999 -e QUERYD_HOST=http://queryd."lit-${env.JOB_NAME}-${env.BUILD_ID}".svc.cluster.local:8093 -e TEST_LIST=tests_lists/gateway_api_tests.list -v "${env.WORKSPACE}":/Litmus/result quay.io/influxdb/litmus:latest
						"""
					slackSend (channel: "#testinng",color: "#00FF00", message: "SUCCESSFUL: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
					}
    				} catch (err) {
					currentBuild.result = "FAILURE" // sets the ordinal as 4 and boolean to false
					slackSend (channel: "#testing",color: "#FF0000", message: "FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
                                        throw err
				} finally {
					sh "ls -lR"
					sh """
					docker run --entrypoint "/ctl/fenvctl" --rm quay.io/influxdb/fenvd --host "http://fenvd.fenv.svc.cluster.local" del "lit-${env.JOB_NAME}-${env.BUILD_ID}"
					docker run --entrypoint "/ctl/fenvctl" --rm quay.io/influxdb/fenvd --host "http://fenvd.fenv.svc.cluster.local" get all
					"""
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
