(function () {
  "use strict";

  const D = window.PAPER_DATA;
  if (!D) return;

  const MODEL_COLORS = {
    model_1: "#5b7c99",
    model_2: "#7c6b9e",
    model_3: "#0d6b5c",
    model_4: "#3d8b7a",
    model_5: "#c47d3a"
  };

  const MODEL_LABELS = Object.fromEntries(D.models.map((m) => [m.id, m.short + ": " + m.name]));

  let metricChart, rollingChart, noiseChart, radarChart;

  /* ── Utilities ── */
  function avgR2(modelId) {
    const rows = D.metrics.filter((r) => r.modelId === modelId);
    return rows.reduce((s, r) => s + r.r2, 0) / rows.length;
  }

  function fmt(n, d = 3) {
    if (n == null || Number.isNaN(n)) return "—";
    return Number(n).toFixed(d);
  }

  /* ── Progress & nav ── */
  function initProgress() {
    const bar = document.getElementById("read-progress");
    window.addEventListener("scroll", () => {
      const h = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.width = h > 0 ? (window.scrollY / h) * 100 + "%" : "0%";
    });
  }

  function initScrollSpy() {
    const links = document.querySelectorAll(".sidebar a[href^='#']");
    const sections = [...links].map((a) => document.querySelector(a.getAttribute("href"))).filter(Boolean);

    const obs = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            links.forEach((l) => l.classList.toggle("active", l.getAttribute("href") === "#" + e.target.id));
          }
        });
      },
      { rootMargin: "-40% 0px -50% 0px" }
    );
    sections.forEach((s) => obs.observe(s));
  }

  function initSidebar() {
    const toggle = document.getElementById("menu-toggle");
    const sidebar = document.querySelector(".sidebar");
    toggle?.addEventListener("click", () => sidebar.classList.toggle("open"));
    document.querySelectorAll(".sidebar a").forEach((a) => {
      a.addEventListener("click", () => sidebar.classList.remove("open"));
    });
  }

  /* ── Tabs ── */
  function initTabs() {
    document.querySelectorAll(".tabs").forEach((tabGroup) => {
      const btns = tabGroup.querySelectorAll(".tab-btn");
      const panels = tabGroup.parentElement.querySelectorAll(".tab-panel");
      btns.forEach((btn, i) => {
        btn.addEventListener("click", () => {
          btns.forEach((b, j) => {
            b.classList.toggle("active", j === i);
            panels[j]?.classList.toggle("active", j === i);
          });
        });
      });
    });
  }

  /* ── Accordions ── */
  function initAccordions() {
    document.querySelectorAll(".accordion-trigger").forEach((btn) => {
      btn.addEventListener("click", () => btn.closest(".accordion-item").classList.toggle("open"));
    });
  }

  /* ── Lightbox ── */
  function initLightbox() {
    const lb = document.getElementById("lightbox");
    const lbImg = document.getElementById("lightbox-img");
    document.querySelectorAll("figure img").forEach((img) => {
      img.addEventListener("click", () => {
        if (img.classList.contains("error")) return;
        lbImg.src = img.src;
        lbImg.alt = img.alt;
        lb.classList.add("open");
      });
      img.addEventListener("error", () => img.classList.add("error"));
    });
    lb?.addEventListener("click", () => lb.classList.remove("open"));
  }

  /* ── Model cards ── */
  function initModelCards() {
    const container = document.getElementById("model-cards");
    if (!container) return;
    D.models.forEach((m) => {
      const el = document.createElement("div");
      el.className = "card interactive" + (m.best ? " selected" : "");
      el.dataset.modelId = m.id;
      const avg = avgR2(m.id);
      el.innerHTML =
        "<strong>" + m.short + "</strong>" +
        m.name +
        "<br><small>Avg R² = " + fmt(avg) + " · " + m.params.toLocaleString() + " params</small>" +
        (m.aux ? '<br><span class="chip" style="display:inline-block;margin-top:0.4rem;font-size:0.7rem">+ auxiliaries</span>' : "");
      el.addEventListener("click", () => {
        container.querySelectorAll(".card").forEach((c) => c.classList.remove("selected"));
        el.classList.add("selected");
        document.getElementById("metric-model").value = m.id;
        updateMetricChart();
        updateRadarChart(m.id);
      });
      container.appendChild(el);
    });
  }

  /* ── Metric explorer chart ── */
  function initMetricExplorer() {
    const modelSel = document.getElementById("metric-model");
    const indexSel = document.getElementById("metric-index");
    const metricSel = document.getElementById("metric-type");

    D.models.forEach((m) => {
      const o = document.createElement("option");
      o.value = m.id;
      o.textContent = m.short + " — " + m.name;
      modelSel.appendChild(o);
    });
    modelSel.value = "model_3";

    const allIdx = [...new Set(D.metrics.map((r) => r.index))];
    allIdx.forEach((idx) => {
      const o = document.createElement("option");
      o.value = idx;
      o.textContent = idx;
      indexSel.appendChild(o);
    });
    indexSel.value = "all";

    [modelSel, indexSel, metricSel].forEach((el) => el.addEventListener("change", updateMetricChart));
    updateMetricChart();
  }

  function updateMetricChart() {
    const modelId = document.getElementById("metric-model").value;
    const indexFilter = document.getElementById("metric-index").value;
    const metricKey = document.getElementById("metric-type").value;
    const ctx = document.getElementById("metric-chart");
    if (!ctx) return;

    let rows;
    if (indexFilter === "all") {
      rows = D.models.map((m) => {
        const mRows = D.metrics.filter((r) => r.modelId === m.id);
        const val = mRows.reduce((s, r) => s + r[metricKey], 0) / mRows.length;
        return { label: m.short, value: val, id: m.id };
      });
    } else {
      rows = D.metrics
        .filter((r) => r.index === indexFilter)
        .map((r) => ({ label: D.models.find((m) => m.id === r.modelId)?.short || r.modelId, value: r[metricKey], id: r.modelId }));
    }

    const higherBetter = ["r2", "correlation"].includes(metricKey);
    rows.sort((a, b) => higherBetter ? b.value - a.value : a.value - b.value);

    if (metricChart) metricChart.destroy();
    metricChart = new Chart(ctx, {
      type: "bar",
      data: {
        labels: rows.map((r) => r.label),
        datasets: [{
          label: metricKey.toUpperCase(),
          data: rows.map((r) => r.value),
          backgroundColor: rows.map((r) => MODEL_COLORS[r.id] + "cc"),
          borderColor: rows.map((r) => MODEL_COLORS[r.id]),
          borderWidth: 1.5,
          borderRadius: 4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (c) => metricKey.toUpperCase() + ": " + fmt(c.raw, metricKey === "mape" ? 1 : 3)
            }
          }
        },
        scales: {
          y: {
            title: { display: true, text: metricKey.toUpperCase() },
            grid: { color: "rgba(0,0,0,0.06)" }
          },
          x: { grid: { display: false } }
        }
      }
    });
  }

  /* ── Grouped bar: all models × indices ── */
  function initGroupedChart() {
    const sel = document.getElementById("grouped-metric");
    const ctx = document.getElementById("grouped-chart");
    if (!ctx) return;

    function render() {
      const key = sel.value;
      const indices = D.indices;
      const datasets = D.models.map((m) => ({
        label: m.short,
        data: indices.map((idx) => {
          const row = D.metrics.find((r) => r.modelId === m.id && r.index === idx);
          return row ? row[key] : null;
        }),
        backgroundColor: MODEL_COLORS[m.id] + "bb",
        borderColor: MODEL_COLORS[m.id],
        borderWidth: 1
      }));

      if (window._groupedChart) window._groupedChart.destroy();
      window._groupedChart = new Chart(ctx, {
        type: "bar",
        data: { labels: indices, datasets },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { position: "bottom", labels: { boxWidth: 12, font: { size: 11 } } } },
          scales: {
            x: { stacked: false, grid: { display: false } },
            y: { title: { display: true, text: key.toUpperCase() }, grid: { color: "rgba(0,0,0,0.06)" } }
          }
        }
      });
    }
    sel.addEventListener("change", render);
    render();
  }

  /* ── Rolling origin chart ── */
  function initRollingChart() {
    const ctx = document.getElementById("rolling-chart");
    if (!ctx) return;
    const years = ["2019", "2020", "2021", "2024"];
    const keys = ["y2019", "y2020", "y2021", "y2024"];

    rollingChart = new Chart(ctx, {
      type: "line",
      data: {
        labels: years,
        datasets: D.rollingOrigin.map((r) => ({
          label: r.name,
          data: keys.map((k) => r[k]),
          borderColor: MODEL_COLORS[r.modelId],
          backgroundColor: MODEL_COLORS[r.modelId] + "33",
          tension: 0.3,
          pointRadius: 5,
          pointHoverRadius: 7
        }))
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: "bottom", labels: { boxWidth: 12, font: { size: 11 } } },
          tooltip: { callbacks: { label: (c) => c.dataset.label + ": R² = " + fmt(c.raw) } }
        },
        scales: {
          y: { min: 0.65, max: 1, title: { display: true, text: "R²" }, grid: { color: "rgba(0,0,0,0.06)" } },
          x: { grid: { display: false } }
        }
      }
    });
  }

  /* ── Noise robustness ── */
  function initNoiseExplorer() {
    const slider = document.getElementById("noise-slider");
    const display = document.getElementById("noise-value");
    const ctx = document.getElementById("noise-chart");
    if (!slider || !ctx) return;

    const scenarios = [
      { key: "twoStep", label: "Two-step input" },
      { key: "original", label: "Original (σ=0)" },
      { key: "n001", label: "σ = 0.01" },
      { key: "n003", label: "σ = 0.03" },
      { key: "n005", label: "σ = 0.05" }
    ];

    function render(idx) {
      const sc = scenarios[idx];
      display.textContent = sc.label;
      if (noiseChart) noiseChart.destroy();
      const sorted = [...D.noiseRobustness].sort((a, b) => b[sc.key] - a[sc.key]);
      noiseChart = new Chart(ctx, {
        type: "bar",
        data: {
          labels: sorted.map((r) => r.name),
          datasets: [{
            label: "R²",
            data: sorted.map((r) => r[sc.key]),
            backgroundColor: sorted.map((r) => MODEL_COLORS[r.modelId] + "cc"),
            borderColor: sorted.map((r) => MODEL_COLORS[r.modelId]),
            borderWidth: 1.5,
            borderRadius: 4
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          indexAxis: "y",
          plugins: { legend: { display: false } },
          scales: {
            x: { min: 0, max: 1, title: { display: true, text: "R²" } },
            y: { grid: { display: false } }
          }
        }
      });
    }

    slider.addEventListener("input", () => render(Number(slider.value)));
    render(1);
  }

  /* ── Radar chart for selected model ── */
  function initRadarChart() {
    updateRadarChart("model_3");
  }

  function updateRadarChart(modelId) {
    const ctx = document.getElementById("radar-chart");
    if (!ctx) return;
    const rows = D.metrics.filter((r) => r.modelId === modelId);
    const labels = rows.map((r) => r.index);
    const data = rows.map((r) => Math.max(0, r.r2));

    if (radarChart) radarChart.destroy();
    radarChart = new Chart(ctx, {
      type: "radar",
      data: {
        labels,
        datasets: [{
          label: MODEL_LABELS[modelId] || modelId,
          data,
          backgroundColor: MODEL_COLORS[modelId] + "44",
          borderColor: MODEL_COLORS[modelId],
          pointBackgroundColor: MODEL_COLORS[modelId],
          borderWidth: 2
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          r: {
            min: 0,
            max: 1,
            ticks: { stepSize: 0.2 },
            pointLabels: { font: { size: 10 } }
          }
        },
        plugins: { legend: { display: false } }
      }
    });
  }

  /* ── Sortable metrics table ── */
  function initMetricsTable() {
    const tbody = document.getElementById("metrics-tbody");
    const search = document.getElementById("metrics-search");
    if (!tbody) return;

    let sortKey = "r2";
    let sortAsc = false;

    function render(filter = "") {
      const q = filter.toLowerCase();
      let rows = D.metrics.filter(
        (r) =>
          !q ||
          r.index.toLowerCase().includes(q) ||
          r.model.toLowerCase().includes(q) ||
          r.modelId.includes(q)
      );
      rows.sort((a, b) => {
        const va = a[sortKey], vb = b[sortKey];
        return sortAsc ? (va > vb ? 1 : -1) : (va < vb ? 1 : -1);
      });
      tbody.innerHTML = rows
        .map((r) => {
          const r2cls = r.r2 < 0 ? "negative" : r.r2 > 0.8 ? "positive" : "";
          return (
            "<tr>" +
            "<td>" + (D.models.find((m) => m.id === r.modelId)?.short || "") + "</td>" +
            "<td>" + r.index + "</td>" +
            "<td class='" + r2cls + "'>" + fmt(r.r2) + "</td>" +
            "<td>" + fmt(r.rmse) + "</td>" +
            "<td>" + fmt(r.mae) + "</td>" +
            "<td>" + fmt(r.correlation) + "</td>" +
            "<td>" + fmt(r.mape, 1) + "</td>" +
            "</tr>"
          );
        })
        .join("");
    }

    document.querySelectorAll("#metrics-table th[data-sort]").forEach((th) => {
      th.addEventListener("click", () => {
        const key = th.dataset.sort;
        if (sortKey === key) sortAsc = !sortAsc;
        else { sortKey = key; sortAsc = key === "index" || key === "modelId"; }
        document.querySelectorAll("#metrics-table th").forEach((h) => h.classList.remove("sorted"));
        th.classList.add("sorted");
        render(search?.value || "");
      });
    });

    search?.addEventListener("input", (e) => render(e.target.value));
    render();
  }

  /* ── Reference search ── */
  function initRefSearch() {
    const input = document.getElementById("ref-search");
    const list = document.getElementById("ref-list");
    if (!input || !list) return;
    input.addEventListener("input", () => {
      const q = input.value.toLowerCase();
      list.querySelectorAll("li").forEach((li) => {
        li.classList.toggle("hidden", q && !li.textContent.toLowerCase().includes(q));
      });
    });
  }

  /* ── Pipeline hover ── */
  function initPipeline() {
    document.querySelectorAll(".pipeline-step").forEach((step) => {
      step.addEventListener("mouseenter", () => {
        const tip = step.dataset.tip;
        if (tip) step.title = tip;
      });
    });
  }

  /* ── Stat cards ── */
  function initStats() {
    const best = D.models.find((m) => m.best);
    const el = document.getElementById("hero-stats");
    if (!el) return;
    el.innerHTML =
      '<div class="stat-card"><div class="value">' + fmt(avgR2("model_3")) + '</div><div class="label">Best avg R² (NA-LSTM+aux)</div></div>' +
      '<div class="stat-card"><div class="value">25</div><div class="label">Years of data (2000–2024)</div></div>' +
      '<div class="stat-card"><div class="value">5</div><div class="label">Model configurations</div></div>' +
      '<div class="stat-card"><div class="value">10</div><div class="label">Spectral indices</div></div>' +
      '<div class="stat-card"><div class="value">' + D.meta.studyArea.areaHa.toLocaleString() + '</div><div class="label">Hectares study area</div></div>';
  }

  /* ── Boot ── */
  document.addEventListener("DOMContentLoaded", () => {
    initProgress();
    initScrollSpy();
    initSidebar();
    initTabs();
    initAccordions();
    initLightbox();
    initModelCards();
    initMetricExplorer();
    initGroupedChart();
    initRollingChart();
    initNoiseExplorer();
    initRadarChart();
    initMetricsTable();
    initRefSearch();
    initPipeline();
    initStats();
  });
})();
