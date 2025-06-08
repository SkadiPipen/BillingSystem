import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import sys
import os

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5 import QtCore, QtGui, QtWidgets
from pages.employee_customers_page import EmployeeCustomersPage
from pages.billing_page import EmployeeBillingPage
from pages.category_page import CategoryPage
from pages.address_page import AddressPage
from pages.transactions_page import TransactionsPage
from pages.meters_page import MetersPage

class WorkersPanel(QtWidgets.QMainWindow):
    def __init__(self, username=None):
        super().__init__()
        self.username = username if username else "System"
        self.setWindowTitle("SOWBASCO - Workers Panel")
        self.setMinimumSize(1200, 800)
        self.showMaximized()
        self.setWindowIcon(QtGui.QIcon("../images/logosowbasco.png"))
        
        # Main widget and layout setup
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QtWidgets.QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Create sidebar
        self.setup_sidebar()
        
        # Create stacked widget and header
        self.setup_main_content()
        
        # Initialize pages dictionary to track loaded pages
        self.pages = {}
        self.page_indices = {
            "Customers": 0,
            "Categories": 1,
            "Address": 2,
            "Meters": 3,  # Added Meters page index
            "Billing": 4,
            "Transactions": 5
        }
        
        # Create placeholder pages
        self.create_placeholders()
        
        # Load only the customers page initially
        self.load_page("Customers")
        
        # Set initial page
        self.stacked_widget.setCurrentIndex(0)

    def setup_main_content(self):
        # Create stacked widget for different pages
        self.stacked_widget = QtWidgets.QStackedWidget()
        
        # Create green header bar
        header_bar = QtWidgets.QWidget()
        header_bar.setStyleSheet("background-color: rgb(201, 235, 203);")
        header_bar.setFixedHeight(70)
        
        header_layout = QtWidgets.QHBoxLayout(header_bar)
        header_layout.setContentsMargins(20, 0, 20, 0)
        
        # Add company name on the left
        company_name = QtWidgets.QLabel("SouthWestern Barangays Water Services Cooperative II")
        company_name.setStyleSheet("""
            color: rgb(60, 60, 60);
            font-size: 16px;
            font-family: 'Poppins', sans-serif;
            font-weight: 600;
        """)
        header_layout.addWidget(company_name)
        
        # Add username on the right
        user_label = QtWidgets.QLabel(f"User: {self.username}")
        user_label.setStyleSheet("""
            color: rgb(60, 60, 60);
            font-size: 14px;
            font-family: 'Poppins', sans-serif;
            font-weight: 500;
        """)
        user_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        header_layout.addWidget(user_label)
        
        # Create container for stacked widget and header
        container = QtWidgets.QWidget()
        container_layout = QtWidgets.QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        
        container_layout.addWidget(header_bar)
        container_layout.addWidget(self.stacked_widget)
        
        self.main_layout.addWidget(container)

    def create_placeholders(self):
        """Create placeholders for all pages to prevent UI glitches"""
        for page_name in self.page_indices:
            # Create a placeholder widget with white background
            placeholder = QtWidgets.QWidget()
            placeholder.setStyleSheet("background-color: white;")
            
            # Add placeholder to stacked widget
            self.stacked_widget.addWidget(placeholder)

    def load_page(self, page_name):
        # If page is already loaded, just return its index
        if page_name in self.pages:
            return self.page_indices[page_name]
        
        # Get the placeholder at the correct index
        index = self.page_indices[page_name]
        placeholder = self.stacked_widget.widget(index)
            
        # Use a QTimer to create a small delay before loading the actual page
        # This allows the UI to update and show the placeholder first
        QtCore.QTimer.singleShot(10, lambda: self._delayed_load_page(page_name, index, placeholder))
            
        return index
        
    def _delayed_load_page(self, page_name, index, placeholder):
        """Actually load the page after a small delay"""
        # Create the page
        page = None
        if page_name == "Customers":
            page = EmployeeCustomersPage(self)
        elif page_name == "Categories":
            page = CategoryPage(self)
        elif page_name == "Address":
            page = AddressPage(self)
        elif page_name == "Meters":
            page = MetersPage(self)    
        elif page_name == "Billing":
            page = EmployeeBillingPage(self)
        elif page_name == "Transactions":
            page = TransactionsPage(self)
        
        if page:
            # Replace the placeholder with the actual page
            self.stacked_widget.removeWidget(placeholder)
            self.stacked_widget.insertWidget(index, page)
            self.stacked_widget.setCurrentIndex(index)
            
            # Save reference to page
            self.pages[page_name] = page
            
            # Process events to ensure UI updates
            QtWidgets.QApplication.processEvents()

    def setup_sidebar(self):
        sidebar = QtWidgets.QFrame()
        sidebar.setStyleSheet("""
            QFrame {
                background-color: rgb(201, 235, 203);
                border: none;
            }
            QPushButton {
                text-align: left;
                padding: 15px 20px;
                border: none;
                border-radius: 0;
                font-size: 16px;
                font-family: 'Roboto', sans-serif;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #E8F8E4;
            }
            QPushButton:checked {
                background-color: #E8F8E4;
            }
        """)
        sidebar.setFixedWidth(250)
        
        # Create sidebar layout
        sidebar_layout = QtWidgets.QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        
        # Logo and text container
        header_layout = QtWidgets.QHBoxLayout()
        
        # Logo image
        logo_image = QtWidgets.QLabel()
        logo_pixmap = QtGui.QPixmap("../images/logosowbasco.png")
        scaled_pixmap = logo_pixmap.scaled(50, 50, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        logo_image.setPixmap(scaled_pixmap)
        logo_image.setStyleSheet("padding: 10px;")
        header_layout.addWidget(logo_image)
        
        # Title text
        logo_label = QtWidgets.QLabel("SOWBASCO")
        logo_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            padding: 10px;
            font-family: 'Montserrat', sans-serif;
        """)
        header_layout.addWidget(logo_label)
        
        sidebar_layout.addLayout(header_layout)
        
        # Navigation buttons
        self.nav_buttons = []
        for text, icon_path in [
            ("Customers", "../images/clients.png"),
            ("Categories", "../images/category.png"),
            ("Address", "../images/address.png"),
            ("Meters", "../images/meters.png"),  # Added Meters button
            ("Billing", "../images/bill.png"),
            ("Transactions", "../images/transaction.png")
        ]:
            btn = QtWidgets.QPushButton(text)
            btn.setIcon(QtGui.QIcon(icon_path))
            btn.setIconSize(QtCore.QSize(50, 50))
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, x=text: self.change_page(x))
            sidebar_layout.addWidget(btn)
            self.nav_buttons.append(btn)
        
        # Add stretch to push logout to bottom
        sidebar_layout.addStretch()
        
        # Logout button
        logout_btn = QtWidgets.QPushButton("Logout")
        logout_btn.setIcon(QtGui.QIcon("../images/logout.png"))
        logout_btn.setIconSize(QtCore.QSize(50, 50))
        logout_btn.clicked.connect(self.logout)
        sidebar_layout.addWidget(logout_btn)
        
        self.main_layout.addWidget(sidebar)
        self.nav_buttons[0].setChecked(True)

    def logout(self):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Logout")
        dialog.setFixedWidth(400)
        dialog.setWindowFlags(dialog.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        dialog.setStyleSheet("""
            QDialog {
                background-color: #C9EBCB;
                border-radius: 10px;
            }
            QLabel {
                font-family: 'Roboto', sans-serif;
                color: #333;
            }
            QPushButton {
                padding: 8px 20px;
                font-family: 'Roboto', sans-serif;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton#confirm {
                background-color: rgb(229, 115, 115);
                color: white;
                border: none;
            }
            QPushButton#confirm:hover {
                background-color: rgb(200, 100, 100);
            }
            QPushButton#cancel {
                background-color: #6c757d;
                border: 1px solid #ddd;
                color: white;
            }
            QPushButton#cancel:hover {
                background-color: #5a6268;
            }
        """)

        # Dialog layout
        layout = QtWidgets.QVBoxLayout(dialog)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Message
        message = QtWidgets.QLabel("Confirm Logout?")
        message.setStyleSheet("font-size: 16px; font-weight: bold; text-align: center;")
        message.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(message)

        # Buttons layout
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSpacing(10)

        # Cancel button
        cancel_btn = QtWidgets.QPushButton("Cancel")
        cancel_btn.setObjectName("cancel")
        cancel_btn.clicked.connect(dialog.reject)
        button_layout.addWidget(cancel_btn)

        # Confirm button
        confirm_btn = QtWidgets.QPushButton("Confirm")
        confirm_btn.setObjectName("confirm")
        confirm_btn.clicked.connect(dialog.accept)
        button_layout.addWidget(confirm_btn)

        layout.addLayout(button_layout)

        # Show dialog and handle result
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            from frontend.login import LoginWindow
            self.login = LoginWindow()
            self.login.show()
            self.close()

    def change_page(self, page_name):
        # Uncheck all buttons except the clicked one
        for btn in self.nav_buttons:
            if page_name not in btn.text():
                btn.setChecked(False)
        
        # Get the page index
        page_index = self.page_indices[page_name]
        
        # First switch to page index immediately to show placeholder
        self.stacked_widget.setCurrentIndex(page_index)
        
        # Then load the actual page content if needed (in background)
        if page_name not in self.pages:
            QtCore.QTimer.singleShot(10, lambda: self.load_page(page_name))

# Add this at the very end of the file:
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = WorkersPanel()
    window.show()
    sys.exit(app.exec_())