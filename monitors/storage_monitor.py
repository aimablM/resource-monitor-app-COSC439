import psutil
import time
from datetime import datetime
import os

class StorageMonitor:
    """
    A simple class to monitor storage statistics
    """
    def __init__(self):
        pass
    
    def get_partitions(self):
        """Get information about disk partitions"""
        partitions = []
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                partitions.append({
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'fstype': partition.fstype,
                    'total': usage.total,
                    'used': usage.used,
                    'free': usage.free,
                    'percent': usage.percent
                })
            except Exception:
                continue
        return partitions
    
    def get_disk_io(self):
        """Get disk I/O statistics"""
        io = psutil.disk_io_counters()
        return {
            'read_bytes': io.read_bytes,
            'write_bytes': io.write_bytes,
            'read_count': io.read_count,
            'write_count': io.write_count
        }
    
    def get_all_info(self):
        """Get all storage information"""
        return {
            'partitions': self.get_partitions(),
            'io': self.get_disk_io()
        }