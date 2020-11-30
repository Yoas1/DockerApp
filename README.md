
# Docker GUI app

## Use with ubuntu 20.04

### Install Docker:

**1**-Update Local Database:
>$ sudo apt-get update

**2**-Download Dependencies:
>$ sudo apt-get install apt-transport-https ca-certificates curl gnupg-agent software-properties-common

**3**-Add Docker’s GPG Key:
>$curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

**4**-Install the Docker Repository:
>$ sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs)\ stable"

**5**-Update Repositories
>$ sudo apt-get update

**6**-Install Latest Version of Docker:
>$ sudo apt-get install docker-ce docker-ce-cli containerd.io

**7**-Check the Docker version:
>$ docker version

**8**-Create the docker group:
>$ sudo groupadd docker

**9**-Add your user to the docker group:
>$ sudo usermod -aG docker ${USER}

**10**-Logout and log back from your user.

**11**-Check if you can run docker commands without sudo:
>$ docker run hello-world


### Install Python3

**1**-Install Python3, Python3-pip and Python3-tk:
>$ sudo apt-get install python3 python3-pip python3-tk

**2-After pip3 install you must install Docker SDK for python:**
>**$ pip3 install docker** 

### Install Pycharm

**1**-Download Pycharme software from here:
>https://www.jetbrains.com/pycharm/download/download-thanks.html?platform=linux&code=PCC

**2**-Extract the file you download.

**3**-Go to the **bin** folder, right click and choose "open in Terminal".

**4**-run command: **./pycharm.sh**

**5**-After install Pycharm software, go to settings:
> Configure -> Settings

**6**-Adding Python interpreter:
>Project Interpreter -> click on gear on right side -> Add -> System Interpreter -> choose python3

**7**-Create new Project.

**8**-install docker SDK in python project interpreter:
>File -> Settins -> Python Interpreter -> click on plus sign in right side -> search "docker" -> **Install Package**

**9**-Load **DockerAPP.py** file to the project.

**10**-now you can run it.


### DOCKER APP

**1**-For run container insert in "Image for container" the image name like:

>nginx:latest / ubuntu / or you repository :<user>/<name_repo>

**2**-You can choose name for container in "Name for container".

**3**-In port insert ports like:

>8000:8000

**4**-In "Command" insert commands like:

>echo hello world"

**5**-Click on "Update list" button to update container table.

**6**-For Start/Stop/Remove insert the name of container in "Name for container" and click button.

**7**-For pull image insert the image <name>:<tag> in "image for container" and click button "pull"

**8**-For push image to your Docker Hub you must login!

**9**-For push after login insert in "Image for container" the name for you repository **<user>/<name_repo>**

in "Name for container" insert the container name you want push from container table

in "tag" insert the tag for repository.

and click "push".




### ENJOY!!
 
