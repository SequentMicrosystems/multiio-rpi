#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#include "cli.h"
#include "comm.h"
#include "data.h"
#include "rtd.h"

const CliCmdType CMD_RTD_TEMP_READ = {
        "rtdrd",
        2,
        &doRtdTempRead,
        "  rtdrd            Display rtd temperature(C)\n",
        "  Usage:           "PROGRAM_NAME" <id> rtdrd <ch>\n",
        "  Example:         "PROGRAM_NAME" 0 rtdrd 1  Display rtd termperature on channel #1 on board #0 \n"
};
int doRtdTempRead(int argc, char *argv[]) {
        (void)argv;
        if(argc != 4) {
                return ARG_CNT_ERR;
        }
        int ch = atoi(argv[3]);
        if(!(MIN_CH_NO <= ch && ch <= RTD_CH_NO)) {
                return ARG_RANGE_ERROR;
        }
        int dev = doBoardInit(atoi(argv[1]));
        if(dev < 0) {
                return ERROR;
        }
        uint8_t buf[4];
        if(OK != i2cMem8Read(dev, I2C_MEM_RTD_VAL1_ADD + RTD_TEMP_DATA_SIZE * (ch - 1), buf, RTD_TEMP_DATA_SIZE)) {
		printf("Failed to read rtd temperature");
		return ERROR;
        }
        float val;
        memcpy(&val, buf, RTD_TEMP_DATA_SIZE);
        printf("%f\n", val);
        return OK;
}

const CliCmdType CMD_RTD_RES_READ = {
        "rtdresrd",
        2,
        &doRtdResRead,
        "  rtdresrd         Display rtd resistance(Ohm)\n",
        "  Usage:           "PROGRAM_NAME" <id> rtdresrd <ch>\n",
        "  Example:         "PROGRAM_NAME" 0 rtdresrd 1  Display rtd resistance on channel #1 on board #0 \n"
};
int doRtdResRead(int argc, char *argv[]) {
        (void)argv;
        if(argc != 4) {
                return ARG_CNT_ERR;
        }
        int ch = atoi(argv[3]);
        if(!(MIN_CH_NO <= ch && ch <= RTD_CH_NO)) {
                return ARG_RANGE_ERROR;
        }
        int dev = doBoardInit(atoi(argv[1]));
        if(dev < 0) {
                return ERROR;
        }
        uint8_t buf[4];
        if(OK != i2cMem8Read(dev, I2C_MEM_RTD_RES1_ADD + RTD_RES_DATA_SIZE * (ch - 1), buf, RTD_RES_DATA_SIZE)) {
		printf("Failed to read rtd resistance");
		return ERROR;
        }
        float val;
        memcpy(&val, buf, RTD_RES_DATA_SIZE);
        printf("%f\n", val);
        return OK;
}
