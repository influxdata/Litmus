currentBuild.result = "SUCCESS" // sets the ordinal as 0 and boolean to true
// In case JOB_NAME has a forward slash in its name replace it with dash
env.JOB_NAME = "${JOB_NAME}".replaceAll("/","-")
properties([[$class: 'GithubProjectProperty', displayName: '', projectUrlStr: 'https://github.com/influxdata/idpe/'], pipelineTriggers([cron('@midnight')])])
node('dind') {
	container('dind') {
		withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG'),
		                usernamePassword(credentialsId: 'quay-k8scloud', passwordVariable: 'QUAYPASS', usernameVariable: 'QUAYUSER')]) {
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
					    sh "cp $KUBECONFIG config"
						sh "printenv"
						sh """
                			docker run --rm -e ETCD_HOST=http://etcd."lit-${env.JOB_NAME}-${env.BUILD_ID}".svc.cluster.local:2379 -e GATEWAY_HOST=http://gateway."lit-${env.JOB_NAME}-${env.BUILD_ID}".svc.cluster.local:9999 -e QUERYD_HOST=http://queryd."lit-${env.JOB_NAME}-${env.BUILD_ID}".svc.cluster.local:8093 -e TRANSPILERDE_HOST=http://transpilerde."lit-${env.JOB_NAME}-${env.BUILD_ID}".svc.cluster.local:8098 -e NAMESPACE="lit-${env.JOB_NAME}-${env.BUILD_ID}" -e STORAGE_HOST=http://storage."lit-bucket-${env.BUILD_ID}".svc.cluster.local:6060 -e TEST_LIST=tests_lists/gateway_api_tests.list -v "${env.WORKSPACE}":/Litmus/result quay.io/influxdb/litmus:latest
						"""
					slackSend (channel: "#testing",color: "#00FF00", message: "SUCCESSFUL: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
					}
    			} catch (err) {
					currentBuild.result = "FAILURE" // sets the ordinal as 4 and boolean to false
					slackSend (channel: "#testing",color: "#FF0000", message: "FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
					throw err
				} finally {
					sh "ls -lR"
					sh """
					    docker run --entrypoint "/ctl/fenvctl" --rm quay.io/influxdb/fenvd --host "http://fenvd.fenv.svc.cluster.local" del "lit-${env.JOB_NAME}-${env.BUILD_ID}"
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
<<<<<<< HEAD
}	
=======
}

def triggerOnDirChange(String targetBranch, String branch, String subfolder) {\
    List<String> changedFiles = sh(returnStdout: true, script: "git diff --name-only ${targetBranch}..${branch} ${subfolder}").split()

    if (changedFiles.size() > 0) {
        return true
    }

    return false
}

def triggerOnGolangChange(String targetBranch, String branch, String subfolder) {\
    sh """GOOS=linux GOARCH=amd64 CGO_ENABLED=0 go build -ldflags='-s -w' -o dirty ./cmd/dirty/main.go"""
    List<String> changedFiles = sh(returnStdout: true, script: "git diff --name-only ${targetBranch}..${branch} | GOPATH=${GOPATH} ./dirty -dir ${subfolder}").split()

    if (changedFiles.size() > 0) {
        for (file in changedFiles) {
            println file
        }
        return true
    }

    return false
}

def commitHashForBuild(build) {
    def scmAction = build?.actions.find { action -> action instanceof jenkins.scm.api.SCMRevisionAction }
    return scmAction?.revision?.hash
}


def getLastSuccessfulCommit() {
    def lastSuccessfulHash = null
    def lastSuccessfulBuild = currentBuild.rawBuild.getPreviousSuccessfulBuild()
    if (lastSuccessfulBuild) {
        lastSuccessfulHash = commitHashForBuild(lastSuccessfulBuild)
    }
    return lastSuccessfulHash
}

node("dind") {
    def appProjects = [
        "apps/fenv",
        "apps/welcome-internal",
        "apps/kafka",
        "apps/docs",
        "litmus"
    ]

    def goProjects = [
        "cmd/gatewayd": "apps/gateway",
        "cmd/queryd": "apps/queryd",
        "cmd/taskd": "apps/tasks",
        "cmd/transpilerde": "apps/transpilerde",
        "cmd/storage": "apps/storage",
        "cmd/operator": "apps/operator"
    ]

    // If not in a PR and not in master branch, discard the build
    if (!env.CHANGE_TARGET && env.BRANCH_NAME != "master") {
      echo "Skip CI for branch different than master and not in a PR"
      return
    }

    container('dind') {
        sh "apk update"
        sh "apk add --no-cache make git curl bash wget go musl-dev"
        sh 'curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl'
        sh "chmod +x ./kubectl"
        sh "mv ./kubectl /bin/kubectl"

        withEnv(['GOPATH=' + pwd()]) {
            dir('src/github.com/influxdata/idpe') {
                checkout scm

                // Generate a netrc
                withCredentials([usernamePassword(credentialsId: 'bowie-bot', passwordVariable: 'PASSWORD', usernameVariable: 'USERNAME')]) {
                    def netrc = "machine github.com\n\tlogin ${USERNAME}\n\tpassword ${PASSWORD}"
                    sh "echo '${netrc}' > .netrc"
                }
                stage("Testing") {
                    sh "docker build -t quay.io/influxdb/golang:1.11.1 -f apps/testing/Dockerfile ."
                    // Run unit and integration tests
                    def PWD = pwd();
                    // Set JENKINS_URL so that tests configured to skip on Jenkins, skip as expected.
                    sh "docker run --memory=8g --rm --env JENKINS_URL=x --env ETCD_ADDR=etcd.testing.svc.cluster.local:2379 --env GOCACHE=/tmp/gocache -v /tmp/gocache:/tmp/gocache -v $PWD:/out quay.io/influxdb/golang:1.11.1 -i -r"
                    junit 'idpe.junit.xml'
                    archiveArtifacts artifacts: 'tests.log'
                }

                def diffLeftBranch = "origin/${env.CHANGE_TARGET}"
                def diffRightBranch = "origin/${env.BRANCH_NAME}"

                // If it's not the master, the image tag is the name of the branch,
                // on PRs the name of the branch is actually PR-<number>
                def imageTag = "${env.BRANCH_NAME}"
                if (env.BRANCH_NAME == "master") {
                    diffLeftBranch = "origin/master"
                    diffRightBranch = getLastSuccessfulCommit()
                    // In master use a short 7 commit id
                    imageTag = sh(returnStdout: true, script: "git rev-parse --short=7 HEAD").trim()
                }


                // Check against each app subfolder if there's any change
                // and if there is call the subfolder's build.groovy
                stage("apps") {
                    parallel appProjects.collectEntries {
                        ["Building ${it}": {
                            def doTrigger = triggerOnDirChange(diffLeftBranch, diffRightBranch, it)
                            if (doTrigger) {
                                dir(it) {
                                    // if litmus project has changed, then use PR as a litmus image tag
                                    if (it == "litmus") {
                                      litmusChange = true
                                    }
                                    def project = load "build.groovy"
                                    project.build(imageTag)
                                }
                            } else {
                                echo "This subfolder has been skipped since there where no changes in it - YaY - Less changes, less damages!"
                            }
                        }]
                    }
                }

                // Check against the docs folder and build if the docs have been changed.
                stage("docs") {
                    def doTrigger = triggerOnDirChange(diffLeftBranch, diffRightBranch, "docs")
                    if (doTrigger) {
                        dir("apps/docs") {
                            def project = load "build.groovy"
                            project.build(imageTag)
                        }
                    } else {
                        echo "The docs build has been skipped, looks like you're not documenting your stuff!"
                    }
                }

                // Check against each go project to build and if there's any change
                // to the dependent files, build it.
                stage("cmd") {
                    parallel goProjects.collectEntries { cli, pkg ->
                        ["Building ${cli}": {
                            def doTrigger = triggerOnGolangChange(diffLeftBranch, diffRightBranch, cli)
                            if (doTrigger) {
                                dir(pkg) {
                                    def project = load "build.groovy"
                                    project.build(imageTag)
                                    // set component image to the imageTag
                                    if (env.BRANCH_NAME != "master") {
                                        setComponentImg(cli, imageTag)
                                    }
                                    if (env.BRANCH_NAME == "master") {
                                       // Add a chronograf annotation about deploying this package to k8s.
                                       def CUR_UNIX_TIME = sh returnStdout: true, script: 'date +\'%s\'000000000'
                                       CUR_UNIX_TIME = CUR_UNIX_TIME.trim()
                                       def GUID = sh returnStdout: true, script: 'cat /proc/sys/kernel/random/uuid'
                                       GUID = GUID.trim()
                                       sh "set -x;  curl -i -XPOST http://influxdb.monitoring.svc.cluster.local:8086/write?db=chronograf --data-binary 'annotations,id=${GUID},app=${pkg},image=${imageTag} deleted=false,start_time=${CUR_UNIX_TIME}i,modified_time_ns=${CUR_UNIX_TIME}i,text=\"deploy ${pkg}:${imageTag}\" ${CUR_UNIX_TIME}'"
                                    }
                                }
                            } else {
                                echo "This subfolder has been skipped since there where no changes in it - YaY - Less changes, less damages!"
                            }
                        }]
                    }
                }
                stage("E2E Smoke Test") {
		            withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG'),
					    usernamePassword(credentialsId: 'quay-k8scloud', passwordVariable: 'QUAYPASS', usernameVariable: 'QUAYUSER')]) {
		              def litmusTag = "latest"
		              if (litmusChange) {
				            litmusTag = "${env.BRANCH_NAME}"
				            if (env.BRANCH_NAME == "master") {
					            litmusTag = "latest"
				            }
		              }
		            currentBuild.result = "SUCCESS" // sets the ordinal as 0 and boolean to true
		            // In case BRANCH_NAME has a forward slash in its name replace it with dash
		            // Name of the namespace should be lowercase
		            env.BRANCH_NAME = "${BRANCH_NAME}".replaceAll("/","-").toLowerCase()
		            try {
			            slackSend (channel: "#testing",color: "#FFFF00", message: "STARTED: Job '${env.BRANCH_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")	
                            // Setting test cluster
			            sh """
                            docker login -u="${QUAYUSER}" -p="${QUAYPASS}" quay.io
			                docker run --entrypoint "/ctl/fenvctl" --rm quay.io/influxdb/fenvd --transpilerde-image ${compImg.transpilerde} --tasks-image ${compImg.tasks} --storage-image ${compImg.storage} --queryd-image ${compImg.queryd} --gateway-image ${compImg.gateway}  --host "http://fenvd.fenv.svc.cluster.local" new "lit-${env.BRANCH_NAME}-${env.BUILD_ID}"
			            """
                        // Running tests
			            timeout(time: 10, unit: "MINUTES") {
			                sh "cp $KUBECONFIG config"
			                sh """
			                    docker run --rm -e ETCD_HOST=http://etcd."lit-${env.BRANCH_NAME}-${env.BUILD_ID}".svc.cluster.local:2379 -e GATEWAY_HOST=http://gateway."lit-${env.BRANCH_NAME}-${env.BUILD_ID}".svc.cluster.local:9999 -e QUERYD_HOST=http://queryd."lit-${env.BRANCH_NAME}-${env.BUILD_ID}".svc.cluster.local:8093 -e TRANSPILERDE_HOST=http://transpilerde."lit-${env.BRANCH_NAME}-${env.BUILD_ID}".svc.cluster.local:8098 -e NAMESPACE="lit-${env.BRANCH_NAME}-${env.BUILD_ID}" -e STORAGE_HOST=http://storage."lit-${env.BRANCH_NAME}-${env.BUILD_ID}".svc.cluster.local:6060 -e KUBE_CLUSTER=influx-internal -e ONE_TEST=src/cloud/rest_api/smoke/test_smoke.py -v "${env.WORKSPACE}"/src/github.com/influxdata/idpe:/Litmus/result quay.io/influxdb/litmus:"${litmusTag}"
			                """
			                slackSend (channel: "#testing",color: "#00FF00", message: "SUCCESSFUL: Job '${env.BRANCH_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
			                // if branch master then start the rest of integration tests
			                if (env.BRANCH_NAME == "master") {
			                    //start the integration tests
			                    echo "Starting litmus integration tests"
			                    build job: 'k8s-cloud/Litmus/litmus_organization_tests', wait: false
			                    build job: 'k8s-cloud/Litmus/litmus_buckets_tests', wait: false
			                    build job: 'k8s-cloud/Litmus/litmus_user_tests', wait: false
			                }
		                }
		            } catch (err) {
			            currentBuild.result = "FAILURE" // sets the ordinal as 4 and boolean to false
			            slackSend (channel: "#testing",color: "#FF0000", message: "FAILED: Job '${env.BRANCH_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
			            throw err
		            } finally {
			            sh """
			                docker run --entrypoint "/ctl/fenvctl" --rm quay.io/influxdb/fenvd --host "http://fenvd.fenv.svc.cluster.local" del "lit-${env.BRANCH_NAME}-${env.BUILD_ID}"
			            """
			            archiveArtifacts allowEmptyArchive: true, artifacts: 'test_smoke.log', defaultExcludes: false
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
        sh "docker system prune -a -f"
    }
}

// vim: set ts=4 sw=4:
>>>>>>> af9b9cd4d... test (litmus): verifying if data made it to kafka (#1971)
