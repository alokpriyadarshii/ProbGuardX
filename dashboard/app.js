function toRows(source) {
  return source.map(([customer_id, region, channel, spend, sessions, support_tickets, clicked_offer, churned, signup_date, event_date]) => ({
    customer_id,
    region,
    channel,
    spend,
    sessions,
    support_tickets,
    clicked_offer,
    churned,
    signup_date,
    event_date
  }));
}

const pythonRows = toRows([
  ["P001", "North", "web", 142.40, 11, 1, 1, 0, "2025-01-04", "2026-01-10"],
  ["P002", "North", "app", 96.75, 7, 2, 0, 1, "2025-02-12", "2026-01-19"],
  ["P003", "South", "web", 188.20, 14, 1, 1, 0, "2025-03-03", "2026-02-05"],
  ["P004", "South", "store", 74.30, 5, 3, 0, 1, "2025-03-21", "2026-02-18"],
  ["P005", "East", "app", 121.90, 10, 2, 1, 0, "2025-04-06", "2026-03-08"],
  ["P006", "East", "web", 59.60, 4, 4, 0, 1, "2025-04-29", "2026-03-22"],
  ["P007", "West", "store", 230.15, 18, 0, 1, 0, "2025-05-11", "2026-04-02"],
  ["P008", "West", "app", 172.80, 13, 1, 1, 0, "2025-06-17", "2026-04-20"],
  ["P009", "North", "store", 83.10, 6, 3, 0, 1, "2025-07-01", "2026-05-03"],
  ["P010", "South", "app", 139.95, 12, 1, 1, 0, "2025-08-14", "2026-05-28"],
  ["P011", "East", "store", 68.40, 5, 2, 0, 1, "2025-09-09", "2026-06-06"],
  ["P012", "West", "web", 201.25, 16, 0, 1, 0, "2025-10-20", "2026-06-18"]
]);

const rRows = toRows([
  ["R001", "Central", "branch", 212.00, 15, 1, 1, 0, "2025-01-08", "2026-01-14"],
  ["R002", "Central", "digital", 128.50, 9, 2, 1, 0, "2025-02-15", "2026-01-27"],
  ["R003", "Coastal", "branch", 77.25, 5, 3, 0, 1, "2025-03-11", "2026-02-08"],
  ["R004", "Coastal", "digital", 154.80, 11, 1, 1, 0, "2025-04-02", "2026-02-24"],
  ["R005", "Metro", "partner", 63.90, 4, 4, 0, 1, "2025-04-30", "2026-03-19"],
  ["R006", "Metro", "digital", 198.45, 14, 0, 1, 0, "2025-05-16", "2026-04-03"],
  ["R007", "Central", "partner", 91.60, 6, 2, 0, 1, "2025-06-07", "2026-04-21"],
  ["R008", "Coastal", "partner", 110.35, 8, 2, 0, 1, "2025-07-23", "2026-05-07"],
  ["R009", "Metro", "branch", 236.70, 17, 1, 1, 0, "2025-08-19", "2026-05-26"],
  ["R010", "Central", "digital", 119.95, 10, 1, 1, 0, "2025-09-28", "2026-06-03"],
  ["R011", "Coastal", "digital", 82.40, 6, 3, 0, 1, "2025-10-12", "2026-06-13"],
  ["R012", "Metro", "partner", 144.10, 9, 2, 1, 0, "2025-11-02", "2026-06-20"]
]);

const sqlRows = toRows([
  ["Q001", "Urban", "online", 154.30, 10, 1, 1, 0, "2025-01-11", "2026-01-09"],
  ["Q002", "Urban", "retail", 92.10, 6, 3, 0, 1, "2025-02-04", "2026-01-25"],
  ["Q003", "Rural", "online", 118.45, 8, 2, 1, 0, "2025-03-13", "2026-02-12"],
  ["Q004", "Rural", "retail", 61.80, 4, 4, 0, 1, "2025-04-22", "2026-03-01"],
  ["Q005", "Suburban", "partner", 209.50, 15, 1, 1, 0, "2025-05-08", "2026-03-27"],
  ["Q006", "Suburban", "online", 133.75, 11, 2, 1, 0, "2025-06-18", "2026-04-19"],
  ["Q007", "Urban", "partner", 70.25, 5, 3, 0, 1, "2025-07-02", "2026-05-03"],
  ["Q008", "Rural", "partner", 83.60, 6, 3, 0, 1, "2025-07-30", "2026-05-20"],
  ["Q009", "Suburban", "retail", 248.90, 17, 0, 1, 0, "2025-08-21", "2026-06-01"],
  ["Q010", "Urban", "online", 166.40, 12, 1, 1, 0, "2025-09-10", "2026-06-07"],
  ["Q011", "Rural", "online", 55.95, 4, 4, 0, 1, "2025-10-17", "2026-06-16"],
  ["Q012", "Suburban", "partner", 190.20, 13, 1, 1, 0, "2025-11-06", "2026-06-21"]
]);

