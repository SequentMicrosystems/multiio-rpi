#ifndef ANALOG_H
#define ANALOG_H

#include "cli.h"

extern const CliCmdType CMD_UIN_READ;
extern const CliCmdType CMD_UOUT_READ;
extern const CliCmdType CMD_UOUT_WRITE;
extern const CliCmdType CMD_IIN_READ;
extern const CliCmdType CMD_IOUT_READ;
extern const CliCmdType CMD_IOUT_WRITE;

extern const CliCmdType CMD_UIN_CAL;
extern const CliCmdType CMD_UIN_CAL_RESET;
extern const CliCmdType CMD_IIN_CAL;
extern const CliCmdType CMD_IIN_CAL_RESET;
extern const CliCmdType CMD_UOUT_CAL;
extern const CliCmdType CMD_UOUT_CAL_RESET;
extern const CliCmdType CMD_IOUT_CAL;
extern const CliCmdType CMD_IOUT_CAL_RESET;

int doUInRead(int argc, char *argv[]);
int doUOutRead(int argc, char *argv[]);
int doUOutWrite(int argc, char *argv[]);
int doIInRead(int argc, char *argv[]);
int doIOutRead(int argc, char *argv[]);
int doIOutWrite(int argc, char *argv[]);

int doUInCal(int argc, char *argv[]);
int doUInCalReset(int argc, char *argv[]);
int doIInCal(int argc, char *argv[]);
int doIInCalReset(int argc, char *argv[]);
int doUOutCal(int argc, char *argv[]);
int doUOutCalReset(int argc, char *argv[]);
int doIOutCal(int argc, char *argv[]);
int doIOutCalReset(int argc, char *argv[]);

#endif /* ANALOG_H */

// vi:fdm=marker
