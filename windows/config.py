# Genel stil tanımlamaları
STYLES = {
    'main_window': """
        QMainWindow {
            background-color: #f0f0f0;
        }
    """,
    
    'label': """
        QLabel {
            color: #333333;
            font-size: 14px;
            font-weight: bold;
        }
    """,
    
    'line_edit': """
        QLineEdit {
            padding: 8px;
            border: 2px solid #cccccc;
            border-radius: 5px;
            background-color: white;
            font-size: 14px;
        }
        QLineEdit:focus {
            border: 2px solid #4CAF50;
        }
    """,
    
    'button': """
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 5px;
            font-size: 14px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        QPushButton:pressed {
            background-color: #3d8b40;
        }
    """,
    
    'title': """
        QLabel {
            font-size: 24px;
            color: #333333;
            font-weight: bold;
            margin-bottom: 20px;
        }
    """
}

APP_STYLE = """
    QMainWindow { background-color: #F7F9FA; }
    QLabel { color: #1F3A93; font-size: 16px; font-weight: bold; }
    QLineEdit, QComboBox { background-color: #FFFFFF; border: 2px solid #D5D8DC; border-radius: 8px; padding: 8px; font-size: 15px; color: #2F4F4F; }
    QPushButton { background-color: #1F3A93; border: none; border-radius: 8px; padding: 12px 0; font-size: 15px; font-weight: bold; color: #FFFFFF; min-width: 120px; }
    QPushButton:hover { background-color: #2C3E99; }
    QPushButton:pressed { background-color: #0D2B7E; }
    QTableWidget { background-color: #FFFFFF; border: 1px solid #D5D8DC; alternate-background-color: #F8F9FA; gridline-color: #E6E6E6; border-radius: 8px; }
    QHeaderView::section { background-color: #1F3A93; color: #FFFFFF; font-weight: bold; font-size: 15px; padding: 8px; border: none; }
    QCheckBox { font-size: 14px; }
    QCalendarWidget { background: #FFFFFF; border-radius: 8px; }
"""