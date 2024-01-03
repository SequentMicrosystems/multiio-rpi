#include "rs485.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#include "cli.h"
#include "comm.h"
#include "data.h"

typedef struct __attribute__((packed))
{
	unsigned int mbBaud :24;
	unsigned int mbType :4;
	unsigned int mbParity :2;
	unsigned int mbStopB :2;
	unsigned int add :8;
} ModbusSetingsType;

const CliCmdType CMD_CFG485_READ =
{
	"cfg485rd",
	2,
	&doCfg485Read,
	"  cfg485rd         Display the card RS485 port settings\n",
	"  Usage:           "PROGRAM_NAME" <id> cfg485rd\n",
	"  Example:         "PROGRAM_NAME" 0 motrd  Display RS485 port settings \n"
};
int doCfg485Read(int argc, char *argv[])
{
	(void)argv;
	if (argc != 3)
	{
		return ARG_CNT_ERR;
	}
	int dev = doBoardInit(atoi(argv[1]));
	if (dev < 0)
	{
		return ERROR;
	}
	//uint8_t buf[sizeof(ModbusSetingsType)];
	ModbusSetingsType settings;
	if (OK
		!= i2cMem8Read(dev, I2C_MODBUS_SETINGS_ADD, (uint8_t*)&settings,
			sizeof(ModbusSetingsType)))
	{
		printf("Fail to read!\n");
		return ERROR;
	}
	
	if (settings.mbType == 0)
	{
		printf(
			"RS485 port disconnected from local procesoor and can be used with Raspberry Pi Serial port\n");
	}
	else
	{
		printf("Modbus RTU slave enabled,Id: %d, BR: %d, stopB: %d, parity: %d\n",
			(int)settings.add, (int)settings.mbBaud, (int)settings.mbStopB,
			(int)settings.mbParity);
	}
	return OK;
}

const CliCmdType CMD_CFG485_WRITE =
{
	"cfg485wr",
	2,
	&doCfg485Write,
	"  cfg485wr            Set the RS485 port parameters\n",
	"  Usage:           "PROGRAM_NAME" <id> cfg485wr <modbus (0/1)> <modbus ID [1..254]> <baudrate> <stop bits(1/2)> <parity(0/1/2)>\n",
	"  Example:         "PROGRAM_NAME" 0 cfg485wr 1 1 9600 1 0  Set modbus RTU, ID = 1, baudrate 9600bps, one stop bit, parity none  \n"
};
int doCfg485Write(int argc, char *argv[])
{
	if (argc < 4)
	{
		return ARG_CNT_ERR;
	}

	ModbusSetingsType settings;
	int aux = atoi(argv[3]);
	if (aux == 0) // Disable modbus and free the RS485 for Raspberry usage
	{
		settings.mbType = 0;
		settings.mbBaud = 38400; //default 
		settings.mbParity = 0;
		settings.mbStopB = 1;
		settings.add = 1;
	}
	else //  enable the modbus and we need all the parameters
	{
		if (argc != 8)
		{
			return ARG_CNT_ERR;
		}
		settings.mbType = 1;
		aux = atoi(argv[4]); // Modbus ID
		if (aux < 1 || aux > 254)
		{
			printf("Modbus ID must be [1..254]\n");
			return ARG_RANGE_ERROR;
		}
		settings.add = aux;
		aux = atoi(argv[5]); // Baudrate
		if (aux < 1200 || aux > 115200)
		{
			printf("Baudrate must be [1200..115200]\n");
			return ARG_RANGE_ERROR;
		}
		settings.mbBaud = aux;
		aux = atoi(argv[6]); // Stop bits
		if (aux < 1 || aux > 2)
		{
			printf("Stop bits must be [1/2]\n");
			return ARG_RANGE_ERROR;
		}
		settings.mbStopB = aux;
		aux = atoi(argv[7]); // Parity
		if (aux < 0 || aux > 2)
		{
			printf("Parity must be [0/1/2]\n");
			return ARG_RANGE_ERROR;
		}
		settings.mbParity = aux;
	}
	int dev = doBoardInit(atoi(argv[1]));
	if (dev <= 0)
	{
		return ERROR;
	}
	
	if (OK != i2cMem8Write(dev, I2C_MODBUS_SETINGS_ADD, (uint8_t*)&settings, sizeof(ModbusSetingsType)))
	{
		printf("Fail to write!\n");
		return ERROR;
	}
	return OK;
}

