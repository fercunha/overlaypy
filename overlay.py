import tkinter as tk
from tkinter import ttk
import ctypes
import platform
from screeninfo import get_monitors

class OverlayApp:
    def __init__(self, master):
        self.master = master
        master.title("Overlay Controller")
        master.geometry("450x500")
        master.attributes("-topmost", True)  # Keep main window always on top

        # Create main frame with scrollbar
        main_frame = tk.Frame(master)
        main_frame.pack(fill=tk.BOTH, expand=1)

        # Create canvas and scrollbar
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        # Configure canvas
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind mousewheel to canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Use scrollable_frame as the parent for all widgets
        container = scrollable_frame

        # --- Message Input ---
        tk.Label(container, text="Message:", font=("Arial", 12, "bold")).pack(pady=(10, 2))
        self.entry = tk.Entry(container, width=40, font=("Arial", 14))
        self.entry.pack(padx=10, pady=(0, 10))
        self.entry.insert(0, "Your message here...")

        # --- Controls Row (Font Size, Position, Padding side by side) ---
        controls_frame = tk.Frame(container)
        controls_frame.pack(pady=(10, 10), padx=20, fill=tk.X)

        # Font Size Column
        font_col = tk.Frame(controls_frame)
        font_col.pack(side=tk.LEFT, padx=(0, 15), fill=tk.X, expand=True)
        tk.Label(font_col, text="Font Size:", font=("Arial", 11, "bold")).pack()
        self.font_size_var = tk.StringVar(container)
        font_sizes = ["12", "18", "24", "30", "36", "42", "48", "60", "72", "84", "96", "120", "144", "168", "192", "216", "240"]
        self.font_size_var.set("36")  # Default font size
        self.font_size_menu = tk.OptionMenu(font_col, self.font_size_var, *font_sizes, command=self.on_setting_change)
        self.font_size_menu.config(width=8)
        self.font_size_menu.pack(fill=tk.X)

        # Position Column  
        position_col = tk.Frame(controls_frame)
        position_col.pack(side=tk.LEFT, padx=(0, 15), fill=tk.X, expand=True)
        tk.Label(position_col, text="Position:", font=("Arial", 11, "bold")).pack()
        self.corner_var = tk.StringVar(container)
        corners = ["Bottom Left", "Bottom Right", "Top Left", "Top Right"]
        self.corner_var.set("Bottom Left")  # Default position
        self.corner_menu = tk.OptionMenu(position_col, self.corner_var, *corners, command=self.on_setting_change)
        self.corner_menu.config(width=10)
        self.corner_menu.pack(fill=tk.X)

        # Padding Column
        padding_col = tk.Frame(controls_frame)
        padding_col.pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Label(padding_col, text="Padding (px):", font=("Arial", 11, "bold")).pack()
        self.padding_entry = tk.Entry(padding_col, width=8, font=("Arial", 12), justify='center')
        self.padding_entry.pack(fill=tk.X)
        self.padding_entry.insert(0, "40")
        # Bind real-time updates for padding
        self.padding_entry.bind('<KeyRelease>', self.on_setting_change)

        # --- Timer Settings ---
        timer_frame = tk.Frame(container)
        timer_frame.pack(pady=(10, 10))
        
        self.timer_enabled = tk.BooleanVar(value=True)
        self.timer_checkbox = tk.Checkbutton(timer_frame, text="Auto-hide after", 
                                           variable=self.timer_enabled, font=("Arial", 11),
                                           command=self.on_timer_change)
        self.timer_checkbox.pack(side=tk.LEFT)
        
        self.timer_entry = tk.Entry(timer_frame, width=5, font=("Arial", 12))
        self.timer_entry.pack(side=tk.LEFT, padx=(5, 2))
        self.timer_entry.insert(0, "60")
        # Bind real-time updates for timer
        self.timer_entry.bind('<KeyRelease>', self.on_timer_change)
        
        tk.Label(timer_frame, text="seconds", font=("Arial", 11)).pack(side=tk.LEFT)

        # --- Monitor Selection ---
        tk.Label(container, text="Select Monitor:", font=("Arial", 12, "bold")).pack(pady=(10, 2))
        self.monitors = get_monitors()
        self.monitor_var = tk.StringVar(container)
        
        # Create monitor names for dropdown
        monitor_names = []
        for i, monitor in enumerate(self.monitors):
            if hasattr(monitor, 'name') and monitor.name:
                monitor_names.append(f"{monitor.name} ({monitor.width}x{monitor.height})")
            else:
                monitor_names.append(f"Monitor {i+1} ({monitor.width}x{monitor.height})")
        
        self.monitor_var.set(monitor_names[0])
        self.monitor_menu = tk.OptionMenu(container, self.monitor_var, *monitor_names, command=self.on_setting_change)
        self.monitor_menu.config(width=35)
        self.monitor_menu.pack(pady=(0, 15))

        # --- Buttons ---
        self.toggle_btn = tk.Button(container, text="Show Overlay", font=("Arial", 12, "bold"),
                                    bg="lightgreen", fg="black", command=self.toggle_overlay)
        self.toggle_btn.pack(pady=5)

        self.quit_btn = tk.Button(container, text="Quit", font=("Arial", 12),
                                  bg="lightcoral", fg="black", command=master.quit)
        self.quit_btn.pack(pady=(5, 20))  # Extra bottom padding

        # Overlay state
        self.overlay = None
        self.overlay_visible = False
        self.timer_job = None  # Store timer job reference

    def on_setting_change(self, event=None):
        """Called when font size, position, or padding changes - updates overlay in real-time"""
        if self.overlay_visible and self.overlay is not None:
            self.update_overlay_appearance()

    def on_timer_change(self, event=None):
        """Called when timer settings change - updates timer in real-time"""
        if self.overlay_visible and self.overlay is not None:
            # Cancel existing timer
            if self.timer_job:
                self.master.after_cancel(self.timer_job)
                self.timer_job = None
            
            # Set new timer if enabled
            if self.timer_enabled.get():
                try:
                    timer_seconds = int(self.timer_entry.get())
                    if timer_seconds > 0:
                        self.timer_job = self.master.after(timer_seconds * 1000, self.auto_hide_overlay)
                except ValueError:
                    pass  # Invalid timer value, skip timer

    def update_overlay_appearance(self):
        """Update the overlay appearance without hiding/showing"""
        if not self.overlay_visible or self.overlay is None:
            return

        # Find the selected monitor
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

        # Get current font size
        try:
            font_size = int(self.font_size_var.get())
        except ValueError:
            font_size = 36
            
        # Update font size
        self.label.config(font=("Arial", font_size, "bold"))
        
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
        
        # Position overlay based on selected corner
        margin = 20  # Margin from screen edges
        corner = self.corner_var.get()
        
        if corner == "Bottom Left":
            x_pos = selected_monitor.x + margin
            y_pos = selected_monitor.y + selected_monitor.height - req_height - margin
        elif corner == "Bottom Right":
            x_pos = selected_monitor.x + selected_monitor.width - req_width - margin
            y_pos = selected_monitor.y + selected_monitor.height - req_height - margin
        elif corner == "Top Left":
            x_pos = selected_monitor.x + margin
            y_pos = selected_monitor.y + margin
        elif corner == "Top Right":
            x_pos = selected_monitor.x + selected_monitor.width - req_width - margin
            y_pos = selected_monitor.y + margin
        else:  # Default to bottom left if something goes wrong
            x_pos = selected_monitor.x + margin
            y_pos = selected_monitor.y + selected_monitor.height - req_height - margin
        
        self.overlay.geometry(f"{req_width}x{req_height}+{x_pos}+{y_pos}")
        # Force immediate update to ensure positioning takes effect
        self.overlay.update()

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
            # Hide initially until properly positioned
            self.overlay.withdraw()

            # Get font size from user input
            try:
                font_size = int(self.font_size_var.get())
            except ValueError:
                font_size = 36  # default font size

            # Label (BOLD, WHITE on BLACK)
            self.label = tk.Label(
                self.overlay,
                text=self.entry.get(),
                font=("Arial", font_size, "bold"),
                fg="white",
                bg="black"
            )
            
            # Get padding from user input
            try:
                padding = int(self.padding_entry.get())
            except ValueError:
                padding = 40  # default padding if invalid input
                
            self.label.pack(padx=padding, pady=padding)
        else:
            # Only update the text content (not real-time)
            self.label.config(text=self.entry.get())

        # Update appearance (font, padding, position) using the real-time method
        # Force window update before positioning
        self.overlay.update_idletasks()
        # Small delay to ensure proper measurement, then position
        self.master.after(10, self.update_overlay_appearance)
        # Show the overlay only after it's properly positioned
        self.master.after(20, lambda: self.overlay.deiconify())

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
