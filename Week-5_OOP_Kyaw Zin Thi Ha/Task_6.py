from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Set, Any

def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")

def read_int(prompt: str) -> int:
    raw = input(prompt).strip()
    try:
        return int(raw)
    except ValueError:
        raise ValueError("Please enter a valid integer.")

def read_nonempty(prompt: str) -> str:
    s = input(prompt).strip()
    if not s:
        raise ValueError("Input cannot be empty.")
    return s

def read_choice(prompt: str, allowed: List[str]) -> str:
    c = input(prompt).strip()
    if c not in allowed:
        raise ValueError(f"Invalid choice. Allowed: {', '.join(allowed)}")
    return c


class User(ABC):
    def __init__(self, user_id: int, name: str, email: str, role: str) -> None:
        self.user_id = user_id
        self.name = name.strip()
        self.email = email.strip().lower()
        self.role = role

    @abstractmethod
    def get_permissions(self) -> Set[str]:
        """Return a set of permission strings."""
        raise NotImplementedError

    def __str__(self) -> str:
        return f"{self.role} | ID {self.user_id} | {self.name} ({self.email})"


class AdminUser(User):
    def __init__(self, user_id: int, name: str, email: str) -> None:
        super().__init__(user_id, name, email, role="ADMIN")

    def get_permissions(self) -> Set[str]:
        return {
            "USER_MANAGE",
            "PROJECT_CREATE",
            "PROJECT_MANAGE",
            "TASK_CREATE",
            "TASK_ASSIGN",
            "TASK_UPDATE_ANY",
            "REPORT_VIEW",
        }


class ManagerUser(User):
    def __init__(self, user_id: int, name: str, email: str) -> None:
        super().__init__(user_id, name, email, role="MANAGER")

    def get_permissions(self) -> Set[str]:
        return {
            "PROJECT_CREATE",
            "PROJECT_MANAGE",
            "TASK_CREATE",
            "TASK_ASSIGN",
            "TASK_UPDATE_ANY",
            "REPORT_VIEW",
        }


class DeveloperUser(User):
    def __init__(self, user_id: int, name: str, email: str) -> None:
        super().__init__(user_id, name, email, role="DEVELOPER")

    def get_permissions(self) -> Set[str]:
        return {
            "TASK_UPDATE_OWN",
            "TASK_LOG_HOURS_OWN",
            "REPORT_VIEW",
        }




@dataclass
class Comment:
    comment_id: int
    user_id: int
    content: str
    timestamp: str


@dataclass
class Task:
    task_id: int
    title: str
    status: str = "TODO"         
    priority: str = "MEDIUM"    
    assigned_to: Optional[int] = None
    time_logged: float = 0.0
    comments: List[Comment] = field(default_factory=list)

    def update_status(self, new_status: str) -> None:
        allowed = {"TODO", "IN_PROGRESS", "DONE", "BLOCKED"}
        if new_status not in allowed:
            raise ValueError(f"Invalid status. Allowed: {', '.join(sorted(allowed))}")
        self.status = new_status

    def add_comment(self, comment: Comment) -> None:
        self.comments.append(comment)

    def log_time(self, hours: float) -> None:
        if hours <= 0:
            raise ValueError("Hours must be > 0.")
        self.time_logged += hours


@dataclass
class Project:
    project_id: int
    title: str
    description: str
    manager_id: int
    members: Set[int] = field(default_factory=set)
    tasks: Dict[int, Task] = field(default_factory=dict)

    def add_task(self, task: Task) -> None:
        if task.task_id in self.tasks:
            raise ValueError("Task ID already exists in this project.")
        self.tasks[task.task_id] = task

    def assign_user(self, user_id: int) -> None:
        self.members.add(user_id)

    def get_progress(self) -> float:
        if not self.tasks:
            return 0.0
        done = sum(1 for t in self.tasks.values() if t.status == "DONE")
        return round((done / len(self.tasks)) * 100.0, 2)



