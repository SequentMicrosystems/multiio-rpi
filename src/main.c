#include <stdio.h>
#include <string.h>
#include <unistd.h>

#include "cli.h"
#include "help.h"
#include "data.h"

// TODO: Implement parseArgs(int argc, char *argv[]);

int main(int argc, char *argv[]) {
	if(argc == 1) {
		printf("Command option required!\n");
		generalHelp();
		return ARG_CNT_ERR;
	}
	int cmdi = findCmd(argc, argv);
	if(cmdi < 0) {
		printf("Invalid command option!\n");
		generalHelp();
		return ERROR;
	}
	int ret = gCmdArray[cmdi]->pFunc(argc, argv);
	if(ret == ARG_CNT_ERR) {
		printf("Invalid parameters number!\n");
		printf("%s", gCmdArray[cmdi]->usage);
	}
	return ret;
}

// vi:fdm=marker
