# Source: Copilot.microsoft.com
# Prompt: 
# I'm creating a chess timer in Python using tkinter. The timer will display two clocks, a left clock and a right clock, that show hours, minutes and seconds. There will be three operating modes. The first operating mode is that the left clock is counting down to zero from a preset time, and the right clock does not count down. The second operating mode is that the right clock is counting down to zero from a preset time and the left clock does not count down. The third operating mode is that neither of the clocks are running. The timer needs three buttons. The first button, the "left" button, starts the right clock and stops the left clock. This is the second operating mode. The second button, the "right" button, starts the left clock and stops the right clock. This is the first operating mode. The third button, the "pause" button stops both clocks. This is the third operating mode. When either of the clocks gets to zero time, the clocks stop counting down. Please show me the code to do this.

import tkinter as tk

class ChessTimer:
    def __init__(self, master, preset_time=300):
        """
        Creates two clocks (left and right) counting down from a preset_time (in seconds).
        Initially both clocks are paused.
        """
        self.master = master
        self.preset_time = preset_time
        self.left_time = preset_time
        self.right_time = preset_time

        # Flags indicating whether a particular clock is running
        self.left_running = False
        self.right_running = False

        # Holds the job ID for after() so that it can be cancelled if necessary.
        self.job = None

        self.create_widgets()

    def create_widgets(self):
        """Create and layout the labels and buttons."""
        # Display labels for the two clocks
        self.left_label = tk.Label(self.master,
                                   text=self.format_time(self.left_time),
                                   font=("Helvetica", 32))
        self.left_label.grid(row=0, column=0, padx=20, pady=20)

        self.right_label = tk.Label(self.master,
                                    text=self.format_time(self.right_time),
                                    font=("Helvetica", 32))
        self.right_label.grid(row=0, column=1, padx=20, pady=20)

        # The "Left" button will start the right clock
        self.left_button = tk.Button(self.master,
                                     text="Left",
                                     font=("Helvetica", 20),
                                     command=self.start_right_clock)
        self.left_button.grid(row=1, column=0, padx=20, pady=20)

        # The "Right" button will start the left clock
        self.right_button = tk.Button(self.master,
                                      text="Right",
                                      font=("Helvetica", 20),
                                      command=self.start_left_clock)
        self.right_button.grid(row=1, column=1, padx=20, pady=20)

        # The "Pause" button stops both clocks.
        self.pause_button = tk.Button(self.master,
                                      text="Pause",
                                      font=("Helvetica", 20),
                                      command=self.pause_timers)
        self.pause_button.grid(row=2, column=0, columnspan=2, pady=20)

    def format_time(self, seconds):
        """Return a string formatted as HH:MM:SS given a number of seconds."""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    def update_timers(self):
        """
        Update each clock if it is running. If a clock’s time reaches 0, turn off its running flag.
        Then update the labels, and if at least one clock is running, schedule the next update.
        """
        # Update left clock if it is running and has time remaining
        if self.left_running and self.left_time > 0:
            self.left_time -= 1
            if self.left_time == 0:
                self.left_running = False

        # Update right clock if it is running and has time remaining
        if self.right_running and self.right_time > 0:
            self.right_time -= 1
            if self.right_time == 0:
                self.right_running = False

        # Update the display labels
        self.left_label.config(text=self.format_time(self.left_time))
        self.right_label.config(text=self.format_time(self.right_time))
        
        # Schedule the next update if either clock is still running
        if self.left_running or self.right_running:
            self.job = self.master.after(1000, self.update_timers)
        else:
            self.job = None

    def start_left_clock(self):
        """
        This method is linked to the "Right" button. It starts the left clock (first operating mode)
        while stopping the right clock.
        """
        self.left_running = True
        self.right_running = False

        # If no update is scheduled, start the timer updates.
        if self.job is None:
            self.job = self.master.after(1000, self.update_timers)

    def start_right_clock(self):
        """
        This method is linked to the "Left" button. It starts the right clock (second operating mode)
        while stopping the left clock.
        """
        self.right_running = True
        self.left_running = False

        if self.job is None:
            self.job = self.master.after(1000, self.update_timers)

    def pause_timers(self):
        """
        This method stops both clocks (third operating mode).
        It cancels any scheduled updates.
        """
        self.left_running = False
        self.right_running = False

        if self.job is not None:
            self.master.after_cancel(self.job)
            self.job = None

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Chess Timer")
    # Create a chess timer with the preset countdown time (here 5 minutes = 300 seconds)
    timer = ChessTimer(root, preset_time=300)
    root.mainloop()