class TaskBoard:
    def __init__(self, project: Project) -> None:
        self.project = project

    def group_tasks_by_status(self) -> Dict[str, List[Task]]:
        grouped: Dict[str, List[Task]] = {}
        for t in self.project.tasks.values():
            grouped.setdefault(t.status, []).append(t)
        return grouped

    def filter_tasks_by_user(self, user_id: int) -> List[Task]:
        return [t for t in self.project.tasks.values() if t.assigned_to == user_id]

    def generate_report(self) -> str:
        total = len(self.project.tasks)
        progress = self.project.get_progress()
        grouped = self.group_tasks_by_status()

        lines = []
        lines.append("=" * 70)
        lines.append(f"Project Report: {self.project.title} (ID {self.project.project_id})")
        lines.append(f"Progress: {progress}% | Total tasks: {total}")
        lines.append("-" * 70)
        for status, tasks in sorted(grouped.items(), key=lambda x: x[0]):
            lines.append(f"{status}: {len(tasks)}")
        lines.append("=" * 70)
        return "\n".join(lines)




class ProjectManagerSystem:
    def __init__(self) -> None:
        self.users: Dict[int, User] = {}
        self.projects: Dict[int, Project] = {}

        self._next_user_id = 1001
        self._next_project_id = 2001
        self._next_task_id = 3001
        self._next_comment_id = 4001

        self.current_user: Optional[User] = None



    def login(self, user_id: int) -> None:
        u = self.users.get(user_id)
        if not u:
            raise ValueError("User not found.")
        self.current_user = u

    def logout(self) -> None:
        self.current_user = None

    def require_perm(self, perm: str) -> None:
        if not self.current_user:
            raise ValueError("You must login first.")
        if perm not in self.current_user.get_permissions():
            raise ValueError("Permission denied.")

   

    def create_user(self, role: str, name: str, email: str) -> User:
        self.require_perm("USER_MANAGE")
        role = role.upper().strip()
        uid = self._next_user_id
        self._next_user_id += 1

        if role == "ADMIN":
            u = AdminUser(uid, name, email)
        elif role == "MANAGER":
            u = ManagerUser(uid, name, email)
        elif role == "DEVELOPER":
            u = DeveloperUser(uid, name, email)
        else:
            raise ValueError("Invalid role. Use ADMIN / MANAGER / DEVELOPER.")

        self.users[uid] = u
        return u

  

    def create_project(self, title: str, description: str, manager_id: int) -> Project:
        self.require_perm("PROJECT_CREATE")
        manager = self.users.get(manager_id)
        if not manager or manager.role not in {"ADMIN", "MANAGER"}:
            raise ValueError("Manager ID must be an existing ADMIN or MANAGER user.")

        pid = self._next_project_id
        self._next_project_id += 1

        p = Project(project_id=pid, title=title.strip(), description=description.strip(), manager_id=manager_id)
        p.assign_user(manager_id)  
        self.projects[pid] = p
        return p

    def add_member_to_project(self, project_id: int, user_id: int) -> None:
        self.require_perm("PROJECT_MANAGE")
        p = self._get_project(project_id)
        if user_id not in self.users:
            raise ValueError("User not found.")
        p.assign_user(user_id)

   

    def create_task(self, project_id: int, title: str, priority: str) -> Task:
        self.require_perm("TASK_CREATE")
        p = self._get_project(project_id)

        tid = self._next_task_id
        self._next_task_id += 1

        priority = priority.upper().strip()
        allowed = {"LOW", "MEDIUM", "HIGH", "CRITICAL"}
        if priority not in allowed:
            raise ValueError(f"Invalid priority. Allowed: {', '.join(sorted(allowed))}")

        t = Task(task_id=tid, title=title.strip(), priority=priority)
        p.add_task(t)
        return t

    def assign_task(self, project_id: int, task_id: int, user_id: int) -> None:
        self.require_perm("TASK_ASSIGN")
        p = self._get_project(project_id)
        t = self._get_task(p, task_id)
        if user_id not in p.members:
            raise ValueError("User must be a member of the project to be assigned tasks.")
        t.assigned_to = user_id

    def update_task_status(self, project_id: int, task_id: int, new_status: str) -> None:
        p = self._get_project(project_id)
        t = self._get_task(p, task_id)

        if not self.current_user:
            raise ValueError("You must login first.")

        perms = self.current_user.get_permissions()

      
        if "TASK_UPDATE_ANY" in perms:
            pass
        elif "TASK_UPDATE_OWN" in perms:
            if t.assigned_to != self.current_user.user_id:
                raise ValueError("Developers can only update their own tasks.")
        else:
            raise ValueError("Permission denied.")

        t.update_status(new_status)

    def log_task_time(self, project_id: int, task_id: int, hours: float) -> None:
        p = self._get_project(project_id)
        t = self._get_task(p, task_id)

        if not self.current_user:
            raise ValueError("You must login first.")

        perms = self.current_user.get_permissions()
        if "TASK_UPDATE_ANY" in perms:
            t.log_time(hours)
        elif "TASK_LOG_HOURS_OWN" in perms:
            if t.assigned_to != self.current_user.user_id:
                raise ValueError("Developers can only log time for their own tasks.")
            t.log_time(hours)
        else:
            raise ValueError("Permission denied.")

    def add_task_comment(self, project_id: int, task_id: int, content: str) -> Comment:
        if not self.current_user:
            raise ValueError("You must login first.")
        self.require_perm("REPORT_VIEW")

        p = self._get_project(project_id)
        t = self._get_task(p, task_id)

        cid = self._next_comment_id
        self._next_comment_id += 1

        c = Comment(comment_id=cid, user_id=self.current_user.user_id, content=content.strip(), timestamp=now_iso())
        t.add_comment(c)
        return c


    def project_report(self, project_id: int) -> str:
        self.require_perm("REPORT_VIEW")
        p = self._get_project(project_id)
        return TaskBoard(p).generate_report()

    def list_users(self) -> None:
        if not self.users:
            print("No users.")
            return
        print("\nUsers")
        print("-" * 70)
        for u in self.users.values():
            print(str(u))
        print("-" * 70)

    def list_projects(self) -> None:
        if not self.projects:
            print("No projects.")
            return
        print("\nProjects")
        print("-" * 70)
        for p in self.projects.values():
            print(f"ID {p.project_id} | {p.title} | Manager ID {p.manager_id} | Progress {p.get_progress()}%")
        print("-" * 70)

    def list_project_tasks(self, project_id: int) -> None:
        self.require_perm("REPORT_VIEW")
        p = self._get_project(project_id)
        if not p.tasks:
            print("No tasks in this project.")
            return

        print(f"\nTasks for Project: {p.title} (ID {p.project_id})")
        print("-" * 90)
        for t in p.tasks.values():
            assigned = t.assigned_to if t.assigned_to is not None else "None"
            print(f"Task {t.task_id} | {t.title} | {t.status} | {t.priority} | Assigned: {assigned} | Hours: {t.time_logged}")
        print("-" * 90)

 

    def _get_project(self, project_id: int) -> Project:
        p = self.projects.get(project_id)
        if not p:
            raise ValueError("Project not found.")
        return p

    @staticmethod
    def _get_task(project: Project, task_id: int) -> Task:
        t = project.tasks.get(task_id)
        if not t:
            raise ValueError("Task not found in this project.")
        return t




