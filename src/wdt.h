#ifndef WDT_H
#define WDT_H

#include "cli.h"

extern const CliCmdType CMD_WDT_RELOAD;
int doWdtReload(int argc, char *argv[]);

extern const CliCmdType CMD_WDT_SET_PERIOD;
int doWdtSetPeriod(int argc, char *argv[]);

extern const CliCmdType CMD_WDT_GET_PERIOD;
int doWdtGetPeriod(int argc, char *argv[]);

extern const CliCmdType CMD_WDT_SET_INIT_PERIOD;
int doWdtSetInitPeriod(int argc, char *argv[]);

extern const CliCmdType CMD_WDT_GET_INIT_PERIOD;
int doWdtGetInitPeriod(int argc, char *argv[]);

extern const CliCmdType CMD_WDT_SET_OFF_PERIOD;
int doWdtSetOffPeriod(int argc, char *argv[]);

extern const CliCmdType CMD_WDT_GET_OFF_PERIOD;
int doWdtGetOffPeriod(int argc, char *argv[]);

extern const CliCmdType CMD_WDT_GET_RESET_COUNT;
int doWdtGetResetCount(int argc, char *argv[]);

extern const CliCmdType CMD_WDT_CLR_RESET_COUNT;
int doWdtClearResetCount(int argc, char *argv[]);

#endif /* WDT_H */

// vi:fdm=marker
