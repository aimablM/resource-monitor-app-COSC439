from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QGroupBox
from PyQt6.QtCore import QTimer
from monitors.cpu_monitor import CPUMonitor

class CPUWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CPU Monitor")
        self.setMinimumSize(400, 300)
        
        # Initialize CPU monitor
        self.cpu_monitor = CPUMonitor()
        
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
        """Create CPU information sections"""
        # Overall CPU Usage
        self.usage_group = QGroupBox("Overall CPU Usage")
        usage_layout = QVBoxLayout()
        self.usage_label = QLabel()
        usage_layout.addWidget(self.usage_label)
        self.usage_group.setLayout(usage_layout)
        layout.addWidget(self.usage_group)
        
        # Per-Core Usage
        self.cores_group = QGroupBox("Per-Core Usage")
        cores_layout = QVBoxLayout()
        self.core_labels = []
        for i in range(self.cpu_monitor.get_cpu_count()['logical']):
            label = QLabel()
            self.core_labels.append(label)
            cores_layout.addWidget(label)
        self.cores_group.setLayout(cores_layout)
        layout.addWidget(self.cores_group)
        
        # CPU Frequency
        self.freq_group = QGroupBox("CPU Frequency")
        freq_layout = QVBoxLayout()
        self.freq_label = QLabel()
        freq_layout.addWidget(self.freq_label)
        self.freq_group.setLayout(freq_layout)
        layout.addWidget(self.freq_group)
        
    def update_info(self):
        """Update all CPU information"""
        # Get CPU info
        cpu_info = self.cpu_monitor.get_all_info()
        
        # Update overall usage
        self.usage_label.setText(f"Total CPU Usage: {cpu_info['usage']['total']}%")
        
        # Update per-core usage
        for i, percentage in enumerate(cpu_info['usage']['per_cpu']):
            self.core_labels[i].setText(f"Core {i}: {percentage}%")
        
        # Update frequency
        if cpu_info['frequency']:
            freq_text = f"""
            Current: {cpu_info['frequency']['current']:.1f} MHz
            Min: {cpu_info['frequency']['min']:.1f} MHz
            Max: {cpu_info['frequency']['max']:.1f} MHz
            """
            self.freq_label.setText(freq_text)