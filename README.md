## Amarisoft Radio monitoring
Both Amarisoft and EPC and ENB are providing communication via a remote API. The protocol used is WebSocket as defined in RFC 6455. The messaged exchanged between the client and MME/ENB server are in strict JSON format. The APIs of both EPC and ENB are providing a plethora of messages (config_get, config_set, log_get, stats, ue_get, etc. …). The current implementation of the Amarisoft monitoring is using the messages: ue_get, enb, stats from the EPC API and the ue_get, stats from the ENB API.

The Amarisoft Radio monitoring is based on Prometheus, an open-source software application used for event monitoring and alerting. Prometheus collects the data in the form of time series. The time series are built through a pull model: the Prometheus server queries a list of data sources (exporters) at a specific polling frequency. Each of the data sources serves the current values of the metrics of that data source. The exporter using the amarisoft monitoring system is based on collectd. 

Collectd is a daemon which collects system and application performance metrics periodically and provides mechanisms to store the values in a variety of ways. The collectd daemon has implemented two plugins. The write_prometheus and the python plugin. The write_prometheus plugin is used to listen to queries from the Prometheus server, but also to translate the metrics to a form that can be read from the Prometheus server. The python plugin embeds a Python interpreter into the collectd and exposes the API to the python-scripts. This allows to write own plugins in the popular scripting language, which then loaded and executed by the daemon without the need start new process and interpreter every few seconds.
We can name the Collectd alongside with the python plugin as the amarisoft exporter. In the amarisoft exporter there are two configuration files that are defined the the IP addresses of the EPC and ENB that need to be monitored. There are also implemented two python Scripts, one for the EPC and one for the ENB that initiate a websocket connection with the EPCs, and ENBs that are listed in the configuration files and retrieve the desired information for each of the component. 

Currently for the EPC the metrics retrieved are:
* CPU_usage
* IP, PLMN, ENB_ID, active_UEs per connected ENB
* ENB count

The ENB metrics retrieved are:

* CPU_usage
* Total throughput (DL/UL)
* UE count
* Throughput, UL/DL mcs per connected UE
* Pusch/pucch SNR and CQI per connected UE

Every time that the Prometheus queries for data the collectd daemon, the python plugin asks for the desired data all the amarisoft components API, translate the responses to the appropriate form and exposes the metrics.

For portability and ease of usage reasons, the Amarisoft Exporter, which is consisted from the collectd daemon, the Prometheus and the python plugin, is implemented as a docker container  image.

## Usage 

### Add the desired EPC and ENB
You have to add the list of the IPs of the modules that needed to be monitored.
```
cd centralized_amarisoft_exporter
cd collectd/collectd/data/plugins
nano epc_list.cfg ## configure the EPC list
nano enb_list.cfg ## configure the ENB list

```

### Start the Docker Container

First you have to configure the  docker-compose file. The exposed port currently is 9103. The image is on dockerHub but also the Dockerfile is provided.

```
cd collectd
nano docker-compose.yml  ## if you want to edit the file
sudo docker-compose up -d ## start the docker as a daemon

```


### Stop the Docker Container

```
cd collectd
sudo docker-compose down -d ## stops the docker daemon

```

### Edit Prometheus Config File

Assuming that the Prometheus is at IP: 10.30.0.249 you have to add the following at the prometheus.yml file
```
 - job_name: 'collectd'
   scrape_interval: 5s
   static_configs:
     - targets: ['10.30.0.249:9103']
```

