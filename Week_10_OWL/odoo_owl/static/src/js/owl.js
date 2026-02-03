/** @odoo-module **/

import {registry} from "@web/core/registry";
import {Component, useState} from "@odoo/owl";

export class Owl extends Component {
    setup() {
        this.state = useState({
            count: 0,
            value: 0,
            result: 0,
            newTask: "",
            tasks: [],
            editIndex: null,
        });
    }

    addTask() {
        if (!this.state.newTask.trim()) return;

        if (this.state.editIndex !== null) {
            this.state.tasks[this.state.editIndex].text = this.state.newTask;
            this.state.editIndex = null;
        } else {
            this.state.tasks.push({
                id: Date.now(),
                text: this.state.newTask,
                done: false,
            });
        }

        this.state.newTask = "";
    }

    editTask(task) {
        this.state.newTask = task.text;
        this.state.editIndex = this.state.tasks.indexOf(task);
    }

    deleteTask(task) {
        const index = this.state.tasks.indexOf(task);
        if (index !== -1) {
            this.state.tasks.splice(index, 1);
        }
    }

    toggleDone(task) {
        if (!task) return;
        task.done = !task.done;
    }


    onKeydown(ev) {
        if (ev.key === "Enter") {
            this.addTask();
        }
    }

    increment() {
        this.state.count++;
        this.total()
    }

    decrement() {
        this.state.count--;
        this.total()
    }

    add() {
        this.state.value++;
        this.total()
    }

    minus() {
        this.state.value--;
        this.total()
    }

    total() {
        this.state.result = this.state.count + this.state.value
    }


}

Owl.template = "odoo_owl.Template";

registry.category("actions").add("owl.main", Owl);