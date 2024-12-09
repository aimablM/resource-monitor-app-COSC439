from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QLabel, QProgressBar, QGroupBox, QScrollArea, QApplication)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon, QFont, QPainter, QPixmap
import psutil
import platform

def create_emoji_icon(emoji, size=32):
    """Create a QIcon from an emoji character"""
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    
    painter = QPainter(pixmap)
    font = QFont()
    font.setPointSize(size - 8)
    painter.setFont(font)
    
    painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, emoji)
    painter.end()
    
    return QIcon(pixmap)

class CPUMonitorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CPU Monitor")
        self.setMinimumSize(600, 800)
        self.setWindowIcon(create_emoji_icon('⚡'))
        
        # Create scroll area for content
        scroll = QScrollArea()
        self.setCentralWidget(scroll)
        
        # Create main widget and layout
        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Add welcome header
        self.create_welcome_header(layout)
        
        # Create info sections
        self.create_total_usage_section(layout)
        self.create_cores_section(layout)
        self.create_cpu_info_section(layout)
        self.create_frequency_section(layout)
        
        # Add credits footer
        self.create_credits_footer(layout)
        
        # Make the scroll area display our widget
        scroll.setWidget(main_widget)
        scroll.setWidgetResizable(True)
        
        # Set up timer for updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(1000)  # Update every second
        
        # Initial update
        self.update_stats()

    def create_welcome_header(self, layout):
        """Create welcome header"""
        header = QLabel("CPU Monitor - Real-time Processing Power Stats")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)

    def create_total_usage_section(self, layout):
        """Create total CPU usage section"""
        group = QGroupBox("Total CPU Usage")
        group_layout = QVBoxLayout()
        
        # Create total usage progress bar
        self.total_usage_bar = QProgressBar()
        self.total_usage_bar.setMinimum(0)
        self.total_usage_bar.setMaximum(100)
        
        # Create label for percentage
        self.total_usage_label = QLabel()
        self.total_usage_label.setTextFormat(Qt.TextFormat.RichText)
        
        group_layout.addWidget(self.total_usage_bar)
        group_layout.addWidget(self.total_usage_label)
        group.setLayout(group_layout)
        layout.addWidget(group)

    def create_cores_section(self, layout):
        """Create CPU cores section"""
        group = QGroupBox("CPU Cores Usage")
        group_layout = QVBoxLayout()
        
        # Create widgets for each CPU core
        self.core_bars = []
        self.core_labels = []
        
        for i in range(psutil.cpu_count()):
            core_layout = QHBoxLayout()
            
            # Create label for core number
            label = QLabel(f"Core {i + 1}:")
            label.setMinimumWidth(70)
            core_layout.addWidget(label)
            
            # Create progress bar for core usage
            bar = QProgressBar()
            bar.setMinimum(0)
            bar.setMaximum(100)
            core_layout.addWidget(bar)
            
            # Create label for percentage
            percent_label = QLabel()
            percent_label.setMinimumWidth(50)
            core_layout.addWidget(percent_label)
            
            group_layout.addLayout(core_layout)
            self.core_bars.append(bar)
            self.core_labels.append(percent_label)
        
        group.setLayout(group_layout)
        layout.addWidget(group)

    def create_cpu_info_section(self, layout):
        """Create CPU information section"""
        group = QGroupBox("CPU Information")
        group_layout = QVBoxLayout()
        
        self.cpu_info_label = QLabel()
        self.cpu_info_label.setTextFormat(Qt.TextFormat.RichText)
        group_layout.addWidget(self.cpu_info_label)
        
        group.setLayout(group_layout)
        layout.addWidget(group)

    def create_frequency_section(self, layout):
        """Create CPU frequency section"""
        group = QGroupBox("CPU Frequency")
        group_layout = QVBoxLayout()
        
        self.freq_label = QLabel()
        self.freq_label.setTextFormat(Qt.TextFormat.RichText)
        group_layout.addWidget(self.freq_label)
        
        group.setLayout(group_layout)
        layout.addWidget(group)

    def create_credits_footer(self, layout):
        """Create credits footer"""
        footer = QLabel("Designed and built by Aimable M and Jash M")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(footer)

    def update_stats(self):
        """Update all CPU statistics"""
        # Update total CPU usage
        total_cpu = psutil.cpu_percent()
        self.total_usage_bar.setValue(int(total_cpu))
        self.total_usage_label.setText(f"<b>Total CPU Usage: {total_cpu}%</b>")
        
        # Update individual core usage
        per_cpu = psutil.cpu_percent(percpu=True)
        for i, (bar, label, usage) in enumerate(zip(self.core_bars, self.core_labels, per_cpu)):
            bar.setValue(int(usage))
            label.setText(f"{usage:.1f}%")
        
        # Update CPU information
        cpu_info = (
            f"<b>Processor:</b> {platform.processor()}<br>"
            f"<b>Physical cores:</b> {psutil.cpu_count(logical=False)}<br>"
            f"<b>Total cores:</b> {psutil.cpu_count()}<br>"
            f"<b>Max threads per core:</b> {psutil.cpu_count() // psutil.cpu_count(logical=False)}<br>"
            f"<b>Architecture:</b> {platform.machine()}"
        )
        self.cpu_info_label.setText(cpu_info)
        
        # Update frequency information
        try:
            freq = psutil.cpu_freq()
            if freq:
                freq_info = (
                    f"<b>Current Frequency:</b> {freq.current:.1f} MHz<br>"
                    f"<b>Minimum Frequency:</b> {freq.min:.1f} MHz<br>"
                    f"<b>Maximum Frequency:</b> {freq.max:.1f} MHz"
                )
            else:
                freq_info = "CPU frequency information not available"
        except Exception:
            freq_info = "CPU frequency information not available"
            
        self.freq_label.setText(freq_info)

def main():
    app = QApplication([])
    window = CPUMonitorWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()