## Prerequisites

```
$ pip install apache-libcloud
```

## Credentials

Credentials can be obtained from the console by going to the “APIs and Auth” section and choosing to create a new client ID for a service account.
Once you’ve created a new client ID and downloaded the generated private key (in the pkcs12 format), you’ll need to convert the key by running the following command:

```
$ openssl pkcs12 -in pkey.pkcs12 -passin pass:notasecret -nodes -nocerts | openssl rsa -out pkey.pem
```

## Create the cloud

- reserver nodes

    ```
    $ ansible-playbook -i localhost, create-gc-cloud.yml
    ```

- create a static inventory file (reduces the time of ansible playlists)
    
    ```
    $ ./inventory/gce.py --list | ./gce2inv.py > inv
    ```

## Provision Ambari

```
$ ansible-playbook -i inv site.yml -e ambari_blueprint=datalyse-hdfs-yarn
```

## Install hadoop cluster

```
$ gcloud compute ssh datalyse-master
$ python
```

```python
> import json
> from ambariclient.client import Ambari
> client = Ambari('datalyse-master',8080,'admin','admin') # the docker port is exposed on datalyse-master
> client.blueprints.create('datalyse-hdfs-yarn',**json.load(file('/tmp/blueprints/datalyse-hdfs-yarn')))
> cluster = client.clusters.create('datalyse',**json.load(file('/tmp/blueprints/datalyse-hdfs-yarn.hosts_map')))
> cluster.wait()
```

##Resources

- [python-ambariclient](https://github.com/jimbobhickville/python-ambariclient)
- [Ambari Blueprints ](https://cwiki.apache.org/confluence/display/AMBARI/Blueprints)
- [Ambari REST API](https://github.com/apache/ambari/blob/trunk/ambari-server/docs/api/v1)
- [HDFS parameters](https://hadoop.apache.org/docs/r2.3.0/hadoop-project-dist/hadoop-hdfs/hdfs-default.xml)