# Realmodal

### Introduction

This repository is designed for all the python development, namely **RealModal**, including framework, submodules, etc..

Realmodal is originally designed to process multimodal data streams in real time with attachable processors. It receives
data stream from [PSI](https://github.com/DANCEcollaborative/PSI) or other modules and send back the processed 
information.

Realmodal contains two parts, **Realmodal Client** and **Realmodal Server**, which can be required to run on a same or 
two different machines.
* **Realmodal Client**: designed to communicate directly with other modules within the whole project via ActiveMQ. It 
can receive real-time multimodal streaming data, forward them to the server or process them locally, and send back the 
results back.
* **Realmodal Server**: designed for higher-load processing works including works with GPU usage. It receives data from 
Realmodal Client, process the multimodal data with complex processors including deep learning methods, and send the 
result back to the client. 

### Quick Start
#### Requirements for both Client and Server
* python >= 3.7
* Required packages are listed in ```requirement.txt```. You can install all the requirements by running:
```shell script
pip install -r requirement.txt
```
* Sometimes, the ```stomp.py``` package might not be properly installed using the previous shell command. You might need 
to install it manually from its official website or specify a different version. 
 
#### Deployment of server
* Install the requirements listed above. 
* Install [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose) if you would like to use the body pose 
estimation functions.
* Run the server using command:
```shell script
python3 StartServer.py
```
or specify your use of gpus using command:
```shell script
CUDA_VISIBLE_DEVICES=0,1 python3 StartServer.py
```

#### Running the client
* Change the variables in ```GlobalVariables.py``` and ensure the ip address is matching your server.
* Run the client using command ```python3 StartClient.py```

### Progress

* Communication between Python and Psi (Done).
* Communication between Client and Server (Done).
* Add Face Recognition and Open Pose Module (Done).
* Add Positioning calculation Module (Done).
* Demo v2.0 (Done).
* Add comments and documents (In progress).
