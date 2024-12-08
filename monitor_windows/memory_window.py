from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QGroupBox, QProgressBar
from PyQt6.QtCore import QTimer
from monitors.memory_monitor import MemoryMonitor

class MemoryWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Memory Monitor")
        self.setMinimumSize(400, 300)
        
        # Initialize memory monitor
        self.memory_monitor = MemoryMonitor()
        
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
        """Create memory information sections"""
        # RAM Usage
        self.ram_group = QGroupBox("RAM Usage")
        ram_layout = QVBoxLayout()
        
        self.ram_percent = QProgressBar()
        self.ram_details = QLabel()
        
        ram_layout.addWidget(self.ram_percent)
        ram_layout.addWidget(self.ram_details)
        self.ram_group.setLayout(ram_layout)
        layout.addWidget(self.ram_group)
        
        # Swap Usage
        self.swap_group = QGroupBox("Swap Memory")
        swap_layout = QVBoxLayout()
        
        self.swap_percent = QProgressBar()
        self.swap_details = QLabel()
        
        swap_layout.addWidget(self.swap_percent)
        swap_layout.addWidget(self.swap_details)
        self.swap_group.setLayout(swap_layout)
        layout.addWidget(self.swap_group)
        
    def format_bytes(self, bytes):
        """Convert bytes to human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes < 1024:
                return f"{bytes:.2f} {unit}"
            bytes /= 1024
        
    def update_info(self):
        """Update all memory information"""
        # Get memory info
        memory_info = self.memory_monitor.get_all_info()
        
        # Update RAM usage
        ram = memory_info['ram']
        self.ram_percent.setValue(int(ram['percent']))  # Convert to integer
        ram_text = f"""
        Total: {self.format_bytes(ram['total'])}
        Used: {self.format_bytes(ram['used'])}
        Available: {self.format_bytes(ram['available'])}
        Free: {self.format_bytes(ram['free'])}
        """
        self.ram_details.setText(ram_text)
        
        # Update Swap usage
        swap = memory_info['swap']
        self.swap_percent.setValue(int(swap['percent']))  # Convert to integer
        swap_text = f"""
        Total: {self.format_bytes(swap['total'])}
        Used: {self.format_bytes(swap['used'])}
        Free: {self.format_bytes(swap['free'])}
        """
        self.swap_details.setText(swap_text)