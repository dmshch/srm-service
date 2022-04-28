# srm-service

Satellite Receivers Monitoring service -  a service for collecting signal parameters from satellite receivers.

Installation and configuration are [here](https://github.com/dmshch/srm-service/wiki).
WEB interface is [here] (https://github.com/dmshch/web-app-srm-service).

##### SRM service currently works for the following satellite receiver models: 

* ProView 2962 (1 RF input; telnet access ->  synchronous and asynchronous implementation; web access -> asynchronous implementation)
* ProView 7000 (1 RF input; telnet access ->  synchronous and asynchronous implementation; web access -> asynchronous implementation)
* ProView 7100 (1 RF input; ssh access -> synchronous and asynchronous implementation; web access -> asynchronous implementation)
* ProView 7100 (4 RF input; ssh access -> synchronous and asynchronous implementation; web access -> asynchronous implementation; only for old firmware < 4.0 - without web-configuration)
* ProView 7100 (4 RF input; web access -> asynchronous implementation; only for new firmware >= 4.0 - with web-configuration)
* ProView 8130 (2 RF, main/backup; web access -> asynchronous implementation)

##### The service receives the following parameters:

* C/N (dB)
* Eb/NO(dB)
* Link Margin (dB)
* Program Number for output (SDI and IP)
* CC Errors for output services (for ProView 7100 old firmware < 4.0 - N/A)

##### Requirements:

* Python >= 3.8
* You can see all requirements in requirements.txt