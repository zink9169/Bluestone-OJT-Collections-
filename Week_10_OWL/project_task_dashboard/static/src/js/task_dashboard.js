/** @odoo-module **/

import {Component, useState, onWillStart} from "@odoo/owl";
import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";

export class TaskDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.actionService = useService("action");
        this.dialogService = useService("dialog");

        this.state = useState({
            tasks: [],
            sections: [],
            search: "",
            mode: "all",
            openStateTaskId: null,

        });

        // Bind methods to preserve 'this' context
        this.openTask = this.openTask.bind(this);
        this.openProjectTasks = this.openProjectTasks.bind(this);
        this.createNewTask = this.createNewTask.bind(this);
        this.searchTasks = this.searchTasks.bind(this);
        this.refreshDashboard = this.refreshDashboard.bind(this);
        this.setMode = this.setMode.bind(this);

        this.changeTaskState = this.changeTaskState.bind(this);
        this.toggleStateMenu = this.toggleStateMenu.bind(this);
        this.openSectionTasks = this.openSectionTasks.bind(this);


        onWillStart(async () => {
            await this.loadTasks();
            this.buildSections();
        });
    }

    async refreshDashboard() {
        this.state.mode = "all"; // reset filter
        await this.loadTasks();
        this.buildSections();
    }


    async createNewTask() {
        // Open the task creation form
        this.actionService.doAction({
            type: "ir.actions.act_window",
            name: "New Task",
            res_model: "project.task",
            views: [[false, "form"]],
            target: "current",
            context: {
                'default_project_id': this.props.project_id || false,
                'default_stage_id': false
            }
        }).then(() => {
            // Refresh after creating new task
            setTimeout(() => this.refreshDashboard(), 1000);
        });
    }

    async changeTaskState(taskId, newState) {
        try {
            await this.orm.write("project.task", [taskId], {
                state: newState,
            });

            this.state.openStateTaskId = null;
            await this.refreshDashboard();
        } catch (err) {
            console.error("Failed to change task state", err);
        }
    }


    async loadTasks() {
        try {
            this.state.tasks = await this.orm.searchRead(
                "project.task",
                [],
                ["name", "date_deadline", "stage_id", "project_id", "is_urgent", "state"]
            );


            // DEBUG: Log to see what's loaded
            console.log("=== LOADED TASKS ===");
            this.state.tasks.forEach(task => {
                console.log(`Task: ${task}`);
            });

        } catch (error) {
            console.error("Error loading tasks:", error);
            this.state.tasks = [];
        }
    }

    getStateLabel(state) {
        console.log("getStateLabel called with state:", state); // Add this

        switch (state) {
            case "01_in_progress":
                return "In Progress";
            case "02_changes_requested":
                return "Change Request";
            case "1_done":
                return "Done";
            case "04_waiting_normal":
                return "New"; // Add this
            default:
                console.log("Unknown state:", state);
                return "New";
        }
    }

    getStateClass(state) {
        switch (state) {
            case "01_in_progress":
                return "state-progress";
            case "02_changes_requested":
                return "state-change";
            case "1_done":
                return "state-done";
            default:
                return "state-new";
        }
    }

    toggleStateMenu(taskId) {
        if (!taskId) return;
        this.state.openStateTaskId =
            this.state.openStateTaskId === taskId ? null : taskId;
    }


    openTask(taskId) {
        if (!taskId) return;

        // Open the task form view
        this.actionService.doAction({
            type: "ir.actions.act_window",
            name: "Task",
            res_model: "project.task",
            res_id: taskId,
            views: [[false, "form"]],
            target: "current"
        }).then(() => {
            // Refresh after editing task
            setTimeout(() => this.refreshDashboard(), 1000);
        });
    }

    // Helper function to determine date status
    getDateStatus(dateDeadline) {
        if (!dateDeadline) return 'far';

        const today = new Date();
        today.setHours(0, 0, 0, 0);

        const deadline = new Date(dateDeadline);
        deadline.setHours(0, 0, 0, 0);

        const diffTime = deadline - today;
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

        if (diffDays < 0) {
            return 'overdue';
        } else if (diffDays <= 5) {
            return 'near';
        } else {
            return 'far';
        }
    }

    // Helper function to get CSS class based on date status
    getDateClass(dateDeadline) {
        const status = this.getDateStatus(dateDeadline);
        return `deadline-${status}`;
    }

