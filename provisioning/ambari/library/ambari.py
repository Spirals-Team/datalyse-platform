#!/usr/bin/python
#

# (c) 2015, Filip Krikava <krikava@gmail.com>

######################################################################

DOCUMENTATION = '''
---
module: ambari
requirements: [ "requests", "python-ambariclient" ]
'''

EXAMPLES = '''
Create a blueprint:

- hosts: ambari-server
  sudo: yes
  tasks:
  - name: create a cluster
    ambari:
      name: mycluster
      blueprint: /blueprints/multi-node-hdfs-yarn
      hosts_map: /blueprints/multi-node-hdfs-yarn.hosts_map
      server: ambari-server
      port: 8080
      username: admin
      password: admin
      state: present
'''

try:
    import json
    import logging
    from ambariclient.client import Ambari
except ImportError, e:
    print "failed=True msg='failed to import python module: %s'" % e
    sys.exit(1)

logging.basicConfig(level=logging.DEBUG)

class AmbariClusterManager:

    def __init__(self, module):
        self.client = Ambari(module.params.get('server'), \
            port=module.params.get('port'), \
            username=module.params.get('username'), \
            password=module.params.get('password'))

        self.name = self.module.params.get('name')
        self.blueprint = json.load(file(self.module.params.get('blueprint')))
        self.blueprint_name = self.blueprint['Blueprints']['blueprint_name']
        self.hosts_map = json.load(file(self.module.params.get('hosts_map')))

    # client.blueprints('datalyse-hdfs-yarn').delete()

    def ensure_present(self):
        if self.name in [x.cluster_name for x in self.clusters]:
            return False
        else:
            if not self.blueprint_name in [x.blueprint_name for x in self.blueprints]:
                client.blueprints.create(self.blueprint_name,**self.blueprint)

            c = client.clusters.create(self.name, **self.hosts_map)
            c.wait()
            return True

    def ensure_absent(self):
        if self.name in [x.cluster_name for x in self.clusters]:
            client.clusters(self.name).delete()
            return True
        else:
            return False

                
    def create_blueprint(self, name, blueprint_data):
        client.blueprints.create(name,**blueprint_data)

    def get_clusters(self):
        filtered_images = []
        images = self.client.images()
        for i in images:
            # Docker-py version >= 0.3 (Docker API >= 1.8)
            if 'RepoTags' in i:
                repotag = ':'.join([self.name, self.tag])
                if not self.name or repotag in i['RepoTags']:
                    filtered_images.append(i)
            # Docker-py version < 0.3 (Docker API < 1.8)
            elif (not self.name or self.name == i['Repository']) and (not self.tag or self.tag == i['Tag']):
                filtered_images.append(i)
        return filtered_images

    def remove_images(self):
        images = self.get_images()
        for i in images:
            try:
                self.client.remove_image(i['Id'])
                self.changed = True
            except DockerAPIError as e:
                # image can be removed by docker if not used
                pass


def main():
    module = AnsibleModule(
        argument_spec = dict(
            server          = dict(),
            port            = dict(required=False, type='int', default=8080),
            username        = dict(required=False, default='admin'),
            password        = dict(default=False, default='admin'),
            state           = dict(default='present', choices=['absent']),
            name            = dict(),
            blueprint       = dict(),
            hosts_map       = dict(),
            timeout         = dict(default=600, type='int'),
        )
    )

    try:
        manager = AmbariManager(module)
        state = module.params.get('state')
        msg = ''

        clusters = manager.get_clusters()
        if 

        if state == "present":
            clusters = manager.get_clusters()
            if len(images) == 0:
                do_build = True
        # build image
        elif state == "build":
            do_build = True
        # remove image or images
        elif state == "absent":
            manager.remove_images()

        if do_build:
            image_id = manager.build()
            if image_id:
                msg = "Image built: %s" % image_id
            else:
                failed = True
                msg = "Error: %s\nLog:%s" % (manager.error_msg, manager.get_log())

        module.exit_json(failed=failed, changed=manager.has_changed(), msg=msg, image_id=image_id)

    except DockerAPIError as e:
        module.exit_json(failed=True, changed=manager.has_changed(), msg="Docker API error: " + e.explanation)

    except RequestException as e:
        module.exit_json(failed=True, changed=manager.has_changed(), msg=repr(e))
        
# import module snippets
from ansible.module_utils.basic import *

main()
