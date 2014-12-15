FROM datalyse/openstack-base
MAINTAINER Filip Krikava "filip.krikava@inria.fr"

RUN DEBIAN_FRONTEND=noninteractive \
		apt-get update -yqq && \
		apt-get install -yqq \
			apache2 \
			memcached \
			libapache2-mod-wsgi \
			openstack-dashboard && \
		apt-get remove -y --purge openstack-dashboard-ubuntu-theme

ADD run.sh /run.sh
RUN chmod +x /run.sh

EXPOSE 80

CMD ["/run.sh"]
