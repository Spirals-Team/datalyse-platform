def all_drivers():
    from dsprovgen.drivers import vagrant, ansible

    return (('ansible', ansible.AnsibleDriver),
            ('vagrant', vagrant.VagrantDriver))


class Driver(object):
    def __init__(self, output_dir):
        self.output_dir = output_dir

    def generate(self, hosts, **kwargs):
        raise NotImplementedError()