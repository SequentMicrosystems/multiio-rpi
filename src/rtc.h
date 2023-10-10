#ifndef RTC_H
#define RTC_H

#include "cli.h"

extern const CliCmdType CMD_RTC_GET;
int doRTCGet(int argc, char *argv[]);
extern const CliCmdType CMD_RTC_SET;
int doRTCSet(int argc, char *argv[]);

#endif /* RTC_H */
