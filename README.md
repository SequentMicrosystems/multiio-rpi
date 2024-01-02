# [multiio-rpi](https://sequentmicrosystems.com/collections/all-io-cards/products/multi-io-8-layer-stackable-hat-for-raspberry-pi)

## Setup

Enable I2C communication first:
```bash
sudo raspi-config
```
A good article about I2C on Raspberry can be found [here](https://www.raspberrypi-spy.co.uk/2014/11/enabling-the-i2c-interface-on-the-raspberry-pi/).

If you use Ubuntu you need to install `raspi-config` first:
```bash
sudo apt update
sudo apt install raspi-config
```

Make sure you have all tools you need:
```bash
sudo apt update
sudo apt-get install git build-essential
```

## Usage

Install the command:
```bash
git clone https://github.com/SequentMicrosystems/multiio-rpi.git
cd multiio-rpi/
sudo make install
```

Now you can access all the functions of the [Multi-IO](https://sequentmicrosystems.com/collections/all-io-cards/products/multi-io-8-layer-stackable-hat-for-raspberry-pi) through the command "multiio". Use -h option for help:
```bash
multiio -h
```

If you clone the repository any update can be made with the following commands:
```bash
cd multiio-rpi/  
git pull
sudo make install
```

 ## Examples

 The repository contains usage [examples](https://github.com/SequentMicrosystems/multiio-rpi/tree/main/examples)
 
