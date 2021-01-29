# srm-service

Satellite Receivers Monitoring service -  a service for collecting signal parameters from satellite receivers.

##### This currently works for the following satellite receiver models: 

* ProView 2962 (telnet access, synchronous and asynchronous implementation)
* ProView 7000 (telnet access, synchronous and asynchronous implementation)
* ProView 7100 (1 RF input, ssh access, synchronous and asynchronous implementation)
* ProView 7100 (4 RF input, ssh access, synchronous and asynchronous implementation; only for old firmware < 4.0 - without web-configuration)
* ProView 7100 - with web-configuration, in plans
* ProView 8130 - in plans

##### The service receives the following parameters:

* C/N (dB)
* Eb/NO(dB)
* Link Margin (dB)