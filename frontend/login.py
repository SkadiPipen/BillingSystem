from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, \
    QLineEdit, QFrame, QMenuBar, QDialog, QMessageBox
from PyQt5 import QtCore, QtGui
import sys
import os
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", message=".*sipPyTypeDict.*")
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5 import QtCore, QtGui, QtWidgets

# Create QApplication first
app = QApplication(sys.argv)

# Then import other modules
import os
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", message=".*sipPyTypeDict.*")
from backend.loginPagesBack import LoginPagesBack

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_loginpage(object):
    def setupUi(self, loginpage):
        loginpage.setObjectName("loginpage")
        loginpage.resize(1207, 797)
        loginpage.setStyleSheet("background-color: #D9D9D9;")

        # Central Widget
        self.centralwidget = QtWidgets.QWidget(loginpage)
        self.centralwidget.setObjectName("centralwidget")

        # Main Vertical Layout
        self.main_vertical_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.main_vertical_layout.setContentsMargins(0, 0, 0, 0)

        # Add top spacer
        self.main_vertical_layout.addStretch(1)

        # Horizontal Layout for frames
        self.horizontal_layout = QtWidgets.QHBoxLayout()
        self.horizontal_layout.setContentsMargins(130, 0, 130, 0)
        self.horizontal_layout.setSpacing(0)  # No gap between frames

        # Add left spacer
        self.horizontal_layout.addStretch(1)

        # Container Frame for both panels
        self.container_frame = QtWidgets.QFrame()
        self.container_frame.setObjectName("container_frame")
        self.container_layout = QtWidgets.QHBoxLayout(self.container_frame)
        self.container_layout.setContentsMargins(0, 0, 0, 0)
        self.container_layout.setSpacing(0)

        # Login Frame
        self.frame = QtWidgets.QFrame()
        self.frame.setMinimumSize(400, 500)
        self.frame.setStyleSheet("background-color: rgb(201, 235, 203);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        # Login Frame Layout
        self.login_layout = QtWidgets.QVBoxLayout(self.frame)
        self.login_layout.setContentsMargins(30, 60, 30, 60)

        # Content Widget to control spacing
        self.content_widget = QtWidgets.QWidget()
        self.content_layout = QtWidgets.QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(10)

        # Title (SOWBASCO)
        self.label1 = QtWidgets.QLabel()
        # Fix the text-shadow in label1 stylesheet
        self.label1.setStyleSheet("""
            font-size: 45px;
            font-weight: bold;
            font-family: 'Montserrat', sans-serif;
            color: #333333;
        """)
        self.label1.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(
            blurRadius=4,
            color=QtGui.QColor(0, 0, 0, 127),
            offset=QtCore.QPointF(2, 2)
        ))
        self.label1.setAlignment(QtCore.Qt.AlignCenter)
        self.content_layout.addWidget(self.label1)

        # Login text
        self.label2 = QtWidgets.QLabel()
        self.label2.setStyleSheet("font-family: 'Poppins', sans-serif;\n"
                                  "font-size: 25px;\n"
                                  "font-weight: bold;\n")
        self.content_layout.addWidget(self.label2)

        # Sign in text
        self.label3 = QtWidgets.QLabel()
        self.label3.setStyleSheet("font-family: 'Roboto', sans-serif;\n"
                                  "font-size: 15px;\n"
                                  "font-style: regular;\n")
        self.content_layout.addWidget(self.label3)

        self.content_layout.addSpacing(20)

        # Username label
        self.label3_2 = QtWidgets.QLabel()
        self.label3_2.setStyleSheet("font-family: 'Roboto', sans-serif;\n"
                                    "font-size: 13px;\n"
                                    "font-style: regular;\n")
        self.content_layout.addWidget(self.label3_2)

        # Username input
        self.username = QtWidgets.QLineEdit()
        self.username.setStyleSheet("background-color: rgb(248, 248, 248);\n"
                                    "font-family: 'Roboto', sans-serif;\n"
                                    "padding: 5px;")
        self.content_layout.addWidget(self.username)

        # Password label
        self.label3_3 = QtWidgets.QLabel()
        self.label3_3.setStyleSheet("font-family: 'Roboto', sans-serif;\n"
                                    "font-size: 13px;\n"
                                    "font-style: regular;\n")
        self.content_layout.addWidget(self.label3_3)

        # Password input
        self.password = QtWidgets.QLineEdit()
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setStyleSheet("background-color: rgb(248, 248, 248);\n"
                                    "font-family: 'Roboto', sans-serif;\n"
                                    "padding: 5px;")
        self.content_layout.addWidget(self.password)

        self.content_layout.addSpacing(20)

        # Login button container
        self.button_container = QtWidgets.QHBoxLayout()
        self.button_container.addStretch(1)

        # Login button
        self.pushButton_2 = QtWidgets.QPushButton()
        self.pushButton_2.setMinimumSize(93, 28)
        self.pushButton_2.setStyleSheet("background-color: rgb(229, 115, 115);\n"
                                        "font-family: 'Poppins', sans-serif;\n"
                                        "font-weight: 500;\n"
                                        "padding: 5px 15px;")
        self.button_container.addWidget(self.pushButton_2)
        self.button_container.addStretch(1)
        self.content_layout.addLayout(self.button_container)

        # Forgot Password button
        self.forgot_password_btn = QtWidgets.QPushButton("Forgot Password?")
        self.forgot_password_btn.setStyleSheet("""
            QPushButton {
                border: none;
                font-family: 'Roboto', sans-serif;
                font-size:15px;
                text-align: right;
                padding: 5px 0px;
            }
            QPushButton:hover {
                color: rgb(200, 100, 100);
            }
        """)
        self.forgot_password_btn.clicked.connect(self.show_password_reset_dialog)
        self.content_layout.addWidget(self.forgot_password_btn, alignment=QtCore.Qt.AlignRight)

        # Add content widget to login layout
        self.login_layout.addWidget(self.content_widget)

        # Add content widget to login layout
        self.login_layout.addWidget(self.content_widget)

        # Image Frame
        self.frame_2 = QtWidgets.QFrame()
        self.frame_2.setMinimumSize(400, 500)
        self.frame_2.setStyleSheet("background-color: rgb(248, 248, 248);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")

        # Image Frame Layout
        self.image_layout = QtWidgets.QVBoxLayout(self.frame_2)

        # Image Label
        self.label = QtWidgets.QLabel()
        self.label.setPixmap(QtGui.QPixmap("../images/logosowbasco.png"))
        self.label.setScaledContents(True)
        self.label.setMinimumSize(251, 221)
        self.label.setMaximumSize(400, 350)
        self.image_layout.addWidget(self.label, 0, QtCore.Qt.AlignCenter)

        # Add frames to container
        self.container_layout.addWidget(self.frame)
        self.container_layout.addWidget(self.frame_2)

        # Add container to horizontal layout
        self.horizontal_layout.addWidget(self.container_frame)

        # Add right spacer
        self.horizontal_layout.addStretch(1)

        # Add horizontal layout to main vertical layout
        self.main_vertical_layout.addLayout(self.horizontal_layout)

        # Add bottom spacer
        self.main_vertical_layout.addStretch(1)

        loginpage.setCentralWidget(self.centralwidget)

        # Menu Bar
        self.menubar = QtWidgets.QMenuBar(loginpage)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1207, 26))
        self.menubar.setObjectName("menubar")
        loginpage.setMenuBar(self.menubar)

        self.retranslateUi(loginpage)
        QtCore.QMetaObject.connectSlotsByName(loginpage)

    def show_password_reset_dialog(self):
        dialog = PasswordResetDialog(self.centralwidget)
        result = dialog.exec_()
        if result == QtWidgets.QDialog.Accepted:
            QtWidgets.QMessageBox.information(self.centralwidget, "Success", "Password has been reset successfully!")

    def retranslateUi(self, loginpage):
        _translate = QtCore.QCoreApplication.translate
        loginpage.setWindowTitle(_translate("loginpage", "SOWBASCO - Login Page"))
        self.label1.setText(_translate("loginpage", "SOWBASCO"))
        self.label2.setText(_translate("loginpage", "Login"))
        self.label3.setText(_translate("loginpage", "Sign in to continue"))
        self.label3_2.setText(_translate("loginpage", "Username"))
        self.label3_3.setText(_translate("loginpage", "Password"))
        self.pushButton_2.setText(_translate("loginpage", "Login"))


