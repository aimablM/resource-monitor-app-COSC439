from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QLabel, QGroupBox, QProgressBar, QScrollArea)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon, QFont, QPainter, QPixmap
from monitors.cpu_monitor import CPUMonitor
from monitor_windows.utils import create_emoji_icon

class CPUWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CPU Monitor")
        self.setMinimumSize(600, 800)
        self.setWindowIcon(create_emoji_icon('⚡'))
        
        # Initialize CPU monitor
        self.cpu_monitor = CPUMonitor()
        
        # Create scroll area for content
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
        header = QLabel("CPU Monitor - Real-time Processing Power Stats")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)

    def create_credits_footer(self, layout):
        """Create credits footer"""
        footer = QLabel("Designed and built by Aimable M and Jash M")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(footer)
        
    def create_info_sections(self, layout):
        """Create CPU information sections"""
        # Overall CPU Usage
        self.usage_group = QGroupBox("Overall CPU Usage")
        usage_layout = QVBoxLayout()
        
        # Add progress bar for total CPU usage
        self.total_usage_bar = QProgressBar()
        self.total_usage_bar.setMinimum(0)
        self.total_usage_bar.setMaximum(100)
        usage_layout.addWidget(self.total_usage_bar)
        
        self.usage_label = QLabel()
        self.usage_label.setTextFormat(Qt.TextFormat.RichText)
        usage_layout.addWidget(self.usage_label)
        
        self.usage_group.setLayout(usage_layout)
        layout.addWidget(self.usage_group)
        
        # Per-Core Usage
        self.cores_group = QGroupBox("Per-Core Usage")
        cores_layout = QVBoxLayout()
        
        # Create widgets for each CPU core
        self.core_bars = []
        self.core_labels = []
        
        for i in range(self.cpu_monitor.get_cpu_count()['logical']):
            core_layout = QHBoxLayout()
            
            # Create label for core number
            label = QLabel(f"Core {i + 1}:")
            label.setMinimumWidth(70)
            core_layout.addWidget(label)
            
            # Create progress bar for core usage
            bar = QProgressBar()
            bar.setMinimum(0)
            bar.setMaximum(100)
            core_layout.addWidget(bar)
            
            # Create label for percentage
            percent_label = QLabel()
            percent_label.setMinimumWidth(50)
            core_layout.addWidget(percent_label)
            
            cores_layout.addLayout(core_layout)
            self.core_bars.append(bar)
            self.core_labels.append(percent_label)
            
        self.cores_group.setLayout(cores_layout)
        layout.addWidget(self.cores_group)
        
        # CPU Information
        self.info_group = QGroupBox("CPU Information")
        info_layout = QVBoxLayout()
        self.info_label = QLabel()
        self.info_label.setTextFormat(Qt.TextFormat.RichText)
        info_layout.addWidget(self.info_label)
        self.info_group.setLayout(info_layout)
        layout.addWidget(self.info_group)
        
        # CPU Frequency
        self.freq_group = QGroupBox("CPU Frequency")
        freq_layout = QVBoxLayout()
        self.freq_label = QLabel()
        self.freq_label.setTextFormat(Qt.TextFormat.RichText)
        freq_layout.addWidget(self.freq_label)
        self.freq_group.setLayout(freq_layout)
        layout.addWidget(self.freq_group)
        
    def update_info(self):
        """Update all CPU information"""
        # Get CPU info
        cpu_info = self.cpu_monitor.get_all_info()
        
        # Update overall usage
        total_usage = cpu_info['usage']['total']
        self.total_usage_bar.setValue(int(total_usage))
        self.usage_label.setText(f"<b>Total CPU Usage: {total_usage}%</b>")
        
        # Update per-core usage
        for i, (bar, label, percentage) in enumerate(zip(
            self.core_bars, 
            self.core_labels, 
            cpu_info['usage']['per_cpu']
        )):
            bar.setValue(int(percentage))
            label.setText(f"{percentage:.1f}%")
        
        # Update CPU information
        cores = cpu_info['cores']
        info_text = (
            f"<b>Physical cores:</b> {cores['physical']}<br>"
            f"<b>Logical cores:</b> {cores['logical']}<br>"
            f"<b>Max threads per core:</b> {cores['logical'] // cores['physical']}"
        )
        self.info_label.setText(info_text)
        
        # Update frequency
        if cpu_info['frequency']:
            freq_text = (
                f"<b>Current Frequency:</b> {cpu_info['frequency']['current']:.1f} MHz<br>"
                f"<b>Minimum Frequency:</b> {cpu_info['frequency']['min']:.1f} MHz<br>"
                f"<b>Maximum Frequency:</b> {cpu_info['frequency']['max']:.1f} MHz"
            )
            self.freq_label.setText(freq_text)