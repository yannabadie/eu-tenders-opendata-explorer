/**
 * Interactive EU Public Tenders Explorer — Same-Origin Official TED v3 Snapshot (0 CORS errors)
 * + Live API snippet generator (TED v3 / RapidAPI / Apify / MCP).
 */
(function () {
  "use strict";

  var fmtInt = new Intl.NumberFormat("en-US");

  function clearEl(el) {
    while (el && el.firstChild) el.removeChild(el.firstChild);
  }

  function renderRows(tbody, items, emptyMsg) {
    if (!tbody) return;
    clearEl(tbody);
    if (!items.length) {
      var tr0 = document.createElement("tr");
      var td0 = document.createElement("td");
      td0.colSpan = 6;
      td0.textContent = emptyMsg || "No matching active tenders in this filter.";
      tr0.appendChild(td0);
      tbody.appendChild(tr0);
      return;
    }
    for (var i = 0; i < items.length; i++) {
      var it = items[i];
      var tr = document.createElement("tr");

      var tdCountry = document.createElement("td");
      tdCountry.textContent = it.countryName + " (" + it.iso2 + ")";
      tr.appendChild(tdCountry);

      var tdSector = document.createElement("td");
      var cpv = document.createElement("span");
      cpv.className = "cpv-pill";
      cpv.textContent = it.cpv || "CPV";
      tdSector.appendChild(cpv);
      var br = document.createElement("div");
      br.style.fontSize = "0.78rem";
      br.style.color = "#64748b";
      br.style.marginTop = "3px";
      br.textContent = it.sectorName;
      tdSector.appendChild(br);
      tr.appendChild(tdSector);

      var tdTitle = document.createElement("td");
      var a = document.createElement("a");
      a.href = it.url;
      a.target = "_blank";
      a.rel = "noopener noreferrer";
      a.textContent = it.title;
      tdTitle.appendChild(a);
      var pub = document.createElement("div");
      pub.style.fontSize = "0.76rem";
      pub.style.color = "#64748b";
      pub.textContent = "TED " + it.pub + " · Published " + (it.published || "—");
      tdTitle.appendChild(pub);
      tr.appendChild(tdTitle);

      var tdBuyer = document.createElement("td");
      tdBuyer.textContent = it.buyer;
      tr.appendChild(tdBuyer);

      var tdDeadline = document.createElement("td");
      var dl = document.createElement("span");
      dl.className = "deadline-pill";
      dl.textContent = it.deadline || "Open";
      tdDeadline.appendChild(dl);
      tr.appendChild(tdDeadline);

      var tdPage = document.createElement("td");
      var link = document.createElement("a");
      link.href = it.pageHref;
      link.textContent = "Sector Guide →";
      tdPage.appendChild(link);
      tr.appendChild(tdPage);

      tbody.appendChild(tr);
    }
  }

  function updateSnippet(preEl, iso3, cpvQuery) {
    if (!preEl) return;
    var q = "CY = " + (iso3 === "ALL" ? "FRA" : iso3) + " AND " + (cpvQuery || "(PC = 72* OR PC = 48*)") + " AND notice-type = cn-standard AND DT >= 20261121";
    preEl.textContent =
      'curl -s -X POST "https://api.ted.europa.eu/v3/notices/search" \\\n' +
      '  -H "Content-Type: application/json" \\\n' +
      '  -d \'{"query": "' + q + '", "fields": ["publication-number", "notice-title", "buyer-name", "deadline-receipt-tender-date-lot"], "limit": 20}\'';
  }

  function init() {
    var root = document.getElementById("ted-live-explorer");
    if (!root) return;

    var dataUrl = root.getAttribute("data-snapshot-url") || "./data/ted_snapshot_60.json";
    var pagePrefix = root.getAttribute("data-page-prefix") || "./sectors/";
    var countrySel = document.getElementById("ted-country");
    var sectorSel = document.getElementById("ted-sector");
    var kwInput = document.getElementById("ted-keyword");
    var tbody = document.getElementById("ted-results-tbody");
    var statusEl = document.getElementById("ted-explorer-status");
    var snippetEl = document.getElementById("ted-curl-snippet");

    fetch(dataUrl)
      .then(function (r) {
        if (!r.ok) throw new Error("HTTP " + r.status);
        return r.json();
      })
      .then(function (snap) {
        var flat = [];
        var pages = snap.pages || [];
        var sectorMap = {};
        for (var i = 0; i < pages.length; i++) {
          var p = pages[i];
          sectorMap[p.sector.slug] = p.sector.cpv_query;
          var samples = p.samples || [];
          for (var j = 0; j < samples.length; j++) {
            var s = samples[j];
            flat.push({
              countrySlug: p.country.slug,
              countryName: p.country.name,
              iso2: p.country.iso2,
              iso3: p.country.iso3,
              sectorSlug: p.sector.slug,
              sectorName: p.sector.name,
              pageHref: pagePrefix + p.slug + ".html",
              pub: s.pub,
              title: s.title,
              buyer: s.buyer,
              published: s.published,
              deadline: s.deadline,
              cpv: s.cpv,
              url: s.url,
              hay: (p.country.name + " " + p.sector.name + " " + s.title + " " + s.buyer + " " + s.cpv + " " + s.pub).toLowerCase()
            });
          }
        }

        function apply() {
          var cVal = countrySel ? countrySel.value : "all";
          var sVal = sectorSel ? sectorSel.value : "all";
          var kw = (kwInput && kwInput.value ? kwInput.value : "").trim().toLowerCase();

          var matched = [];
          var matchedOpenTotal = 0;
          var activeIso3 = "ALL";
          for (var pIdx = 0; pIdx < pages.length; pIdx++) {
            var pg = pages[pIdx];
            if ((cVal === "all" || pg.country.slug === cVal) && (sVal === "all" || pg.sector.slug === sVal)) {
              matchedOpenTotal += Number(pg.open_tenders_count || 0);
              if (cVal !== "all") activeIso3 = pg.country.iso3;
            }
          }

          for (var k = 0; k < flat.length; k++) {
            var row = flat[k];
            if (cVal !== "all" && row.countrySlug !== cVal) continue;
            if (sVal !== "all" && row.sectorSlug !== sVal) continue;
            if (kw && row.hay.indexOf(kw) === -1) continue;
            matched.push(row);
          }

          renderRows(tbody, matched.slice(0, 30), "No sample notices match your keyword — clear the keyword or use our RapidAPI / Apify Actor for full pagination.");
          if (statusEl) {
            statusEl.textContent =
              "Official EU TED v3 snapshot (" + (snap.as_of || "2026-11-21") + "): " +
              fmtInt.format(matchedOpenTotal) + " active open tenders across matching country/sector scope · Showing " +
              Math.min(matched.length, 30) + " / " + matched.length + " live sample notices.";
          }
          updateSnippet(snippetEl, activeIso3, sVal !== "all" ? sectorMap[sVal] : "(PC = 72* OR PC = 48*)");
        }

        if (countrySel) countrySel.addEventListener("change", apply);
        if (sectorSel) sectorSel.addEventListener("change", apply);
        if (kwInput) kwInput.addEventListener("input", apply);
        apply();
      })
      .catch(function (err) {
        if (statusEl) statusEl.textContent = "Unable to load local snapshot (" + err.message + ").";
      });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
