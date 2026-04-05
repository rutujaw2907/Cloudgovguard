const App = {
    charts: {},
    data: null,

    init() {
        this.bindEvents();
        this.initCharts();
        this.load();
    },

    bindEvents() {
        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', (e) => {
                const view = e.currentTarget.dataset.view;
                this.switchView(view);
            });
        });

        document.getElementById('runScanBtn').onclick = () => this.load();
        document.getElementById('closePanel').onclick = () => document.getElementById('sidePanel').classList.remove('active');
    },

    async load() {
        try {
            const res = await fetch('/api/dashboard');
            this.data = await res.json();
            this.render();
        } catch (e) { console.error("Link Terminated", e); }
    },

    switchView(viewId) {
        document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
        document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
        
        document.getElementById(`view-${viewId}`).classList.add('active');
        document.querySelector(`[data-view="${viewId}"]`).classList.add('active');
        
        // Update Titles
        const titles = { 
            dashboard: "Executive Overview", 
            remediation: "Threat Remediation", 
            inventory: "Asset Inventory", 
            compliance: "Compliance Reports" 
        };
        document.getElementById('main-title').innerText = titles[viewId];
    },

    render() {
        const d = this.data;
        document.getElementById('val-assets').innerText = d.resources.total;
        document.getElementById('val-violations').innerText = d.violations.length;
        document.getElementById('val-critical').innerText = d.score.critical;
        document.getElementById('val-score').innerText = d.score.score + "%";

        // Render Table
        document.getElementById('violationsBody').innerHTML = d.violations.map(v => `
            <tr onclick="App.showDetails('${v.policy_name}')">
                <td><strong>${v.resource_name}</strong></td>
                <td>${v.policy_name}</td>
                <td style="color:var(--${v.severity === 'CRITICAL' ? 'red' : 'orange'})">${v.severity}</td>
                <td><button style="background:var(--glass); border:1px solid var(--glass-border); color:white; padding:5px 10px; border-radius:5px; cursor:pointer;">Investigate</button></td>
            </tr>`).join('');

        // Render Inventory
        document.getElementById('inventoryBody').innerHTML = Array.from({length: d.resources.total}).map((_, i) => `
            <div class="asset-card"><i class="fas fa-cube" style="color:var(--accent)"></i><h4>Asset-${i+1}</h4><p style="font-size:0.7rem; color:var(--text-secondary)">ID: xxxx-${i+1}</p></div>
        `).join('');

        // Render Compliance
        const frameworks = ['CIS Benchmark', 'NIST 800-53', 'SOC2 Type II', 'HIPAA'];
        document.getElementById('complianceBody').innerHTML = frameworks.map(f => `
            <div class="compliance-item"><span>${f}</span><span style="color:var(--green)">92% PASS</span></div>
        `).join('');

        // Update Chart
        this.charts.sev.data.datasets[0].data = [d.score.critical, d.score.high, d.score.medium, d.score.low];
        this.charts.sev.update();
    },

    showDetails(policy) {
        const v = this.data.violations.find(x => x.policy_name === policy);
        document.getElementById('panelBody').innerHTML = `
            <h2>${v.policy_name}</h2>
            <p style="color:var(--text-secondary); margin-top:10px;">Resource: ${v.resource_name}</p>
            <div style="margin-top:30px; background:var(--glass); padding:20px; border-radius:15px; border-left:4px solid var(--red);">
                <h4 style="color:var(--red)">REASON</h4><p>${v.reason}</p>
            </div>
            <div style="margin-top:20px; background:var(--glass); padding:20px; border-radius:15px; border-left:4px solid var(--green);">
                <h4 style="color:var(--green)">REMEDIATION</h4><p>${v.remediation}</p>
            </div>
        `;
        document.getElementById('sidePanel').classList.add('active');
    },

    initCharts() {
        this.charts.sev = new Chart(document.getElementById('severityChart'), {
            type: 'doughnut',
            data: {
                labels: ['Crit', 'High', 'Med', 'Low'],
                datasets: [{
                    data: [0,0,0,0],
                    backgroundColor: ['#f43f5e', '#fb923c', '#fbbf24', '#10b981'],
                    borderWidth: 0
                }]
            },
            options: {
                cutout: '80%', maintainAspectRatio: false,
                plugins: { legend: { position: 'bottom', labels: { color: '#94a3b8', usePointStyle: true, padding: 25 } } }
            }
        });
    }
};

document.addEventListener('DOMContentLoaded', () => App.init());