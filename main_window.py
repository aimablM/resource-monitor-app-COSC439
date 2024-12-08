# main_window.py
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QPushButton, QGroupBox)
from PyQt6.QtCore import QTimer
import sys
from datetime import datetime
from monitors.system_monitor import SystemMonitor
from monitor_windows.cpu_window import CPUWindow
from monitor_windows.memory_window import MemoryWindow
from monitor_windows.storage_window import StorageWindow
from monitor_windows.network_window import NetworkWindow
from monitor_windows.process_window import ProcessWindow 

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("System Resource Monitor")
        self.setMinimumSize(800, 600)
        
        # Initialize system monitor
        self.system_monitor = SystemMonitor()
        
        # Add this line to initialize monitor_windows dictionary
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
        
        # Create navigation buttons
        nav_layout = QHBoxLayout()
        self.create_nav_buttons(nav_layout)
        layout.addLayout(nav_layout)
        
        # Create info sections
        self.create_info_sections(layout)
        
        # Set up timer for updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_info)
        self.timer.start(5000)  # Update every 5 seconds
        
        # Initial update
        self.update_info()

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
        os_layout.addWidget(self.os_info_label)
        self.os_group.setLayout(os_layout)
        layout.addWidget(self.os_group)
        
        # Boot Information
        self.boot_group = QGroupBox("Boot Information")
        boot_layout = QVBoxLayout()
        self.boot_info_label = QLabel()
        boot_layout.addWidget(self.boot_info_label)
        self.boot_group.setLayout(boot_layout)
        layout.addWidget(self.boot_group)
        
        # User Information
        self.user_group = QGroupBox("User Information")
        user_layout = QVBoxLayout()
        self.user_info_label = QLabel()
        user_layout.addWidget(self.user_info_label)
        self.user_group.setLayout(user_layout)
        layout.addWidget(self.user_group)

    def update_info(self):
        """Update all information labels"""
        # Get system information
        info = self.system_monitor.get_all_info()
        
        # Update OS information
        os_info = info['os_info']
        os_text = f"""
        System: {os_info['system']}
        Release: {os_info['release']}
        Version: {os_info['version']}
        Machine: {os_info['machine']}
        """
        self.os_info_label.setText(os_text)
        
        # Update boot information
        boot_timestamp = info['boot_time']
        boot_time = datetime.fromtimestamp(boot_timestamp)
        current_time = datetime.now()
        uptime = current_time - boot_time
        
        boot_text = f"""
        Boot Time: {boot_time.strftime('%Y-%m-%d %H:%M:%S')}
        Uptime: {uptime}
        """
        self.boot_info_label.setText(boot_text)
        
        # Update user information
        users = info['users']
        users_text = "Logged in users:\n"
        for user in users:
            users_text += f"""
            User: {user['name']}
            Terminal: {user['terminal']}
            Host: {user['host']}
            Started: {datetime.fromtimestamp(user['started']).strftime('%Y-%m-%d %H:%M:%S')}
            \n"""
        self.user_info_label.setText(users_text)

    # Placeholder methods for monitor windows
    def show_cpu_monitor(self):
        print("CPU Monitor button clicked")
        if not self.monitor_windows['cpu']:
            self.monitor_windows['cpu'] = CPUWindow()
        self.monitor_windows['cpu'].show()
        self.monitor_windows['cpu'].activateWindow()
        
    def show_memory_monitor(self):
        print("Memory Monitor button clicked")
        if not self.monitor_windows['memory']:
            self.monitor_windows['memory'] = MemoryWindow()
        self.monitor_windows['memory'].show()
        self.monitor_windows['memory'].activateWindow()

    def show_storage_monitor(self):
        print("Storage Monitor button clicked")
        if not self.monitor_windows['storage']:
            self.monitor_windows['storage'] = StorageWindow()
        self.monitor_windows['storage'].show()
        self.monitor_windows['storage'].activateWindow()
        
    def show_network_monitor(self):
        print("Network Monitor button clicked")
        if not self.monitor_windows['network']:
            self.monitor_windows['network'] = NetworkWindow()
        self.monitor_windows['network'].show()
        self.monitor_windows['network'].activateWindow()
        
    def show_process_monitor(self):
        print("Process Monitor button clicked")
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