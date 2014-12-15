






## TODO

- docker
- cinder
- fix supervisor
- network
- creating external IP
- simplify passwords? - only one: master password

## Prerequisite

1. install maestro

  The following will install maestro-ng 0.2.3. The latest development version seems to be buggy.

  ```sh
  pip install --upgrade git+git://github.com/signalfuse/maestro-ng@f1ee6c277a2a3c48f9a400cc4b511498cbca5d23
  ```

  TODO: we should move out from maestro!

## Single node demo

### On boot2docker

1. Start boot2docker

  ```sh
  boot2docker up
  ```

1. Make sure the `ebtables` is loaded

  ```sh
  boot2docker ssh lsmod | grep ebtables
  ebtables               24576  2 ebtable_filter,ebtable_nat
  ```

  If it is not, load it.

  ```sh
  boot2docker ssh sudo modprobe ebtables
  ```

  Note: to do this permanently, add the following to the `/var/lib/boot2docker/bootlocal.sh`:

  ```sh
  #!/bin/sh

  modprobe ebtables
  ```

1. Start `docker-http` proxy that allow maestor to connect to docker using HTTP instead of HTTPS

  ```sh
  docker start docker-http || docker run -d -p 2375:2375 --volume=/var/run/docker.sock:/var/run/docker.sock --name=docker-http sequenceiq/socat
  ```

1. Make sure the IP address is correct

  ```sh
  boot2docker ip
  ```

  should return the same address as the one which is in the `boot2docker/inventory` and `maestro.yaml`.

### On Vagrant

1. Start the Vagrant VM

  ```sh
  vagrant up
  ```

1. Initialize the inventory file

  ```sh
  ./vagrant/shellinit.sh
  ```

1. Install docker

  We use a base ubuntu image which does not have docker installed and therefore it has to be installed manually.
  While we could use vagrant provisioning, we do not opt for this as it allows us to test the docker provisioning using the ansible script `install-docker.yml`.

  ```sh
  ansible-playbook -i vagrant/inventory ../../playbooks/install-docker.yml
  ```

1. start maestro

1. configure client

    ```sh
    ssh-copy-id -p 2222 -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@<ip_of_the_client_docker>
    ```

1. do a basic configuration

    ```sh
    ansible-playbook -i environments/boot2docker/inventory  basic-configuration.yml
    ```

1. create a network for floating addresses - bash through docker exec (compute / controller?)

  ```sh
  docker exec -ti nova-compute-kvm-1 nova-manage floating create --ip_range=172.16.1.0/24  --pool demo
  ```

1. import docker images - bash through docker exec (compute-docker)

  ```sh
  ansible-playbook -i environments/boot2docker/inventory  import-docker-images.yml
  ```

4. provision VMs

    - test if docker works

        ```sh
        nova boot --flavor m1.tiny --image rastasheep/ubuntu-sshd test
        ```

    - test if KVM works

        ```sh
        nova get-vnc-console i1 novnc
        ```

5. provision Ansible cluster
6. run SWIM
