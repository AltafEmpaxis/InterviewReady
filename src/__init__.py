"""
TaskbarManager - A Python application for managing Windows taskbar applications.

This module provides functionality to list, hide, show, and close taskbar applications
on Windows systems using the Windows API.
"""

__version__ = "1.0.0"
__author__ = "AltafEmpaxis"
__license__ = "MIT"

from .taskbar_manager import TaskbarManager

__all__ = ["TaskbarManager"]