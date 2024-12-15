#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>

#include "board.h"
#include "comm.h"
#include "data.h"

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

const CliCmdType CMD_LIST =
{
	"-list",
	1,
	&doList,
	"  -list            Display cartd in the srack and their stack level\n",
	"  Usage:           "PROGRAM_NAME" -list\n",
	"  Example:         "PROGRAM_NAME" -list  Display list of the connected cards\n"

};
int doList(int argc, char *argv[])
{
	(void)argc;
	(void)argv;

	int ids[8];
	int i;
	int cnt = 0;

	// Supress the output of doBoardInit(Don't want to see the "Failed to open the bus")
	int stdout_fd = dup(STDOUT_FILENO);
	int null_fd = open("/dev/null", O_WRONLY);
	dup2(null_fd, STDOUT_FILENO);
	close(null_fd);
	for (i = 0; i < 8; i++)
	{
		if (doBoardInit(i) >= 0)
		{
			ids[cnt] = i;
			cnt++;
		}
	}
	fflush(stdout);
	// Restore the stdout
	dup2(stdout_fd, STDOUT_FILENO);
	close(stdout_fd);
	printf("%d board(s) detected\n", cnt);
	if (cnt > 0)
	{
		printf("Id:");
	}
	for (int i = 0; i < cnt; ++i) {
		printf(" %d", ids[i]);
	}
	printf("\n");
	return OK ;
}
// vi:fdm=marker
