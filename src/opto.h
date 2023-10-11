#ifndef OPTO_H
#define OPTO_H

#include "cli.h"

extern const CliCmdType CMD_OPTO_READ;
int doOptoRead(int argc, char *argv[]);
extern const CliCmdType CMD_OPTO_EDGE_WRITE;
int doOptoEdgeWrite(int argc, char *argv[]);
extern const CliCmdType CMD_OPTO_EDGE_READ;
int doOptoEdgeRead(int argc, char *argv[]);
extern const CliCmdType CMD_OPTO_CNT_READ;
int doOptoCntRead(int argc, char *argv[]);
extern const CliCmdType CMD_OPTO_CNT_RESET;
int doOptoCntReset(int argc, char *argv[]);
extern const CliCmdType CMD_OPTO_ENC_WRITE;
int doOptoEncoderWrite(int argc, char *argv[]);
extern const CliCmdType CMD_OPTO_ENC_READ;
int doOptoEncoderRead(int argc, char *argv[]);
extern const CliCmdType CMD_OPTO_ENC_CNT_READ;
int doOptoEncoderCntRead(int argc, char *argv[]);
extern const CliCmdType CMD_OPTO_ENC_CNT_RESET;
int doOptoEncoderCntReset(int argc, char *argv[]);

typedef enum {
	ON,
	OFF,
	STATE_COUNT
} StateType;

#endif /* OPTO_H */
