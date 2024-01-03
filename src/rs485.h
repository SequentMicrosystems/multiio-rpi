#ifndef RS485_H
#define RS485_H

#include "cli.h"

extern const CliCmdType CMD_CFG485_READ;
extern const CliCmdType CMD_CFG485_WRITE;

int doCfg485Read(int argc, char *argv[]);
int doCfg485Write(int argc, char *argv[]);

#endif /* RS485_H */