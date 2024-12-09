from PyQt6.QtGui import QIcon, QFont, QPainter, QPixmap
from PyQt6.QtCore import Qt

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