from pkg_resources import resource_string
from string import Template
import os
import yaml

import dsprovgen

ANSIBLE_CFG = "ansible.cfg"
ANSIBLE_HOSTS = "ansible_hosts"
ANSIBLE_HOST_VARS = "host_vars"
ANSIBLE_GROUP_VARS = "group_vars"
ANSIBLE_GROUP_VARS_ALL = "all"
ANSIBLE_TEMPLATES = "templates"

CONFIG_MAPPING = {
    "ssh_username": "ansible_ssh_user",
    "ssh_port": "ansible_ssh_port",
    "ssh_host": "ansible_ssh_host",
    "ssh_private_key": "ansible_ssh_private_key_file",
    "username": None,
    "password": None,
    "repo": "devstack_repo",
    "version": "devstack_version"
}


def _create_if_missing(path):
    if not os.path.exists(path):
        os.makedirs(path)

    return path


def _copy_resource(source, target):
    _create_if_missing(os.path.dirname(target))

    res = resource_string(__name__, source)
    with open(target, "wt") as f:
        f.write(res)


class AnsibleDriver(dsprovgen.drivers.Driver):
    def _generate_ansible_cfg(self):
        with open(os.path.join(self.output_dir, ANSIBLE_CFG), "wt") as f:
            f.write(("[defaults]\n"
                     "host_key_checking = False\n"
                     "hostfile = %s\n" % ANSIBLE_HOSTS))

    def _generate_ansible_hosts(self, hosts):
        template = Template(resource_string(__name__, "resources/" + ANSIBLE_HOSTS))
        res = template.substitute(
            control_nodes="\n".join(
                [host.hostname for host in hosts if host.config[dsprovgen.ROLE] == dsprovgen.CONTROL]),
            compute_nodes="\n".join(
                [host.hostname for host in hosts if host.config[dsprovgen.ROLE] == dsprovgen.COMPUTE]))

        with open(os.path.join(self.output_dir, ANSIBLE_HOSTS), "wt") as f:
            f.write(res)

    def _generate_host_vars(self, hosts):
        host_vars_dir = _create_if_missing(os.path.join(self.output_dir, ANSIBLE_HOST_VARS))

        for host in hosts:
            host_vars = {"host_ip": host.hostname,
                         "devstack_home": "/home/%s/%s" % (host.config["username"], host.config["install_dir"])}

            for k, v in CONFIG_MAPPING.iteritems():
                if k in host.config:
                    if v is None:
                        host_vars[k] = host.config[k]
                    else:
                        host_vars[v] = host.config[k]

            host_vars["local_conf"] = host.local_conf

            with open(os.path.join(host_vars_dir, host.hostname), "wt") as f:
                f.write(yaml.dump(host_vars, default_flow_style=False))

    def _generate_group_vars(self, hosts):
        control = dsprovgen.find_control_host(hosts)

        group_vars = {"openstack_username": "admin",
                      "openstack_password": control.config[dsprovgen.DEVSTACK][dsprovgen.MASTER_PASSWORD],
                      "openstack_tenant_name": "admin",
                      "openstack_auth_url": "http://%s:5000/v2.0" % control.hostname}

        group_vars_dir = _create_if_missing(os.path.join(self.output_dir, ANSIBLE_GROUP_VARS))

        with open(os.path.join(group_vars_dir, ANSIBLE_GROUP_VARS_ALL), "wt") as f:
            f.write(yaml.dump(group_vars, default_flow_style=False))

    def generate(self, hosts, **kwargs):
        self._generate_ansible_cfg()
        self._generate_ansible_hosts(hosts)
        self._generate_group_vars(hosts)
        self._generate_host_vars(hosts)

        _copy_resource("resources/local.conf.j2",
                       os.path.join(self.output_dir, ANSIBLE_TEMPLATES, "local.conf.j2"))
        _copy_resource("resources/site.yml", os.path.join(self.output_dir, "site.yml"))
        _copy_resource("resources/devstack.yml", os.path.join(self.output_dir, "devstack.yml"))

    def __str__(self):
        return "Ansible generator"
