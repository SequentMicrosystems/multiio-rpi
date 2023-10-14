#include <stdio.h>
#include <stdlib.h>

#include "comm.h"
#include "led.h"
#include "data.h"

const CliCmdType CMD_LED_READ = {
	"ledrd",
        2,
        &doLedRead,
        "  ledrd            Display the state of general purpose LEDS on the card\n",
        "  Usage 1:         "PROGRAM_NAME" <id> ledrd <led[1.."STR(LED_CH_NO)"]>\n"
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
		for(int led = 1; led <= LED_CH_NO; ++led) {
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
                if(!(1 <= led && led <= LED_CH_NO)) {
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
        "  Usage 1:         "PROGRAM_NAME" <id> ledwr <led[1.."STR(LED_CH_NO)"]> <state(0/1)>\n"
        "  Usage 2:         "PROGRAM_NAME" <id> ledwr <mask[0.."STR(MASK(LED_CH_NO))"]>\n",
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
                int mask = atoi(argv[3]);
                if(!(0 <= mask && mask <= (1 << LED_CH_NO))) {
                        return ARG_RANGE_ERROR;
                }
                uint8_t buf[1];
                buf[0] = 0xff & mask;
                if(OK != i2cMem8Write(dev, I2C_MEM_LEDS, buf, 1)) {
                        printf("Fail to write!\n");
                        return ERROR;
                }
        }
        else if(argc == 5) {
                int led = atoi(argv[3]);
                if(!(1 <= led && led <= LED_CH_NO)) {
			printf("Led number out of range");
                        return ARG_RANGE_ERROR;
                }
                int state = atoi(argv[4]);
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

