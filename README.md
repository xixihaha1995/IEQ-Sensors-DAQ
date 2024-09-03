### Arduino-XBee-Volttron

| Methods | Toolkit Names    | Sensors                                                                            | Notes                                                                                                                                                                                                    |
|---------|------------------|------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1       | DI-149 White Box | CO2, T-RH, Lighting Air velocity, Globe temperature, Occupancy sensor, PM2.5, VOCs | This is based on a commercial data acquisition card. I was able to collect 4 channel voltages (I need some documentation to convert those voltages to corresponding physical data.                       |
| 2       | XBee White Box   | CO2, T-RH, Lighting Air velocity, Globe temperature, Occupancy sensor, PM2.5, VOCs | This is based on XBee data acquisition and VOLTTRON message bus for data storage. We're missing XBee Module, XBee USB adapter. I'm **not confident enough** to configure VOLTTRON-XBeeAgent for any laptops. |
| 3       | 3D Printed       | CO2, T-RH, Lighting                                                                | This toolkit is working now. I might be able write some simple script to make the automatic data monitoring possible. Sensors <> Arduino <> Raspberry Pi/Computers <> Google Driver                      |

### Arduino-USB
For Arduino power supply, can you use external power supply for power and use the USB port connecting with laptop for data storage?

Yes, you can simultaneously connect external power supply and USB. As explained in one of the answers, that you linked, the Arduino chooses it's power input through the supplied voltage on Vin/barrel jack. Vin has no direct connection to the VUSB, so the USB port will not get any voltage from the external supply, thus it does not get damaged.
https://arduino.stackexchange.com/questions/78838/can-i-use-and-external-power-supply-and-usb-at-the-same-time-on-my-arduino

```
conda env create -f arduino-monitor.yml
conda activate arduino-monitor
python monitor-serial-local.py
python monitor-serial-google-drive.py
```

others: https://d35mpxyw7m7k7g.cloudfront.net/bigdata_1/Get+Authentication+for+Google+Service+API+.pdf

### DATAQ DI-149
A 10 voltages power supply should be used.
```
Download the software
https://www.dataq.com/resources/obsolete/products/di-149/
DATAQ Hardware Manager > Edit > Enable Channels (5,6,7,8)
DATAQ Hardware Manager > Edit > Engineering Unit Settings #please ref the conversion from ./DAQ/Jan2216.WDQ
```