#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "analog.h"
#include "calib.h"
#include "comm.h"
#include "data.h"

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

/* bad channel check functoin {{{ */
bool badUInCh(int ch) {
	if(!(MIN_CH_NO <= ch && ch <= U_IN_CH_NO)) {
		printf("0-10V input channel out of range![%d..%d]\n", MIN_CH_NO, U_IN_CH_NO);
		return true;
	}
	return false;
}
bool badUOutCh(int ch) {
	if(!(MIN_CH_NO <= ch && ch <= U_OUT_CH_NO)) {
		printf("0-10V output channel out of range![%d..%d]\n", MIN_CH_NO, U_OUT_CH_NO);
		return true;
	}
	return false;
}
bool badIInCh(int ch) {
	if(!(MIN_CH_NO <= ch && ch <= I_IN_CH_NO)) {
		printf("0-10V input channel out of range![%d..%d]\n", MIN_CH_NO, I_IN_CH_NO);
		return true;
	}
	return false;
}
bool badIOutCh(int ch) {
	if(!(MIN_CH_NO <= ch && ch <= I_OUT_CH_NO)) {
		printf("4-20mA input channel out of range![%d..%d]\n", MIN_CH_NO, I_OUT_CH_NO);
		return true;
	}
	return false;
}
/* }}} */

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
	if(badUInCh(ch)) {
		return ARG_RANGE_ERROR;
	}
	float val = 0;
	if(OK != val16Get(dev, I2C_MEM_U_IN, ch, VOLT_TO_MILIVOLT, &val)) {
		return ERROR;
	}
	printf("%0.3f\n", val);
	return OK;
}/*}}}*/
const CliCmdType CMD_UIN_CAL = {/*{{{*/
	"uincal",
	2,
	&doUInCal,
	"  uincal           Calibrate 0-10V input channel, the calibration must be done in 2 points at min 5V apart\n",
	"  Usage 1:         "PROGRAM_NAME" <id> uincal <channel> <value(V)>\n"
	"  Usage 2:         "PROGRAM_NAME" <id> uincal <channel> reset\n",
	"  Example:         "PROGRAM_NAME" 0 uincal 1 0.5; Calibrate the 0-10V input channel #1 on board #0 at 0.5V\n"
};
int doUInCal(int argc, char *argv[]) {
	if(argc != 5) {
		return ARG_CNT_ERR;
	}
	int ch = atoi(argv[3]);
	if(badUInCh(ch)) {
		return ARG_RANGE_ERROR;
	}
	int dev = doBoardInit(atoi(argv[1]));
	if(dev < 0) {
		return ERROR;
	}
	if(strcasecmp(argv[4], "reset") == 0) {
		if(OK != calibReset(dev, CALIB_U_IN_CH1 + (ch - 1))) {
			return ERROR;
		}
		return OK;
	}
	float value = atof(argv[4]);
	if(OK != calibSet(dev, CALIB_U_IN_CH1 + (ch - 1), value)) {
		return ERROR;
	}
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
	if(badIInCh(ch)) {
		return ARG_RANGE_ERROR;
	}
	float val = 0;
	if(OK != val16Get(dev, I2C_MEM_I_IN, ch, MILIAMPER_TO_MICROAMPER, &val)) {
		return ERROR;
	}
	printf("%0.3f\n", val);
	return OK;
}/*}}}*/
const CliCmdType CMD_IIN_CAL = {/*{{{*/
	"iincal",
	2,
	&doIInCal,
	"  iincal           Calibrate 4-20mA input channel, the calibration must be done in 2 points at min 10mA apart\n",
	"  Usage 1:         "PROGRAM_NAME" <id> iincal <channel> <value(A)>\n"
	"  Usage 2:         "PROGRAM_NAME" <id> iincal <channel> reset\n",
	"  Example:         "PROGRAM_NAME" 0 iincal 1 5; Calibrate the 4-20mA input channel #1 on board #0 at 5mA\n"
};
int doIInCal(int argc, char *argv[]) {
	if(argc != 5) {
		return ARG_CNT_ERR;
	}
	int ch = atoi(argv[3]);
	if(badIInCh(ch)) {
		return ARG_RANGE_ERROR;
	}
	int dev = doBoardInit(atoi(argv[1]));
	if(dev < 0) {
		return ERROR;
	}
	float value = atof(argv[4]);
	if(strcasecmp(argv[4], "reset") == 0) {
		if(OK != calibReset(dev, CALIB_I_IN_CH1 + (ch - 1))) {
			return ERROR;
		}
		return OK;
	}
	if(OK != calibSet(dev, CALIB_I_IN_CH1 + (ch - 1), value)) {
		return ERROR;
	}
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
	if(badUOutCh(ch)) {
		return ARG_RANGE_ERROR;
	}
	float val = 0;
	if(OK != val16Get(dev, I2C_MEM_U_OUT, ch, VOLT_TO_MILIVOLT, &val)) {
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
	if(badUOutCh(ch)) {
		return ARG_RANGE_ERROR;
	}
	float val = atof(argv[4]);
	if(!(0 <= val && val <= 10)) {
		printf("Invalid voltage value, must be 0..10\n");
		return ARG_RANGE_ERROR;
	}
	if(OK != val16Set(dev, I2C_MEM_U_OUT, ch, VOLT_TO_MILIVOLT, val)) {
		return ERROR;
	}
	return OK;
}/*}}}*/
const CliCmdType CMD_UOUT_CAL = {/*{{{*/
	"uoutcal",
	2,
	&doUOutCal,
	"  uoutcal          Calibrate 0-10V output channel, the calibration must be done in 2 points at min 5V apart\n",
	"  Usage 1:         "PROGRAM_NAME" <id> uoutcal <channel> <value(V)>\n"
	"  Usage 2:         "PROGRAM_NAME" <id> uoutcal <channel> reset\n",
	"  Example:         "PROGRAM_NAME" 0 uoutcal 1 0.5; Calibrate the 0-10V output channel #1 on board #0 at 0.5V\n"
};
int doUOutCal(int argc, char *argv[]) {
	if(argc != 5) {
		return ARG_CNT_ERR;
	}
	int ch = atoi(argv[3]);
	if(badUOutCh(ch)) {
		return ARG_RANGE_ERROR;
	}
	int dev = doBoardInit(atoi(argv[1]));
	if(dev < 0) {
		return ERROR;
	}
	if(strcasecmp(argv[4], "reset") == 0) {
		if(OK != calibReset(dev, CALIB_U_OUT_CH1 + (ch - 1))) {
			return ERROR;
		}
		return OK;
	}
	float value = atof(argv[4]);
	if(OK != calibSet(dev, CALIB_U_OUT_CH1 + (ch - 1), value)) {
		return ERROR;
	}
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
	if(badIOutCh(ch)) {
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
	if(badIOutCh(ch)) {
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
	return OK;
}/*}}}*/
const CliCmdType CMD_IOUT_CAL = {/*{{{*/
	"ioutcal",
	2,
	&doIOutCal,
	"  ioutcal          Calibrate 4-20mA output channel, the calibration must be done in 2 points at min 10mA apart\n",
	"  Usage 1:         "PROGRAM_NAME" <id> ioutcal <channel> <value(A)>\n"
	"  Usage 2:         "PROGRAM_NAME" <id> ioutcal <channel> reset\n",
	"  Example:         "PROGRAM_NAME" 0 ioutcal 1 5; Calibrate the 4-20mA output channel #1 on board #0 at 5mA\n"
};
int doIOutCal(int argc, char *argv[]) {
	if(argc != 5) {
		return ARG_CNT_ERR;
	}
	int ch = atoi(argv[3]);
	if(badIInCh(ch)) {
		return ARG_RANGE_ERROR;
	}
	int dev = doBoardInit(atoi(argv[1]));
	if(dev < 0) {
		return ERROR;
	}
	float value = atof(argv[4]);
	if(strcasecmp(argv[4], "reset") == 0) {
		if(OK != calibReset(dev, CALIB_I_OUT_CH1 + (ch - 1))) {
			return ERROR;
		}
		return OK;
	}
	if(OK != calibSet(dev, CALIB_I_OUT_CH1 + (ch - 1), value)) {
		return ERROR;
	}
	return OK;
}/*}}}*/

// vi:fdm=marker
