/** @odoo-module **/

import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "todo_owl.TodoList";
    static components = { TodoItem };

    setup() {
        this.todos = useState([
            { id: 1, description: "First task", isCompleted: false },
            { id: 2, description: "Second task", isCompleted: true }
        ]);
        this.nextId = 3;

        this.inputRef = useRef("todoInput");
        onMounted(() => {
            this.inputRef.el?.focus();
        });
    }

    addTodo(ev) {
        if (ev.key === "Enter") {
            const description = ev.target.value.trim();
            if (description) {
                this.todos.push({
                    id: this.nextId++,
                    description,
                    isCompleted: false
                });
                ev.target.value = "";
            }
        }
    }

    toggleTodo(todoId) {
        const todo = this.todos.find(t => t.id === todoId);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    deleteTodo(todoId) {
        const index = this.todos.findIndex(t => t.id === todoId);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }
}
