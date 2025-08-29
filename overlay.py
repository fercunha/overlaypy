import tkinter as tk
from tkinter import ttk
import ctypes
import platform
import logging
import os
import sys
from datetime import datetime
from screeninfo import get_monitors


# Configure comprehensive logging
def setup_logging():
    """Set up comprehensive logging for debugging Windows issues."""
    
    # Create logs directory if it doesn't exist
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Create log filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = os.path.join(log_dir, f"overlaypy_{timestamp}.log")
    
    # Configure logging with multiple levels
    # Use a StreamHandler with UTF-8 encoding for console output
    console_handler = logging.StreamHandler(sys.stdout)
    try:
        console_handler.setStream(open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1))
    except Exception:
        # Fallback for environments where fileno() is not available
        pass
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            console_handler
        ]
    )
    
    logger = logging.getLogger(__name__)
    
    # Log system information
    logger.info("=" * 60)
    logger.info("OVERLAYPY STARTUP - SYSTEM INFORMATION")
    logger.info("=" * 60)
    logger.info(f"Platform: {platform.platform()}")
    logger.info(f"System: {platform.system()}")
    logger.info(f"Release: {platform.release()}")
    logger.info(f"Version: {platform.version()}")
    logger.info(f"Machine: {platform.machine()}")
    logger.info(f"Processor: {platform.processor()}")
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Python executable: {sys.executable}")
    logger.info(f"Current working directory: {os.getcwd()}")
    logger.info(f"Script location: {os.path.abspath(__file__)}")
    logger.info(f"Log file: {log_filename}")
    
    # Test monitor detection
    try:
        monitors = get_monitors()
        logger.info(f"Detected {len(monitors)} monitor(s):")
        for i, monitor in enumerate(monitors):
            logger.info(f"  Monitor {i+1}: {monitor}")
    except Exception as e:
        logger.error(f"Failed to detect monitors: {e}")
    
    # Test Windows-specific features
    if platform.system() == "Windows":
        logger.info("Checking Windows-specific features...")
        try:
            # Test ctypes availability
            kernel32 = ctypes.windll.kernel32
            logger.info("✓ ctypes.windll.kernel32 accessible")
            
            user32 = ctypes.windll.user32
            logger.info("✓ ctypes.windll.user32 accessible")
            
            # Test getting window handle capability
            hwnd = kernel32.GetConsoleWindow()
            logger.info(f"Console window handle: {hwnd}")
            
        except Exception as e:
            logger.error(f"Windows-specific feature test failed: {e}")
    
    logger.info("=" * 60)
    return logger

# Initialize logging
logger = setup_logging()


