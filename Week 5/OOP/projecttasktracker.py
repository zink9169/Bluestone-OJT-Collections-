from abc import ABC, abstractmethod
from datetime import datetime



class User(ABC):
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email

    @abstractmethod
    def get_permissions(self):
        pass


class AdminUser(User):
    def get_permissions(self):
        return ["manage_users", "manage_projects", "manage_tasks", "log_hours"]


class ManagerUser(User):
    def get_permissions(self):
        return ["manage_projects", "manage_tasks", "log_hours"]


class DeveloperUser(User):
    def get_permissions(self):
        return ["update_own_tasks", "log_hours"]



class Comment:
    def __init__(self, comment_id, user, content):
        self.comment_id = comment_id
        self.user = user
        self.content = content
        self.timestamp = datetime.now()


class Task:
    def __init__(self, task_id, title, priority, assigned_to=None):
        self.task_id = task_id
        self.title = title
        self.priority = priority
        self.assigned_to = assigned_to
        self.status = "To Do"  # To Do, In Progress, Done
        self.time_logged = 0
        self.comments = []

    def update_status(self, new_status):
        self.status = new_status
        print(f"Task {self.task_id} moved to {new_status}")

    def add_comment(self, user, content):
        comment = Comment(len(self.comments) + 1, user, content)
        self.comments.append(comment)

    def log_time(self, hours):
        self.time_logged += hours



class Project:
    def __init__(self, project_id, title, manager):
        self.project_id = project_id
        self.title = title
        self.manager = manager
        self.members = []
        self.tasks = []

    def add_task(self, title, priority):
        task = Task(len(self.tasks) + 1, title, priority)
        self.tasks.append(task)
        return task

    def get_progress(self):
        if not self.tasks: return 0
        done = sum(1 for t in self.tasks if t.status == "Done")
        return (done / len(self.tasks)) * 100



class ProjectManagerSystem:
    def __init__(self):
        self.users = {}
        self.projects = {}

    def add_user(self, user):
        self.users[user.user_id] = user

    def create_project(self, p_id, title, manager_id):
        manager = self.users.get(manager_id)
        if manager and "manage_projects" in manager.get_permissions():
            project = Project(p_id, title, manager)
            self.projects[p_id] = project
            print(f"Project '{title}' created.")
        else:
            print("Access Denied or Manager not found.")

    def generate_report(self):
        print("\n--- Project Status Report ---")
        for p in self.projects.values():
            print(f"Project: {p.title} | Progress: {p.get_progress()}% | Manager: {p.manager.name}")



sys = ProjectManagerSystem()

admin = AdminUser("A1", "Alice", "alice@company.com")
dev = DeveloperUser("D1", "Bob", "bob@code.com")
sys.add_user(admin)
sys.add_user(dev)

sys.create_project("PRJ01", "AI Integration", "A1")
ai_project = sys.projects["PRJ01"]
t1 = ai_project.add_task("Setup Environment", "High")

t1.assigned_to = dev
t1.update_status("In Progress")
t1.log_time(5)
t1.add_comment(dev, "Working on the Dockerfile.")

sys.generate_report()