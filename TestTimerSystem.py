import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import time
from playsound import playsound

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Timer")

        # Load settings
        self.load_settings()

        self.timers = []  # List to store timer information (name, end_time, is_running, alarm_sound)
        self.current_timer_index = None  # Index of the currently active timer

        # Alarm sound options
        self.alarm_options = ["None", "beep.wav", "bell.wav"]

        # Create and configure widgets
        self.create_widgets()

    def load_settings(self):
        # Load settings from a file or default values
        self.settings = {"always_on_top": False, "dark_mode": False}  # Default values

        try:
            with open("settings.txt", "r") as file:
                for line in file:
                    key, value = line.strip().split(":")
                    if key in self.settings:
                        self.settings[key] = bool(int(value))
        except FileNotFoundError:
            # Settings file does not exist, use default values
            pass

        self.apply_settings()

    def save_settings(self):
        # Save settings to a file
        with open("settings.txt", "w") as file:
            for key, value in self.settings.items():
                file.write(f"{key}:{int(value)}\n")

    def apply_settings(self):
        # Apply settings to the application
        if self.settings["always_on_top"]:
            self.root.attributes("-topmost", True)
        else:
            self.root.attributes("-topmost", False)

        if self.settings["dark_mode"]:
            self.apply_dark_mode()

    def create_widgets(self):
        # Timer input
        timer_frame = ttk.Frame(self.root)
        timer_frame.pack(pady=10)

        ttk.Label(timer_frame, text="Timer Name:").grid(row=0, column=0, padx=5)
        self.timer_name_var = tk.StringVar()
        ttk.Entry(timer_frame, textvariable=self.timer_name_var, width=20).grid(row=0, column=1)

        ttk.Label(timer_frame, text="Hours:").grid(row=0, column=2, padx=5)
        self.hours_var = tk.StringVar(value="0")
        ttk.Entry(timer_frame, textvariable=self.hours_var, width=5).grid(row=0, column=3)

        ttk.Label(timer_frame, text="Minutes:").grid(row=0, column=4, padx=5)
        self.minutes_var = tk.StringVar(value="0")
        ttk.Entry(timer_frame, textvariable=self.minutes_var, width=5).grid(row=0, column=5)

        ttk.Label(timer_frame, text="Seconds:").grid(row=0, column=6, padx=5)
        self.seconds_var = tk.StringVar(value="0")
        ttk.Entry(timer_frame, textvariable=self.seconds_var, width=5).grid(row=0, column=7)

        # Alarm sound dropdown
        ttk.Label(timer_frame, text="Alarm Sound:").grid(row=0, column=8, padx=5)
        alarm_menu = ttk.Combobox(timer_frame, values=self.alarm_options, state="readonly")
        alarm_menu.grid(row=0, column=9)
        alarm_menu.set("None")  # Default to "None"
        self.alarm_menu = alarm_menu

        # Options button
        ttk.Button(timer_frame, text="Options", command=self.open_options).grid(row=0, column=10, padx=5)

        # Buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Start Timer", command=self.start_timer).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Stop Timer", command=self.stop_timer).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Show Timers", command=self.show_timers).grid(row=0, column=2, padx=5)

    def start_timer(self):
        # Validate timer input
        timer_name = self.timer_name_var.get()
        hours = int(self.hours_var.get())
        minutes = int(self.minutes_var.get())
        seconds = int(self.seconds_var.get())
        alarm_sound = self.alarm_menu.get()

        if hours == minutes == seconds == 0:
            messagebox.showwarning("Invalid Timer", "Timer duration cannot be zero.")
            return

        end_time = time.time() + hours * 3600 + minutes * 60 + seconds

        # Check if a timer with the same name is already running
        for index, timer in enumerate(self.timers):
            if timer[0] == timer_name and timer[2]:
                messagebox.showwarning("Timer Already Running", f"A timer with the name '{timer_name}' is already running.")
                return

        # Create a new timer
        self.timers.append([timer_name, end_time, True, alarm_sound])

        # Notify user when the timer ends
        self.root.after(int((end_time - time.time()) * 1000), lambda timer_name=timer_name, index=len(self.timers)-1: self.timer_notification(timer_name, index))

    def stop_timer(self):
        # Validate timer input
        timer_name = self.timer_name_var.get()

        # Stop the timer if it is running
        for index, timer in enumerate(self.timers):
            if timer[0] == timer_name and timer[2]:
                self.timers[index][2] = False
                messagebox.showinfo("Timer Stopped", f"The timer '{timer_name}' has been stopped.")
                return

        # Display a message if the timer is not found
        messagebox.showwarning("Timer Not Found", f"No running timer found with the name '{timer_name}'.")

    def show_timers(self):
        # Display a list of running timers along with the remaining time
        ShowTimersDialog(self.root, self.timers)

    def timer_notification(self, timer_name, index):
        # Notify user when the timer ends
        alarm_sound = self.timers[index][3]
        if alarm_sound != "None":
            playsound(alarm_sound)  # You can customize this to your preferred notification sound
        messagebox.showinfo("Timer Ended", f"The timer '{timer_name}' has ended.")

        # Remove the timer from the list
        self.timers[index][2] = False

    def open_options(self):
        OptionsDialog(self.root, self.settings, self.apply_settings, self.save_settings)

    def apply_dark_mode(self):
        # Apply dark mode to the main window or other widgets as needed
        self.root.configure(bg="black")
        self.root.option_add("*TButton*background", "black")  # Example for TButton background
        self.root.option_add("*TButton*foreground", "white")  # Example for TButton foreground
        self.root.option_add("*TButton*highlightColor", "black")  # Example for TButton highlight color

        # Apply dark mode to specific buttons
        self.root.option_add("*TButton.dark_mode.TButton*background", "dark gray")
        self.root.option_add("*TButton.dark_mode.TButton*foreground", "white")
        self.root.option_add("*TButton.dark_mode.TButton*highlightColor", "dark gray")

        # Change buttons to dark mode
        self.change_button_style(self.root.winfo_children(), "dark_mode")

    def change_button_style(self, widgets, style):
        for widget in widgets:
            if isinstance(widget, tk.Button) and "dark_mode" in widget.winfo_class():
                widget.configure(style=style)
            self.change_button_style(widget.winfo_children(), style)

