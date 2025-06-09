import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice
from backend.adminBack import adminPageBack

class AdminDashboardPage(QtWidgets.QWidget):
    def __init__(self, username=None):
        super().__init__()
        self.parent = None
        self.username = username if username else "System"
        self.backend = adminPageBack(self.username)
        self.sample_data = [
            ("TR001", "Alice Brown", "₱50", "John Doe", "2023-10-15", "COMPLETED"),
            ("TR002", "Charlie Davis", "₱50", "John Doe", "2023-10-15", "PENDING"),
            ("TR003", "Eve Franklin", "₱50", "John Doe", "2023-10-15", "FAILED"),
            ("TR004", "George Harris", "₱50", "John Doe", "2023-10-15", "COMPLETED"),
        ]
        self.setup_ui()

    def get_client_stats(self):
        clients = self.backend.fetch_clients()
        total_clients = len(clients)
        active_clients = sum(1 for client in clients if client[10] == "Active")
        inactive_clients = sum(1 for client in clients if client[10] == "Inactive")
        return total_clients, active_clients, inactive_clients

    def refresh_dashboard(self):
        def clear_layout(layout):
            while layout.count():
                item = layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
                elif item.layout():
                    clear_layout(item.layout())

        clear_layout(self.content_layout)
        self.populate_dashboard_content()

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Top bar with refresh button
        top_bar = QtWidgets.QHBoxLayout()
        top_bar.addStretch()

        refresh_btn = QtWidgets.QPushButton("🔄 Refresh")
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #A5D6A7;
                color: white;
                font-weight: bold;
                padding: 8px 20px;
                border-radius: 6px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #81C784;
            }
        """)
        refresh_btn.clicked.connect(self.refresh_dashboard)
        top_bar.addWidget(refresh_btn)
        layout.addLayout(top_bar)

        # Dashboard content section
        content_widget = QtWidgets.QWidget()
        self.content_layout = QtWidgets.QVBoxLayout(content_widget)
        self.content_layout.setSpacing(40)
        self.content_layout.setContentsMargins(0, 0, 0, 0)

        self.populate_dashboard_content()
        layout.addWidget(content_widget)

    def populate_dashboard_content(self):
        stats_grid = QtWidgets.QGridLayout()
        stats_grid.setSpacing(20)

        total_clients, active_clients, inactive_clients = self.get_client_stats()

        customers_card = self.create_stat_card("Total Customers", str(total_clients), "../images/clients.png")
        stats_grid.addWidget(customers_card, 0, 1)

        active_card = self.create_stat_card("Active", str(active_clients), "../images/active.png")
        stats_grid.addWidget(active_card, 0, 2)

        inactive_card = self.create_stat_card("Inactive", str(inactive_clients), "../images/not-active.png")
        stats_grid.addWidget(inactive_card, 0, 3)

        total_billed = sum(float(trans_amount.replace('₱', ''))
                          for _, _, trans_amount, _, _, _ in self.sample_data)
        billed_card = self.create_stat_card("Total Billed Amount", f"₱{total_billed:,.2f}", "../images/bill.png")
        stats_grid.addWidget(billed_card, 0, 4)

        self.content_layout.addLayout(stats_grid)

        charts_container = QtWidgets.QWidget()
        charts_layout = QtWidgets.QHBoxLayout(charts_container)
        charts_layout.setSpacing(20)

        daily_chart = self.create_revenue_chart("Daily Revenue")
        monthly_chart = self.create_revenue_chart("Monthly Revenue")

        charts_layout.addWidget(daily_chart, 1)
        charts_layout.addWidget(monthly_chart, 1)

        self.content_layout.addWidget(charts_container)

    def create_stat_card(self, title, value, icon):
        card = QtWidgets.QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #C9EBCB;
                border-radius: 10px;
                padding: 15px;
            }
        """)

        layout = QtWidgets.QVBoxLayout(card)
        layout.setSpacing(10)
        layout.setAlignment(QtCore.Qt.AlignCenter)

        icon_container = QtWidgets.QWidget()
        icon_layout = QtWidgets.QVBoxLayout(icon_container)
        icon_layout.setAlignment(QtCore.Qt.AlignCenter)

        icon_label = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap(icon)
        scaled_pixmap = pixmap.scaled(40, 40, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        icon_label.setPixmap(scaled_pixmap)
        icon_layout.addWidget(icon_label)
        layout.addWidget(icon_container)

        text_label = QtWidgets.QLabel(title)
        text_label.setStyleSheet("""
            font-family: 'Montserrat', sans-serif;
            font-weight: bold;
            font-size: 14px;
            color: #666;
            text-align: center;
        """)
        text_label.setAlignment(QtCore.Qt.AlignCenter)
        text_label.setWordWrap(True)
        layout.addWidget(text_label)

        value_label = QtWidgets.QLabel(value)
        value_label.setStyleSheet("""
            font-family: 'Roboto', sans-serif;
            font-size: 24px;
            color: #333;
        """)
        value_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(value_label)

        card.setMinimumSize(200, 150)
        return card

    def create_revenue_chart(self, title):
        container = QtWidgets.QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: #C9EBCB;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        layout = QtWidgets.QVBoxLayout(container)

        title_label = QtWidgets.QLabel(title)
        title_label.setStyleSheet("""
            font-family: 'Montserrat', sans-serif;
            font-size: 18px;
            font-weight: bold;
            color: #333;
            padding-bottom: 10px;
        """)
        layout.addWidget(title_label)

        series = QPieSeries()

        if "Daily" in title:
            completed = sum(float(amount.replace('₱', ''))
                          for _, _, amount, _, date, status in self.sample_data
                          if status == "COMPLETED" and date == "2023-10-15")
            pending = sum(float(amount.replace('₱', ''))
                        for _, _, amount, _, date, status in self.sample_data
                        if status == "PENDING" and date == "2023-10-15")
        else:
            completed = sum(float(amount.replace('₱', ''))
                          for _, _, amount, _, _, status in self.sample_data
                          if status == "COMPLETED")
            pending = sum(float(amount.replace('₱', ''))
                        for _, _, amount, _, _, status in self.sample_data
                        if status == "PENDING")

        completed_slice = QPieSlice("Completed", completed)
        pending_slice = QPieSlice("Pending", pending)

        series.append(completed_slice)
        series.append(pending_slice)

        completed_slice.setBrush(QtGui.QColor("#4CAF50"))
        pending_slice.setBrush(QtGui.QColor("#FFA726"))

        total = completed + pending
        if total > 0:
            completed_slice.setLabel(f"₱{completed:,.0f}\n({completed/total*100:.1f}%)")
            pending_slice.setLabel(f"₱{pending:,.0f}\n({pending/total*100:.1f}%)")
            completed_slice.setLabelVisible(True)
            pending_slice.setLabelVisible(True)
            completed_slice.setLabelArmLengthFactor(0.35)
            pending_slice.setLabelArmLengthFactor(0.35)
        else:
            completed_slice.setLabel("No\nRevenue")
            pending_slice.setLabel("")

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("")
        chart.legend().hide()
        chart.setMargins(QtCore.QMargins(10, 10, 10, 10))
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.layout().setContentsMargins(0, 0, 0, 0)
        chart.setBackgroundVisible(False)
        chart.setMinimumSize(QtCore.QSizeF(250, 200))

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QtGui.QPainter.Antialiasing)
        chart_view.setMinimumSize(QtCore.QSize(250, 200))

        layout.addWidget(chart_view)
        return container

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = AdminDashboardPage()
    window.show()
    sys.exit(app.exec_())
