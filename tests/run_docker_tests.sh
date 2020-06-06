#!/usr/bin/env bash

container_cmd=""
sudo=""

if which docker &> /dev/null
then
	container_cmd=docker

	if ! groups | grep docker
	then
		sudo="sudo"
	fi
elif which podman &> /dev/null
then
	container_cmd=podman
else
	echo "this script need either docker or podman to be installed... aborting"
	exit 1
fi

for d in docker_fedora docker_ubuntu
do
    $sudo $container_cmd build -v$(pwd)/../:/test:Z -t $d - < $d
    $sudo $container_cmd run --rm $d
done
