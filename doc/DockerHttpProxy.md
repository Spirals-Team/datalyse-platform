# Configuring HTTP proxy for docker `boot2docker` VM

Docker containers by default have a direct access to Internet.
When playing with docker images one usually has to pull some packages or other software resources which might be time consuming (despite the fact that docker support [cache](http://crosbymichael.com/dockerfile-best-practices.html)) in particular on slower networks.
This guide overviews how to configure a simple HTTP caching proxy solution for docker, concretely for docker deployment using the `boot2docker` VM.

1. Install a caching proxy server on the host machine.

  A simple, yet useful one is [polipo](http://www.pps.univ-paris-diderot.fr/~jch/software/polipo/).
  On OSX, it can be installed using [homebrew](http://brew.sh/):
  ```sh
  $ brew install polipo
  ```
  It does not require any configuration and can be easily launched as a foreground process as well as a background daemon using launchctl (cf. instructions at the end of brewing).
  For simplicity we run it as a foreground processes when it is needed simply by
  ```sh
  $ polipo
  Established listening socket on port 8123.
  ```
  By default it listens on the port 8123 and it stores the cache in `/usr/local/var/cache/polipo/` (when installed by homebrew).
  It also provides a simple management UI accessible on `http://localhost:8123/polipo`.

2. Configure the `boot2docker` host

  The `boot2docker` runs the docker daemon and is the default gateway for all docker containers.
  It has to provide http proxy for both the docker daemon and for the containers.

  1. Setting an HTTP proxy for the docker daemon.

    Like other processes, docker respects the `http_proxy` and `https_proxy` environment variable.
    However, they have to be set before docker daemon is run.
    Therefore, we first need to stop docker if it is running:

    ```sh
    docker@boot2docker:~$ sudo /etc/init.d/docker stop
    ```

    Next, before we can set them, we need to figure out what IP is used to connect to the host machine that runs the `boot2docker` virtual machine.
    This can be figured out from the routing table:

    ```sh
    docker@boot2docker:~$ netstat -rn
    Kernel IP routing table
    Destination     Gateway         Genmask         Flags   MSS Window  irtt Iface
    0.0.0.0         10.0.2.2        0.0.0.0         UG        0 0          0 eth0
    10.0.2.0        0.0.0.0         255.255.255.0   U         0 0          0 eth0
    127.0.0.1       0.0.0.0         255.255.255.255 UH        0 0          0 lo
    172.17.0.0      0.0.0.0         255.255.0.0     U         0 0          0 docker0
    ```

    The row with `0.0.0.0` destination indicates the default gateway which is in this case routed to `10.0.2.2` which is the IP of the host running the `boot2docker` VM.
    Now, we can set the environment variables:

    ```sh
    docker@boot2docker:~$ export http_proxy='http://10.0.2.2:8123/'
    docker@boot2docker:~$ export https_proxy='http://10.0.2.2:8123/'
    ```

    and start docker

    ```sh
    docker@boot2docker:~$ sudo /etc/init.d/docker start
    ```

  1. Setting port forwarding

    The docker containers do not have a direct access to the host running the `boot2docker` VM.
    However, they can access the container host, `boot2docker` VM which can forward all the requests to its host.
    We therefore configure a [port forwarding](http://www.ridinglinux.org/2008/05/21/simple-port-forwarding-with-iptables-in-linux/) for all traffic coming to port `boot2docker:8123` to be redirected to the host running docker.

    ```sh
    # To allow forwarding rule specifically to machine 10.0.2.2 and port 8123 in the FORWARD chain
    docker@boot2docker:~$ sudo iptables -I FORWARD -p tcp -d 10.0.2.2 --dport 8123 -j ACCEPT
    # To masquerade the routed connection so that the firewall will treat it as local connection.
    docker@boot2docker:~$ sudo iptables -t nat -A POSTROUTING -o docker0 -j MASQUERADE
    # The actual port forwarding rule
    docker@boot2docker:~$ sudo iptables -t nat -A PREROUTING -i docker0 -p tcp --dport 8123 -j DNAT --to-destination 10.0.2.2:8123
    ```

1. Configure docker containers

  Configuring docker containers consists simply in setting the `http_proxy` variables.
  The IP is again found using the netstat:

  ```sh
  bash-4.1# netstat -nr
  Kernel IP routing table
  Destination     Gateway         Genmask         Flags   MSS Window  irtt Iface
  0.0.0.0         172.17.42.1     0.0.0.0         UG        0 0          0 eth0
  172.17.0.0      0.0.0.0         255.255.0.0     U         0 0          0 eth0
  ```

  The actual proxy setting:

  ```sh
  docker@boot2docker:~$ export http_proxy='http://172.17.42.1:8123/'
  docker@boot2docker:~$ export https_proxy='http://172.17.42.1:8123/'
  ```

  It will likely be always `172.17.42.1` and so can also be set directly in the Dockerfile:

  ```
  # local cache
  ENV http_proxy http://172.17.42.1:8123/
  ENV https_proxy https://172.17.42.1:8123/
  ```

  This will however make it non-portable since it will always require a proxy.
  It is only good for testing.

## Persisting VM Proxy Configuration

The above `boot2docker` configuration will not be persisted over reboots.
In order to persist the customization, the above commands should be included in the `boot2docker` VM customization files (cf. boot2docker official [FAQ](https://github.com/boot2docker/boot2docker/blob/master/doc/FAQ.md)).

1. Create `/var/lib/boot2docker/bootlocal.sh `

  ```sh
  docker@boot2docker:~$ sudo cat << EOF > /var/lib/boot2docker/bootlocal.sh
  #!/bin/sh

  iptables -I FORWARD -p tcp -d 10.0.2.2 --dport 8123 -j ACCEPT                           
  iptables -t nat -A POSTROUTING -o docker0 -j MASQUERADE                           
  iptables -t nat -A PREROUTING -i docker0 -p tcp --dport 8123 -j DNAT --to-destination 10.0.2.2:8123 
  EOF

  docker@boot2docker:~$ sudo chmod +x /var/lib/boot2docker/bootlocal.sh 
  ```

2. Create `/var/lib/boot2docker/profile`

  ```sh
  sudo cat << EOF > /var/lib/boot2docker/profile
  http_proxy='http://10.0.2.2:8123/'
  https_proxy='http://10.0.2.2:8123/'
  EOF
  ```