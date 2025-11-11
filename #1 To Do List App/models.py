from dataclasses import dataclass, asdict
from datetime import date, datetime
from typing import Dict, List

@dataclass
class Task:
    id: str
    title: str
    description: str
    priority: int  # 1 = highest, 5 = lowest
    due_date: date
    assignee_status: Dict[str, Dict[str, any]]  # {user_id: {'assigned_date': datetime, 'completed': bool}}

    def to_dict(self):
        d = asdict(self)
        d['due_date'] = d['due_date'].isoformat()
        for status in d['assignee_status'].values():
            status['assigned_date'] = status['assigned_date'].isoformat()
        return d

    @classmethod
    def from_dict(cls, d):
        d['due_date'] = date.fromisoformat(d['due_date'])
        for status in d['assignee_status'].values():
            status['assigned_date'] = datetime.fromisoformat(status['assigned_date'])
        return cls(**d)

@dataclass
class User:
    id: str
    username: str
    name: str
    email: str
    password_hash: str
    is_manager: bool
    date_employed: date
    assigned_task_ids: List[str]
    pending_verifications: List[str]
    current_assigned: int = 0
    ever_assigned: int = 0
    completed: int = 0

    def to_dict(self):
        d = asdict(self)
        d['date_employed'] = d['date_employed'].isoformat()
        return d

    @classmethod
    def from_dict(cls, d):
        d['date_employed'] = date.fromisoformat(d['date_employed'])
        return cls(**d)