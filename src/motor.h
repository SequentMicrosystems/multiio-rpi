#ifndef MOTOR_H
#define MOTOR_H

#include "cli.h"

extern const CliCmdType CMD_MOTOR_READ;
extern const CliCmdType CMD_MOTOR_WRITE;

int doMotorRead(int argc, char *argv[]);
int doMotorWrite(int argc, char *argv[]);

#endif /* MOTOR_H */
