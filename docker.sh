#!/bin/bash
docker_image=cs176b-p2p
docker_network=p2p_nw
if [ "$(docker images -q $docker_image)" ==  "" ]
then
    docker build -t $docker_image .
fi

if [ "$(docker network ls | grep $docker_network)" == "" ]
then
    echo Missing docker network
    exit 1
fi

count=10
for i in `seq 1 $count`;
do
    echo "docker run --name node-$i -d --network $docker_network $docker_image"
    docker run --name node-$i -d --network $docker_network $docker_image
done
