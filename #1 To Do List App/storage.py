import os
import json
import uuid
import hashlib
from datetime import date, datetime
from models import Task, User

class Storage:
    def __init__(self, root_dir='./data'):
        self.root_dir = root_dir
        os.makedirs(self.root_dir, exist_ok=True)
        self.users_dir = os.path.join(self.root_dir, 'users')
        os.makedirs(self.users_dir, exist_ok=True)
        self.tasks_dir = os.path.join(self.root_dir, 'tasks')
        os.makedirs(self.tasks_dir, exist_ok=True)
        self.lists_file = os.path.join(self.root_dir, 'lists.json')
        if not os.path.exists(self.lists_file):
            with open(self.lists_file, 'w') as f:
                json.dump({}, f)

    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def save_user(self, user: User):
        path = os.path.join(self.users_dir, f'{user.id}.json')
        with open(path, 'w') as f:
            json.dump(user.to_dict(), f)

    def load_user(self, user_id: str) -> User | None:
        path = os.path.join(self.users_dir, f'{user_id}.json')
        if not os.path.exists(path):
            return None
        with open(path, 'r') as f:
            d = json.load(f)
        return User.from_dict(d)

    def load_user_by_username(self, username: str) -> User | None:
        for uid in self.get_all_user_ids():
            u = self.load_user(uid)
            if u and u.username == username:
                return u
        return None

    def get_all_user_ids(self) -> list[str]:
        return [f.split('.json')[0] for f in os.listdir(self.users_dir) if f.endswith('.json')]

    def get_manager(self) -> User | None:
        for uid in self.get_all_user_ids():
            u = self.load_user(uid)
            if u and u.is_manager:
                return u
        return None

    def create_manager(self, name: str, email: str, username: str, password: str) -> User:
        uid = str(uuid.uuid4())
        ph = self.hash_password(password)
        user = User(uid, username, name, email, ph, True, date.today(), [], [])
        self.save_user(user)
        return user

    def create_employee(self, name: str, email: str, username: str, password: str) -> User:
        uid = str(uuid.uuid4())
        ph = self.hash_password(password)
        user = User(uid, username, name, email, ph, False, date.today(), [], [])
        self.save_user(user)
        return user

    def authenticate(self, username: str, password: str) -> User | None:
        user = self.load_user_by_username(username)
        if user and user.password_hash == self.hash_password(password):
            return user
        return None

    def load_lists(self) -> dict[str, list[str]]:
        with open(self.lists_file, 'r') as f:
            return json.load(f)

    def save_lists(self, lists_dict: dict[str, list[str]]):
        with open(self.lists_file, 'w') as f:
            json.dump(lists_dict, f)

    def save_task(self, task: Task):
        path = os.path.join(self.tasks_dir, f'{task.id}.json')
        with open(path, 'w') as f:
            json.dump(task.to_dict(), f)

    def load_task(self, task_id: str) -> Task | None:
        path = os.path.join(self.tasks_dir, f'{task_id}.json')
        if not os.path.exists(path):
            return None
        with open(path, 'r') as f:
            d = json.load(f)
        return Task.from_dict(d)

    def get_all_task_ids(self) -> list[str]:
        return [f.split('.json')[0] for f in os.listdir(self.tasks_dir) if f.endswith('.json')]