from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QGroupBox, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import QTimer
from monitors.process_monitor import ProcessMonitor

class ProcessWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Process Monitor")
        self.setMinimumSize(800, 600)
        
        # Initialize process monitor
        self.process_monitor = ProcessMonitor()
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Create info sections
        self.create_info_sections(layout)
        
        # Set up timer for updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_info)
        self.timer.start(2000)  # Update every 2 seconds
        
        # Initial update
        self.update_info()
        
    def create_info_sections(self, layout):
        """Create process information sections"""
        # Process count
        self.count_group = QGroupBox("Process Statistics")
        count_layout = QVBoxLayout()
        self.count_label = QLabel()
        count_layout.addWidget(self.count_label)
        self.count_group.setLayout(count_layout)
        layout.addWidget(self.count_group)
        
        # Process table
        self.table_group = QGroupBox("Running Processes")
        table_layout = QVBoxLayout()
        
        # Create table
        self.process_table = QTableWidget()
        self.process_table.setColumnCount(4)
        self.process_table.setHorizontalHeaderLabels([
            "PID", "Name", "CPU %", "Memory %"
        ])
        table_layout.addWidget(self.process_table)
        
        self.table_group.setLayout(table_layout)
        layout.addWidget(self.table_group)
            
    def update_info(self):
        """Update all process information"""
        # Get process info
        process_info = self.process_monitor.get_all_info()
        
        # Update process count
        self.count_label.setText(f"Total Processes: {process_info['total_count']}")
        
        # Update process table
        processes = process_info['processes']
        # Sort processes by CPU usage
        processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
        
        # Update table
        self.process_table.setRowCount(len(processes))
        for i, proc in enumerate(processes):
            # PID
            self.process_table.setItem(i, 0, QTableWidgetItem(str(proc['pid'])))
            # Name
            self.process_table.setItem(i, 1, QTableWidgetItem(proc['name']))
            # CPU %
            self.process_table.setItem(i, 2, QTableWidgetItem(f"{proc['cpu_percent']:.1f}"))
            # Memory %
            self.process_table.setItem(i, 3, QTableWidgetItem(f"{proc['memory_percent']:.1f}"))
        
        # Resize columns to content
        self.process_table.resizeColumnsToContents()