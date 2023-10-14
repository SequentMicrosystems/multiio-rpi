#include "analog.h"
#include "board.h"
#include "calib.h"
#include "cli.h"
#include "comm.h"
#include "help.h"
#include "led.h"
#include "motor.h"
#include "opto.h"
#include "relay.h"
#include "rtc.h"
#include "rtd.h"
#include "servo.h"
#include "wdt.h"

const CliCmdType *gCmdArray[] = {
	&CMD_HELP,
	&CMD_VERSION,
	&CMD_BOARD,
	&CMD_CAL_STATUS,
	&CMD_UIN_READ,
	&CMD_UIN_CAL,
	&CMD_IIN_READ,
	&CMD_IIN_CAL,
	&CMD_UOUT_READ,
	&CMD_UOUT_WRITE,
	&CMD_UOUT_CAL,
	&CMD_IOUT_READ,
	&CMD_IOUT_WRITE,
	&CMD_IOUT_CAL,
	&CMD_RTD_TEMP_READ,
	&CMD_RTD_RES_READ,
	&CMD_RTC_GET,
	&CMD_RTC_SET,
	&CMD_WDT_RELOAD,
	&CMD_WDT_GET_PERIOD,
	&CMD_WDT_SET_PERIOD,
	&CMD_WDT_GET_INIT_PERIOD,
	&CMD_WDT_SET_INIT_PERIOD,
	&CMD_WDT_GET_OFF_PERIOD,
	&CMD_WDT_SET_OFF_PERIOD,
	&CMD_WDT_GET_RESET_COUNT,
	&CMD_WDT_CLR_RESET_COUNT,
	&CMD_OPTO_READ,
	&CMD_OPTO_EDGE_READ,
	&CMD_OPTO_EDGE_WRITE,
	&CMD_OPTO_CNT_READ,
	&CMD_OPTO_CNT_RESET,
	&CMD_OPTO_ENC_READ,
	&CMD_OPTO_ENC_WRITE,
	&CMD_OPTO_ENC_CNT_READ,
	&CMD_SERVO_READ,
	&CMD_SERVO_WRITE,
	&CMD_MOTOR_READ,
	&CMD_MOTOR_WRITE,
	&CMD_DOD_READ,
	&CMD_DOD_WRITE,
	&CMD_LED_READ,
	&CMD_LED_WRITE,
	0
};
