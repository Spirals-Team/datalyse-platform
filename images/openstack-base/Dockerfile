FROM ubuntu:14.04
MAINTAINER Filip Krikava "filip.krikava@inria.fr"

RUN DEBIAN_FRONTEND=noninteractive \
    apt-get update -yqq && \
    apt-get install -yqq \
      git \
      ntp \
      curl \
      tmux \
      multitail \
      python-mysqldb \
      supervisor \
      software-properties-common \
      python-software-properties

# add juno repository
RUN add-apt-repository -y cloud-archive:juno

# install ansible (apt-add-repository comes from software-properties-common)
RUN apt-add-repository -y ppa:rquillo/ansible && \
    apt-get update -yqq && \
    apt-get install -yqq ansible

ADD mtail.sh /mtail.sh
RUN chmod +x /mtail.sh
