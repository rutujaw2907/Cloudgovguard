/* ===== CloudGovGuard — CSPM Dashboard Logic ===== */

// ── Mock Data (simulates /api/dashboard response) ──
const DATA = {
  score: 72,
  resources: 1247,
  violations: [
    { id:"v1", policy_name:"S3 Bucket Public Access", resource_name:"arn:aws:s3:::prod-customer-data", severity:"critical", reason:"S3 bucket has public read access enabled, exposing sensitive customer PII data to the internet.", remediation:"Disable public access by enabling S3 Block Public Access settings and reviewing bucket ACL policies.", service:"S3", region:"us-east-1", detected_at:"2026-04-05T08:23:00Z" },
    { id:"v2", policy_name:"EC2 SSH Open to World", resource_name:"i-0a3b7c9d2e1f4g5h6", severity:"critical", reason:"Security group sg-0abc123 allows inbound SSH (port 22) from 0.0.0.0/0, enabling brute-force attacks.", remediation:"Restrict SSH access to specific CIDR ranges or use AWS Systems Manager Session Manager for secure access.", service:"EC2", region:"us-west-2", detected_at:"2026-04-05T06:15:00Z" },
    { id:"v3", policy_name:"IAM Root Account MFA", resource_name:"arn:aws:iam::123456789012:root", severity:"critical", reason:"Root account does not have multi-factor authentication enabled, risking full account takeover.", remediation:"Enable hardware or virtual MFA device for the root account immediately via IAM console.", service:"IAM", region:"global", detected_at:"2026-04-04T22:00:00Z" },
    { id:"v4", policy_name:"RDS Encryption at Rest", resource_name:"db-prod-analytics-01", severity:"high", reason:"RDS instance is not using encryption at rest, violating data protection compliance requirements.", remediation:"Create an encrypted snapshot, then restore the database from the encrypted snapshot.", service:"RDS", region:"eu-west-1", detected_at:"2026-04-05T03:45:00Z" },
    { id:"v5", policy_name:"CloudTrail Disabled", resource_name:"trail-prod-audit", severity:"high", reason:"CloudTrail logging is disabled in us-east-2 region, creating blind spots in the audit trail.", remediation:"Enable CloudTrail with multi-region logging and configure log file delivery to a centralized S3 bucket.", service:"CloudTrail", region:"us-east-2", detected_at:"2026-04-05T01:12:00Z" },
    { id:"v6", policy_name:"Lambda Env Secrets Exposure", resource_name:"fn-payment-processor", severity:"high", reason:"Lambda function has hardcoded API keys and database credentials in environment variables.", remediation:"Migrate secrets to AWS Secrets Manager and update Lambda to retrieve secrets at runtime.", service:"Lambda", region:"us-east-1", detected_at:"2026-04-04T18:30:00Z" },
    { id:"v7", policy_name:"EBS Volume Unencrypted", resource_name:"vol-0f1e2d3c4b5a6789", severity:"medium", reason:"EBS volume attached to production workload is not encrypted, risking data exposure if snapshot is shared.", remediation:"Create an encrypted copy of the volume, detach the unencrypted volume, and attach the encrypted one.", service:"EC2", region:"ap-southeast-1", detected_at:"2026-04-05T09:00:00Z" },
    { id:"v8", policy_name:"VPC Flow Logs Disabled", resource_name:"vpc-0a1b2c3d4e5f", severity:"medium", reason:"VPC flow logs are not enabled, preventing network traffic analysis for incident response.", remediation:"Enable VPC Flow Logs and configure delivery to CloudWatch Logs or S3 for retention.", service:"VPC", region:"us-east-1", detected_at:"2026-04-04T14:20:00Z" },
    { id:"v9", policy_name:"S3 Versioning Disabled", resource_name:"arn:aws:s3:::staging-backups", severity:"low", reason:"S3 bucket versioning is disabled, preventing recovery from accidental deletions.", remediation:"Enable versioning on the S3 bucket and configure lifecycle policies for version management.", service:"S3", region:"us-west-1", detected_at:"2026-04-05T07:55:00Z" },
    { id:"v10", policy_name:"CloudWatch Alarm Missing", resource_name:"alarm-cpu-prod-web", severity:"low", reason:"No CloudWatch alarms configured for CPU utilization on production web tier instances.", remediation:"Create CloudWatch alarms for key metrics (CPU, memory, disk) with appropriate SNS notification topics.", service:"CloudWatch", region:"us-east-1", detected_at:"2026-04-03T11:00:00Z" },
  ],
  assets: [
    { id:"a1", name:"prod-web-server-01", type:"EC2 Instance", region:"us-east-1", status:"non-compliant", risk_score:87 },
    { id:"a2", name:"prod-customer-data", type:"S3 Bucket", region:"us-east-1", status:"non-compliant", risk_score:95 },
    { id:"a3", name:"db-prod-analytics-01", type:"RDS Instance", region:"eu-west-1", status:"non-compliant", risk_score:72 },
    { id:"a4", name:"fn-payment-processor", type:"Lambda Function", region:"us-east-1", status:"non-compliant", risk_score:68 },
    { id:"a5", name:"vpc-production", type:"VPC", region:"us-east-1", status:"compliant", risk_score:15 },
    { id:"a6", name:"cdn-global-dist", type:"CloudFront", region:"global", status:"compliant", risk_score:8 },
    { id:"a7", name:"k8s-prod-cluster", type:"EKS Cluster", region:"us-west-2", status:"compliant", risk_score:22 },
    { id:"a8", name:"redis-cache-prod", type:"ElastiCache", region:"us-east-1", status:"compliant", risk_score:12 },
    { id:"a9", name:"sqs-order-queue", type:"SQS Queue", region:"us-east-1", status:"compliant", risk_score:5 },
    { id:"a10", name:"dynamodb-sessions", type:"DynamoDB", region:"us-east-1", status:"compliant", risk_score:18 },
    { id:"a11", name:"staging-backups", type:"S3 Bucket", region:"us-west-1", status:"non-compliant", risk_score:35 },
    { id:"a12", name:"ecr-prod-images", type:"ECR Repository", region:"us-east-1", status:"compliant", risk_score:10 },
  ],
  compliance: [
    { id:"c1", name:"CIS AWS Foundations Benchmark v1.5", shortName:"CIS", passed:42, failed:8, total:50 },
    { id:"c2", name:"NIST 800-53 Rev 5", shortName:"NIST", passed:156, failed:24, total:180 },
    { id:"c3", name:"SOC 2 Type II", shortName:"SOC2", passed:89, failed:11, total:100 },
    { id:"c4", name:"HIPAA Security Rule", shortName:"HIPAA", passed:34, failed:6, total:40 },
    { id:"c5", name:"PCI DSS v4.0", shortName:"PCI", passed:210, failed:15, total:225 },
    { id:"c6", name:"ISO 27001:2022", shortName:"ISO", passed:108, failed:6, total:114 },
  ],
  trend: [
    { date:"Mar 1", critical:5, high:12, medium:18, low:8 },
    { date:"Mar 8", critical:4, high:10, medium:20, low:9 },
    { date:"Mar 15", critical:6, high:14, medium:17, low:7 },
    { date:"Mar 22", critical:3, high:11, medium:15, low:10 },
    { date:"Mar 29", critical:4, high:9, medium:19, low:6 },
    { date:"Apr 5", critical:3, high:8, medium:14, low:7 },
  ],
};

