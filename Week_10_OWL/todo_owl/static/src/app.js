/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";
import { TodoList } from "./components/todo_list";

class TodoApp extends Component {
    static template = "todo_owl.App";
    static components = { TodoList };
}

// REQUIRED for ir.actions.client
registry.category("actions").add("todo_owl.app", TodoApp);
