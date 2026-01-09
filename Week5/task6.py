from abc import ABC, abstractmethod
from datetime import datetime

class User(ABC):
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email

    #Parent class မှာ method ရှိရမယ် / Child class တိုင်းမှာ မဖြစ်မနေ override လုပ်စေချင်တဲ့အခါ @ abstractmethod ကို သုံးပါတယ်
    #Parent class မှာရှိပြီးသား method ကို Child class ထဲမှာ ပြန်ရေး (re-define) လုပ်တာကို override လို့ခေါ်ပါတယ်
    @abstractmethod
    def get_permissions(self):
        pass

class AdminUser(User):
    def get_permissions(self):
        return ["manage_users", "manage_projects", "manage_tasks"]

class ManagerUser(User):
    def get_permissions(self):
        return ["create_projects", "assign_tasks"]

class DeveloperUser(User):
    def get_permissions(self):
        return ["update_tasks", "log_hours"]


class Comment:
    def __init__(self, comment_id, user, content):
        self.comment_id = comment_id
        self.user = user
        self.content = content
        self.timestamp = datetime.now()


class Task:
    def __init__(self, task_id, title, priority="Medium"):
        self.task_id = task_id
        self.title = title
        self.status = "ToDo"  # ToDo, InProgress, Done
        self.priority = priority
        self.assigned_to = None
        self.time_logged = 0  # hours
        self.comments = []

    def update_status(self, status):
        self.status = status

    def add_comment(self, comment):
        self.comments.append(comment)

    def log_time(self, hours):
        self.time_logged += hours


class Project:
    def __init__(self, project_id, title, description, manager):
        self.project_id = project_id
        self.title = title
        self.description = description
        self.manager = manager
        self.members = []  # list of Users
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def assign_user(self, user):
        if user not in self.members:
            self.members.append(user)

    def get_progress(self):
        if not self.tasks:
            return 0
        done_tasks = sum(1 for t in self.tasks if t.status=="Done")
        return round((done_tasks/len(self.tasks))*100, 2)

# Static Method  → "General purpose tool"
# Normal Method  → "Tool attached to this specific object"
class TaskBoard:
    @staticmethod
    def group_tasks_by_status(project):
        grouped = {"ToDo": [], "InProgress": [], "Done": []}
        for t in project.tasks:
            grouped[t.status].append(t)
        return grouped

    @staticmethod
    def filter_tasks_by_user(project, user):
        return [t for t in project.tasks if t.assigned_to == user]

    @staticmethod
    def generate_report(project):
        print(f"\nProject: {project.title}")
        print(f"Manager: {project.manager.name}")
        print(f"Progress: {project.get_progress()}%")
        print("Tasks:")
        for t in project.tasks:
            assigned = t.assigned_to.name if t.assigned_to else "Unassigned"
            print(f"  {t.task_id}: {t.title}, Status: {t.status}, Assigned to: {assigned}, Logged Hours: {t.time_logged}")

class ProjectManagerSystem:
    def __init__(self):
        self.users = {}
        self.projects = {}
        self.logged_in_user = None

    def add_user(self, user):
        self.users[user.user_id] = user

    def authenticate(self, user_id):
        user = self.users.get(user_id)
        if user:
            self.logged_in_user = user
            print(f"Welcome {user.name} ({type(user).__name__})!")
        else:
            print("Invalid user ID!")

    def create_project(self, project_id, title, description):
        if isinstance(self.logged_in_user, ManagerUser) or isinstance(self.logged_in_user, AdminUser):
            project = Project(project_id, title, description, self.logged_in_user)
            self.projects[project_id] = project
            print(f"Project '{title}' created successfully.")
        else:
            print("You do not have permission to create projects.")

    def add_task_to_project(self, project_id, task_id, title, priority="Medium"):
        project = self.projects.get(project_id)
        if project and (isinstance(self.logged_in_user, ManagerUser) or isinstance(self.logged_in_user, AdminUser)):
            task = Task(task_id, title, priority)
            project.add_task(task)
            print(f"Task '{title}' added to project '{project.title}'")
        else:
            print("Project not found or insufficient permissions.")

    def assign_task(self, project_id, task_id, user_id):
        project = self.projects.get(project_id)
        task = next((t for t in project.tasks if t.task_id==task_id), None)
        user = self.users.get(user_id)
        if task and user and (isinstance(self.logged_in_user, ManagerUser) or isinstance(self.logged_in_user, AdminUser)):
            task.assigned_to = user
            project.assign_user(user)
            print(f"Task '{task.title}' assigned to {user.name}")
        else:
            print("Task/User not found or insufficient permissions.")


if __name__ == "__main__":
    system = ProjectManagerSystem()

    admin = AdminUser("U001", "Alice", "alice@example.com")
    manager = ManagerUser("U002", "Bob", "bob@example.com")
    dev1 = DeveloperUser("U003", "Charlie", "charlie@example.com")
    dev2 = DeveloperUser("U004", "Diana", "diana@example.com")

    system.add_user(admin)
    system.add_user(manager)
    system.add_user(dev1)
    system.add_user(dev2)

    system.authenticate("U002")

    system.create_project("P001", "Website Revamp", "Update website UI and backend")


    system.add_task_to_project("P001", "T001", "Design new UI", "High")
    system.add_task_to_project("P001", "T002", "Implement API", "Medium")


    system.assign_task("P001", "T001", "U003")
    system.assign_task("P001", "T002", "U004")


    dev_task = system.projects["P001"].tasks[0]
    dev_task.log_time(5)
    dev_task.update_status("InProgress")
    comment = Comment("C001", dev1, "Started working on UI design")
    dev_task.add_comment(comment)


    TaskBoard.generate_report(system.projects["P001"])
