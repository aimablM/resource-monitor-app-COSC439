import psutil
import time
from datetime import datetime

class CPUMonitor:
    """
    A simple class to monitor CPU statistics
    """
    def __init__(self):
        # Initialize any required variables
        self.prev_cpu_times = psutil.cpu_times()
    
    def get_cpu_percent(self):
        """Get CPU usage percentage"""
        return {
            'total': psutil.cpu_percent(interval=1),
            'per_cpu': psutil.cpu_percent(interval=1, percpu=True)
        }
    
    def get_cpu_freq(self):
        """Get CPU frequency information"""
        freq = psutil.cpu_freq()
        if freq:
            return {
                'current': freq.current,
                'min': freq.min,
                'max': freq.max
            }
        return None
    
    def get_cpu_count(self):
        """Get CPU core count"""
        return {
            'physical': psutil.cpu_count(logical=False),
            'logical': psutil.cpu_count(logical=True)
        }
    
    def get_all_info(self):
        """Get all CPU information"""
        return {
            'usage': self.get_cpu_percent(),
            'frequency': self.get_cpu_freq(),
            'cores': self.get_cpu_count()
        }
