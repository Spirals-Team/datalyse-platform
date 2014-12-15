FROM datalyse/openstack-base
MAINTAINER Filip Krikava "filip.krikava@inria.fr"

RUN DEBIAN_FRONTEND=noninteractive \
    apt-get update -yqq && \
    apt-get install -yqq \
	    libvirt-bin \
	    nova-network \
	    nova-api-metadata \
	    nova-compute-kvm

ADD run.sh /run.sh
RUN chmod +x /run.sh

ADD bootstrap-pre.yml /bootstrap-pre.yml

EXPOSE 8774

CMD ["/run.sh"]
