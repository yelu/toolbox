# docker cheatsheet

## images

```bash
# build image    
sudo docker build -t queryindex_s2s:1rc0 .
# saves a non-running container image to a tar file
docker save -o queryindex_s2s.tar queryindex_s2s:1rc1
# load a docker image from file
docker load -i exported.tar
# find docker containers by image name
docker container ls -a --filter ancestor="centos:7" -q
```

## containers

```bash
# list all containers
docker ps -a
# run an image in a container
docker run queryindex_s2s:1rc3 /model/run.sh http
# run an image in interactive mode
docker run -it --entrypoint=/bin/bash queryindex_s2s:1rc1
# stop a running container
docker stop 1fa4ab2cf395
# delete a container
docker rm -f 1fa4ab2cf395
# track stdout/stderr from a running container
docker logs -f 1fa4ab2cf395
# saves a runnning or paused container instance to a tar file
docker pull ubuntu
docker run -t -i -d ubuntu /bin/bash
docker export bd227533eeb5 > docker_exported.tar
```

## docker deamon

```bash
# start docker daemon service
sudo systemctl start docker
# no sudo
sudo groupadd docker
sudo usermod -aG docker $USER
# log out and log back in
```

## working with remote registry	
Login to a docker registry	docker login cgcregistry.azurecr.io -u cgcregistry -p [password]
Push docker image into a registry	"docker tag mysql_client:latest cgcregistry.azurecr.io/cgc/mysql_client
docker push cgcregistry.azurecr.io/cgc/mysql_client:latest"