const sasRows = toRows([
  ["S001", "Northwest", "portal", 305.20, 21, 1, 1, 0, "2025-01-02", "2026-01-04"],
  ["S002", "Northwest", "field", 176.40, 13, 2, 1, 0, "2025-02-18", "2026-01-29"],
  ["S003", "Southeast", "portal", 88.70, 6, 4, 0, 1, "2025-03-07", "2026-02-14"],
  ["S004", "Southeast", "field", 112.15, 7, 3, 0, 1, "2025-04-13", "2026-03-02"],
  ["S005", "Mountain", "portal", 257.90, 18, 1, 1, 0, "2025-05-01", "2026-03-30"],
  ["S006", "Mountain", "phone", 134.60, 9, 2, 0, 1, "2025-05-25", "2026-04-16"],
  ["S007", "Northwest", "phone", 198.75, 14, 1, 1, 0, "2025-06-11", "2026-05-05"],
  ["S008", "Southeast", "phone", 74.25, 5, 4, 0, 1, "2025-07-09", "2026-05-18"],
  ["S009", "Mountain", "field", 221.30, 16, 0, 1, 0, "2025-08-22", "2026-06-01"],
  ["S010", "Northwest", "portal", 159.85, 12, 2, 1, 0, "2025-09-15", "2026-06-08"],
  ["S011", "Southeast", "field", 93.45, 7, 3, 0, 1, "2025-10-10", "2026-06-17"],
  ["S012", "Mountain", "phone", 168.95, 11, 2, 1, 0, "2025-11-05", "2026-06-21"]
]);

const mapreduceRows = toRows([
  ["C001", "North", "web", 129.50, 12, 1, 1, 0, "2025-01-05", "2026-01-03"],
  ["C002", "South", "mobile", 84.00, 8, 2, 0, 1, "2025-02-14", "2026-01-12"],
  ["C003", "West", "store", 212.30, 17, 0, 1, 0, "2025-03-01", "2026-01-22"],
  ["C004", "East", "web", 45.20, 3, 3, 0, 1, "2025-03-18", "2026-02-02"],
  ["C005", "North", "mobile", 168.75, 14, 1, 1, 1, "2025-04-09", "2026-02-11"],
  ["C006", "South", "store", 76.40, 6, 2, 0, 1, "2025-04-21", "2026-02-19"],
  ["C007", "West", "web", 193.10, 16, 0, 1, 0, "2025-05-10", "2026-03-01"],
  ["C008", "East", "mobile", 58.90, 5, 4, 0, 1, "2025-05-25", "2026-03-13"],
  ["C009", "North", "store", 241.00, 20, 1, 1, 0, "2025-06-03", "2026-03-27"],
  ["C010", "South", "web", 99.25, 9, 2, 0, 1, "2025-06-18", "2026-04-04"],
  ["C011", "West", "mobile", 185.60, 15, 1, 1, 1, "2025-07-02", "2026-04-17"],
  ["C012", "East", "store", 63.30, 4, 3, 0, 0, "2025-07-19", "2026-04-28"],
  ["C013", "North", "web", 205.45, 18, 0, 1, 0, "2025-08-01", "2026-05-06"],
  ["C014", "South", "mobile", 71.80, 7, 3, 0, 1, "2025-08-20", "2026-05-18"],
  ["C015", "West", "store", 224.90, 19, 0, 1, 0, "2025-09-05", "2026-05-29"],
  ["C016", "East", "web", 52.60, 4, 4, 0, 1, "2025-09-22", "2026-06-03"],
  ["C017", "North", "mobile", 176.20, 13, 1, 1, 0, "2025-10-08", "2026-06-08"],
  ["C018", "South", "store", 88.10, 8, 2, 0, 0, "2025-10-25", "2026-06-12"],
  ["C019", "West", "web", 199.95, 16, 0, 1, 0, "2025-11-10", "2026-06-17"],
  ["C020", "East", "mobile", 67.45, 6, 3, 0, 0, "2025-11-27", "2026-06-20"]
]);

