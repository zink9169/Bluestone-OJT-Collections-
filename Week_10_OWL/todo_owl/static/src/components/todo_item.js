/** @odoo-module **/

import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "todo_owl.TodoItem";

    static props = {
        todo: Object,
        toggleState: { type: Function, optional: true },
        removeTodo: { type: Function, optional: true }
    };
}
