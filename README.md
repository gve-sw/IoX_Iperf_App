# CISCO IoX Iperf App
[Iperf](https://iperf.fr/) is a network monitoring tool, in this prototype we embded this tool in a docker container to be shiped into IoX devices, this will enable insights on the network for customers acorss difrent IoT networks.


In this prototype we built a python flask app with the Iperf tool to monitor network link from the IoX device to a centrla Iperf server.
![alt text][Prototype]

[Prototype]:./prototype.png "Prototype workflow"

## Install:

#### Install Docker :
Follow instructions [here](https://runnable.com/docker/getting-started/)
```
$ sudo apt-get install docker-engine -y
```

#### Clone the repo :
```
$ git clone https://github.com/gve-sw/IoX_Iperf_App.git
```

#### Install dependencies :
```
$ pip3 install requirements.txt
```

## Setup:
#### DevNet IoX sandbox :
You can deploy this prototype using IoX DevNet sanbox [IoX Lab](https://devnetsandbox.cisco.com/RM/Diagram/Index/856d2943-eded-4f45-a76b-e50ee3dc9c02?diagramType=Topology), reserve your lab and follow instructions on email to access the sandbox
The rest of this documenttation will assume using the DevNet Sandbox, you can use your own hardware you can find more details on how to setup your lab [here](https://developer.cisco.com/docs/iox/)

#### IoX Client tool :
You need the ioxclient to package and deploy the IOx Application. To install ioxclient, you can find it at this [link](https://developer.cisco.com/docs/iox/#!iox-resource-downloads/downloads).
To get started, connect to your IoX host
```
$ ioxclient profiles reset
```
This command resets any previously set profiles and allows you to start fresh with the ioxclient profile wizard.
With no profiles by default, the first time you run ioxclient it will create a configuration file in your home directory and you will be asked questions about the connection Profile you want to establish.
If you are using the DevNet sandbox, use the following ip address 10.10.20.51 or 10.10.20.52 and credentials username: cisco, password: cisco instead of root and select 22 for the ssh default port instead of 2222. All other values should be fine at their defaults.
```
$ ioxclient platform info
```
If you receive JSON platform information your connection is succeful. 

#### Iperf server tool :
You need the have the Iperf tool locally to test conecticity incase if your lab dosent have access to internet, the default Iperf server for testing is 'bouygues.iperf.fr', To install Iperf tool, you can find it at this [link](https://iperf.fr/iperf-download.php).
If you need to test locally you can start a server locally 
```
$ iperf -s
-----------------------------------------------------------
Server listening on 5201
-----------------------------------------------------------

```


## Usage:
#### Deploy app to IoX :
- Build image :
Build the package from the downloded files  
```
$ docker build -t gve_devnet/ioxiperf_app .
```

Make sure your image has been built
```
$ docker images
REPOSITORY                 TAG                 IMAGE ID            CREATED             SIZE
gve_devnet/iox_iperf_pov   latest              8c091382f51e        3 hours ago         71MB
alpine                     3.7                 6d1ef012b567        9 months ago        4.21MB
```
- Package for IoX:
Creat a package.tar file 
```
$ ioxclient docker package gve_devnet/iox_iperf_pov:latest .
```
Deploy the app to IoX
```
$ ioxclient application install iox_iperf_pov package.tar
Currently active profile :  default
Command Name: application-install
Saving current configuration
Installation Successful. App is available at : https://10.10.20.51:8443/iox/api/v2/hosting/apps/myapp_iox
Successfully deployed
```
Verify the Application state
```
$ ioxclient application list
Currently using profile :  TEST
Command Name: application-list
List of installed apps :
 1\. iox_iperf_pov --->  DEPLOYED
```
- Activate and run:server
To activate the IOx application, run the following command
```
$ ioxclient application activate --payload activation.json iox_iperf_pov
```
To start your application run the start command
```
$ ioxclient application start
```

#### Run :
- Check server is runing
To check if the application is runing on the IoX device access the server address [http://10.10.20.51:5500/](http://10.10.20.51:5500/)
![alt text][Serevr]

[Serevr]:./server.png "Server web"
- Use [postman](https://www.getpostman.com/) to test:
You can import the postman collection and envirenement files to start testing using postman:
Configure the IoX app to use your local Iperf server using the API endpoint POST /config, then run the Iperf GET reqest to test link from the IoX host to your machine
![alt text][Postman]

[Postman]:./postman.png "postman"

To learn more about deploying IoX applications you can access DevNet labs for free [here](https://developer.cisco.com/learning/modules/iox-basic/iot-iox-app-docker/step/1)





