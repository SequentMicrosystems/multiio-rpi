#include <stdio.h>
#include <stdlib.h>

#include "button.h"
#include "comm.h"
#include "data.h"

int buttonGet(int dev, State *state) {
        uint8_t buff[2];
        if(OK != i2cMem8Read(dev, I2C_MEM_BUTTON, buff, 1)) {
                return ERROR;
        }
        if(buff[0] & 1) {
                *state = ON;
        } else {
                *state = OFF;
        }
        return OK;
}

int buttonLatchGet(int dev, State *state) {
        uint8_t buff[1];
        if(OK != i2cMem8Read(dev, I2C_MEM_BUTTON, buff, 1)) {
                return ERROR;
        }
        if(buff[0] & 2) {
                *state = ON;
                buff[0] = 0;
                if(OK != i2cMem8Write(dev, I2C_MEM_BUTTON, buff, 1)) {
			printf("Fail to reset latch!\n");
			return ERROR;
		}//clear the latch
        }
        else {
                *state = OFF;
        }
        return OK;
}

const CliCmdType CMD_BUTTON_LATCH_READ = {
        "blrd",
        2,
        &doButtonLatch,
        "  blrd:            Read the button latch, return 1 if the button has been pushed since last read\n",
        "  Usage:           "PROGRAM_NAME" <id> blrd \n",
        "  Example:         "PROGRAM_NAME" 0 blrd \n"
};
int doButtonLatch(int argc, char *argv[]) {
	if(argc != 3) {
		return ARG_CNT_ERR;
	}
        int dev = 0;
        State state = STATE_COUNT;
        dev = doBoardInit(atoi(argv[1]));
        if(dev <= 0) {
                return ERROR;
        }
	if(OK != buttonLatchGet(dev, &state)) {
		printf("Fail to read!\n");
		return ERROR;
	}
	printf("%d\n", state);
	return OK;
}

const CliCmdType CMD_BUTTON_READ = {
        "brd",
        2,
        &doButton,
        "  brd:             Read the button current state, 1 = pushed, 0 = released\n",
        "  Usage:           "PROGRAM_NAME" <stack> brd \n",
        "  Example:         "PROGRAM_NAME" 0 brd \n"
};
int doButton(int argc, char *argv[]) {
	if(argc != 3) {
		return ARG_CNT_ERR;
	}
        int dev = 0;
        State state = STATE_COUNT;
        dev = doBoardInit(atoi(argv[1]));
        if(dev < 0) {
                return ERROR;
        }
	if(OK != buttonGet(dev, &state)) {
		printf("Fail to read!\n");
		return ERROR;
	}
	printf("%d\n", state);
	return OK;
}