const COLORS = { critical:"#f43f5e", high:"#fb923c", medium:"#fbbf24", low:"#10b981" };

const ASSET_ICONS = {
  "EC2 Instance":"fa-server", "S3 Bucket":"fa-database", "RDS Instance":"fa-database",
  "Lambda Function":"fa-cloud", "VPC":"fa-globe", "CloudFront":"fa-globe",
  "EKS Cluster":"fa-layer-group", "ElastiCache":"fa-hard-drive", "SQS Queue":"fa-layer-group",
  "DynamoDB":"fa-database", "ECR Repository":"fa-hard-drive",
};

// ── Chart instances ──
let severityChart = null;
let trendChart = null;

// ── Navigation ──
document.querySelectorAll(".nav-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".nav-btn").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    const view = btn.dataset.view;
    document.querySelectorAll(".view").forEach(v => v.classList.remove("active"));
    document.getElementById("view-" + view).classList.add("active");
  });
});

// ── Forensic Panel ──
const panel = document.getElementById("forensic-panel");
const overlay = document.getElementById("panel-overlay");
const panelBody = document.getElementById("panel-body");

function openPanel(v) {
  panelBody.innerHTML = `
    <span class="severity-badge ${v.severity}">${v.severity}</span>
    <h3>${v.policy_name}</h3>
    <div class="detail-card">
      <div class="detail-row"><i class="fa-solid fa-server"></i><div><p class="detail-label">Resource</p><p class="detail-value mono">${v.resource_name}</p></div></div>
      <div class="detail-row"><i class="fa-solid fa-location-dot"></i><div><p class="detail-label">Region</p><p class="detail-value">${v.region}</p></div></div>
      <div class="detail-row"><i class="fa-solid fa-clock"></i><div><p class="detail-label">Detected</p><p class="detail-value">${new Date(v.detected_at).toLocaleString()}</p></div></div>
    </div>
    <div class="detail-card">
      <div class="detail-section-title"><i class="fa-solid fa-triangle-exclamation orange"></i> REASON</div>
      <p class="detail-text">${v.reason}</p>
    </div>
    <div class="detail-card">
      <div class="detail-section-title"><i class="fa-solid fa-wrench green"></i> REMEDIATION</div>
      <p class="detail-text">${v.remediation}</p>
    </div>
  `;
  panel.classList.add("open");
  overlay.classList.add("open");
}

