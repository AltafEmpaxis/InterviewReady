# TaskbarManager

![CI](https://github.com/AltafEmpaxis/InterviewReady/workflows/CI/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)

A Python application that lets you list, hide, and close taskbar applications on Windows. Built with tkinter for the GUI and Windows APIs for system interaction.

## ✨ Features

- 📋 **List Applications**: View all active taskbar applications with detailed information
- 👁️ **Hide/Show**: Hide applications without closing them, then show them again
- ❌ **Close Applications**: Safely close selected applications
- 🔍 **Process Information**: View process IDs, names, and visibility status
- 🖥️ **Windows Integration**: Deep integration with Windows taskbar and window management
- 🎯 **User-Friendly GUI**: Clean, intuitive interface built with tkinter

## 🖼️ Screenshots

_Application interface showing taskbar applications management_

## 🚀 Quick Start

### Option 1: Download Executable

1. Go to [Releases](https://github.com/AltafEmpaxis/InterviewReady/releases)
2. Download the latest executable
3. Run `TaskbarManager.exe`

### Option 2: Run from Source

```bash
# Clone the repository
git clone https://github.com/AltafEmpaxis/InterviewReady.git
cd InterviewReady

# Install dependencies
pip install -r requirements.txt

# Run the application
python src/taskbar_manager.py
```

## 📦 Installation

### Prerequisites

- **Windows OS** (Required for Windows API functionality)
- **Python 3.7+** (For running from source)

### From Source

```bash
# Create virtual environment (recommended)
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python src/taskbar_manager.py
```

### Build Executable

```bash
# Install build dependencies
pip install -r requirements.txt

# Build executable
python build.py

# Find executable in dist/ folder
```

## 🛠️ Development

### Setting Up Development Environment

```bash
# Clone and enter directory
git clone https://github.com/AltafEmpaxis/InterviewReady.git
cd InterviewReady

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies including dev tools
pip install -r requirements.txt
pip install -e .[dev]
```

### Development Tools

- **Black**: Code formatting
- **Flake8**: Linting
- **MyPy**: Type checking
- **Pytest**: Testing framework

```bash
# Format code
black .

# Lint code
flake8 .

# Type check
mypy src/
```

## 🔧 Usage

1. **Launch**: Start the application
2. **View**: See all active taskbar applications in the list
3. **Select**: Click on applications to select them
4. **Actions**:
   - **Refresh**: Update the application list
   - **Hide**: Hide selected applications (they continue running)
   - **Show**: Restore previously hidden applications
   - **Close**: Terminate selected applications

### Application Columns

- **Window Title**: The title displayed in the window
- **Process Name**: Name of the executable
- **Process ID**: System process identifier
- **Visibility**: Current visibility status

## ⚠️ Security & Permissions

### Administrator Rights

Some operations may require administrator privileges for system applications.

### Antivirus Considerations

PyInstaller executables may trigger antivirus warnings. This is a common false positive. Solutions:

- Add the executable to your antivirus exclusions
- Run from source code instead
- Build the executable yourself from the source

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Contribution Steps

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📋 Requirements

### Runtime Dependencies

- `pywin32>=310` - Windows API access
- `psutil>=7.0.0` - Process and system utilities
- `pillow>=11.0.0` - Image processing support

### Build Dependencies

- `pyinstaller>=6.0.0` - Executable building

### Development Dependencies

- `pytest>=6.0` - Testing framework
- `black>=21.0` - Code formatter
- `flake8>=3.8` - Code linter
- `mypy>=0.812` - Type checker

## 🐛 Troubleshooting

### Common Issues

**Q: Application won't start**

- Ensure you're running on Windows
- Check Python version (3.7+)
- Verify all dependencies are installed

**Q: Can't close system applications**

- Run as administrator
- Some system processes are protected

**Q: Antivirus blocks executable**

- Add to exclusions or run from source
- This is a common PyInstaller false positive

**Q: Application list is empty**

- Click "Refresh" button
- Ensure you have taskbar applications running

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Python and tkinter
- Uses Windows API through pywin32
- Inspired by Windows task management needs

## 📞 Support

- 🐛 **Bug Reports**: [Create an issue](https://github.com/AltafEmpaxis/InterviewReady/issues)
- 💡 **Feature Requests**: [Create an issue](https://github.com/AltafEmpaxis/InterviewReady/issues)
- 📖 **Documentation**: [Wiki](https://github.com/AltafEmpaxis/InterviewReady/wiki)

---

⭐ **Star this repository if you find it helpful!**
