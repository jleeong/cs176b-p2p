# P2P implementation for CS176B
## Setting up P2P node.
1. Clone this project into the target computer
2. Navigate to the project root
3. Create a `files/` subdirectory in the project root (this is where files local to the current node will reside)
3. run `python3 runnode.py`

## Using `ansible` to bootstrap VMs
This requires you to have ansible installed on your system.
1. Create the desired amount of VMs. (These must all have the same system user and password and `openssh-server` installed)

_Ensure that the system user has passwordless sudo enabled._

2. Connect VMs to the same virtual host only network and configure network settings
3. Navigate to the `ansible` subdirectory

`cd ansible`

4. Add all the VMs IPs to the `inventory` file
5. Copy your SSH private key to the `roles/p2p_node/templates` directory

This can be done typically by `cp ~/.ssh/id_rsa ./roles/p2p_node/templates/`

6. Run `ansible-playbook -b -u <VM_SYSTEM_USERNAME> -k -i inventory deploy-p2p-node.yml`

_replace <VM_SYSTEM_USERNAME> with the username you created the VMs with_

## Using `docker` to set up virtual network
This requires you to have Docker installed on your system.
### To create the network
1. Create the appropriate number of nodes in the `test_data/nodes.json` file

_These can be named whatever you want. If one of them has the word "ingress" in the name, docker will port map the container to you machine, enabling you to hit the container at 127.0.0.1:8080_

2. `python3 genhostfiles.py`
3. `python3 deploydocker.py`
4. `python3 distributefiles.py <FILE_DISTRIBUTION_PERCENTAGE> [-v]`

_replace <FILE_DISTRIBUTION_PERCENTAGE> with the probability for a file to exist on a container. (e.g. 5 gives a 5% chance for a file to be on a container). Add the -v flag if you want verbosity for the file distribution_
### To stop the network
1. `docker stop $(docker ps -qf 'name=<SOME_COMMON_STRING>')`

_replace <SOME_COMMON_STRING> with a substring that appears in every node name listed in `test_data/nodes.json`_
### IMPORTANT if you make changes to the python source code (i.e. anything in the `node/` directory), stop the virtual network and run this command
`docker rmi cs176b-p2p`

If you do not do this, you will not see your changes in the existing or future docker containers
