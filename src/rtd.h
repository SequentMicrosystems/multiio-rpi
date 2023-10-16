#ifndef RTD_H
#define RTD_H

#include "cli.h"

extern const CliCmdType CMD_RTD_TEMP_READ;
extern const CliCmdType CMD_RTD_RES_READ;
extern const CliCmdType CMD_RTD_RES_CALIB;

int doRtdTempRead(int argc, char *argv[]);
int doRtdResRead(int argc, char *argv[]);
int doRtdResCal(int argc, char *argv[]);

#endif /* RTD_H */
