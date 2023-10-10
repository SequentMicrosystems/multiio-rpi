#ifndef HELP_H
#define HELP_H

#include "cli.h"

int generalHelp(void);
int findCmdByName(char *name);
int findCmd(int argc, char *argv[]);
int doHelp(int argc, char *argv[]);
extern const CliCmdType CMD_HELP;
int doVersion(int argc, char *argv[]);
extern const CliCmdType CMD_VERSION;

#endif /* HELP_H */

// vi:fdm=marker
