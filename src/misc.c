#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "misc.h"
#include "cli.h"
#include "comm.h"
#include "multiio.h"

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

const CliCmdType CMD_LED_READ = {
	"ledrd",
        2,
        &doLedRead,
        "  ledrd            Display the state of general purpose LEDS on the card\n",
        "  Usage 1:         "PROGRAM_NAME" <id> ledrd <led[1..6]>\n"
        "  Usage 2:         "PROGRAM_NAME" <id> ledrd\n",
        "  Example:         "PROGRAM_NAME" 0 ledrd 2  Get the state of #2 on board #0\n"
};
int doLedRead(int argc, char *argv[]) {
        if(!(argc == 3 || argc == 4)) {
                return ARG_CNT_ERR;
        }
        int dev = doBoardInit(atoi(argv[1]));
        if(dev < 0) {
                return ERROR;
        }
        if(argc == 3) {
		uint8_t buf[1];
                if(OK != i2cMem8Read(dev, I2C_MEM_LEDS, buf, 1)) {
                        printf("Fail to read!\n");
                        return ERROR;
                }
		for(int led = 1; led <= LED_NO; ++led) {
			if(buf[0] & (1 << (led - 1))) {
				printf("1 ");
			} else {
				printf("0 ");
			}
		}
		printf("\n");
        }
        else if(argc == 4) {
		uint8_t buf[1];
		if(OK != i2cMem8Read(dev, I2C_MEM_LEDS, buf, 1)) {
			printf("Fail to write!\n");
			return ERROR;
		}
		int led = atoi(argv[3]);
                if(!(1 <= led && led <= LED_NO)) {
			printf("Led number out of range");
                        return ARG_RANGE_ERROR;
                }
		if(buf[0] & (1 << (led - 1))) {
			printf("1\n"); /* LED ON */
		} else {
			printf("0\n");
		}
        }
        return OK;
} 

const CliCmdType CMD_LED_WRITE = {
	"ledwr",
        2,
        &doLedWrite,
        "  ledwr            Set the state of general purpose LEDS on the card\n",
        "  Usage 1:         "PROGRAM_NAME" <id> ledwr <led[1..6]> <state(0/1)>\n"
        "  Usage 2:         "PROGRAM_NAME" <id> ledwr <value[0..63]>\n",
        "  Example:         "PROGRAM_NAME" 0 ledwr 2 1  Turn ON the LED #2 on board #0\n"
};
int doLedWrite(int argc, char *argv[]) {
        if(!(argc == 4 || argc == 5)) {
                return ARG_CNT_ERR;
        }
        int dev = doBoardInit(atoi(argv[1]));
        if(dev < 0) {
                return ERROR;
        }
        if(argc == 4) {
                int state = 0;
                state = atoi(argv[3]);
                if(!(0 <= state && state <= (1 << LED_NO))) {
                        return ARG_RANGE_ERROR;
                }
                uint8_t buf[1];
                buf[0] = 0xff & state;
                if(OK != i2cMem8Write(dev, I2C_MEM_LEDS, buf, 1)) {
                        printf("Fail to write!\n");
                        return ERROR;
                }
        }
        else if(argc == 5) {
                int state = 0;
                int led = atoi(argv[3]);
                if(!(1 <= led && led <= LED_NO)) {
			printf("Led number out of range");
                        return ARG_RANGE_ERROR;
                }
                state = atoi(argv[4]);
                uint8_t buf[1];
                buf[0] = 0xff & led;
                if(state > 0) {
                        if(OK != i2cMem8Write(dev, I2C_MEM_LED_SET, buf, 1)) {
                                printf("Fail to write!\n");
                                return ERROR;
                        }
                }
                else {
                        if(OK != i2cMem8Write(dev, I2C_MEM_LED_CLR, buf, 1)) {
                                printf("Fail to write!\n");
                                return ERROR;
                        }
                }
        }
        return OK;
} 

const CliCmdType CMD_BOARD = {
        "board",
        2,
        &doBoard,
        "  board            Display the board status and firmware version number\n",

        "  Usage:           "PROGRAM_NAME" <stack> board\n",
        "  Example:         "PROGRAM_NAME" 0 board  Display vcc, temperature, firmware version \n"

};
int doBoard(int argc, char *argv[]) {
        if(argc != 3) {
                return ARG_CNT_ERR;
        }
        int dev = doBoardInit(atoi(argv[1]));
        if(dev <= 0) {
                return ERROR;
        }
        uint8_t buf[3];
        if(OK != i2cMem8Read(dev, I2C_MEM_DIAG_TEMPERATURE_ADD, buf, 3)) {
                printf("Fail to read board info!\n");
                return ERROR;
        }
        uint8_t temperature = buf[0];
        int16_t resp;
        memcpy(&resp, &buf[1], 2);
        float vIn = (float)resp / VOLT_TO_MILIVOLT; //read in milivolts
        if(ERROR == i2cMem8Read(dev, I2C_MEM_REVISION_MAJOR_ADD, buf, 2)) {
                printf("Fail to read board info!\n");
                return ERROR;
        }
        printf("Firmware version %d.%d, CPU temperature %d C, Power source %0.2f V\n",
                (int)buf[0], (int)buf[1], temperature, vIn);
        return OK;
}

// vi:fdm=marker
