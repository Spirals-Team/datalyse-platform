FROM datalyse/openstack-base
MAINTAINER Filip Krikava "filip.krikava@inria.fr"

RUN DEBIAN_FRONTEND=noninteractive \
		apt-get update -yqq && \
		apt-get install -yqq \
			keystone

ADD run.sh /run.sh
RUN chmod +x /run.sh

ADD bootstrap-pre.yml /bootstrap-pre.yml
ADD bootstrap-post.yml /bootstrap-post.yml

EXPOSE 35357 5000

CMD ["/run.sh"]
