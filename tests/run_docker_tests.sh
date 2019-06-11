#!/usr/bin/env bash

for d in docker_fedora docker_ubuntu
do
    sudo docker build -v$(pwd)/../:/test -t $d - < $d
    sudo docker run --rm $d
done
