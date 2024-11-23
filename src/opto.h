#ifndef OPTO_H
#define OPTO_H

#include "cli.h"

extern const CliCmdType CMD_OPTO_READ;
extern const CliCmdType CMD_OPTO_EDGE_WRITE;
extern const CliCmdType CMD_OPTO_EDGE_READ;
extern const CliCmdType CMD_OPTO_CNT_READ;
extern const CliCmdType CMD_OPTO_CNT_RESET;
extern const CliCmdType CMD_OPTO_ENC_WRITE;
extern const CliCmdType CMD_OPTO_ENC_READ;
extern const CliCmdType CMD_OPTO_ENC_CNT_READ;
extern const CliCmdType CMD_OPTO_ENC_CNT_RESET;
extern const CliCmdType CMD_OPTO_FREQUENCY_READ;
extern const CliCmdType CMD_OPTO_PWM_READ;

int doOptoRead(int argc, char *argv[]);
int doOptoEdgeWrite(int argc, char *argv[]);
int doOptoEdgeRead(int argc, char *argv[]);
int doOptoCntRead(int argc, char *argv[]);
int doOptoCntReset(int argc, char *argv[]);
int doOptoEncoderWrite(int argc, char *argv[]);
int doOptoEncoderRead(int argc, char *argv[]);
int doOptoEncoderCntRead(int argc, char *argv[]);
int doOptoEncoderCntReset(int argc, char *argv[]);
int doOptoPWMRead(int argc, char *argv[]);
int doOptoFreqRead(int argc, char *argv[]);

#endif /* OPTO_H */
