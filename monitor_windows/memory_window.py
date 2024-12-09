from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QLabel, QGroupBox, QProgressBar, QScrollArea)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon, QFont, QPainter, QPixmap
from monitors.memory_monitor import MemoryMonitor
from monitor_windows.utils import create_emoji_icon

class MemoryWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Memory Monitor")
        self.setMinimumSize(600, 800)
        self.setWindowIcon(create_emoji_icon('🧠'))
        
        # Initialize memory monitor
        self.memory_monitor = MemoryMonitor()
        
        # Create scroll area
        scroll = QScrollArea()
        self.setCentralWidget(scroll)
        
        # Create main widget and layout
        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Add welcome header
        self.create_welcome_header(layout)
        
        # Create info sections
        self.create_info_sections(layout)
        
        # Add credits footer
        self.create_credits_footer(layout)
        
        # Make the scroll area display our widget
        scroll.setWidget(main_widget)
        scroll.setWidgetResizable(True)
        
        # Set up timer for updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_info)
        self.timer.start(1000)  # Update every second
        
        # Initial update
        self.update_info()

    def create_welcome_header(self, layout):
        """Create welcome header"""
        header = QLabel("Memory Monitor - RAM and Swap Usage Stats")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)

    def create_credits_footer(self, layout):
        """Create credits footer"""
        footer = QLabel("Designed and built by Aimable M and Jash M")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(footer)

    def create_info_sections(self, layout):
        """Create memory information sections"""
        # RAM Usage Overview
        self.ram_group = QGroupBox("RAM Usage Overview")
        ram_layout = QVBoxLayout()
        
        # Add RAM usage progress bar
        self.ram_bar = QProgressBar()
        self.ram_bar.setMinimum(0)
        self.ram_bar.setMaximum(100)
        ram_layout.addWidget(self.ram_bar)
        
        # Add RAM usage details
        self.ram_details = QLabel()
        self.ram_details.setTextFormat(Qt.TextFormat.RichText)
        ram_layout.addWidget(self.ram_details)
        
        self.ram_group.setLayout(ram_layout)
        layout.addWidget(self.ram_group)
        
        # RAM Distribution
        self.distribution_group = QGroupBox("Memory Distribution")
        distribution_layout = QVBoxLayout()
        
        # Create bars for different memory types
        self.used_bar = QProgressBar()
        self.used_bar.setMinimum(0)
        self.used_bar.setMaximum(100)
        
        self.available_bar = QProgressBar()
        self.available_bar.setMinimum(0)
        self.available_bar.setMaximum(100)
        
        self.free_bar = QProgressBar()
        self.free_bar.setMinimum(0)
        self.free_bar.setMaximum(100)
        
        # Add labels and bars to layout
        for label_text, bar in [
            ("Used Memory:", self.used_bar),
            ("Available Memory:", self.available_bar),
            ("Free Memory:", self.free_bar)
        ]:
            bar_layout = QHBoxLayout()
            label = QLabel(label_text)
            label.setMinimumWidth(120)
            bar_layout.addWidget(label)
            bar_layout.addWidget(bar)
            distribution_layout.addLayout(bar_layout)
        
        self.distribution_details = QLabel()
        self.distribution_details.setTextFormat(Qt.TextFormat.RichText)
        distribution_layout.addWidget(self.distribution_details)
        
        self.distribution_group.setLayout(distribution_layout)
        layout.addWidget(self.distribution_group)
        
        # Swap Memory
        self.swap_group = QGroupBox("Swap Memory")
        swap_layout = QVBoxLayout()
        
        # Add swap usage progress bar
        self.swap_bar = QProgressBar()
        self.swap_bar.setMinimum(0)
        self.swap_bar.setMaximum(100)
        swap_layout.addWidget(self.swap_bar)
        
        # Add swap details
        self.swap_details = QLabel()
        self.swap_details.setTextFormat(Qt.TextFormat.RichText)
        swap_layout.addWidget(self.swap_details)
        
        self.swap_group.setLayout(swap_layout)
        layout.addWidget(self.swap_group)
        
        # Memory Performance
        self.performance_group = QGroupBox("Memory Performance Metrics")
        performance_layout = QVBoxLayout()
        self.performance_label = QLabel()
        self.performance_label.setTextFormat(Qt.TextFormat.RichText)
        performance_layout.addWidget(self.performance_label)
        self.performance_group.setLayout(performance_layout)
        layout.addWidget(self.performance_group)

    def format_bytes(self, bytes_value):
        """Convert bytes to human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024:
                return f"{bytes_value:.2f} {unit}"
            bytes_value /= 1024

    def update_info(self):
        """Update all memory information"""
        # Get memory info
        memory_info = self.memory_monitor.get_all_info()
        ram_info = memory_info['ram']
        swap_info = memory_info['swap']
        
        # Update RAM Overview
        self.ram_bar.setValue(int(ram_info['percent']))
        ram_text = (
            f"<b>Total RAM:</b> {self.format_bytes(ram_info['total'])}<br>"
            f"<b>Current Usage:</b> {ram_info['percent']}%"
        )
        self.ram_details.setText(ram_text)
        
        # Update Memory Distribution
        total = ram_info['total']
        
        # Update used memory
        used_percent = (ram_info['used'] / total) * 100
        self.used_bar.setValue(int(used_percent))
        
        # Update available memory
        available_percent = (ram_info['available'] / total) * 100
        self.available_bar.setValue(int(available_percent))
        
        # Update free memory
        free_percent = (ram_info['free'] / total) * 100
        self.free_bar.setValue(int(free_percent))
        
        distribution_text = (
            f"<b>Used:</b> {self.format_bytes(ram_info['used'])} "
            f"({used_percent:.1f}%)<br>"
            f"<b>Available:</b> {self.format_bytes(ram_info['available'])} "
            f"({available_percent:.1f}%)<br>"
            f"<b>Free:</b> {self.format_bytes(ram_info['free'])} "
            f"({free_percent:.1f}%)"
        )
        self.distribution_details.setText(distribution_text)
        
        # Update Swap Information
        self.swap_bar.setValue(int(swap_info['percent']))
        swap_text = (
            f"<b>Total Swap:</b> {self.format_bytes(swap_info['total'])}<br>"
            f"<b>Used Swap:</b> {self.format_bytes(swap_info['used'])} "
            f"({swap_info['percent']}%)<br>"
            f"<b>Free Swap:</b> {self.format_bytes(swap_info['free'])}"
        )
        self.swap_details.setText(swap_text)
        
        # Update Performance Metrics
        # You can add additional metrics here if your MemoryMonitor provides them
        performance_text = (
            f"<b>Memory Usage Trend:</b> "
            f"{'Increasing' if ram_info['percent'] > 80 else 'Stable'}<br>"
            f"<b>Swap Usage Status:</b> "
            f"{'High' if swap_info['percent'] > 50 else 'Normal'}<br>"
            f"<b>Available Memory Status:</b> "
            f"{'Low' if available_percent < 20 else 'Adequate'}"
        )
        self.performance_label.setText(performance_text)