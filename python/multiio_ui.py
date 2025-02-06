#!/usr/bin/python3
import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import multiio.multiio_data as data
from multiio import SMmultiio
MULTI_IO_AVAILABLE = True
import json # Import for JSON
from tkinter import filedialog # Import for file dialogs


class MultiIO_UI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("MultiIO Control Panel")
        self.geometry("800x600") # Adjusted initial window size

        # Calibration settings
        self.calib_status_var = tk.StringVar(value="N/A") # Calibration status stringvar
        self.calibration_settings = {
            'analog_in': [],
            'rtd': []
        }
        for _ in range(data.CHANNEL_NO["u_in"] + data.CHANNEL_NO["i_in"]):
            self.calibration_settings['analog_in'].append({'gain': 1.0, 'offset': 0.0})
        for _ in range(data.CHANNEL_NO["rtd"]):
            self.calibration_settings['rtd'].append({'gain': 1.0, 'offset': 0.0})

        self.multiio_card = None # Initialize to None initially
        self.board_connected = False # Track connection status

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both', padx=5, pady=5)

        self.create_version_tab()
        self.create_relay_tab()
        self.create_led_tab()
        self.create_analog_io_tab()
        self.create_rtd_tab()
        self.create_wdt_tab()
        self.create_rtc_tab()
        self.create_opto_tab()
        self.create_servo_motor_tab()
        self.create_button_tab()

        self.load_calibration_settings() # Load settings at startup

        self.reconnect_multiio_card() # Initial connection attempt with defaults
        self.update_ui_periodic()

    def load_calibration_settings(self):
        try:
            filename = filedialog.askopenfilename(defaultextension=".json",
                                                   initialfile=f"cal_multiio_{self.stack_var.get()}_{self.i2c_var.get()}",
                                                   filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                                                   title="Load Calibration Settings")
            if filename:
                with open(filename, 'r') as f:
                    loaded_settings = json.load(f)
                    # Basic validation, ensure keys are present (you can add more robust checks)
                    if 'analog_in' in loaded_settings and 'rtd' in loaded_settings:
                        self.calibration_settings = loaded_settings
                        messagebox.showinfo("Calibration", "Calibration settings loaded successfully.")
                    else:
                        messagebox.showerror("Error", "Invalid calibration settings file format.")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading calibration settings: {e}")

    def save_calibration_settings(self):
        try:
            filename = filedialog.asksaveasfilename(defaultextension=".json",
                                                    initialfile=f"cal_multiio_{self.stack_var.get()}_{self.i2c_var.get()}",
                                                    filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                                                    title="Save Calibration Settings")
            if filename:
                with open(filename, 'w') as f:
                    json.dump(self.calibration_settings, f, indent=4) # indent for pretty formatting
                messagebox.showinfo("Calibration", "Calibration settings saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving calibration settings: {e}")

    def reconnect_multiio_card(self):
        stack_id_str = self.stack_var.get()
        i2c_bus_str = self.i2c_var.get()

        try:
            stack_id = int(stack_id_str)
            i2c_bus = int(i2c_bus_str)

            if not (0 <= stack_id <= 7):
                messagebox.showerror("Value Error", "Stack ID must be between 0 and 7.")
                return
            if i2c_bus not in [1, 2]:
                messagebox.showerror("Value Error", "I2C Bus must be 1 or 2.")
                return

            # Close existing card if it exists before re-initializing
            if self.multiio_card:
                self.multiio_card.close() # Assuming SMmultiio has a close method for clean up

            self.multiio_card = SMmultiio(stack=stack_id, i2c=i2c_bus)
            self.board_connected = True
            messagebox.showinfo("Connection", f"Connected to MultiIO Board (Stack: {stack_id}, I2C: {i2c_bus})")

        except ValueError:
            messagebox.showerror("Value Error", "Invalid Stack ID or I2C Bus. Please enter integers.")
            self.multiio_card = None
            self.board_connected = False
        except Exception as e:
            messagebox.showerror("Error", f"MultiIO Card not detected or error initializing: {e}")
            self.multiio_card = None
            self.board_connected = False

        # Update UI regardless of connection success/failure to reflect status
        self.update_ui_periodic() # Refresh all UI elements
        self.update_calibration_status_label() # Specifically update calibration status


    def create_version_tab(self):
        self.version_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.version_tab, text='Version')

        ttk.Label(self.version_tab, text="Firmware Version:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.firmware_version_label = ttk.Label(self.version_tab, text="N/A")
        self.firmware_version_label.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

        ttk.Label(self.version_tab, text="Hardware Revision:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.hardware_revision_label = ttk.Label(self.version_tab, text="N/A")
        self.hardware_revision_label.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        # Stack Input
        ttk.Label(self.version_tab, text="Stack ID (0-7):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.stack_var = tk.StringVar(value="0") # Default to 0
        stack_entry = ttk.Entry(self.version_tab, textvariable=self.stack_var, width=5)
        stack_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)

        # I2C Bus Input
        ttk.Label(self.version_tab, text="I2C Bus (1 or 2):").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.i2c_var = tk.StringVar(value="1") # Default to 1
        i2c_entry = ttk.Entry(self.version_tab, textvariable=self.i2c_var, width=5)
        i2c_entry.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)

        # Connect Button
        ttk.Button(self.version_tab, text="Connect to Board", command=self.reconnect_multiio_card).grid(row=4, column=0, columnspan=2, pady=10)

    def create_relay_tab(self):
        self.relay_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.relay_tab, text='Relays')
        self.relay_vars = []
        for i in range(data.CHANNEL_NO["relay"]):
            frame = ttk.Frame(self.relay_tab, padding="5")
            frame.grid(row=i // 2, column=i % 2, padx=5, pady=5, sticky="ew") # Arrange in 2 columns
            ttk.Label(frame, text=f"Relay {i+1}:").pack(side=tk.LEFT)
            var = tk.IntVar()
            cb = ttk.Checkbutton(frame, text="ON", variable=var, command=lambda v=var, relay_num=i+1: self.set_relay_state(relay_num, v.get()))
            cb.pack(side=tk.LEFT)
            self.relay_vars.append(var)

        ttk.Button(self.relay_tab, text="Get All Relays", command=self.update_all_relays).grid(row=data.CHANNEL_NO["relay"] // 2 + 1, column=0, columnspan=2, pady=10)

    def create_led_tab(self):
        self.led_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.led_tab, text='LEDs')
        self.led_vars = []
        for i in range(data.CHANNEL_NO["led"]):
            frame = ttk.Frame(self.led_tab, padding="5")
            frame.grid(row=i // 2, column=i % 2, padx=5, pady=5, sticky="ew") # Arrange in 2 columns
            ttk.Label(frame, text=f"LED {i+1}:").pack(side=tk.LEFT)
            var = tk.IntVar()
            cb = ttk.Checkbutton(frame, text="ON", variable=var, command=lambda v=var, led_num=i+1: self.set_led_state(led_num, v.get()))
            cb.pack(side=tk.LEFT)
            self.led_vars.append(var)

        ttk.Button(self.led_tab, text="Get All LEDs", command=self.update_all_leds).grid(row=data.CHANNEL_NO["led"] // 2 + 1, column=0, columnspan=2, pady=10)

    def create_analog_io_tab(self):
        self.analog_io_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.analog_io_tab, text='Analog I/O')

        # Calibration Status Label
        calib_status_frame = ttk.Frame(self.analog_io_tab) # Frame to group status and buttons
        calib_status_frame.grid(row=0, column=0, columnspan=6, sticky="ew", padx=5, pady=5) # Span all columns

        ttk.Label(calib_status_frame, text="Calibration Status:", font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.calib_status_label_analog = ttk.Label(calib_status_frame, textvariable=self.calib_status_var, font=("Arial", 10, "bold"))
        self.calib_status_label_analog.grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)

        ttk.Button(calib_status_frame, text="Load Calibration Settings", command=self.load_calibration_settings).grid(row=0, column=2, padx=10)
        ttk.Button(calib_status_frame, text="Save Calibration Settings", command=self.save_calibration_settings).grid(row=0, column=3, padx=10)


        # 0-10V Inputs
        ttk.Label(self.analog_io_tab, text="0-10V Inputs", font=("Arial", 12)).grid(row=1, column=0, columnspan=3, pady=10)
        self.u_in_labels = []
        for i in range(data.CHANNEL_NO["u_in"]):
            frame = ttk.Frame(self.analog_io_tab, padding="5")
            frame.grid(row=i+2, column=0, columnspan=3, sticky="ew", padx=5, pady=2) # Span 3 columns to include calibration

            ttk.Label(frame, text=f"U_IN {i+1}:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
            label = ttk.Label(frame, text="N/A V")
            label.grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
            self.u_in_labels.append(label)

            # Calibration Frame
            calib_frame = ttk.LabelFrame(frame, text="Calibration", padding=5)
            calib_frame.grid(row=0, column=2, padx=10, pady=2, sticky="nw")

            ttk.Label(calib_frame, text="Point 1 Value:").grid(row=0, column=0, sticky=tk.W, padx=2, pady=1)
            point1_entry_var = tk.StringVar()
            point1_entry = ttk.Entry(calib_frame, textvariable=point1_entry_var, width=6)
            point1_entry.grid(row=0, column=1, padx=2, pady=1)
            calib_button1 = ttk.Button(calib_frame, text="Calibrate Point 1", command=lambda channel_num=i+1, entry_var=point1_entry_var: self.calibrate_u_in_point1(channel_num, entry_var.get()))
            calib_button1.grid(row=0, column=2, padx=2, pady=1)

            ttk.Label(calib_frame, text="Point 2 Value:").grid(row=1, column=0, sticky=tk.W, padx=2, pady=1)
            point2_entry_var = tk.StringVar()
            point2_entry = ttk.Entry(calib_frame, textvariable=point2_entry_var, width=6)
            point2_entry.grid(row=1, column=1, padx=2, pady=1)
            calib_button2 = ttk.Button(calib_frame, text="Calibrate Point 2", command=lambda channel_num=i+1, entry_var=point2_entry_var: self.calibrate_u_in_point2(channel_num, entry_var.get()))
            calib_button2.grid(row=1, column=2, padx=2, pady=1)


        # 0-10V Outputs
        ttk.Label(self.analog_io_tab, text="0-10V Outputs", font=("Arial", 12)).grid(row=1, column=3, columnspan=3, pady=10, padx=20) # Adjusted column span and position
        self.u_out_entries = []
        self.u_out_labels = []
        for i in range(data.CHANNEL_NO["u_out"]):
            ttk.Label(self.analog_io_tab, text=f"U_OUT {i+1}:").grid(row=i+2, column=3, sticky=tk.W, padx=5, pady=2)
            entry_var = tk.StringVar()
            entry = ttk.Entry(self.analog_io_tab, textvariable=entry_var, width=5)
            entry.grid(row=i+2, column=4, sticky=tk.W, padx=5, pady=2)
            button = ttk.Button(self.analog_io_tab, text="Set V", command=lambda v=entry_var, channel_num=i+1: self.set_u_out_voltage(channel_num, v.get()))
            button.grid(row=i+2, column=5, sticky=tk.W, padx=2, pady=2)
            label = ttk.Label(self.analog_io_tab, text="N/A V")
            label.grid(row=i+2, column=6, sticky=tk.W, padx=5, pady=2)
            self.u_out_entries.append(entry_var)
            self.u_out_labels.append(label)

        # 4-20mA Inputs
        ttk.Label(self.analog_io_tab, text="4-20mA Inputs", font=("Arial", 12)).grid(row=len(self.u_in_labels)+2, column=0, columnspan=3, pady=10) # Adjusted row position
        self.i_in_labels = []
        for i in range(data.CHANNEL_NO["i_in"]):
            ttk.Label(self.analog_io_tab, text=f"I_IN {i+1}:").grid(row=len(self.u_in_labels)+ 3 + i, column=0, sticky=tk.W, padx=5, pady=2)
            label = ttk.Label(self.analog_io_tab, text="N/A mA")
            label.grid(row=len(self.u_in_labels) + 3 + i, column=1, sticky=tk.W, padx=5, pady=2)
            self.i_in_labels.append(label)

        # 4-20mA Outputs
        ttk.Label(self.analog_io_tab, text="4-20mA Outputs", font=("Arial", 12)).grid(row=len(self.u_in_labels)+2, column=3, columnspan=3, pady=10, padx=20) # Adjusted row position and column span
        self.i_out_entries = []
        self.i_out_labels = []
        for i in range(data.CHANNEL_NO["i_out"]):
            ttk.Label(self.analog_io_tab, text=f"I_OUT {i+1}:").grid(row=len(self.u_in_labels) + 3 + i, column=3, sticky=tk.W, padx=5, pady=2)
            entry_var = tk.StringVar()
            entry = ttk.Entry(self.analog_io_tab, textvariable=entry_var, width=5)
            entry.grid(row=len(self.u_in_labels) + 3 + i, column=4, sticky=tk.W, padx=5, pady=2)
            button = ttk.Button(self.analog_io_tab, text="Set mA", command=lambda v=entry_var, channel_num=i+1: self.set_i_out_current(channel_num, v.get()))
            button.grid(row=len(self.u_in_labels) + 3 + i, column=5, sticky=tk.W, padx=2, pady=2)
            label = ttk.Label(self.analog_io_tab, text="N/A mA")
            label.grid(row=len(self.u_in_labels) + 3 + i, column=6, sticky=tk.W, padx=5, pady=2)
            self.i_out_entries.append(entry_var)
            self.i_out_labels.append(label)


    def create_rtd_tab(self):
        self.rtd_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.rtd_tab, text='RTD')

        # Calibration Status Label for RTD Tab
        calib_status_frame = ttk.Frame(self.rtd_tab) # Frame to group status and buttons
        calib_status_frame.grid(row=0, column=0, columnspan=4, sticky="ew", padx=5, pady=5) # Span all columns

        ttk.Label(calib_status_frame, text="Calibration Status:", font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.calib_status_label_rtd = ttk.Label(calib_status_frame, textvariable=self.calib_status_var, font=("Arial", 10, "bold"))
        self.calib_status_label_rtd.grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)

        ttk.Button(calib_status_frame, text="Load Calibration Settings", command=self.load_calibration_settings).grid(row=0, column=2, padx=10)
        ttk.Button(calib_status_frame, text="Save Calibration Settings", command=self.save_calibration_settings).grid(row=0, column=3, padx=10)


        ttk.Label(self.rtd_tab, text="RTD Sensors", font=("Arial", 12)).grid(row=1, column=0, columnspan=4, pady=10) # Adjusted column span
        self.rtd_temp_labels = []
        self.rtd_res_labels = []
        for i in range(data.CHANNEL_NO["rtd"]):
            frame = ttk.Frame(self.rtd_tab, padding="5")
            frame.grid(row=i+2, column=0, columnspan=4, sticky="ew", padx=5, pady=2) # Span 4 columns for calibration UI

            ttk.Label(frame, text=f"RTD {i+1} Temp:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
            temp_label = ttk.Label(frame, text="N/A °C")
            temp_label.grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
            self.rtd_temp_labels.append(temp_label)

            ttk.Label(frame, text=f"RTD {i+1} Res:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2) # Column 2 and 3 for Resistance
            res_label = ttk.Label(self.rtd_tab, text="N/A Ohm")
            res_label.grid(row=0, column=3, sticky=tk.W, padx=5, pady=2)
            self.rtd_res_labels.append(res_label)

            # Calibration Frame for RTD
            calib_frame = ttk.LabelFrame(frame, text="Calibration", padding=5)
            calib_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=2, sticky="nw") # Span all columns of the main frame

            ttk.Label(calib_frame, text="Point 1 Res (Ohm):").grid(row=0, column=0, sticky=tk.W, padx=2, pady=1)
            point1_entry_var = tk.StringVar()
            point1_entry = ttk.Entry(calib_frame, textvariable=point1_entry_var, width=6)
            point1_entry.grid(row=0, column=1, padx=2, pady=1)
            calib_button1 = ttk.Button(calib_frame, text="Calibrate Point 1", command=lambda channel_num=i+1, entry_var=point1_entry_var: self.calibrate_rtd_res_point1(channel_num, entry_var.get()))
            calib_button1.grid(row=0, column=2, padx=2, pady=1)

            ttk.Label(calib_frame, text="Point 2 Res (Ohm):").grid(row=1, column=0, sticky=tk.W, padx=2, pady=1)
            point2_entry_var = tk.StringVar()
            point2_entry = ttk.Entry(calib_frame, textvariable=point2_entry_var, width=6)
            point2_entry.grid(row=1, column=1, padx=2, pady=1)
            calib_button2 = ttk.Button(calib_frame, text="Calibrate Point 2", command=lambda channel_num=i+1, entry_var=point2_entry_var: self.calibrate_rtd_res_point2(channel_num, entry_var.get()))
            calib_button2.grid(row=1, column=2, padx=2, pady=1)


    def create_wdt_tab(self):
        self.wdt_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.wdt_tab, text='Watchdog')

        ttk.Label(self.wdt_tab, text="Watchdog Timer Settings", font=("Arial", 12)).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(self.wdt_tab, text="Period (sec):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.wdt_period_var = tk.StringVar()
        ttk.Entry(self.wdt_tab, textvariable=self.wdt_period_var, width=10).grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
        ttk.Button(self.wdt_tab, text="Set Period", command=self.set_wdt_period).grid(row=1, column=2, padx=5, pady=2)
        self.wdt_period_label = ttk.Label(self.wdt_tab, text="N/A sec")
        self.wdt_period_label.grid(row=1, column=3, sticky=tk.W, padx=5, pady=2)

        ttk.Label(self.wdt_tab, text="Initial Period (sec):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.wdt_init_period_var = tk.StringVar()
        ttk.Entry(self.wdt_tab, textvariable=self.wdt_init_period_var, width=10).grid(row=2, column=1, sticky=tk.W, padx=5, pady=2)
        ttk.Button(self.wdt_tab, text="Set Init Period", command=self.set_wdt_init_period).grid(row=2, column=2, padx=5, pady=2)
        self.wdt_init_period_label = ttk.Label(self.wdt_tab, text="N/A sec")
        self.wdt_init_period_label.grid(row=2, column=3, sticky=tk.W, padx=5, pady=2)

        ttk.Label(self.wdt_tab, text="Off Period (sec):").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        self.wdt_off_period_var = tk.StringVar()
        ttk.Entry(self.wdt_tab, textvariable=self.wdt_off_period_var, width=10).grid(row=3, column=1, sticky=tk.W, padx=5, pady=2)
        ttk.Button(self.wdt_tab, text="Set Off Period", command=self.set_wdt_off_period).grid(row=3, column=2, padx=5, pady=2)
        self.wdt_off_period_label = ttk.Label(self.wdt_tab, text="N/A sec")
        self.wdt_off_period_label.grid(row=3, column=3, sticky=tk.W, padx=5, pady=2)

        ttk.Button(self.wdt_tab, text="Reload Watchdog", command=self.reload_wdt).grid(row=4, column=0, columnspan=2, pady=10)

        ttk.Label(self.wdt_tab, text="Reset Count:").grid(row=5, column=0, sticky=tk.W, padx=5, pady=2)
        self.wdt_reset_count_label = ttk.Label(self.wdt_tab, text="N/A")
        self.wdt_reset_count_label.grid(row=5, column=1, sticky=tk.W, padx=5, pady=2)
        ttk.Button(self.wdt_tab, text="Clear Reset Count", command=self.clear_wdt_reset_count).grid(row=5, column=2, padx=5, pady=2)

    def create_rtc_tab(self):
        self.rtc_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.rtc_tab, text='RTC')

        ttk.Label(self.rtc_tab, text="Real-Time Clock", font=("Arial", 12)).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(self.rtc_tab, text="Current Time:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.rtc_time_label = ttk.Label(self.rtc_tab, text="N/A")
        self.rtc_time_label.grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)

        datetime_frame = ttk.Frame(self.rtc_tab)
        datetime_frame.grid(row=2, column=0, columnspan=3, pady=10)

        ttk.Label(datetime_frame, text="Year:").grid(row=0, column=0, padx=2)
        self.rtc_year_var = tk.StringVar()
        ttk.Entry(datetime_frame, textvariable=self.rtc_year_var, width=5).grid(row=0, column=1, padx=2)

        ttk.Label(datetime_frame, text="Month:").grid(row=0, column=2, padx=2)
        self.rtc_month_var = tk.StringVar()
        ttk.Entry(datetime_frame, textvariable=self.rtc_month_var, width=3).grid(row=0, column=3, padx=2)

        ttk.Label(datetime_frame, text="Day:").grid(row=0, column=4, padx=2)
        self.rtc_day_var = tk.StringVar()
        ttk.Entry(datetime_frame, textvariable=self.rtc_day_var, width=3).grid(row=0, column=5, padx=2)

        ttk.Label(datetime_frame, text="Hour:").grid(row=0, column=6, padx=2)
        self.rtc_hour_var = tk.StringVar()
        ttk.Entry(datetime_frame, textvariable=self.rtc_hour_var, width=3).grid(row=0, column=7, padx=2)

        ttk.Label(datetime_frame, text="Minute:").grid(row=0, column=8, padx=2)
        self.rtc_minute_var = tk.StringVar()
        ttk.Entry(datetime_frame, textvariable=self.rtc_minute_var, width=3).grid(row=0, column=9, padx=2)

        ttk.Label(datetime_frame, text="Second:").grid(row=0, column=10, padx=2)
        self.rtc_second_var = tk.StringVar()
        ttk.Entry(datetime_frame, textvariable=self.rtc_second_var, width=3).grid(row=0, column=11, padx=2)

        ttk.Button(self.rtc_tab, text="Set RTC Time", command=self.set_rtc_time).grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(self.rtc_tab, text="Get RTC Time", command=self.update_rtc_time).grid(row=3, column=2, columnspan=2, pady=10)


    def create_opto_tab(self):
        self.opto_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.opto_tab, text='Opto Inputs')

        # Digital Inputs
        ttk.Label(self.opto_tab, text="Optocoupled Inputs", font=("Arial", 12)).grid(row=0, column=0, columnspan=3, pady=10)
        self.opto_input_labels = []
        for i in range(data.CHANNEL_NO["opto"]):
            ttk.Label(self.opto_tab, text=f"OPTO IN {i+1}:").grid(row=i+1, column=0, sticky=tk.W, padx=5, pady=2)
            label = ttk.Label(self.opto_tab, text="N/A")
            label.grid(row=i+1, column=1, sticky=tk.W, padx=5, pady=2)
            self.opto_input_labels.append(label)

        # Edge Counters
        ttk.Label(self.opto_tab, text="Edge Counters", font=("Arial", 12)).grid(row=0, column=3, columnspan=4, pady=10, padx=20)
        self.opto_edge_mode_vars = []
        self.opto_counter_labels = []
        for i in range(data.CHANNEL_NO["opto"]):
            ttk.Label(self.opto_tab, text=f"OPTO IN {i+1} Edge:").grid(row=i+1, column=3, sticky=tk.W, padx=5, pady=2)
            mode_var = tk.StringVar()
            mode_var.set("none")
            mode_combo = ttk.Combobox(self.opto_tab, textvariable=mode_var, values=["none", "rising", "falling", "both"], width=6)
            mode_combo.grid(row=i+1, column=4, sticky=tk.W, padx=2, pady=2)
            mode_combo.bind("<<ComboboxSelected>>", lambda event, channel_num=i+1, var=mode_var: self.set_opto_edge_mode(channel_num, var.get()))
            self.opto_edge_mode_vars.append(mode_var)

            counter_label = ttk.Label(self.opto_tab, text="N/A")
            counter_label.grid(row=i+1, column=5, sticky=tk.W, padx=5, pady=2)
            self.opto_counter_labels.append(counter_label)
            reset_button = ttk.Button(self.opto_tab, text="Reset", command=lambda channel_num=i+1: self.reset_opto_counter_value(channel_num))
            reset_button.grid(row=i+1, column=6, padx=2, pady=2)

        # Encoders
        ttk.Label(self.opto_tab, text="Encoders", font=("Arial", 12)).grid(row=len(self.opto_input_labels)+1, column=0, columnspan=3, pady=10)
        self.opto_encoder_state_vars = []
        self.opto_encoder_counter_labels = []
        for i in range(data.CHANNEL_NO["opto_enc"]):
            ttk.Label(self.opto_tab, text=f"Encoder {i+1}:").grid(row=len(self.opto_input_labels) + 2 + i, column=0, sticky=tk.W, padx=5, pady=2)
            state_var = tk.IntVar()
            cb = ttk.Checkbutton(self.opto_tab, text="Enabled", variable=state_var, command=lambda v=state_var, channel_num=i+1: self.set_opto_encoder_state_value(channel_num, v.get()))
            cb.grid(row=len(self.opto_input_labels) + 2 + i, column=1, sticky=tk.W, padx=2, pady=2)
            self.opto_encoder_state_vars.append(state_var)

            enc_counter_label = ttk.Label(self.opto_tab, text="N/A")
            enc_counter_label.grid(row=len(self.opto_input_labels) + 2 + i, column=2, sticky=tk.W, padx=5, pady=2)
            self.opto_encoder_counter_labels.append(enc_counter_label)
            reset_button = ttk.Button(self.opto_tab, text="Reset", command=lambda channel_num=i+1: self.reset_opto_encoder_counter_value(channel_num))
            reset_button.grid(row=len(self.opto_input_labels) + 2 + i, column=3, padx=2, pady=2)

    def create_servo_motor_tab(self):
        self.servo_motor_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.servo_motor_tab, text='Servo/Motor')

        # Servos
        ttk.Label(self.servo_motor_tab, text="Servos", font=("Arial", 12)).grid(row=0, column=0, columnspan=2, pady=10)
        self.servo_sliders = []
        self.servo_value_labels = []
        for i in range(data.CHANNEL_NO["servo"]):
            ttk.Label(self.servo_motor_tab, text=f"Servo {i+1}:").grid(row=i+1, column=0, sticky=tk.W, padx=5, pady=2)
            slider_var = tk.DoubleVar()
            slider = tk.Scale(self.servo_motor_tab, from_=-140, to=140, orient=tk.HORIZONTAL, variable=slider_var, command=lambda value, channel_num=i+1: self.set_servo_position_value(channel_num, value), length=200)
            slider.grid(row=i+1, column=1, padx=5, pady=2)
            self.servo_sliders.append(slider_var)
            value_label = ttk.Label(self.servo_motor_tab, text="N/A %")
            value_label.grid(row=i+1, column=2, sticky=tk.W, padx=5, pady=2)
            self.servo_value_labels.append(value_label)

        # Motor
        ttk.Label(self.servo_motor_tab, text="Motor", font=("Arial", 12)).grid(row=data.CHANNEL_NO["servo"] + 1, column=0, columnspan=2, pady=10)
        ttk.Label(self.servo_motor_tab, text="Motor Speed:").grid(row=data.CHANNEL_NO["servo"] + 2, column=0, sticky=tk.W, padx=5, pady=2)
        self.motor_slider_var = tk.DoubleVar()
        motor_slider = tk.Scale(self.servo_motor_tab, from_=-100, to=100, orient=tk.HORIZONTAL, variable=self.motor_slider_var, command=lambda value: self.set_motor_speed_value(value), length=200)
        motor_slider.grid(row=data.CHANNEL_NO["servo"] + 2, column=1, padx=5, pady=2)
        self.motor_value_label = ttk.Label(self.servo_motor_tab, text="N/A %")
        self.motor_value_label.grid(row=data.CHANNEL_NO["servo"] + 2, column=2, sticky=tk.W, padx=5, pady=2)


    def create_button_tab(self):
        self.button_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.button_tab, text='Button')

        ttk.Label(self.button_tab, text="Button Input", font=("Arial", 12)).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(self.button_tab, text="Button Status:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.button_status_label = ttk.Label(self.button_tab, text="N/A")
        self.button_status_label.grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)

        ttk.Label(self.button_tab, text="Latch Status:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.button_latch_label = ttk.Label(self.button_tab, text="N/A")
        self.button_latch_label.grid(row=2, column=1, sticky=tk.W, padx=5, pady=2)


    # --- UI Update Functions ---
    def update_ui_periodic(self):
        if self.multiio_card:
            try:
                self.update_version_info()
                self.update_relay_states()
                self.update_led_states()
                self.update_analog_inputs()
                self.update_analog_outputs_labels() # Only labels updated here
                self.update_rtd_values()
                self.update_wdt_info()
                self.update_rtc_time_label()
                self.update_opto_inputs()
                self.update_opto_counters()
                self.update_opto_encoders()
                self.update_servo_motor_values()
                self.update_button_status()
                self.update_calibration_status_label() # Update calibration status

            except Exception as e:
                print(f"Error updating UI: {e}") # Print error for debugging, don't block UI

        self.after(100, self.update_ui_periodic) # Update every 100ms

    def update_calibration_status_label(self):
        if not self.multiio_card: return
        try:
            status = self.multiio_card.calib_status()
            status_text = "Calibrated" if status else "Not Calibrated"
            self.calib_status_var.set(status_text) # Update stringvar
        except Exception:
            self.calib_status_var.set("Error")


    def update_version_info(self):
        if not self.multiio_card: return
        try:
            version = self.multiio_card.get_version()
            hw_major = self.multiio_card._card_rev_major
            hw_minor = self.multiio_card._card_rev_minor
            self.firmware_version_label.config(text=version)
            self.hardware_revision_label.config(text=f"{hw_major}.{hw_minor}")
        except Exception:
            self.firmware_version_label.config(text="Error")
            self.hardware_revision_label.config(text="Error")

    def update_relay_states(self):
        if not self.multiio_card: return
        try:
            for i in range(data.CHANNEL_NO["relay"]):
                state = self.multiio_card.get_relay(i+1)
                self.relay_vars[i].set(state)
        except Exception:
            for i in range(data.CHANNEL_NO["relay"]):
                self.relay_vars[i].set(-1) # Indicate error state

    def update_all_relays(self):
        if not self.multiio_card: return
        try:
            for i in range(data.CHANNEL_NO["relay"]):
                state = self.multiio_card.get_relay(i+1)
                self.relay_vars[i].set(state)
        except Exception as e:
            messagebox.showerror("Error", f"Error reading relay states: {e}")

    def update_led_states(self):
        if not self.multiio_card: return
        try:
            for i in range(data.CHANNEL_NO["led"]):
                state = self.multiio_card.get_led(i+1)
                self.led_vars[i].set(state)
        except Exception:
            for i in range(data.CHANNEL_NO["led"]):
                self.led_vars[i].set(-1) # Indicate error state

    def update_all_leds(self):
        if not self.multiio_card: return
        try:
            for i in range(data.CHANNEL_NO["led"]):
                state = self.multiio_card.get_led(i+1)
                self.led_vars[i].set(state)
        except Exception as e:
            messagebox.showerror("Error", f"Error reading LED states: {e}")

    def update_analog_inputs(self):
        if not self.multiio_card: return
        try:
            for i in range(data.CHANNEL_NO["u_in"]):
                value = self.multiio_card.get_u_in(i+1)
                self.u_in_labels[i].config(text=f"{value:.2f} V") # Display raw value for now - will apply calibration later
            for i in range(data.CHANNEL_NO["i_in"]):
                value = self.multiio_card.get_i_in(i+1)
                self.i_in_labels[i].config(text=f"{value:.2f} mA") # Display raw value for now - will apply calibration later
        except Exception:
            for label in self.u_in_labels:
                label.config(text="Error")
            for label in self.i_in_labels:
                label.config(text="Error")

    def update_analog_outputs_labels(self):
        if not self.multiio_card: return
        try:
            for i in range(data.CHANNEL_NO["u_out"]):
                value = self.multiio_card.get_u_out(i+1)
                self.u_out_labels[i].config(text=f"{value:.2f} V")
            for i in range(data.CHANNEL_NO["i_out"]):
                value = self.multiio_card.get_i_out(i+1)
                self.i_out_labels[i].config(text=f"{value:.2f} mA")
        except Exception:
            for label in self.u_out_labels:
                label.config(text="Error")
            for label in self.i_out_labels:
                label.config(text="Error")


    def update_rtd_values(self):
        if not self.multiio_card: return
        try:
            for i in range(data.CHANNEL_NO["rtd"]):
                temp = self.multiio_card.get_rtd_temp(i+1)
                res = self.multiio_card.get_rtd_res(i+1)
                self.rtd_temp_labels[i].config(text=f"{temp:.2f} °C") # Display raw for now
                self.rtd_res_labels[i].config(text=f"{res:.2f} Ohm") # Display raw for now
        except Exception:
            for label in self.rtd_temp_labels:
                label.config(text="Error")
            for label in self.rtd_res_labels:
                label.config(text="Error")

    def update_wdt_info(self):
        if not self.multiio_card: return
        try:
            period = self.multiio_card.wdt_get_period()
            init_period = self.multiio_card.wdt_get_init_period()
            off_period = self.multiio_card.wdt_get_off_period()
            reset_count = self.multiio_card.wdt_get_reset_count()

            self.wdt_period_label.config(text=f"{period} sec")
            self.wdt_init_period_label.config(text=f"{init_period} sec")
            self.wdt_off_period_label.config(text=f"{off_period} sec")
            self.wdt_reset_count_label.config(text=str(reset_count))

            self.wdt_period_var.set(str(period)) # Update entry fields too
            self.wdt_init_period_var.set(str(init_period))
            self.wdt_off_period_var.set(str(off_period))

        except Exception:
            self.wdt_period_label.config(text="Error")
            self.wdt_init_period_label.config(text="Error")
            self.wdt_off_period_label.config(text="Error")
            self.wdt_reset_count_label.config(text="Error")

    def update_rtc_time_label(self):
        if not self.multiio_card: return
        try:
            rtc_tuple = self.multiio_card.get_rtc()
            current_time_str = datetime.datetime(*rtc_tuple).strftime("%Y-%m-%d %H:%M:%S")
            self.rtc_time_label.config(text=current_time_str)
            self.rtc_year_var.set(str(rtc_tuple[0]))
            self.rtc_month_var.set(str(rtc_tuple[1]))
            self.rtc_day_var.set(str(rtc_tuple[2]))
            self.rtc_hour_var.set(str(rtc_tuple[3]))
            self.rtc_minute_var.set(str(rtc_tuple[4]))
            self.rtc_second_var.set(str(rtc_tuple[5]))

        except Exception:
            self.rtc_time_label.config(text="Error")

    def update_opto_inputs(self):
        if not self.multiio_card: return
        try:
            for i in range(data.CHANNEL_NO["opto"]):
                state = self.multiio_card.get_opto(i+1)
                self.opto_input_labels[i].config(text="ON" if state else "OFF")
        except Exception:
            for label in self.opto_input_labels:
                label.config(text="Error")

    def update_opto_counters(self):
        if not self.multiio_card: return
        try:
            for i in range(data.CHANNEL_NO["opto"]):
                count = self.multiio_card.get_opto_counter(i+1)
                self.opto_counter_labels[i].config(text=str(count))
                edge_mode = self.multiio_card.get_opto_edge(i+1)
                mode_str = ["none", "rising", "falling", "both"][edge_mode] if 0 <= edge_mode <= 3 else "unknown"
                self.opto_edge_mode_vars[i].set(mode_str)

        except Exception:
            for label in self.opto_counter_labels:
                label.config(text="Error")

    def update_opto_encoders(self):
        if not self.multiio_card: return
        try:
            for i in range(data.CHANNEL_NO["opto_enc"]):
                count = self.multiio_card.get_opto_encoder_counter(i+1)
                self.opto_encoder_counter_labels[i].config(text=str(count))
                state = self.multiio_card.get_opto_encoder_state(i+1)
                self.opto_encoder_state_vars[i].set(state)
        except Exception:
            for label in self.opto_encoder_counter_labels:
                label.config(text="Error")

    def update_servo_motor_values(self):
        if not self.multiio_card: return
        try:
            for i in range(data.CHANNEL_NO["servo"]):
                value = self.multiio_card.get_servo(i+1)
                self.servo_value_labels[i].config(text=f"{value:.1f} %")
                self.servo_sliders[i].set(value)

            motor_value = self.multiio_card.get_motor()
            self.motor_value_label.config(text=f"{motor_value:.1f} %")
            self.motor_slider_var.set(motor_value)
        except Exception:
            for label in self.servo_value_labels:
                label.config(text="Error")
            self.motor_value_label.config(text="Error")

    def update_button_status(self):
        if not self.multiio_card: return
        try:
            button_state = self.multiio_card.get_button()
            latch_state = self.multiio_card.get_button_latch()
            self.button_status_label.config(text="Pressed" if button_state else "Released")
            self.button_latch_label.config(text="Latched" if latch_state else "Not Latched")
        except Exception:
            self.button_status_label.config(text="Error")
            self.button_latch_label.config(text="Error")


    # --- Calibration Functions ---
    def calibrate_u_in_point1(self, channel_num, value_str):
        if not self.multiio_card: return
        try:
            value = float(value_str)
            self.multiio_card.cal_u_in(channel_num, value)
            messagebox.showinfo("Calibration", f"U_IN {channel_num} Point 1 Calibrated with value: {value}")
            self.update_calibration_status_label() # Update status after calibration
        except ValueError:
            messagebox.showerror("Value Error", "Invalid calibration value. Please enter a number.")
        except Exception as e:
            messagebox.showerror("Error", f"Error calibrating U_IN {channel_num} Point 1: {e}")

    def calibrate_u_in_point2(self, channel_num, value_str):
        if not self.multiio_card: return
        try:
            value = float(value_str)
            self.multiio_card.cal_u_in(channel_num, value) # Same cal function for point 2 as per SMmultiio.py description
            messagebox.showinfo("Calibration", f"U_IN {channel_num} Point 2 Calibrated with value: {value}")
            self.update_calibration_status_label() # Update status after calibration
        except ValueError:
            messagebox.showerror("Value Error", "Invalid calibration value. Please enter a number.")
        except Exception as e:
            messagebox.showerror("Error", f"Error calibrating U_IN {channel_num} Point 2: {e}")

    def calibrate_rtd_res_point1(self, channel_num, value_str):
        if not self.multiio_card: return
        try:
            value = float(value_str)
            self.multiio_card.cal_rtd_res(channel_num, value)
            messagebox.showinfo("Calibration", f"RTD {channel_num} Point 1 Calibrated with resistance: {value} Ohm")
            self.update_calibration_status_label() # Update status after calibration
        except ValueError:
            messagebox.showerror("Value Error", "Invalid resistance value. Please enter a number.")
        except Exception as e:
            messagebox.showerror("Error", f"Error calibrating RTD {channel_num} Point 1: {e}")

    def calibrate_rtd_res_point2(self, channel_num, value_str):
        if not self.multiio_card: return
        try:
            value = float(value_str)
            self.multiio_card.cal_rtd_res(channel_num, value) # Same cal function for point 2
            messagebox.showinfo("Calibration", f"RTD {channel_num} Point 2 Calibrated with resistance: {value} Ohm")
            self.update_calibration_status_label() # Update status after calibration
        except ValueError:
            messagebox.showerror("Value Error", "Invalid resistance value. Please enter a number.")
        except Exception as e:
            messagebox.showerror("Error", f"Error calibrating RTD {channel_num} Point 2: {e}")


    # --- Set Value Functions ---
    def set_relay_state(self, relay_num, value):
        if not self.multiio_card: return
        try:
            self.multiio_card.set_relay(relay_num, value)
        except Exception as e:
            messagebox.showerror("Error", f"Error setting relay {relay_num}: {e}")

    def set_led_state(self, led_num, value):
        if not self.multiio_card: return
        try:
            self.multiio_card.set_led(led_num, value)
        except Exception as e:
            messagebox.showerror("Error", f"Error setting LED {led_num}: {e}")

    def set_u_out_voltage(self, channel_num, voltage_str):
        if not self.multiio_card: return
        try:
            voltage = float(voltage_str)
            if not (0 <= voltage <= 10):
                messagebox.showerror("Value Error", "Voltage must be between 0 and 10V.")
                return
            self.multiio_card.set_u_out(channel_num, voltage)
            self.update_analog_outputs_labels() # Update label immediately after setting
        except ValueError:
            messagebox.showerror("Value Error", "Invalid voltage value. Please enter a number.")
        except Exception as e:
            messagebox.showerror("Error", f"Error setting U_OUT {channel_num}: {e}")

    def set_i_out_current(self, channel_num, current_str):
        if not self.multiio_card: return
        try:
            current = float(current_str)
            if not (4 <= current <= 20):
                messagebox.showerror("Value Error", "Current must be between 4 and 20mA.")
                return
            self.multiio_card.set_i_out(channel_num, current)
            self.update_analog_outputs_labels() # Update label immediately after setting
        except ValueError:
            messagebox.showerror("Value Error", "Invalid current value. Please enter a number.")
        except Exception as e:
            messagebox.showerror("Error", f"Error setting I_OUT {channel_num}: {e}")

    def set_wdt_period(self):
        if not self.multiio_card: return
        try:
            period = int(self.wdt_period_var.get())
            self.multiio_card.wdt_set_period(period)
            self.update_wdt_info() # Refresh display after set
        except ValueError:
            messagebox.showerror("Value Error", "Invalid period value. Please enter an integer.")
        except Exception as e:
            messagebox.showerror("Error", f"Error setting WDT period: {e}")

    def set_wdt_init_period(self):
        if not self.multiio_card: return
        try:
            period = int(self.wdt_init_period_var.get())
            self.multiio_card.wdt_set_init_period(period)
            self.update_wdt_info() # Refresh display after set
        except ValueError:
            messagebox.showerror("Value Error", "Invalid initial period value. Please enter an integer.")
        except Exception as e:
            messagebox.showerror("Error", f"Error setting WDT initial period: {e}")

    def set_wdt_off_period(self):
        if not self.multiio_card: return
        try:
            period = int(self.wdt_off_period_var.get())
            self.multiio_card.wdt_set_off_period(period)
            self.update_wdt_info() # Refresh display after set
        except ValueError:
            messagebox.showerror("Value Error", "Invalid off period value. Please enter an integer.")
        except Exception as e:
            messagebox.showerror("Error", f"Error setting WDT off period: {e}")

    def reload_wdt(self):
        if not self.multiio_card: return
        try:
            self.multiio_card.wdt_reload()
            messagebox.showinfo("Watchdog", "Watchdog Reloaded!")
        except Exception as e:
            messagebox.showerror("Error", f"Error reloading watchdog: {e}")

    def clear_wdt_reset_count(self):
        if not self.multiio_card: return
        confirm = messagebox.askyesno("Confirm Clear", "Are you sure you want to clear the watchdog reset count?")
        if confirm:
            try:
                self.multiio_card.wdt_clear_reset_count()
                self.update_wdt_info() # Refresh display after clear
            except Exception as e:
                messagebox.showerror("Error", f"Error clearing WDT reset count: {e}")

    def set_rtc_time(self):
        if not self.multiio_card: return
        try:
            year = int(self.rtc_year_var.get())
            month = int(self.rtc_month_var.get())
            day = int(self.rtc_day_var.get())
            hour = int(self.rtc_hour_var.get())
            minute = int(self.rtc_minute_var.get())
            second = int(self.rtc_second_var.get())
            self.multiio_card.set_rtc(year, month, day, hour, minute, second)
            self.update_rtc_time() # Update the displayed time after setting
            messagebox.showinfo("RTC", "RTC Time Set!")
        except ValueError:
            messagebox.showerror("Value Error", "Invalid RTC time values. Please enter integers.")
        except Exception as e:
            messagebox.showerror("Error", f"Error setting RTC time: {e}")

    def update_rtc_time(self):
        self.update_rtc_time_label() # Simply refresh the label

    def set_opto_edge_mode(self, channel_num, mode_str):
        if not self.multiio_card: return
        mode_value = {"none": 0, "rising": 1, "falling": 2, "both": 3}.get(mode_str, 0)
        try:
            self.multiio_card.set_opto_edge(channel_num, mode_value)
        except Exception as e:
            messagebox.showerror("Error", f"Error setting Opto IN {channel_num} edge mode: {e}")

    def reset_opto_counter_value(self, channel_num):
        if not self.multiio_card: return
        try:
            self.multiio_card.reset_opto_counter(channel_num)
            self.update_opto_counters() # Refresh counter display
        except Exception as e:
            messagebox.showerror("Error", f"Error resetting Opto IN {channel_num} counter: {e}")

    def set_opto_encoder_state_value(self, channel_num, state):
        if not self.multiio_card: return
        try:
            self.multiio_card.set_opto_encoder_state(channel_num, state)
            self.update_opto_encoders() # Refresh encoder display
        except Exception as e:
            messagebox.showerror("Error", f"Error setting Encoder {channel_num} state: {e}")

    def reset_opto_encoder_counter_value(self, channel_num):
        if not self.multiio_card: return
        try:
            self.multiio_card.reset_opto_encoder_counter(channel_num)
            self.update_opto_encoders() # Refresh encoder display
        except Exception as e:
            messagebox.showerror("Error", f"Error resetting Encoder {channel_num} counter: {e}")

    def set_servo_position_value(self, channel_num, value_str):
        if not self.multiio_card: return
        try:
            value = float(value_str)
            self.multiio_card.set_servo(channel_num, value)
            self.update_servo_motor_values() # Refresh servo value display
        except ValueError:
            messagebox.showerror("Value Error", "Invalid servo value. Please enter a number.")
        except Exception as e:
            messagebox.showerror("Error", f"Error setting Servo {channel_num} position: {e}")

    def set_motor_speed_value(self, value_str):
        if not self.multiio_card: return
        try:
            value = float(value_str)
            self.multiio_card.set_motor(value)
            self.update_servo_motor_values() # Refresh motor value display
        except ValueError:
            messagebox.showerror("Value Error", "Invalid motor speed value. Please enter a number.")
        except Exception as e:
            messagebox.showerror("Error", f"Error setting Motor speed: {e}")


if __name__ == "__main__":
    app = MultiIO_UI()
    app.mainloop()
