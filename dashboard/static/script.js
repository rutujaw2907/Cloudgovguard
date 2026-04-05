/**
 * CLOUDGOVGUARD - CSPM Core Logic
 */

// 1. MOCK DATA (Simulated Backend Response)
const mockData = {
    summary: {
        totalResources: 1248,
        totalViolations: 86,
        criticalIssues: 12,
        securityScore: 74,
        scoreTrend: -2,
        resourceTrend: 15
    },
    severityData: {
        labels: ['Critical', 'High', 'Medium', 'Low'],
        values: [12, 24, 32, 18]
    },
    resourceData: {
        labels: ['S3 Storage', 'EC2 Instances', 'IAM Roles', 'RDS Databases', 'Lambda'],
        values: [450, 320, 280, 100, 98]
    },
    policyData: {
        labels: ['Encryption', 'Network Config', 'Identity Access', 'Logging'],
        values: [30, 25, 35, 10]
    },
    violations: [
        { policy: "S3 Bucket Publicly Accessible", resource: "prod-customer-data", severity: "critical", desc: "Bucket allows public read access", fix: "Disable ACL public access" },
        { policy: "MFA Not Enabled", resource: "admin-user-01", severity: "high", desc: "Root account missing MFA", fix: "Enable hardware/virtual MFA" },
        { policy: "Unused Security Group", resource: "web-server-sg", severity: "low", desc: "No resources attached to SG", fix: "Delete security group" },
        { policy: "Insecure SSH Port", resource: "dev-jump-box", severity: "medium", desc: "Port 22 open to 0.0.0.0/0", fix: "Restrict to known IP range" },
        { policy: "DB Snapshot Unencrypted", resource: "billing-db-snapshot", severity: "high", desc: "Snapshot lacks KMS encryption", fix: "Enable AES-256 encryption" }
    ],
    attackPath: [
        { label: "Public SSH Port", type: "entry" },
        { label: "EC2 Instance", type: "asset" },
        { label: "Privilege Escalation", type: "action" },
        { label: "Cloud Admin Access", type: "compromise" }
    ]
};

// 2. CORE INITIALIZATION
document.addEventListener('DOMContentLoaded', () => {
    // Simulate loading delay for "Real SaaS" feel
    setTimeout(() => {
        initDashboard();
    }, 800);
});

async function initDashboard() {
    renderKPIs(mockData.summary);
    renderCharts(mockData);
    renderTable(mockData.violations);
    renderAttackPath(mockData.attackPath);
    setupInteractions();
}

// 3. UI RENDERING FUNCTIONS
function renderKPIs(data) {
    const container = document.getElementById('kpi-container');
    container.innerHTML = `
        <div class="card">
            <p class="card-title">Total Resources</p>
            <p class="card-value">${data.totalResources.toLocaleString()}</p>
            <p class="trend down">↑ ${data.resourceTrend}% from last month</p>
        </div>
        <div class="card">
            <p class="card-title">Total Violations</p>
            <p class="card-value">${data.totalViolations}</p>
            <p class="trend up">↑ 4% trend</p>
        </div>
        <div class="card">
            <p class="card-title">Critical Issues</p>
            <p class="card-value" style="color: var(--critical)">${data.criticalIssues}</p>
            <p class="trend up">High Priority</p>
        </div>
        <div class="card" style="border-left: 4px solid var(--accent)">
            <p class="card-title">Security Score</p>
            <p class="card-value">${data.securityScore}%</p>
            <p class="trend ${data.scoreTrend < 0 ? 'up' : 'down'}">
                ${data.scoreTrend}% vs yesterday
            </p>
        </div>
    `;
}

function renderCharts(data) {
    // Shared Chart Options
    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { labels: { color: '#94a3b8', font: { family: 'Inter' } } }
        }
    };

    // Severity Bar Chart
    new Chart(document.getElementById('severityBarChart'), {
        type: 'bar',
        data: {
            labels: data.severityData.labels,
            datasets: [{
                label: 'Violations',
                data: data.severityData.values,
                backgroundColor: ['#ef4444', '#f97316', '#eab308', '#22c55e'],
                borderRadius: 6
            }]
        },
        options: {
            ...chartOptions,
            scales: {
                y: { grid: { color: '#334155' }, ticks: { color: '#94a3b8' } },
                x: { grid: { display: false }, ticks: { color: '#94a3b8' } }
            }
        }
    });

    // Resource Doughnut
    new Chart(document.getElementById('resourceDoughnutChart'), {
        type: 'doughnut',
        data: {
            labels: data.resourceData.labels,
            datasets: [{
                data: data.resourceData.values,
                backgroundColor: ['#38bdf8', '#818cf8', '#c084fc', '#fb7185', '#34d399'],
                borderWidth: 0
            }]
        },
        options: chartOptions
    });

    // Policy Pie
    new Chart(document.getElementById('policyPieChart'), {
        type: 'pie',
        data: {
            labels: data.policyData.labels,
            datasets: [{
                data: data.policyData.values,
                backgroundColor: ['#0ea5e9', '#6366f1', '#a855f7', '#f43f5e'],
                borderWidth: 0
            }]
        },
        options: chartOptions
    });
}

function renderTable(violations) {
    const tbody = document.getElementById('violations-body');
    tbody.innerHTML = violations.map(v => `
        <tr>
            <td style="font-weight: 600;">${v.policy}</td>
            <td style="color: var(--accent);">${v.resource}</td>
            <td><span class="badge ${v.severity}">${v.severity.toUpperCase()}</span></td>
            <td style="color: var(--text-muted);">${v.desc}</td>
            <td><code style="background: #0f172a; padding: 4px; border-radius: 4px;">${v.fix}</code></td>
        </tr>
    `).join('');
}

function renderAttackPath(path) {
    const container = document.getElementById('attack-path-flow');
    container.innerHTML = path.map((node, index) => `
        <div class="node">
            <small style="color: var(--accent); display: block; margin-bottom: 4px;">STEP ${index + 1}</small>
            <strong>${node.label}</strong>
        </div>
        ${index < path.length - 1 ? '<div class="arrow">➞</div>' : ''}
    `).join('');
}

function setupInteractions() {
    // Simple Navigation active state toggle
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            navItems.forEach(n => n.classList.remove('active'));
            item.classList.add('active');
            document.getElementById('page-title').innerText = item.dataset.page;
        });
    });
}