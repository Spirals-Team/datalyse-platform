FROM datalyse/openstack-base
MAINTAINER Filip Krikava "filip.krikava@inria.fr"

RUN DEBIAN_FRONTEND=noninteractive \
    apt-get update -yqq && \
    apt-get install -yqq \
	    nova-network \
	    nova-api-metadata \
	    python-pip \
	    nova-compute-kvm

# Install latest docker
RUN curl -sSL https://get.docker.com/ubuntu/ | sh -x

ADD entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ADD wrapdocker.sh /wrapdocker.sh
RUN chmod +x /wrapdocker.sh

ADD bootstrap-pre.yml /bootstrap-pre.yml

ADD supervisord.conf /supervisord.conf

# TODO: do we need to export this port here?
EXPOSE 8774

VOLUME /var/lib/docker
VOLUME /src

ENTRYPOINT ["/entrypoint.sh"]
CMD ["/usr/bin/supervisord", "-c", "/supervisord.conf"]
