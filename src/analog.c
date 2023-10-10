#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "analog.h"
#include "comm.h"
#include "multiio.h"

int val16Get(int dev, int baseAddr, int ch, float scale, float* val) {
	int addr = baseAddr + ANALOG_VAL_SIZE * (ch - 1);
	// TODO: check if addr in I2C_MEM_SIZE
	uint8_t buf[ANALOG_VAL_SIZE];
	if(OK != i2cMem8Read(dev, addr, buf, ANALOG_VAL_SIZE)) {
		return ERROR;
	}
	int16_t raw = 0;
	memcpy(&raw, buf, ANALOG_VAL_SIZE);
	*val = (float)raw / scale;
	return OK;
}
int val16Set(int dev, int baseAddr, int ch, float scale, float val) {
	int addr = baseAddr + ANALOG_VAL_SIZE * (ch - 1);
	// TODO: check if addr in I2C_MEM_SIZE
	uint8_t buf[ANALOG_VAL_SIZE];
	int16_t raw = ceil(val * scale);
	memcpy(buf, &raw, 2);
	if(OK != i2cMem8Write(dev, addr, buf, ANALOG_VAL_SIZE)) {
		return ERROR;
	}
	return OK;
}

const CliCmdType CMD_UOUT_READ = {/*{{{*/
	"uoutrd",
	2,
	&doUOutRead,
	"  uoutrd           Read 0-10V output voltage value(V)\n",
	"  Usage:           "PROGRAM_NAME" <id> uoutrd <channel>\n",
	"  Example:         "PROGRAM_NAME" 0 uoutrd 2 #Read voltage on 0-10V out channel #2 on board #0\n",
};
int doUOutRead(int argc, char *argv[]) {
	if(argc != 4) {
		return ARG_CNT_ERR;
	}
	int id = atoi(argv[1]);
	int dev = doBoardInit(id);
	if(dev < 0) {
		return ERROR;
	}
	int ch = atoi(argv[3]);
	if(!(CH_NR_MIN <= ch && ch <= U_OUT_CH_NO)) {
		printf("0-10V Output channel out of range!\n");
		return ARG_RANGE_ERROR;
	}
	float val = 0;
	if(OK != val16Get(dev, I2C_MEM_V_OUT, ch, VOLT_TO_MILIVOLT, &val)) {
		return ERROR;
	}
	printf("%0.3f\n", val);
	return OK;
}/*}}}*/

const CliCmdType CMD_IOUT_READ = {/*{{{*/
	"ioutrd",
	2,
	&doIOutRead,
	"  ioutrd           Read 4-20mA output current value(mA)\n",
	"  Usage:           "PROGRAM_NAME" <id> ioutrd <channel>\n",
	"  Example:         "PROGRAM_NAME" 0 ioutrd 2 #Read voltage on 4-20mA out channel #2 on board #0\n",
};
int doIOutRead(int argc, char *argv[]) {
	if(argc != 4) {
		return ARG_CNT_ERR;
	}
	int id = atoi(argv[1]);
	int dev = doBoardInit(id);
	if(dev < 0) {
		return ERROR;
	}
	int ch = atoi(argv[3]);
	if(!(CH_NR_MIN <= ch && ch <= I_OUT_CH_NO)) {
		printf("4-20mA Output channel out of range!\n");
		return ARG_RANGE_ERROR;
	}
	float val = 0;
	if(OK != val16Get(dev, I2C_MEM_I_OUT, ch, MILIAMPER_TO_MICROAMPER, &val)) {
		return ERROR;
	}
	printf("%0.3f\n", val);
	return OK;
}/*}}}*/

// vi:fdm=marker
