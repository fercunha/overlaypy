import tkinter as tk
import ctypes
import platform
from screeninfo import get_monitors

class OverlayApp:
    def __init__(self, master):
        self.master = master
        master.title("Overlay Controller")
        master.geometry("400x350")
        master.attributes("-topmost", True)  # Keep main window always on top

        # --- Message Input ---
        tk.Label(master, text="Message:", font=("Arial", 12, "bold")).pack(pady=(10, 2))
        self.entry = tk.Entry(master, width=40, font=("Arial", 14))
        self.entry.pack(padx=10, pady=(0, 10))
        self.entry.insert(0, "Your message here...")

        # --- Padding Input ---
        tk.Label(master, text="Padding (pixels):", font=("Arial", 12, "bold")).pack(pady=(10, 2))
        self.padding_entry = tk.Entry(master, width=10, font=("Arial", 14))
        self.padding_entry.pack(padx=10, pady=(0, 10))
        self.padding_entry.insert(0, "40")

        # --- Timer Settings ---
        timer_frame = tk.Frame(master)
        timer_frame.pack(pady=(10, 10))
        
        self.timer_enabled = tk.BooleanVar(value=True)
        self.timer_checkbox = tk.Checkbutton(timer_frame, text="Auto-hide after", 
                                           variable=self.timer_enabled, font=("Arial", 11))
        self.timer_checkbox.pack(side=tk.LEFT)
        
        self.timer_entry = tk.Entry(timer_frame, width=5, font=("Arial", 12))
        self.timer_entry.pack(side=tk.LEFT, padx=(5, 2))
        self.timer_entry.insert(0, "60")
        
        tk.Label(timer_frame, text="seconds", font=("Arial", 11)).pack(side=tk.LEFT)

        # --- Monitor Selection ---
        tk.Label(master, text="Select Monitor:", font=("Arial", 12, "bold")).pack(pady=(10, 2))
        self.monitors = get_monitors()
        self.monitor_var = tk.StringVar(master)
        
        # Create monitor names for dropdown
        monitor_names = []
        for i, monitor in enumerate(self.monitors):
            if hasattr(monitor, 'name') and monitor.name:
                monitor_names.append(f"{monitor.name} ({monitor.width}x{monitor.height})")
            else:
                monitor_names.append(f"Monitor {i+1} ({monitor.width}x{monitor.height})")
        
        self.monitor_var.set(monitor_names[0])
        self.monitor_menu = tk.OptionMenu(master, self.monitor_var, *monitor_names)
        self.monitor_menu.config(width=35)
        self.monitor_menu.pack(pady=(0, 15))

        # --- Buttons ---
        self.toggle_btn = tk.Button(master, text="Show Overlay", font=("Arial", 12, "bold"),
                                    bg="lightgreen", fg="black", command=self.toggle_overlay)
        self.toggle_btn.pack(pady=5)

        self.quit_btn = tk.Button(master, text="Quit", font=("Arial", 12),
                                  bg="lightcoral", fg="black", command=master.quit)
        self.quit_btn.pack(pady=5)

        # Overlay state
        self.overlay = None
        self.overlay_visible = False
        self.timer_job = None  # Store timer job reference

    def toggle_overlay(self):
        if self.overlay_visible:
            self.hide_overlay()
        else:
            self.show_overlay()

    def auto_hide_overlay(self):
        """Called by timer to automatically hide overlay"""
        self.hide_overlay()

    def show_overlay(self):
        # Find the selected monitor by matching the dropdown selection
        selected_monitor = None
        selected_text = self.monitor_var.get()
        
        for i, monitor in enumerate(self.monitors):
            if hasattr(monitor, 'name') and monitor.name:
                monitor_name = f"{monitor.name} ({monitor.width}x{monitor.height})"
            else:
                monitor_name = f"Monitor {i+1} ({monitor.width}x{monitor.height})"
            
            if monitor_name == selected_text:
                selected_monitor = monitor
                break
        
        if selected_monitor is None:
            selected_monitor = self.monitors[0]

        if self.overlay is None:
            self.overlay = tk.Toplevel(self.master)
            self.overlay.overrideredirect(True)
            self.overlay.attributes("-topmost", True)
            self.overlay.configure(bg="black")

            # Label (BOLD, WHITE on BLACK)
            self.label = tk.Label(
                self.overlay,
                text=self.entry.get(),
                font=("Arial", 36, "bold"),
                fg="white",
                bg="black"
            )
            
            # Get padding from user input
            try:
                padding = int(self.padding_entry.get())
            except ValueError:
                padding = 40  # default padding if invalid input
                
            self.label.pack(padx=padding, pady=padding)

        # Update text and padding
        self.label.config(text=self.entry.get())
        
        # Get current padding value
        try:
            padding = int(self.padding_entry.get())
        except ValueError:
            padding = 40
            
        # Update padding
        self.label.pack_configure(padx=padding, pady=padding)
        
        # Calculate size based on text content and padding
        self.overlay.update_idletasks()  # Force update to get accurate measurements
        req_width = self.label.winfo_reqwidth() + (padding * 2)
        req_height = self.label.winfo_reqheight() + (padding * 2)
        
        # Position overlay in bottom-left corner of selected monitor
        x_pos = selected_monitor.x + 20  # 20px margin from left edge
        y_pos = selected_monitor.y + selected_monitor.height - req_height - 20  # 20px margin from bottom
        
        self.overlay.geometry(f"{req_width}x{req_height}+{x_pos}+{y_pos}")
        self.overlay.deiconify()

        # Make overlay click-through (Windows only)
        if platform.system() == "Windows":
            hwnd = ctypes.windll.user32.GetParent(self.overlay.winfo_id())
            style = ctypes.windll.user32.GetWindowLongW(hwnd, -20)
            ctypes.windll.user32.SetWindowLongW(hwnd, -20, style | 0x80000 | 0x20)

        self.overlay_visible = True
        self.toggle_btn.config(text="Hide Overlay", bg="orange", fg="black")
        
        # Set up auto-hide timer if enabled
        if self.timer_enabled.get():
            try:
                timer_seconds = int(self.timer_entry.get())
                if timer_seconds > 0:
                    # Cancel any existing timer
                    if self.timer_job:
                        self.master.after_cancel(self.timer_job)
                    # Set new timer
                    self.timer_job = self.master.after(timer_seconds * 1000, self.auto_hide_overlay)
            except ValueError:
                pass  # Invalid timer value, skip timer

    def hide_overlay(self):
        # Cancel any pending timer
        if self.timer_job:
            self.master.after_cancel(self.timer_job)
            self.timer_job = None
            
        if self.overlay:
            self.overlay.withdraw()
        self.overlay_visible = False
        self.toggle_btn.config(text="Show Overlay", bg="lightgreen", fg="black")


if __name__ == "__main__":
    root = tk.Tk()
    app = OverlayApp(root)
    root.mainloop()