function closePanel() {
  panel.classList.remove("open");
  overlay.classList.remove("open");
}

document.getElementById("panel-close").addEventListener("click", closePanel);
overlay.addEventListener("click", closePanel);

// ── Render violations table ──
function renderTable(tbody, violations) {
  tbody.innerHTML = violations.map(v => `
    <tr data-id="${v.id}">
      <td><span class="severity-badge ${v.severity}">${v.severity}</span></td>
      <td class="td-policy">${v.policy_name}</td>
      <td class="td-mono">${v.resource_name}</td>
      <td class="td-muted">${v.service}</td>
      <td class="td-muted">${v.region}</td>
    </tr>
  `).join("");

  tbody.querySelectorAll("tr").forEach(row => {
    row.addEventListener("click", () => {
      const v = violations.find(x => x.id === row.dataset.id);
      if (v) openPanel(v);
    });
  });
}

// ── Render assets ──
function renderAssets(assets) {
  document.getElementById("assets-count").textContent = `${assets.length} resources across 3 regions`;
  const grid = document.getElementById("assets-grid");
  grid.innerHTML = assets.map((a, i) => {
    const icon = ASSET_ICONS[a.type] || "fa-server";
    const riskClass = a.risk_score >= 70 ? "risk-high" : a.risk_score >= 40 ? "risk-med" : "risk-low";
    return `
      <div class="asset-card" style="animation-delay:${i * 0.04}s">
        <div class="asset-top">
          <div class="asset-icon"><i class="fa-solid ${icon}"></i></div>
          <span class="asset-status ${a.status}">${a.status.replace("-", " ")}</span>
        </div>
        <p class="asset-name">${a.name}</p>
        <p class="asset-type">${a.type}</p>
        <div class="asset-bottom">
          <span class="asset-region">${a.region}</span>
          <span class="asset-risk">Risk: <span class="${riskClass}">${a.risk_score}</span></span>
        </div>
      </div>
    `;
  }).join("");
}

// ── Render compliance ──
function renderCompliance(frameworks) {
  const grid = document.getElementById("compliance-grid");
  grid.innerHTML = frameworks.map((fw, i) => {
    const pct = Math.round((fw.passed / fw.total) * 100);
    const cls = pct >= 90 ? "green" : pct >= 75 ? "yellow" : "orange";
    return `
      <div class="compliance-card" style="animation-delay:${i * 0.06}s">
        <div class="comp-top">
          <div><span class="comp-short">${fw.shortName}</span><p class="comp-name">${fw.name}</p></div>
          <span class="comp-pct ${cls}">${pct}%</span>
        </div>
        <div class="comp-bar"><div class="comp-bar-fill ${cls}" style="width:${pct}%"></div></div>
        <div class="comp-stats">
          <span class="comp-stat"><i class="fa-solid fa-shield-check green"></i> ${fw.passed} passed</span>
          <span class="comp-stat"><i class="fa-solid fa-shield-xmark red"></i> ${fw.failed} failed</span>
        </div>
      </div>
    `;
  }).join("");
}

