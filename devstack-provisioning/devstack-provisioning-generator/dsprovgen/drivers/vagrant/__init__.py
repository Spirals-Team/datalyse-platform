from pkg_resources import resource_string
from string import Template
import os

import dsprovgen

VAGRANTFILE = "Vagrantfile"


class VagrantDriver(dsprovgen.drivers.Driver):
    def generate(self, hosts, **kwargs):

        nodes = []
        for (idx, host) in enumerate(hosts):
            if host.config[dsprovgen.ROLE] == dsprovgen.CONTROL:
                cpus = 4
                memory = 4096
            else:
                cpus = 2
                memory = 2048

            if "vagrant" in host.config:
                vagrant = host.config["vagrant"]
                if "cpus" in vagrant:
                    cpus = int(vagrant["cpus"])
                if "memory" in vagrant:
                    memory = int(vagrant["memory"])

            name = "%s-%d" % (host.config[dsprovgen.ROLE].lower(), idx)

            nodes.append(
                '{ :ip => "%s", :name => "%s", :cpus => %d, :memory => %d}' % (host.hostname, name, cpus, memory))

        template = Template(resource_string(__name__, "resources/" + VAGRANTFILE))
        res = template.substitute(nodes=",\n  ".join(nodes))

        with open(os.path.join(self.output_dir, VAGRANTFILE), "wt") as f:
            f.write(res)

    def __str__(self):
        return "Vagrant generator"