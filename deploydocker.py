"""python script to deploy docker containers"""
import os
import json
import subprocess

with open('test_data/nodes.json','r') as nodes:
    raw = ''.join(nodes.readlines())
    containers = json.loads(raw)

docker_image = 'cs176b-p2p'
docker_nw = 'p2p_nw'
if subprocess.check_output(['docker','images','-q',docker_image]).decode('utf-8') == '':
    subprocess.run(['docker','build','-t',docker_image,'.'])
existing_nw = subprocess.check_output(['docker','network','ls']).decode('utf-8')
if  docker_nw not in existing_nw:
    subprocess.run(['docker','network','create',docker_nw])

for c in containers:
    subprocess.run(['docker','run','--name',c,'-d','--network',docker_nw,\
        '-v'+os.getcwd()+'/test_data/networking'+c+'hosts:/var/cs176/p2p/hosts',\
        docker_image])
