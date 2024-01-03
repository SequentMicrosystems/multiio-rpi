#include "motor.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#include "cli.h"
#include "comm.h"
#include "data.h"
#include "motor.h"

const CliCmdType CMD_MOTOR_READ = {
        "motrd",
        2,
        &doMotorRead,
        "  motrd            Display motor PWM fill factor value in %\n",
        "  Usage:           "PROGRAM_NAME" <id> motrd\n",
        "  Example:         "PROGRAM_NAME" 0 motrd  Display motor PWM on board #0 \n"
};
int doMotorRead(int argc, char *argv[]) {
        (void)argv;
        if(argc != 3) {
                return ARG_CNT_ERR;
        }
        int dev = doBoardInit(atoi(argv[1]));
        if(dev < 0) {
                return ERROR;
        }
        uint8_t buf[2];
        if(OK != i2cMem8Read(dev, I2C_MEM_MOT_VAL, buf, 2)) {
		printf("Fail to read!\n");
		return ERROR;
        }
        int16_t val;
        memcpy(&val, buf, 2);
        printf("%.1f\n", (float)val / 10);
        return OK;
}

const CliCmdType CMD_MOTOR_WRITE = {
        "motwr",
        2,
        &doMotorWrite,
        "  motwr            Set the motor PWM fill factor (-100..100)\n",
        "  Usage:           "PROGRAM_NAME" <id> motwr <value(%)>\n",
        "  Example:         "PROGRAM_NAME" 0 motwr 25.2  Set motor PWM  to 25.2% on board #0  \n"
};
int doMotorWrite(int argc, char *argv[]) {
        if(argc != 4) {
                return ARG_CNT_ERR;
        }
        float val = atof(argv[3]);
        if(!(-100 <= val && val <= 100)) {
                return ARG_RANGE_ERROR;
        }
        int dev = doBoardInit(atoi(argv[1]));
        if(dev <= 0) {
                return ERROR;
        }
        int16_t aux = round(val * 10);
        uint8_t buf[2];
        memcpy(buf, &aux, 2);
        if(OK != i2cMem8Write(dev, I2C_MEM_MOT_VAL, buf, 2)) {
                printf("Fail to write!\n");
                return ERROR;
        }
        return OK;
}