class OverlayApp:
    def __init__(self, master):
        self.logger = logging.getLogger(f"{__name__}.OverlayApp")
        self.logger.info("Initializing OverlayApp...")
        
        self.master = master
        master.title("Overlay Controller")
        master.geometry("450x500")
        
        try:
            master.attributes("-topmost", True)  # Keep main window always on top
            self.logger.info("✓ Main window set to topmost")
        except Exception as e:
            self.logger.error(f"Failed to set main window topmost: {e}")

        # Create main frame with scrollbar
        self.logger.debug("Creating main UI components...")
        main_frame = tk.Frame(master)
        main_frame.pack(fill=tk.BOTH, expand=1)

        # Create canvas and scrollbar
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        # Configure canvas
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.logger.debug("✓ Canvas and scrollbar created")

        # Bind mousewheel to canvas (cross-platform)
        def _on_mousewheel(event):
            try:
                # Windows and macOS use different scroll directions and deltas
                if platform.system() == "Windows":
                    delta = int(-1 * (event.delta / 120))
                    self.logger.debug(f"Windows mousewheel: delta={event.delta}, scroll units={delta}")
                    canvas.yview_scroll(delta, "units")
                elif platform.system() == "Darwin":  # macOS
                    delta = int(-1 * event.delta)
                    self.logger.debug(f"macOS mousewheel: delta={event.delta}, scroll units={delta}")
                    canvas.yview_scroll(delta, "units")
                else:  # Linux
                    if event.num == 4:
                        self.logger.debug("Linux mousewheel: scroll up")
                        canvas.yview_scroll(-1, "units")
                    elif event.num == 5:
                        self.logger.debug("Linux mousewheel: scroll down")
                        canvas.yview_scroll(1, "units")
            except Exception as e:
                self.logger.error(f"Mousewheel event error: {e}")

        # Bind mouse wheel events for different platforms
        try:
            if platform.system() == "Linux":
                canvas.bind_all("<Button-4>", _on_mousewheel)
                canvas.bind_all("<Button-5>", _on_mousewheel)
                self.logger.debug("✓ Linux mousewheel events bound")
            else:
                canvas.bind_all("<MouseWheel>", _on_mousewheel)
                self.logger.debug(f"✓ {platform.system()} mousewheel events bound")
        except Exception as e:
            self.logger.error(f"Failed to bind mousewheel events: {e}")
        else:
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
        font_sizes = [
            "12",
            "18",
            "24",
            "30",
            "36",
            "42",
            "48",
            "60",
            "72",
            "84",
            "96",
            "120",
            "144",
            "168",
            "192",
            "216",
            "240",
        ]
        self.font_size_var.set("36")  # Default font size
        self.font_size_menu = tk.OptionMenu(font_col, self.font_size_var, *font_sizes, command=self.on_setting_change)
        self.font_size_menu.config(width=8)
        self.font_size_menu.pack(fill=tk.X)

        # Position Column
        position_col = tk.Frame(controls_frame)
        position_col.pack(side=tk.LEFT, padx=(0, 15), fill=tk.X, expand=True)
        tk.Label(position_col, text="Position:", font=("Arial", 11, "bold")).pack()
        self.corner_var = tk.StringVar(container)
        corners = ["Bottom Left", "Bottom Right", "Top Left", "Top Right", "Center"]
        self.corner_var.set("Bottom Left")  # Default position
        self.corner_menu = tk.OptionMenu(position_col, self.corner_var, *corners, command=self.on_setting_change)
        self.corner_menu.config(width=10)
        self.corner_menu.pack(fill=tk.X)

        # Padding Column
        padding_col = tk.Frame(controls_frame)
        padding_col.pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Label(padding_col, text="Padding (px):", font=("Arial", 11, "bold")).pack()
        self.padding_entry = tk.Entry(padding_col, width=8, font=("Arial", 12), justify="center")
        self.padding_entry.pack(fill=tk.X)
        self.padding_entry.insert(0, "40")
        # Bind real-time updates for padding
        self.padding_entry.bind("<KeyRelease>", self.on_setting_change)

        # --- Timer Settings ---
        timer_frame = tk.Frame(container)
        timer_frame.pack(pady=(10, 10))

        self.timer_enabled = tk.BooleanVar(value=True)
        self.timer_checkbox = tk.Checkbutton(
            timer_frame, text="Auto-hide after", variable=self.timer_enabled, font=("Arial", 11), command=self.on_timer_change
        )
        self.timer_checkbox.pack(side=tk.LEFT)

        self.timer_entry = tk.Entry(timer_frame, width=5, font=("Arial", 12))
        self.timer_entry.pack(side=tk.LEFT, padx=(5, 2))
        self.timer_entry.insert(0, "60")
        # Bind real-time updates for timer
        self.timer_entry.bind("<KeyRelease>", self.on_timer_change)

        tk.Label(timer_frame, text="seconds", font=("Arial", 11)).pack(side=tk.LEFT)

        # --- Monitor Selection ---
        tk.Label(container, text="Select Monitor:", font=("Arial", 12, "bold")).pack(pady=(10, 2))
        
        self.logger.info("Detecting monitors...")
        try:
            self.monitors = get_monitors()
            self.logger.info(f"✓ Detected {len(self.monitors)} monitor(s)")
            for i, monitor in enumerate(self.monitors):
                self.logger.info(f"  Monitor {i+1}: {monitor}")
        except Exception as e:
            self.logger.error(f"Failed to detect monitors: {e}")
            # Create a fallback monitor for testing
            self.monitors = []
            
        if not self.monitors:
            self.logger.warning("No monitors detected, creating fallback monitor")
            # Create a simple fallback monitor object
            class FallbackMonitor:
                def __init__(self):
                    self.x = 0
                    self.y = 0
                    self.width = 1920
                    self.height = 1080
                    self.name = "Fallback Monitor"
                def __str__(self):
                    return f"FallbackMonitor(x={self.x}, y={self.y}, width={self.width}, height={self.height})"
            self.monitors = [FallbackMonitor()]
        
        self.monitor_var = tk.StringVar(container)

        # Create monitor names for dropdown
        monitor_names = []
        self.logger.debug("Creating monitor dropdown options...")
        for i, monitor in enumerate(self.monitors):
            try:
                if hasattr(monitor, "name") and monitor.name:
                    monitor_name = f"{monitor.name} ({monitor.width}x{monitor.height})"
                    self.logger.debug(f"Monitor {i+1} with name: {monitor_name}")
                else:
                    monitor_name = f"Monitor {i + 1} ({monitor.width}x{monitor.height})"
                    self.logger.debug(f"Monitor {i+1} without name: {monitor_name}")
                monitor_names.append(monitor_name)
            except Exception as e:
                self.logger.error(f"Error processing monitor {i+1}: {e}")
                monitor_names.append(f"Monitor {i + 1} (Unknown)")

        if monitor_names:
            # Try to set primary monitor as default
            primary_monitor_name = None
            for i, monitor in enumerate(self.monitors):
                if hasattr(monitor, 'is_primary') and monitor.is_primary:
                    if hasattr(monitor, "name") and monitor.name:
                        primary_monitor_name = f"{monitor.name} ({monitor.width}x{monitor.height})"
                    else:
                        primary_monitor_name = f"Monitor {i + 1} ({monitor.width}x{monitor.height})"
                    break
            
            if primary_monitor_name and primary_monitor_name in monitor_names:
                self.monitor_var.set(primary_monitor_name)
                self.logger.info(f"✓ Default monitor set to primary: {primary_monitor_name}")
            else:
                self.monitor_var.set(monitor_names[0])
                self.logger.info(f"✓ Default monitor set to: {monitor_names[0]}")
        else:
            self.monitor_var.set("No monitors detected")
            self.logger.error("No monitor names available for dropdown")
            
        self.monitor_menu = tk.OptionMenu(container, self.monitor_var, *monitor_names, command=self.on_setting_change)
        self.monitor_menu.config(width=35)
        self.monitor_menu.pack(pady=(0, 15))
        self.logger.debug("✓ Monitor selection UI created")

        # --- Buttons ---
        self.toggle_btn = tk.Button(
            container,
            text="Show Overlay",
            font=("Arial", 12, "bold"),
            bg="lightgreen",
            fg="black",
            command=self.toggle_overlay,
        )
        self.toggle_btn.pack(pady=5)

        self.quit_btn = tk.Button(container, text="Quit", font=("Arial", 12), bg="lightcoral", fg="black", command=master.quit)
        self.quit_btn.pack(pady=(5, 20))  # Extra bottom padding

        # Overlay state
        self.overlay = None
        self.overlay_visible = False
        self.timer_job = None  # Store timer job reference

    def on_setting_change(self, event=None):
        """Called when font size, position, or padding changes - updates overlay in real-time"""
        self.logger.debug(f"Setting change detected: event={event}")
        if self.overlay_visible and self.overlay is not None:
            self.logger.debug("Updating overlay appearance due to setting change")
            self.update_overlay_appearance()
        else:
            self.logger.debug("Skipping overlay update (not visible or None)")

    def on_timer_change(self, event=None):
        """Called when timer settings change - updates timer in real-time"""
        self.logger.debug(f"Timer setting change detected: event={event}")
        if self.overlay_visible and self.overlay is not None:
            # Cancel existing timer
            if self.timer_job:
                self.master.after_cancel(self.timer_job)
                self.timer_job = None
                self.logger.debug("✓ Cancelled existing timer")

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
        self.logger.debug("Starting update_overlay_appearance...")
        
        if not self.overlay_visible or self.overlay is None:
            self.logger.debug("Skipping update: overlay not visible or None")
            return

        # Find the selected monitor
        selected_monitor = None
        selected_text = self.monitor_var.get()
        self.logger.debug(f"Selected monitor for positioning: '{selected_text}'")

        for i, monitor in enumerate(self.monitors):
            if hasattr(monitor, "name") and monitor.name:
                monitor_name = f"{monitor.name} ({monitor.width}x{monitor.height})"
            else:
                monitor_name = f"Monitor {i+1} ({monitor.width}x{monitor.height})"

            if monitor_name == selected_text:
                selected_monitor = monitor
                self.logger.debug(f"✓ Found positioning monitor: {monitor}")
                break

        if selected_monitor is None:
            # Try to find the primary monitor first
            primary_monitor = None
            for monitor in self.monitors:
                if hasattr(monitor, 'is_primary') and monitor.is_primary:
                    primary_monitor = monitor
                    break
            
            selected_monitor = primary_monitor if primary_monitor else self.monitors[0]
            self.logger.warning(f"No matching monitor for positioning, using primary/default: {selected_monitor}")

        # Get current font size
        try:
            font_size = int(self.font_size_var.get())
            self.logger.debug(f"Font size: {font_size}")
        except ValueError as e:
            font_size = 36
            self.logger.warning(f"Invalid font size, using default 36: {e}")

        # Update font size
        try:
            self.label.config(font=("Arial", font_size, "bold"))
            self.logger.debug("✓ Font updated")
        except Exception as e:
            self.logger.error(f"Failed to update font: {e}")

        # Get current padding value
        try:
            padding = int(self.padding_entry.get())
            self.logger.debug(f"Padding: {padding}")
        except ValueError as e:
            padding = 40
            self.logger.warning(f"Invalid padding, using default 40: {e}")

        # Update padding
        try:
            self.label.pack_configure(padx=padding, pady=padding)
            self.logger.debug("✓ Padding updated")
        except Exception as e:
            self.logger.error(f"Failed to update padding: {e}")

        # Calculate size based on text content and padding
        try:
            self.overlay.update_idletasks()  # Force update to get accurate measurements
            self.logger.debug("✓ update_idletasks completed for size calculation")
            
            req_width = self.label.winfo_reqwidth() + (padding * 2)
            req_height = self.label.winfo_reqheight() + (padding * 2)
            self.logger.debug(f"Required size: {req_width}x{req_height} (label: {self.label.winfo_reqwidth()}x{self.label.winfo_reqheight()}, padding: {padding})")
        except Exception as e:
            self.logger.error(f"Failed to calculate overlay size: {e}")
            return

        # Position overlay based on selected corner
        margin = 20  # Margin from screen edges
        corner = self.corner_var.get()
        self.logger.debug(f"Positioning in corner: '{corner}' with margin: {margin}")

        try:
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
            elif corner == "Center":
                x_pos = selected_monitor.x + (selected_monitor.width - req_width) // 2
                y_pos = selected_monitor.y + (selected_monitor.height - req_height) // 2
            else:  # Default to bottom left if something goes wrong
                x_pos = selected_monitor.x + margin
                y_pos = selected_monitor.y + selected_monitor.height - req_height - margin
                self.logger.warning(f"Unknown corner '{corner}', using bottom left")

            # Clamp x_pos and y_pos to stay within monitor bounds
            x_pos = max(selected_monitor.x, min(x_pos, selected_monitor.x + selected_monitor.width - req_width))
            y_pos = max(selected_monitor.y, min(y_pos, selected_monitor.y + selected_monitor.height - req_height))

            self.logger.debug(f"Clamped position: ({x_pos}, {y_pos})")
            self.logger.debug(f"Monitor bounds: x={selected_monitor.x}, y={selected_monitor.y}, w={selected_monitor.width}, h={selected_monitor.height}")

            # Set geometry
            geometry_string = f"{req_width}x{req_height}+{x_pos}+{y_pos}"
            self.logger.debug(f"Setting geometry: {geometry_string}")

            self.overlay.geometry(geometry_string)
            self.logger.debug("✓ Geometry set")

            # Force immediate update to ensure positioning takes effect
            self.overlay.update()
            self.logger.debug("✓ Overlay update completed")

            # Verify final position
            actual_x = self.overlay.winfo_x()
            actual_y = self.overlay.winfo_y()
            actual_width = self.overlay.winfo_width()
            actual_height = self.overlay.winfo_height()
            self.logger.info(f"Final overlay position: ({actual_x}, {actual_y}), size: {actual_width}x{actual_height}")

        except Exception as e:
            self.logger.error(f"Failed to position overlay: {e}")

    def toggle_overlay(self):
        self.logger.debug(f"Toggle overlay called, current state: {'visible' if self.overlay_visible else 'hidden'}")
        if self.overlay_visible:
            self.hide_overlay()
        else:
            self.show_overlay()

    def auto_hide_overlay(self):
        """Called by timer to automatically hide overlay"""
        self.logger.info("Auto-hide timer triggered")
        self.hide_overlay()

    def show_overlay(self):
        self.logger.info("Starting show_overlay process...")
        
        # Find the selected monitor by matching the dropdown selection
        selected_monitor = None
        selected_text = self.monitor_var.get()
        self.logger.debug(f"Selected monitor text: '{selected_text}'")

        for i, monitor in enumerate(self.monitors):
            if hasattr(monitor, "name") and monitor.name:
                monitor_name = f"{monitor.name} ({monitor.width}x{monitor.height})"
            else:
                monitor_name = f"Monitor {i+1} ({monitor.width}x{monitor.height})"

            self.logger.debug(f"Checking monitor {i}: {monitor_name}")
            if monitor_name == selected_text:
                selected_monitor = monitor
                self.logger.info(f"✓ Found matching monitor: {monitor}")
                break

        if selected_monitor is None:
            selected_monitor = self.monitors[0]
            self.logger.warning(f"No matching monitor found, using default: {selected_monitor}")

        if self.overlay is None:
            self.logger.info("Creating new overlay window...")
            try:
                self.overlay = tk.Toplevel(self.master)
                self.logger.debug("✓ Toplevel window created")
                
                # Temporarily disable overrideredirect on Windows for debugging
                if platform.system() == "Windows":
                    # Try without overrideredirect first to see if window appears
                    self.overlay.overrideredirect(False)
                    self.logger.debug("✓ Override redirect set to FALSE (Windows debug mode)")
                    # Add a title for debugging
                    self.overlay.title("OverlayPy Debug")
                else:
                    self.overlay.overrideredirect(True)
                    self.logger.debug("✓ Override redirect set to TRUE")
                
                self.overlay.attributes("-topmost", True)
                self.logger.debug("✓ Topmost attribute set")
                
                # Windows-specific visibility attributes
                if platform.system() == "Windows":
                    try:
                        self.overlay.attributes("-alpha", 0.95)  # Slight transparency to ensure visibility
                        self.overlay.attributes("-disabled", False)  # Ensure window is enabled
                        self.overlay.attributes("-toolwindow", True)  # Tool window style
                        self.logger.debug("✓ Windows-specific attributes set")
                    except Exception as e:
                        self.logger.warning(f"Could not set Windows attributes: {e}")
                
                self.overlay.configure(bg="black")
                self.logger.debug("✓ Background color configured")
                
                # Hide initially until properly positioned
                self.overlay.withdraw()
                self.logger.debug("✓ Window initially withdrawn")

                # Get font size from user input
                try:
                    font_size = int(self.font_size_var.get())
                    self.logger.debug(f"Font size: {font_size}")
                except ValueError as e:
                    font_size = 36  # default font size
                    self.logger.warning(f"Invalid font size, using default 36: {e}")

                # Create label
                message_text = self.entry.get()
                self.logger.debug(f"Message text: '{message_text}'")
                
                self.label = tk.Label(
                    self.overlay, 
                    text=message_text, 
                    font=("Arial", font_size, "bold"), 
                    fg="white", 
                    bg="black"
                )
                self.logger.debug("✓ Label widget created")

                # Get padding from user input
                try:
                    padding = int(self.padding_entry.get())
                    self.logger.debug(f"Padding: {padding}")
                except ValueError as e:
                    padding = 40  # default padding if invalid input
                    self.logger.warning(f"Invalid padding, using default 40: {e}")

                self.label.pack(padx=padding, pady=padding)
                self.logger.debug("✓ Label packed with padding")

                # Position the overlay immediately when first created
                self.overlay.update_idletasks()
                self.logger.debug("✓ Initial update_idletasks completed")
                
                self.update_overlay_appearance()
                self.logger.debug("✓ Initial overlay appearance updated")
                
            except Exception as e:
                self.logger.error(f"Failed to create overlay window: {e}")
                return
        else:
            self.logger.info("Updating existing overlay...")
            try:
                # Only update the text content (not real-time)
                new_text = self.entry.get()
                self.label.config(text=new_text)
                self.logger.debug(f"✓ Label text updated to: '{new_text}'")
            except Exception as e:
                self.logger.error(f"Failed to update overlay text: {e}")

        # Update appearance (font, padding, position) using the real-time method
        try:
            # Force window update before positioning
            self.overlay.update_idletasks()
            self.logger.debug("✓ Final update_idletasks completed")
            
            # Small delay to ensure proper measurement, then position
            self.master.after(10, self.update_overlay_appearance)
            self.logger.debug("✓ Scheduled overlay appearance update")
            
            # Show the overlay only after it's properly positioned
            self.master.after(20, lambda: self._show_overlay_delayed())
            self.logger.debug("✓ Scheduled overlay display")
            
        except Exception as e:
            self.logger.error(f"Failed to schedule overlay updates: {e}")

        # Make overlay click-through (Windows only) - Make this optional for debugging
        if platform.system() == "Windows":
            self.logger.info("Attempting to enable Windows click-through feature...")
            try:
                # Get the window handle
                overlay_id = self.overlay.winfo_id()
                self.logger.debug(f"Overlay winfo_id: {overlay_id}")
                
                hwnd = ctypes.windll.user32.GetParent(overlay_id)
                self.logger.debug(f"GetParent result: {hwnd}")
                
                if hwnd:
                    # Get current window style
                    current_style = ctypes.windll.user32.GetWindowLongW(hwnd, -20)
                    self.logger.debug(f"Current window style: 0x{current_style:x}")
                    
                    # Try a less aggressive approach first - just WS_EX_LAYERED without transparent
                    new_style = current_style | 0x80000  # WS_EX_LAYERED only
                    self.logger.debug(f"New window style (layered only): 0x{new_style:x}")
                    
                    result = ctypes.windll.user32.SetWindowLongW(hwnd, -20, new_style)
                    self.logger.debug(f"SetWindowLongW result: {result}")
                    
                    if result == 0:
                        error_code = ctypes.windll.kernel32.GetLastError()
                        self.logger.warning(f"SetWindowLongW returned 0, error code: {error_code}")
                    else:
                        self.logger.info("✓ Layered window feature enabled successfully")
                        
                        # Force window to be visible and on top
                        ctypes.windll.user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002 | 0x0010)
                        self.logger.debug("✓ SetWindowPos called to ensure visibility")
                else:
                    self.logger.warning("GetParent returned 0 (no parent window)")
                    
            except Exception as e:
                self.logger.error(f"Failed to set up Windows click-through: {e}")
                # Continue without click-through functionality
                    
            except Exception as e:
                # Click-through feature failed, but overlay still works
                self.logger.warning(f"Click-through feature failed (overlay still functional): {e}")
                print(f"Note: Click-through feature unavailable: {e}")
        else:
            self.logger.debug(f"Skipping click-through (not Windows): {platform.system()}")

        self.overlay_visible = True
        self.toggle_btn.config(text="Hide Overlay", bg="orange", fg="black")
        self.logger.debug("✓ Toggle button updated to 'Hide Overlay'")

        # Set up auto-hide timer if enabled
        if self.timer_enabled.get():
            self.logger.info("Setting up auto-hide timer...")
            try:
                timer_seconds = int(self.timer_entry.get())
                self.logger.debug(f"Timer duration: {timer_seconds} seconds")
                
                if timer_seconds > 0:
                    # Cancel any existing timer
                    if self.timer_job:
                        self.master.after_cancel(self.timer_job)
                        self.logger.debug("✓ Cancelled existing timer")
                    
                    # Set new timer
                    self.timer_job = self.master.after(timer_seconds * 1000, self.auto_hide_overlay)
                    self.logger.info(f"✓ Auto-hide timer set for {timer_seconds} seconds")
                else:
                    self.logger.warning("Timer duration is 0 or negative, skipping timer")
            except ValueError as e:
                self.logger.warning(f"Invalid timer value, skipping timer: {e}")
        else:
            self.logger.debug("Auto-hide timer disabled")
            
        self.logger.info("show_overlay process completed")

    def _show_overlay_delayed(self):
        """Helper method for delayed overlay display with logging."""
        try:
            if self.overlay:
                # Force focus and visibility on Windows
                if platform.system() == "Windows":
                    try:
                        # Additional Windows-specific visibility calls
                        self.overlay.lift()
                        self.overlay.focus_force()
                        self.logger.debug("✓ Windows lift() and focus_force() called")
                    except Exception as e:
                        self.logger.warning(f"Windows visibility calls failed: {e}")
                
                self.overlay.deiconify()
                self.logger.info("✓ Overlay window displayed (deiconify)")
                
                # Log final window position and size
                self.overlay.update_idletasks()
                x = self.overlay.winfo_x()
                y = self.overlay.winfo_y()
                width = self.overlay.winfo_width()
                height = self.overlay.winfo_height()
                self.logger.info(f"Final overlay position: ({x}, {y}), size: {width}x{height}")
                
                # Additional visibility check on Windows
                if platform.system() == "Windows":
                    try:
                        visible = self.overlay.winfo_viewable()
                        mapped = self.overlay.winfo_ismapped()
                        self.logger.info(f"Window visibility check - viewable: {visible}, mapped: {mapped}")
                    except Exception as e:
                        self.logger.warning(f"Visibility check failed: {e}")
            else:
                self.logger.error("Overlay is None in _show_overlay_delayed")
        except Exception as e:
            self.logger.error(f"Failed to display overlay: {e}")

    def hide_overlay(self):
        self.logger.info("Hiding overlay...")
        
        # Cancel any pending timer
        if self.timer_job:
            self.master.after_cancel(self.timer_job)
            self.timer_job = None
            self.logger.debug("✓ Auto-hide timer cancelled")

        try:
            if self.overlay:
                self.overlay.withdraw()
                self.logger.info("✓ Overlay window hidden (withdraw)")
            else:
                self.logger.warning("Overlay is None when trying to hide")
                
            self.overlay_visible = False
            self.toggle_btn.config(text="Show Overlay", bg="lightgreen", fg="black")
            self.logger.debug("✓ Toggle button updated to 'Show Overlay'")
            
        except Exception as e:
            self.logger.error(f"Failed to hide overlay: {e}")


