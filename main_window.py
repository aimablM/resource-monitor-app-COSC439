from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QPushButton, QGroupBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon, QFont, QPainter, QPixmap
import sys
from datetime import datetime
import platform
import psutil
import os
from monitors.system_monitor import SystemMonitor
from monitor_windows.cpu_window import CPUWindow
from monitor_windows.memory_window import MemoryWindow
from monitor_windows.storage_window import StorageWindow
from monitor_windows.network_window import NetworkWindow
from monitor_windows.process_window import ProcessWindow

def create_emoji_icon(emoji, size=32):
        """Create a QIcon from an emoji character"""
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        font = QFont()
        font.setPointSize(size - 8)  # Adjust emoji size to fit
        painter.setFont(font)
        
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, emoji)
        painter.end()
        
        return QIcon(pixmap)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("System Resource Monitor")
        self.setMinimumSize(800, 600)
        self.setWindowIcon(create_emoji_icon('💻'))
        
        # Initialize system monitor
        self.system_monitor = SystemMonitor()
        
        # Initialize monitor_windows dictionary
        self.monitor_windows = {
            'cpu': None,
            'memory': None,
            'storage': None,
            'network': None,
            'process': None
        }
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Add welcome header
        self.create_welcome_header(layout)
        
        # Create navigation buttons
        nav_layout = QHBoxLayout()
        self.create_nav_buttons(nav_layout)
        layout.addLayout(nav_layout)
        
        # Create info sections
        self.create_info_sections(layout)
        
        # Add credits footer
        self.create_credits_footer(layout)
        
        # Set up timer for updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_info)
        self.timer.start(5000)  # Update every 5 seconds
        
        # Initial update
        self.update_info()

    def create_welcome_header(self, layout):
        """Create welcome header"""
        header = QLabel("Hi there! Let me tell you about your system!")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)

    def create_credits_footer(self, layout):
        """Create credits footer"""
        footer = QLabel("Designed and built by Aimable M and Jash M")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(footer)

    def create_nav_buttons(self, layout):
        """Create navigation buttons"""
        buttons = [
            ("CPU Monitor", self.show_cpu_monitor),
            ("Memory Monitor", self.show_memory_monitor),
            ("Storage Monitor", self.show_storage_monitor),
            ("Network Monitor", self.show_network_monitor),
            ("Process Monitor", self.show_process_monitor)
        ]
        
        for text, slot in buttons:
            button = QPushButton(text)
            button.clicked.connect(slot)
            layout.addWidget(button)

    def create_info_sections(self, layout):
        """Create information section groupboxes"""
        # OS Information
        self.os_group = QGroupBox("Operating System Information")
        os_layout = QVBoxLayout()
        self.os_info_label = QLabel()
        self.os_info_label.setTextFormat(Qt.TextFormat.RichText)
        os_layout.addWidget(self.os_info_label)
        self.os_group.setLayout(os_layout)
        layout.addWidget(self.os_group)
        
        # Hardware Information
        self.hardware_group = QGroupBox("Hardware Information")
        hardware_layout = QVBoxLayout()
        self.hardware_info_label = QLabel()
        self.hardware_info_label.setTextFormat(Qt.TextFormat.RichText)
        hardware_layout.addWidget(self.hardware_info_label)
        self.hardware_group.setLayout(hardware_layout)
        layout.addWidget(self.hardware_group)
        
        # Boot Information
        self.boot_group = QGroupBox("Boot Information")
        boot_layout = QVBoxLayout()
        self.boot_info_label = QLabel()
        self.boot_info_label.setTextFormat(Qt.TextFormat.RichText)
        boot_layout.addWidget(self.boot_info_label)
        self.boot_group.setLayout(boot_layout)
        layout.addWidget(self.boot_group)
        
        # Python Environment
        self.python_group = QGroupBox("Python Environment")
        python_layout = QVBoxLayout()
        self.python_info_label = QLabel()
        self.python_info_label.setTextFormat(Qt.TextFormat.RichText)
        python_layout.addWidget(self.python_info_label)
        self.python_group.setLayout(python_layout)
        layout.addWidget(self.python_group)
        
        # User Information
        self.user_group = QGroupBox("User Information")
        user_layout = QVBoxLayout()
        self.user_info_label = QLabel()
        self.user_info_label.setTextFormat(Qt.TextFormat.RichText)
        user_layout.addWidget(self.user_info_label)
        self.user_group.setLayout(user_layout)
        layout.addWidget(self.user_group)

    def update_info(self):
        """Update all information labels"""
        # Get system information
        info = self.system_monitor.get_all_info()
        
        # Update OS information
        os_info = info['os_info']
        os_text = (
            f"<b>OS Name:</b> {os.name}<br>"
            f"<b>System Name:</b> {os_info['system']}<br>"
            f"<b>OS Version:</b> {os_info['version']}<br>"
            f"<b>Release:</b> {os_info['release']}<br>"
            f"<b>Machine Type:</b> {os_info['machine']}<br>"
            f"<b>Architecture:</b> {os_info['architecture'][0]} ({os_info['architecture'][1]})<br>"
            f"<b>Node/Hostname:</b> {os_info['node']}<br>"
            f"<b>Platform:</b> {os_info['platform']}"
        )
        self.os_info_label.setText(os_text)
        
        # Update Hardware information
        hardware_info = (
            f"<b>Processor:</b> {os_info['processor']}<br>"
            f"<b>Number of CPUs:</b> {psutil.cpu_count()} (Physical: {psutil.cpu_count(logical=False)})<br>"
            f"<b>System Architecture:</b> {os_info['architecture'][0]}<br>"
            f"<b>CPU Usage:</b> {psutil.cpu_percent()}%"
        )
        self.hardware_info_label.setText(hardware_info)
        
        # Update boot information
        boot_timestamp = info['boot_time']
        boot_time = datetime.fromtimestamp(boot_timestamp)
        current_time = datetime.now()
        uptime = current_time - boot_time
        
        boot_text = (
            f"<b>Boot Time:</b> {boot_time.strftime('%Y-%m-%d %H:%M:%S')}<br>"
            f"<b>System Uptime:</b> {str(uptime).split('.')[0]}"
        )
        self.boot_info_label.setText(boot_text)
        
        # Update Python information
        python_info = (
            f"<b>Python Version:</b> {platform.python_version()}<br>"
            f"<b>Python Implementation:</b> {platform.python_implementation()}<br>"
            f"<b>Python Compiler:</b> {platform.python_compiler()}<br>"
            f"<b>Python Build:</b> {platform.python_build()[0]} ({platform.python_build()[1]})"
        )
        self.python_info_label.setText(python_info)
        
        # Update user information
        users = info['users']
        users_text = "<b>Logged in users:</b><br>"
        for user in users:
            users_text += f"""
            <b>User:</b> {user['name']}<br>
            <b>Terminal:</b> {user['terminal']}<br>
            <b>Host:</b> {user['host']}<br>
            <b>Started:</b> {datetime.fromtimestamp(user['started']).strftime('%Y-%m-%d %H:%M:%S')}<br>
            <br>"""
        self.user_info_label.setText(users_text)

    def show_cpu_monitor(self):
        if not self.monitor_windows['cpu']:
            self.monitor_windows['cpu'] = CPUWindow()
        self.monitor_windows['cpu'].show()
        self.monitor_windows['cpu'].activateWindow()
        
    def show_memory_monitor(self):
        if not self.monitor_windows['memory']:
            self.monitor_windows['memory'] = MemoryWindow()
        self.monitor_windows['memory'].show()
        self.monitor_windows['memory'].activateWindow()

    def show_storage_monitor(self):
        if not self.monitor_windows['storage']:
            self.monitor_windows['storage'] = StorageWindow()
        self.monitor_windows['storage'].show()
        self.monitor_windows['storage'].activateWindow()
        
    def show_network_monitor(self):
        if not self.monitor_windows['network']:
            self.monitor_windows['network'] = NetworkWindow()
        self.monitor_windows['network'].show()
        self.monitor_windows['network'].activateWindow()
        
    def show_process_monitor(self):
        if not self.monitor_windows['process']:
            self.monitor_windows['process'] = ProcessWindow()
        self.monitor_windows['process'].show()
        self.monitor_windows['process'].activateWindow()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()