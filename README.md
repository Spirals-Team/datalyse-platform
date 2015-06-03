# Datalyse Eolas

This branch contains code for running the Datalyse platform on the top of Eolas cluster.

## Overview

## Provisioning

In order to set up the cluster, the following tools are needed:

- git
- ansible
- docker
- docker-machine (_optional_)

### Reserving the nodes

First, it is needed to get the nodes that will be part of the cluster.
This can be done either using the provided ansible scripts or directly, using docker-machine.
The latter option has yet to be tested as by the time of writing the Eolas cluster did not provided a direct OpenStack API access and thus the nide reservations had to be done manually.
For the purpose of this tutorial, we use the three `dlyse.large` machines called respectively:

- `datalyse-master`
- `datalyse-1`
- `datalyse-2`

All run Ubuntu 14.04 LTS image.

### Create a docker-swarm token for node discovery

```sh
$ docker-swarm create
feba5683f4a1645b68365f562f81694f
```

### Bootstrap the cluster with docker-machine

_TBW_

### Bootstrap the cluster with Ansible

1. Edit the configuration files
1. Start

    1. Bootstrap

        ```sh
        $ ansible-playbook -i inventory bootstrap.yml
        ``` 
        
        This will install docker, weave and prepare the host to join the cluster.

    1. Create cluster
    
        ```sh
        $ ansible-playbook -i inventory setup-cluster.yml
        ``` 
        
        This will setup the weave network and create the swarm.

    Together the operations can be launched using:

    ```sh
    $ ansible-playbook -i inventory site.yml
    ``` 


1. Try

    ```
    $ docker -H tcp://datalyse-master:3376 info
    Containers: 13
    Strategy: spread
    Filters: affinity, health, constraint, port, dependency
    Nodes: 3
     datalyse-1: 10.67.24.194:12375
      └ Containers: 4
      └ Reserved CPUs: 0 / 4
      └ Reserved Memory: 0 B / 8.188 GiB
     datalyse-2: 10.67.24.195:12375
      └ Containers: 4
      └ Reserved CPUs: 0 / 4
      └ Reserved Memory: 0 B / 8.188 GiB
     datalyse-master: 10.67.24.190:12375
      └ Containers: 5
      └ Reserved CPUs: 0 / 4
      └ Reserved Memory: 0 B / 8.188 GiB
    ```
    
    Check the cluster status
    
    ```
    $ docker-swarm list token://23d833b51ae3a37bf7269e0cf1779520
    datalyse-master:12375
    datalyse-2:12375
    datalyse-1:12375
    ```
    
    Check containers
    
    ```
    $ docker -H tcp://datalyse-master:3376 ps
    CONTAINER ID        IMAGE                         COMMAND                CREATED             STATUS              PORTS                                                      NAMES
    618f12d84869        weaveworks/weaveexec:0.11.1   "/home/weave/weavepr   6 minutes ago       Up 6 minutes                                                                   datalyse-master/weaveproxy   
    1aa2321369a9        weaveworks/weaveexec:0.11.1   "/home/weave/weavepr   6 minutes ago       Up 6 minutes                                                                   datalyse-1/weaveproxy        
    484ca3016c3e        weaveworks/weaveexec:0.11.1   "/home/weave/weavepr   6 minutes ago       Up 6 minutes                                                                   datalyse-2/weaveproxy        
    e82ec4ad5bd6        weaveworks/weavedns:0.11.1    "/home/weave/weavedn   6 minutes ago       Up 6 minutes        172.17.42.1:53->53/udp                                     datalyse-1/weavedns          
    390cdc280669        weaveworks/weavedns:0.11.1    "/home/weave/weavedn   6 minutes ago       Up 6 minutes        172.17.42.1:53->53/udp                                     datalyse-master/weavedns     
    dbc8ad512717        weaveworks/weavedns:0.11.1    "/home/weave/weavedn   6 minutes ago       Up 6 minutes        172.17.42.1:53->53/udp                                     datalyse-2/weavedns          
    a192866ee1f6        weaveworks/weave:0.11.1       "/home/weave/weaver    6 minutes ago       Up 6 minutes        10.67.24.190:6783->6783/tcp, 10.67.24.190:6783->6783/udp   datalyse-master/weave        
    038f2a0c09ad        weaveworks/weave:0.11.1       "/home/weave/weaver    6 minutes ago       Up 6 minutes        10.67.24.194:6783->6783/tcp, 10.67.24.194:6783->6783/udp   datalyse-1/weave             
    3ea31a1cd521        weaveworks/weave:0.11.1       "/home/weave/weaver    6 minutes ago       Up 6 minutes        10.67.24.195:6783->6783/udp, 10.67.24.195:6783->6783/tcp   datalyse-2/weave            
    ```