if __name__ == "__main__":
    import argparse
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='OverlayPy - Text overlay application')
    parser.add_argument('--test', action='store_true', help='Run in test mode (exit after 3 seconds)')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging to console')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], 
                        default='INFO', help='Set logging level')
    args = parser.parse_args()
    
    # Adjust logging level if requested
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(getattr(logging, args.log_level))
    
    logger.info(f"Starting OverlayPy with arguments: {vars(args)}")
    
    try:
        logger.info("Creating Tkinter root window...")
        root = tk.Tk()
        logger.info("✓ Tkinter root window created")
        
        # Test mode setup
        if args.test:
            logger.info("Running in TEST MODE - will exit after 3 seconds")
            root.title("OverlayPy - TEST MODE")
            
        logger.info("Initializing OverlayApp...")
        app = OverlayApp(root)
        logger.info("✓ OverlayApp initialized successfully")
        
        if args.test:
            # In test mode, show the overlay briefly then exit
            def test_sequence():
                logger.info("TEST: Starting test sequence...")
                try:
                    app.entry.delete(0, tk.END)
                    app.entry.insert(0, "TEST OVERLAY")
                    logger.info("TEST: Set test message")
                    
                    app.show_overlay()
                    logger.info("TEST: Overlay shown")
                    
                    # Wait 2 seconds then hide and exit
                    root.after(2000, lambda: [
                        logger.info("TEST: Hiding overlay"),
                        app.hide_overlay(),
                        logger.info("TEST: Test completed successfully"),
                        root.quit()
                    ])
                except Exception as e:
                    logger.error(f"TEST: Test sequence failed: {e}")
                    root.quit()
            
            # Start test sequence after UI is ready
            root.after(500, test_sequence)
        
        logger.info("Starting main event loop...")
        root.mainloop()
        logger.info("Main event loop ended")
        
    except Exception as e:
        logger.error(f"Fatal error in main: {e}")
        logger.error(f"Exception type: {type(e).__name__}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        
        # Try to show a simple error dialog
        try:
            import tkinter.messagebox as mb
            mb.showerror("OverlayPy Error", 
                        f"Fatal error occurred:\n{e}\n\nCheck the log file in the 'logs' directory for details.")
        except:
            print(f"FATAL ERROR: {e}")
            
        sys.exit(1)
    
    logger.info("OverlayPy shutdown complete")
