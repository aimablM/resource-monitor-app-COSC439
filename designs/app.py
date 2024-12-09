from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QGroupBox, QLabel, QScrollArea, QApplication,
                           QPushButton)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QFont
import platform
import psutil
import os
from datetime import datetime
from monitor_windows.cpu_window import CPUWindow
from monitor_windows.memory_window import MemoryWindow
from monitor_windows.storage_window import StorageWindow
from monitor_windows.process_window import ProcessWindow
from monitor_windows.network_window import NetworkWindow

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

class SystemInfoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Your System Info Buddy")
        self.setMinimumSize(800, 600)

        self.setWindowIcon(create_emoji_icon('💻'))
        
        # Initialize monitor windows dictionary
        self.monitor_windows = {
            'cpu': None,
            'memory': None,
            'storage': None,
            'network': None,
            'process': None
        }
        
        # Create a scroll area to handle overflow
        scroll = QScrollArea()
        self.setCentralWidget(scroll)
        
        # Create main widget and layout
        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Add welcome header
        self.create_welcome_header(layout)
        
        # Add navigation buttons
        self.create_navigation_buttons(layout)
        
        # Create information sections
        self.create_os_info_group(layout)
        self.create_hardware_info_group(layout)
        self.create_boot_info_group(layout)
        self.create_python_info_group(layout)
        
        # Add credits footer
        self.create_credits_footer(layout)
        
        # Make the scroll area display our widget
        scroll.setWidget(main_widget)
        scroll.setWidgetResizable(True)
        
        # Set up periodic updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_dynamic_info)
        self.timer.start(1000)  # Update every second
        
        # Initial update
        self.update_dynamic_info()

    def create_navigation_buttons(self, parent_layout):
        """Create navigation button section"""
        nav_group = QGroupBox("Detailed Monitors")
        nav_layout = QHBoxLayout()
        
        # Define buttons with their respective window classes
        buttons = [
            ("CPU Monitor", 'cpu', CPUWindow),
            ("Memory Monitor", 'memory', MemoryWindow),
            ("Storage Monitor", 'storage', StorageWindow),
            ("Process Monitor", 'process', ProcessWindow),
            ("Network Monitor", 'network', NetworkWindow)
        ]
        
        for btn_text, key, window_class in buttons:
            button = QPushButton(btn_text)
            button.clicked.connect(lambda checked, k=key, w=window_class: self.show_monitor_window(k, w))
            nav_layout.addWidget(button)
        
        nav_group.setLayout(nav_layout)
        parent_layout.addWidget(nav_group)

    def show_monitor_window(self, key, window_class):
        """Show or create and show a monitor window"""
        if not self.monitor_windows[key]:
            self.monitor_windows[key] = window_class()
        self.monitor_windows[key].show()
        self.monitor_windows[key].activateWindow()

    def create_welcome_header(self, parent_layout):
        """Create a friendly welcome header"""
        header = QLabel("Hi there! Let me tell you about your system!")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        parent_layout.addWidget(header)

    def create_credits_footer(self, parent_layout):
        """Create a credits footer"""
        footer = QLabel("Designed and built by Aimable M and Jash M")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        parent_layout.addWidget(footer)

    def create_group_box(self, title):
        """Helper method to create basic group boxes"""
        group = QGroupBox(title)
        return group

    def create_info_label(self):
        """Helper method to create basic labels"""
        label = QLabel()
        label.setTextFormat(Qt.TextFormat.RichText)
        return label

    def create_os_info_group(self, parent_layout):
        """Create Operating System Information group"""
        group = self.create_group_box("Operating System Information")
        layout = QVBoxLayout()
        self.os_info_label = self.create_info_label()
        layout.addWidget(self.os_info_label)
        group.setLayout(layout)
        parent_layout.addWidget(group)

    def create_hardware_info_group(self, parent_layout):
        """Create Hardware Information group"""
        group = self.create_group_box("Hardware Information")
        layout = QVBoxLayout()
        self.hardware_info_label = self.create_info_label()
        layout.addWidget(self.hardware_info_label)
        group.setLayout(layout)
        parent_layout.addWidget(group)

    def create_boot_info_group(self, parent_layout):
        """Create Boot Information group"""
        group = self.create_group_box("System Boot Information")
        layout = QVBoxLayout()
        self.boot_info_label = self.create_info_label()
        layout.addWidget(self.boot_info_label)
        group.setLayout(layout)
        parent_layout.addWidget(group)

    def create_python_info_group(self, parent_layout):
        """Create Python Environment Information group"""
        group = self.create_group_box("Python Environment")
        layout = QVBoxLayout()
        self.python_info_label = self.create_info_label()
        layout.addWidget(self.python_info_label)
        group.setLayout(layout)
        parent_layout.addWidget(group)

    def update_dynamic_info(self):
        """Update all dynamic information"""
        # Update OS Information
        os_info = (
            f"<b>OS Name:</b> {os.name}<br>"
            f"<b>System Name:</b> {platform.system()}<br>"
            f"<b>OS Version:</b> {platform.version()}<br>"
            f"<b>Release:</b> {platform.release()}<br>"
            f"<b>Machine Type:</b> {platform.machine()}<br>"
            f"<b>Architecture:</b> {platform.architecture()[0]} ({platform.architecture()[1]})<br>"
            f"<b>Node/Hostname:</b> {platform.node()}<br>"
            f"<b>Platform:</b> {platform.platform()}"
        )
        self.os_info_label.setText(os_info)

        # Update Hardware Information
        hardware_info = (
            f"<b>Processor:</b> {platform.processor()}<br>"
            f"<b>Number of CPUs:</b> {psutil.cpu_count()} (Physical: {psutil.cpu_count(logical=False)})<br>"
            f"<b>System Architecture:</b> {platform.architecture()[0]}<br>"
            f"<b>CPU Usage:</b> {psutil.cpu_percent()}%"
        )
        self.hardware_info_label.setText(hardware_info)

        # Update Boot Information
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot_time
        boot_info = (
            f"<b>Boot Time:</b> {boot_time.strftime('%Y-%m-%d %H:%M:%S')}<br>"
            f"<b>System Uptime:</b> {str(uptime).split('.')[0]}"
        )
        self.boot_info_label.setText(boot_info)

        # Update Python Information
        python_info = (
            f"<b>Python Version:</b> {platform.python_version()}<br>"
            f"<b>Python Implementation:</b> {platform.python_implementation()}<br>"
            f"<b>Python Compiler:</b> {platform.python_compiler()}<br>"
            f"<b>Python Build:</b> {platform.python_build()[0]} ({platform.python_build()[1]})"
        )
        self.python_info_label.setText(python_info)

def main():
    app = QApplication([])
    window = SystemInfoWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()