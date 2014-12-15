FROM datalyse/openstack-base
MAINTAINER Filip Krikava "filip.krikava@inria.fr"

RUN DEBIAN_FRONTEND=noninteractive \
    apt-get update -yqq && \
    apt-get install -yqq \
	    glance \
	    python-glanceclient

ADD run.sh /run.sh
RUN chmod +x /run.sh

ADD bootstrap-pre.yml /bootstrap-pre.yml
ADD bootstrap-post.yml /bootstrap-post.yml

EXPOSE 9191 9292

CMD ["/run.sh"]
