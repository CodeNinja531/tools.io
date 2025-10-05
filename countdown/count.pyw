import tkinter as tk
from datetime import datetime
import webbrowser

def countdown():
    target_time = datetime(2026, 4, 8, 8, 30, 0) # 8th of April: Art 1 & 2
    now = datetime.now()
    remaining = target_time - now

    # Check if the target time has passed
    if remaining.total_seconds() <= 0:
        # If time is up or passed, display all zeros
        days = 0
        hours = 0
        minutes = 0
        seconds = 0
    else:
        # Calculate remaining time as usual
        days = remaining.days
        hours, remainder = divmod(remaining.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
    
    # Update the label with the formatted time
    label.config(text=f"{days} days {hours:02d}h {minutes:02d}m {seconds:02d}s")
    
    # Continue the countdown if there's still time remaining, or if it's 0 to keep displaying zeros
    if remaining.total_seconds() > 0:
        label.after(1000, countdown)
    # If total_seconds is 0 or less, we stop calling countdown() after this update.
    # The label will remain showing "0 days 00h 00m 00s".


def open_schedule():
    """Opens the DSE timetable PDF in the default web browser."""
    url = "https://www.hkeaa.edu.hk/doclibrary/hkdse/exam_timetable/2026_dse_timetable.pdf"
    webbrowser.open_new(url)

root = tk.Tk()
root.title("2026 DSE Countdown")

label = tk.Label(root, text="", font=("Helvetica", 24))
label.pack(padx=20, pady=2)

schedule_button = tk.Button(root, text="Timetable", command=open_schedule)
schedule_button.pack(pady=10)

countdown()

root.mainloop()