from PyQt5 import QtCore, QtGui, QtWidgets
import sys, os, warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.adminBack import adminPageBack

class LogsAndHistoryPage(QtWidgets.QWidget):
    def __init__(self, username, parent=None):
        super().__init__(parent)
        self.username = username
        self.backend = adminPageBack(self.username)
        self.setup_ui()

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header
        header_layout = QtWidgets.QHBoxLayout()
        title = QtWidgets.QLabel("System Logs")
        title.setStyleSheet("""
            font-family: 'Montserrat', sans-serif;
            font-size: 24px;
            font-weight: bold;
        """)
        header_layout.addWidget(title)
        header_layout.addStretch()

        # Refresh Button
        refresh_btn = QtWidgets.QPushButton("🔄 Refresh")
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #81C784;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                font-family: 'Roboto', sans-serif;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #66BB6A;
            }
        """)
        refresh_btn.clicked.connect(self.refresh_logs)
        header_layout.addWidget(refresh_btn)

        layout.addLayout(header_layout)

        # Table
        self.system_logs_table = self.create_system_logs_table()
        layout.addWidget(self.system_logs_table)

    def create_system_logs_table(self):
        table = QtWidgets.QTableWidget()
        table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: #C9EBCB;
            }
            QHeaderView::section {
                background-color: #B2C8B2;
                padding: 8px;
                border: none;
                font-family: 'Roboto', sans-serif;
                font-weight: bold;
            }
        """)
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels([
            "Log ID", "Log Message", "Timestamp", "User"
        ])
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        table.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        table.verticalHeader().setVisible(False)

        logs_data = self.backend.fetch_system_logs()
        self.populate_table(table, logs_data)
        return table

    def populate_table(self, table, data):
        table.setRowCount(len(data))
        for row, data_row in enumerate(data):
            for col, value in enumerate(data_row):
                table.setItem(row, col, QtWidgets.QTableWidgetItem(str(value)))

    def refresh_logs(self):
        """Fetch new logs and repopulate the table."""
        logs_data = self.backend.fetch_system_logs()
        self.populate_table(self.system_logs_table, logs_data)
        QtWidgets.QMessageBox.information(self, "Refreshed", "System logs have been refreshed.")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LogsAndHistoryPage()
    window.showMaximized()
    sys.exit(app.exec_())