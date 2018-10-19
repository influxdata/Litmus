# Using parent image with minimal python packages
# Using python 2.7.14
FROM python:2.7.15-slim

MAINTAINER Gershon Shif "<gershon@influxdata.com>"

COPY . Litmus

# get the latest updates and install sudo, 
# since Litmus is using sudo to install missing python packages
# install curl to be able to get etcdctl
RUN apt-get update && apt-get install -y curl

# Install required python modules
RUN pip install --no-cache-dir requests[security]==2.17.3
RUN pip install --no-cache-dir pytest==3.0.7
RUN pip install --no-cache-dir python-dateutil==2.6.1
RUN pip install --no-cache-dir pytest-html==1.6.0
RUN pip install --no-cache-dir pytest-metadata==1.5.0
RUN pip install --no-cache-dir influxdb

# Install  etcdctl:
RUN curl -L https://github.com/coreos/etcd/releases/download/v3.3.9/etcd-v3.3.9-linux-amd64.tar.gz -o etcd-v3.3.9-linux-amd64.tar.gz
RUN tar zxvf etcd-v3.3.9-linux-amd64.tar.gz -C /tmp 
RUN cp /tmp/etcd-v3.3.9-linux-amd64/etcdctl /usr/local/bin

# Install kubectl
RUN apt-get install -y apt-transport-https
RUN apt-get install -y gnupg
RUN curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
RUN echo "deb http://apt.kubernetes.io/ kubernetes-xenial main" | tee -a /etc/apt/sources.list.d/kubernetes.list
RUN apt-get update
RUN apt-get install -y kubectl
RUN cp /usr/bin/kubectl /usr/local/bin/kubectl

WORKDIR Litmus
RUN cp scripts/litmus_run_master.py .
RUN cp scripts/run_litmus_tests.sh .

ENTRYPOINT ["bash","run_litmus_tests.sh"]
