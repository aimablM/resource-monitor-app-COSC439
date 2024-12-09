from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QLabel, QGroupBox, QProgressBar, QScrollArea)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon, QFont, QPainter, QPixmap
from monitors.storage_monitor import StorageMonitor
from monitor_windows.utils import create_emoji_icon

class StorageWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Storage Monitor")
        self.setMinimumSize(600, 800)
        self.setWindowIcon(create_emoji_icon('💾'))
        
        # Initialize storage monitor
        self.storage_monitor = StorageMonitor()
        
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
        
        # Dictionary to store partition widgets
        self.partition_widgets = {}
        
        # Set up timer for updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_info)
        self.timer.start(1000)  # Update every second
        
        # Initial update
        self.update_info()

    def create_welcome_header(self, layout):
        """Create welcome header"""
        header = QLabel("Storage Monitor - Disk Space and I/O Stats")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)

    def create_credits_footer(self, layout):
        """Create credits footer"""
        footer = QLabel("Designed and built by Aimable M and Jash M")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(footer)

    def create_info_sections(self, layout):
        """Create storage information sections"""
        # Partitions section
        self.partitions_group = QGroupBox("Disk Partitions")
        self.partitions_layout = QVBoxLayout()
        self.partitions_group.setLayout(self.partitions_layout)
        layout.addWidget(self.partitions_group)
        
        # I/O Statistics section
        self.io_group = QGroupBox("Disk I/O Statistics")
        io_layout = QVBoxLayout()
        
        # Create read/write stats displays
        stats_layout = QHBoxLayout()
        
        # Read stats
        read_layout = QVBoxLayout()
        self.read_speed_label = QLabel("Read Speed")
        self.read_speed_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.read_total_label = QLabel("Total Read")
        self.read_total_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        read_layout.addWidget(self.read_speed_label)
        read_layout.addWidget(self.read_total_label)
        
        # Write stats
        write_layout = QVBoxLayout()
        self.write_speed_label = QLabel("Write Speed")
        self.write_speed_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.write_total_label = QLabel("Total Written")
        self.write_total_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        write_layout.addWidget(self.write_speed_label)
        write_layout.addWidget(self.write_total_label)
        
        stats_layout.addLayout(read_layout)
        stats_layout.addLayout(write_layout)
        
        # Add detailed I/O info label
        self.io_details_label = QLabel()
        self.io_details_label.setTextFormat(Qt.TextFormat.RichText)
        
        io_layout.addLayout(stats_layout)
        io_layout.addWidget(self.io_details_label)
        self.io_group.setLayout(io_layout)
        layout.addWidget(self.io_group)
        
        # Performance Metrics section
        self.performance_group = QGroupBox("Storage Performance Metrics")
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

    def create_partition_widget(self, partition):
        """Create or update widgets for a partition"""
        device = partition['device']
        if device not in self.partition_widgets:
            # Create new widgets for this partition
            group = QGroupBox(f"Partition: {device} ({partition['mountpoint']})")
            layout = QVBoxLayout()
            
            # Progress bar for usage
            progress = QProgressBar()
            progress.setMinimum(0)
            progress.setMaximum(100)
            
            # Labels for details
            details = QLabel()
            details.setTextFormat(Qt.TextFormat.RichText)
            
            layout.addWidget(progress)
            layout.addWidget(details)
            group.setLayout(layout)
            
            self.partition_widgets[device] = {
                'group': group,
                'progress': progress,
                'details': details
            }
            
            self.partitions_layout.addWidget(group)
        
        # Update widgets with current values
        widgets = self.partition_widgets[device]
        widgets['progress'].setValue(int(partition['percent']))
        
        details_text = (
            f"<b>Filesystem:</b> {partition['fstype']}<br>"
            f"<b>Mount Point:</b> {partition['mountpoint']}<br>"
            f"<b>Total Space:</b> {self.format_bytes(partition['total'])}<br>"
            f"<b>Used Space:</b> {self.format_bytes(partition['used'])} "
            f"({partition['percent']}%)<br>"
            f"<b>Free Space:</b> {self.format_bytes(partition['free'])}"
        )
        widgets['details'].setText(details_text)

    def calculate_speed(self, current_bytes, prev_bytes, interval):
        #Calculate bytes per second
        return (current_bytes - prev_bytes) / interval if prev_bytes is not None else 0

    def update_info(self):
        #Update all storage information
        # Store previous I/O values for speed calculation
        self.prev_io = getattr(self, 'current_io', None)
        self.prev_time = getattr(self, 'current_time', None)
        
        # Get current storage info
        storage_info = self.storage_monitor.get_all_info()
        
        # Update partition information
        current_devices = set()
        for partition in storage_info['partitions']:
            self.create_partition_widget(partition)
            current_devices.add(partition['device'])
        
        # Remove widgets for partitions that no longer exist
        for device in list(self.partition_widgets.keys()):
            if device not in current_devices:
                self.partition_widgets[device]['group'].deleteLater()
                del self.partition_widgets[device]
        
        # Update I/O statistics
        io_info = storage_info['io']
        
        # Calculate read/write speeds
        if self.prev_io and self.prev_time:
            interval = 1  # Update interval in seconds
            read_speed = self.calculate_speed(
                io_info['read_bytes'], 
                self.prev_io['read_bytes'],
                interval
            )
            write_speed = self.calculate_speed(
                io_info['write_bytes'],
                self.prev_io['write_bytes'],
                interval
            )
            
            self.read_speed_label.setText(
                f"Read Speed:\n{self.format_bytes(read_speed)}/s"
            )
            self.write_speed_label.setText(
                f"Write Speed:\n{self.format_bytes(write_speed)}/s"
            )
        
        # Update total read/write
        self.read_total_label.setText(
            f"Total Read:\n{self.format_bytes(io_info['read_bytes'])}"
        )
        self.write_total_label.setText(
            f"Total Written:\n{self.format_bytes(io_info['write_bytes'])}"
        )
        
        # Update detailed I/O info
        io_details = (
            f"<b>Read Operations:</b> {io_info['read_count']}<br>"
            f"<b>Write Operations:</b> {io_info['write_count']}<br>"
        )
        self.io_details_label.setText(io_details)
        
        # Update performance metrics
        total_space = sum(p['total'] for p in storage_info['partitions'])
        used_space = sum(p['used'] for p in storage_info['partitions'])
        overall_usage = (used_space / total_space * 100) if total_space > 0 else 0
        
        performance_text = (
            f"<b>Overall Storage Usage:</b> {overall_usage:.1f}%<br>"
            f"<b>Total Storage Space:</b> {self.format_bytes(total_space)}<br>"
            f"<b>Total Used Space:</b> {self.format_bytes(used_space)}<br>"
            f"<b>Storage Status:</b> "
            f"{'Critical' if overall_usage > 90 else 'Warning' if overall_usage > 80 else 'Normal'}"
        )
        self.performance_label.setText(performance_text)
        
        # Store current I/O values for next update
        self.current_io = io_info