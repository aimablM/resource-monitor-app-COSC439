import platform
import psutil
from .cpu_monitor import CPUMonitor
from .memory_monitor import MemoryMonitor
from .storage_monitor import StorageMonitor
from .network_monitor import NetworkMonitor
from .process_monitor import ProcessMonitor

class SystemMonitor:
    """
    A simple class to monitor system-wide statistics
    """
    def __init__(self):
        pass
    
    def get_boot_time(self):
        """Get system boot time"""
        return psutil.boot_time()
    
    def get_users(self):
        """Get logged in users"""
        users = []
        for user in psutil.users():
            users.append({
                'name': user.name,
                'terminal': user.terminal,
                'host': user.host,
                'started': user.started
            })
        return users
    
    def get_os_info(self):
        """Get operating system information"""
        
        return {
            'system': platform.system(),
            'release': platform.release(),
            'version': platform.version(),
            'machine': platform.machine()
        }
    
    def get_all_info(self):
        """Get all system information"""
        return {
            'boot_time': self.get_boot_time(),
            'users': self.get_users(),
            'os_info': self.get_os_info()
        }

# Example usage:
if __name__ == "__main__":
    # Create instances of monitors
    cpu_monitor = CPUMonitor()
    memory_monitor = MemoryMonitor()
    storage_monitor = StorageMonitor()
    network_monitor = NetworkMonitor()
    process_monitor = ProcessMonitor()
    system_monitor = SystemMonitor()
    
    # Get information from each monitor
    print("CPU Info:", cpu_monitor.get_all_info())
    print("\nMemory Info:", memory_monitor.get_all_info())
    print("\nStorage Info:", storage_monitor.get_all_info())
    print("\nNetwork Info:", network_monitor.get_all_info())
    print("\nProcess Info:", process_monitor.get_all_info())
    print("\nSystem Info:", system_monitor.get_all_info())