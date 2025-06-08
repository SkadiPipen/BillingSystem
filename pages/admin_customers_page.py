import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

import sys
import os
import math

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtPrintSupport import QPrinter, QPrintPreviewDialog
from PyQt5.QtGui import QTextDocument

from backend.adminBack import adminPageBack
import base64


def image_to_base64(path):
    import base64
    with open(path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode("utf-8")
        return f"data:image/png;base64,{encoded}"


class AdminCustomersPage(QtWidgets.QWidget):
    def __init__(self, username, parent=None):
        super().__init__()
        self.parent = parent
        self.username = username
        self.IadminPageBack = adminPageBack(self.username)
        self.all_customers_data = []  # Store all customer data
        self.current_page = 1
        self.records_per_page = 10  # Number of records per page
        self.total_pages = 1
        self.setup_ui()
        self.showMaximized()

    def create_scrollable_cell(self, row, column, text):
        scrollable_widget = ScrollableTextWidget(text)
        self.customers_table.setCellWidget(row, column, scrollable_widget)

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header with title and search
        header_layout = QtWidgets.QHBoxLayout()
        title = QtWidgets.QLabel("CUSTOMERS LIST")
        title.setStyleSheet("""
            font-family: 'Montserrat', sans-serif;
            font-size: 24px;
            font-weight: bold;
        """)
        header_layout.addWidget(title)
        header_layout.addStretch()

        # Search and Add button container
        search_add_layout = QtWidgets.QHBoxLayout()

        # Search container
        search_container = QtWidgets.QHBoxLayout()

        # Search criteria dropdown
        self.search_criteria = QtWidgets.QComboBox()
        self.search_criteria.addItems(["First Name", "Last Name", "Location", "Category", "Active", "Inactive"])
        self.search_criteria.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-family: 'Roboto', sans-serif;
                min-width: 120px;
                background-color: white;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(../images/dropdown.png);
                width: 12px;
                height: 12px;
            }
        """)
        search_container.addWidget(self.search_criteria)

        # Search input
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("Search customers...")
        self.search_input_combo = QtWidgets.QComboBox()
        self.search_input_combo.addItems(["Residential", "Commercial", "Industrial"])
        self.search_input_combo.hide()  # Initially hidden

        # Apply same styling to both widgets
        input_style = """
            QLineEdit, QComboBox {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-family: 'Roboto', sans-serif;
                min-width: 250px;
            }
        """
        self.search_input.setStyleSheet(input_style)
        self.search_input_combo.setStyleSheet(input_style)

        self.search_input.textChanged.connect(self.filter_table)
        self.search_input_combo.currentTextChanged.connect(self.filter_table)

        # Add widgets to container
        search_container.addWidget(self.search_input)
        search_container.addWidget(self.search_input_combo)

        # Connect search criteria change
        self.search_criteria.currentTextChanged.connect(self.toggle_search_input)

        search_add_layout.addLayout(search_container)

        # Add button with icon
        add_btn = QtWidgets.QPushButton("ADD CUSTOMER", icon=QtGui.QIcon("../images/add.png"))
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: rgb(229, 115, 115);
                color: white;
                padding: 8px 15px;
                border-radius: 4px;
                font-family: 'Roboto', sans-serif;
            }
            QPushButton:hover {
                background-color: rgb(200, 100, 100);
            }
        """)
        add_btn.clicked.connect(self.show_add_customer_page)
        search_add_layout.addWidget(add_btn)

        header_layout.addLayout(search_add_layout)
        layout.addLayout(header_layout)

        # Table setup
        self.customers_table = QtWidgets.QTableWidget()
        self.customers_table.setAlternatingRowColors(True)
        self.customers_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: #E8F5E9;
                alternate-background-color: #FFFFFF;
            }
            QHeaderView::section {
                background-color: #B2C8B2;
                padding: 8px;
                border: none;
                font-family: 'Roboto', sans-serif;
                font-weight: bold;
            }
            QTableWidget::item:selected {
                background-color: transparent; /* Or set to same as normal background */
                color: black;
            }
            QTableWidget::item:hover {
                background-color: transparent; /* Disable hover highlight */
            }
        """)

        # Set up columns (9 columns)
        self.customers_table.setColumnCount(11)
        self.customers_table.verticalHeader().setVisible(False)
        self.customers_table.setHorizontalHeaderLabels([
            "CLIENT NUMBER", "FIRST NAME", "MIDDLE NAME", "LAST NAME", "CONTACT",
            "CATEGORY", "ADDRESS", "LOCATION", "DATE CREATED", "STATUS", "ACTION"
        ])

        # Set the table to fill all available space
        self.customers_table.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.customers_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        # Enable horizontal scrollbar
        self.customers_table.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.customers_table.setWordWrap(False)

        customer_back = adminPageBack()
        data = customer_back.fetch_clients()
        self.all_customers_data = data  # Store all customer data

        # Add pagination controls
        pagination_layout = QtWidgets.QHBoxLayout()
        pagination_layout.setAlignment(QtCore.Qt.AlignCenter)

        # First page button
        self.first_page_btn = QtWidgets.QPushButton("⏮ First")
        self.first_page_btn.clicked.connect(self.go_to_first_page)

        # Previous page button
        self.prev_page_btn = QtWidgets.QPushButton("◀ Previous")
        self.prev_page_btn.clicked.connect(self.go_to_prev_page)

        # Page indicator
        self.page_indicator = QtWidgets.QLabel("Page 1 of 1")
        self.page_indicator.setAlignment(QtCore.Qt.AlignCenter)
        self.page_indicator.setStyleSheet("font-weight: bold; min-width: 150px;")

        # Next page button
        self.next_page_btn = QtWidgets.QPushButton("Next ▶")
        self.next_page_btn.clicked.connect(self.go_to_next_page)

        # Last page button
        self.last_page_btn = QtWidgets.QPushButton("Last ⏭")
        self.last_page_btn.clicked.connect(self.go_to_last_page)

        # Records per page selector
        self.page_size_label = QtWidgets.QLabel("Records per page:")
        self.page_size_combo = QtWidgets.QComboBox()
        self.page_size_combo.addItems(["5", "10", "20", "50", "100"])
        self.page_size_combo.setCurrentText(str(self.records_per_page))
        self.page_size_combo.currentTextChanged.connect(self.change_page_size)

        # Style for pagination buttons
        pagination_btn_style = """
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

        self.first_page_btn.setStyleSheet(pagination_btn_style)
        self.prev_page_btn.setStyleSheet(pagination_btn_style)
        self.next_page_btn.setStyleSheet(pagination_btn_style)
        self.last_page_btn.setStyleSheet(pagination_btn_style)

        # Add pagination controls to layout
        pagination_layout.addWidget(self.first_page_btn)
        pagination_layout.addWidget(self.prev_page_btn)
        pagination_layout.addWidget(self.page_indicator)
        pagination_layout.addWidget(self.next_page_btn)
        pagination_layout.addWidget(self.last_page_btn)
        pagination_layout.addSpacing(20)
        pagination_layout.addWidget(self.page_size_label)
        pagination_layout.addWidget(self.page_size_combo)

        # Calculate total pages and update table
        self.update_pagination()

        # Adjust table properties
        self.customers_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.customers_table.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self.customers_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        # Create a custom delegate for text elision with tooltip
        delegate = TextEllipsisDelegate(self.customers_table)
        self.customers_table.setItemDelegate(delegate)

        # Add table and pagination to the main layout
        layout.addWidget(self.customers_table)
        layout.addLayout(pagination_layout)

        # Print Preview button
        print_btn = QtWidgets.QPushButton("PRINT PREVIEW", icon=QtGui.QIcon("../images/print.png"))
        print_btn.setStyleSheet(add_btn.styleSheet())
        print_btn.clicked.connect(self.show_print_preview)
        search_add_layout.addWidget(print_btn)

    def update_pagination(self):
        # Calculate total pages based on filtered data
        visible_rows = 0
        for row in range(len(self.all_customers_data)):
            if not self.is_row_filtered(row):
                visible_rows += 1

        self.total_pages = max(1, math.ceil(visible_rows / self.records_per_page))

        # Adjust current page if it's beyond the new total
        if self.current_page > self.total_pages:
            self.current_page = self.total_pages

        # Update page indicator
        self.page_indicator.setText(f"Page {self.current_page} of {self.total_pages}")

        # Enable/disable navigation buttons
        self.first_page_btn.setEnabled(self.current_page > 1)
        self.prev_page_btn.setEnabled(self.current_page > 1)
        self.next_page_btn.setEnabled(self.current_page < self.total_pages)
        self.last_page_btn.setEnabled(self.current_page < self.total_pages)

        # Update table with current page data
        self.populate_table(self.all_customers_data)

    def is_row_filtered(self, row_index):
        if row_index >= len(self.all_customers_data):
            return True
        customer = self.all_customers_data[row_index]
        search_by = self.search_criteria.currentText()

        if search_by in ["Active", "Inactive"]:
            search_text = search_by.lower()
            return customer[9].lower() != search_text

        if search_by == "Category":
            search_text = self.search_input_combo.currentText().lower()
        else:
            search_text = self.search_input.text().lower()

        if not search_text:
            return False

        field_mapping = {
            "First Name": 2,
            "Middle Name": 3,
            "Last Name": 4,
            "Location": 8,
            "Category": 6
        }

        field_index = field_mapping.get(search_by, -1)
        if field_index >= 0 and field_index < len(customer):
            field_value = str(customer[field_index]).lower()
            return search_text not in field_value

        return False

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
        self.current_page = 1  # Reset to first page when changing page size
        self.update_pagination()

    def populate_table(self, data):
        self.customers_table.setRowCount(0)  # Clear previous rows

        # Apply pagination and filtering
        visible_row_counter = 0
        rows_to_show = []

        # First pass: determine which rows are visible based on filters
        for row_index, customer in enumerate(data):
            if not self.is_row_filtered(row_index):
                visible_row_counter += 1

                # Check if this row should be on the current page
                start_index = (self.current_page - 1) * self.records_per_page + 1
                end_index = self.current_page * self.records_per_page

                if start_index <= visible_row_counter <= end_index:
                    rows_to_show.append(customer)

        # Set row count for visible rows on current page
        self.customers_table.setRowCount(len(rows_to_show))

        # Populate only the rows that should be visible on this page
        for table_row, customer in enumerate(rows_to_show):
            client_id, client_number, fname, middle_name, lname, contact, categ_name, address_id, location, created_at, status = customer

            # Use create_scrollable_cell for all data columns
            self.create_scrollable_cell(table_row, 0, str(client_number))
            self.create_scrollable_cell(table_row, 1, fname)
            self.create_scrollable_cell(table_row, 2, middle_name)
            self.create_scrollable_cell(table_row, 3, lname)
            self.create_scrollable_cell(table_row, 4, contact)
            self.create_scrollable_cell(table_row, 5, categ_name)
            self.create_scrollable_cell(table_row, 6, address_id)
            self.create_scrollable_cell(table_row, 7, location)
            self.create_scrollable_cell(table_row, 8, str(created_at))

            # Create status layout with label + toggle button
            status_layout = QtWidgets.QHBoxLayout()
            status_layout.setContentsMargins(20, 0, 20, 0)

            # Status label
            status_label = QtWidgets.QLabel(status)
            status_label.setStyleSheet(f"color: {'#4CAF50' if status == 'Active' else '#E57373'}; font-weight: bold;")

            # Toggle button for status
            toggle_button = QtWidgets.QPushButton()
            toggle_button.setCheckable(True)
            toggle_button.setChecked(status == "Active")
            toggle_button.setFixedSize(40, 20)
            toggle_button.setStyleSheet("""
                QPushButton {
                    background-color: red;
                    border: 1px solid #aaa;
                    border-radius: 10px;
                }
                QPushButton:checked {
                    background-color: green;
                }
            """)
            toggle_button.pressed.connect(lambda r=table_row, lbl=status_label: self.toggle_status(r, lbl))

            # Add label and button to layout
            status_layout.addWidget(status_label)
            status_layout.addStretch()
            status_layout.addWidget(toggle_button)

            # Set the layout into a QWidget
            status_container = QtWidgets.QWidget()
            status_container.setLayout(status_layout)
            self.customers_table.setCellWidget(table_row, 9, status_container)

            # Create action buttons layout
            action_layout = QtWidgets.QHBoxLayout()
            action_layout.setContentsMargins(0, 0, 0, 0)
            action_layout.setSpacing(0)

            # Add stretch before and after to center the button
            action_layout.addStretch()
            edit_button = QtWidgets.QPushButton()
            edit_button.setIcon(QtGui.QIcon("../images/edit.png"))  # Make sure you have the icon
            edit_button.setFixedSize(30, 30)
            edit_button.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                }
            """)
            edit_button.clicked.connect(lambda _, r=table_row: self.edit_customer_row(r))
            action_layout.addWidget(edit_button)
            action_layout.addStretch()

            # Set widget in cell
            action_container = QtWidgets.QWidget()
            action_container.setLayout(action_layout)
            self.customers_table.setCellWidget(table_row, 10, action_container)

    def filter_table(self):
        # Just need to update pagination, which will apply filters automatically
        self.current_page = 1  # Reset to first page when filtering
        self.update_pagination()

    def toggle_search_input(self, text):
        if text == "Category":
            self.search_input.hide()
            self.search_input_combo.show()
        else:
            self.search_input.show()
            self.search_input_combo.hide()

            # Update filtering when search type changes
        self.filter_table()

    def toggle_status(self, row, label):
        table = self.customers_table
        container = table.cellWidget(row, 9)  # Status column index
        if container:
            toggle_button = container.findChild(QtWidgets.QPushButton)
            if toggle_button:
                # Get client_id from customer data
                visible_index = 0
                selected_customer = None
                for idx, customer in enumerate(self.all_customers_data):
                    if not self.is_row_filtered(idx):
                        if visible_index == row:
                            selected_customer = customer
                            break
                        visible_index += 1

                if not selected_customer:
                    QtWidgets.QMessageBox.warning(self, "Error", "Customer not found.")
                    return

                client_id = selected_customer[0]
                current_status = selected_customer[10].capitalize()  # Ensure case for enum
                next_status = 'Inactive' if current_status == 'Active' else 'Active'

                toggle_button.blockSignals(True)

                reply = QMessageBox.question(
                    self,
                    "Confirm Status Change",
                    f"Are you sure you want to change the status to {next_status}?",
                    QMessageBox.Yes | QMessageBox.No
                )

                if reply == QMessageBox.Yes:
                    self.IadminPageBack.update_client_status(client_id, next_status)
                    label.setText(next_status)
                    label.setStyleSheet(
                        f"color: {'#4CAF50' if next_status == 'Active' else '#E57373'}; font-weight: bold;")
                    toggle_button.setChecked(next_status == "Active")
                else:
                    toggle_button.setChecked(current_status == "Active")

                toggle_button.blockSignals(False)



    def show_add_customer_page(self):
        add_dialog = QtWidgets.QDialog(self)
        add_dialog.setWindowTitle("New Customer")
        add_dialog.setModal(True)
        add_dialog.setFixedSize(1000, 700)
        add_dialog.setStyleSheet("""
            QDialog {
                background-color: #C9EBCB;
            }
            QLabel {
                font-family: 'Arial', sans-serif;
                font-weight: bold;
            }
        """)

        layout = QtWidgets.QVBoxLayout(add_dialog)
        layout.setContentsMargins(30, 5, 30, 5)
        layout.setSpacing(10)

        # Section Title
        title = QtWidgets.QLabel("ADD NEW CUSTOMER")
        title.setStyleSheet("""
            font-size: 20px;
            padding: 10px;
        """)
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)

        form_layout = QtWidgets.QGridLayout()
        form_layout.setHorizontalSpacing(40)
        form_layout.setVerticalSpacing(20)

        input_style = """
            QLineEdit, QComboBox {
                font-family: 'Arial';
                font-size: 14px;
                padding: 8px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                background-color: #ffffff;
            }
        """

        def create_labeled_widget(label_text, widget):
            container = QtWidgets.QVBoxLayout()
            label = QtWidgets.QLabel(label_text)
            label.setFont(QtGui.QFont("Arial", 10))
            container.addWidget(label)
            container.addWidget(widget)
            return container

        fields = {
            "First Name": QtWidgets.QLineEdit(),
            "Middle Name": QtWidgets.QLineEdit(),
            "Last Name": QtWidgets.QLineEdit(),
            "Contact Number": QtWidgets.QLineEdit(),
            "Category": QtWidgets.QComboBox(),
            "Location": QtWidgets.QLineEdit(),
            "Address": QtWidgets.QComboBox(),
            "Serial Number": QtWidgets.QLineEdit(),
            "First Reading": QtWidgets.QLineEdit(),
        }

        for widget in fields.values():
            widget.setStyleSheet(input_style)

        # Fetch backend data
        for category_id, category_name, category_status, category_date in self.IadminPageBack.fetch_categories():
            fields["Category"].addItem(category_name, category_id)
        for address_id, address_name, address_status, address_date in self.IadminPageBack.fetch_address():
            fields["Address"].addItem(address_name, address_id)

        # Layout inputs in 2 columns
        left_fields = ["First Name", "Middle Name", "Last Name", "Contact Number", "Category"]
        right_fields = ["Location", "Address", "Serial Number", "First Reading"]

        for i, key in enumerate(left_fields):
            form_layout.addLayout(create_labeled_widget(f"{key}:", fields[key]), i, 0)

        for i, key in enumerate(right_fields):
            form_layout.addLayout(create_labeled_widget(f"{key}:", fields[key]), i, 1)

        layout.addLayout(form_layout)

        # Buttons
        button_container = QtWidgets.QWidget()
        button_layout = QtWidgets.QHBoxLayout(button_container)
        button_layout.setAlignment(QtCore.Qt.AlignRight)

        cancel_btn = QtWidgets.QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                padding: 8px 15px;
                border-radius: 4px;
                font-family: 'Roboto', sans-serif;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        cancel_btn.clicked.connect(add_dialog.reject)

        save_btn = QtWidgets.QPushButton("Save Customer")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: white;
                padding: 8px 15px;
                border-radius: 4px;
                font-family: 'Roboto', sans-serif;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)

        def save_customer():
            category_combo = fields["Category"]
            address_combo = fields["Address"]
            category_id = category_combo.currentData()
            address_id = address_combo.currentData()

            input_values = {
                label: widget.text().strip() if isinstance(widget, QtWidgets.QLineEdit)
                else widget.currentText().strip()
                for label, widget in fields.items()
            }

            missing_fields = [label for label in fields if label != "Middle Name" and not input_values[label]]
            if missing_fields:
                QtWidgets.QMessageBox.warning(self, "Missing Fields", "Please fill in all the required fields.")
                return

            name_fields = ["First Name", "Middle Name", "Last Name"]
            invalid_name_fields = [label for label in name_fields if
                                   input_values[label] and not input_values[label].replace(" ", "").isalpha()]
            if invalid_name_fields:
                QtWidgets.QMessageBox.warning(self, "Error",
                                              f"These fields must contain letters only: {', '.join(invalid_name_fields)}")
                return

            try:
                float(input_values["Contact Number"])
            except ValueError:
                QtWidgets.QMessageBox.warning(self, "Error", "Contact Number must be a valid number.")
                return

            try:
                meter_reading = float(input_values["First Reading"])
            except ValueError:
                QtWidgets.QMessageBox.warning(self, "Error", "First Reading must be a number.")
                return

            serial_number = input_values["Serial Number"]
            # ✅ Check if the serial number already exists
            if self.IadminPageBack.serial_exists(serial_number):
                QtWidgets.QMessageBox.warning(self, "Duplicate Serial", "This serial number is already registered.")
                return

            meter_id = self.IadminPageBack.add_meter(meter_reading, serial_number)
            new_client_id = self.IadminPageBack.add_client(
                client_name=input_values["First Name"],
                client_lname=input_values["Last Name"],
                client_contact_num=input_values["Contact Number"],
                client_location=input_values["Location"],
                meter_id=meter_id,
                address_id=address_id,
                categ_id=category_id,
                client_mname=input_values["Middle Name"],
                status="Active"
            )

            QtWidgets.QMessageBox.information(self, "Success", "Customer added successfully.")
            add_dialog.accept()

            self.all_customers_data = self.IadminPageBack.fetch_clients()
            self.update_pagination()

        save_btn.clicked.connect(save_customer)
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(save_btn)
        layout.addWidget(button_container)

        add_dialog.exec_()

    def edit_customer_row(self, table_row):
        # Map visible row to actual data index
        visible_index = 0
        client_index = -1
        for row_index, customer in enumerate(self.all_customers_data):
            if not self.is_row_filtered(row_index):
                if visible_index == table_row:
                    client_index = row_index
                    break
                visible_index += 1

        if client_index == -1:
            return

        customer = self.all_customers_data[client_index]
        client_id, client_number, fname, middle_name, lname, contact, categ_name, address_id, location, created_at, status = customer

        # Create edit dialog
        edit_dialog = QtWidgets.QDialog(self)
        edit_dialog.setWindowTitle("Edit Customer")
        edit_dialog.setModal(True)
        edit_dialog.setFixedSize(600, 500)  # Adjusted size for single column
        edit_dialog.setStyleSheet("""
            QDialog {
                background-color: #C9EBCB;
            }
            QLabel {
                font-family: 'Arial', sans-serif;
                font-weight: bold;
            }
        """)

        layout = QtWidgets.QVBoxLayout(edit_dialog)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(15)

        # Section Title
        title = QtWidgets.QLabel("EDIT CUSTOMER DETAILS")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)

        input_style = """
            QLineEdit {
                font-family: 'Arial';
                font-size: 14px;
                padding: 8px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                background-color: #ffffff;
            }
        """

        # Input Fields
        fname_input = QtWidgets.QLineEdit(fname)
        mname_input = QtWidgets.QLineEdit(middle_name)
        lname_input = QtWidgets.QLineEdit(lname)
        contact_input = QtWidgets.QLineEdit(contact)
        location_input = QtWidgets.QLineEdit(location)

        fname_input.setStyleSheet(input_style)
        mname_input.setStyleSheet(input_style)
        lname_input.setStyleSheet(input_style)
        contact_input.setStyleSheet(input_style)
        location_input.setStyleSheet(input_style)

        # Add form rows one by one
        layout.addWidget(QtWidgets.QLabel("First Name"))
        layout.addWidget(fname_input)

        layout.addWidget(QtWidgets.QLabel("Middle Name"))
        layout.addWidget(mname_input)

        layout.addWidget(QtWidgets.QLabel("Last Name"))
        layout.addWidget(lname_input)

        layout.addWidget(QtWidgets.QLabel("Contact Number"))
        layout.addWidget(contact_input)

        layout.addWidget(QtWidgets.QLabel("Location"))
        layout.addWidget(location_input)

        # Buttons
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSpacing(10)
        button_layout.addStretch()

        cancel_btn = QtWidgets.QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                padding: 8px 15px;
                border-radius: 4px;
                font-family: 'Roboto', sans-serif;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        cancel_btn.clicked.connect(edit_dialog.reject)

        save_btn = QtWidgets.QPushButton("Save Changes")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #A8D8B9;
                color: white;
                padding: 8px 15px;
                border-radius: 4px;
                font-family: 'Roboto', sans-serif;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #8CC084;
            }
        """)
        save_btn.clicked.connect(lambda: self.save_edited_customer(
            client_id,
            fname_input, mname_input, lname_input,
            contact_input, location_input,
            edit_dialog
        ))

        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(save_btn)
        layout.addLayout(button_layout)

        edit_dialog.exec_()

    def save_edited_customer(self, client_id, fname_input, mname_input, lname_input, contact_input, location_input,
                         dialog):
        fname = fname_input.text().strip()
        mname = mname_input.text().strip()
        lname = lname_input.text().strip()
        contact = contact_input.text().strip()
        location = location_input.text().strip()

        # Validation
        if not fname or not lname or not contact or not location:
            QtWidgets.QMessageBox.warning(dialog, "Error", "All required fields must be filled.")
            return

        try:
            # Use the existing instance with correct username instead of creating new one
            self.IadminPageBack.update_client(
                client_id,
                fname,
                lname,
                contact,
                location,
                mname
            )

            # Refresh UI
            self.all_customers_data = self.IadminPageBack.fetch_clients()
            self.update_pagination()
            QtWidgets.QMessageBox.information(dialog, "Success", "Customer updated successfully.")
            dialog.accept()
        except Exception as e:
            QtWidgets.QMessageBox.critical(dialog, "Error", f"Failed to update customer: {str(e)}")

    def show_print_preview(self):
        # Load logo as base64
        logo_path = os.path.join(os.path.dirname(__file__), "..", "images", "logosowbasco.png")
        logo_base64 = image_to_base64(logo_path)

        html = f"""
        <table width="100%" style="border-collapse: collapse;">
          <tr>
            <td style="width: 1px; padding-right: 10px; vertical-align: top;">
              <img src="{logo_base64}" width="120">
            </td>
            <td style="text-align: center;">
              <div style="font-family: Arial, sans-serif; line-height: 1.1;">
                <div style="font-size: 14pt; font-weight: bold;">Southwestern Barangays Water Service Cooperative II</div>
                <div style="font-size: 11pt; font-weight: bold;">(SOWBASCO)</div>
                <div style="font-size: 10pt;">Consuelo, San Francisco, Cebu</div>
              </div>
            </td>
          </tr>
        </table>

        <hr style="margin: 8px 0;">

        <div style="text-align: center; font-weight: bold; font-size: 11pt; margin-bottom: 10px;">List of Clients</div>

        <table border="1" cellspacing="0" cellpadding="5" width="100%">
          <thead>
            <tr>
              <th>Client No.</th>
              <th>First Name</th>
              <th>Middle Name</th>
              <th>Last Name</th>
              <th>Contact</th>
              <th>Category</th>
              <th>Address</th>
              <th>Location</th>
              <th>Date Created</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
        """

        visible_data = []
        visible_index = 0
        start = (self.current_page - 1) * self.records_per_page + 1
        end = self.current_page * self.records_per_page

        for row_index, customer in enumerate(self.all_customers_data):
            if not self.is_row_filtered(row_index):
                visible_index += 1
                if start <= visible_index <= end:
                    visible_data.append(customer)

        for customer in visible_data:
            client_id, client_number, fname, mname, lname, contact, category, address, location, date_created, status = customer
            html += f"""
            <tr>
                <td>{client_number}</td>
                <td>{fname}</td>
                <td>{mname}</td>
                <td>{lname}</td>
                <td>{contact}</td>
                <td>{category}</td>
                <td>{address}</td>
                <td>{location}</td>
                <td>{date_created}</td>
                <td>{status}</td>
            </tr>
            """

        html += "</tbody></table>"

        # Create document and print preview
        document = QTextDocument()
        document.setHtml(html)

        printer = QPrinter(QPrinter.HighResolution)
        preview_dialog = QPrintPreviewDialog(printer, self)
        preview_dialog.setWindowTitle("Print Preview - Customer List")
        preview_dialog.paintRequested.connect(document.print_)
        preview_dialog.exec_()
        self.IadminPageBack.log_action("Printed customer list preview")


