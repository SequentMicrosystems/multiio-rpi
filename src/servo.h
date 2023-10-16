#include "cli.h"

extern const CliCmdType CMD_SERVO_READ;
extern const CliCmdType CMD_SERVO_WRITE;

int doServoRead(int argc, char *argv[]);
int doServoWrite(int argc, char *argv[]);
