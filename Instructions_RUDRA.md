# Instructions for RUDRA

## 0. Environment

- OS: ubuntu 20.04 LTS
- Docker installed

## 1. Download RUDRA repository and docker image
```
$ git clone https://github.com/sslab-gatech/Rudra.git
$ docker pull ghcr.io/sslab-gatech/rudra:master && docker tag ghcr.io/sslab-gatech/rudra:master rudra:latest
$ cd Rudra
$ ./setup_rudra_runner_home.py ~/rudra-home
$ export RUDRA_RUNNER_HOME=$HOME/rudra-home
```
After the instructions, the directory `rudra-home` is created in your `HOME` directory.

### 1-1. Permission denied docker

Permission denied message :
```
docker: Got permission denied while trying to connect to the Docker daemon socket at unix:
...
```
Solution :
```
$ sudo groupadd docker // create docker group
$ sudo usermod -aG docker $USER // add the user in docker group
$ newgrp docker // resetting
```

## 2. Run RUDRA for a Rust crate
```
$ docker-helper/docker-cargo-rudra /path/to/crate
```