function average(values) {
  return values.reduce((sum, value) => sum + value, 0) / values.length;
}

function groupBy(rows, keyFn) {
  return rows.reduce((groups, row) => {
    const key = keyFn(row);
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(row);
    return groups;
  }, new Map());
}

function daysBetween(start, end) {
  return Math.round((new Date(end) - new Date(start)) / 86400000);
}

function features(rows) {
  return rows.map((row) => {
    const sessions = Math.max(row.sessions, 1);
    const supportLoad = row.support_tickets / sessions;
    return {
      ...row,
      tenure_days: daysBetween(row.signup_date, row.event_date),
      spend_per_session: row.spend / sessions,
      support_load: supportLoad,
      risk_segment: supportLoad >= 0.4 ? "high" : supportLoad >= 0.1 ? "medium" : "low"
    };
  });
}

function channelSummary(rows) {
  return Array.from(groupBy(rows, (row) => `${row.region}|${row.channel}`).entries())
    .map(([key, members]) => {
      const [region, channel] = key.split("|");
      return {
        region,
        channel,
        customers: new Set(members.map((row) => row.customer_id)).size,
        totalSpend: members.reduce((sum, row) => sum + row.spend, 0),
        avgSessions: average(members.map((row) => row.sessions)),
        churnRate: average(members.map((row) => row.churned)),
        clickRate: average(members.map((row) => row.clicked_offer))
      };
    })
    .sort((a, b) => a.region.localeCompare(b.region) || a.channel.localeCompare(b.channel));
}

function regionSummary(rows) {
  return Array.from(groupBy(rows, (row) => row.region).entries())
    .map(([region, members]) => ({
      region,
      customers: members.length,
      totalSpend: members.reduce((sum, row) => sum + row.spend, 0),
      avgSessions: average(members.map((row) => row.sessions)),
      churnRate: average(members.map((row) => row.churned))
    }))
    .sort((a, b) => a.region.localeCompare(b.region));
}

function crosstab(rows, leftField, rightField, leftLabel) {
  return Array.from(groupBy(rows, (row) => row[leftField]).entries())
    .map(([name, members]) => ({
      [leftLabel]: name,
      churn0: members.filter((row) => row[rightField] === 0).length,
      churn1: members.filter((row) => row[rightField] === 1).length,
      total: members.length
    }))
    .sort((a, b) => String(a[leftLabel]).localeCompare(String(b[leftLabel])));
}

function sigmoid(value) {
  return 1 / (1 + Math.exp(-Math.max(-35, Math.min(35, value))));
}

function churnScores(rows) {
  const columns = ["support_tickets", "clicked_offer", "spend_per_session", "tenure_days"];
  const means = Object.fromEntries(columns.map((column) => [column, average(rows.map((row) => row[column]))]));
  const scales = Object.fromEntries(columns.map((column) => {
    const variance = average(rows.map((row) => (row[column] - means[column]) ** 2));
    return [column, Math.sqrt(variance) || 1];
  }));
  const matrix = rows.map((row) => [1, ...columns.map((column) => (row[column] - means[column]) / scales[column])]);
  const labels = rows.map((row) => row.churned);
  const weights = new Array(matrix[0].length).fill(0);

  for (let epoch = 0; epoch < 1200; epoch += 1) {
    const gradients = new Array(weights.length).fill(0);
    matrix.forEach((rowFeatures, rowIndex) => {
      const prediction = sigmoid(rowFeatures.reduce((sum, value, index) => sum + value * weights[index], 0));
      rowFeatures.forEach((value, index) => {
        gradients[index] += (prediction - labels[rowIndex]) * value;
      });
    });
    weights.forEach((_, index) => {
      weights[index] -= 0.08 * gradients[index] / rows.length;
    });
  }

  return rows
    .map((row, index) => ({
      ...row,
      score: sigmoid(matrix[index].reduce((sum, value, weightIndex) => sum + value * weights[weightIndex], 0))
    }))
    .sort((a, b) => b.score - a.score)
    .slice(0, 8);
}

