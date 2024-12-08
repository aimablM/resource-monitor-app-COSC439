import psutil
import time
from datetime import datetime
from collections import defaultdict
import subprocess
import socket

class NetworkMonitor:
    """
    A simple class to monitor network statistics
    """
    def __init__(self):
        self.prev_net_io = psutil.net_io_counters()
        self.prev_time = time.time()
    
    def get_network_io(self):
        """Get network I/O statistics"""
        net_io = psutil.net_io_counters()
        return {
            'bytes_sent': net_io.bytes_sent,
            'bytes_recv': net_io.bytes_recv,
            'packets_sent': net_io.packets_sent,
            'packets_recv': net_io.packets_recv
        }
    
    def get_connections(self):
        """Get current network connections"""
        connections = []
        for conn in psutil.net_connections():
            try:
                connections.append({
                    'local_addr': conn.laddr,
                    'remote_addr': conn.raddr,
                    'status': conn.status
                })
            except Exception:
                continue
        return connections
    
    def get_all_info(self):
        """Get all network information"""
        return {
            'io': self.get_network_io(),
            'connections': self.get_connections()
        }
