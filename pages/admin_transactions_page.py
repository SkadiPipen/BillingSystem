import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt5 import QtCore, QtGui, QtWidgets

class AdminTransactionsPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header with title and search
        header_layout = QtWidgets.QHBoxLayout()
        title = QtWidgets.QLabel("TRANSACTIONS LIST")
        title.setStyleSheet("""
            font-family: 'Montserrat', sans-serif;
            font-size: 24px;
            font-weight: bold;
        """)
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        # Search bar
        search_input = QtWidgets.QLineEdit()
        search_input.setPlaceholderText("Search transactions by Id...")
        search_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-family: 'Roboto', sans-serif;
                min-width: 250px;
            }
        """)
        header_layout.addWidget(search_input)
        layout.addLayout(header_layout)

        # Table setup
        self.transactions_table = QtWidgets.QTableWidget()
        self.transactions_table.verticalHeader().setVisible(False)
        self.transactions_table.setStyleSheet("""
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
        
        # Set up columns
        self.transactions_table.setColumnCount(7)
        self.transactions_table.setHorizontalHeaderLabels([
            "TRANSACTION ID", "CUSTOMER NAME", "AMOUNT", "COLLECTOR", "DATE", "STATUS", "ACTIONS"
        ])
        
        # Sample data
        sample_data = [
            ("TR001", "Alice Brown", "₱50", "John Doe", "2023-10-15", "COMPLETED"),
            ("TR002", "Charlie Davis", "₱50", "John Doe", "2023-10-15", "PENDING"),
            ("TR003", "Eve Franklin", "₱50", "John Doe", "2023-10-15", "FAILED"),
        ]
        
        self.populate_table(sample_data)
        
        # Adjust table properties
        self.transactions_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.transactions_table.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self.transactions_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        
        layout.addWidget(self.transactions_table)

    def populate_table(self, data):
        self.transactions_table.setRowCount(len(data))
        for row, (TRANS_ID, CUST_NAME, TRANS_AMOUNT, COLLECTOR, TRANS_DATE, TRANS_STATUS) in enumerate(data):
            self.transactions_table.setItem(row, 0, QtWidgets.QTableWidgetItem(TRANS_ID))
            self.transactions_table.setItem(row, 1, QtWidgets.QTableWidgetItem(CUST_NAME))
            self.transactions_table.setItem(row, 2, QtWidgets.QTableWidgetItem(TRANS_AMOUNT))
            self.transactions_table.setItem(row, 3, QtWidgets.QTableWidgetItem(COLLECTOR))
            self.transactions_table.setItem(row, 4, QtWidgets.QTableWidgetItem(TRANS_DATE))
            
            # Status with color
            status_item = QtWidgets.QTableWidgetItem(TRANS_STATUS)
            if TRANS_STATUS == "COMPLETED":
                status_item.setForeground(QtGui.QColor('green'))
            elif TRANS_STATUS == "PENDING":
                status_item.setForeground(QtGui.QColor('orange'))
            else:
                status_item.setForeground(QtGui.QColor('red'))
            self.transactions_table.setItem(row, 5, status_item)
            
            # Action buttons
            actions_widget = QtWidgets.QWidget()
            actions_layout = QtWidgets.QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(4, 4, 4, 4)
            
            view_btn = QtWidgets.QPushButton(icon=QtGui.QIcon("../images/view.png"))
            delete_btn = QtWidgets.QPushButton(icon=QtGui.QIcon("../images/delete.png"))
            
            view_btn.setIconSize(QtCore.QSize(24, 24))
            delete_btn.setIconSize(QtCore.QSize(24, 24))
            
            for btn in [view_btn, delete_btn]:
                btn.setStyleSheet("""
                    QPushButton {
                        padding: 5px 10px;
                        border: none;
                        border-radius: 4px;
                    }
                    QPushButton:hover {
                        background-color: #f0f0f0;
                    }
                """)
                actions_layout.addWidget(btn)
            
            self.transactions_table.setCellWidget(row, 6, actions_widget)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = AdminTransactionsPage()
    window.show()
    sys.exit(app.exec_())                