### (_optional_) Test the weave networking

In this section we will test the weave networking.
Concretely we will look at two things:

- Automatic IP address assignment
- DNS resolution

First check the weave status:

```
$ ssh datalyse-master weave status
weave router 0.11.1
Encryption off
Our name is 7e:ba:e9:71:fb:a9(datalyse-2)
Sniffing traffic on &{9 65535 ethwe 92:ba:71:55:c5:4c up|broadcast|multicast}
MACs:
92:ba:71:55:c5:4c -> 7e:ba:e9:71:fb:a9(datalyse-2) (2015-06-03 13:33:09.763506408 +0000 UTC)
7e:ba:e9:71:fb:a9 -> 7e:ba:e9:71:fb:a9(datalyse-2) (2015-06-03 13:33:09.949557528 +0000 UTC)
42:ef:1d:93:0c:7c -> 7e:ba:e9:71:fb:a9(datalyse-2) (2015-06-03 13:33:10.477415802 +0000 UTC)
fa:9d:62:d1:6a:cf -> 7e:ba:e9:71:fb:a9(datalyse-2) (2015-06-03 13:33:22.057473044 +0000 UTC)
Peers:
7e:ba:e9:71:fb:a9(datalyse-2) (v6) (UID 5112344731971000702)
   -> 5e:a1:5d:09:65:12(datalyse-1) [10.67.24.194:57007]
   -> be:b7:52:cd:73:3f(datalyse-master) [10.67.24.190:6783]
be:b7:52:cd:73:3f(datalyse-master) (v4) (UID 1076997732339896607)
   -> 7e:ba:e9:71:fb:a9(datalyse-2) [10.67.24.195:39475]
   -> 5e:a1:5d:09:65:12(datalyse-1) [10.67.24.194:60241]
5e:a1:5d:09:65:12(datalyse-1) (v6) (UID 4160590684391850174)
   -> 7e:ba:e9:71:fb:a9(datalyse-2) [10.67.24.195:6783]
   -> be:b7:52:cd:73:3f(datalyse-master) [10.67.24.190:6783]
Routes:
unicast:
5e:a1:5d:09:65:12 -> 5e:a1:5d:09:65:12
7e:ba:e9:71:fb:a9 -> 00:00:00:00:00:00
be:b7:52:cd:73:3f -> be:b7:52:cd:73:3f
broadcast:
7e:ba:e9:71:fb:a9 -> [be:b7:52:cd:73:3f 5e:a1:5d:09:65:12]
be:b7:52:cd:73:3f -> []
5e:a1:5d:09:65:12 -> []
Reconnects:

Allocator subnet 10.1.1.0/24

weave DNS 0.11.1
Local domain weave.local.
Listen address :53
mDNS interface &{13 65535 ethwe fa:9d:62:d1:6a:cf up|broadcast|multicast}
Fallback DNS config &{[10.64.1.1 10.64.1.2] [openstacklocal] 53 1 5 2}
Zone database:
```

Next, we try the inter container communication:

1. Configure the swarm master

    ```
    $ export DOCKER_HOST="tcp://178.237.109.178:3376"
    ```

1. Launch a container

    ```
    $ docker run -ti --rm -h b.weave.local centos:centos6 ifconfig
    eth0      Link encap:Ethernet  HWaddr 02:42:AC:11:00:04  
              inet addr:172.17.0.4  Bcast:0.0.0.0  Mask:255.255.0.0
              inet6 addr: fe80::42:acff:fe11:4/64 Scope:Link
              UP BROADCAST RUNNING  MTU:1454  Metric:1
              RX packets:4 errors:0 dropped:0 overruns:0 frame:0
              TX packets:3 errors:0 dropped:0 overruns:0 carrier:0
              collisions:0 txqueuelen:0 
              RX bytes:332 (332.0 b)  TX bytes:258 (258.0 b)
    
    ethwe     Link encap:Ethernet  HWaddr 62:80:E5:B5:E2:2E  
              inet addr:10.1.1.1  Bcast:0.0.0.0  Mask:255.255.255.0
              inet6 addr: fe80::6080:e5ff:feb5:e22e/64 Scope:Link
              UP BROADCAST RUNNING MULTICAST  MTU:65535  Metric:1
              RX packets:3 errors:0 dropped:0 overruns:0 frame:0
              TX packets:4 errors:0 dropped:0 overruns:0 carrier:0
              collisions:0 txqueuelen:1000 
              RX bytes:258 (258.0 b)  TX bytes:300 (300.0 b)
    
    lo        Link encap:Local Loopback  
              inet addr:127.0.0.1  Mask:255.0.0.0
              inet6 addr: ::1/128 Scope:Host
              UP LOOPBACK RUNNING  MTU:65536  Metric:1
              RX packets:0 errors:0 dropped:0 overruns:0 frame:0
              TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
              collisions:0 txqueuelen:0 
              RX bytes:0 (0.0 b)  TX bytes:0 (0.0 b)
    ```
    
    The `ethwe` is the weave network interface.

