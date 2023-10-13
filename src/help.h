#ifndef HELP_H
#define HELP_H

#include "cli.h"

extern const CliCmdType CMD_HELP;
extern const CliCmdType CMD_VERSION;

int generalHelp(void);
int findCmdByName(char *name);
int findCmd(int argc, char *argv[]);
int doHelp(int argc, char *argv[]);
int doVersion(int argc, char *argv[]);

#endif /* HELP_H */

// vi:fdm=marker
