import psutil
import time
class MemoryMonitor:
    """
    A simple class to monitor memory statistics
    """
    def __init__(self):
        pass
    
    def get_memory_info(self):
        """Get basic memory information"""
        mem = psutil.virtual_memory()
        return {
            'total': mem.total,
            'available': mem.available,
            'used': mem.used,
            'free': mem.free,
            'percent': mem.percent
        }
    
    def get_swap_info(self):
        """Get swap memory information"""
        swap = psutil.swap_memory()
        return {
            'total': swap.total,
            'used': swap.used,
            'free': swap.free,
            'percent': swap.percent
        }
    
    def get_all_info(self):
        """Get all memory information"""
        return {
            'ram': self.get_memory_info(),
            'swap': self.get_swap_info()
        }