import random
import smtplib
from email.mime.text import MIMEText

class PasswordResetDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Forgot Password")
        self.setFixedSize(400, 320)
        self.setStyleSheet("background-color: #F5F5F5;")
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.generated_code = None

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Gmail input
        self.email_label = QtWidgets.QLabel("Enter your registered Gmail:")
        self.email_input = QtWidgets.QLineEdit()
        self.email_input.setStyleSheet("background-color: #D9D9D9;")
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)

        # Send code
        self.send_code_btn = QtWidgets.QPushButton("Send Verification Code")
        self.send_code_btn.setStyleSheet("background-color: rgb(229, 115, 115);")
        self.send_code_btn.clicked.connect(self.send_code)
        layout.addWidget(self.send_code_btn)

        # Verification code input
        self.code_label = QtWidgets.QLabel("Enter 6-digit code:")
        self.code_input = QtWidgets.QLineEdit()
        self.code_input.setStyleSheet("background-color: #D9D9D9;")
        layout.addWidget(self.code_label)
        layout.addWidget(self.code_input)

        # New password inputs
        self.new_pass_label = QtWidgets.QLabel("New Password:")
        self.new_password = QtWidgets.QLineEdit()
        self.new_password.setStyleSheet("background-color: #D9D9D9;")
        self.new_password.setEchoMode(QtWidgets.QLineEdit.Password)
        layout.addWidget(self.new_pass_label)
        layout.addWidget(self.new_password)

        self.confirm_pass_label = QtWidgets.QLabel("Confirm New Password:")
        self.confirm_password = QtWidgets.QLineEdit()
        self.confirm_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirm_password.setStyleSheet("background-color: #D9D9D9;")
        layout.addWidget(self.confirm_pass_label)
        layout.addWidget(self.confirm_password)

        # Buttons
        self.reset_btn = QtWidgets.QPushButton("Reset Password")
        self.reset_btn.clicked.connect(self.reset_password)
        self.reset_btn.setStyleSheet("""
            QPushButton {
                background-color: green;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 5px;
                font-family: 'Poppins', sans-serif;
            }
            QPushButton:hover {
                background-color: rgb(201, 235, 203);
            }
        """)

        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #888888;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 5px;
                font-family: 'Poppins', sans-serif;
            }
            QPushButton:hover {
                background-color: #D9D9D9;
            }
        """)

        self.cancel_btn.clicked.connect(self.reject)

        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.reset_btn)
        layout.addLayout(btn_layout)

    def send_code(self):
        email = self.email_input.text().strip()
        if not email:
            QMessageBox.warning(self, "Input Error", "Please enter your Gmail.")
            return

        from backend.loginPagesBack import LoginPagesBack
        backend = LoginPagesBack()

        # Check if Gmail exists
        if not backend.gmail_exists(email):
            QMessageBox.warning(self, "Not Found", "This Gmail is not registered.")
            return

        self.generated_code = str(random.randint(100000, 999999))
        try:
            self.send_email_code(email, self.generated_code)
            QMessageBox.information(self, "Code Sent", f"A code has been sent to {email}.")
        except Exception as e:
            QMessageBox.critical(self, "Email Error", f"Failed to send code: {e}")

    def send_email_code(self, to_email, code):
        msg = MIMEText(f"Your SOWBASCO password reset code is: {code}")
        msg['Subject'] = "SOWBASCO Password Reset"
        msg['From'] = "jpaulnoquiana2@gmail.com"
        msg['To'] = to_email

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login("jpaulnoquiana2@gmail.com", "weyu rlzf rhny vuoq")
        server.send_message(msg)
        server.quit()

    def reset_password(self):
        if self.code_input.text().strip() != self.generated_code:
            QMessageBox.warning(self, "Invalid Code", "The verification code is incorrect.")
            return

        new_pass = self.new_password.text().strip()
        confirm_pass = self.confirm_password.text().strip()
        if not new_pass:
            QMessageBox.warning(self, "Error", "New password cannot be empty.")
            return
        if new_pass != confirm_pass:
            QMessageBox.warning(self, "Error", "Passwords do not match.")
            return

        from backend.loginPagesBack import LoginPagesBack
        backend = LoginPagesBack()
        success = backend.update_password_by_gmail(self.email_input.text().strip(), new_pass)
        if success:
            QMessageBox.information(self, "Success", "Password has been reset.")
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "Failed to update password.")



class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SOWBASCO - Login Page")
        self.ui = Ui_loginpage()
        self.ui.setupUi(self)
        self.ui.pushButton_2.clicked.connect(self.login)
        self.setMinimumSize(1200, 800)
        self.showMaximized()
        self.setWindowIcon(QtGui.QIcon("../images/logosowbasco.png"))

    def login(self):
        login_back = LoginPagesBack()
        username = self.ui.username.text()
        type = login_back.checkUserType(username, self.ui.password.text())
        if type == 'Admin':
            from adminPanel import AdminPanel
            self.admin = AdminPanel(username)
            self.admin.show()
            self.close()
        elif type == 'Employee':
            from workersPanel import WorkersPanel
            self.worker = WorkersPanel(username)
            self.worker.show()
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password")


if __name__ == "__main__":
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())