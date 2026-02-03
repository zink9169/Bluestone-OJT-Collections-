/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component, useState } from "@odoo/owl";

export class TodoApp extends Component {
    setup() {
        this.state = useState({
            newTask: "",
            todos: [],
        });
    }

    addTodo() {
        if (!this.state.newTask.trim()) return;
        this.state.todos.push({
            id: Date.now(),
            text: this.state.newTask,
            done: false,
        });
        this.state.newTask = "";
    }

    toggleTodo(todo) {
        todo.done = !todo.done;
    }

    deleteTodo(todoId) {
        this.state.todos = this.state.todos.filter(t => t.id !== todoId);
    }
}

TodoApp.template = "todo_owl.TodoApp";

// 🔑 THE FIX: This key must match the 'tag' in your XML exactly.
registry.category("actions").add("todo_owl.todo_action", TodoApp);