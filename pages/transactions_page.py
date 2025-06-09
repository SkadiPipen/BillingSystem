import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import sys
import os
import math
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt5 import QtCore, QtGui, QtWidgets
from backend.adminBack import adminPageBack
from PyQt5.QtPrintSupport import QPrinter, QPrintPreviewDialog
from PyQt5.QtGui import QTextDocument
import base64

def image_to_base64(path):
    with open(path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode("utf-8")
        return f"data:image/png;base64,{encoded}"

class TransactionsPage(QtWidgets.QWidget):
    def __init__(self, username=None, parent=None):
        super().__init__(parent)
        self.username = username
        self.all_transactions_data = []
        self.current_page = 1
        self.records_per_page = 10
        self.total_pages = 1
        self.setup_ui()
        self.showMaximized()

    def create_scrollable_cell(self, row, column, text):
        scrollable_widget = ScrollableTextWidget(text)
        self.transaction_table.setCellWidget(row, column, scrollable_widget)

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Create a header panel with some padding
        header_panel = QtWidgets.QWidget()
        header_panel.setStyleSheet("background-color: #f5f5f5; border-bottom: 1px solid #ddd;")
        header_layout = QtWidgets.QVBoxLayout(header_panel)
        header_layout.setContentsMargins(20, 15, 20, 15)

        # Header with title, search bar, and dropdown
        controls_layout = QtWidgets.QHBoxLayout()
        title = QtWidgets.QLabel("TRANSACTIONS")
        title.setStyleSheet("""
            font-family: 'Montserrat', sans-serif;
            font-size: 24px;
            font-weight: bold;
        """)
        controls_layout.addWidget(title)
        controls_layout.addStretch()

        # Search container
        search_container = QtWidgets.QHBoxLayout()
        self.filter_combo = QtWidgets.QComboBox()
        self.filter_combo.addItems([
            "Transaction Number",
            "Client Name",
            "Employee",
            "Date",
            "Status: Paid",
            "Status: Pending",
            "Status: Voided"
        ])

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
        search_container.addWidget(self.filter_combo)

        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("Search transactions...")
        self.search_input_date = QtWidgets.QDateEdit()
        self.search_input_date.setCalendarPopup(True)
        self.search_input_date.hide()

        input_style = """
            QLineEdit, QDateEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-family: 'Roboto', sans-serif;
                min-width: 250px;
                background-color: white;
            }
        """
        self.search_input.setStyleSheet(input_style)
        self.search_input_date.setStyleSheet(input_style)

        search_container.addWidget(self.search_input)
        search_container.addWidget(self.search_input_date)

        self.filter_combo.currentTextChanged.connect(self.toggle_search_input)
        self.search_input.textChanged.connect(self.filter_table)
        self.search_input_date.dateChanged.connect(self.filter_table)

        controls_layout.addLayout(search_container)

        # Transaction type dropdown
        self.transaction_type_combo = QtWidgets.QComboBox()
        self.transaction_type_combo.addItems(["All Transactions", "Daily Transaction", "Monthly Transaction"])
        self.transaction_type_combo.setStyleSheet("""
            QComboBox {
                padding: 6px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-family: 'Roboto', sans-serif;
            }
        """)
        self.transaction_type_combo.currentIndexChanged.connect(self.filter_table)
        controls_layout.addWidget(self.transaction_type_combo)


        header_layout.addLayout(controls_layout)
        layout.addWidget(header_panel)

        # Create table with horizontal scrollbar enabled - using all remaining space
        self.transaction_table = QtWidgets.QTableWidget()
        self.transaction_table.setAlternatingRowColors(True)
        self.transaction_table.setStyleSheet("""
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
        self.transaction_table.setColumnCount(9)
        self.transaction_table.setHorizontalHeaderLabels([
            "TRANSACTION NUMBER", "PAYMENT DATE", "CLIENT NUMBER", "CLIENT NAME", "READING", "DUE DATE", "CONSUMPTION",
            "STATUS", "AMOUNT"
        ])

        # Set the table to fill all available space
        self.transaction_table.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.transaction_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        # Enable horizontal scrollbar
        self.transaction_table.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.transaction_table.setWordWrap(False)

        # Fetch all transactions data
        IadminPageBack = adminPageBack()
        self.all_transactions_data = IadminPageBack.fetch_transactions()

        self.transaction_table.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self.transaction_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.transaction_table.verticalHeader().setVisible(False)

        # Create a custom delegate for text elision with tooltip
        delegate = TextEllipsisDelegate(self.transaction_table)
        self.transaction_table.setItemDelegate(delegate)

        # Add table to the main layout with full expansion
        layout.addWidget(self.transaction_table)

        # Label to display total amount based on filtered status

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

        layout.addLayout(pagination_layout)

        # Calculate total pages and update table
        self.update_pagination()

        # Create sub-layout for search and buttons
        search_add_layout = QtWidgets.QHBoxLayout()

        # Add existing widgets
        search_add_layout.addLayout(search_container)

        # Add Print Preview Button (styled like Add Customer)
        print_btn = QtWidgets.QPushButton("PRINT PREVIEW", icon=QtGui.QIcon("../images/print.png"))
        print_btn.setStyleSheet("""
            QPushButton {
                background-color: #E57373;
                color: white;
                padding: 8px 15px;
                border-radius: 4px;
                font-family: 'Roboto', sans-serif;
            }
            QPushButton:hover {
                background-color: #C62828;
            }
        """)
        print_btn.clicked.connect(self.show_print_preview)
        search_add_layout.addWidget(print_btn)

        # Add the layout to the controls header
        controls_layout.addLayout(search_add_layout)




    def get_filtered_status_label(self):
        # Check if all visible rows are PAID or PENDING
        paid_count = 0
        pending_count = 0
        visible_index = 0
        start = (self.current_page - 1) * self.records_per_page + 1
        end = self.current_page * self.records_per_page

        for row_index, transaction in enumerate(self.all_transactions_data):
            if not self.is_row_filtered(row_index):
                visible_index += 1
                if start <= visible_index <= end:
                    status = str(transaction[8]).upper()
                    if status == "PAID":
                        paid_count += 1
                    elif status == "PENDING":
                        pending_count += 1

        if paid_count > 0 and pending_count == 0:
            return "PAID"
        elif pending_count > 0 and paid_count == 0:
            return "PENDING"
        elif paid_count == 0 and pending_count == 0:
            return "None"
        else:
            return "Mixed"

    def show_print_preview(self):
        from backend.adminBack import adminPageBack
        IadminPageBack = adminPageBack()

        logo_path = os.path.join(os.path.dirname(__file__), "..", "images", "logosowbasco.png")
        logo_base64 = image_to_base64(logo_path)

        visible_data = []
        visible_index = 0
        start = (self.current_page - 1) * self.records_per_page + 1
        end = self.current_page * self.records_per_page

        for row_index, transaction in enumerate(self.all_transactions_data):
            if not self.is_row_filtered(row_index):
                visible_index += 1
                if start <= visible_index <= end:
                    visible_data.append(transaction)

        selected_type = self.transaction_type_combo.currentText()
        if selected_type == "Daily Transaction":
            report_title = "Daily Transactions"
        elif selected_type == "Monthly Transaction":
            report_title = "Monthly Transactions"
        else:
            report_title = "Transaction Report"

        paid_con = pend_con = 0.0
        paid_amt = pend_amt = 0.0

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
        <div style="text-align: center; font-weight: bold; font-size: 11pt; margin-bottom: 10px;">{report_title}</div>

        <table border="1" cellspacing="0" cellpadding="5"
       style="width: 100%; table-layout: fixed; font-size:8pt; font-family: Arial; border-collapse: collapse;">
          <colgroup>
            <col style="width: 11%;">
            <col style="width: 11%;">
            <col style="width: 11%;">
            <col style="width: 11%;">
            <col style="width: 11%;">
            <col style="width: 11%;">
            <col style="width: 11%;">
            <col style="width: 11%;">
            <col style="width: 12%;">
          </colgroup>
          <thead>
            <tr style="height: 30px;">
              <th style="white-space: nowrap; text-align: left;">Transaction No.</th>
              <th style="white-space: nowrap; text-align: left;">Payment Date</th>
              <th style="white-space: nowrap; text-align: left;">Client No.</th>
              <th style="white-space: nowrap; text-align: left;">Client Name</th>
              <th style="white-space: nowrap; text-align: left;">Employee</th>
              <th style="white-space: nowrap; text-align: left;">Due Date</th>
              <th style="white-space: nowrap; text-align: right;">Consumption</th>
              <th style="white-space: nowrap; text-align: left;">Status</th>
              <th style="white-space: nowrap; text-align: right;">Amount</th>
            </tr>
          </thead>

          <tbody>
        """

        for trans in visible_data:
            try:
                status = str(trans[8]).strip().upper()
                con = float(trans[5])
                amt = float(trans[6])
                if status == "PAID":
                    paid_con += con
                    paid_amt += amt
                elif status == "PENDING":
                    pend_con += con
                    pend_amt += amt
            except:
                continue

            # Get reading display text (like in populate_table)
            try:
                reading_text = "N/A"
                reading_id = trans[4]
                if reading_id:
                    reading = IadminPageBack.get_prev_current_by_id(reading_id)
                    if reading and isinstance(reading, (list, tuple)) and len(reading) == 2:
                        prev, curr = reading
                        if prev is not None and curr is not None:
                            reading_text = f"Prev: {float(prev):,.2f}<br>Current: {float(curr):,.2f}"
            except Exception as e:
                reading_text = "Error"

            html += f"""
            <tr>
              <td>{trans[0]}</td>
              <td>{trans[1]}</td>
              <td>{trans[2]}</td>
              <td>{trans[3]}</td>
              <td>{reading_text}</td>
              <td>{trans[7]}</td>
              <td align="right">{con:,.2f}</td>
              <td>{status.title()}</td>
              <td align="right" style="white-space: nowrap;">₱{amt:,.2f}</td>
            </tr>
            """

        if self.filter_combo.currentText() != "Status: Voided":
            total_con = paid_con + pend_con
            total_amt = paid_amt + pend_amt

            html += f"""
            <tr style="font-size: 8pt;">
              <td colspan="4" style="border:none;"></td>
              <td colspan="2" align="left"><b>Total Paid Consumption:</b></td>
              <td align="right"><b>{paid_con:,.2f}</b></td>
              <td><b>Total Paid Amount:</b></td>
              <td align="right"><b>₱{paid_amt:,.2f}</b></td>
            </tr>
            <tr style="font-size: 8pt;">
              <td colspan="4" style="border:none;"></td>
              <td colspan="2" align="left"><b>Total Pending Consumption:</b></td>
              <td align="right"><b>{pend_con:,.2f}</b></td>
              <td><b>Total Pending Amount:</b></td>
              <td align="right"><b>₱{pend_amt:,.2f}</b></td>
            </tr>
            <tr style="font-size: 8pt;">
              <td colspan="4" style="border:none; border-top:2px solid black;"></td>
              <td colspan="2" align="left"><b style="color: teal;">Grand Total Consumption:</b></td>
              <td align="right" style="border-top:2px solid black;"><b style="color: teal;">{total_con:,.2f}</b></td>
              <td><b style="color: teal;">Grand Total Amount:</b></td>
              <td align="right" style="border-top:2px solid black;"><b style="color: teal;">₱{total_amt:,.2f}</b></td>
            </tr>
            """

        html += "</tbody></table>"

        doc = QTextDocument()
        doc.setHtml(html)

        printer = QPrinter(QPrinter.HighResolution)
        preview = QPrintPreviewDialog(printer, self)
        preview.setWindowTitle("Print Preview - Transactions")
        preview.paintRequested.connect(doc.print_)
        preview.exec_()

    def update_pagination(self):
        # Calculate total pages based on filtered data
        visible_rows = 0
        for row in range(len(self.all_transactions_data)):
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
        self.populate_table(self.all_transactions_data)

    def is_row_filtered(self, row_index):
        filter_by = self.filter_combo.currentText()
        search_text = self.search_input.text().lower()
        transaction = self.all_transactions_data[row_index]


        # Force-hide voided unless explicitly selected
        if filter_by != "Status: Voided" and str(transaction[8]).strip().lower() == "voided":
            return True

        if filter_by == "Transaction Number":
            return search_text not in str(transaction[0]).lower()
        elif filter_by == "Client Name":
            return search_text not in str(transaction[3]).lower()
        elif filter_by == "Employee":
            return search_text not in str(transaction[4]).lower()
        elif filter_by == "Date":
            return search_text not in str(transaction[1]).lower()
        elif filter_by.startswith("Status:"):
            status_target = filter_by.split(":")[1].strip().lower()
            transaction_status = str(transaction[8]).strip().lower()
            return transaction_status != status_target
        return False

        # Get transaction data for the row
        transaction = self.all_transactions_data[row_index]
        
        # Apply current filter
        filter_by = self.filter_combo.currentText()
        
        if filter_by == "Date":
            search_text = self.search_input_date.date().toString("yyyy-MM-dd").lower()
        else:
            search_text = self.search_input.text().lower()

        filter_by = self.filter_combo.currentText()
        search_text = ""

        if filter_by.startswith("Status:"):
            status_target = filter_by.split(":")[1].strip().lower()
            transaction_status = str(transaction[8]).strip().lower()
            if transaction_status != status_target:
                return True
            # still apply transaction type filter
            return self.is_transaction_type_filtered(transaction)

        # existing logic for other filters:
        if filter_by == "Date":
            search_text = self.search_input_date.date().toString("yyyy-MM-dd").lower()
        else:
            search_text = self.search_input.text().lower()

        # Check if the row matches the filter
        # Getting appropriate field index for the search criteria
        field_mapping = {
            "Transaction Number": 0,   # trans_code
            "Client Name": 3,          # client_name
            "Employee": 4,             # user_name
            "Date": 1                  # trans_payment_date
        }
        
        field_index = field_mapping.get(filter_by, -1)
        if field_index >= 0 and field_index < len(transaction):
            field_value = str(transaction[field_index]).lower()
            if search_text not in field_value:
                return True  # Filter out this row

        # Apply transaction type filter
        return self.is_transaction_type_filtered(transaction)

    def is_transaction_type_filtered(self, transaction):
        trans_type_index = self.transaction_type_combo.currentIndex()
        if trans_type_index == 0:  # All Transactions
            return False  # Don't filter
            
        # Get transaction date
        payment_date_str = str(transaction[1]).strip()
        payment_date = QtCore.QDate.fromString(payment_date_str, "yyyy-MM-dd")
        if not payment_date.isValid():
            return True  # Filter out invalid dates
            
        today = QtCore.QDate.currentDate()
        
        if trans_type_index == 1:  # Daily Transaction
            return payment_date != today
        elif trans_type_index == 2:  # Monthly Transaction
            return payment_date.month() != today.month() or payment_date.year() != today.year()
            
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
        from backend.adminBack import adminPageBack
        IadminPageBack = adminPageBack()

        self.transaction_table.setRowCount(0)
        visible_row_counter = 0
        rows_to_show = []

        for row_index, transaction in enumerate(data):
            if not self.is_row_filtered(row_index):
                visible_row_counter += 1
                start_index = (self.current_page - 1) * self.records_per_page + 1
                end_index = self.current_page * self.records_per_page
                if start_index <= visible_row_counter <= end_index:
                    rows_to_show.append(transaction)

        self.transaction_table.setRowCount(len(rows_to_show) + 1)

        for table_row, transaction in enumerate(rows_to_show):
            trans_code = transaction[0]
            trans_payment_date = transaction[1]
            client_number = transaction[2]
            client_name = transaction[3]
            reading_id = transaction[4]
            billing_consumption = transaction[5]
            billing_total = transaction[6]
            billing_due = transaction[7]
            trans_status = transaction[8]
            reading_date = transaction[9] if len(transaction) > 9 else "N/A"

            # Get reading text
            try:
                reading_text = "N/A"
                if reading_id:
                    reading = IadminPageBack.get_prev_current_by_id(reading_id)

                    if reading and isinstance(reading, (list, tuple)) and len(reading) == 2:
                        prev, curr = reading
                        if prev is not None and curr is not None:
                            reading_text = f"Previous: {float(prev):,.2f}\nCurrent: {float(curr):,.2f}"
                        else:
                            reading_text = "N/A"
                    else:
                        reading_text = "N/A"
            except Exception as e:
                print(f"Reading fetch error for ID {reading_id}: {e}")
                reading_text = "Error"

            self.create_scrollable_cell(table_row, 4, reading_text)

            # Display date logic
            status_str = str(trans_status).strip().upper() if trans_status else ""
            payment_display = trans_payment_date if status_str == "PAID" else reading_date

            # Display table cells
            self.create_scrollable_cell(table_row, 0, str(trans_code))
            self.create_scrollable_cell(table_row, 1, str(payment_display))
            self.create_scrollable_cell(table_row, 2, str(client_number))
            self.create_scrollable_cell(table_row, 3, str(client_name))

            self.create_scrollable_cell(table_row, 5, str(billing_due))  # DUE DATE here
            self.create_scrollable_cell(table_row, 6,
                                        f"{float(billing_consumption):,.2f}" if billing_consumption else "0.00")  # CONSUMPTION

            # Correct STATUS in Column 7
            status_label = QtWidgets.QLabel(str(trans_status))
            status_label.setStyleSheet(
                f"color: {'#4CAF50' if str(trans_status).upper() == 'PAID' else '#E57373'}; font-weight: bold;")
            self.transaction_table.setCellWidget(table_row, 7, status_label)

            # Correct AMOUNT in Column 8
            try:
                amount = f"₱{float(billing_total):,.2f}" if billing_total else "₱0.00"
            except:
                amount = "₱0.00"
            self.create_scrollable_cell(table_row, 8, amount)

        # Summary Calculations
        paid_con = pend_con = paid_amt = pend_amt = 0.0
        for trans in rows_to_show:
            try:
                status = str(trans[8]).strip().upper()
                con = float(trans[5]) if trans[5] else 0.0
                amt = float(trans[6]) if trans[6] else 0.0
                if status == "PAID":
                    paid_con += con
                    paid_amt += amt
                elif status == "PENDING":
                    pend_con += con
                    pend_amt += amt
            except:
                continue

        summary_start_row = len(rows_to_show)
        current_filter = self.filter_combo.currentText()
        if current_filter == "Status: Voided":
            return

        def add_summary_row(row, label1, value1, label2, value2):
            self.transaction_table.setItem(row, 5, QtWidgets.QTableWidgetItem(label1))
            self.transaction_table.setItem(row, 6, QtWidgets.QTableWidgetItem(f"{value1:,.2f}"))
            self.transaction_table.setItem(row, 7, QtWidgets.QTableWidgetItem(label2))
            self.transaction_table.setItem(row, 8, QtWidgets.QTableWidgetItem(f"₱{value2:,.2f}"))

        if current_filter == "Status: Paid":
            self.transaction_table.setRowCount(summary_start_row + 1)
            add_summary_row(summary_start_row, "Total Paid Consumption", paid_con, "Total Paid Amount", paid_amt)
        elif current_filter == "Status: Pending":
            self.transaction_table.setRowCount(summary_start_row + 1)
            add_summary_row(summary_start_row, "Total Pending Consumption", pend_con, "Total Pending Amount", pend_amt)
        else:
            total_con = paid_con + pend_con
            total_amt = paid_amt + pend_amt
            self.transaction_table.setRowCount(summary_start_row + 3)
            add_summary_row(summary_start_row, "Total Paid Consumption", paid_con, "Total Paid Amount", paid_amt)
            add_summary_row(summary_start_row + 1, "Total Pending Consumption", pend_con, "Total Pending Amount",
                            pend_amt)
            add_summary_row(summary_start_row + 2, "Grand Total Consumption", total_con, "Grand Total Amount",
                            total_amt)

        # Style the summary rows
        for row in range(summary_start_row, self.transaction_table.rowCount()):
            for col in range(5, 9):
                item = self.transaction_table.item(row, col)
                if item:
                    font = self.transaction_table.font()
                    font.setPointSize(font.pointSize() - 1)
                    font.setBold(True)
                    item.setFont(font)

    def toggle_search_input(self, text):
        if text == "Date":
            self.search_input.hide()
            self.search_input_date.show()
        else:
            self.search_input.show()
            self.search_input_date.hide()
        
        # Update filtering when search type changes
        self.filter_table()

    def filter_table(self):
        # Just need to update pagination, which will apply filters automatically
        self.current_page = 1  # Reset to first page when filtering
        self.update_pagination()

        # Dynamically change header label
        current_filter = self.filter_combo.currentText()
        if current_filter == "Status: Pending":
            self.transaction_table.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem("READING DATE"))
        else:
            self.transaction_table.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem("PAYMENT DATE"))

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
    window = TransactionsPage()
    window.show()
    sys.exit(app.exec_())