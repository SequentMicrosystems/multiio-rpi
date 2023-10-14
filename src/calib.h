#ifndef CALIB_H
#define CALIB_H

#include "cli.h"

int calib(int key, int dev, float value, int channel);
int calibSet(int dev, int channel, float value);
int calibReset(int dev, int channel);
int calibStatus(int dev);

extern const CliCmdType CMD_CAL_STATUS;
int doCalStatus(int argc, char *argv[]);

#endif /* CALIB_H */
