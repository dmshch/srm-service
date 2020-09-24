# srm-service
Satellite Receivers Monitoring service - a web application based Flask (Python 3). The service displays signal parameters received from satellite receivers.

##### This currently works for the following satellite receiver models: 

* ProView 2962 (telnet access)
* ProView 7000 (telnet access)
* ProView 7100 (1 RF input, ssh access)
* ProView 7100 (4 RF input, ssh access, old firmware < 4.0 - without web-configuration)

##### Displayed signal parameters:

* C/N (dB)
* Eb/NO(dB)
* Link Margin (dB)
![alt-текст](https://github.com/dmshch/srm-service/blob/master/screenshots/signal_parameters.png "Parameters")


##### Color of alarm:

![alt-текст](https://github.com/dmshch/srm-service/blob/master/screenshots/color_alarm.png "Alarms")


##### External libraries for Python:
* paramiko - https://pypi.org/project/paramiko/ (ssh access)
