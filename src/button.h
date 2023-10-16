#ifndef BUTTON_H
#define BUTTON_H

#include "cli.h"

extern const CliCmdType CMD_BUTTON_READ;
extern const CliCmdType CMD_BUTTON_LATCH_READ;

int doButtonLatch(int argc, char *argv[]);
int doButton(int argc, char *argv[]);

#endif /* BUTTON_H */
