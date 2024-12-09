from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QLabel, QGroupBox, QProgressBar, QScrollArea, QTableWidget,
                           QTableWidgetItem)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon, QFont, QPainter, QPixmap
from monitors.network_monitor import NetworkMonitor
import psutil
import socket
import subprocess
import platform
from monitor_windows.utils import create_emoji_icon

class NetworkWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Network Monitor")
        self.setMinimumSize(800, 600)
        self.setWindowIcon(create_emoji_icon('🌐'))
        
        # Initialize network monitor
        self.network_monitor = NetworkMonitor()
        
        # Store previous network stats for speed calculation
        self.prev_bytes_sent = 0
        self.prev_bytes_recv = 0
        
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

         # Create network interface section first
        self.create_interface_section(layout)
        
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
        header = QLabel("Network Monitor - Traffic and Connection Stats")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)

    def create_credits_footer(self, layout):
        """Create credits footer"""
        footer = QLabel("Designed and built by Aimable M and Jash M")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(footer)

    def create_info_sections(self, layout):
        """Create network information sections"""
        # Network Traffic Overview
        self.traffic_group = QGroupBox("Network Traffic Overview")
        traffic_layout = QVBoxLayout()
        
        # Upload speed display
        upload_layout = QHBoxLayout()
        upload_label = QLabel("Upload Speed:")
        upload_label.setMinimumWidth(100)
        self.upload_speed_label = QLabel()
        upload_layout.addWidget(upload_label)
        upload_layout.addWidget(self.upload_speed_label)
        traffic_layout.addLayout(upload_layout)
        
        # Download speed display
        download_layout = QHBoxLayout()
        download_label = QLabel("Download Speed:")
        download_label.setMinimumWidth(100)
        self.download_speed_label = QLabel()
        download_layout.addWidget(download_label)
        download_layout.addWidget(self.download_speed_label)
        traffic_layout.addLayout(download_layout)
        
        # Total traffic stats
        self.traffic_stats_label = QLabel()
        self.traffic_stats_label.setTextFormat(Qt.TextFormat.RichText)
        traffic_layout.addWidget(self.traffic_stats_label)
        
        self.traffic_group.setLayout(traffic_layout)
        layout.addWidget(self.traffic_group)
        
        # Network Connections
        self.connections_group = QGroupBox("Active Network Connections")
        connections_layout = QVBoxLayout()
        
        # Create connections table
        self.connections_table = QTableWidget()
        self.connections_table.setColumnCount(4)
        self.connections_table.setHorizontalHeaderLabels([
            "Local Address", "Remote Address", "Status", "Type"
        ])
        connections_layout.addWidget(self.connections_table)
        
        self.connections_group.setLayout(connections_layout)
        layout.addWidget(self.connections_group)
        
        # Network Performance
        self.performance_group = QGroupBox("Network Performance")
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

    def format_speed(self, bytes_per_sec):
        """Convert bytes per second to human readable format"""
        return f"{self.format_bytes(bytes_per_sec)}/s"

    def calculate_speed(self, current_bytes, previous_bytes):
        """Calculate bytes per second"""
        return current_bytes - previous_bytes
    
    def create_interface_section(self, layout):
        """Create network interface information section"""
        self.interface_group = QGroupBox("Network Interfaces")
        interface_layout = QVBoxLayout()
        
        # Add interface details table
        self.interface_table = QTableWidget()
        self.interface_table.setColumnCount(5)
        self.interface_table.setHorizontalHeaderLabels([
            "Interface", "IP Address", "Netmask", "MAC Address", "Status"
        ])
        interface_layout.addWidget(self.interface_table)
        
        # Add WiFi details section if available
        self.wifi_details = QLabel()
        self.wifi_details.setTextFormat(Qt.TextFormat.RichText)
        interface_layout.addWidget(self.wifi_details)
        
        self.interface_group.setLayout(interface_layout)
        layout.addWidget(self.interface_group)

    def get_wifi_info(self):
        """Get WiFi information based on the operating system"""
        wifi_info = {}
        
        try:
            if platform.system() == "Windows":
                # Windows WiFi info using netsh
                output = subprocess.check_output(
                    ["netsh", "wlan", "show", "interfaces"],
                    universal_newlines=True
                )
                for line in output.split('\n'):
                    if ': ' in line:
                        key, value = line.split(': ', 1)
                        key = key.strip()
                        value = value.strip()
                        wifi_info[key] = value
                        
            elif platform.system() == "Linux":
                # Linux WiFi info using iwconfig
                try:
                    output = subprocess.check_output(
                        ["iwconfig"],
                        universal_newlines=True,
                        stderr=subprocess.DEVNULL
                    )
                    wifi_info['raw'] = output
                    # Parse basic info
                    if "ESSID:" in output:
                        essid = output.split('ESSID:"')[1].split('"')[0]
                        wifi_info['SSID'] = essid
                    if "Bit Rate=" in output:
                        rate = output.split('Bit Rate=')[1].split(' ')[0]
                        wifi_info['Bit Rate'] = rate
                except:
                    pass
                    
            elif platform.system() == "Darwin":  # macOS
                # macOS WiFi info using airport
                try:
                    output = subprocess.check_output(
                        ["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-I"],
                        universal_newlines=True
                    )
                    for line in output.split('\n'):
                        if ': ' in line:
                            key, value = line.split(': ', 1)
                            key = key.strip()
                            value = value.strip()
                            wifi_info[key] = value
                except:
                    pass
                    
        except Exception as e:
            wifi_info['error'] = str(e)
            
        return wifi_info

    def update_interface_info(self):
        """Update network interface information"""
        interfaces = psutil.net_if_addrs()
        stats = psutil.net_if_stats()
        
        # Prepare table data
        table_data = []
        for interface_name, addrs in interfaces.items():
            interface_info = {
                'name': interface_name,
                'ip': '',
                'netmask': '',
                'mac': '',
                'status': 'Down'
            }
            
            # Get interface status
            if interface_name in stats:
                interface_info['status'] = 'Up' if stats[interface_name].isup else 'Down'
            
            # Get addresses
            for addr in addrs:
                if addr.family == socket.AF_INET:  # IPv4
                    interface_info['ip'] = addr.address
                    interface_info['netmask'] = addr.netmask
                elif addr.family == psutil.AF_LINK:  # MAC address
                    interface_info['mac'] = addr.address
                    
            table_data.append(interface_info)
        
        # Update interface table
        self.interface_table.setRowCount(len(table_data))
        for row, info in enumerate(table_data):
            self.interface_table.setItem(row, 0, QTableWidgetItem(info['name']))
            self.interface_table.setItem(row, 1, QTableWidgetItem(info['ip']))
            self.interface_table.setItem(row, 2, QTableWidgetItem(info['netmask']))
            self.interface_table.setItem(row, 3, QTableWidgetItem(info['mac']))
            
            status_item = QTableWidgetItem(info['status'])
            if info['status'] == 'Up':
                status_item.setForeground(Qt.GlobalColor.green)
            else:
                status_item.setForeground(Qt.GlobalColor.red)
            self.interface_table.setItem(row, 4, status_item)
        
        self.interface_table.resizeColumnsToContents()
        
        # Update WiFi details if available
        wifi_info = self.get_wifi_info()
        if wifi_info:
            wifi_text = "<b>WiFi Details:</b><br>"
            
            if platform.system() == "Windows":
                relevant_keys = [
                    'Name', 'State', 'SSID', 'Signal',
                    'Channel', 'Authentication', 'Radio type'
                ]
            elif platform.system() == "Linux":
                if 'SSID' in wifi_info:
                    wifi_text += f"SSID: {wifi_info['SSID']}<br>"
                if 'Bit Rate' in wifi_info:
                    wifi_text += f"Bit Rate: {wifi_info['Bit Rate']}<br>"
            elif platform.system() == "Darwin":
                relevant_keys = [
                    'SSID', 'channel', 'agrCtlRSSI',
                    'agrCtlNoise', 'lastTxRate', 'maxRate'
                ]
            
            if platform.system() in ["Windows", "Darwin"]:
                for key in relevant_keys:
                    if key in wifi_info:
                        wifi_text += f"{key}: {wifi_info[key]}<br>"
                        
            self.wifi_details.setText(wifi_text)
        else:
            self.wifi_details.setText("No WiFi information available")

    def update_info(self):
        """Update all network information"""
        # Get network info
        network_info = self.network_monitor.get_all_info()
        io_info = network_info['io']
        
        # Calculate speeds
        bytes_sent_speed = self.calculate_speed(
            io_info['bytes_sent'], self.prev_bytes_sent)
        bytes_recv_speed = self.calculate_speed(
            io_info['bytes_recv'], self.prev_bytes_recv)
        
        # Update speed labels
        self.upload_speed_label.setText(self.format_speed(bytes_sent_speed))
        self.download_speed_label.setText(self.format_speed(bytes_recv_speed))
        
        # Update traffic statistics
        traffic_stats = (
            f"<b>Total Sent:</b> {self.format_bytes(io_info['bytes_sent'])}<br>"
            f"<b>Total Received:</b> {self.format_bytes(io_info['bytes_recv'])}<br>"
            f"<b>Packets Sent:</b> {io_info['packets_sent']}<br>"
            f"<b>Packets Received:</b> {io_info['packets_recv']}"
        )
        self.traffic_stats_label.setText(traffic_stats)
        
        # Update connections table
        connections = network_info['connections']
        self.connections_table.setRowCount(len(connections))


        # Update interface information first
        self.update_interface_info()
        
        for row, conn in enumerate(connections):
            # Format local address
            local_addr = f"{conn['local_addr'][0]}:{conn['local_addr'][1]}" if conn['local_addr'] else "N/A"
            self.connections_table.setItem(row, 0, QTableWidgetItem(local_addr))
            
            # Format remote address
            remote_addr = f"{conn['remote_addr'][0]}:{conn['remote_addr'][1]}" if conn['remote_addr'] else "N/A"
            self.connections_table.setItem(row, 1, QTableWidgetItem(remote_addr))
            
            # Add status
            self.connections_table.setItem(row, 2, QTableWidgetItem(conn['status']))
            
            # Add connection type (can be determined from port numbers)
            conn_type = "TCP" if conn['local_addr'] and conn['local_addr'][1] < 1024 else "Application"
            self.connections_table.setItem(row, 3, QTableWidgetItem(conn_type))
        
        # Auto-adjust column widths
        self.connections_table.resizeColumnsToContents()
        
        # Update performance metrics
        performance_text = (
            f"<b>Active Connections:</b> {len(connections)}<br>"
            f"<b>Upload Status:</b> "
            f"{'High' if bytes_sent_speed > 1000000 else 'Normal'}<br>"
            f"<b>Download Status:</b> "
            f"{'High' if bytes_recv_speed > 1000000 else 'Normal'}<br>"
            f"<b>Network Activity:</b> "
            f"{'Active' if bytes_sent_speed + bytes_recv_speed > 0 else 'Idle'}"
        )
        self.performance_label.setText(performance_text)
        
        # Store current values for next update
        self.prev_bytes_sent = io_info['bytes_sent']
        self.prev_bytes_recv = io_info['bytes_recv']