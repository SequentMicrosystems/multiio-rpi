/*
 * comm.c:
 *	Communication routines "platform specific" for Raspberry Pi
 *	
 *	Copyright (c) 2016-2020 Sequent Microsystem
 *	<http://www.sequentmicrosystem.com>
 ***********************************************************************
 *	Author: Alexandru Burcea
 ***********************************************************************
 */

#include <fcntl.h>
#include <linux/i2c-dev.h>
#include <stdio.h>
#include <string.h>
#include <sys/ioctl.h>
#include <unistd.h>

#include "comm.h"
#include "data.h"

int i2cSetup(int addr) {
	char filename[32];
	sprintf(filename, "/dev/i2c-%d", 1);
	int bus = open(filename, O_RDWR);
	if(bus < 0) {
		printf("Failed to open the bus.\n");
		return ERROR;
	}
	if(ioctl(bus, I2C_SLAVE, addr) < 0) {
		printf("Failed to acquire bus access and/or talk to slave.\n");
		return ERROR;
	}
	return bus;
}

int i2cMem8Read(int dev, int add, uint8_t* buf, int size) {
	uint8_t intBuff[I2C_SMBUS_BLOCK_MAX];
	if(NULL == buf) {
		return ERROR;
	}
	if(size > I2C_SMBUS_BLOCK_MAX) {
		return ERROR;
	}
	intBuff[0] = 0xff & add;
	if(write(dev, intBuff, 1) != 1) {
		printf("Fail to select mem add!\n");
		return ERROR;
	}
	if(read(dev, buf, size) != size) {
		printf("Fail to read memory!\n");
		return ERROR;
	}
	return 0; //OK
}

int i2cMem8Write(int dev, int add, uint8_t* buf, int size) {
	uint8_t intBuff[I2C_SMBUS_BLOCK_MAX];
	if (NULL == buf) {
		return ERROR;
	}
	if (size + 1 > I2C_SMBUS_BLOCK_MAX) {
		return ERROR;
	}
	intBuff[0] = 0xff & add;
	memcpy(&intBuff[1], buf, size);
	if (write(dev, intBuff, size + 1) != size + 1) {
		printf("Fail to write memory!\n");
		return ERROR;
	}
	return 0;
}

int doBoardCheck(int id, int dev) {
	uint8_t buf[1];
	if(ERROR == i2cMem8Read(dev, I2C_MEM_REVISION_MAJOR_ADD, buf , 1)) {
		printf(CARD_NAME" id %d not detected\n", id);
		return ERROR;
	}
	return OK;
}

int doBoardInit(int id) {
	if(!(0 <= id && id <= 7)) {
		return ARG_RANGE_ERROR;
	}
	int addr = SLAVE_OWN_ADDRESS_BASE + id;
	int dev = i2cSetup(addr);
	if(dev < 0) {
		return ERROR;
	}
	if(OK != doBoardCheck(id, dev)) {
		return ERROR;
	}
	return dev;
}

// vi:fdm=marker
