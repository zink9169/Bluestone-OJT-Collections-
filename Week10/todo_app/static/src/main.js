/** @odoo-module **/
import { registry } from "@web/core/registry";
import { TodoApp } from "./components/todo_app";

registry.category("actions").add("my_todo_app.todo_action", TodoApp);