#include <stdio.h>
#include <string.h>

#include "help.h"
#include "data.h"

int generalHelp(void) {
	printf("Usage: "PROGRAM_NAME" [options] [...]\n");
	printf("Options:\n");
	for(int i = 0; gCmdArray[i] != NULL; ++i) {
		if(gCmdArray[i]->name != NULL) {
			printf("%s", gCmdArray[i]->help);
		}
	}
	printf("Use \""PROGRAM_NAME" -h <option>\" for more details\n");
	return OK;
}
int findCmdByName(char *name) {
	for(int i = 0; gCmdArray[i] != NULL; ++i) {
		if(strcasecmp(name, gCmdArray[i]->name) == 0) {
			return i;
		}
	}
	return ERROR;
}
int findCmd(int argc, char *argv[]) {
	int i;
	for(i = 0; gCmdArray[i] != NULL; ++i) {
		if(gCmdArray[i]->name == NULL || gCmdArray[i]->namePos >= argc) {
			continue;
		}
		if(strcasecmp(argv[gCmdArray[i]->namePos], gCmdArray[i]->name) != 0) {
			continue;
		}
		return i;
	}
	return ERROR;
}

const CliCmdType CMD_HELP = {/*{{{*/
	"-h",
	1,
	&doHelp,
	"  -h               Display the list of command options or one command option details\n",
	"  Usage 1:         "PROGRAM_NAME" -h    Display command options list\n"
	"  Usage 2:    	    "PROGRAM_NAME" -h <param>    Display help for <param> command option\n",
	"  Example:         "PROGRAM_NAME" -h rread    Display help for \"rread\" command option\n"
};
int doHelp(int argc, char *argv[]) {
	(void)argv;
	if(argc == 3) {
		int cmd = findCmdByName(argv[2]);
		if(ERROR == cmd) return ERROR;
		printf("%s%s%s", gCmdArray[cmd]->help, gCmdArray[cmd]->usage, gCmdArray[cmd]->example);
	} else {
		generalHelp();
	}
	return OK;
}/*}}}*/
const CliCmdType CMD_VERSION = {/*{{{*/
	"-v",
	1,
	&doVersion,
	"  -v               Display "PROGRAM_NAME" command version\n",
	"  Usage            "PROGRAM_NAME" -v",
	""
};
int doVersion(int argc, char *argv[]) {
	(void)argc;
	(void)argv;
	printf(PROGRAM_NAME" v%s ...\n", VERSION); 
	return OK;
};/*}}}*/

// vi:fdm=marker
