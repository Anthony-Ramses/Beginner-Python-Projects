from tasks import TaskOperations


if __name__ == '__main__':
    app = TaskOperations()

    while True:
        print('1. Create task\n2. Read task\n3. Update task\n4. Read all tasks\n5. Delete task\n6. Sort task\n7. Filter task\n')
        try:
            ans = int(input('Choose an option: '))
        except ValueError:
            print('Please enter a valid number.')
            continue

        if ans == 1:
            name = input('Enter task name: ')
            description = input('Enter task description: ')
            try:
                app.create_tasks(name, description)
            except ValueError as e:
                print('Error:', e)
        elif ans == 2:
            name = input('Enter task name to read: ')
            try:
                app.read_task(name)
            except ValueError as e:
                print('Error:', e)
        elif ans == 3:
            name = input('Enter task name to update: ')
            new_description = input('Enter new task description: ')
            try:
                app.update_task(name, new_description)
            except ValueError as e:
                print('Error:', e)
        elif ans == 4:
            app.read_all_tasks()
        elif ans == 5:
            name = input('Enter task name to delete: ')
            try:
                app.delete_tasks(name)
            except ValueError as e:
                print('Error:', e)
        elif ans == 6:
            by = input('Enter sort condition: ')
            try:
                app.sort_task(by)
            except ValueError as e:
                print('Error:', e)
        elif ans == 7:
            by = input('Enter filter condition: ')
            letter = input('Enter the letter: ')
            try:
                app.filter_task(by, letter)
            except Exception as e:
                print('Error:', e)
        else:
            print('Unknown option.')