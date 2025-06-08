import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
import sys
import os
import math

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt5 import QtCore, QtGui, QtWidgets
from backend.adminBack import adminPageBack
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QDialog
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


class MetersPage(QtWidgets.QWidget):
    def __init__(self, user_name, parent=None):
        super().__init__(parent)
        self.user_name = user_name
        self.all_meters_data = []  # Store all meter data
        self.current_page = 1
        self.records_per_page = 10  # Number of records per page
        self.total_pages = 1
        self.IadminPageBack = adminPageBack(self.user_name)
        self.setup_ui()
        self.showMaximized()

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header Panel
        header_panel = QtWidgets.QWidget()
        header_panel.setStyleSheet("background-color: #f5f5f5; border-bottom: 1px solid #ddd;")
        header_layout = QtWidgets.QVBoxLayout(header_panel)
        header_layout.setContentsMargins(20, 15, 20, 15)

        # Header with title, search bar, and dropdown
        controls_layout = QtWidgets.QHBoxLayout()

        # Title
        title = QtWidgets.QLabel("METERS LIST")
        title.setStyleSheet("""
            font-family: 'Montserrat', sans-serif;
            font-size: 24px;
            font-weight: bold;
        """)
        controls_layout.addWidget(title)
        controls_layout.addStretch()  # Pushes everything after title to the right

        # Filter Combo Box
        self.filter_combo = QtWidgets.QComboBox()
        self.filter_combo.addItems(["Meter Code", "Client Name", "Serial Number", "Last Read"])
        self.filter_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-family: 'Roboto', sans-serif;
                min-width: 150px;
                background-color: white;
            }
        """)
        controls_layout.addWidget(self.filter_combo)

        # Search Input Field
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("Search meters...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-family: 'Roboto', sans-serif;
                min-width: 250px;
                background-color: white;
            }
        """)
        self.search_input.textChanged.connect(self.filter_table)
        controls_layout.addWidget(self.search_input)

        # Add the horizontal layout to the header
        header_layout.addLayout(controls_layout)
        layout.addWidget(header_panel)

        # Table Widget (unchanged)
        self.meter_table = QtWidgets.QTableWidget()
        self.meter_table.setAlternatingRowColors(True)
        self.meter_table.setStyleSheet("""
            QTableWidget {
                border: none;
                background-color: #E8F5E9;
                alternate-background-color: #FFFFFF;
            }
            QHeaderView::section {
                background-color: #B2C8B2;
                padding: 8px;
                border: none;
                font-family: 'Roboto', sans-serif;
                font-weight: bold;
                font-size: 15px;
            }
            QTableWidget::item:selected {
                background-color: transparent;
                color: black;
            }
            QTableWidget::item:hover {
                background-color: transparent;
            }
        """)
        self.meter_table.setColumnCount(5)
        self.meter_table.setHorizontalHeaderLabels([
            "METER CODE", "CLIENT NAME", "SERIAL NUMBER", "LAST READ", "ACTION"
        ])

        self.meter_table.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.meter_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.meter_table.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self.meter_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.meter_table.verticalHeader().setVisible(False)

        layout.addWidget(self.meter_table)

        # Fetch all meters data
        self.all_meters_data = self.IadminPageBack.fetch_meters()
        self.populate_table(self.all_meters_data)

        # Pagination Controls
        pagination_layout = QtWidgets.QHBoxLayout()
        pagination_layout.setAlignment(QtCore.Qt.AlignCenter)

        self.first_page_btn = QtWidgets.QPushButton("⏮ First")
        self.prev_page_btn = QtWidgets.QPushButton("◀ Previous")
        self.page_indicator = QtWidgets.QLabel("Page 1 of 1")
        self.next_page_btn = QtWidgets.QPushButton("Next ▶")
        self.last_page_btn = QtWidgets.QPushButton("Last ⏭")

        self.first_page_btn.clicked.connect(self.go_to_first_page)
        self.prev_page_btn.clicked.connect(self.go_to_prev_page)
        self.next_page_btn.clicked.connect(self.go_to_next_page)
        self.last_page_btn.clicked.connect(self.go_to_last_page)

        btn_style = """
            QPushButton {
                background-color: #81C784;
                color: white;
                padding: 5px 10px;
                border-radius: 4px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #66BB6A;
            }
            QPushButton:disabled {
                background-color: #E0E0E0;
                color: #9E9E9E;
            }
        """
        self.first_page_btn.setStyleSheet(btn_style)
        self.prev_page_btn.setStyleSheet(btn_style)
        self.next_page_btn.setStyleSheet(btn_style)
        self.last_page_btn.setStyleSheet(btn_style)
        self.page_indicator.setStyleSheet("font-weight: bold; min-width: 150px;")

        pagination_layout.addWidget(self.first_page_btn)
        pagination_layout.addWidget(self.prev_page_btn)
        pagination_layout.addWidget(self.page_indicator)
        pagination_layout.addWidget(self.next_page_btn)
        pagination_layout.addWidget(self.last_page_btn)

        # Records per page selector
        self.page_size_label = QtWidgets.QLabel("Records per page:")
        self.page_size_combo = QtWidgets.QComboBox()
        self.page_size_combo.addItems(["5", "10", "20", "50", "100"])
        self.page_size_combo.setCurrentText(str(self.records_per_page))
        self.page_size_combo.currentTextChanged.connect(self.change_page_size)
        pagination_layout.addWidget(self.page_size_label)
        pagination_layout.addWidget(self.page_size_combo)

        layout.addLayout(pagination_layout)

        self.update_pagination()

    def update_pagination(self):
        visible_rows = 0
        for row in range(len(self.all_meters_data)):
            if not self.is_row_filtered(row):
                visible_rows += 1
        self.total_pages = max(1, math.ceil(visible_rows / self.records_per_page))
        if self.current_page > self.total_pages:
            self.current_page = self.total_pages
        self.page_indicator.setText(f"Page {self.current_page} of {self.total_pages}")
        self.first_page_btn.setEnabled(self.current_page > 1)
        self.prev_page_btn.setEnabled(self.current_page > 1)
        self.next_page_btn.setEnabled(self.current_page < self.total_pages)
        self.last_page_btn.setEnabled(self.current_page < self.total_pages)
        self.populate_table(self.all_meters_data)

    def is_row_filtered(self, row_index):
        if not hasattr(self, 'search_input') or self.search_input is None:
            return False  # No search input, show all rows

        if row_index >= len(self.all_meters_data):
            return True  # Invalid row index

        meter = self.all_meters_data[row_index]
        search_text = self.search_input.text().strip().lower()

        if not search_text:
            return False  # No search text, show all rows

        # Map combo box selection to correct column index
        field_mapping = {
            "Meter Code": 0,
            "Client Name": 1,  # now contains full name
            "Serial Number": 2,
            "Last Read": 3
        }

        filter_by = self.filter_combo.currentText()
        field_index = field_mapping.get(filter_by, -1)

        if field_index == -1:
            return True  # Invalid field selected

        try:
            field_value = str(meter[field_index]).lower()
        except IndexError:
            print("Invalid meter data structure:", meter)
            return True  # Skip invalid rows

        return search_text not in field_value

    def go_to_first_page(self):
        if self.current_page != 1:
            self.current_page = 1
            self.update_pagination()

    def go_to_prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.update_pagination()

    def go_to_next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.update_pagination()

    def go_to_last_page(self):
        if self.current_page != self.total_pages:
            self.current_page = self.total_pages
            self.update_pagination()

    def change_page_size(self, size):
        self.records_per_page = int(size)
        self.current_page = 1
        self.update_pagination()

    def populate_table(self, data):
        self.meter_table.setRowCount(0)
        start_index = (self.current_page - 1) * self.records_per_page
        end_index = start_index + self.records_per_page

        # Filter rows based on search input
        filtered_data = [meter for i, meter in enumerate(data) if not self.is_row_filtered(i)]

        # Paginate filtered data
        paginated_data = filtered_data[start_index:end_index]

        for table_row, meter in enumerate(paginated_data):
            try:
                meter_code, full_name, serial_number, last_read, meter_id = meter
            except ValueError as e:
                print("Error unpacking meter data:", meter, e)
                continue

            self.meter_table.insertRow(table_row)

            self.meter_table.setItem(table_row, 0, QtWidgets.QTableWidgetItem(str(meter_code)))
            self.meter_table.setItem(table_row, 1, QtWidgets.QTableWidgetItem(full_name))
            self.meter_table.setItem(table_row, 2, QtWidgets.QTableWidgetItem(str(serial_number)))
            self.meter_table.setItem(table_row, 3, QtWidgets.QTableWidgetItem(str(last_read)))

            view_btn = QPushButton()
            view_btn.setIcon(QtGui.QIcon("../images/view.png"))
            view_btn.setToolTip("View Meter")
            view_btn.clicked.connect(lambda _, mid=meter_id: self.view_meter_details(mid))
            view_btn.setStyleSheet("background-color: transparent; padding: 5px;")

            replace_btn = QPushButton()
            replace_btn.setIcon(QtGui.QIcon("../images/replace.png"))
            replace_btn.setToolTip("Replace Meter")
            replace_btn.clicked.connect(lambda _, mid=meter_id: self.replace_meter_dialog(mid))
            replace_btn.setStyleSheet("background-color: transparent; padding: 5px;")

            btn_layout = QHBoxLayout()
            btn_widget = QWidget()
            btn_layout.setContentsMargins(0, 0, 0, 0)
            btn_layout.addWidget(view_btn)
            btn_layout.addWidget(replace_btn)
            btn_widget.setLayout(btn_layout)
            self.meter_table.setCellWidget(table_row, 4, btn_widget)

    def filter_table(self):
        self.current_page = 1
        self.update_pagination()

    def view_meter_details(self, meter_id):
        # Fetch detailed meter information
        meter_data = next((m for m in self.all_meters_data if m[4] == meter_id), None)

        if not meter_data:
            QtWidgets.QMessageBox.warning(self, "Error", "Meter data not found.")
            return

        # Extract Meter Code from meter_data (index 0 is meter_code in formatted_meters)
        meter_code = meter_data[0]  # ← Get Meter Code instead of Meter ID

        # Get readings for this meter only
        readings = self.IadminPageBack.fetch_readings_by_meter_id(meter_id)

        # Create dialog window
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Meter Readings - {meter_code}")
        dialog.resize(900, 600)  # Set initial dialog size

        layout = QVBoxLayout(dialog)

        # Info Label - Display Meter Code instead of Meter ID
        info_label = QLabel(f"<b>Meter Code:</b> {meter_code}")
        info_label.setStyleSheet("font-size: 16px; padding-bottom: 10px;")
        layout.addWidget(info_label)

        if not readings:
            # Show message if no readings
            no_data_label = QLabel("No reading history found for this meter.")
            no_data_label.setStyleSheet("font-size: 14px; color: #555;")
            no_data_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(no_data_label)
        else:
            # Table setup without Reading ID or Meter ID
            table = QTableWidget()
            table.setColumnCount(3)  # Date, Previous Reading, Current Reading
            table.setHorizontalHeaderLabels(["Date", "Previous Reading", "Current Reading"])
            table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
            table.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
            table.verticalHeader().setVisible(False)

            # Populate table
            table.setRowCount(len(readings))
            for row, reading in enumerate(readings):
                try:
                    reading_id, reading_date, prev_reading, current_reading, _ = reading
                    table.setItem(row, 0, QTableWidgetItem(str(reading_date)))
                    table.setItem(row, 1, QTableWidgetItem(str(prev_reading)))
                    table.setItem(row, 2, QTableWidgetItem(str(current_reading)))
                except Exception as e:
                    print("Error unpacking reading:", reading, e)
                    continue

            layout.addWidget(table)

        # Close button
        close_btn = QPushButton("Close")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #81C784;
                color: white;
                padding: 8px;
                border-radius: 4px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #66BB6A;
            }
        """)
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn, alignment=Qt.AlignRight)

        # Show dialog
        dialog.exec_()

    def replace_meter_dialog(self, old_meter_id):
        dialog = QDialog(self)
        dialog.setWindowTitle("Replace Meter")
        layout = QVBoxLayout(dialog)

        serial_input = QLineEdit()
        serial_input.setPlaceholderText("Enter new serial number")

        reading_input = QLineEdit()
        reading_input.setPlaceholderText("Enter initial reading (e.g., 12345)")

        submit_btn = QPushButton("Confirm Replacement")
        submit_btn.clicked.connect(lambda: self.confirm_meter_replacement(
            old_meter_id,
            serial_input.text(),
            reading_input.text(),
            dialog
        ))

        layout.addWidget(QLabel("New Serial Number:"))
        layout.addWidget(serial_input)
        layout.addWidget(QLabel("Initial Reading:"))
        layout.addWidget(reading_input)
        layout.addWidget(submit_btn)

        dialog.exec_()

    def confirm_meter_replacement(self, old_meter_id, new_serial, initial_reading, dialog):
        if not new_serial:
            QtWidgets.QMessageBox.warning(self, "Error", "Serial number is required.")
            return

        if not initial_reading.isdigit():
            QtWidgets.QMessageBox.warning(self, "Error", "Initial reading must be a valid number.")
            return

        # Check if serial already exists
        existing_meters = self.IadminPageBack.fetch_meters()
        for meter in existing_meters:
            existing_serial = meter[2]  # Adjust index if needed
            if existing_serial == new_serial:
                QtWidgets.QMessageBox.warning(self, "Duplicate Serial", "This serial number is already registered.")
                return

        # Proceed with replacement
        success = self.IadminPageBack.replace_meter(old_meter_id, new_serial, int(initial_reading))
        if success:
            QtWidgets.QMessageBox.information(self, "Success", "Meter replaced successfully.")
            dialog.accept()
            self.all_meters_data = self.IadminPageBack.fetch_meters()
            self.update_pagination()
        else:
            QtWidgets.QMessageBox.critical(self, "Error", "Failed to replace meter.")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MetersPage()
    window.show()
    sys.exit(app.exec_())