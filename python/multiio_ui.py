#!/usr/bin/python3
import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import multiio.multiio_data as data
from multiio import SMmultiio
MULTI_IO_AVAILABLE = True
import json
from tkinter import filedialog


class MultiIO_UI(tk.Tk):
    """
    Main application class for the MultiIO Control Panel.

    This class creates the graphical user interface for controlling and monitoring
    the MultiIO hardware board. It provides tabs for different functionalities
    like relays, LEDs, analog I/O, RTD sensors, watchdog timer, real-time clock,
    opto-inputs, servo motors, and button input.
    """
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("MultiIO Control Panel")
        self.geometry("800x600")

        self.calib_status_var = tk.StringVar(value="N/A") # String variable to track calibration status for UI display
        self.calibration_settings = {
            'analog_in': [],
            'rtd': []
        }
        # Initialize calibration settings for analog inputs (voltage and current)
        for _ in range(data.CHANNEL_NO["u_in"] + data.CHANNEL_NO["i_in"]):
            self.calibration_settings['analog_in'].append({'gain': 1.0, 'offset': 0.0})
        # Initialize calibration settings for RTD inputs
        for _ in range(data.CHANNEL_NO["rtd"]):
            self.calibration_settings['rtd'].append({'gain': 1.0, 'offset': 0.0})

        self.multiio_card = None # Instance of the SMmultiio class, initialized to None until connection
        self.board_connected = False # Flag to track if the MultiIO board is successfully connected

        self.notebook = ttk.Notebook(self) # Tabbed interface to organize different functionalities
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

        self.load_calibration_settings() # Attempt to load calibration settings from file on startup

        self.reconnect_multiio_card() # Attempt to connect to the MultiIO board using default stack and I2C settings
        self.update_ui_periodic() # Start periodic UI update loop

    def load_calibration_settings(self):
        """
        Loads calibration settings from a JSON file selected by the user and applies them to the MultiIO device.

        Opens a file dialog to allow the user to choose a calibration settings file.
        If a valid file is selected and the settings are successfully loaded,
        it updates the `self.calibration_settings` dictionary, applies these settings
        to the MultiIO device, and displays a success message.
        Handles potential errors during file loading, JSON parsing, and applying settings,
        displaying error messages to the user if necessary.
        """
        try:
            default_filename = f"cal_multiio_{self.stack_var.get()}_{self.i2c_var.get()}"
            filename = filedialog.askopenfilename(defaultextension=".json",
                                                   initialfile=default_filename,
                                                   filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                                                   title="Load Calibration Settings")
            if filename:
                with open(filename, 'r') as f:
                    loaded_settings = json.load(f)
                    if 'analog_in' in loaded_settings and 'rtd' in loaded_settings: # Basic validation of loaded settings
                        self.calibration_settings = loaded_settings
                        # Apply calibration settings to the device
                        if self.apply_calibration_settings():
                            messagebox.showinfo("Calibration", "Calibration settings loaded and applied successfully.")
                    else:
                        messagebox.showerror("Error", "Invalid calibration settings file format.")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading calibration settings: {e}")

    def apply_calibration_settings(self):
        """
        Applies the loaded calibration settings to the MultiIO device.

        Iterates through the 'analog_in' and 'rtd' sections of the `self.calibration_settings`
        dictionary and sends the gain and offset values to the corresponding channels on the
        MultiIO device using the `SMmultiio` library functions.
        Handles potential exceptions during the process and updates the calibration status in the UI.
        """
        if not self.multiio_card:
            messagebox.showerror("Error", "MultiIO card not connected. Cannot apply calibration settings.")
            return False

        try:
            # Apply analog input calibration settings
            for i in range(len(self.calibration_settings['analog_in'])):
                channel_num = i + 1 # Channel numbers are 1-based
                gain = self.calibration_settings['analog_in'][i].get('gain', 1.0) # Default to 1.0 if not found
                offset = self.calibration_settings['analog_in'][i].get('offset', 0.0) # Default to 0.0 if not found
                if channel_num <= data.CHANNEL_NO["u_in"]: # Apply to 0-10V inputs
                    self.multiio_card.cal_u_in_gain_offset(channel_num, gain, offset)
                elif channel_num <= data.CHANNEL_NO["u_in"] + data.CHANNEL_NO["i_in"]: # Apply to 4-20mA inputs
                    i_in_channel_num = channel_num - data.CHANNEL_NO["u_in"]
                    self.multiio_card.cal_i_in_gain_offset(i_in_channel_num, gain, offset)

            # Apply RTD input calibration settings
            for i in range(len(self.calibration_settings['rtd'])):
                channel_num = i + 1 # Channel numbers are 1-based
                gain = self.calibration_settings['rtd'][i].get('gain', 1.0) # Default to 1.0 if not found
                offset = self.calibration_settings['rtd'][i].get('offset', 0.0) # Default to 0.0 if not found
                self.multiio_card.cal_rtd_gain_offset(channel_num, gain, offset)

            self.update_calibration_status_label() # Update calibration status in UI
            return True

        except Exception as e:
            messagebox.showerror("Error", f"Error applying calibration settings to device: {e}")
            self.calib_status_var.set("Error") # Indicate error in calibration status
            return False


    def save_calibration_settings(self):
        """
        Saves the current calibration settings to a JSON file selected by the user.

        Opens a file dialog to allow the user to specify where to save the current
        calibration settings stored in `self.calibration_settings`.
        Saves the settings as a JSON formatted file with indentation for readability.
        Displays success or error messages to the user based on the outcome of the save operation.
        """
        try:
            default_filename = f"cal_multiio_{self.stack_var.get()}_{self.i2c_var.get()}"
            filename = filedialog.asksaveasfilename(defaultextension=".json",
                                                    initialfile=default_filename,
                                                    filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                                                    title="Save Calibration Settings")
            if filename:
                with open(filename, 'w') as f:
                    json.dump(self.calibration_settings, f, indent=4) # Save with indentation for readability
                messagebox.showinfo("Calibration", "Calibration settings saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving calibration settings: {e}")

    def reconnect_multiio_card(self):
        """
        Establishes or re-establishes connection to the MultiIO card.

        Reads stack ID and I2C bus from the UI input fields, validates them,
        and attempts to initialize the SMmultiio card instance.
        Handles potential ValueErrors for invalid input and general exceptions during
        card initialization, displaying appropriate error messages to the user.
        Closes any existing connection before attempting a new one.
        Updates the UI to reflect the connection status.
        """
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

            if self.multiio_card: # Close existing connection if present
                self.multiio_card.close() # Ensure proper resource release

            self.multiio_card = SMmultiio(stack=stack_id, i2c=i2c_bus) # Initialize SMmultiio instance
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

        self.update_ui_periodic() # Refresh UI to reflect connection status and read initial values
        self.update_calibration_status_label() # Update calibration status on connection

    def create_version_tab(self):
        """Creates the 'Version' tab in the notebook."""
        self.version_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.version_tab, text='Version')

        ttk.Label(self.version_tab, text="Firmware Version:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.firmware_version_label = ttk.Label(self.version_tab, text="N/A")
        self.firmware_version_label.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

        ttk.Label(self.version_tab, text="Hardware Revision:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.hardware_revision_label = ttk.Label(self.version_tab, text="N/A")
        self.hardware_revision_label.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        ttk.Label(self.version_tab, text="Stack ID (0-7):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.stack_var = tk.StringVar(value="0") # Default stack ID
        stack_entry = ttk.Entry(self.version_tab, textvariable=self.stack_var, width=5)
        stack_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)

        ttk.Label(self.version_tab, text="I2C Bus (1 or 2):").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.i2c_var = tk.StringVar(value="1") # Default I2C bus
        i2c_entry = ttk.Entry(self.version_tab, textvariable=self.i2c_var, width=5)
        i2c_entry.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)

        ttk.Button(self.version_tab, text="Connect to Board", command=self.reconnect_multiio_card).grid(row=4, column=0, columnspan=2, pady=10)

    def create_relay_tab(self):
        """Creates the 'Relays' tab with controls for each relay channel."""
        self.relay_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.relay_tab, text='Relays')
        self.relay_vars = [] # List to store IntVar for each relay Checkbutton
        for i in range(data.CHANNEL_NO["relay"]):
            frame = ttk.Frame(self.relay_tab, padding="5")
            frame.grid(row=i // 2, column=i % 2, padx=5, pady=5, sticky="ew") # Arrange relays in two columns
            ttk.Label(frame, text=f"Relay {i+1}:").pack(side=tk.LEFT)
            var = tk.IntVar()
            cb = ttk.Checkbutton(frame, text="ON", variable=var, command=lambda v=var, relay_num=i+1: self.set_relay_state(relay_num, v.get()))
            cb.pack(side=tk.LEFT)
            self.relay_vars.append(var)

        ttk.Button(self.relay_tab, text="Get All Relays", command=self.update_all_relays).grid(row=data.CHANNEL_NO["relay"] // 2 + 1, column=0, columnspan=2, pady=10)

    def create_led_tab(self):
        """Creates the 'LEDs' tab with controls for each LED channel."""
        self.led_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.led_tab, text='LEDs')
        self.led_vars = [] # List to store IntVar for each LED Checkbutton
        for i in range(data.CHANNEL_NO["led"]):
            frame = ttk.Frame(self.led_tab, padding="5")
            frame.grid(row=i // 2, column=i % 2, padx=5, pady=5, sticky="ew") # Arrange LEDs in two columns
            ttk.Label(frame, text=f"LED {i+1}:").pack(side=tk.LEFT)
            var = tk.IntVar()
            cb = ttk.Checkbutton(frame, text="ON", variable=var, command=lambda v=var, led_num=i+1: self.set_led_state(led_num, v.get()))
            cb.pack(side=tk.LEFT)
            self.led_vars.append(var)

        ttk.Button(self.led_tab, text="Get All LEDs", command=self.update_all_leds).grid(row=data.CHANNEL_NO["led"] // 2 + 1, column=0, columnspan=2, pady=10)

    def create_analog_io_tab(self):
        """Creates the 'Analog I/O' tab with controls and displays for analog input and output channels."""
        self.analog_io_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.analog_io_tab, text='Analog I/O')

        # Calibration Status Section
        calib_status_frame = ttk.Frame(self.analog_io_tab) # Frame to group status label and buttons
        calib_status_frame.grid(row=0, column=0, columnspan=6, sticky="ew", padx=5, pady=5) # Span across all columns of the tab

        ttk.Label(calib_status_frame, text="Calibration Status:", font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.calib_status_label_analog = ttk.Label(calib_status_frame, textvariable=self.calib_status_var, font=("Arial", 10, "bold"))
        self.calib_status_label_analog.grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)

        ttk.Button(calib_status_frame, text="Load Calibration Settings", command=self.load_calibration_settings).grid(row=0, column=2, padx=10)
        ttk.Button(calib_status_frame, text="Save Calibration Settings", command=self.save_calibration_settings).grid(row=0, column=3, padx=10)


        # 0-10V Input Section
        ttk.Label(self.analog_io_tab, text="0-10V Inputs", font=("Arial", 12)).grid(row=1, column=0, columnspan=3, pady=10)
        self.u_in_labels = [] # List to store labels displaying 0-10V input values
        for i in range(data.CHANNEL_NO["u_in"]):
            frame = ttk.Frame(self.analog_io_tab, padding="5")
            frame.grid(row=i+2, column=0, columnspan=3, sticky="ew", padx=5, pady=2) # Span 3 columns to include calibration controls

            ttk.Label(frame, text=f"U_IN {i+1}:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
            label = ttk.Label(frame, text="N/A V")
            label.grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
            self.u_in_labels.append(label)

            calib_frame = ttk.LabelFrame(frame, text="Calibration", padding=5) # Calibration settings frame
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


        # 0-10V Output Section
        ttk.Label(self.analog_io_tab, text="0-10V Outputs", font=("Arial", 12)).grid(row=1, column=3, columnspan=3, pady=10, padx=20) # Positioned to the right of input section
        self.u_out_entries = [] # List to store Entry widgets for setting 0-10V output values
        self.u_out_labels = [] # List to store labels displaying 0-10V output values
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

        # 4-20mA Input Section
        ttk.Label(self.analog_io_tab, text="4-20mA Inputs", font=("Arial", 12)).grid(row=len(self.u_in_labels)+2, column=0, columnspan=3, pady=10) # Positioned below 0-10V inputs
        self.i_in_labels = [] # List to store labels displaying 4-20mA input values
        for i in range(data.CHANNEL_NO["i_in"]):
            ttk.Label(self.analog_io_tab, text=f"I_IN {i+1}:").grid(row=len(self.u_in_labels)+ 3 + i, column=0, sticky=tk.W, padx=5, pady=2)
            label = ttk.Label(self.analog_io_tab, text="N/A mA")
            label.grid(row=len(self.u_in_labels) + 3 + i, column=1, sticky=tk.W, padx=5, pady=2)
            self.i_in_labels.append(label)

        # 4-20mA Output Section
        ttk.Label(self.analog_io_tab, text="4-20mA Outputs", font=("Arial", 12)).grid(row=len(self.u_in_labels)+2, column=3, columnspan=3, pady=10, padx=20) # Positioned to the right of 4-20mA input section
        self.i_out_entries = [] # List to store Entry widgets for setting 4-20mA output values
        self.i_out_labels = [] # List to store labels displaying 4-20mA output values
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
        """Creates the 'RTD' tab with displays for RTD sensor readings and calibration controls."""
        self.rtd_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.rtd_tab, text='RTD')

        # Calibration Status Section for RTD Tab
        calib_status_frame = ttk.Frame(self.rtd_tab) # Frame to group status and calibration buttons
        calib_status_frame.grid(row=0, column=0, columnspan=4, sticky="ew", padx=5, pady=5) # Span all columns

        ttk.Label(calib_status_frame, text="Calibration Status:", font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.calib_status_label_rtd = ttk.Label(calib_status_frame, textvariable=self.calib_status_var, font=("Arial", 10, "bold"))
        self.calib_status_label_rtd.grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)

        ttk.Button(calib_status_frame, text="Load Calibration Settings", command=self.load_calibration_settings).grid(row=0, column=2, padx=10)
        ttk.Button(calib_status_frame, text="Save Calibration Settings", command=self.save_calibration_settings).grid(row=0, column=3, padx=10)


        ttk.Label(self.rtd_tab, text="RTD Sensors", font=("Arial", 12)).grid(row=1, column=0, columnspan=4, pady=10) # Span across columns
        self.rtd_temp_labels = [] # List to store labels displaying RTD temperature values
        self.rtd_res_labels = [] # List to store labels displaying RTD resistance values
        for i in range(data.CHANNEL_NO["rtd"]):
            frame = ttk.Frame(self.rtd_tab, padding="5")
            frame.grid(row=i+2, column=0, columnspan=4, sticky="ew", padx=5, pady=2) # Span 4 columns for calibration UI

            ttk.Label(frame, text=f"RTD {i+1} Temp:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
            temp_label = ttk.Label(frame, text="N/A °C")
            temp_label.grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
            self.rtd_temp_labels.append(temp_label)

            ttk.Label(frame, text=f"RTD {i+1} Res:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2) # Display Resistance values next to Temperature
            res_label = ttk.Label(self.rtd_tab, text="N/A Ohm")
            res_label.grid(row=0, column=3, sticky=tk.W, padx=5, pady=2)
            self.rtd_res_labels.append(res_label)

            calib_frame = ttk.LabelFrame(frame, text="Calibration", padding=5) # Calibration settings frame for each RTD channel
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
        """Creates the 'Watchdog' tab with controls and displays for watchdog timer settings."""
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
        """Creates the 'RTC' tab with controls for setting and displaying the Real-Time Clock."""
        self.rtc_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.rtc_tab, text='RTC')

        ttk.Label(self.rtc_tab, text="Real-Time Clock", font=("Arial", 12)).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(self.rtc_tab, text="Current Time:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.rtc_time_label = ttk.Label(self.rtc_tab, text="N/A")
        self.rtc_time_label.grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)

        datetime_frame = ttk.Frame(self.rtc_tab) # Frame to group RTC date and time entry fields
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
        """Creates the 'Opto Inputs' tab with displays and controls for opto-isolated inputs, edge counters, and encoders."""
        self.opto_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.opto_tab, text='Opto Inputs')

        # Optocoupled Inputs Section
        ttk.Label(self.opto_tab, text="Optocoupled Inputs", font=("Arial", 12)).grid(row=0, column=0, columnspan=3, pady=10)
        self.opto_input_labels = [] # List to store labels displaying opto-input states (ON/OFF)
        for i in range(data.CHANNEL_NO["opto"]):
            ttk.Label(self.opto_tab, text=f"OPTO IN {i+1}:").grid(row=i+1, column=0, sticky=tk.W, padx=5, pady=2)
            label = ttk.Label(self.opto_tab, text="N/A")
            label.grid(row=i+1, column=1, sticky=tk.W, padx=5, pady=2)
            self.opto_input_labels.append(label)

        # Edge Counters Section
        ttk.Label(self.opto_tab, text="Edge Counters", font=("Arial", 12)).grid(row=0, column=3, columnspan=4, pady=10, padx=20)
        self.opto_edge_mode_vars = [] # List to store StringVar for each opto-input edge mode Combobox
        self.opto_counter_labels = [] # List to store labels displaying opto-input edge counter values
        for i in range(data.CHANNEL_NO["opto"]):
            ttk.Label(self.opto_tab, text=f"OPTO IN {i+1} Edge:").grid(row=i+1, column=3, sticky=tk.W, padx=5, pady=2)
            mode_var = tk.StringVar()
            mode_var.set("none") # Default edge detection mode is 'none'
            mode_combo = ttk.Combobox(self.opto_tab, textvariable=mode_var, values=["none", "rising", "falling", "both"], width=6)
            mode_combo.grid(row=i+1, column=4, sticky=tk.W, padx=2, pady=2)
            mode_combo.bind("<<ComboboxSelected>>", lambda event, channel_num=i+1, var=mode_var: self.set_opto_edge_mode(channel_num, var.get())) # Bind Combobox selection to set_opto_edge_mode
            self.opto_edge_mode_vars.append(mode_var)

            counter_label = ttk.Label(self.opto_tab, text="N/A")
            counter_label.grid(row=i+1, column=5, sticky=tk.W, padx=5, pady=2)
            self.opto_counter_labels.append(counter_label)
            reset_button = ttk.Button(self.opto_tab, text="Reset", command=lambda channel_num=i+1: self.reset_opto_counter_value(channel_num))
            reset_button.grid(row=i+1, column=6, padx=2, pady=2)

        # Encoders Section
        ttk.Label(self.opto_tab, text="Encoders", font=("Arial", 12)).grid(row=len(self.opto_input_labels)+1, column=0, columnspan=3, pady=10)
        self.opto_encoder_state_vars = [] # List to store IntVar for each encoder Enable Checkbutton
        self.opto_encoder_counter_labels = [] # List to store labels displaying encoder counter values
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
        """Creates the 'Servo/Motor' tab with sliders and displays for servo and motor control."""
        self.servo_motor_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.servo_motor_tab, text='Servo/Motor')

        # Servos Section
        ttk.Label(self.servo_motor_tab, text="Servos", font=("Arial", 12)).grid(row=0, column=0, columnspan=2, pady=10)
        self.servo_sliders = [] # List to store DoubleVar for each servo Slider
        self.servo_value_labels = [] # List to store labels displaying servo position values (%)
        for i in range(data.CHANNEL_NO["servo"]):
            ttk.Label(self.servo_motor_tab, text=f"Servo {i+1}:").grid(row=i+1, column=0, sticky=tk.W, padx=5, pady=2)
            slider_var = tk.DoubleVar()
            slider = tk.Scale(self.servo_motor_tab, from_=-140, to=140, orient=tk.HORIZONTAL, variable=slider_var, command=lambda value, channel_num=i+1: self.set_servo_position_value(channel_num, value), length=200) # Servo range -140 to 140
            slider.grid(row=i+1, column=1, padx=5, pady=2)
            self.servo_sliders.append(slider_var)
            value_label = ttk.Label(self.servo_motor_tab, text="N/A %")
            value_label.grid(row=i+1, column=2, sticky=tk.W, padx=5, pady=2)
            self.servo_value_labels.append(value_label)

        # Motor Section
        ttk.Label(self.servo_motor_tab, text="Motor", font=("Arial", 12)).grid(row=data.CHANNEL_NO["servo"] + 1, column=0, columnspan=2, pady=10)
        ttk.Label(self.servo_motor_tab, text="Motor Speed:").grid(row=data.CHANNEL_NO["servo"] + 2, column=0, sticky=tk.W, padx=5, pady=2)
        self.motor_slider_var = tk.DoubleVar()
        motor_slider = tk.Scale(self.servo_motor_tab, from_=-100, to=100, orient=tk.HORIZONTAL, variable=self.motor_slider_var, command=lambda value: self.set_motor_speed_value(value), length=200) # Motor speed range -100 to 100 (%)
        motor_slider.grid(row=data.CHANNEL_NO["servo"] + 2, column=1, padx=5, pady=2)
        self.motor_value_label = ttk.Label(self.servo_motor_tab, text="N/A %")
        self.motor_value_label.grid(row=data.CHANNEL_NO["servo"] + 2, column=2, sticky=tk.W, padx=5, pady=2)


    def create_button_tab(self):
        """Creates the 'Button' tab to display the status of the onboard button."""
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
        """
        Periodically updates the UI elements with current values from the MultiIO card.

        This function is called regularly to refresh the displayed values for
        firmware version, hardware revision, relays, LEDs, analog inputs and outputs,
        RTD values, watchdog timer information, RTC time, opto-inputs, edge counters,
        encoders, servo/motor values, and button status.
        Handles potential exceptions during data retrieval from the MultiIO card to prevent
        UI update failures and displays error messages in the console for debugging.
        """
        if self.multiio_card:
            try:
                self.update_version_info()
                self.update_relay_states()
                self.update_led_states()
                self.update_analog_inputs()
                self.update_analog_outputs_labels() # Update output labels to reflect set values
                self.update_rtd_values()
                self.update_wdt_info()
                self.update_rtc_time_label()
                self.update_opto_inputs()
                self.update_opto_counters()
                self.update_opto_encoders()
                self.update_servo_motor_values()
                self.update_button_status()
                self.update_calibration_status_label() # Update calibration status indicator

            except Exception as e:
                print(f"Error updating UI: {e}") # Print error for debugging but don't halt UI update

        self.after(100, self.update_ui_periodic) # Schedule next UI update after 100ms

    def update_calibration_status_label(self):
        """Updates the calibration status label in the Analog I/O and RTD tabs."""
        if not self.multiio_card: return
        try:
            status = self.multiio_card.calib_status() # Retrieve calibration status from MultiIO card
            status_text = "Calibrated" if status else "Not Calibrated"
            self.calib_status_var.set(status_text) # Update StringVar which updates the label text
        except Exception:
            self.calib_status_var.set("Error") # Set status to "Error" if retrieval fails

    def update_version_info(self):
        """Updates the firmware and hardware version labels in the 'Version' tab."""
        if not self.multiio_card: return
        try:
            version = self.multiio_card.get_version() # Get firmware version string
            hw_major = self.multiio_card._card_rev_major # Access hardware revision major number
            hw_minor = self.multiio_card._card_rev_minor # Access hardware revision minor number
            self.firmware_version_label.config(text=version) # Update firmware version label
            self.hardware_revision_label.config(text=f"{hw_major}.{hw_minor}") # Update hardware revision label
        except Exception:
            self.firmware_version_label.config(text="Error")
            self.hardware_revision_label.config(text="Error")

    def update_relay_states(self):
        """Updates the state of relay Checkbuttons based on current relay states from the MultiIO card."""
        if not self.multiio_card: return
        try:
            for i in range(data.CHANNEL_NO["relay"]):
                state = self.multiio_card.get_relay(i+1) # Get relay state (0 or 1)
                self.relay_vars[i].set(state) # Update corresponding Checkbutton variable
        except Exception:
            for i in range(data.CHANNEL_NO["relay"]):
                self.relay_vars[i].set(-1) # Set to -1 to indicate error state for Checkbuttons

    def update_all_relays(self):
        """Retrieves and updates the states of all relays and updates the UI."""
        if not self.multiio_card: return
        try:
            for i in range(data.CHANNEL_NO["relay"]):
                state = self.multiio_card.get_relay(i+1)
                self.relay_vars[i].set(state)
        except Exception as e:
            messagebox.showerror("Error", f"Error reading relay states: {e}")

    def update_led_states(self):
        """Updates the state of LED Checkbuttons based on current LED states from the MultiIO card."""
        if not self.multiio_card: return
        try:
            for i in range(data.CHANNEL_NO["led"]):
                state = self.multiio_card.get_led(i+1) # Get LED state (0 or 1)
                self.led_vars[i].set(state) # Update corresponding Checkbutton variable
        except Exception:
            for i in range(data.CHANNEL_NO["led"]):
                self.led_vars[i].set(-1) # Set to -1 to indicate error state for Checkbuttons

    def update_all_leds(self):
        """Retrieves and updates the states of all LEDs and updates the UI."""
        if not self.multiio_card: return
        try:
            for i in range(data.CHANNEL_NO["led"]):
                state = self.multiio_card.get_led(i+1)
                self.led_vars[i].set(state)
        except Exception as e:
            messagebox.showerror("Error", f"Error reading LED states: {e}")

    def update_analog_inputs(self):
        """Updates the labels displaying analog input values (0-10V and 4-20mA)."""
        if not self.multiio_card: return
        try:
            for i in range(data.CHANNEL_NO["u_in"]):
                value = self.multiio_card.get_u_in(i+1) # Get 0-10V input value
                self.u_in_labels[i].config(text=f"{value:.2f} V") # Update label with value, formatted to 2 decimal places
            for i in range(data.CHANNEL_NO["i_in"]):
                value = self.multiio_card.get_i_in(i+1) # Get 4-20mA input value
                self.i_in_labels[i].config(text=f"{value:.2f} mA") # Update label with value, formatted to 2 decimal places
        except Exception:
            for label in self.u_in_labels:
                label.config(text="Error")
            for label in self.i_in_labels:
                label.config(text="Error")

    def update_analog_outputs_labels(self):
        """Updates the labels displaying the set analog output values (0-10V and 4-20mA)."""
        if not self.multiio_card: return
        try:
            for i in range(data.CHANNEL_NO["u_out"]):
                value = self.multiio_card.get_u_out(i+1) # Get set 0-10V output value
                self.u_out_labels[i].config(text=f"{value:.2f} V") # Update label
            for i in range(data.CHANNEL_NO["i_out"]):
                value = self.multiio_card.get_i_out(i+1) # Get set 4-20mA output value
                self.i_out_labels[i].config(text=f"{value:.2f} mA") # Update label
        except Exception:
            for label in self.u_out_labels:
                label.config(text="Error")
            for label in self.i_out_labels:
                label.config(text="Error")

    def update_rtd_values(self):
        """Updates the labels displaying RTD temperature and resistance values."""
        if not self.multiio_card: return
        try:
            for i in range(data.CHANNEL_NO["rtd"]):
                temp = self.multiio_card.get_rtd_temp(i+1) # Get RTD temperature
                res = self.multiio_card.get_rtd_res(i+1) # Get RTD resistance
                self.rtd_temp_labels[i].config(text=f"{temp:.2f} °C") # Update temperature label
                self.rtd_res_labels[i].config(text=f"{res:.2f} Ohm") # Update resistance label
        except Exception:
            for label in self.rtd_temp_labels:
                label.config(text="Error")
            for label in self.rtd_res_labels:
                label.config(text="Error")

    def update_wdt_info(self):
        """Updates the labels and entry fields in the Watchdog tab with current WDT settings."""
        if not self.multiio_card: return
        try:
            period = self.multiio_card.wdt_get_period() # Get WDT period
            init_period = self.multiio_card.wdt_get_init_period() # Get WDT initial period
            off_period = self.multiio_card.wdt_get_off_period() # Get WDT off period
            reset_count = self.multiio_card.wdt_get_reset_count() # Get WDT reset count

            self.wdt_period_label.config(text=f"{period} sec") # Update period label
            self.wdt_init_period_label.config(text=f"{init_period} sec") # Update initial period label
            self.wdt_off_period_label.config(text=f"{off_period} sec") # Update off period label
            self.wdt_reset_count_label.config(text=str(reset_count)) # Update reset count label

            self.wdt_period_var.set(str(period)) # Update period entry field
            self.wdt_init_period_var.set(str(init_period)) # Update initial period entry field
            self.wdt_off_period_var.set(str(off_period)) # Update off period entry field

        except Exception:
            self.wdt_period_label.config(text="Error")
            self.wdt_init_period_label.config(text="Error")
            self.wdt_off_period_label.config(text="Error")
            self.wdt_reset_count_label.config(text="Error")

    def update_rtc_time_label(self):
        """Updates the RTC time label and entry fields in the RTC tab with the current time from the MultiIO card."""
        if not self.multiio_card: return
        try:
            rtc_tuple = self.multiio_card.get_rtc() # Get RTC time as a tuple (year, month, day, hour, minute, second)
            current_time_str = datetime.datetime(*rtc_tuple).strftime("%Y-%m-%d %H:%M:%S") # Format RTC tuple to string
            self.rtc_time_label.config(text=current_time_str) # Update RTC time label
            self.rtc_year_var.set(str(rtc_tuple[0])) # Update year entry field
            self.rtc_month_var.set(str(rtc_tuple[1])) # Update month entry field
            self.rtc_day_var.set(str(rtc_tuple[2])) # Update day entry field
            self.rtc_hour_var.set(str(rtc_tuple[3])) # Update hour entry field
            self.rtc_minute_var.set(str(rtc_tuple[4])) # Update minute entry field
            self.rtc_second_var.set(str(rtc_tuple[5])) # Update second entry field

        except Exception:
            self.rtc_time_label.config(text="Error")

    def update_opto_inputs(self):
        """Updates the labels displaying the state of opto-isolated inputs (ON/OFF)."""
        if not self.multiio_card: return
        try:
            for i in range(data.CHANNEL_NO["opto"]):
                state = self.multiio_card.get_opto(i+1) # Get opto-input state (0 or 1)
                self.opto_input_labels[i].config(text="ON" if state else "OFF") # Update label based on state
        except Exception:
            for label in self.opto_input_labels:
                label.config(text="Error")

    def update_opto_counters(self):
        """Updates the labels displaying opto-input edge counter values and selected edge detection modes."""
        if not self.multiio_card: return
        try:
            for i in range(data.CHANNEL_NO["opto"]):
                count = self.multiio_card.get_opto_counter(i+1) # Get opto-input edge counter value
                self.opto_counter_labels[i].config(text=str(count)) # Update counter label
                edge_mode = self.multiio_card.get_opto_edge(i+1) # Get opto-input edge detection mode
                mode_str = ["none", "rising", "falling", "both"][edge_mode] if 0 <= edge_mode <= 3 else "unknown" # Convert mode value to string
                self.opto_edge_mode_vars[i].set(mode_str) # Update corresponding Combobox variable
        except Exception:
            for label in self.opto_counter_labels:
                label.config(text="Error")

    def update_opto_encoders(self):
        """Updates the labels displaying encoder counter values and the state of encoder enable Checkbuttons."""
        if not self.multiio_card: return
        try:
            for i in range(data.CHANNEL_NO["opto_enc"]):
                count = self.multiio_card.get_opto_encoder_counter(i+1) # Get encoder counter value
                self.opto_encoder_counter_labels[i].config(text=str(count)) # Update encoder counter label
                state = self.multiio_card.get_opto_encoder_state(i+1) # Get encoder enable state (0 or 1)
                self.opto_encoder_state_vars[i].set(state) # Update encoder enable Checkbutton variable
        except Exception:
            for label in self.opto_encoder_counter_labels:
                label.config(text="Error")

    def update_servo_motor_values(self):
        """Updates the labels and sliders in the Servo/Motor tab with current servo positions and motor speed."""
        if not self.multiio_card: return
        try:
            for i in range(data.CHANNEL_NO["servo"]):
                value = self.multiio_card.get_servo(i+1) # Get servo position value (%)
                self.servo_value_labels[i].config(text=f"{value:.1f} %") # Update servo position label
                self.servo_sliders[i].set(value) # Update servo position slider

            motor_value = self.multiio_card.get_motor() # Get motor speed value (%)
            self.motor_value_label.config(text=f"{motor_value:.1f} %") # Update motor speed label
            self.motor_slider_var.set(motor_value) # Update motor speed slider
        except Exception:
            for label in self.servo_value_labels:
                label.config(text="Error")
            self.motor_value_label.config(text="Error")

    def update_button_status(self):
        """Updates the labels in the Button tab displaying button press and latch status."""
        if not self.multiio_card: return
        try:
            button_state = self.multiio_card.get_button() # Get button press state (0 or 1)
            latch_state = self.multiio_card.get_button_latch() # Get button latch state (0 or 1)
            self.button_status_label.config(text="Pressed" if button_state else "Released") # Update button status label
            self.button_latch_label.config(text="Latched" if latch_state else "Not Latched") # Update button latch label
        except Exception:
            self.button_status_label.config(text="Error")
            self.button_latch_label.config(text="Error")


    # --- Calibration Functions ---
    def calibrate_u_in_point1(self, channel_num, value_str):
        """Calibrates U_IN channel for point 1 using the provided value."""
        if not self.multiio_card: return
        try:
            value = float(value_str)
            self.multiio_card.cal_u_in(channel_num, value) # Call MultiIO card calibration function
            messagebox.showinfo("Calibration", f"U_IN {channel_num} Point 1 Calibrated with value: {value}")
            self.update_calibration_status_label() # Reflect calibration status in UI
        except ValueError:
            messagebox.showerror("Value Error", "Invalid calibration value. Please enter a number.")
        except Exception as e:
            messagebox.showerror("Error", f"Error calibrating U_IN {channel_num} Point 1: {e}")

    def calibrate_u_in_point2(self, channel_num, value_str):
        """Calibrates U_IN channel for point 2 using the provided value."""
        if not self.multiio_card: return
        try:
            value = float(value_str)
            self.multiio_card.cal_u_in(channel_num, value) # Call MultiIO card calibration function
            messagebox.showinfo("Calibration", f"U_IN {channel_num} Point 2 Calibrated with value: {value}")
            self.update_calibration_status_label() # Reflect calibration status in UI
        except ValueError:
            messagebox.showerror("Value Error", "Invalid calibration value. Please enter a number.")
        except Exception as e:
            messagebox.showerror("Error", f"Error calibrating U_IN {channel_num} Point 2: {e}")

    def calibrate_rtd_res_point1(self, channel_num, value_str):
        """Calibrates RTD resistance for point 1 using the provided resistance value."""
        if not self.multiio_card: return
        try:
            value = float(value_str)
            self.multiio_card.cal_rtd_res(channel_num, value) # Call MultiIO card calibration function
            messagebox.showinfo("Calibration", f"RTD {channel_num} Point 1 Calibrated with resistance: {value} Ohm")
            self.update_calibration_status_label() # Reflect calibration status in UI
        except ValueError:
            messagebox.showerror("Value Error", "Invalid resistance value. Please enter a number.")
        except Exception as e:
            messagebox.showerror("Error", f"Error calibrating RTD {channel_num} Point 1: {e}")

    def calibrate_rtd_res_point2(self, channel_num, value_str):
        """Calibrates RTD resistance for point 2 using the provided resistance value."""
        if not self.multiio_card: return
        try:
            value = float(value_str)
            self.multiio_card.cal_rtd_res(channel_num, value) # Call MultiIO card calibration function
            messagebox.showinfo("Calibration", f"RTD {channel_num} Point 2 Calibrated with resistance: {value} Ohm")
            self.update_calibration_status_label() # Reflect calibration status in UI
        except ValueError:
            messagebox.showerror("Value Error", "Invalid resistance value. Please enter a number.")
        except Exception as e:
            messagebox.showerror("Error", f"Error calibrating RTD {channel_num} Point 2: {e}")


    # --- Set Value Functions ---
    def set_relay_state(self, relay_num, value):
        """Sets the state of a specific relay channel (ON or OFF)."""
        if not self.multiio_card: return
        try:
            self.multiio_card.set_relay(relay_num, value) # Call MultiIO card function to set relay state
        except Exception as e:
            messagebox.showerror("Error", f"Error setting relay {relay_num}: {e}")

    def set_led_state(self, led_num, value):
        """Sets the state of a specific LED channel (ON or OFF)."""
        if not self.multiio_card: return
        try:
            self.multiio_card.set_led(led_num, value) # Call MultiIO card function to set LED state
        except Exception as e:
            messagebox.showerror("Error", f"Error setting LED {led_num}: {e}")

    def set_u_out_voltage(self, channel_num, voltage_str):
        """Sets the output voltage for a specific 0-10V analog output channel."""
        if not self.multiio_card: return
        try:
            voltage = float(voltage_str)
            if not (0 <= voltage <= 10): # Validate voltage range (0-10V)
                messagebox.showerror("Value Error", "Voltage must be between 0 and 10V.")
                return
            self.multiio_card.set_u_out(channel_num, voltage) # Call MultiIO card function to set output voltage
            self.update_analog_outputs_labels() # Update UI labels to reflect the set voltage
        except ValueError:
            messagebox.showerror("Value Error", "Invalid voltage value. Please enter a number.")
        except Exception as e:
            messagebox.showerror("Error", f"Error setting U_OUT {channel_num}: {e}")

    def set_i_out_current(self, channel_num, current_str):
        """Sets the output current for a specific 4-20mA analog output channel."""
        if not self.multiio_card: return
        try:
            current = float(current_str)
            if not (4 <= current <= 20): # Validate current range (4-20mA)
                messagebox.showerror("Value Error", "Current must be between 4 and 20mA.")
                return
            self.multiio_card.set_i_out(channel_num, current) # Call MultiIO card function to set output current
            self.update_analog_outputs_labels() # Update UI labels to reflect the set current
        except ValueError:
            messagebox.showerror("Value Error", "Invalid current value. Please enter a number.")
        except Exception as e:
            messagebox.showerror("Error", f"Error setting I_OUT {channel_num}: {e}")

    def set_wdt_period(self):
        """Sets the watchdog timer period."""
        if not self.multiio_card: return
        try:
            period = int(self.wdt_period_var.get())
            self.multiio_card.wdt_set_period(period) # Call MultiIO card function to set WDT period
            self.update_wdt_info() # Update UI to reflect the new period
        except ValueError:
            messagebox.showerror("Value Error", "Invalid period value. Please enter an integer.")
        except Exception as e:
            messagebox.showerror("Error", f"Error setting WDT period: {e}")

    def set_wdt_init_period(self):
        """Sets the watchdog timer initial period."""
        if not self.multiio_card: return
        try:
            period = int(self.wdt_init_period_var.get())
            self.multiio_card.wdt_set_init_period(period) # Call MultiIO card function to set WDT initial period
            self.update_wdt_info() # Update UI to reflect the new initial period
        except ValueError:
            messagebox.showerror("Value Error", "Invalid initial period value. Please enter an integer.")
        except Exception as e:
            messagebox.showerror("Error", f"Error setting WDT initial period: {e}")

    def set_wdt_off_period(self):
        """Sets the watchdog timer off period."""
        if not self.multiio_card: return
        try:
            period = int(self.wdt_off_period_var.get())
            self.multiio_card.wdt_set_off_period(period) # Call MultiIO card function to set WDT off period
            self.update_wdt_info() # Update UI to reflect the new off period
        except ValueError:
            messagebox.showerror("Value Error", "Invalid off period value. Please enter an integer.")
        except Exception as e:
            messagebox.showerror("Error", f"Error setting WDT off period: {e}")

    def reload_wdt(self):
        """Reloads (resets) the watchdog timer."""
        if not self.multiio_card: return
        try:
            self.multiio_card.wdt_reload() # Call MultiIO card function to reload WDT
            messagebox.showinfo("Watchdog", "Watchdog Reloaded!")
        except Exception as e:
            messagebox.showerror("Error", f"Error reloading watchdog: {e}")

    def clear_wdt_reset_count(self):
        """Clears the watchdog timer reset counter after user confirmation."""
        if not self.multiio_card: return
        confirm = messagebox.askyesno("Confirm Clear", "Are you sure you want to clear the watchdog reset count?") # Ask for user confirmation
        if confirm:
            try:
                self.multiio_card.wdt_clear_reset_count() # Call MultiIO card function to clear WDT reset count
                self.update_wdt_info() # Update UI to reflect the cleared count
            except Exception as e:
                messagebox.showerror("Error", f"Error clearing WDT reset count: {e}")

    def set_rtc_time(self):
        """Sets the Real-Time Clock time on the MultiIO card based on UI input fields."""
        if not self.multiio_card: return
        try:
            year = int(self.rtc_year_var.get())
            month = int(self.rtc_month_var.get())
            day = int(self.rtc_day_var.get())
            hour = int(self.rtc_hour_var.get())
            minute = int(self.rtc_minute_var.get())
            second = int(self.rtc_second_var.get())
            self.multiio_card.set_rtc(year, month, day, hour, minute, second) # Call MultiIO card function to set RTC time
            self.update_rtc_time() # Update UI to reflect the set time
            messagebox.showinfo("RTC", "RTC Time Set!")
        except ValueError:
            messagebox.showerror("Value Error", "Invalid RTC time values. Please enter integers.")
        except Exception as e:
            messagebox.showerror("Error", f"Error setting RTC time: {e}")

    def update_rtc_time(self):
        """Refreshes the displayed RTC time in the UI."""
        self.update_rtc_time_label() # Simply call the update label function

    def set_opto_edge_mode(self, channel_num, mode_str):
        """Sets the edge detection mode for a specific opto-input channel."""
        if not self.multiio_card: return
        mode_value = {"none": 0, "rising": 1, "falling": 2, "both": 3}.get(mode_str, 0) # Map mode string to integer value
        try:
            self.multiio_card.set_opto_edge(channel_num, mode_value) # Call MultiIO card function to set edge mode
        except Exception as e:
            messagebox.showerror("Error", f"Error setting Opto IN {channel_num} edge mode: {e}")

    def reset_opto_counter_value(self, channel_num):
        """Resets the edge counter value for a specific opto-input channel."""
        if not self.multiio_card: return
        try:
            self.multiio_card.reset_opto_counter(channel_num) # Call MultiIO card function to reset counter
            self.update_opto_counters() # Update UI to reflect the reset counter value
        except Exception as e:
            messagebox.showerror("Error", f"Error resetting Opto IN {channel_num} counter: {e}")

    def set_opto_encoder_state_value(self, channel_num, state):
        """Enables or disables a specific opto-encoder channel."""
        if not self.multiio_card: return
        try:
            self.multiio_card.set_opto_encoder_state(channel_num, state) # Call MultiIO card function to set encoder state
            self.update_opto_encoders() # Update UI to reflect the encoder state
        except Exception as e:
            messagebox.showerror("Error", f"Error setting Encoder {channel_num} state: {e}")

    def reset_opto_encoder_counter_value(self, channel_num):
        """Resets the counter value for a specific opto-encoder channel."""
        if not self.multiio_card: return
        try:
            self.multiio_card.reset_opto_encoder_counter(channel_num) # Call MultiIO card function to reset encoder counter
            self.update_opto_encoders() # Update UI to reflect the reset counter value
        except Exception as e:
            messagebox.showerror("Error", f"Error resetting Encoder {channel_num} counter: {e}")

    def set_servo_position_value(self, channel_num, value_str):
        """Sets the position of a specific servo motor channel."""
        if not self.multiio_card: return
        try:
            value = float(value_str)
            self.multiio_card.set_servo(channel_num, value) # Call MultiIO card function to set servo position
            self.update_servo_motor_values() # Update UI to reflect the set servo position
        except ValueError:
            messagebox.showerror("Value Error", "Invalid servo value. Please enter a number.")
        except Exception as e:
            messagebox.showerror("Error", f"Error setting Servo {channel_num} position: {e}")

    def set_motor_speed_value(self, value_str):
        """Sets the speed of the onboard motor."""
        if not self.multiio_card: return
        try:
            value = float(value_str)
            self.multiio_card.set_motor(value) # Call MultiIO card function to set motor speed
            self.update_servo_motor_values() # Update UI to reflect the set motor speed
        except ValueError:
            messagebox.showerror("Value Error", "Invalid motor speed value. Please enter a number.")
        except Exception as e:
            messagebox.showerror("Error", f"Error setting Motor speed: {e}")


if __name__ == "__main__":
    app = MultiIO_UI()
    app.mainloop()
