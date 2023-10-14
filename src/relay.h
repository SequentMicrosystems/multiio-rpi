#ifndef RELAY_H
#define RELAY_H

#include "cli.h"

extern const CliCmdType CMD_DOD_READ;
extern const CliCmdType CMD_DOD_WRITE;

int doDODRead(int argc, char *argv[]);
int doDODWrite(int argc, char *argv[]);

#endif /* RELAY_H */