// Method to open Task Dashboard for a specific project
    openProjectTasks(projectId) {
        if (!projectId) return;

        this.actionService.doAction({
            type: "ir.actions.client",
            tag: "project_task_dashboard.action",
            params: {
                project_id: projectId,
            },
        });
    }

    openSectionTasks(sectionKey) {
        let domain = [];

        switch (sectionKey) {
            case "new":
                domain = [
                    "|",
                    ["state", "=", "04_waiting_normal"],
                    ["state", "=", "02_changes_requested"],
                ];
                break;

            case "progress":
                domain = [["state", "=", "01_in_progress"]];
                break;

            case "done":
                domain = [["state", "=", "1_done"]];
                break;

            case "overdue":
                domain = [
                    ["state", "!=", "1_done"],
                    ["date_deadline", "<", new Date().toISOString().split("T")[0]],
                ];
                break;

            case "urgent":
                domain = [
                    ["is_urgent", "=", true],
                    ["state", "!=", "1_done"],
                ];
                break;

            default:
                domain = [];
        }

        this.actionService.doAction({
            type: "ir.actions.act_window",
            name: "Tasks",
            res_model: "project.task",
            views: [
                [false, "list"],
                [false, "form"],
            ],
            domain: domain,
            context: {
                search_default_my_tasks: 0,
                default_project_id: false,
                active_id: false,
                active_ids: [],
            },
            target: "current",
        });
    }


    buildSections() {
        const today = new Date();
        today.setHours(0, 0, 0, 0);

        const daysDiff = d => {
            if (!d) return 999;
            const deadline = new Date(d);
            deadline.setHours(0, 0, 0, 0);
            return (deadline - today) / (1000 * 3600 * 24);
        };

        const limitTasks = (tasks) => {
            return this.state.mode === "all" ? tasks.slice(0, 2) : tasks;
        };


        const tasks = this.state.tasks || [];
        const mode = this.state.mode;

        const allSections = {
            new: {
                key: "new",
                title: "New Tasks",
                tasks: limitTasks(
                    tasks.filter(t =>
                        t &&
                        (t.state === "04_waiting_normal" ||
                            t.state === "02_changes_requested")
                    )
                ),
            },
            progress: {
                key: "progress",
                title: "In Progress",
                tasks: limitTasks(
                    tasks.filter(t => t && t.state === "01_in_progress")
                ),
            },
            done: {
                key: "done",
                title: "Done",
                tasks: limitTasks(
                    tasks.filter(t => t && t.state === "1_done")
                ),
            },
            overdue: {
                key: "overdue",
                title: "Overdue",
                tasks: limitTasks(
                    tasks.filter(t =>
                        t &&
                        t.state !== "1_done" &&
                        daysDiff(t.date_deadline) < 0
                    )
                ),
            },
            due: {
                key: "due",
                title: "Due Soon",
                tasks: limitTasks(
                    tasks.filter(t =>
                        t &&
                        t.state !== "1_done" &&
                        daysDiff(t.date_deadline) <= 5 &&
                        daysDiff(t.date_deadline) > 0
                    )
                ),
            },
            urgent: {
                key: "urgent",
                title: "Urgent Request",
                tasks: limitTasks(
                    tasks.filter(t => t && t.is_urgent && t.state !== "1_done")
                ),
            },
        };

        if (mode === "all") {
            this.state.sections = Object.values(allSections);
        } else {
            this.state.sections = [allSections[mode]];
        }
    }


    searchTasks(ev) {
        const text = ev.target.value.toLowerCase();
        this.state.search = text;

        this.buildSections();

        if (text) {
            this.state.sections.forEach(sec => {
                sec.tasks = sec.tasks.filter(t =>
                    t && t.name && t.name.toLowerCase().includes(text)
                );
            });
        }
    }

    setMode(mode) {
        this.state.mode = mode;
        this.buildSections();
    }

}

TaskDashboard.template = "project_task_dashboard.TaskDashboard";
TaskDashboard.props = {
    project_id: {type: Number, optional: true},
};
registry.category("actions").add("project_task_dashboard.action", TaskDashboard);