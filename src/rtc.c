#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>

#include "comm.h"
#include "data.h"
#include "rtc.h"

// TODO: debug cuz not working

const CliCmdType CMD_RTC_GET = {
	"rtcrd",
	2,
	&doRTCGet,
	"  rtcrd            Get the internal RTC date and time(mm/dd/yy hh:mm:ss)\n",
	"  Usage:           "PROGRAM_NAME" <id> rtcrd \n",
	"  Example:         "PROGRAM_NAME" 0 rtcrd; Get the nternal RTC time and date on Board #0\n"
};
int doRTCGet(int argc, char *argv[])
{
	if(argc != 3) {
		return ARG_CNT_ERR;
	}
	int dev = doBoardInit(atoi(argv[1]));
	if(dev < 0) {
		return ERROR;
	}
	uint8_t buff[6];
	if(OK != i2cMem8Read(dev, I2C_RTC_YEAR_ADD, buff, 6)) {
		printf("Fail to read RTC!\n");
		return ERROR;
	}
	printf("%02u/%02u/%02u %02u:%02u:%02u\n",
			buff[1], buff[2], buff[0],
			buff[3], buff[4], buff[5]
	      );
	return OK;
}

const CliCmdType CMD_RTC_SET = {
	"rtcwr",
	2,
	&doRTCSet,
	"  rtcwr            Set the internal RTC date and time(mm/dd/yy hh:mm:ss)\n",
	"  Usage:           "PROGRAM_NAME" <id> rtcwr <mm> <dd> <yy> <hh> <mm> <ss> \n",
	"  Example:         "PROGRAM_NAME" 0 rtcwr 9 15 20 21 43 15; Set the internal RTC time and date on Board #0 at Sept/15/2020  21:43:15\n"
};
int doRTCSet(int argc, char *argv[])
{
	if(argc != 9) {
		return ARG_CNT_ERR;
	}
	int dev = doBoardInit(atoi(argv[1]));
	if(dev < 0) {
		return ERROR;
	}
	int i;
	uint8_t buf[7];
	i = atoi(argv[3]);
	if(i < 1 || i > 12) {
		printf("Invalid month!\n");
		return ERROR;
	}
	buf[1] = i;
	i = atoi(argv[4]);
	if(i < 1 || i > 31) {
		printf("Invalid date!\n");
		return ERROR;
	}
	buf[2] = i;
	i = atoi(argv[5]);
	if(i < 0 || i > 99) {
		printf("Invalid year!\n");
		return ERROR;
	}
	buf[0] = i;
	i = atoi(argv[6]);
	if(i < 0 || i > 23) {
		printf("Invalid hour!\n");
		return ERROR;
	}
	buf[3] = i;
	i = atoi(argv[7]);
	if(i < 0 || i > 59) {
		printf("Invalid minute!\n");
		return ERROR;
	}
	buf[4] = i;
	i = atoi(argv[8]);
	if(i < 0 || i > 59) {
		printf("Invalid second!\n");
		return ERROR;
	}
	buf[5] = i;
	buf[6] = CALIBRATION_KEY;
	if(OK != i2cMem8Write(dev, I2C_RTC_SET_YEAR_ADD, buf, 7)) {
		printf("Fail to write RTC!\n");
		return ERROR;
	}
	printf("done\n");
	return OK;
}
