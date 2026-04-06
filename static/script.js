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

        // KPI values
        document.getElementById("val-assets").innerText = resources.total_resources ?? 0;
        document.getElementById("val-violations").innerText = violations.length ?? 0;
        document.getElementById("val-critical").innerText = score.critical ?? 0;
        document.getElementById("val-score").innerText = (score.score ?? 0) + "%";

        // Table
        const tbody = document.getElementById("violationsBody");

        tbody.innerHTML = violations.map(v => `
            <tr>
                <td>${v.resource_name ?? "-"}</td>
                <td>${v.policy_name ?? "-"}</td>
                <td>${v.severity ?? "-"}</td>
                <td>${v.reason ?? "-"}</td>
            </tr>
        `).join("");

    } catch (err) {
        console.error("ERROR:", err);
    }
}