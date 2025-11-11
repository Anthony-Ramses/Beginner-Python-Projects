from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QAbstractItemView
from storage import Storage
from models import User

class EmployeeUI(QMainWindow):
    def __init__(self, storage: Storage, user: User):
        super().__init__()
        self.storage = storage
        self.user = user
        self.setWindowTitle("To Do List App v1.0 - Employee")
        self.setFixedSize(800, 600)
        central = QWidget()
        layout = QVBoxLayout()
        label = QLabel(f"Welcome, {user.name}")
        layout.addWidget(label)
        self.task_table = QTableWidget()
        self.task_table.setColumnCount(5)
        self.task_table.setHorizontalHeaderLabels(["Title", "Description", "Priority", "Due Date", "Status"])
        self.task_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.task_table.setSelectionMode(QAbstractItemView.SingleSelection)
        layout.addWidget(self.task_table)
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.load_tasks)
        layout.addWidget(refresh_btn)
        mark_done_btn = QPushButton("Mark Selected as Done")
        mark_done_btn.clicked.connect(self.mark_done)
        layout.addWidget(mark_done_btn)
        logout_btn = QPushButton("Logout")
        logout_btn.clicked.connect(self.close)
        layout.addWidget(logout_btn)
        central.setLayout(layout)
        self.setCentralWidget(central)
        self.load_tasks()

    def load_tasks(self):
        self.user = self.storage.load_user(self.user.id)  # Refresh user data
        self.task_table.setRowCount(0)
        rows = []
        for tid in self.user.assigned_task_ids:
            task = self.storage.load_task(tid)
            if not task:
                continue
            status_dict = task.assignee_status.get(self.user.id, {'completed': False})
            if tid in self.user.pending_verifications:
                status = "Pending Verification"
            elif status_dict['completed']:
                status = "Completed"
            else:
                status = "In Progress"
            rows.append((task.title, task.description, str(task.priority), task.due_date.isoformat(), status))
        self.task_table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.task_table.setItem(i, j, QTableWidgetItem(val))

    def mark_done(self):
        row = self.task_table.currentRow()
        if row == -1:
            return
        tid = self.user.assigned_task_ids[row]
        task = self.storage.load_task(tid)
        if tid not in self.user.pending_verifications and not task.assignee_status[self.user.id]['completed']:
            self.user.pending_verifications.append(tid)
            self.storage.save_user(self.user)
            self.load_tasks()