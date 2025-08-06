import tkinter as tk
from tkinter import ttk, messagebox
import win32gui
import win32con
import win32process
import psutil
import ctypes
import traceback
import os
import time

# Check if running as admin
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

class TaskbarManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Taskbar Manager")
        self.root.geometry("800x500")
        self.root.resizable(True, True)
        
        # Create main frame
        main_frame = ttk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create treeview for displaying applications
        self.tree = ttk.Treeview(main_frame, columns=("title", "process", "pid", "visible"), show="headings")
        self.tree.heading("title", text="Window Title")
        self.tree.heading("process", text="Process Name")
        self.tree.heading("pid", text="Process ID")
        self.tree.heading("visible", text="Visibility")
        self.tree.column("title", width=250)
        self.tree.column("process", width=150)
        self.tree.column("pid", width=80)
        self.tree.column("visible", width=80)
        self.tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(fill=tk.Y, side=tk.RIGHT)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Create buttons frame
        button_frame = ttk.Frame(root)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Add buttons
        ttk.Button(button_frame, text="Refresh", command=self.refresh_apps).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Hide Selected", command=self.hide_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Show Selected", command=self.show_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Close Selected", command=self.close_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Reset All", command=self.reset_all).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Hide All Similar", command=self.hide_all_similar).pack(side=tk.LEFT, padx=5)
        
        # Add status bar
        self.status_var = tk.StringVar()
        status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_var.set("Ready" + (" (Admin Mode)" if is_admin() else ""))
        
        # Initialize window list and track hidden windows
        self.windows = []
        self.hidden_windows = set()  # Track hidden windows by hwnd
        self.window_positions = {}   # Store original positions
        
        # Set up custom styles for buttons
        self.setup_styles()
        
        # Refresh the application list
        self.refresh_apps()
        
        # Show admin warning if not admin
        if not is_admin():
            messagebox.showwarning(
                "Limited Functionality", 
                "Running without administrator privileges.\nSome windows may not be hideable without admin rights."
            )
    
    def setup_styles(self):
        """Set up custom styles for buttons"""
        style = ttk.Style()
        style.configure("Accent.TButton", 
                       background="#007acc", 
                       foreground="white")
        style.configure("Special.TButton",
                       background="#ff7700",
                       foreground="white")
    
    def is_alt_tab_window(self, hwnd):
        """Check if a window would appear in the Alt+Tab dialog"""
        if not win32gui.IsWindow(hwnd):
            return False
            
        if not win32gui.IsWindowVisible(hwnd):
            # Only consider visible windows unless they're in our hidden list
            if hwnd not in self.hidden_windows:
                return False
        
        # Get window styles
        style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
        ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        
        # Check if it's a visible app window
        if (style & win32con.WS_VISIBLE) == 0 and hwnd not in self.hidden_windows:
            return False
        
        # Exclude certain window styles
        if (style & win32con.WS_DISABLED) != 0:
            return False
        
        # Exclude tool windows
        if (ex_style & win32con.WS_EX_TOOLWINDOW) != 0 and hwnd not in self.hidden_windows:
            return False
        
        # Make sure it's not a child window
        if win32gui.GetParent(hwnd) != 0 and hwnd not in self.hidden_windows:
            return False
        
        # Check if window has a title
        title = win32gui.GetWindowText(hwnd)
        if not title and hwnd not in self.hidden_windows:
            return False
        
        return True
    
    def get_process_name_from_hwnd(self, hwnd):
        """Get process name from window handle"""
        try:
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            try:
                process = psutil.Process(pid)
                return process.name(), pid
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                return "Unknown", pid
        except Exception as e:
            print(f"Error getting process: {e}")
            return "Unknown", 0
    
    def refresh_apps(self):
        """Refresh the list of applications"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.windows = []
        
        # Enumerate windows
        def enum_windows_callback(hwnd, _):
            if self.is_alt_tab_window(hwnd) or hwnd in self.hidden_windows:
                title = win32gui.GetWindowText(hwnd)
                proc_name, pid = self.get_process_name_from_hwnd(hwnd)
                visibility = "Visible" if win32gui.IsWindowVisible(hwnd) else "Hidden"
                
                window_info = {
                    "hwnd": hwnd,
                    "title": title,
                    "process": proc_name,
                    "pid": pid,
                    "visible": visibility
                }
                
                self.windows.append(window_info)
                
                # Add to treeview
                item = self.tree.insert("", tk.END, text=title, 
                             values=(title, proc_name, pid, visibility),
                             tags=("visible" if visibility == "Visible" else "hidden"))
                
        win32gui.EnumWindows(enum_windows_callback, None)
        
        # Set colors for visible/hidden status
        self.tree.tag_configure("visible", foreground="green")
        self.tree.tag_configure("hidden", foreground="gray")
        
        self.status_var.set(f"Found {len(self.windows)} applications" + 
                           (" (Admin Mode)" if is_admin() else ""))
    
    def get_selected_windows(self):
        """Get the selected windows from the treeview"""
        selected_ids = self.tree.selection()
        selected_windows = []
        
        for idx in selected_ids:
            item_values = self.tree.item(idx, "values")
            pid = int(item_values[2])  # PID is now at index 2
            
            # Find the window info that matches this PID
            for window in self.windows:
                if window["pid"] == pid:
                    selected_windows.append(window)
                    break
        
        return selected_windows
        
    def hide_window(self, hwnd):
        """Use multiple techniques to hide a window"""
        if not win32gui.IsWindow(hwnd):
            return False
        
        try:
            print(f"Hiding window {hwnd}...")
            
            # Store original position for later
            try:
                rect = win32gui.GetWindowRect(hwnd)
                self.window_positions[hwnd] = rect
            except Exception as e:
                print(f"  Failed to get window rect: {e}")
            
            # Try multiple techniques in sequence with short pauses
            
            # First try with standard hiding
            win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
            time.sleep(0.05)
            
            # Try to minimize first then hide (works better for some windows)
            win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
            time.sleep(0.05)
            win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
            
            # Make window a tool window so it doesn't show in taskbar
            ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, 
                                 ex_style | win32con.WS_EX_TOOLWINDOW)
            
            # Enable layered window for transparency
            ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                                 ex_style | win32con.WS_EX_LAYERED)
            
            # Set complete transparency
            win32gui.SetLayeredWindowAttributes(hwnd, 0, 0, win32con.LWA_ALPHA)
            
            # Move far off-screen
            win32gui.SetWindowPos(hwnd, win32con.HWND_BOTTOM,
                                -32000, -32000, 0, 0, 
                                win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE)
            
            # Try to disable the window
            win32gui.EnableWindow(hwnd, False)
            
            # Add to our list of hidden windows
            self.hidden_windows.add(hwnd)
            
            return True
        except Exception as e:
            print(f"Error hiding window {hwnd}: {e}")
            traceback.print_exc()
            return False
    
    def show_window(self, hwnd):
        """Restore a hidden window"""
        try:
            print(f"Showing window {hwnd}...")
            
            # Re-enable the window
            try:
                win32gui.EnableWindow(hwnd, True)
            except Exception as e:
                print(f"  Failed to re-enable: {e}")
            
            # Restore opacity
            try:
                ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
                if (ex_style & win32con.WS_EX_LAYERED):
                    win32gui.SetLayeredWindowAttributes(hwnd, 0, 255, win32con.LWA_ALPHA)
            except Exception as e:
                print(f"  Failed to restore opacity: {e}")
            
            # Move window back to original or visible position
            try:
                if hwnd in self.window_positions:
                    rect = self.window_positions[hwnd]
                    win32gui.SetWindowPos(
                        hwnd, 
                        win32con.HWND_TOP,
                        rect[0], rect[1],  # Original position
                        rect[2] - rect[0], rect[3] - rect[1],  # Original size
                        win32con.SWP_SHOWWINDOW
                    )
                else:
                    win32gui.SetWindowPos(
                        hwnd, 
                        win32con.HWND_TOP,
                        100, 100,  # Visible position
                        0, 0,  # Keep same size
                        win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW
                    )
            except Exception as e:
                print(f"  Failed to reposition window: {e}")
            
            # Restore window style
            try:
                style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
                win32gui.SetWindowLong(
                    hwnd, 
                    win32con.GWL_EXSTYLE, 
                    style & ~win32con.WS_EX_TOOLWINDOW
                )
            except Exception as e:
                print(f"  Failed to restore window style: {e}")
                
            # Show the window with multiple flags
            try:
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
                win32gui.ShowWindow(hwnd, win32con.SW_NORMAL)
            except Exception as e:
                print(f"  Failed to show window: {e}")
            
            return True
            
        except Exception as e:
            print(f"Error showing window {hwnd}: {e}")
            traceback.print_exc()
            return False
            
    def hide_selected(self):
        """Hide selected windows"""
        selected_windows = self.get_selected_windows()
        
        if not selected_windows:
            self.status_var.set("No windows selected")
            return
        
        count = 0
        for window in selected_windows:
            hwnd = window["hwnd"]
            if self.hide_window(hwnd):
                count += 1
        
        self.refresh_apps()
        self.status_var.set(f"Hidden {count} window(s)")
    
    def show_selected(self):
        """Show selected windows"""
        selected_windows = self.get_selected_windows()
        
        if not selected_windows:
            self.status_var.set("No windows selected")
            return
        
        count = 0
        for window in selected_windows:
            hwnd = window["hwnd"]
            if self.show_window(hwnd):
                count += 1
                if hwnd in self.hidden_windows:
                    self.hidden_windows.remove(hwnd)
        
        self.refresh_apps()
        self.status_var.set(f"Showed {count} window(s)")
    
    def hide_all_similar(self):
        """Hide all windows of the same application as the selected window"""
        selected_windows = self.get_selected_windows()
        
        if not selected_windows:
            self.status_var.set("No windows selected")
            return
            
        # Get the process name of the first selected window
        target_process = selected_windows[0]["process"].lower()
        
        count = 0
        for window in self.windows:
            if window["process"].lower() == target_process:
                hwnd = window["hwnd"]
                if self.hide_window(hwnd):
                    count += 1
        
        self.refresh_apps()
        self.status_var.set(f"Hidden {count} {target_process} window(s)")
    
    def close_selected(self):
        """Close selected windows"""
        selected_windows = self.get_selected_windows()
        
        if not selected_windows:
            self.status_var.set("No windows selected")
            return
        
        count = 0
        for window in selected_windows:
            hwnd = window["hwnd"]
            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
            if hwnd in self.hidden_windows:
                self.hidden_windows.remove(hwnd)
            count += 1
        
        self.refresh_apps()
        self.status_var.set(f"Closed {count} window(s)")
        
    def reset_all(self):
        """Reset all hidden windows to default visible state"""
        if not self.hidden_windows:
            self.status_var.set("No hidden windows to reset")
            return
            
        count = 0
        # Make a copy of hidden_windows since we'll be modifying it during iteration
        hidden_hwnd_copy = self.hidden_windows.copy()
        
        for hwnd in hidden_hwnd_copy:
            if self.show_window(hwnd):
                count += 1
                self.hidden_windows.remove(hwnd)
            else:
                # Handle case where window no longer exists
                self.hidden_windows.remove(hwnd)
        
        self.refresh_apps()
        self.status_var.set(f"Reset {count} hidden window(s) to visible state")

def main():
    root = tk.Tk()
    app = TaskbarManager(root)
    root.mainloop()

if __name__ == "__main__":
    main() 