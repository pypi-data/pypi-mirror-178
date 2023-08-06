# Python NeuroSDK 2

Welcome to the Python NeuroSDK 2. The library is intended for python version 3.7 and higher, Windows version 10 and higher.

## Documentation

- [Installing](#installing)
- [Description](#description)
- [Searching device](#searching-device)
- [Connection](#connection)
- [Parameters](#paramaters)
- [Receiving signal](#receiving-signal)
- [Clean up](#clean_up)

## Installing

```
pip install pyneurosdk2
```

## Description

The package has the following structure:
 - neurosdk - the main package with the implementation of methods
 - sample - is into the neurosdk package, file `sample.py`
 - libs - also into neurosdk package, contain dll library files

The library provides three main modules:

- scanner - to search for devices

```python
from neurosdk.scanner import Scanner
```

- sensor - methods of interaction with the device

```python
from neurosdk.sensor import Sensor
```

- types - implementation of all types of the library, you can either connect everything or only those necessary for a specific task

```python
from neurosdk.cmn_types import *
```

Here is a description of how to work with a BrainBit device.

## Searching device

The `Scanner` class is used to search for a device. For a correct search, you must specify the list of device types, in this case the list will consist of one type - BrainBit. Instance creation:

```python
scanner = Scanner([SensorFamily.SensorLEBrainBit])
```

Search start:

```python
scanner.Start()
```

Stop search:

```python
scanner.Stop()
```

All found devices can be obtained using the method:

```python
sensors = scanner.Sensors()
```

During the search, an `sensorsChanged` callback will be called, which will display a list of found devices. If the device leaves the scanner's field of view for any reason, the device will disappear from the list after 12 seconds.

```python
def sensorFound(scanner, sensors):
   for i in range(len(sensors)):
       print('Sensor %s' % sensors[i])

scanner.sensorsChanged = sensorFound
```

The sensor's list will contain records of the SensorInfo type with fields:

- SensFamily: SensorFamily
- SensModel: int
- Name: str
- Address: str
- SerialNumber: str
- PairingRequired: bool

## Connection

Next, you can create any device from the list using the method:

```python
sensor = scanner.CreateSensor(sensInfo)
```
When created, the device will connect automatically. This is a blocking function, so it is desirable to call it from an separate thread. Upon successful connection, a sensor instance will be returned. If unsuccessful, an exception is thrown. On subsequent connections and disconnections, a callback will be called indicating the state of the device.

To disconnect from the device, use the following method:

```python
sensor.Disconnect()
```

To connect to a device created but not connected for any reason, the method:

```python
sensor.Connect()
```

It is blocking too.

## Parameters

SDK allows you to get information about the connected device:

```python
print(sensor.SensFamily) # SensorFamily.SensorLEBrainBit
print(sensor.Features) # [<SensorFeature.FeatureSignal: 0>, ...]
print(sensor.Commands) # [<SensorCommand.CommandStartSignal: 0>,...]
print(sensor.Parameters)
print(sensor.Name) # BrainBit
print(sensor.State) # SensorState.StateInRange
print(sensor.Address) # AA:BB:CC:DD:EE:FF
print(sensor.SerialNumber) # 123456
print(sensor.BattPower) # 50
print(sensor.SamplingFrequency) # SensorSamplingFrequency.FrequencyHz250
print(sensor.Gain) # SensorGain.SensorGain6
print(sensor.DataOffset) # SensorDataOffset.DataOffset0
print(sensor.Version) # SensorVersion(FwMajor=50, FwMinor=0, FwPatch=0, HwMajor=1, HwMinor=0, HwPatch=0, ExtMajor=65)
```

>  You can distinguish BrainBit device from Flex by the firmware version number: if the `SensorVersion.FwMajor` is more than 100 - it's Flex, if it's less than BrainBit.

If you need to change any property, you first need to check if it is writable. This can be done by reading the list of device parameters, where each parameter will have an access level:

```
[ParameterInfo(Param=<SensorParameter.ParameterOffset: 8>, ParamAccess=<SensorParamAccess.ParamAccessRead: 0>),  
 ParameterInfo(Param=<SensorParameter.ParameterState: 1>,  ParamAccess=<SensorParamAccess.ParamAccessReadNotify: 2>)
 ...]
```

And also check the support of certain modules:

```python
sensor.IsSupportedFeature(sensor_future)
sensor.IsSupportedCommand(sensor_command)
sensor.IsSupportedParameter(sensor_parameter)
```

## Receiving signal

You can start the signal with the following command:

```python
sensor.ExecCommand(SensorCommand.CommandStartSignal)
```

Stop:

```python
sensor.ExecCommand(SensorCommand.CommandStopSignal)
```

You can get the signal value using the callback:

```python
def onBrainBitSignalDataReceived(sensor, data):
   print(data)

sensor.brainBitSignalDataReceived = onBrainBitSignalDataReceived
```

After you have finished working with the signal, you can unsubscribe from the callback as follows:

```python
sensor.brainBitSignalDataReceived = None
```

It gives a list of packages. Each package contains:
- PackNum: int
- Marker: int
- O1: float
- O2: float
- T3: float
- T4: float

It is values from 4 channels in volts, a number for each packet and a marker if it was sent and this feature is supported by the device.

Similarly, to get resistance values:

```python
def onBrainBitResistDataReceived(sensor, data):
   print(data)

sensor.brainBitResistDataReceived = onBrainBitResistDataReceived

sensor.ExecCommand(SensorCommand.CommandStartResist)
sensor.ExecCommand(SensorCommand.CommandStopResist)
```

The callback returns one packet of samples, each packet contains the resistance values in volts:
- O1: float
- O2: float
- T3: float
- T4: float

After you have finished working with the resistance, you can unsubscribe from the callback as follows:

```python
sensor.brainBitResistDataReceived = None
```

> BrainBit cannot be in the resistance and signal readout mode at the same time, so you must first get the resistance values, but only after this signal, or vice versa. For example:
> ```python
> sensor.ExecCommand(SensorCommand.CommandStartResist)
> sleep(10)
> sensor.ExecCommand(SensorCommand.CommandStopResist)
> ...
> sensor.ExecCommand(SensorCommand.CommandStartSignal)
> sleep(10)
> sensor.ExecCommand(SensorCommand.CommandStopSignal)
> ```

## Clean up

After you finish working with the device, you need to clean up the resources used. This happens in the destructor of the scanner and sensor, so if they were not called by the system, you must call them manually.

```python
del sensor
del scanner
```

## License

Copyright (c) Brainbit Inc. All rights reserved.

Licensed under the [MIT license](LICENSE).