// ── Charts ──
function initSeverityChart(violations) {
  const counts = { critical:0, high:0, medium:0, low:0 };
  violations.forEach(v => counts[v.severity]++);

  const ctx = document.getElementById("severityChart").getContext("2d");
  if (severityChart) severityChart.destroy();
  severityChart = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: ["Critical","High","Medium","Low"],
      datasets: [{
        data: [counts.critical, counts.high, counts.medium, counts.low],
        backgroundColor: [COLORS.critical, COLORS.high, COLORS.medium, COLORS.low],
        borderWidth: 0,
        spacing: 3,
      }]
    },
    options: {
      cutout: "80%",
      responsive: true,
      maintainAspectRatio: true,
      plugins: { legend: { display: false } },
    }
  });

  const legend = document.getElementById("severityLegend");
  legend.innerHTML = Object.entries(counts).map(([key, val]) => `
    <div class="legend-item">
      <div class="legend-left"><div class="legend-dot" style="background:${COLORS[key]}"></div><span class="legend-name">${key.charAt(0).toUpperCase() + key.slice(1)}</span></div>
      <span class="legend-val">${val}</span>
    </div>
  `).join("");
}

function initTrendChart(trend) {
  const ctx = document.getElementById("trendChart").getContext("2d");
  if (trendChart) trendChart.destroy();
  trendChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: trend.map(t => t.date),
      datasets: [
        { label:"Critical", data: trend.map(t => t.critical), borderColor: COLORS.critical, backgroundColor: COLORS.critical + "30", fill: true, tension: 0.4, borderWidth: 2, pointRadius: 0 },
        { label:"High", data: trend.map(t => t.high), borderColor: COLORS.high, backgroundColor: COLORS.high + "20", fill: true, tension: 0.4, borderWidth: 2, pointRadius: 0 },
        { label:"Medium", data: trend.map(t => t.medium), borderColor: COLORS.medium, fill: false, tension: 0.4, borderWidth: 1.5, borderDash: [5,5], pointRadius: 0 },
        { label:"Low", data: trend.map(t => t.low), borderColor: COLORS.low, fill: false, tension: 0.4, borderWidth: 1.5, borderDash: [5,5], pointRadius: 0 },
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: { grid: { display: false }, ticks: { color: "#6b7a94", font: { size: 10 } } },
        y: { grid: { color: "rgba(255,255,255,0.04)" }, ticks: { color: "#6b7a94", font: { size: 10 } } },
      },
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: "rgba(15,18,26,0.95)",
          borderColor: "rgba(255,255,255,0.1)",
          borderWidth: 1,
          cornerRadius: 8,
          titleFont: { size: 11 },
          bodyFont: { size: 11 },
        }
      }
    }
  });
}

// ── fetchData (simulates API call) ──
function fetchData() {
  // Replace with: fetch('/api/dashboard').then(r => r.json()).then(data => { ... })
  const data = DATA;

  // KPIs
  document.getElementById("kpi-assets").textContent = data.resources.toLocaleString();
  const critCount = data.violations.filter(v => v.severity === "critical").length;
  document.getElementById("kpi-critical").textContent = critCount;
  document.getElementById("kpi-violations").textContent = data.violations.length;
  document.getElementById("kpi-score").textContent = data.score + "%";

  // Tables
  renderTable(document.getElementById("violations-tbody"), data.violations);
  renderTable(document.getElementById("threats-tbody"), data.violations);

  // Charts
  initSeverityChart(data.violations);
  initTrendChart(data.trend);

  // Assets & Compliance
  renderAssets(data.assets);
  renderCompliance(data.compliance);
}

// ── Init ──
document.addEventListener("DOMContentLoaded", fetchData);
