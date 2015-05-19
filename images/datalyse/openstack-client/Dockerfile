FROM datalyse/openstack-base
MAINTAINER Filip Krikava "filip.krikava@inria.fr"

RUN DEBIAN_FRONTEND=noninteractive \
    apt-get update -yqq && \
    apt-get install -yqq \
	    python-keystoneclient \
	    python-glanceclient \
	    python-novaclient \
	    python-heatclient \
	    python-cinderclient \
	    mysql-client \
	    python-pip \
	    openssh-server

# Install latest docker
RUN curl -sSL https://get.docker.com/ubuntu/ | sh -x

# # install ansible openstack module
# RUN git clone https://github.com/fikovnik/openstack-ansible-modules.git /opt/openstack-ansible-modules
# ENV ANSIBLE_LIBRARY /usr/share/ansible/:/opt/openstack-ansible-modules

ADD admin-id_rsa /root/.ssh/id_rsa
ADD admin-id_rsa.pub /root/.ssh/id_rsa.pub
RUN chmod 700 /root/.ssh && \
    chmod 600 /root/.ssh/id_rsa && \
    chmod 644 /root/.ssh/id_rsa.pub

ADD openrc.sh /root/openrc.sh
ADD admin-openrc.sh /root/admin-openrc.sh
RUN chmod +x /root/*openrc.sh

ADD entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# SSHD
RUN mkdir /var/run/sshd

RUN echo 'root:root' | chpasswd

RUN sed -ri 's/^PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -ri 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config

EXPOSE 22

ENTRYPOINT ["/entrypoint.sh"]
CMD ["/usr/sbin/sshd", "-D"]
