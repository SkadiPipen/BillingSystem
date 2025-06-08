# on and off status

import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

from backend.adminBack import adminPageBack
from repositories.category_repository import CategoryRepository


class CategoryPage(QtWidgets.QWidget):
    def __init__(self, username, parent=None):
        super().__init__()
        self.parent = parent
        self.username = username
        self.rateblock_panel = None
        self.IadminPageBack = adminPageBack(self.username)
        self.setup_ui()

    def create_scrollable_cell(self, row, column, text):
        scrollable_widget = ScrollableTextWidget(text)
        self.categorys_table.setCellWidget(row, column, scrollable_widget)

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header with title and search
        header_layout = QtWidgets.QHBoxLayout()
        title = QtWidgets.QLabel("CATEGORIES LIST")
        title.setStyleSheet("""
            font-family: 'Montserrat', sans-serif;
            font-size: 24px;
            font-weight: bold;
        """)
        header_layout.addWidget(title)
        header_layout.addStretch()

        search_add_layout = QtWidgets.QHBoxLayout()

        # Search container
        search_container = QtWidgets.QHBoxLayout()

        # Search input
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("Search address by name...")

        # Apply same styling to both widgets
        input_style = """
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-family: 'Roboto', sans-serif;
                min-width: 250px;
            }
        """
        self.search_input.setStyleSheet(input_style)
        self.search_input.textChanged.connect(self.filter_table)

        # Add widgets to container
        search_container.addWidget(self.search_input)

        search_add_layout.addLayout(search_container)


        header_layout.addLayout(search_add_layout)
        layout.addLayout(header_layout)

        # Table setup
        self.categorys_table = QtWidgets.QTableWidget()
        self.categorys_table.setAlternatingRowColors(True)
        self.categorys_table.setStyleSheet("""
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
        """)

        # Set up columns (10 columns)
        self.categorys_table.setColumnCount(4)
        self.categorys_table.verticalHeader().setVisible(False)
        self.categorys_table.setHorizontalHeaderLabels([
            "NAME", "DATE", "STATUS", "ACTION"
        ])

        # Set the table to fill all available space
        self.categorys_table.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.categorys_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        # Enable horizontal scrollbar
        self.categorys_table.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.categorys_table.setWordWrap(False)

        self.populate_table(self.IadminPageBack.fetch_categories())

        # Adjust table properties
        self.categorys_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.categorys_table.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self.categorys_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        # Create a custom delegate for text elision with tooltip
        delegate = TextEllipsisDelegate(self.categorys_table)
        self.categorys_table.setItemDelegate(delegate)

        # Add table to the main layout with full expansion
        layout.addWidget(self.categorys_table)

    def populate_table(self, data, row=None):
        self.categorys_table.setRowCount(0)
        self.categorys_table.setRowCount(len(data))

        for row, category in enumerate(data):
            category_id, category_name, category_status, category_date = category

            self.create_scrollable_cell(row, 0, category_name)
            self.create_scrollable_cell(row, 1, str(category_date))

            status_layout = QtWidgets.QHBoxLayout()
            status_layout.setContentsMargins(5, 0, 5, 0)

            status_label = QtWidgets.QLabel(category_status)
            status_label.setStyleSheet(
                f"color: {'#4CAF50' if category_status == 'Active' else '#E57373'}; font-weight: bold;")

            toggle_button = QtWidgets.QPushButton()
            toggle_button.setCheckable(True)
            toggle_button.setChecked(category_status == "Active")
            toggle_button.setFixedSize(40, 20)
            toggle_button.setProperty("category_id", category_id)
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
            toggle_button.pressed.connect(lambda r=row, lbl=status_label: self.toggle_status(r, lbl))

            status_layout.addWidget(status_label)
            status_layout.addStretch()
            status_layout.addWidget(toggle_button)

            status_container = QtWidgets.QWidget()
            status_container.setLayout(status_layout)
            self.categorys_table.setCellWidget(row, 2, status_container)

            actions_widget = QtWidgets.QWidget()
            actions_layout = QtWidgets.QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            actions_layout.setSpacing(15)
            actions_layout.setAlignment(QtCore.Qt.AlignCenter)

            edit_btn = QtWidgets.QPushButton(icon=QtGui.QIcon("../images/edit.png"))
            edit_btn.setIconSize(QtCore.QSize(24, 24))
            edit_btn.setStyleSheet("""
                QPushButton {
                    padding: 5px;
                    border: none;
                    border-radius: 4px;
                }
                QPushButton:hover {F
                    background-color: #f0f0f0;
                }
            """)
            edit_btn.clicked.connect(lambda _, r=row: self.show_edit_category_page(r))
            actions_layout.addWidget(edit_btn)

            view_btn = QtWidgets.QPushButton(icon=QtGui.QIcon("../images/view.png"))
            view_btn.setIconSize(QtCore.QSize(24, 24))
            view_btn.setToolTip("View Rate Blocks")
            view_btn.setStyleSheet("""
                QPushButton {
                    padding: 5px;
                    border: none;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #e0f7fa;
                }
            """)
            view_btn.clicked.connect(lambda _, cat_name=category_name: self.open_rateblock_panel(cat_name))
            actions_layout.addWidget(view_btn)

            self.categorys_table.setCellWidget(row, 3, actions_widget)

    def open_rateblock_panel(self, category_name):
        if hasattr(self, 'rateblock_panel') and self.rateblock_panel:
            self.rateblock_panel.close_panel()

        self.rateblock_panel = RateBlockPanel(category_name, parent=self)
        self.rateblock_panel.setParent(self)
        self.rateblock_panel.resize(self.width(), self.height())
        self.rateblock_panel.move(self.width(), 0)
        self.rateblock_panel.open_panel()

    def show_edit_category_page(self, row):
        # Get the category name from the ScrollableTextWidget
        cell_widget = self.categorys_table.cellWidget(row, 0)
        if cell_widget and isinstance(cell_widget, ScrollableTextWidget):
            current_name = cell_widget.text()
        else:
            current_name = ""  # Default value if widget not found

        edit_dialog = QtWidgets.QDialog(self)
        edit_dialog.setWindowTitle("Edit Category")
        edit_dialog.setFixedSize(600, 250)
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
        layout.setSpacing(10)

        # Title
        title = QtWidgets.QLabel("EDIT CATEGORY")
        title.setStyleSheet("""
            font-size: 20px;
            padding: 10px;
        """)
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)

        # Input styles
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

        # Create labeled widget helper
        def create_labeled_widget(label_text, widget):
            container = QtWidgets.QVBoxLayout()
            label = QtWidgets.QLabel(label_text)
            label.setFont(QtGui.QFont("Arial", 10))
            container.addWidget(label)
            container.addWidget(widget)
            return container

        # Form layout
        form_layout = QtWidgets.QGridLayout()
        form_layout.setHorizontalSpacing(30)
        form_layout.setVerticalSpacing(15)

        name_input = QtWidgets.QLineEdit(current_name)
        name_input.setStyleSheet(input_style)

        form_layout.addLayout(create_labeled_widget("CATEGORY NAME:", name_input), 0, 0)

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
        cancel_btn.clicked.connect(edit_dialog.reject)

        save_btn = QtWidgets.QPushButton("Save")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 8px 15px;
                border-radius: 4px;
                font-family: 'Roboto', sans-serif;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #219a52;
            }
        """)

        def save_action():
            if not name_input.text().strip():
                QMessageBox.warning(edit_dialog, "Validation Error", "Category name cannot be empty.")
                return

            # Get the category name from input
            new_category_name = name_input.text().strip()

            # Check if the name is unchanged
            if new_category_name == current_name:
                QMessageBox.information(edit_dialog, "No Changes", "The category name is unchanged.")
                edit_dialog.accept()
                return

            # Get the category ID from the table
            status_container = self.categorys_table.cellWidget(row, 2)
            if status_container:
                toggle_button = status_container.findChild(QtWidgets.QPushButton)
                if toggle_button:
                    category_id = toggle_button.property("category_id")

                    # Update the category in the database
                    category_repository = CategoryRepository()
                    category_repository.update_category(category_id, new_category_name)
                    
                    # Log the action with the actual username
                    self.IadminPageBack.log_action(f"Updated category from '{current_name}' to '{new_category_name}'")

                    # Show success message
                    QMessageBox.information(edit_dialog, "Success",
                                            f"Category '{new_category_name}' has been successfully updated.")

                    # Refresh the table with updated data
                    self.populate_table(self.IadminPageBack.fetch_categories())

            # Close the dialog
            edit_dialog.accept()

        save_btn.clicked.connect(save_action)
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(save_btn)
        layout.addWidget(button_container)

        edit_dialog.exec_()

    def deactivate_category(self, row):
        # Get the category name from the ScrollableTextWidget
        cell_widget = self.categorys_table.cellWidget(row, 0)
        if cell_widget and isinstance(cell_widget, ScrollableTextWidget):
            category_name = cell_widget.text()

            # Get the status widget to find the category_id
            status_container = self.categorys_table.cellWidget(row, 2)
            if status_container:
                toggle_button = status_container.findChild(QtWidgets.QPushButton)
                if toggle_button:
                    category_id = toggle_button.property("category_id")

                    reply = QtWidgets.QMessageBox.question(
                        self, 'Deactivate Category',
                        f"Are you sure you want to deactivate category {category_name}?",
                        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                        QtWidgets.QMessageBox.No
                    )

                    if reply == QtWidgets.QMessageBox.Yes:
                        self.IadminPageBack.toggle_category_status(category_id, 'Inactive')
                        # Refresh the table
                        self.populate_table(self.IadminPageBack.fetch_categories())

    def toggle_search_input(self, text):
        if text == "Category":
            self.search_input.hide()
            self.search_input_combo.show()
        else:
            self.search_input.show()
            self.search_input_combo.hide()

    def filter_table(self, text):
        # Filter rows based on the search text
        for row in range(self.categorys_table.rowCount()):
            cell_widget = self.categorys_table.cellWidget(row, 0)  # Get the NAME column widget
            if cell_widget and isinstance(cell_widget, ScrollableTextWidget):
                category_name = cell_widget.text().lower()
                if text.lower() in category_name:
                    self.categorys_table.setRowHidden(row, False)  # Show row if name matches
                else:
                    self.categorys_table.setRowHidden(row, True)  # Hide row if name doesn't match

    def toggle_status(self, row, label):
        table = self.categorys_table
        container = table.cellWidget(row, 2)
        if container:
            toggle_button = container.findChild(QtWidgets.QPushButton)
            if toggle_button:
                category_id = toggle_button.property("category_id")
                category_info = self.IadminPageBack.get_category_by_id(category_id)
                current_status = category_info[0][2]  # 'Active' or 'Inactive'
                next_status = 'Inactive' if current_status == 'Active' else 'Active'

                # Block toggle auto-switch
                toggle_button.blockSignals(True)

                reply = QMessageBox.question(
                    self,
                    "Confirm Status Change",
                    f"Are you sure you want to change the status to {next_status}?",
                    QMessageBox.Yes | QMessageBox.No
                )

                if reply == QMessageBox.Yes:
                    # Update DB
                    self.IadminPageBack.toggle_category_status(category_id, next_status)
                    # Update label and toggle state
                    label.setText(next_status)
                    label.setStyleSheet(
                        f"color: {'#4CAF50' if next_status == 'Active' else '#E57373'}; font-weight: bold;")
                    toggle_button.setChecked(next_status == "Active")  # Convert to boolean
                else:
                    # Keep original state
                    toggle_button.setChecked(current_status == "Active")  # Convert to boolean

                toggle_button.blockSignals(False)
                


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


from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from backend.adminBack import adminPageBack


class RateBlockPanel(QtWidgets.QWidget):
    def __init__(self, category_name, parent=None):
        super().__init__(parent)
        self.category_name = category_name
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setFixedWidth(int(parent.width() * 0.6))
        self.setStyleSheet("background-color: #ffffff; border-left: 2px solid #ccc;")

        # Get the username from the parent CategoryPage
        self.username = parent.username if hasattr(parent, 'username') else "System"
        self.admin = adminPageBack(self.username)  # Pass the username here
        self.category_id = self.get_category_id_by_name(category_name)
        self.setup_ui()

    def get_category_id_by_name(self, name):
        categories = self.admin.fetch_categories()
        for cat in categories:
            if cat[1] == name:
                return cat[0]
        return None

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)

        title = QtWidgets.QLabel(f"Rate Blocks for {self.category_name}")
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(title)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Range", "Rate", "Rate Type", "Actions"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        layout.addWidget(self.table)

        self.refresh_table()

        add_btn = QtWidgets.QPushButton("+ Add Rate Block")
        add_btn.clicked.connect(self.add_rate_block)
        layout.addWidget(add_btn)

        close_btn = QtWidgets.QPushButton("Close")
        close_btn.clicked.connect(self.close_panel)
        layout.addWidget(close_btn)

    def refresh_table(self):
        data = self.admin.fetch_rate_blocks_by_categ(self.category_id)
        self.table.setRowCount(len(data))
        for row, block in enumerate(data):
            block_id, is_minimum, min_con, max_con, rate, _ = block
            range_text = f"{min_con}+" if max_con is None else f"{min_con}-{max_con}"
            rate_type = "Fixed" if is_minimum else "Per Cubic Meter"

            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(range_text))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(rate)))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(rate_type))

            edit_btn = QtWidgets.QPushButton("Edit")
            edit_btn.clicked.connect(lambda _, b=block: self.edit_rate_block(b))
            del_btn = QtWidgets.QPushButton("Delete")
            del_btn.clicked.connect(lambda _, id=block_id: self.delete_rate_block(id))

            actions = QtWidgets.QHBoxLayout()
            actions.addWidget(edit_btn)
            actions.addWidget(del_btn)

            widget = QtWidgets.QWidget()
            widget.setLayout(actions)
            self.table.setCellWidget(row, 3, widget)

    def is_range_overlapping(self, new_min, new_max, exclude_id=None):
        for block in self.admin.fetch_rate_blocks_by_categ(self.category_id):
            block_id, _, min_c, max_c, _, _ = block
            if exclude_id and block_id == exclude_id:
                continue
            if max_c is None:
                max_c = float('inf')
            if new_max is None:
                new_max = float('inf')
            if not (new_max < min_c or new_min > max_c):
                return True
        return False

    def add_rate_block(self):
        self.show_rate_block_dialog("Add Rate Block", is_edit=False)

    def edit_rate_block(self, block):
        self.show_rate_block_dialog("Edit Rate Block", is_edit=True, block=block)

    def delete_rate_block(self, block_id):
        reply = QMessageBox.question(self, "Confirm", "Delete this rate block?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.admin.delete_rate_block(block_id)
            self.refresh_table()

    def show_rate_block_dialog(self, title, is_edit=False, block=None):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle(title)
        layout = QtWidgets.QFormLayout(dialog)

        min_input = QtWidgets.QLineEdit(str(block[2]) if is_edit else "")
        max_input = QtWidgets.QLineEdit("" if block and block[3] is None else str(block[3]) if is_edit else "")
        rate_input = QtWidgets.QLineEdit(str(block[4]) if is_edit else "")
        type_combo = QtWidgets.QComboBox()
        type_combo.addItems(["Fixed", "Per Cubic Meter"])
        if is_edit and block[1]:
            type_combo.setCurrentIndex(0 if block[1] else 1)

        layout.addRow("Min Consumption:", min_input)
        layout.addRow("Max Consumption (leave blank for +):", max_input)
        layout.addRow("Rate:", rate_input)
        layout.addRow("Rate Type:", type_combo)

        # Create custom buttons instead of using QDialogButtonBox
        button_layout = QtWidgets.QHBoxLayout()
        save_btn = QtWidgets.QPushButton("Save")
        cancel_btn = QtWidgets.QPushButton("Cancel")
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addRow(button_layout)

        def save():
            try:
                min_val = float(min_input.text())
                # Handle blank max consumption more carefully
                max_text = max_input.text().strip()
                max_val = None if max_text == "" else float(max_text)
                rate_val = float(rate_input.text())
                is_min = (type_combo.currentText() == "Fixed")
                if self.is_range_overlapping(min_val, max_val, block[0] if is_edit else None):
                    QMessageBox.warning(dialog, "Overlap", "Range overlaps with existing block.")
                    return
                if is_edit:
                    self.admin.update_rate_block(block[0], is_min, min_val, max_val, rate_val)
                    # Log the edit action
                    range_text = f"{min_val}+" if max_val is None else f"{min_val}-{max_val}"
                    self.admin.log_action(f"Updated rate block (Range: {range_text}, Rate: {rate_val}) in category '{self.category_name}'")
                else:
                    self.admin.insert_rate_block(is_min, min_val, max_val, rate_val, self.category_id)
                    # Log the add action
                    range_text = f"{min_val}+" if max_val is None else f"{min_val}-{max_val}"
                    self.admin.log_action(f"Added rate block (Range: {range_text}, Rate: {rate_val}) to category '{self.category_name}'")
                self.refresh_table()
                QMessageBox.information(dialog, "Success", "Rate block saved successfully.")
                # Don't close the dialog after saving to allow adding multiple rate blocks
                if not is_edit:
                    # Clear the form for the next entry
                    min_input.setText("")
                    max_input.setText("")
                    rate_input.setText("")
                    type_combo.setCurrentIndex(1)  # Default to "Per Cubic Meter"
                    # Explicitly prevent the dialog from closing
                    return False
                else:
                    dialog.accept()  # Close only when editing
                    return True
            except ValueError:
                QMessageBox.warning(dialog, "Invalid", "Please enter valid numbers.")
                return False

        # Custom handler for save button to prevent dialog from closing
        def on_save_clicked():
            result = save()
            # If we're adding a new rate block and save was successful, don't close the dialog
            # The dialog will only close if save() returns True (which happens in edit mode)
            if result:
                dialog.accept()

        save_btn.clicked.connect(on_save_clicked)
        cancel_btn.clicked.connect(dialog.reject)

        # Set dialog to not close automatically when a button is clicked
        dialog.setModal(True)
        dialog.exec_()

    def open_panel(self):
        anim = QtCore.QPropertyAnimation(self, b"pos")
        anim.setDuration(300)
        anim.setStartValue(self.pos())
        anim.setEndValue(QtCore.QPoint(self.parent().width() - self.width(), 0))
        anim.start()
        self.anim = anim
        self.show()

    def close_panel(self):
        anim = QtCore.QPropertyAnimation(self, b"pos")
        anim.setDuration(300)
        anim.setStartValue(self.pos())
        anim.setEndValue(QtCore.QPoint(self.parent().width(), 0))
        anim.finished.connect(self.hide)
        anim.start()
        self.anim = anim


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CategoryPage()
    window.show()
    sys.exit(app.exec_())
