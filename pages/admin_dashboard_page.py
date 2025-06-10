import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

import sys
import os
from datetime import datetime, date

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

        # Fetch live transactions
        self.transactions = self.backend.fetch_transaction()  # Ensure this returns a list of tuples

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

        # === Re-fetch live data ===
        self.transactions = self.backend.fetch_transaction()  # Refresh transactions
        # ==========================

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

        # Calculate dynamic total billed amount
        total_billed = 0.0
        for trans in self.transactions:
            try:
                status = trans[8].upper()  # Assuming status is at index 8
                billing_total = float(trans[6])  # billing_total at index 6
                if status in ("PAID", "PENDING"):
                    total_billed += billing_total
            except (IndexError, ValueError, TypeError):
                continue

        billed_card = self.create_stat_card(
            "Total Billed Amount",
            f"₱{total_billed:,.2f}",
            "../images/bill.png"
        )
        stats_grid.addWidget(billed_card, 0, 4)

        self.content_layout.addLayout(stats_grid)

        charts_container = QtWidgets.QWidget()
        charts_layout = QtWidgets.QHBoxLayout(charts_container)
        charts_layout.setSpacing(20)

        daily_chart = self.create_revenue_chart("Daily Revenue", self.transactions)
        monthly_chart = self.create_revenue_chart("Monthly Revenue", self.transactions)

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

    def create_revenue_chart(self, title, transactions):
        container = QtWidgets.QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: #C9EBCB;
                border-radius: 10px;
                padding: 5px;
            }
        """)
        layout = QtWidgets.QVBoxLayout(container)
        title_label = QtWidgets.QLabel(title)
        title_label.setStyleSheet("""
            font-family: 'Montserrat', sans-serif;
            font-size: 18px;
            font-weight: bold;
            color: #333;
            padding-bottom: 2px;
        """)
        layout.addWidget(title_label)

        today = QtCore.QDate.currentDate().toString("yyyy-MM-dd")
        completed_total = 0.0
        pending_total = 0.0

        for trans in transactions:
            try:
                status = trans[8].upper()
                raw_date = trans[1]
                try:
                    if isinstance(raw_date, QtCore.QDate):
                        payment_date = raw_date.toString("yyyy-MM-dd")
                    elif isinstance(raw_date, datetime):
                        payment_date = raw_date.strftime("%Y-%m-%d")
                    elif isinstance(raw_date, date):  # Handle date-only objects
                        payment_date = raw_date.strftime("%Y-%m-%d")
                    elif isinstance(raw_date, str):
                        try:
                            cleaned = raw_date.strip().split()[0]
                            parsed = datetime.strptime(cleaned, "%Y-%m-%d")
                            payment_date = parsed.strftime("%Y-%m-%d")
                        except ValueError as ve:
                            payment_date = ""
                    else:
                        payment_date = ""
                except Exception as e:
                    payment_date = ""
                amount = float(trans[6])  # billing_total at index 6
            except Exception:
                continue

            is_today = (payment_date == today)

            if "Daily" in title:
                if status == "PAID" and is_today:
                    completed_total += amount
                else:
                    print(f"Ignored transaction {trans[0]} because status={status} or not today.")
            else:
                if status == "PAID":
                    completed_total += amount
                elif status == "PENDING":
                    pending_total += amount

        # Check if it's Daily chart and has no data
        if "Daily" in title and completed_total == 0:
            no_data_label = QtWidgets.QLabel("No data available for today.")
            no_data_label.setAlignment(QtCore.Qt.AlignCenter)
            no_data_label.setStyleSheet("font-size: 14px; color: #999;")
            layout.addWidget(no_data_label)
        else:
            series = QPieSeries()

            if "Daily" in title:
                # For Daily chart, only show "PAID" transactions
                series.append("PAID", completed_total)

                # Set color for "PAID"
                colors = [QtGui.QColor("#4CAF50")]  # Green for PAID
                for slice_, color in zip(series.slices(), colors):
                    slice_.setBrush(color)
                    slice_.setLabelFont(
                        QtGui.QFont("Arial", 9, QtGui.QFont.Bold))
                    slice_.setLabel(f"₱{slice_.value():,.0f}")  # Show only the amount
                    slice_.setLabelVisible(True)
                    slice_.setLabelArmLengthFactor(0.15)
            else:
                # For Monthly chart, show both "PAID" and "PENDING"
                series.append("PAID", completed_total)
                series.append("PENDING", pending_total)

                colors = [QtGui.QColor("#4CAF50"), QtGui.QColor("#FFA726")]
                slices = series.slices()
                slices = series.slices()
                for i, slice_ in enumerate(slices):
                    slice_.setBrush(colors[i])
                    total = completed_total + pending_total
                    if total > 0:
                        percent = (slice_.value() / total) * 100
                        # Set label format
                        slice_.setLabel(f"₱{slice_.value():,.0f}\n({percent:.1f}%)")
                        slice_.setLabelVisible(True)
                        slice_.setLabelFont(
                            QtGui.QFont("Arial", 9, QtGui.QFont.Bold))  # Make font bold for better visibility
                        slice_.setLabelArmLengthFactor(0.15)  # Longer arm for better label placement
                        slice_.setExploded(i == 1)  # Optional: Explode PENDING slice slightly

            chart = QChart()
            chart.addSeries(series)
            chart.setTitle("")
            chart.legend().hide()
            chart.setMargins(QtCore.QMargins(10, 10, 10, 10))
            chart.setBackgroundVisible(False)
            chart.setMinimumSize(QtCore.QSizeF(200, 160))
            chart.setAnimationOptions(QChart.SeriesAnimations)

            chart_view = QChartView(chart)
            chart_view.setRenderHint(QtGui.QPainter.Antialiasing)
            chart_view.setMinimumSize(QtCore.QSize(200, 160))

            layout.addWidget(chart_view)

            # === Add Custom Legend Below Chart ===
            legend_layout = QtWidgets.QHBoxLayout()
            paid_legend = QtWidgets.QLabel("🟩 PAID")
            paid_legend.setStyleSheet("font-size: 12px; color: black;")
            legend_layout.addWidget(paid_legend)

            # For Daily chart, remove the "PENDING" legend
            if "Daily" not in title:
                pending_legend = QtWidgets.QLabel("🟨 PENDING")
                pending_legend.setStyleSheet("font-size: 12px; color: black;")
                legend_layout.addWidget(pending_legend)

            legend_layout.addStretch()
            layout.addLayout(legend_layout)
            # =====================================

        return container


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = AdminDashboardPage()
    window.show()
    sys.exit(app.exec_())