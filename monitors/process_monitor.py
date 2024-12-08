import psutil
import time
from datetime import datetime
from collections import defaultdict, deque
import os

class ProcessMonitor:
    """
    A simple class to monitor process statistics
    """
    def __init__(self):
        pass
    
    def get_process_list(self):
        """Get list of running processes"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'cpu_percent': proc.info['cpu_percent'],
                    'memory_percent': proc.info['memory_percent']
                })
            except Exception:
                continue
        return processes
    
    def get_process_count(self):
        """Get total number of processes"""
        return len(psutil.pids())
    
    def get_all_info(self):
        """Get all process information"""
        return {
            'processes': self.get_process_list(),
            'total_count': self.get_process_count()
        }