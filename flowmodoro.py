import tkinter as tk
from tkinter import messagebox, PhotoImage  
from PIL import Image, ImageTk
import pygame
import ctypes

myappid = 'flowmodoro'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

class FlowmodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Flowmodoro Timer")
        self.root.geometry("300x400")
        
        self.root.iconbitmap("icon.ico")  # Update with actual icon file path

        pygame.mixer.init()
        self.sound = pygame.mixer.Sound("ringtone-249206.mp3")
        self.sound.set_volume(0.50)

        self.work_time = 10 * 60  # 10 minutes work time
        self.break_time_factor = 5  # Break time is work time divided by this factor
        self.current_time = 0
        self.timer_running = False
        self.break_timer_running = False

        self.root.configure(bg="#181C14")
        font_color = "#EBEBEB"
        button_bg = "#3C3D37"
        button_fg = "#EBEBEB"

        try:
            self.start_icon = ImageTk.PhotoImage(Image.open("start.png").resize((40, 40)))
            self.stop_icon = ImageTk.PhotoImage(Image.open("stop.png").resize((40, 40)))
            self.reset_icon = ImageTk.PhotoImage(Image.open("reset.png").resize((40, 40)))
        except Exception as e:
            print(f"Error loading icons: {e}")
            self.start_icon = self.stop_icon = self.reset_icon = None

        self.center_frame = tk.Frame(root, bg="#181C14")
        self.center_frame.pack(expand=True)

        self.label = tk.Label(self.center_frame, text="Focus Time", font=("Helvetica", 24, "bold"), fg=font_color, bg="#181C14")
        self.label.pack(pady=20)

        self.time_display = tk.Label(self.center_frame, text=self.format_time(self.current_time), font=("Helvetica", 48, "bold"), fg=font_color, bg="#181C14")
        self.time_display.pack(pady=20)

        self.button_frame = tk.Frame(self.center_frame, bg="#181C14")
        self.button_frame.pack(pady=20)

        self.start_button = tk.Button(self.button_frame, command=self.start_timer, font=("Helvetica", 12),
                                      fg=button_fg, bg=button_bg, image=self.start_icon, compound="left",
                                      padx=10, pady=5, border=0, highlightthickness=0)
        self.start_button.grid(row=0, column=0, padx=10)

        self.stop_button = tk.Button(self.button_frame, command=self.stop_timer, font=("Helvetica", 12),
                                     fg=button_fg, bg=button_bg, image=self.stop_icon, compound="left",
                                     padx=10, pady=5, border=0, highlightthickness=0)
        self.stop_button.grid(row=0, column=1, padx=10)
        self.stop_button.config(state="disabled")

        self.reset_button = tk.Button(self.button_frame, command=self.reset_timer, font=("Helvetica", 12),
                                      fg=button_fg, bg=button_bg, image=self.reset_icon, compound="left",
                                      padx=10, pady=5, border=0, highlightthickness=0)
        self.reset_button.grid(row=0, column=2, padx=10)

    def format_time(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        return f"{minutes:02}:{seconds:02}"

    def count_up(self):
        if self.timer_running:
            self.time_display.config(text=self.format_time(self.current_time))
            self.current_time += 1
            self.root.after(1000, self.count_up)

    def start_timer(self):
        if not self.timer_running and not self.break_timer_running:
            self.timer_running = True
            self.current_time = 0
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            self.label.config(text="Focus Time")
            self.count_up()

    def start_break(self, break_duration):
        self.break_time = break_duration
        self.break_timer_running = True
        self.label.config(text="Break Time")
        self.run_break_timer()

    def run_break_timer(self):
        if self.break_timer_running and self.break_time >= 0:
            self.time_display.config(text=self.format_time(self.break_time))
            self.break_time -= 1
            self.root.after(1000, self.run_break_timer)
        elif self.break_timer_running and self.break_time < 0:
            self.end_break_period()

    def end_break_period(self):
        self.break_timer_running = False
        self.sound.play()
        self.start_button.config(state="normal")
        self.label.config(text="Focus Time")

    def stop_timer(self):
        if self.timer_running:
            self.timer_running = False
            elapsed_time = self.current_time
            break_time = elapsed_time // self.break_time_factor
            self.start_break(break_time)

    def reset_timer(self):
        self.timer_running = False
        self.break_timer_running = False
        self.current_time = 0
        self.break_time = 0
        self.time_display.config(text=self.format_time(self.current_time))
        self.label.config(text="Focus Time")
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.root.after_cancel(self.count_up)

if __name__ == "__main__":
    root = tk.Tk()
    timer_app = FlowmodoroTimer(root)
    root.mainloop()
