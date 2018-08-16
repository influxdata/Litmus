def build(imageTag) {
  sh "make -e IMG_TAG=${imageTag} image/build"
  withCredentials([usernamePassword(credentialsId: 'quay-k8scloud', passwordVariable: 'QUAYPASS', usernameVariable: 'QUAYUSER')]) {
    sh "docker login -u=\"${QUAYUSER}\" -p=\"${QUAYPASS}\" quay.io"
    sh "make -e IMG_TAG=${imageTag} image/publish"
  }

  if (env.BRANCH_NAME == "master") {
    sh "make -e IMG_TAG=${imageTag} image/publish-latest"
  }
}

return this

// vim: set ts=4 sw=4:

