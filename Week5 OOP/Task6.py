from abc import ABC, abstractmethod
from datetime import datetime

# - User Classes -
class User(ABC):
    def __init__(self, user_id: int, name: str, email: str, role: str):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.role = role

    @abstractmethod
    def get_permissions(self):
        pass

class AdminUser(User):
    def __init__(self, user_id, name, email):
        super().__init__(user_id, name, email, role="Admin")

    def get_permissions(self):
        return ["manage_users", "manage_projects", "manage_tasks"]

class ManagerUser(User):
    def __init__(self, user_id, name, email):
        super().__init__(user_id, name, email, role="Manager")

    def get_permissions(self):
        return ["create_projects", "assign_tasks", "view_reports"]

class DeveloperUser(User):
    def __init__(self, user_id, name, email):
        super().__init__(user_id, name, email, role="Developer")

    def get_permissions(self):
        return ["update_tasks", "log_hours", "add_comments"]

# -Comment -
class Comment:
    def __init__(self, comment_id: int, user: User, content: str):
        self.comment_id = comment_id
        self.user = user
        self.content = content
        self.timestamp = datetime.now()

# -Task -
class Task:
    def __init__(self, task_id: int, title: str, priority: str):
        self.task_id = task_id
        self.title = title
        self.status = "Pending"  # Pending, In Progress, Completed
        self.priority = priority  # Low, Medium, High
        self.assigned_to = None
        self.time_logged = 0.0
        self.comments = []

    def update_status(self, new_status: str):
        self.status = new_status

    def add_comment(self, comment: Comment):
        self.comments.append(comment)

    def log_time(self, hours: float):
        self.time_logged += hours

    def assign_user(self, user: User):
        self.assigned_to = user

# - Project -
class Project:
    def __init__(self, project_id: int, title: str, description: str, manager: User):
        self.project_id = project_id
        self.title = title
        self.description = description
        self.manager = manager
        self.members = []
        self.tasks = []

    def add_task(self, task: Task):
        self.tasks.append(task)

    def assign_user(self, task_id: int, user: User):
        for task in self.tasks:
            if task.task_id == task_id:
                task.assign_user(user)
                if user not in self.members:
                    self.members.append(user)

    def get_progress(self):
        if not self.tasks:
            return 0
        completed_tasks = sum(1 for t in self.tasks if t.status == "Completed")
        return round((completed_tasks / len(self.tasks)) * 100, 2)

# -- TaskBoard --
class TaskBoard:
    def __init__(self, tasks: list):
        self.tasks = tasks

    def group_tasks_by_status(self):
        grouped = {"Pending": [], "In Progress": [], "Completed": []}
        for task in self.tasks:
            grouped[task.status].append(task)
        return grouped

    def filter_tasks_by_user(self, user: User):
        return [task for task in self.tasks if task.assigned_to == user]

    def generate_report(self):
        report = {}
        grouped = self.group_tasks_by_status()
        for status, tasks in grouped.items():
            report[status] = len(tasks)
        return report

# -- Project Management System --
class ProjectManagerSystem:
    def __init__(self):
        self.users = []
        self.projects = []
        self.user_counter = 1
        self.project_counter = 1
        self.task_counter = 1
        self.comment_counter = 1

    # - User management --
    def add_user(self, user: User):
        self.users.append(user)
        print(f"{user.role} added: {user.name} (ID: {user.user_id})")

    def list_users(self):
        for user in self.users:
            print(f"ID: {user.user_id}, Name: {user.name}, Role: {user.role}, Email: {user.email}")

    def get_user_by_id(self, user_id: int):
        for user in self.users:
            if user.user_id == user_id:
                return user
        return None

    # - Project management -
    def add_project(self, title: str, description: str, manager_id: int):
        manager = self.get_user_by_id(manager_id)
        if manager and isinstance(manager, ManagerUser):
            project = Project(self.project_counter, title, description, manager)
            self.projects.append(project)
            print(f"Project added: {title} (ID: {self.project_counter})")
            self.project_counter += 1
        else:
            print("Invalid manager ID!")

    def list_projects(self):
        for project in self.projects:
            print(f"ID: {project.project_id}, Title: {project.title}, Manager: {project.manager.name}, Tasks: {len(project.tasks)}")

    def get_project_by_id(self, project_id: int):
        for project in self.projects:
            if project.project_id == project_id:
                return project
        return None

    # -Task management -
    def add_task_to_project(self, project_id: int, title: str, priority: str):
        project = self.get_project_by_id(project_id)
        if project:
            task = Task(self.task_counter, title, priority)
            project.add_task(task)
            print(f"Task added: {title} (ID: {self.task_counter}) to Project {project.title}")
            self.task_counter += 1
        else:
            print("Project not found!")

    def assign_task(self, project_id: int, task_id: int, user_id: int):
        project = self.get_project_by_id(project_id)
        user = self.get_user_by_id(user_id)
        if project and user:
            project.assign_user(task_id, user)
            print(f"Task {task_id} assigned to {user.name}")
        else:
            print("Project or user not found!")

    def update_task_status(self, project_id: int, task_id: int, status: str):
        project = self.get_project_by_id(project_id)
        if project:
            for task in project.tasks:
                if task.task_id == task_id:
                    task.update_status(status)
                    print(f"Task {task_id} status updated to {status}")
                    return
        print("Task not found!")

    def log_task_time(self, project_id: int, task_id: int, hours: float):
        project = self.get_project_by_id(project_id)
        if project:
            for task in project.tasks:
                if task.task_id == task_id:
                    task.log_time(hours)
                    print(f"{hours} hours logged for Task {task_id}")
                    return
        print("Task not found!")

    def add_comment_to_task(self, project_id: int, task_id: int, user_id: int, content: str):
        project = self.get_project_by_id(project_id)
        user = self.get_user_by_id(user_id)
        if project and user:
            for task in project.tasks:
                if task.task_id == task_id:
                    comment = Comment(self.comment_counter, user, content)
                    task.add_comment(comment)
                    self.comment_counter += 1
                    print(f"Comment added to Task {task_id} by {user.name}")
                    return
        print("Task or user not found!")

    # -- Reporting --
    def project_progress_report(self, project_id: int):
        project = self.get_project_by_id(project_id)
        if project:
            print(f"Project: {project.title}, Progress: {project.get_progress()}%")
        else:
            print("Project not found!")

# --Interactive Menu --
def main():
    system = ProjectManagerSystem()

    # -- Sample Users --
    system.add_user(AdminUser(system.user_counter, "Alice", "alice@admin.com"))
    system.user_counter += 1
    system.add_user(ManagerUser(system.user_counter, "Bob", "bob@manager.com"))
    system.user_counter += 1
    system.add_user(DeveloperUser(system.user_counter, "Charlie", "charlie@dev.com"))
    system.user_counter += 1

    while True:
        print("\n--- Project Management Menu ---")
        print("1. List Users")
        print("2. Add Project")
        print("3. List Projects")
        print("4. Add Task to Project")
        print("5. Assign Task")
        print("6. Update Task Status")
        print("7. Log Task Time")
        print("8. Add Comment to Task")
        print("9. Project Progress Report")
        print("10. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            system.list_users()
        elif choice == "2":
            title = input("Project Title: ")
            desc = input("Project Description: ")
            manager_id = int(input("Manager User ID: "))
            system.add_project(title, desc, manager_id)
        elif choice == "3":
            system.list_projects()
        elif choice == "4":
            project_id = int(input("Project ID: "))
            title = input("Task Title: ")
            priority = input("Priority (Low/Medium/High): ")
            system.add_task_to_project(project_id, title, priority)
        elif choice == "5":
            project_id = int(input("Project ID: "))
            task_id = int(input("Task ID: "))
            user_id = int(input("User ID to assign: "))
            system.assign_task(project_id, task_id, user_id)
        elif choice == "6":
            project_id = int(input("Project ID: "))
            task_id = int(input("Task ID: "))
            status = input("New Status (Pending/In Progress/Completed): ")
            system.update_task_status(project_id, task_id, status)
        elif choice == "7":
            project_id = int(input("Project ID: "))
            task_id = int(input("Task ID: "))
            hours = float(input("Hours to log: "))
            system.log_task_time(project_id, task_id, hours)
        elif choice == "8":
            project_id = int(input("Project ID: "))
            task_id = int(input("Task ID: "))
            user_id = int(input("User ID: "))
            content = input("Comment: ")
            system.add_comment_to_task(project_id, task_id, user_id, content)
        elif choice == "9":
            project_id = int(input("Project ID: "))
            system.project_progress_report(project_id)
        elif choice == "10":
            print("Exiting...")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
