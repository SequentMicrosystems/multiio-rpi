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

const CliCmdType CMD_UIN_READ = {/*{{{*/
	"uinrd",
	2,
	&doUInRead,
	"  uinrd            Read 0-10V input voltage value(V)\n",
	"  Usage:           "PROGRAM_NAME" <id> uinrd <channel>\n",
	"  Example:         "PROGRAM_NAME" 0 uinrd 2 #Read voltage on 0-10V input channel #2 on board #0\n",
};
int doUInRead(int argc, char *argv[]) {
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
		printf("0-10V input channel out of range!\n");
		return ARG_RANGE_ERROR;
	}
	float val = 0;
	if(OK != val16Get(dev, I2C_MEM_V_OUT, ch, VOLT_TO_MILIVOLT, &val)) {
		return ERROR;
	}
	printf("%0.3f\n", val);
	return OK;
}/*}}}*/
const CliCmdType CMD_UOUT_READ = {/*{{{*/
	"uoutrd",
	2,
	&doUOutRead,
	"  uoutrd           Read 0-10V output voltage value(V)\n",
	"  Usage:           "PROGRAM_NAME" <id> uoutrd <channel>\n",
	"  Example:         "PROGRAM_NAME" 0 uoutrd 2 #Read voltage on 0-10V output channel #2 on board #0\n",
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
		printf("0-10V output channel out of range!\n");
		return ARG_RANGE_ERROR;
	}
	float val = 0;
	if(OK != val16Get(dev, I2C_MEM_V_OUT, ch, VOLT_TO_MILIVOLT, &val)) {
		return ERROR;
	}
	printf("%0.3f\n", val);
	return OK;
}/*}}}*/
const CliCmdType CMD_UOUT_WRITE = {/*{{{*/
	"uoutwr",
	2,
	&doUOutWrite,
	"  uoutwr           Write 0-10V output voltage value(V)\n",
	"  Usage:           "PROGRAM_NAME" <id> uoutwr <channel> <value(V)>\n",
	"  Example:         "PROGRAM_NAME" 0 uoutwr 2 2.5 #Write 2.5V to 0-10V output channel #2 on board #0\n",
};
int doUOutWrite(int argc, char *argv[]) {
	if(argc != 5) {
		return ARG_CNT_ERR;
	}
	int id = atoi(argv[1]);
	int dev = doBoardInit(id);
	if(dev < 0) {
		return ERROR;
	}
	int ch = atoi(argv[3]);
	if(!(CH_NR_MIN <= ch && ch <= U_OUT_CH_NO)) {
		printf("0-10V output channel out of range!\n");
		return ARG_RANGE_ERROR;
	}
	float val = atof(argv[4]);
	if(!(0 <= val && val <= 10)) {
		printf("Invalid voltage value, must be 0..10\n");
		return ARG_RANGE_ERROR;
	}
	if(OK != val16Set(dev, I2C_MEM_V_OUT, ch, VOLT_TO_MILIVOLT, val)) {
		return ERROR;
	}
	printf("done\n");
	return OK;
}/*}}}*/

const CliCmdType CMD_IIN_READ = {/*{{{*/
	"iinrd",
	2,
	&doIInRead,
	"  iinrd            Read 4-20mA input amperage value(mA)\n",
	"  Usage:           "PROGRAM_NAME" <id> iinrd <channel>\n",
	"  Example:         "PROGRAM_NAME" 0 iinrd 2 #Read amperage on 4-20mA input channel #2 on board #0\n",
};
int doIInRead(int argc, char *argv[]) {
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
		printf("4-20mA input channel out of range!\n");
		return ARG_RANGE_ERROR;
	}
	float val = 0;
	if(OK != val16Get(dev, I2C_MEM_I_OUT, ch, MILIAMPER_TO_MICROAMPER, &val)) {
		return ERROR;
	}
	printf("%0.3f\n", val);
	return OK;
}/*}}}*/
const CliCmdType CMD_IOUT_READ = {/*{{{*/
	"ioutrd",
	2,
	&doIOutRead,
	"  ioutrd           Read 4-20mA output amperage value(mA)\n",
	"  Usage:           "PROGRAM_NAME" <id> ioutrd <channel>\n",
	"  Example:         "PROGRAM_NAME" 0 ioutrd 2 #Read amperage on 4-20mA output channel #2 on board #0\n",
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
		printf("4-20mA output channel out of range!\n");
		return ARG_RANGE_ERROR;
	}
	float val = 0;
	if(OK != val16Get(dev, I2C_MEM_I_OUT, ch, MILIAMPER_TO_MICROAMPER, &val)) {
		return ERROR;
	}
	printf("%0.3f\n", val);
	return OK;
}/*}}}*/
const CliCmdType CMD_IOUT_WRITE = {/*{{{*/
	"ioutwr",
	2,
	&doIOutWrite,
	"  ioutwr           Write 4-20mA output amperage value(mA)\n",
	"  Usage:           "PROGRAM_NAME" <id> ioutwr <channel> <value(mA)>\n",
	"  Example:         "PROGRAM_NAME" 0 ioutwr 2 10.5 #Write 10.5mA to 4-20mA output channel #2 on board #0\n",
};
int doIOutWrite(int argc, char *argv[]) {
	if(argc != 5) {
		return ARG_CNT_ERR;
	}
	int id = atoi(argv[1]);
	int dev = doBoardInit(id);
	if(dev < 0) {
		return ERROR;
	}
	int ch = atoi(argv[3]);
	if(!(CH_NR_MIN <= ch && ch <= U_OUT_CH_NO)) {
		printf("4-20mA output channel out of range!\n");
		return ARG_RANGE_ERROR;
	}
	float val = atof(argv[4]);
	if(!(4 <= val && val <= 20)) {
		printf("Invalid amperage value, must be 4..20\n");
		return ARG_RANGE_ERROR;
	}
	if(OK != val16Set(dev, I2C_MEM_I_OUT, ch, MILIAMPER_TO_MICROAMPER, val)) {
		return ERROR;
	}
	printf("done\n");
	return OK;
}/*}}}*/

// vi:fdm=marker