1. Ping containers using hostnames. Here we start two containers (`test-a` and `test-b`) with hostname `a` and `b` respectively and then we try to pick one from the other. _Note:_ the `.weave.local` is important since otherwise it won't be picked by the weave DNS.
  
  ```
    $ docker run -dti --name test-a -h a.weave.local centos:centos6 bash
    f341653f5583197b4dd3eb702c550b46abe010f2e36abc608ef66093583d1ebe
    
    $ docker run -dti --name test-b -h b.weave.local centos:centos6 bash
    c9208734ff929e3fc7990debb1b900536290d574f3c78a57f220e069432c6df7
    
    $ docker ps | grep test
    c9208734ff92        centos:centos6                "/home/weavewait/wea   15 seconds ago      Up 5 seconds                                                                   datalyse-2/test-b            
    f341653f5583        centos:centos6                "/home/weavewait/wea   28 seconds ago      Up 18 seconds                                                                  datalyse-1/test-a            
    
    $ docker attach test-a
    
    [root@a /]# ifconfig ethwe
    ethwe     Link encap:Ethernet  HWaddr 72:38:4A:67:A0:23  
              inet addr:10.1.1.191  Bcast:0.0.0.0  Mask:255.255.255.0
              inet6 addr: fe80::7038:4aff:fe67:a023/64 Scope:Link
              UP BROADCAST RUNNING MULTICAST  MTU:65535  Metric:1
              RX packets:17 errors:0 dropped:0 overruns:0 frame:0
              TX packets:9 errors:0 dropped:0 overruns:0 carrier:0
              collisions:0 txqueuelen:1000 
              RX bytes:1338 (1.3 KiB)  TX bytes:690 (690.0 b)

    [root@a /]# ping b
    PING b.weave.local (10.1.1.1) 56(84) bytes of data.
    64 bytes from b.weave.local (10.1.1.1): icmp_seq=1 ttl=64 time=1.98 ms
    64 bytes from b.weave.local (10.1.1.1): icmp_seq=2 ttl=64 time=1.24 ms
    64 bytes from b.weave.local (10.1.1.1): icmp_seq=3 ttl=64 time=1.85 ms
    64 bytes from b.weave.local (10.1.1.1): icmp_seq=4 ttl=64 time=1.06 ms
    ^C
    --- b.weave.local ping statistics ---
    4 packets transmitted, 4 received, 0% packet loss, time 3713ms
    rtt min/avg/max/mdev = 1.061/1.539/1.989/0.392 ms
    [root@a /]# exit  
  ```

## Operations

Here is a set of useful commands for working with the cluster

- Restart docker

  ```sh
  ansible all -s -i inventory -m service -a "name=docker state=restarted"
  ```

- Command to all nodes

  ```sh
  ansible all -i inventory -a "docker ps"
  ```

- Remove all containers

  ```sh
  $ ansible all -s -i inventory -m shell -a "docker ps -qa | xargs docker rm -f"
  ```

- Remove all images

  ```sh
  $ ansible all -s -i inventory -m shell -a "docker images -q | xargs docker rmi -f"
  ```

  
## Operations in VPN

The `vpn-user` and `vpn-host` denotes respectively a username and a machine within the VPN which has a direct access to the Eolas cluster.

- Setting up a SOCKS proxy

    ```sh
    $ ssh -vND 8888 vpn-user@vpn-host
    ```

- Connecting to the nodes

    Having the follwing `~/.ssh/config`: 
      
    ```
    Host *.eolas
       User vpn-user
       ProxyCommand ssh vpn-host "nc -w 60 `basename %h .eolas` %p"
    ```  

    permits:
    
    ```sh
    $ ssh <IP of datalyse node>.eolas
    ```
