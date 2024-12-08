from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QGroupBox
from PyQt6.QtCore import QTimer
from monitors.network_monitor import NetworkMonitor

class NetworkWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Network Monitor")
        self.setMinimumSize(500, 400)
        
        # Initialize network monitor
        self.network_monitor = NetworkMonitor()
        
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
        """Create network information sections"""
        # Network IO
        self.io_group = QGroupBox("Network I/O")
        io_layout = QVBoxLayout()
        self.io_label = QLabel()
        io_layout.addWidget(self.io_label)
        self.io_group.setLayout(io_layout)
        layout.addWidget(self.io_group)
        
        # Network Connections
        self.connections_group = QGroupBox("Network Connections")
        connections_layout = QVBoxLayout()
        self.connections_label = QLabel()
        connections_layout.addWidget(self.connections_label)
        self.connections_group.setLayout(connections_layout)
        layout.addWidget(self.connections_group)
        
    def format_bytes(self, bytes):
        """Convert bytes to human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes < 1024:
                return f"{bytes:.2f} {unit}"
            bytes /= 1024
            
    def update_info(self):
        """Update all network information"""
        # Get network info
        network_info = self.network_monitor.get_all_info()
        
        # Update IO statistics
        io = network_info['io']
        io_text = f"""
        Bytes Sent: {self.format_bytes(io['bytes_sent'])}
        Bytes Received: {self.format_bytes(io['bytes_recv'])}
        Packets Sent: {io['packets_sent']}
        Packets Received: {io['packets_recv']}
        """
        self.io_label.setText(io_text)
        
        # Update connections
        connections = network_info['connections']
        if connections:
            conn_text = "Active Connections:\n"
            for conn in connections[:10]:  # Show first 10 connections
                local = f"{conn['local_addr'][0]}:{conn['local_addr'][1]}" if conn['local_addr'] else "N/A"
                remote = f"{conn['remote_addr'][0]}:{conn['remote_addr'][1]}" if conn['remote_addr'] else "N/A"
                conn_text += f"\nStatus: {conn['status']}\n"
                conn_text += f"Local: {local}\n"
                conn_text += f"Remote: {remote}\n"
                conn_text += "-" * 30
        else:
            conn_text = "No active connections"
        self.connections_label.setText(conn_text)