#ifndef BOARD_H
#define BOARD_H

#include "cli.h"

extern const CliCmdType CMD_BOARD;
extern const CliCmdType CMD_LIST;

int doBoard(int argc, char *argv[]);
int doList(int argc, char *argv[]);

#endif
