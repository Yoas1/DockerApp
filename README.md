# DockerApp
Docker GUI app

USE with ububntu 20.04

first install docker:
1-Update Local Database:
$ sudo apt-get update
2-Download Dependencies:
$ sudo apt-get install apt-transport-https ca-certificates curl gnupg-agent software-properties-common
3-Add Docker’s GPG Key:
$curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
4-Install the Docker Repository:
$ sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs)\ stable"
5-Update Repositories
$ sudo apt-get update
6-Install Latest Version of Docker:
$ sudo apt-get install docker-ce docker-ce-cli containerd.io
7-Check the Docker version:
$ docker version
8-Create the docker group:
$ sudo groupadd docker
9-Add your user to the docker group:
$ sudo usermod -aG docker ${USER}
10-Logout and log back from your user.
11-Check if you can run docker commands without sudo:
$ docker run hello-world
