#ifndef MISC_H
#define MISC_H

#include "cli.h"

extern const CliCmdType CMD_SERVO_WRITE;
int doServoWrite(int argc, char *argv[]);
extern const CliCmdType CMD_SERVO_READ;
int doServoRead(int argc, char *argv[]);

extern const CliCmdType CMD_BOARD;
int doBoard(int argc, char *argv[]);

extern const CliCmdType CMD_LED_READ;
int doLedRead(int argc, char *argv[]);
extern const CliCmdType CMD_LED_WRITE;
int doLedWrite(int argc, char *argv[]);

#endif /* MISC_H */
