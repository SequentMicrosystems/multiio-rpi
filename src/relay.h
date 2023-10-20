#ifndef RELAY_H
#define RELAY_H

#include "cli.h"

extern const CliCmdType CMD_RELAY_READ;
extern const CliCmdType CMD_RELAY_WRITE;

int doRelayRead(int argc, char *argv[]);
int doRelayWrite(int argc, char *argv[]);

#endif /* RELAY_H */
