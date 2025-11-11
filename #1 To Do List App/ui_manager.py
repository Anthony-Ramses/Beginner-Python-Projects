from PySide6.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox, QComboBox, QDateEdit, QTableWidget, QTableWidgetItem, QAbstractItemView, QInputDialog, QHBoxLayout
from PySide6.QtCore import QDate
from storage import Storage
from models import User, Task
from utils import generate_list_pdf, generate_task_pdf
from datetime import datetime, date
import uuid
import os

class ManagerUI(QMainWindow):
    def __init__(self, storage: Storage, user: User):
        super().__init__()
        self.storage = storage
        self.user = user
        self.setWindowTitle("To Do List App v1.0 - Manager")
        self.setFixedSize(800, 600)
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_list_tab(), "Lists")
        self.tabs.addTab(self.create_task_tab(), "Tasks")
        self.tabs.addTab(self.create_employee_tab(), "Employees")
        self.tabs.addTab(self.create_verification_tab(), "Verifications")
        self.setCentralWidget(self.tabs)
        self.refresh_all()

    def refresh_all(self):
        self.refresh_lists()
        self.refresh_tasks()
        self.refresh_employees()
        self.refresh_verifications()

    def create_list_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        create_hbox = QHBoxLayout()
        self.create_list_input = QLineEdit()
        self.create_list_input.setPlaceholderText("New List Title")
        create_hbox.addWidget(self.create_list_input)
        create_btn = QPushButton("Create List")
        create_btn.clicked.connect(self.create_list)
        create_hbox.addWidget(create_btn)
        layout.addLayout(create_hbox)
        self.list_list = QListWidget()
        layout.addWidget(self.list_list)
        rename_btn = QPushButton("Rename Selected")
        rename_btn.clicked.connect(self.rename_list)
        layout.addWidget(rename_btn)
        delete_btn = QPushButton("Delete Selected")
        delete_btn.clicked.connect(self.delete_list)
        layout.addWidget(delete_btn)
        share_btn = QPushButton("Share Selected")
        share_btn.clicked.connect(self.share_list)
        layout.addWidget(share_btn)
        tab.setLayout(layout)
        return tab

    def create_list(self):
        title = self.create_list_input.text().strip()
        if not title:
            return
        lists = self.storage.load_lists()
        if title in lists:
            QMessageBox.warning(self, "Error", "List exists")
            return
        lists[title] = []
        self.storage.save_lists(lists)
        self.refresh_lists()

    def rename_list(self):
        item = self.list_list.currentItem()
        if not item:
            return
        old_title = item.text()
        new_title, ok = QInputDialog.getText(self, "Rename", "New Title:")
        if ok and new_title and new_title != old_title:
            lists = self.storage.load_lists()
            if new_title in lists:
                QMessageBox.warning(self, "Error", "Title exists")
                return
            lists[new_title] = lists.pop(old_title)
            self.storage.save_lists(lists)
            self.refresh_lists()

    def delete_list(self):
        item = self.list_list.currentItem()
        if not item:
            return
        title = item.text()
        lists = self.storage.load_lists()
        del lists[title]
        self.storage.save_lists(lists)
        self.refresh_lists()

    def share_list(self):
        item = self.list_list.currentItem()
        if not item:
            return
        title = item.text()
        receiver, ok = QInputDialog.getText(self, "Share", "Enter User ID or Email:")
        if not ok:
            return
        lists = self.storage.load_lists()
        task_ids = lists[title]
        user = self.find_user_by_id_or_email(receiver)
        if user:
            for tid in task_ids:
                self.assign_task_to_user(tid, user)
            QMessageBox.information(self, "Success", "List shared via app ID")
        else:
            pdf_path = generate_list_pdf(title, task_ids, self.storage.load_task)
            QMessageBox.information(self, "PDF Generated", f"PDF saved to {pdf_path}. Send via email manually.")

    def find_user_by_id_or_email(self, value: str) -> User | None:
        for uid in self.storage.get_all_user_ids():
            u = self.storage.load_user(uid)
            if u.id == value or u.email == value:
                return u
        return None

    def assign_task_to_user(self, task_id: str, user: User):
        task = self.storage.load_task(task_id)
        if user.id not in task.assignee_status:
            task.assignee_status[user.id] = {'assigned_date': datetime.now(), 'completed': False}
            self.storage.save_task(task)
            if task_id not in user.assigned_task_ids:
                user.assigned_task_ids.append(task_id)
                user.current_assigned += 1
                user.ever_assigned += 1
                self.storage.save_user(user)

    def refresh_lists(self):
        self.list_list.clear()
        lists = self.storage.load_lists()
        for title in sorted(lists.keys()):
            self.list_list.addItem(title)

    def create_task_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        self.list_combo = QComboBox()
        layout.addWidget(QLabel("Select List for New Task:"))
        layout.addWidget(self.list_combo)
        title_input = QLineEdit()
        title_input.setPlaceholderText("Title")
        layout.addWidget(title_input)
        desc_input = QLineEdit()
        desc_input.setPlaceholderText("Description")
        layout.addWidget(desc_input)
        pri_input = QLineEdit()
        pri_input.setPlaceholderText("Priority (1-5)")
        layout.addWidget(pri_input)
        due_input = QDateEdit()
        due_input.setDate(QDate.currentDate())
        layout.addWidget(due_input)
        create_btn = QPushButton("Create Task")
        create_btn.clicked.connect(lambda: self.create_task(title_input.text(), desc_input.text(), pri_input.text(), due_input.date().toPyDate()))
        layout.addWidget(create_btn)
        self.task_table = QTableWidget()
        self.task_table.setColumnCount(5)
        self.task_table.setHorizontalHeaderLabels(["Title", "Desc", "Pri", "Due", "Assignees"])
        self.task_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.task_table.setSelectionMode(QAbstractItemView.SingleSelection)
        layout.addWidget(self.task_table)
        filter_pri = QLineEdit("Priority Range (e.g. 1-3)")
        layout.addWidget(filter_pri)
        filter_due = QLineEdit("Due Date Range (e.g. 2025-11-01 to 2025-11-30)")
        layout.addWidget(filter_due)
        filter_ass = QLineEdit("Assignee Name")
        layout.addWidget(filter_ass)
        search_input = QLineEdit("Search Title/Desc")
        layout.addWidget(search_input)
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["Priority Desc", "Due Date Asc", "Assignment Time Asc"])
        layout.addWidget(self.sort_combo)
        apply_btn = QPushButton("Apply Filters/Sort/Search")
        apply_btn.clicked.connect(lambda: self.refresh_tasks(filter_pri.text(), filter_due.text(), filter_ass.text(), search_input.text(), self.sort_combo.currentText()))
        layout.addWidget(apply_btn)
        update_btn = QPushButton("Update Selected")
        update_btn.clicked.connect(self.update_task)
        layout.addWidget(update_btn)
        delete_btn = QPushButton("Delete Selected")
        delete_btn.clicked.connect(self.delete_task)
        layout.addWidget(delete_btn)
        assign_btn = QPushButton("Assign Selected")
        assign_btn.clicked.connect(self.assign_task)
        layout.addWidget(assign_btn)
        pri_change_btn = QPushButton("Change Priority of Selected")
        pri_change_btn.clicked.connect(self.change_priority)
        layout.addWidget(pri_change_btn)
        tab.setLayout(layout)
        return tab

    def create_task(self, title: str, desc: str, pri_str: str, due: date):
        try:
            pri = int(pri_str)
            if not 1 <= pri <= 5:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid priority")
            return
        list_title = self.list_combo.currentText()
        if not list_title:
            QMessageBox.warning(self, "Error", "Select list")
            return
        tid = str(uuid.uuid4())
        task = Task(tid, title, desc, pri, due, {})
        self.storage.save_task(task)
        lists = self.storage.load_lists()
        lists[list_title].append(tid)
        self.storage.save_lists(lists)
        self.refresh_tasks()

    def update_task(self):
        row = self.task_table.currentRow()
        if row == -1:
            return
        tid = self.current_tasks[row].id
        task = self.storage.load_task(tid)
        new_title, ok = QInputDialog.getText(self, "Update Title", "New Title:", text=task.title)
        if ok:
            task.title = new_title
        new_desc, ok = QInputDialog.getText(self, "Update Desc", "New Desc:", text=task.description)
        if ok:
            task.description = new_desc
        self.storage.save_task(task)
        self.refresh_tasks()

    def delete_task(self):
        row = self.task_table.currentRow()
        if row == -1:
            return
        tid = self.current_tasks[row].id
        lists = self.storage.load_lists()
        for task_ids in lists.values():
            if tid in task_ids:
                task_ids.remove(tid)
        self.storage.save_lists(lists)
        os.remove(os.path.join(self.storage.tasks_dir, f'{tid}.json'))
        self.refresh_tasks()

    def assign_task(self):
        row = self.task_table.currentRow()
        if row == -1:
            return
        tid = self.current_tasks[row].id
        receiver, ok = QInputDialog.getText(self, "Assign", "Enter User ID or Email:")
        if not ok:
            return
        user = self.find_user_by_id_or_email(receiver)
        if user:
            self.assign_task_to_user(tid, user)
            QMessageBox.information(self, "Success", "Task assigned via app ID")
            self.refresh_tasks()
        else:
            task = self.storage.load_task(tid)
            pdf_path = generate_task_pdf(task)
            QMessageBox.information(self, "PDF Generated", f"PDF saved to {pdf_path}. Send via email manually.")
    
    def change_priority(self):
        row = self.task_table.currentRow()
        if row == -1:
            return
        tid = self.current_tasks[row].id
        new_pri_str, ok = QInputDialog.getInt(self, "Change Priority", "New Priority (1-5):", min=1, max=5)
        if ok:
            task = self.storage.load_task(tid)
            task.priority = new_pri_str
            self.storage.save_task(task)
            self.refresh_tasks()

    def refresh_tasks(self, pri_filter: str = "", due_filter: str = "", assignee_filter: str = "", search_text: str = "", sort_mode: str = "Priority Desc"):
        self.list_combo.clear()
        self.list_combo.addItems(sorted(self.storage.load_lists().keys()))
        if search_text:
            tasks = [t for t in self.current_tasks if search_text.lower() in t.title.lower() or search_text.lower() in t.description.lower()]
        if pri_filter:
            try:
                low, high = map(int, pri_filter.split('-'))
                tasks = [t for t in self.current_tasks if low <= t.priority <= high]
            except:
                pass#
        if due_filter:
            try:
                start_str, end_str = due_filter.split('to')
                start_date = date.fromisoformat(start_str.strip())
                end_date = date.fromisoformat(end_str.strip())
                tasks = [t for t in self.current_tasks if start_date <= t.due_date <= end_date]
            except:
                pass
        if assignee_filter:
            tasks = [t for t in self.current_tasks if any(self.storage.load_user(uid).name.lower() == assignee_filter.lower().find(assignee_filter.lower()) != -1 for uid in t.assignee_status)]
        if sort_mode == "Priority Desc":
            tasks.sort(key=lambda t: t.priority, reverse=True)
        elif sort_mode == "Due Date Asc":
            tasks.sort(key=lambda t: t.due_date)
        elif sort_mode == "Assignment Time Asc":
            tasks.sort(key=lambda t: min((status['assigned_date'] for status in t.assignee_status.values()), default=datetime.max))
        self.current_tasks = tasks
        self.task_table.setRowCount(len(tasks))
        for i, t in enumerate(tasks):
            self.task_table.setItem(i, 0, QTableWidgetItem(t.title))
            self.task_table.setItem(i, 1, QTableWidgetItem(t.description))
            self.task_table.setItem(i, 2, QTableWidgetItem(str(t.priority)))
            self.task_table.setItem(i, 3, QTableWidgetItem(t.due_date.isoformat()))
            assignees = ', '.join(self.storage.load_user(uid).name for uid in t.assignee_status)
            self.task_table.setItem(i, 4, QTableWidgetItem(assignees))
        
    def create_employee_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        create_btn = QPushButton("Create New Employee")
        create_btn.clicked.connect(self.create_employee_ui)
        layout.addWidget(create_btn)
        self.employee_table = QTableWidget()
        self.employee_table.setColumnCount(7)
        self.employee_table.setHorizontalHeaderLabels(["Name", "Username", "Email", "Date Employed", "Current Assigned", "Ever Assigned", "Completed"])
        layout.addWidget(self.employee_table)
        tab.setLayout(layout)
        return tab

    def create_employee_ui(self):
        name, ok = QInputDialog.getText(self, "Employee Name", "Enter Name:")
        if not ok: return
        username, ok = QInputDialog.getText(self, "Employee Username", "Enter Username:")
        if not ok: return
        email, ok = QInputDialog.getText(self, "Employee Email", "Enter Email:")
        if not ok: return
        password, ok = QInputDialog.getText(self, "Employee Password", "Enter Password:", QLineEdit.Password)
        if not ok: return
        self.storage.create_employee(name, email, username, password)
        self.refresh_employees()

    def refresh_employees(self):
        employees = [self.storage.load_user(uid) for uid in self.storage.get_all_user_ids() if not self.storage.load_user(uid).is_manager]
        self.employee_table.setRowCount(len(employees))
        for i, u in enumerate(employees):
            self.employee_table.setItem(i, 0, QTableWidgetItem(u.name))
            self.employee_table.setItem(i, 1, QTableWidgetItem(u.username))
            self.employee_table.setItem(i, 2, QTableWidgetItem(u.email))
            self.employee_table.setItem(i, 3, QTableWidgetItem(u.date_employed.isoformat()))
            self.employee_table.setItem(i, 4, QTableWidgetItem(str(u.current_assigned)))
            self.employee_table.setItem(i, 5, QTableWidgetItem(str(u.ever_assigned)))
            self.employee_table.setItem(i, 6, QTableWidgetItem(str(u.completed)))

    def create_verification_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        self.verification_table = QTableWidget()
        self.verification_table.setColumnCount(3)
        self.verification_table.setHorizontalHeaderLabels(["Employee Name", "Task Title", "Assigned Date"])
        self.verification_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.verification_table.setSelectionMode(QAbstractItemView.SingleSelection)
        layout.addWidget(self.verification_table)
        verify_btn = QPushButton("Verify Selected Completion")
        verify_btn.clicked.connect(self.verify_completion)
        layout.addWidget(verify_btn)
        tab.setLayout(layout)
        return tab
    
    def refresh_verifications(self):
        self.pendings = []
        row = 0
        self.verification_table.setRowCount(0)
        for uid in self.storage.get_all_user_ids():
            u = self.storage.load_user(uid)
            if u.is_manager:
                continue
            for tid in u.pending_verifications:
                task = self.storage.load_task(tid)
                if task:
                    self.verification_table.setRowCount(row + 1)
                    self.verification_table.setItem(row, 0, QTableWidgetItem(u.name))
                    self.verification_table.setItem(row, 1, QTableWidgetItem(task.title))
                    self.verification_table.setItem(row, 2, QTableWidgetItem(task.due_date.isoformat()))
                    self.pendings.append((uid, tid))
                    row += 1

    def verify_completion(self):
        row = self.verification_table.currentRow()
        if row == -1:
            return
        uid, tid = self.pendings[row]
        task = self.storage.load_task(tid)
        if user and task:
            task.assignee_status[uid]['completed'] = True
            self.storage.save_task(task)
            user = self.storage.load_user(uid)
            user.pending_verifications.remove(tid)
            user.completed += 1
            user.current_assigned -= 1
            self.storage.save_user(user)
            self.refresh_verifications()