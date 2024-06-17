import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import schedule
import time
import threading
import pygame
import json

class SchoolBellRingerApp:
    def __init__(self, master):
        # Initialize pygame mixer
        pygame.mixer.init()

        self.master = master
        self.master.title("School Bell Ringer")
        self.master.geometry("600x400")
        self.master.resizable(True, True)

        # Colors
        self.background_color = "#f0f0f0"
        self.foreground_color = "#333333"
        self.highlight_color = "#4682b4"

        # Initialize variables
        self.schedule = []
        self.current_period = None

        # Create GUI elements
        self.create_widgets()

        # Load schedule data from JSON file
        self.load_schedule()

        # Start the scheduler in a background thread
        self.scheduler_thread = threading.Thread(target=self.run_scheduler)
        self.scheduler_thread.daemon = True
        self.scheduler_thread.start()

    def create_widgets(self):
        # Set background color
        self.master.configure(bg=self.background_color)

        # Frame for adding schedule
        self.frame_add_schedule = ttk.LabelFrame(self.master, text="Add Schedule", relief=tk.RIDGE)
        self.frame_add_schedule.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        # Day select box
        ttk.Label(self.frame_add_schedule, text="Day:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.day_select = ttk.Combobox(self.frame_add_schedule, values=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        self.day_select.grid(row=0, column=1, padx=5, pady=5)
        self.day_select.current(0)  # Default to Monday

        # Time select box
        ttk.Label(self.frame_add_schedule, text="Time:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.time_select = ttk.Combobox(self.frame_add_schedule, values=self.get_time_options())
        self.time_select.grid(row=1, column=1, padx=5, pady=5)

        # Sound upload button
        self.sound_button = ttk.Button(self.frame_add_schedule, text="Upload Sound", command=self.upload_sound)
        self.sound_button.grid(row=1, column=2, padx=5, pady=5)

        # List box to display schedule
        self.schedule_listbox = tk.Listbox(self.frame_add_schedule, width=50, height=10)
        self.schedule_listbox.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

        # Edit, Delete, and Save buttons
        self.edit_button = ttk.Button(self.frame_add_schedule, text="Edit", command=self.edit_schedule, style="Highlight.TButton")
        self.edit_button.grid(row=3, column=0, padx=5, pady=5, sticky="ew")
        self.delete_button = ttk.Button(self.frame_add_schedule, text="Delete", command=self.delete_schedule, style="Highlight.TButton")
        self.delete_button.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        self.save_button = ttk.Button(self.frame_add_schedule, text="Save", command=self.save_schedule, style="Highlight.TButton")
        self.save_button.grid(row=3, column=2, padx=5, pady=5, sticky="ew")

        # Apply custom styles
        self.apply_styles()

    def apply_styles(self):
        self.master.option_add("*TCombobox*Listbox*foreground", self.foreground_color)
        self.master.option_add("*TCombobox*Listbox*background", self.background_color)
        self.master.option_add("*TEntry*foreground", self.foreground_color)
        self.master.option_add("*TEntry*background", self.background_color)
        self.master.option_add("*TButton*foreground", "#FFFFFF")
        self.master.option_add("*TButton*background", self.highlight_color)
        self.master.option_add("*TButton*font", ("Arial", 10, "bold"))

    def get_time_options(self):
        # Generate time options for combobox
        time_options = []
        for hour in range(24):
            for minute in range(0, 60, 5):
                time_options.append(f"{hour:02d}:{minute:02d}")
        return time_options

    def upload_sound(self):
        # Open file dialog to select sound file
        sound_file = filedialog.askopenfilename()
        if sound_file:
            messagebox.showinfo("Sound Uploaded", f"Sound file '{sound_file}' uploaded successfully.")
            self.sound_file = sound_file

    def save_schedule(self):
        # Get the selected day, time, and sound
        day = self.day_select.get()
        time = self.time_select.get()
        sound = getattr(self, 'sound_file', '')

        # Add new schedule item to the list
        self.schedule.append({"day": day, "time": time, "sound": sound})

        # Save schedule to JSON file
        with open("schedule.json", "w") as file:
            json.dump(self.schedule, file)
        messagebox.showinfo("Schedule Saved", "Schedule saved successfully.")
        self.update_schedule_listbox()  # Update the listbox with the new schedule

    def load_schedule(self):
        # Load schedule data from JSON file
        try:
            with open("schedule.json", "r") as file:
                self.schedule = json.load(file)
        except FileNotFoundError:
            messagebox.showwarning("File Not Found", "No schedule file found. Starting with empty schedule.")
        print("Schedule data loaded:", self.schedule)  # Debug print
        self.update_schedule_listbox()

    def update_schedule_listbox(self):
        # Update schedule list box
        self.schedule_listbox.delete(0, tk.END)
        for item in self.schedule:
            self.schedule_listbox.insert(tk.END, f"Day: {item['day']}, Time: {item['time']}, Sound: {item['sound']}")

    def edit_schedule(self):
        # Edit selected schedule
        selected_index = self.schedule_listbox.curselection()
        if selected_index:
            selected_item = self.schedule[selected_index[0]]
            self.edit_window = tk.Toplevel(self.master)
            self.edit_window.title("Edit Schedule")

            ttk.Label(self.edit_window, text="Day:", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="e")
            day_var = tk.StringVar(value=selected_item["day"])
            day_entry = ttk.Combobox(self.edit_window, values=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], textvariable=day_var)
            day_entry.grid(row=0, column=1, padx=5, pady=5)

            ttk.Label(self.edit_window, text="Time:", font=("Arial", 12, "bold")).grid(row=1, column=0, padx=5, pady=5, sticky="e")
            time_var = tk.StringVar(value=selected_item["time"])
            time_entry = ttk.Combobox(self.edit_window, values=self.get_time_options(), textvariable=time_var)
            time_entry.grid(row=1, column=1, padx=5, pady=5)

            ttk.Label(self.edit_window, text="Sound:", font=("Arial", 12, "bold")).grid(row=2, column=0, padx=5, pady=5, sticky="e")
            sound_var = tk.StringVar(value=selected_item["sound"])
            sound_entry = ttk.Entry(self.edit_window, textvariable=sound_var)
            sound_entry.grid(row=2, column=1, padx=5, pady=5)

            save_button = ttk.Button(self.edit_window, text="Save", command=lambda: self.save_edit(selected_index[0], day_entry.get(), time_entry.get(), sound_entry.get()), style="Highlight.TButton")
            save_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

    def save_edit(self, index, day, time, sound):
        self.schedule[index] = {"day": day, "time": time, "sound": sound}
        self.edit_window.destroy()
        self.update_schedule_listbox()

    def delete_schedule(self):
        # Delete selected schedule
        selected_index = self.schedule_listbox.curselection()
        if selected_index:
            self.schedule.pop(selected_index[0])
            self.update_schedule_listbox()

    def run_scheduler(self):
        # Main scheduler loop
        while True:
            current_time = time.strftime("%H:%M")
            current_day = time.strftime("%A")
            for item in self.schedule:
                if current_time == item["time"] and current_day == item["day"] and item["time"] != self.current_period:
                    self.current_period = item["time"]
                    self.trigger_bell_ring(item["time"], item["sound"])
            time.sleep(10)  # Check every 10 seconds

    def trigger_bell_ring(self, time, sound):
        # Load and play the sound file
        pygame.mixer.music.load(sound)
        pygame.mixer.music.play()
        # Placeholder for bell ringing code
        messagebox.showinfo("Bell Ringing", f"Bell ringing at {time}. Sound file: {sound}")


def main():
    root = tk.Tk()
    app = SchoolBellRingerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
