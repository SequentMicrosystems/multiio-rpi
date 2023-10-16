#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#include "cli.h"
#include "comm.h"
#include "data.h"
#include "servo.h"

const CliCmdType CMD_SERVO_READ = {
        "servord",
        2,
        &doServoRead,
        "  servord          Display the servo position value in %\n",
        "  Usage:           "PROGRAM_NAME" <id> servord <ch>\n",
        "  Example:         "PROGRAM_NAME" 0 servord 1  Display the servo 1 position on board #0 \n"
};
int doServoRead(int argc, char *argv[]) {
        (void)argv;
        if(argc != 4) {
                return ARG_CNT_ERR;
        }
        int ch = atoi(argv[3]);
        if(1 != ch && 2 != ch) {
                return ARG_RANGE_ERROR;
        }
        int dev = doBoardInit(atoi(argv[1]));
        if(dev < 0) {
                return ERROR;
        }
        uint8_t buf[2];
        if(OK != i2cMem8Read(dev, I2C_MEM_SERVO_VAL1 + 2 * (ch - 1), buf, 2)) {
        }
        int16_t val;
        memcpy(&val, buf, 2);
        printf("%.1f\n", (float)val / 10);
        return OK;
}

const CliCmdType CMD_SERVO_WRITE = {
        "servowr",
        2,
        &doServoWrite,
        "  servowr          Set the servo position (-100..100) for standard (-120..120) for extended range servo's \n",
        "  Usage:           "PROGRAM_NAME" <id> servowr <ch> <value(%)>\n",
        "  Example:         "PROGRAM_NAME" 0 servowr 1 25.2  Set the servo 1 position to 25.2% on board #0  \n"
};
int doServoWrite(int argc, char *argv[]) {
        if(argc != 5) {
                return ARG_CNT_ERR;
        }
        int ch = atoi(argv[3]);
        if(1 != ch && 2 != ch) {
                return ARG_RANGE_ERROR;
        }
        float val = atof(argv[4]);
        if(val > 140 || val < -140) {
                return ARG_RANGE_ERROR;
        }
        int dev = doBoardInit(atoi(argv[1]));
        if(dev <= 0) {
                return ERROR;
        }
        int16_t aux = round(val * 10);
        uint8_t buf[2];
        memcpy(buf, &aux, 2);
        if(OK != i2cMem8Write(dev, I2C_MEM_SERVO_VAL1 + 2 * (ch - 1), buf, 2)) {
                printf("Fail to write!\n");
                return ERROR;
        }
        return OK;
}

