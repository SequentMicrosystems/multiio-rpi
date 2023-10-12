#ifndef ANALOG_H
#define ANALOG_H

#include "cli.h"

extern const CliCmdType CMD_UIN_READ;
int doUInRead(int argc, char *argv[]);
extern const CliCmdType CMD_UOUT_READ;
int doUOutRead(int argc, char *argv[]);
extern const CliCmdType CMD_UOUT_WRITE;
int doUOutWrite(int argc, char *argv[]);

extern const CliCmdType CMD_IIN_READ;
int doIInRead(int argc, char *argv[]);
extern const CliCmdType CMD_IOUT_READ;
int doIOutRead(int argc, char *argv[]);
extern const CliCmdType CMD_IOUT_WRITE;
int doIOutWrite(int argc, char *argv[]);

#endif /* ANALOG_H */

// vi:fdm=marker
