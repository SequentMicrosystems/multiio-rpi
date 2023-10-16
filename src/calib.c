#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "calib.h"
#include "comm.h"
#include "data.h"

int calibSet(int dev, int channel, float value) {
	uint8_t buf[6] = {
		0,
		0,
		0,
		0,
		0xff & channel,
		CALIBRATION_KEY,
	};
	memcpy(buf, &value, 4);
	if(OK != i2cMem8Write(dev, I2C_MEM_CALIB_VALUE, buf, 6)) {
		printf("Failed to write calibration\n");
		return ERROR;
	}
	return OK;
}

int calibReset(int dev, int channel) {
	uint8_t buf[2] = {
		0xff & channel,
		RESET_CALIBRATION_KEY,
	};
	if(OK != i2cMem8Write(dev, I2C_MEM_CALIB_CHANNEL, buf, 2)) {
		printf("Failed to reset calibration\n");
		return ERROR;
	}
	return OK;
}

int calibStatus(int dev) {
	uint8_t buf[1];
	if(OK != i2cMem8Read(dev, I2C_MEM_CALIB_STATUS, buf, 1)) {
		printf("Failed to read calibration status\n");
		return ERROR;
	}
	switch(buf[0]) {
	case CALIB_IN_PROGRESS:
		printf("Calibration in progress\n");
		break;
	case CALIB_DONE:
		printf("Calibration done\n");
		break;
	case CALIB_ERROR:
		printf("Calibration error\n");
		break;
	default:
		printf("Unkown calibration status\n");
		break;
	}
	return OK;
}

const CliCmdType CMD_CAL_STATUS = {
	"calstat",
	2,
	&doCalStatus,
	"  calstat          Display current calibration status of device\n",
	"  Usage:           "PROGRAM_NAME" <id> calstat\n",
	"  Example:         "PROGRAM_NAME" 0 calstat\n",

};
int doCalStatus(int argc, char *argv[]) {
	if(argc != 3) {
		return ARG_CNT_ERR;
	}
	int dev = doBoardInit(atoi(argv[1]));
	if(dev < 0) {
		return ERROR;
	}
	return calibStatus(dev);
}
