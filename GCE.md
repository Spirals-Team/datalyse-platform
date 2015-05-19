```sh
$ gcloud auth login
```

```sh
$ gcloud config set project datalyse-exp
```

```sh
$ gcloud compute zones list
NAME           REGION       STATUS          NEXT_MAINTENANCE TURNDOWN_DATE
asia-east1-a   asia-east1   UP
asia-east1-b   asia-east1   UP
asia-east1-c   asia-east1   UP
europe-west1-b europe-west1 UP
europe-west1-d europe-west1 UP
europe-west1-c europe-west1 UP
europe-west1-a europe-west1 UP (DEPRECATED)                  2015-03-29T00:00:00.000-07:00
us-central1-f  us-central1  UP
us-central1-b  us-central1  UP
us-central1-a  us-central1  UP
```

```sh
$ gcloud config set compute/zone europe-west1-b
```

```sh
$ gcloud compute regions  list
NAME         CPUS          DISKS_GB     ADDRESSES RESERVED_ADDRESSES STATUS TURNDOWN_DATE
asia-east1      0.00/24.00      0/10240      0/23      0/7           UP
europe-west1    0.00/24.00      0/10240      0/23      0/7           UP
us-central1     0.00/24.00      0/10240      0/23      0/7           UP
```

```sh
$ gcloud config set compute/region europe-west1
```

```sh
$ gcloud config list
```

```sh
docker-machine -D create -d google --google-project datalyse-exp --google-machine-type n1-standard-1 --google-zone europe-west1-b gc-datalyse-1
```

```sh
gcloud compute firewall-rules create docker-http --allow tcp:2374 --target-tags docker-machine
```