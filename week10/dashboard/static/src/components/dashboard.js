/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, onWillStart, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class ProjectDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.action = useService("action");

        this.state = useState({
            data: { sections: {}, dates: {} },
            loading: true,
        });

        onWillStart(async () => {
            await this.loadData();
        });
    }

    async loadData() {
        this.state.loading = true;
        const result = await this.orm.call(
            "project.task",
            "get_dashboard_data",
            []
        );
        this.state.data = result;
        this.state.loading = false;
    }

    // 🔹 OPEN LIST VIEW
    async openSection(key) {
        const section = this.state.data.sections[key];

        await this.action.doAction({
            type: "ir.actions.act_window",
            name: section.title,
            res_model: "project.task",
            views: [
                [false, "list"],
                [false, "form"],
            ],
            domain: section.domain || [], // now ALWAYS exists
            target: "current",
        });
    }

    // 🔹 OPEN FORM VIEW
    async openTask(taskId) {
        await this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "project.task",
            res_id: taskId,
            views: [[false, "form"]],
            target: "current",
        });
    }
}

ProjectDashboard.template = "project_dashboard.DashboardMain";
registry.category("actions").add("project_dashboard_tag", ProjectDashboard);
