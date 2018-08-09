# Using parent image with minimal python packages
# Using python 2.7.14
FROM python:2.7.15-slim

MAINTAINER Gershon Shif "<gershon@influxdata.com>"

COPY . Litmus

# get the latest updates and install sudo, 
# since Litmus is using sudo to install missing python packages
# install curl to be able to get etcdctl
RUN apt-get update && apt-get install -y \
sudo \
curl

# need to install etcdctl:
RUN curl -L https://github.com/coreos/etcd/releases/download/v3.3.9/etcd-v3.3.9-linux-amd64.tar.gz -o etcd-v3.3.9-linux-amd64.tar.gz
RUN tar zxvf etcd-v3.3.9-linux-amd64.tar.gz -C /tmp 
RUN cp /tmp/etcd-v3.3.9-linux-amd64/etcdctl /usr/local/bin

WORKDIR Litmus
RUN cp scripts/litmus_run_master.py .

RUN cp scripts/run_litmus_tests.sh .

ENTRYPOINT ["bash","run_litmus_tests.sh"]
