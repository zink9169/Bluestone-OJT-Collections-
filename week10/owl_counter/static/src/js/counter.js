/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";

class CounterApp extends Component {
    setup() {
        this.state = useState({
            counter1: 0,
            counter2: 0,
        });
    }

    inc1() { this.state.counter1++; }
    dec1() { this.state.counter1--; }
    reset1() { this.state.counter1 = 0; }

    inc2() { this.state.counter2++; }
    dec2() { this.state.counter2--; }
    reset2() { this.state.counter2 = 0; }

    get total() {
        return this.state.counter1 + this.state.counter2;
    }
}

CounterApp.template = "owl_counter.CounterTemplate";

/* ✅ Register Client Action */
registry.category("actions").add("owl_counter.counter_action", CounterApp);
