class Tasks:
    def __init__(self, name, description):
        self.name = name
        self.description = description


class TaskOperations:
    def __init__(self):
        self.lists = []
        self.tasks = []

    def create_tasks(self, name, description):
        # don't allow duplicate task names
        if any(t.name == name for t in self.tasks):
            raise ValueError('Task with the same name found')
        task = Tasks(name, description)
        self.tasks.append(task)
        print(f'Task [{name}] created successfully.')

    def read_task(self, name):
        # find task by name and print it
        for t in self.tasks:
            if t.name == name:
                print(f'Task Name: {t.name}\nTask Description: {t.description}')
                return
        # if not found, raise
        raise ValueError(f'No task named [{name}] found.')
    
    def read_all_tasks(self):
        if not self.tasks:
            print("No tasks available.")
            return
        for t in self.tasks:
            print(f'Task Name: {t.name}\nTask Description: {t.description}\n')
    
    def update_task(self, name, new_description):
        for t in self.tasks:
            if t.name == name:
                t.description = new_description
                print(f'Task [{name}] updated successfully.')
                return
        raise ValueError(f'No task named [{name}] found.')
    
    def delete_tasks(self, name):
        for t in self.tasks:
            if t.name == name:
                self.tasks.remove(t)
                print(f'Task [{name}] deleted successfully.')
                return
        raise ValueError(f'No task named [{name}] found.')
    