class OptionsDialog(simpledialog.Dialog):
    def __init__(self, parent, settings, apply_settings, save_settings):
        self.settings = settings
        self.apply_settings = apply_settings
        self.save_settings = save_settings
        super().__init__(parent)

    def body(self, master):
        ttk.Label(master, text="Options").pack()

        # Dark mode checkbox
        self.dark_mode_var = tk.BooleanVar(value=self.settings["dark_mode"])
        ttk.Checkbutton(master, text="Dark Mode", variable=self.dark_mode_var).pack()

        # Always on top checkbox
        self.always_on_top_var = tk.BooleanVar(value=self.settings["always_on_top"])
        ttk.Checkbutton(master, text="Always on Top", variable=self.always_on_top_var).pack()

        return master

    def apply(self):
        # Retrieve selected options
        dark_mode = self.dark_mode_var.get()
        always_on_top = self.always_on_top_var.get()

        # Apply options
        self.settings["dark_mode"] = dark_mode
        self.settings["always_on_top"] = always_on_top
        self.apply_settings()
        self.save_settings()

    def change_button_style(self, widgets, style):
        for widget in widgets:
            if isinstance(widget, tk.Button) and "dark_mode" in widget.winfo_class():
                widget.configure(style=style)
            self.change_button_style(widget.winfo_children(), style)

class ShowTimersDialog(simpledialog.Dialog):
    def __init__(self, parent, timers):
        self.timers = timers
        super().__init__(parent)

    def body(self, master):
        ttk.Label(master, text="Running Timers").pack()

        self.timer_labels = []

        # Create labels for each timer
        for timer_info in self.get_running_timers_info():
            label = ttk.Label(master, text=timer_info)
            label.pack()
            self.timer_labels.append(label)

        return master

    def update_timers(self):
        # Update timer labels with remaining time
        for label, timer_info in zip(self.timer_labels, self.get_running_timers_info()):
            label.config(text=timer_info)

    def get_running_timers_info(self):
        # Get information about running timers
        running_timers_info = []
        current_time = time.time()

        for timer in self.timers:
            if timer[2]:
                remaining_time = max(0, timer[1] - current_time)
                hours, remainder = divmod(remaining_time, 3600)
                minutes, seconds = divmod(remainder, 60)
                remaining_time_str = "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))
                running_timers_info.append(f"{timer[0]} - {remaining_time_str}")

        return running_timers_info

    def update_after(self):
        # Schedule the next update
        self.after(1000, self.update_after)
        # Update timer labels
        self.update_timers()

    def show(self):
        # Override show method to start the update loop
        super().show()
        self.update_after()

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
