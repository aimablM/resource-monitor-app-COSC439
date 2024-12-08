from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QGroupBox, QProgressBar
from PyQt6.QtCore import QTimer
from monitors.storage_monitor import StorageMonitor

class StorageWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Storage Monitor")
        self.setMinimumSize(500, 400)
        
        # Initialize storage monitor
        self.storage_monitor = StorageMonitor()
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Create info sections
        self.create_info_sections(layout)
        
        # Set up timer for updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_info)
        self.timer.start(1000)  # Update every second
        
        # Initial update
        self.update_info()
        
    def create_info_sections(self, layout):
        """Create storage information sections"""
        # Partitions Usage
        self.partitions_group = QGroupBox("Disk Partitions")
        partitions_layout = QVBoxLayout()
        self.partition_widgets = {}  # Store widgets for each partition
        self.partitions_group.setLayout(partitions_layout)
        layout.addWidget(self.partitions_group)
        
        # IO Statistics
        self.io_group = QGroupBox("Disk I/O Statistics")
        io_layout = QVBoxLayout()
        self.io_label = QLabel()
        io_layout.addWidget(self.io_label)
        self.io_group.setLayout(io_layout)
        layout.addWidget(self.io_group)
        
    def format_bytes(self, bytes):
        """Convert bytes to human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes < 1024:
                return f"{bytes:.2f} {unit}"
            bytes /= 1024
            
    def update_partition_widgets(self, partitions):
        """Update partition widgets based on current partitions"""
        # Clear existing widgets
        for widgets in self.partition_widgets.values():
            for widget in widgets:
                widget.setParent(None)
        self.partition_widgets.clear()
        
        # Create new widgets for each partition
        layout = self.partitions_group.layout()
        for partition in partitions:
            label = QLabel(f"Drive: {partition['device']} ({partition['mountpoint']})")
            progress = QProgressBar()
            progress.setValue(int(partition['percent']))
            details = QLabel(
                f"Total: {self.format_bytes(partition['total'])}\n"
                f"Used: {self.format_bytes(partition['used'])}\n"
                f"Free: {self.format_bytes(partition['free'])}"
            )
            
            layout.addWidget(label)
            layout.addWidget(progress)
            layout.addWidget(details)
            
            self.partition_widgets[partition['device']] = [label, progress, details]
        
    def update_info(self):
        """Update all storage information"""
        # Get storage info
        storage_info = self.storage_monitor.get_all_info()
        
        # Update partitions
        self.update_partition_widgets(storage_info['partitions'])
        
        # Update IO statistics
        io = storage_info['io']
        io_text = f"""
        Read:
        - Total: {self.format_bytes(io['read_bytes'])}
        - Count: {io['read_count']} operations
        
        Write:
        - Total: {self.format_bytes(io['write_bytes'])}
        - Count: {io['write_count']} operations
        """
        self.io_label.setText(io_text)