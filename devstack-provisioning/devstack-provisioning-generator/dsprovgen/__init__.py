from copy import deepcopy
import shutil
import argparse
import sys
import os

from pkg_resources import resource_string
import yaml

import drivers
import checkers

CONTROL = "control"
COMPUTE = "compute"
CONFIG = "config"
GROUPS = "groups"
HOSTS = "hosts"
DEVSTACK = "devstack"
MASTER_PASSWORD = "master_password"
ROLE = "role"


class Host(object):
    def __init__(self, hostname, config):
        self.hostname = hostname
        self.config = config
        self.local_conf = []

    def __str__(self):
        return "%s:\n---\n%s" % (self.hostname, yaml.dump(self.config, default_flow_style=False))


def _merge_dicts(*args):
    r = dict()
    for d in args:
        for (k, v) in d.iteritems():
            if k in r and isinstance(v, dict):
                r[k] = _merge_dicts(r[k], v)
            elif isinstance(v, dict):
                r[k] = deepcopy(v)
            else:
                r[k] = v

    return r


def check(hosts):
    checks = [f for f in dir(checkers) if f.startswith("check_")]

    def check_one(h):
        for check_name in checks:
            check_method = getattr(checkers, check_name)
            if not check_method(h):
                sys.exit(1)

    for host in hosts:
        check_one(host)


def configure_devstack(hosts):
    control_host = find_control_host(hosts)

    for host in hosts:
        devstack_config = host.config["devstack"]

        if len(hosts) > 1:
            host.local_conf.append("MULTI_HOST=True")

        # host_ip
        host.local_conf.append("HOST_IP="+host.hostname)

        # config to be copied
        for key in ("dest", "logfile", "screen_logdir", "fixed_range", "floating_range", "flat_interface"):
            host.local_conf.append("%s=%s" % (key.upper(), devstack_config[key]))

        # compute the fixed network size as the
        # 2 ^ (the number of `0`) - 2 (as all 0 and 255 cannot be used)
        netmask = int(devstack_config["fixed_range"].split("/")[1])
        host.local_conf.append("FIXED_NETWORK_SIZE=%s" % (2 ** (32 - netmask) - 2))

        # passwords
        host.local_conf.append("ADMIN_PASSWORD=" + devstack_config["master_password"])
        for key in ("database_password", "rabbit_password", "service_password", "service_token"):
            if key in devstack_config and devstack_config[key] is not None and devstack_config[key] > 0:
                val = devstack_config[key]
            else:
                val = "$ADMIN_PASSWORD"
            host.local_conf.append("%s=%s" % (key.upper(), val))

        # versions
        # TODO: versions
        # - the problem here is how to determine the right versions for the different components
        # - according to stack.sh - clients should always use the master while others should do
        #   differently.

        host.local_conf += devstack_config["local_conf_extra_lines"]

        if host.config[ROLE] == COMPUTE:
            host.local_conf.append("DATABASE_TYPE=mysql")
            host.local_conf.append("SERVICE_HOST=" + control_host.hostname)
            host.local_conf.append("MYSQL_HOST=" + control_host.hostname)
            host.local_conf.append("RABBIT_HOST=" + control_host.hostname)
            host.local_conf.append("GLANCE_HOSTPORT=" + control_host.hostname + ":9292")
            host.local_conf.append("disable_all_services")
            host.local_conf.append("enable_service n-cpu n-net n-api")
            host.local_conf.append("enable_service c-sch c-api c-vol")


def find_control_host(hosts):
    return next((host for host in hosts if host.config[ROLE] == CONTROL))


def run(drivers_names, no_check, clean_output, input_file, output_dir):
    if not os.path.exists(input_file):
        print "%s: no such a file" % input_file
        sys.exit(1)

    if os.path.exists(output_dir) and clean_output:
        shutil.rmtree(output_dir)

    # load drivers
    drivers_classes = []
    for d in drivers_names:
        drivers_classes.append(next((clazz for (name, clazz) in drivers.all_drivers() if name == d)))

    # load defaults
    defaults = yaml.load(resource_string(__name__, "resources/defaults.yml"))
    # load locals
    with open(input_file, "r") as f:
        data = f.read()
        cluster_def = yaml.load(data)

    # merge defaults with user specified configuration overriding defaults when needed
    cluster_def = _merge_dicts(defaults, cluster_def)
    default_config = cluster_def[CONFIG]

    # using the scope defaults < globals < group < host gather all the variables at the host scope
    cluster_hosts = []
    for group in cluster_def[GROUPS]:
        if CONFIG in group:
            config = _merge_dicts(default_config, group[CONFIG])
        else:
            config = {}

        for host in group[HOSTS]:
            if isinstance(host, dict):
                hostname = host.keys()[0]
                del host[hostname]
                config = _merge_dicts(config, host)
            else:
                hostname = host

            cluster_hosts.append(Host(hostname, config))

    configure_devstack(cluster_hosts)

    if not no_check:
        check(cluster_hosts)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for clazz in drivers_classes:
        clazz(output_dir).generate(deepcopy(cluster_hosts))


def parse_args():
    all_drivers = drivers.all_drivers()
    parser = argparse.ArgumentParser(description="Devstack provisioning generator")

    parser.add_argument("-d",
                        nargs="*",
                        dest="drivers_names",
                        default=all_drivers[0][0],
                        choices=[k for (k, v) in all_drivers],
                        help="Target provisioning systems. Available are: %s" % ",".join([k for (k, v) in all_drivers]),
                        metavar="DRIVER")
    parser.add_argument("-c", "--clean-output",
                        action="store_true",
                        dest="clean_output",
                        default=False,
                        required=False,
                        help="Clean output folder")
    parser.add_argument("-n", "--no-check",
                        action="store_true",
                        dest="no_check",
                        required=False,
                        default=False,
                        help="Skip cluster definition check")
    parser.add_argument("-i", "--input",
                        required=True,
                        dest="input_file",
                        metavar="FILE",
                        help="Cluster definition file")
    parser.add_argument("-o", "--output",
                        required=True,
                        dest="output_dir",
                        metavar="DIR",
                        help="Output directory")

    return parser.parse_args()


def main():
    run(**vars(parse_args()))

if __name__ == "__main__":
    main()