class TrackerApp:
    def __init__(self) -> None:
        self.sys = ProjectManagerSystem()
        self._seed_data()

    def _seed_data(self) -> None:
   
        admin = AdminUser(1001, "Admin", "admin@example.com")
        mgr = ManagerUser(1002, "Manager", "manager@example.com")
        dev = DeveloperUser(1003, "Dev", "dev@example.com")
        self.sys.users[admin.user_id] = admin
        self.sys.users[mgr.user_id] = mgr
        self.sys.users[dev.user_id] = dev
        self.sys._next_user_id = 1004

    def run(self) -> None:
        while True:
            print("\nTask 6: Project / Task Tracker")
            print("1. Login")
            print("2. Logout")
            print("3. My Info")
            print("4. Role Menu")
            print("5. Exit")

            try:
                choice = read_choice("Choose: ", ["1", "2", "3", "4", "5"])
                if choice == "1":
                    self._login()
                elif choice == "2":
                    self.sys.logout()
                    print("Logged out.")
                elif choice == "3":
                    self._my_info()
                elif choice == "4":
                    self._role_menu()
                elif choice == "5":
                    print("Goodbye.")
                    return
            except ValueError as e:
                print(f"Error: {e}")

    def _login(self) -> None:
        self.sys.list_users()
        uid = read_int("Enter user ID to login: ")
        self.sys.login(uid)
        print(f"Logged in as: {self.sys.current_user}")

    def _my_info(self) -> None:
        if not self.sys.current_user:
            print("Not logged in.")
            return
        u = self.sys.current_user
        print("\nMy Info")
        print("-" * 70)
        print(u)
        print("Permissions:", ", ".join(sorted(u.get_permissions())))
        print("-" * 70)

    def _role_menu(self) -> None:
        if not self.sys.current_user:
            print("Please login first.")
            return

        role = self.sys.current_user.role
        if role == "ADMIN":
            self._admin_menu()
        elif role == "MANAGER":
            self._manager_menu()
        elif role == "DEVELOPER":
            self._developer_menu()
        else:
            print("Unknown role.")


    def _admin_menu(self) -> None:
        while True:
            print("\nAdmin Menu")
            print("1. Create User")
            print("2. Create Project")
            print("3. Add Member to Project")
            print("4. Create Task")
            print("5. Assign Task")
            print("6. Update Task Status")
            print("7. Log Task Time")
            print("8. Add Comment")
            print("9. Reports / Lists")
            print("10. Back")

            try:
                choice = read_choice("Choose: ", [str(i) for i in range(1, 11)])
                if choice == "1":
                    self._create_user()
                elif choice == "2":
                    self._create_project()
                elif choice == "3":
                    self._add_member()
                elif choice == "4":
                    self._create_task()
                elif choice == "5":
                    self._assign_task()
                elif choice == "6":
                    self._update_task_status()
                elif choice == "7":
                    self._log_time()
                elif choice == "8":
                    self._add_comment()
                elif choice == "9":
                    self._reports_menu()
                elif choice == "10":
                    return
            except ValueError as e:
                print(f"Error: {e}")


    def _manager_menu(self) -> None:
        while True:
            print("\nManager Menu")
            print("1. Create Project")
            print("2. Add Member to Project")
            print("3. Create Task")
            print("4. Assign Task")
            print("5. Update Task Status")
            print("6. Reports / Lists")
            print("7. Back")

            try:
                choice = read_choice("Choose: ", ["1", "2", "3", "4", "5", "6", "7"])
                if choice == "1":
                    self._create_project()
                elif choice == "2":
                    self._add_member()
                elif choice == "3":
                    self._create_task()
                elif choice == "4":
                    self._assign_task()
                elif choice == "5":
                    self._update_task_status()
                elif choice == "6":
                    self._reports_menu()
                elif choice == "7":
                    return
            except ValueError as e:
                print(f"Error: {e}")



    def _developer_menu(self) -> None:
        while True:
            print("\nDeveloper Menu")
            print("1. View Projects")
            print("2. View Tasks in Project")
            print("3. Update My Task Status")
            print("4. Log Hours on My Task")
            print("5. Add Comment")
            print("6. Reports / Lists")
            print("7. Back")

            try:
                choice = read_choice("Choose: ", ["1", "2", "3", "4", "5", "6", "7"])
                if choice == "1":
                    self.sys.list_projects()
                elif choice == "2":
                    self._list_tasks()
                elif choice == "3":
                    self._update_task_status()
                elif choice == "4":
                    self._log_time()
                elif choice == "5":
                    self._add_comment()
                elif choice == "6":
                    self._reports_menu()
                elif choice == "7":
                    return
            except ValueError as e:
                print(f"Error: {e}")

    

    def _create_user(self) -> None:
        role = read_choice("Role (ADMIN/MANAGER/DEVELOPER): ", ["ADMIN", "MANAGER", "DEVELOPER"])
        name = read_nonempty("Name: ")
        email = read_nonempty("Email: ")
        u = self.sys.create_user(role, name, email)
        print(f"User created: {u}")

    def _create_project(self) -> None:
        title = read_nonempty("Project title: ")
        desc = input("Description (optional): ").strip()
        self.sys.list_users()
        mid = read_int("Manager user ID: ")
        p = self.sys.create_project(title, desc, mid)
        print(f"Project created: ID {p.project_id}")

    def _add_member(self) -> None:
        self.sys.list_projects()
        pid = read_int("Project ID: ")
        self.sys.list_users()
        uid = read_int("User ID to add as member: ")
        self.sys.add_member_to_project(pid, uid)
        print("Member added to project.")

    def _create_task(self) -> None:
        self.sys.list_projects()
        pid = read_int("Project ID: ")
        title = read_nonempty("Task title: ")
        priority = read_choice("Priority (LOW/MEDIUM/HIGH/CRITICAL): ", ["LOW", "MEDIUM", "HIGH", "CRITICAL"])
        t = self.sys.create_task(pid, title, priority)
        print(f"Task created: Task ID {t.task_id}")

    def _assign_task(self) -> None:
        self.sys.list_projects()
        pid = read_int("Project ID: ")
        self.sys.list_project_tasks(pid)
        tid = read_int("Task ID: ")
        self.sys.list_users()
        uid = read_int("Assign to User ID: ")
        self.sys.assign_task(pid, tid, uid)
        print("Task assigned.")

    def _update_task_status(self) -> None:
        self.sys.list_projects()
        pid = read_int("Project ID: ")
        self.sys.list_project_tasks(pid)
        tid = read_int("Task ID: ")
        status = read_choice("New status (TODO/IN_PROGRESS/DONE/BLOCKED): ", ["TODO", "IN_PROGRESS", "DONE", "BLOCKED"])
        self.sys.update_task_status(pid, tid, status)
        print("Task status updated.")

    def _log_time(self) -> None:
        self.sys.list_projects()
        pid = read_int("Project ID: ")
        self.sys.list_project_tasks(pid)
        tid = read_int("Task ID: ")
        hours = float(read_nonempty("Hours to log (e.g., 1.5): "))
        self.sys.log_task_time(pid, tid, hours)
        print("Time logged.")

    def _add_comment(self) -> None:
        self.sys.list_projects()
        pid = read_int("Project ID: ")
        self.sys.list_project_tasks(pid)
        tid = read_int("Task ID: ")
        content = read_nonempty("Comment: ")
        c = self.sys.add_task_comment(pid, tid, content)
        print(f"Comment added (ID {c.comment_id}).")

    def _list_tasks(self) -> None:
        self.sys.list_projects()
        pid = read_int("Project ID: ")
        self.sys.list_project_tasks(pid)

    def _reports_menu(self) -> None:
        while True:
            print("\nReports / Lists")
            print("1. List Users")
            print("2. List Projects")
            print("3. List Tasks in Project")
            print("4. Project Report")
            print("5. Back")

            choice = read_choice("Choose: ", ["1", "2", "3", "4", "5"])
            if choice == "1":
                self.sys.list_users()
            elif choice == "2":
                self.sys.list_projects()
            elif choice == "3":
                self._list_tasks()
            elif choice == "4":
                self.sys.list_projects()
                pid = read_int("Project ID: ")
                print(self.sys.project_report(pid))
            elif choice == "5":
                return


if __name__ == "__main__":
    TrackerApp().run()
