# update

This is the [Sequent Microsystems](https://www.sequentmicrosystems.com) Multi-IO 8-Layer Stackable HAT with Node-RED Tutorial for Raspberry Pi
firmware update tool.

## Usage

```bash 
~$ git clone https://github.com/SequentMicrosystems/multiio-rpi.git 
~$ cd multiio-rpi/update/ 
~/multiio-rpi/update$ ./update 0 
```
If your os is 64bit replace the last line with:
```bash
~/multiio-rpi/update$ ./update64 0 
```

If you already cloned the repository, skip the first step.

The command will download the newest firmware version from our server and write it to the board. The stack level of the board must be provided as a parameter. It is very important to stop all programs, scripts, etc., that access the I2C port before starting the update. If you fail to do so and the update process stops, restart the update program until the process is complete.