function fillRows(selector, rows, columns) {
  const body = document.querySelector(`${selector} tbody`);
  body.innerHTML = rows.map((row) => `
    <tr>
      ${columns.map((column) => `<td>${column.format ? column.format(row[column.key], row) : row[column.key]}</td>`).join("")}
    </tr>
  `).join("");
}

let viewConfig = {};

function formatPercent(value) {
  return `${(value * 100).toFixed(1)}%`;
}

function formatMoney(value) {
  return value.toFixed(2);
}

function uniqueCount(rows, field) {
  return new Set(rows.map((row) => row[field])).size;
}

function datasetMetrics(rows) {
  return [
    { label: "Records", value: rows.length },
    { label: "Regions", value: uniqueCount(rows, "region") },
    { label: "Channels", value: uniqueCount(rows, "channel") },
    { label: "Churn Rate", value: formatPercent(average(rows.map((row) => row.churned))) }
  ];
}

function mapreduceMetrics(rows) {
  return [
    { label: "Customers", value: rows.length },
    { label: "Regions", value: uniqueCount(rows, "region") },
    { label: "Total Spend", value: formatMoney(rows.reduce((sum, row) => sum + row.spend, 0)) },
    { label: "Churn Rate", value: formatPercent(average(rows.map((row) => row.churned))) }
  ];
}

function logisticMetrics(scores) {
  return [
    { label: "Scores", value: scores.length },
    { label: "Highest Risk", value: scores[0].score.toFixed(3) },
    { label: "Top Churned", value: scores.filter((row) => row.churned === 1).length },
    { label: "Model", value: "SAS" }
  ];
}

function freqMetrics(rows) {
  return [
    { label: "Records", value: rows.length },
    { label: "Regions", value: uniqueCount(rows, "region") },
    { label: "Risk Segments", value: uniqueCount(rows, "risk_segment") },
    { label: "Churned", value: rows.filter((row) => row.churned === 1).length }
  ];
}

function renderMetrics(metrics) {
  document.getElementById("metricGrid").innerHTML = metrics.map((metric) => `
    <article class="metric-card">
      <span>${metric.label}</span>
      <strong>${metric.value}</strong>
    </article>
  `).join("");
}

function selectedViewFromHash() {
  const view = window.location.hash.replace("#", "");
  return viewConfig[view] ? view : "python";
}

function setActiveView(view, updateHash = true) {
  const config = viewConfig[view];
  if (!config) return;

  if (updateHash && window.location.hash !== `#${view}`) {
    window.history.replaceState(null, "", `#${view}`);
  }

  document.getElementById("viewEyebrow").textContent = config.eyebrow;
  document.getElementById("viewTitle").textContent = config.title;
  renderMetrics(config.metrics);

  document.querySelectorAll("[data-view]").forEach((button) => {
    const active = button.dataset.view === view;
    button.classList.toggle("is-active", active);
    button.setAttribute("aria-pressed", String(active));
  });

  document.querySelectorAll("[data-panel]").forEach((panel) => {
    const active = panel.dataset.panel === view;
    panel.hidden = !active;
    panel.classList.toggle("is-active", active);
  });
}

function bindNavigation() {
  document.querySelectorAll("[data-view]").forEach((button) => {
    button.addEventListener("click", () => setActiveView(button.dataset.view));
  });

  window.addEventListener("hashchange", () => setActiveView(selectedViewFromHash(), false));
}

function profileInitials(name) {
  const parts = name.trim().split(/\s+/).filter(Boolean);
  return (parts.length ? parts.slice(0, 2).map((part) => part[0]).join("") : "AP").toUpperCase();
}

function updateProfileMark() {
  const mark = document.querySelector(".profile-mark");
  const name = localStorage.getItem("probguardx.profileName") || "Alok Priyadarshi";
  if (mark) mark.textContent = profileInitials(name);
}

function finishInlineEdit(element, input, save) {
  if (save) {
    const value = input.value.trim();
    if (value) {
      localStorage.setItem(element.dataset.storageKey, value);
      element.textContent = value;
    }
  }

  input.remove();
  element.hidden = false;
  element.focus();
  updateProfileMark();
}

