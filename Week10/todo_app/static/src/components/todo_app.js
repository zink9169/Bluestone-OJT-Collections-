/** @odoo-module **/
import { Component, useState } from "@odoo/owl";

export class TodoApp extends Component {
    static template = "my_todo_app.TodoApp";

    setup() {
        this.state = useState({
            newTask: "",
            tasks: []
        });
    }

    addTask() {
        if (this.state.newTask.trim()) {
            this.state.tasks.push({
                id: Date.now(),
                text: this.state.newTask,
                isCompleted: false
            });
            this.state.newTask = "";
        }
    }

    onInputKeydown(ev) {
        if (ev.key === "Enter") {
            this.addTask();
        }
    }

    toggleTask(taskId) {
        const task = this.state.tasks.find(t => t.id === taskId);
        if (task) {
            task.isCompleted = !task.isCompleted;
        }
    }

    deleteTask(taskId) {
        this.state.tasks = this.state.tasks.filter(t => t.id !== taskId);
    }
}