const metricsEl = document.querySelector("#metrics");
const statusChartEl = document.querySelector("#statusChart");
const pavilionChartEl = document.querySelector("#pavilionChart");
const recordsBodyEl = document.querySelector("#recordsBody");
const statusFilterEl = document.querySelector("#statusFilter");

let records = [];

function metric(label, value) {
  return `<article class="metric"><span>${label}</span><strong>${value}</strong></article>`;
}

function renderBars(target, values, warn = false) {
  const max = Math.max(...Object.values(values), 1);
  target.innerHTML = Object.entries(values)
    .sort((a, b) => b[1] - a[1])
    .map(([label, value]) => {
      const width = Math.max((value / max) * 100, 4);
      return `
        <div class="bar-row">
          <span>${label}</span>
          <div class="bar-track"><div class="bar-fill ${warn ? "warn" : ""}" style="width:${width}%"></div></div>
          <strong>${value}</strong>
        </div>
      `;
    })
    .join("");
}

function countBy(rows, key) {
  return rows.reduce((acc, row) => {
    const value = row[key] || "Unassigned";
    acc[value] = (acc[value] || 0) + 1;
    return acc;
  }, {});
}

function renderRecords() {
  const selected = statusFilterEl.value;
  const visible = records
    .filter((row) => !selected || row["Operational Status"] === selected)
    .slice(0, 40);

  recordsBodyEl.innerHTML = visible
    .map((row) => `
      <tr>
        <td>${row.Pavilion}</td>
        <td>${row.Module}</td>
        <td>${row.Requirement}</td>
        <td>${row["Implementation Level"]}</td>
        <td>${row.Verified}</td>
        <td>${row.Urgent}</td>
        <td>${row["Operational Status"]}</td>
      </tr>
    `)
    .join("");
}

async function init() {
  const [summaryResponse, recordsResponse] = await Promise.all([
    fetch("/api/summary"),
    fetch("/api/records"),
  ]);

  const summary = await summaryResponse.json();
  records = await recordsResponse.json();

  metricsEl.innerHTML = [
    metric("Synthetic Records", summary.total_records),
    metric("Urgent Requirements", summary.urgent_records),
    metric("Verified Records", summary.verified_records),
    metric("Owner Teams", summary.owner_teams),
  ].join("");

  renderBars(statusChartEl, summary.by_status, true);
  renderBars(pavilionChartEl, summary.by_pavilion);

  Object.keys(countBy(records, "Operational Status"))
    .sort()
    .forEach((status) => {
      const option = document.createElement("option");
      option.value = status;
      option.textContent = status;
      statusFilterEl.appendChild(option);
    });

  statusFilterEl.addEventListener("change", renderRecords);
  renderRecords();
}

init().catch((error) => {
  metricsEl.innerHTML = `<article class="metric"><span>Load Error</span><strong>${error.message}</strong></article>`;
});
