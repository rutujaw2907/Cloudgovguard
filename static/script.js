console.log("SYSTEM READY");

window.onload = loadDashboard;

async function loadDashboard() {
    try {
        const [res1, res2, res3] = await Promise.all([
            fetch("/api/resources"),
            fetch("/api/violations"),
            fetch("/api/score")
        ]);

        const resources = await res1.json();
        const violations = await res2.json();
        const score = await res3.json();

        // -------- KPIs --------
        document.getElementById("kpi-assets").innerText = resources.total_resources;
        document.getElementById("kpi-violations").innerText = violations.length;
        document.getElementById("kpi-critical").innerText = score.critical;
        document.getElementById("kpi-score").innerText = score.score + "%";

        // -------- TABLE --------
        const tbody = document.querySelector("#violationsTable tbody");

        tbody.innerHTML = violations.map(v => `
            <tr>
                <td>${v.policy_name}</td>
                <td>${v.resource_name}</td>
                <td>${v.severity}</td>
                <td>${v.reason}</td>
            </tr>
        `).join("");

    } catch (err) {
        console.error("ERROR:", err);
    }
}