class ScrollableTextWidget(QtWidgets.QWidget):

    def __init__(self, text, parent=None):
        super(ScrollableTextWidget, self).__init__(parent)
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create scrollable text area
        self.text_area = QtWidgets.QScrollArea()
        self.text_area.setWidgetResizable(True)
        self.text_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.text_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.text_area.setFrameShape(QtWidgets.QFrame.NoFrame)

        # Create a label with the text
        self.label = QtWidgets.QLabel(text)
        self.label.setTextFormat(QtCore.Qt.PlainText)
        self.label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        # Add label to scroll area
        self.text_area.setWidget(self.label)

        # Add scroll area to layout
        layout.addWidget(self.text_area)

        # Set the widget's style
        self.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
            }
            QLabel {
                background-color: transparent;
                padding-left: 4px;
                padding-right: 4px;
            }
            QScrollBar:horizontal {
                height: 10px;
                background: transparent;
                margin: 0px;
            }
            QScrollBar::handle:horizontal {
                background: #c0c0c0;
                min-width: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
            }
        """)

        # Add tooltip for the full text
        self.setToolTip(text)

        # Install event filter to track mouse events
        self.installEventFilter(self)

    def text(self):
        return self.label.text()

    def eventFilter(self, obj, event):
        if obj is self:
            if event.type() == QtCore.QEvent.Enter:
                # Show scrollbar when mouse enters
                self.text_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
                return True
            elif event.type() == QtCore.QEvent.Leave:
                # Hide scrollbar when mouse leaves
                self.text_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
                return True
        return super(ScrollableTextWidget, self).eventFilter(obj, event)


class TextEllipsisDelegate(QtWidgets.QStyledItemDelegate):

    def __init__(self, parent=None):
        super(TextEllipsisDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        # Use default painting
        super(TextEllipsisDelegate, self).paint(painter, option, index)

    def helpEvent(self, event, view, option, index):
        # Show tooltip when hovering if text is truncated
        if not event or not view:
            return False

        if event.type() == QtCore.QEvent.ToolTip:
            # Get the cell widget
            cell_widget = view.cellWidget(index.row(), index.column())

            if cell_widget and isinstance(cell_widget, ScrollableTextWidget):
                # Show tooltip for ScrollableTextWidget
                QtWidgets.QToolTip.showText(event.globalPos(), cell_widget.text(), view)
                return True
            else:
                # For standard items
                item = view.itemFromIndex(index)
                if item:
                    text = item.text()
                    width = option.rect.width()
                    metrics = QtGui.QFontMetrics(option.font)
                    elidedText = metrics.elidedText(text, QtCore.Qt.ElideRight, width)

                    # If text is truncated, show tooltip
                    if elidedText != text:
                        QtWidgets.QToolTip.showText(event.globalPos(), text, view)
                    else:
                        QtWidgets.QToolTip.hideText()

                    return True

        return super(TextEllipsisDelegate, self).helpEvent(event, view, option, index)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = AdminCustomersPage()
    window.show()
    sys.exit(app.exec_())