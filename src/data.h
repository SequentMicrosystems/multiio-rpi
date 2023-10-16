#ifndef DATA_H
#define DATA_H

#include <stdint.h>

#define CARD_NAME "Multi-IO"
#define PROGRAM_NAME "multiio"
#define VERSION "1.0.0"

#define SLAVE_OWN_ADDRESS_BASE 0x06

#define OPTO_CH_NO 4
#define COUNTER_SIZE 4
#define ADC_CH_NO 3
#define ADC_RAW_CHANNELS 5
#define ADC_RAW_VAL_SIZE 2
#define ANALOG_VAL_SIZE 2
#define SERVO_VAL_SIZE 2
#define MIN_CH_NO 1
#define I_IN_CH_NO 2
#define U_IN_CH_NO 2
#define I_OUT_CH_NO 2
#define U_OUT_CH_NO 2
#define RTD_CH_NO 2
#define RTD_TEMP_DATA_SIZE 4
#define RTD_RES_DATA_SIZE 4
#define LED_CH_NO 6
#define RELAY_CH_NO 2

#define CALIBRATION_KEY 0xaa
#define RESET_CALIBRATION_KEY	0x55
#define WDT_RESET_SIGNATURE     0xca
#define WDT_RESET_COUNT_SIGNATURE    0xbe

#define VOLT_TO_MILIVOLT 1000
#define MILIAMPER_TO_MICROAMPER 1000

enum {
	CALIB_IN_PROGRESS = 0,
	CALIB_DONE,
	CALIB_ERROR,
};
enum {
	CALIB_NOTHING = 0,
	CALIB_RTD_CH1,
	CALIB_U_IN_CH1 = CALIB_RTD_CH1 + RTD_CH_NO,
	CALIB_I_IN_CH1 = CALIB_U_IN_CH1 + U_IN_CH_NO,
	CALIB_U_OUT_CH1 = CALIB_I_IN_CH1 + I_IN_CH_NO,
	CALIB_I_OUT_CH1 = CALIB_U_OUT_CH1 + U_OUT_CH_NO,
	CALIB_LAST_CH = 10,
};

