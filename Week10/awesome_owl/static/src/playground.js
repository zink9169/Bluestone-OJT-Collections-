import { Component, useState } from "@odoo/owl";
import { Counter } from "./components/counter/counter";

export class Playground extends Component {
    static template = "awesome_owl.Playground";
    static components = { Counter };

    setup() {
        this.state = useState({ sum: 2 });
    }

    updateSum(val) {
        this.state.sum += val;
    }
}