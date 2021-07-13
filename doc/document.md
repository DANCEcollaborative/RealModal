# Realmodal Document
This is a document which has everything you need to know if you want to make modifications.

- [Realmodal Document](#realmodal-document)
  * [Requirements and Quick Start](#requirements-and-quick-start)
  * [Configuration Details](#configuration-details)
    + [Overview](#overview)
    + [Meta-Information](#meta-information)
    + [Address](#address)
    
## Requirements and Quick Start
Refer to [readme.md](../readme.md). 
## Configuration Details
### Overview
Our project uses `.yaml` file to manage configurations between different settings. It is a language similar to `.json` 
but more readable for human. One needs to learn some basic `.yaml` grammar to use this but don't worry, it's simple.

In the project, we use [OmegaConf](https://github.com/omry/omegaconf) to load the configurations from `.yaml` file. The
configuration dictionary is stored as a `DictConfig` object, and there are three ways to fetch a property from the 
dictionary. As an example, to get the `config_name` property from the primitive object, the following 3 lines are 
equivalent and will print "Sigdial 2020 - Demo" to console:
```python
print(config.config_name)
print(config["config_name"])
print(config.get("config_name"))
```
There is a small difference when using the third method. When the key is missing in the dictionary, the `get` method 
will return `None` as the default value. You can also specify this default value by passing it to the method as:
```python
print(config.get("config_name", "Default Configuration"))
```

For most components of this project, configurations are passed and stored in `self.config` for later use.

### Meta-Information
* **config_name**: a string. The name of this configuration.
* **config_version**: a string. The version of this configuration.
* **debug**: True or False. When turning on, Realmodal will print more information to the console for easier debugging.
*May be removed or changed in recent future*.

### Address
The address of the server. The server will set up services on specified ports and communicate with the client.

In order to check your ip address of the server, one can use the command:
```shell script
ifconfig -a
``` 
* **ip**: a string of the format `x.x.x.x`. The ip address of the server. Currently, only ipv4 addresses are supported.
* **port**: two integer numbers named **upstream** and **downstream**. Available ports on the server to build 
communication. 