enum I2C_MEM {
	/* i2c memory addresses */
	I2C_MEM_RELAYS,
	I2C_MEM_RELAY_SET,
	I2C_MEM_RELAY_CLR,
	I2C_MEM_LEDS,
	I2C_MEM_LED_SET,
	I2C_MEM_LED_CLR,
	I2C_MEM_OPTO,
	I2C_MEM_ANALOG_TYPE,
	I2C_MEM_U_IN,
	I2C_MEM_I_IN = I2C_MEM_U_IN + U_IN_CH_NO * ANALOG_VAL_SIZE,
	I2C_MEM_U_OUT = I2C_MEM_I_IN + I_IN_CH_NO * ANALOG_VAL_SIZE,
	I2C_MEM_I_OUT = I2C_MEM_U_OUT + U_OUT_CH_NO * ANALOG_VAL_SIZE,
	I2C_MEM_MOT_VAL = I2C_MEM_I_OUT + I_OUT_CH_NO * ANALOG_VAL_SIZE,
	I2C_MEM_SERVO_VAL1 = I2C_MEM_MOT_VAL + ADC_RAW_VAL_SIZE,
	I2C_MEM_SERVO_VAL2 = I2C_MEM_SERVO_VAL1 + SERVO_VAL_SIZE,
	I2C_MEM_RTD_VAL1_ADD = I2C_MEM_SERVO_VAL2 + SERVO_VAL_SIZE,
	I2C_MEM_RTD_RES1_ADD = I2C_MEM_RTD_VAL1_ADD
		+ RTD_CH_NO * RTD_TEMP_DATA_SIZE,
	I2C_MEM_DIAG_TEMPERATURE_ADD = I2C_MEM_RTD_RES1_ADD
		+ RTD_CH_NO * RTD_RES_DATA_SIZE,
	I2C_MEM_DIAG_3V3_MV_ADD,
	I2C_MEM_DIAG_3V3_MV_ADD1,
	I2C_MEM_OPTO_IT_RISING_ADD,
	I2C_MEM_OPTO_IT_FALLING_ADD,
	I2C_MEM_OPTO_ENC_ENABLE_ADD,
	I2C_MEM_OPTO_CNT_RST_ADD,
	I2C_MEM_OPTO_ENC_CNT_RST_ADD,
	I2C_MEM_OPTO_EDGE_COUNT_ADD,
	I2C_MEM_OPTO_ENC_COUNT_ADD = I2C_MEM_OPTO_EDGE_COUNT_ADD
		+ OPTO_CH_NO * COUNTER_SIZE,
	I2C_MEM_CALIB_VALUE = I2C_MEM_OPTO_ENC_COUNT_ADD
		+ OPTO_CH_NO * COUNTER_SIZE / 2,
	I2C_MEM_CALIB_CHANNEL = I2C_MEM_CALIB_VALUE + sizeof(float),
	I2C_MEM_CALIB_KEY,
	I2C_MEM_CALIB_STATUS,
	I2C_RTC_YEAR_ADD,
	I2C_RTC_MONTH_ADD,
	I2C_RTC_DAY_ADD,
	I2C_RTC_HOUR_ADD,
	I2C_RTC_MINUTE_ADD,
	I2C_RTC_SECOND_ADD,
	I2C_RTC_SET_YEAR_ADD,
	I2C_RTC_SET_MONTH_ADD,
	I2C_RTC_SET_DAY_ADD,
	I2C_RTC_SET_HOUR_ADD,
	I2C_RTC_SET_MINUTE_ADD,
	I2C_RTC_SET_SECOND_ADD,
	I2C_RTC_CMD_ADD,
	I2C_MEM_WDT_RESET_ADD,
	I2C_MEM_WDT_INTERVAL_SET_ADD,
	I2C_MEM_WDT_INTERVAL_GET_ADD = I2C_MEM_WDT_INTERVAL_SET_ADD + 2,
	I2C_MEM_WDT_INIT_INTERVAL_SET_ADD = I2C_MEM_WDT_INTERVAL_GET_ADD + 2,
	I2C_MEM_WDT_INIT_INTERVAL_GET_ADD = I2C_MEM_WDT_INIT_INTERVAL_SET_ADD + 2,
	I2C_MEM_WDT_RESET_COUNT_ADD = I2C_MEM_WDT_INIT_INTERVAL_GET_ADD + 2,
	I2C_MEM_WDT_CLEAR_RESET_COUNT_ADD = I2C_MEM_WDT_RESET_COUNT_ADD + 2,
	I2C_MEM_WDT_POWER_OFF_INTERVAL_SET_ADD,
	I2C_MEM_WDT_POWER_OFF_INTERVAL_GET_ADD = I2C_MEM_WDT_POWER_OFF_INTERVAL_SET_ADD + 4,
	I2C_MEM_REVISION_HW_MAJOR_ADD = 0x78,
	I2C_MEM_REVISION_HW_MINOR_ADD,
	I2C_MEM_REVISION_MAJOR_ADD,
	I2C_MEM_REVISION_MINOR_ADD,
	I2C_MEM_BUTTON, /* TODO: ADD ME */
	SLAVE_BUFF_SIZE = 255,
};

#define ERROR -1
#define OK 0
#define ARG_CNT_ERR -2
#define ARG_RANGE_ERROR -3
#define IO_ERROR -4

#define STR_(x) #x
#define STR(x) STR_(x)
#define MASK_1 1
#define MASK_2 3
#define MASK_3 7
#define MASK_4 15
#define MASK_5 31
#define MASK_6 63
#define MASK_7 127
#define MASK_(x) MASK_##x
#define MASK(x) MASK_(x)

typedef enum {
	ON,
	OFF,
	STATE_COUNT,
} State;

#endif /* DATA_H */

// vi:fdm=marker