function startInlineEdit(element) {
  if (element.hidden) return;

  const input = document.createElement("input");
  input.className = "inline-edit-input";
  input.value = element.textContent.trim();
  input.setAttribute("aria-label", element.getAttribute("aria-label") || "Edit text");

  element.hidden = true;
  element.insertAdjacentElement("afterend", input);
  input.focus();
  input.select();

  input.addEventListener("click", (event) => event.stopPropagation());
  input.addEventListener("keydown", (event) => {
    if (event.key === "Enter") finishInlineEdit(element, input, true);
    if (event.key === "Escape") finishInlineEdit(element, input, false);
  });
  input.addEventListener("blur", () => finishInlineEdit(element, input, true), { once: true });
}

function bindEditableText() {
  document.querySelectorAll("[data-editable-text]").forEach((element) => {
    const value = localStorage.getItem(element.dataset.storageKey) || element.dataset.defaultValue;
    element.textContent = value;
    element.tabIndex = 0;
    element.setAttribute("role", "button");

    element.addEventListener("click", () => startInlineEdit(element));
    element.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        startInlineEdit(element);
      }
    });
  });

  updateProfileMark();
}

function render() {
  const summaryColumns = [
    { key: "region" },
    { key: "channel" },
    { key: "customers" },
    { key: "totalSpend", format: (value) => value.toFixed(2) },
    { key: "avgSessions", format: (value) => value.toFixed(2) },
    { key: "churnRate", format: (value) => value.toFixed(3) },
    { key: "clickRate", format: (value) => value.toFixed(3) }
  ];
  const pythonFeatures = features(pythonRows);
  const rFeatures = features(rRows);
  const sqlFeatures = features(sqlRows);
  const sasFeatures = features(sasRows);
  const mapreduceFeatures = features(mapreduceRows);
  const sasScores = churnScores(sasFeatures);
  const sasRegionFreq = crosstab(sasFeatures, "region", "churned", "region");
  const sasRiskFreq = crosstab(sasFeatures, "risk_segment", "churned", "risk_segment");

  fillRows("#pythonTable", channelSummary(pythonFeatures), summaryColumns);
  fillRows("#rTable", channelSummary(rFeatures), summaryColumns);
  fillRows("#sqlTable", channelSummary(sqlFeatures), summaryColumns);
  fillRows("#sasTable", channelSummary(sasFeatures), summaryColumns);

  fillRows("#mapreduceTable", regionSummary(mapreduceFeatures), [
    { key: "region" },
    { key: "customers" },
    { key: "totalSpend", format: (value) => value.toFixed(2) },
    { key: "avgSessions", format: (value) => value.toFixed(2) },
    { key: "churnRate", format: (value) => value.toFixed(3) }
  ]);

  fillRows("#regionFreqTable", sasRegionFreq, [
    { key: "region" },
    { key: "churn0" },
    { key: "churn1" },
    { key: "total" }
  ]);

  fillRows("#riskFreqTable", sasRiskFreq, [
    { key: "risk_segment" },
    { key: "churn0" },
    { key: "churn1" },
    { key: "total" }
  ]);

  document.getElementById("riskList").innerHTML = sasScores.map((row) => `
    <div class="risk-row">
      <strong>${row.customer_id} ${row.region}</strong>
      <div class="risk-track"><div class="risk-fill" style="width: ${(row.score * 100).toFixed(1)}%"></div></div>
      <span>${row.score.toFixed(3)}</span>
    </div>
  `).join("");

  viewConfig = {
    python: {
      eyebrow: "Python",
      title: "Dataset Output",
      metrics: datasetMetrics(pythonFeatures)
    },
    r: {
      eyebrow: "R",
      title: "Dataset Output",
      metrics: datasetMetrics(rFeatures)
    },
    sql: {
      eyebrow: "SQL",
      title: "Dataset Output",
      metrics: datasetMetrics(sqlFeatures)
    },
    sas: {
      eyebrow: "SAS",
      title: "Dataset Output",
      metrics: datasetMetrics(sasFeatures)
    },
    mapreduce: {
      eyebrow: "MapReduce",
      title: "Region Aggregate Output",
      metrics: mapreduceMetrics(mapreduceFeatures)
    },
    "sas-logistic": {
      eyebrow: "SAS PROC LOGISTIC",
      title: "Churn Score Output",
      metrics: logisticMetrics(sasScores)
    },
    "sas-freq": {
      eyebrow: "SAS PROC FREQ",
      title: "Frequency Output",
      metrics: freqMetrics(sasFeatures)
    }
  };

  bindNavigation();
  bindEditableText();
  setActiveView(selectedViewFromHash(), false);
}

render();
