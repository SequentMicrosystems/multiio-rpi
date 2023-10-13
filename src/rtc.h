#ifndef RTC_H
#define RTC_H

#include "cli.h"

extern const CliCmdType CMD_RTC_GET;
extern const CliCmdType CMD_RTC_SET;

int doRTCGet(int argc, char *argv[]);
int doRTCSet(int argc, char *argv[]);

#endif /* RTC_H */
