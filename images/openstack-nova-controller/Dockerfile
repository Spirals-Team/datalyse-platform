FROM datalyse/openstack-base
MAINTAINER Filip Krikava "filip.krikava@inria.fr"

RUN DEBIAN_FRONTEND=noninteractive \
		apt-get update -yqq && \
		apt-get install -yqq \
	    nova-api \
	    nova-cert \
	    nova-conductor \
	    nova-consoleauth \
	    nova-novncproxy \
	    nova-scheduler \
	    python-novaclient

ADD run.sh /run.sh
RUN chmod +x /run.sh

ADD bootstrap-pre.yml /bootstrap-pre.yml
ADD bootstrap-post.yml /bootstrap-post.yml

EXPOSE 8774 6080

CMD ["/run.sh"]
