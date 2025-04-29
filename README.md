# System Resource Monitor

<div align="center">
  <img src="https://raw.githubusercontent.com/username/system-resource-monitor/main/assets/logo.png" alt="System Resource Monitor Logo" width="200"/>
  <h3>A comprehensive desktop application for real-time system performance monitoring</h3>
  
  ![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
  ![PyQt6](https://img.shields.io/badge/PyQt-6.0+-green.svg)
  ![psutil](https://img.shields.io/badge/psutil-5.9+-orange.svg)
  ![License](https://img.shields.io/badge/License-MIT-yellow.svg)
</div>

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Technical Highlights](#technical-highlights)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [Contact](#contact)
- [License](#license)

## Overview

System Resource Monitor is a robust, cross-platform desktop application built with Python and PyQt6 that provides real-time monitoring and visualization of system resources. It offers a user-friendly interface for tracking CPU, memory, storage, network, and process performance metrics on Windows, macOS, and Linux systems.

Designed with both technical and non-technical users in mind, this application makes complex system data easily accessible and understandable through intuitive visualizations and detailed statistics. Whether you're a developer diagnosing performance issues, an IT professional monitoring system health, or simply a user curious about your system's resource usage, System Resource Monitor provides the insights you need in a clean, modern interface.

## Features

### Main Dashboard
- **System Overview**: Quick access to key system information
- **OS Details**: Operating system name, version, architecture, and release information
- **Hardware Information**: CPU model, core count, and current usage
- **Boot Statistics**: System boot time and uptime tracking
- **Python Environment**: Python version, implementation, and build information
- **User Session Data**: Currently logged-in users and session details

### CPU Monitoring
- **Total CPU Usage**: Real-time overall CPU utilization percentage
- **Per-Core Performance**: Individual core usage with progress bars
- **CPU Information**: Physical and logical core counts, architecture details
- **Frequency Statistics**: Current, minimum, and maximum CPU frequencies

### Memory Monitoring
- **RAM Usage**: Overall memory utilization with graphical representation
- **Memory Distribution**: Used, available, and free memory tracking
- **Swap Memory**: Swap file/partition usage statistics
- **Performance Metrics**: Memory usage trends and status indicators

### Storage Monitoring
- **Disk Partitions**: Detailed view of all mounted partitions
- **Space Allocation**: Total, used, and free space for each storage device
- **I/O Statistics**: Disk read/write speeds and operation counts
- **Performance Analysis**: Overall storage usage status and warnings

### Network Monitoring
- **Traffic Analysis**: Upload and download speeds in real-time
- **Connection Tracking**: Active network connections with details
- **Interface Information**: Network adapter status and configuration
- **WiFi Details**: Wireless connection information when available

### Process Monitoring
- **Active Processes**: List of running processes with resource usage
- **System Statistics**: Total process count and related metrics
- **Performance Impact**: Identification of resource-intensive processes

## Architecture

System Resource Monitor follows a modular architecture with clear separation of concerns:

```
                    ┌───────────────────┐
                    │     Main Window   │
                    │  (User Interface) │
                    └─────────┬─────────┘
                              │
                              ▼
         ┌───────────────────────────────────────┐
         │          Monitor Windows Layer        │
         │ (Specialized displays for each metric)│
         └───────────────────┬───────────────────┘
                             │
                             ▼
         ┌───────────────────────────────────────┐
         │           Monitors Layer              │
         │     (Data collection and analysis)    │
         └───────────────────┬───────────────────┘
                             │
                             ▼
         ┌───────────────────────────────────────┐
         │       System Resources (psutil)       │
         │    (Raw data from operating system)   │
         └───────────────────────────────────────┘
```

### Data Flow:
1. **Data Collection**: The lowest layer uses `psutil` to gather raw system metrics
2. **Data Processing**: Monitor classes analyze and transform the raw data
3. **Data Presentation**: Monitor windows display the processed data in a user-friendly format
4. **User Interaction**: The main window coordinates the overall flow and handles user events

This architecture ensures:
- **Modularity**: Each component has a specific responsibility
- **Testability**: Components can be tested independently
- **Extensibility**: New monitoring capabilities can be added with minimal changes
- **Performance**: Real-time data capture with minimal system impact

## Technology Stack

### Core Technologies
- **Python** (3.8+): Foundation programming language chosen for its cross-platform compatibility and extensive libraries
- **PyQt6**: Modern Qt bindings for Python, providing a comprehensive GUI framework
- **psutil**: Cross-platform library for retrieving system information and resource usage

### Key Python Libraries
- **platform**: Access to underlying platform's identifying data
- **datetime**: Time and date handling for tracking system uptime
- **subprocess**: Interface for running external commands on specific monitoring tasks
- **socket**: Network interface details and connection management

### Development Tools
- **pytest**: Comprehensive testing framework for unit and integration tests
- **flake8**: Code linting for maintaining coding standards
- **black**: Code formatting for consistent style

## Project Structure

```
system-resource-monitor/
├── main_window.py                # Application entry point and main UI
├── monitors/                     # Data collection and processing modules
│   ├── __init__.py
│   ├── cpu_monitor.py            # CPU metrics collection
│   ├── memory_monitor.py         # RAM and swap metrics collection
│   ├── network_monitor.py        # Network metrics collection
│   ├── process_monitor.py        # Process metrics collection
│   ├── storage_monitor.py        # Disk metrics collection
│   └── system_monitor.py         # General system metrics collection
├── monitor_windows/              # Specialized UI windows for each metric
│   ├── cpu_window.py             # CPU monitoring interface
│   ├── memory_window.py          # Memory monitoring interface
│   ├── network_window.py         # Network monitoring interface
│   ├── process_window.py         # Process monitoring interface
│   ├── storage_window.py         # Storage monitoring interface
│   └── utils.py                  # Shared UI utilities
├── requirements.txt              # Project dependencies
└── designs/                      # Design files and prototypes
    └── ...
```

## Installation

### Prerequisites
- Python 3.8 or higher
- Qt6 libraries (automatically installed with PyQt6)
- Git (for cloning the repository)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/username/system-resource-monitor.git
   cd system-resource-monitor
   ```

2. **Create and activate a virtual environment (recommended)**
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python main_window.py
   ```

### Platform-Specific Notes

#### Windows
- Administrator privileges may be required for certain metrics
- Some advanced network features require additional Windows dependencies

#### macOS
- Additional permissions may be requested for system monitoring
- For full network monitoring, system extensions may need to be approved

#### Linux
- Some metrics may require root privileges (run with `sudo` if needed)
- For complete access to all features: `sudo apt-get install python3-dev` (or equivalent for your distribution)

## Usage

### Main Window
The main window provides a comprehensive overview of your system:

![Main Window](https://raw.githubusercontent.com/username/system-resource-monitor/main/assets/screenshots/main.png)

From this window, you can:
- View key system metrics at a glance
- Access detailed monitoring windows via the navigation buttons
- See real-time updates of critical system information

### Detailed Monitoring
Click on any of the navigation buttons to open specialized monitoring windows:

**CPU Monitor**
```
Shows detailed CPU usage with per-core statistics and frequency information.
Use this to identify CPU bottlenecks and monitor processor performance.
```

**Memory Monitor**
```
Displays RAM and swap usage with allocation breakdowns.
Useful for tracking memory leaks and resource-intensive applications.
```

**Storage Monitor**
```
Provides disk partitions, space usage, and I/O performance.
Helps identify disk-space issues and performance bottlenecks.
```

**Network Monitor**
```
Shows real-time network traffic, connections, and interface details.
Ideal for monitoring bandwidth usage and network performance.
```

**Process Monitor**
```
Lists all running processes with their resource consumption.
Use this to identify which applications are consuming system resources.
```

### Tips for Effective Monitoring
- Use the Process Monitor to identify resource-intensive applications
- Monitor Memory trends to detect potential memory leaks
- Watch I/O statistics during file operations to identify bottlenecks
- Track network traffic during online activities to understand bandwidth usage

## Technical Highlights

### Performance Optimizations
- **Efficient Polling**: Optimized data collection intervals based on metric volatility
- **Lazy Loading**: Monitor windows are created only when needed
- **Resource-Conscious Design**: Minimal CPU footprint for monitoring itself
- **Caching**: Previous metric values stored for performance calculations

### Cross-Platform Compatibility
- **Adaptive Monitoring**: Uses platform-specific methods when available
- **Graceful Degradation**: Falls back to cross-platform alternatives when needed
- **Consistent UI**: Uniform experience across different operating systems

### UI/UX Design Patterns
- **Master-Detail Interface**: Main overview with detailed drill-down capabilities
- **Real-Time Data Visualization**: Progress bars and dynamic updates
- **Consistent Visual Language**: Uniform design across all monitoring windows
- **Accessibility Considerations**: Text-based alternatives for visual elements

### Code Design Patterns
- **Observer Pattern**: Monitoring components observe system resources
- **Factory Pattern**: Standardized creation of monitoring windows
- **Facade Pattern**: Simplified interface to complex monitoring subsystems
- **Strategy Pattern**: Different monitoring strategies based on platform

## Roadmap

### Short-term Plans
- [ ] Historical data logging for trend analysis
- [ ] Customizable alerts for threshold violations
- [ ] System tray integration for background monitoring
- [ ] Export functionality for metrics and reports

### Medium-term Goals
- [ ] GPU monitoring support for NVIDIA and AMD graphics cards
- [ ] Temperature and fan speed monitoring
- [ ] Remote system monitoring capabilities
- [ ] Customizable dashboard layouts

### Long-term Vision
- [ ] Machine learning-based anomaly detection
- [ ] Network-wide monitoring of multiple systems
- [ ] Mobile companion app for remote monitoring
- [ ] Extensible plugin system for custom monitors

## Contributing

Contributions are welcome! Here's how you can contribute:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add some amazing feature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### Contribution Guidelines
- Follow PEP 8 style guide for Python code
- Write unit tests for new features
- Update documentation for any changes
- Add comments for complex logic
- Respect the existing architecture and design patterns

## Contact

**Project Maintainers**: Aimable M. and Jash M.

- Email: [aimable.mugwaneza@gmail.com](mailto:aimable.mugwaneza@gmail.com)
- GitHub: [https://github.com/username/system-resource-monitor](https://github.com/username/system-resource-monitor)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

<div align="center">
  <p>Made with ❤️ by Aimable M. and Jash M.</p>
</div>
