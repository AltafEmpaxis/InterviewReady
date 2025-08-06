# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Comprehensive project documentation and setup files
- GitHub Actions CI/CD workflow
- Development environment configuration

## [1.0.0] - 2024-12-19

### Added

- Initial release of TaskbarManager
- Core functionality to list, hide, show, and close taskbar applications
- GUI interface built with tkinter
- Windows API integration through pywin32
- Process information display (PID, name, visibility status)
- Refresh functionality to update application list
- Multi-selection support for batch operations

### Features

- **Application Management**: Complete control over taskbar applications
- **Process Visibility**: Hide applications without closing them
- **System Integration**: Deep Windows taskbar integration
- **User Interface**: Clean, intuitive GUI with sortable columns
- **Error Handling**: Graceful handling of system errors and permissions
- **Admin Support**: Enhanced functionality when running as administrator

### Technical Details

- Built with Python 3.7+ compatibility
- Uses tkinter for cross-Windows GUI
- Windows API access via pywin32
- Process management through psutil
- PyInstaller for executable building

### Security

- Safe process manipulation
- Proper permission handling
- Admin rights detection
- Graceful error recovery

---

## Release Notes

### Version 1.0.0

This is the initial stable release of TaskbarManager. The application provides a complete solution for managing Windows taskbar applications with the following key capabilities:

**Core Features:**

- List all active taskbar applications
- Hide/show applications without closing them
- Close selected applications safely
- View detailed process information

**User Experience:**

- Simple, intuitive interface
- Multi-selection support
- Real-time application list updates
- Clear status indicators

**Technical Implementation:**

- Robust Windows API integration
- Proper error handling and recovery
- Administrator permission support
- Executable building capability

**Future Development:**
Future versions may include additional features such as:

- Application grouping and categorization
- Custom hotkeys and shortcuts
- Advanced filtering and search
- System tray integration
- Startup management
- Application monitoring and logging

---

For detailed information about changes in each version, see the [commit history](https://github.com/AltafEmpaxis/InterviewReady/commits/main) or [releases page](https://github.com/AltafEmpaxis/InterviewReady/releases).
