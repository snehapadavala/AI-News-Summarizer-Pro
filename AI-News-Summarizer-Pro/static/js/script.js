const state = {
  mode: "paste",
  currentSummary: "",
  currentAnalysis: {},
  currentStats: {},
  history: []
};

const elements = {
  articleInput: document.getElementById("articleInput"),
  fileInput: document.getElementById("fileInput"),
  urlInput: document.getElementById("urlInput"),
  charCount: document.getElementById("charCount"),
  wordCount: document.getElementById("wordCount"),
  readTime: document.getElementById("readTime"),
  loader: document.getElementById("loader"),
  progressBar: document.getElementById("progressBar"),
  statusText: document.getElementById("statusText"),
  emptyState: document.getElementById("emptyState"),
  resultPanel: document.getElementById("resultPanel"),
  summaryOutput: document.getElementById("summaryOutput"),
  headlineOutput: document.getElementById("headlineOutput"),
  categoryOutput: document.getElementById("categoryOutput"),
  sentimentOutput: document.getElementById("sentimentOutput"),
  languageOutput: document.getElementById("languageOutput"),
  pointsOutput: document.getElementById("pointsOutput"),
  historyList: document.getElementById("historyList"),
  historySearch: document.getElementById("historySearch"),
  statWords: document.getElementById("statWords"),
  statSummaryWords: document.getElementById("statSummaryWords"),
  statCompression: document.getElementById("statCompression"),
  statTime: document.getElementById("statTime")
};

function updateCounters() {
  const text = elements.articleInput.value;
  const characters = text.length;
  const words = text.trim() ? text.trim().split(/\s+/).length : 0;
  const minutes = Math.max(1, Math.round(words / 200));
  elements.charCount.textContent = `${characters} characters`;
  elements.wordCount.textContent = `${words} words`;
  elements.readTime.textContent = `${minutes} min read`;
}

function setMode(mode) {
  state.mode = mode;
  document.querySelectorAll(".input-panel").forEach((panel) => panel.classList.add("d-none"));
  if (mode === "paste") {
    document.getElementById("pastePanel").classList.remove("d-none");
  } else if (mode === "txt" || mode === "pdf") {
    document.getElementById("uploadPanel").classList.remove("d-none");
  } else {
    document.getElementById("urlPanel").classList.remove("d-none");
  }
}

function setLoading(isLoading) {
  elements.loader.classList.toggle("d-none", !isLoading);
  if (isLoading) {
    elements.progressBar.style.width = "30%";
    elements.statusText.textContent = "Preparing your article...";
  }
}

function showResult(result) {
  elements.emptyState.classList.add("d-none");
  elements.resultPanel.classList.remove("d-none");
  elements.summaryOutput.innerHTML = `<p>${result.summary}</p>`;
  elements.headlineOutput.textContent = result.analysis?.headline || "News Insight";
  elements.categoryOutput.textContent = result.analysis?.category || "General";
  elements.sentimentOutput.textContent = result.analysis?.sentiment || "Neutral";
  elements.languageOutput.textContent = result.analysis?.language || "English";
  elements.pointsOutput.innerHTML = "";
  (result.analysis?.importantPoints || []).forEach((point) => {
    const li = document.createElement("li");
    li.className = "list-group-item";
    li.textContent = point;
    elements.pointsOutput.appendChild(li);
  });
}

function updateStats(stats) {
  elements.statWords.textContent = stats.originalWords || 0;
  elements.statSummaryWords.textContent = stats.summaryWords || 0;
  elements.statCompression.textContent = `${stats.compressionPercentage || 0}%`;
  elements.statTime.textContent = `${stats.processingTime || 0}s`;
}

function persistHistory() {
  localStorage.setItem("aiNewsHistory", JSON.stringify(state.history));
}

function loadStoredHistory() {
  const stored = localStorage.getItem("aiNewsHistory");
  if (stored) {
    state.history = JSON.parse(stored);
  }
}

function renderHistory() {
  const query = elements.historySearch.value.toLowerCase();
  const filtered = state.history.filter((entry) => entry.summary.toLowerCase().includes(query) || entry.title.toLowerCase().includes(query));
  if (!filtered.length) {
    elements.historyList.innerHTML = '<div class="empty-state"><p>No history yet.</p></div>';
    return;
  }
  elements.historyList.innerHTML = filtered.map((entry) => `
    <div class="history-item">
      <div>
        <strong>${entry.title}</strong>
        <div class="meta">${entry.source} • ${entry.timestamp}</div>
        <p class="mb-0 mt-2">${entry.summary}</p>
      </div>
      <div class="d-flex gap-2">
        <button class="btn btn-sm btn-outline-warning" data-favorite="${entry.id}">${entry.favorite ? "★" : "☆"}</button>
        <button class="btn btn-sm btn-outline-primary" data-reopen="${entry.id}">Reopen</button>
        <button class="btn btn-sm btn-outline-danger" data-delete="${entry.id}">Delete</button>
      </div>
    </div>
  `).join("");
}

async function loadHistory() {
  loadStoredHistory();
  try {
    const response = await fetch("/history");
    const data = await response.json();
    state.history = data.history || state.history;
    persistHistory();
    renderHistory();
  } catch (error) {
    console.error(error);
    renderHistory();
  }
}

async function submitSummary() {
  setLoading(true);
  elements.progressBar.style.width = "60%";
  elements.statusText.textContent = "Generating summary...";

  try {
    let body;
    let endpoint;
    if (state.mode === "paste") {
      endpoint = "/summarize";
      body = {
        article: elements.articleInput.value,
        mode: document.querySelector('input[name="summaryMode"]:checked').value,
        maxLength: Number(document.getElementById("maxLength").value),
        minLength: Number(document.getElementById("minLength").value),
        beamSearch: document.getElementById("beamSearch").value === "true",
        temperature: Number(document.getElementById("temperature").value),
        topK: Number(document.getElementById("topK").value),
        topP: Number(document.getElementById("topP").value)
      };
    } else if (state.mode === "txt" || state.mode === "pdf") {
      endpoint = "/upload";
      const formData = new FormData();
      formData.append("file", elements.fileInput.files[0]);
      formData.append("mode", document.querySelector('input[name="summaryMode"]:checked').value);
      formData.append("maxLength", document.getElementById("maxLength").value);
      formData.append("minLength", document.getElementById("minLength").value);
      formData.append("beamSearch", document.getElementById("beamSearch").value);
      formData.append("temperature", document.getElementById("temperature").value);
      formData.append("topK", document.getElementById("topK").value);
      formData.append("topP", document.getElementById("topP").value);
      body = formData;
    } else {
      endpoint = "/url";
      body = {
        url: elements.urlInput.value,
        mode: document.querySelector('input[name="summaryMode"]:checked').value,
        maxLength: Number(document.getElementById("maxLength").value),
        minLength: Number(document.getElementById("minLength").value),
        beamSearch: document.getElementById("beamSearch").value === "true",
        temperature: Number(document.getElementById("temperature").value),
        topK: Number(document.getElementById("topK").value),
        topP: Number(document.getElementById("topP").value)
      };
    }

    const options = {
      method: "POST",
      body: body instanceof FormData ? body : JSON.stringify(body),
      headers: body instanceof FormData ? {} : { "Content-Type": "application/json" }
    };

    const response = await fetch(endpoint, options);
    const data = await response.json();
    if (!response.ok || !data.success) {
      throw new Error(data.message || "Unable to generate a summary.");
    }

    state.currentSummary = data.summary;
    state.currentAnalysis = data.analysis;
    state.currentStats = data.statistics;
    state.history = data.history || [];
    showResult(data);
    updateStats(data.statistics);
    renderHistory();
    elements.progressBar.style.width = "100%";
    elements.statusText.textContent = "Summary ready";
  } catch (error) {
    elements.statusText.textContent = error.message;
    elements.progressBar.style.width = "100%";
  } finally {
    setTimeout(() => setLoading(false), 500);
  }
}

function clearInput() {
  elements.articleInput.value = "";
  elements.fileInput.value = "";
  elements.urlInput.value = "";
  updateCounters();
  elements.emptyState.classList.remove("d-none");
  elements.resultPanel.classList.add("d-none");
}

function copySummary() {
  navigator.clipboard.writeText(state.currentSummary).then(() => {
    elements.statusText.textContent = "Summary copied to clipboard";
  });
}

function downloadText() {
  const blob = new Blob([state.currentSummary], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = "summary.txt";
  anchor.click();
  URL.revokeObjectURL(url);
}

function downloadPdf() {
  const content = state.currentSummary || "No summary";
  const pdfText = `%PDF-1.4\n1 0 obj<< /Type /Catalog /Pages 2 0 R >>endobj\n2 0 obj<< /Type /Pages /Kids [3 0 R] /Count 1 >>endobj\n3 0 obj<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>endobj\n4 0 obj<< /Length 44 >>stream\nBT /F1 18 Tf 72 720 Td (${content.replace(/\n/g, " ")}) Tj ET\nendstream\nendobj\n5 0 obj<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>endobj\nxref\n0 6\n0000000000 65535 f \n0000000010 00000 n \n0000000062 00000 n \n0000000119 00000 n \n0000000207 00000 n \n0000000305 00000 n \ntrailer<< /Size 6 /Root 1 0 R >>\nstartxref\n0\n%%EOF`;
  const blob = new Blob([pdfText], { type: "application/pdf" });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = "summary.pdf";
  anchor.click();
  URL.revokeObjectURL(url);
}

function printSummary() {
  window.print();
}

function shareSummary() {
  if (navigator.share) {
    navigator.share({ title: "AI News Summary", text: state.currentSummary });
  } else {
    navigator.clipboard.writeText(state.currentSummary);
  }
}

function saveHistory() {
  if (!state.currentSummary) {
    return;
  }
  const entry = {
    id: crypto.randomUUID(),
    title: state.currentAnalysis.headline || "Saved Summary",
    summary: state.currentSummary,
    source: "Local Save",
    timestamp: new Date().toLocaleString(),
    favorite: false
  };
  state.history.unshift(entry);
  persistHistory();
  renderHistory();
}

function clearHistory() {
  state.history = [];
  persistHistory();
  renderHistory();
  fetch("/history", { method: "DELETE" });
}

function toggleFavorite(entryId) {
  state.history = state.history.map((entry) => (entry.id === entryId ? { ...entry, favorite: !entry.favorite } : entry));
  persistHistory();
  renderHistory();
}

document.addEventListener("DOMContentLoaded", () => {
  updateCounters();
  document.querySelectorAll(".nav-link").forEach((button) => {
    button.addEventListener("click", (event) => {
      if (event.currentTarget.dataset.mode) {
        document.querySelectorAll(".nav-link").forEach((link) => link.classList.remove("active"));
        event.currentTarget.classList.add("active");
        setMode(event.currentTarget.dataset.mode);
      }
    });
  });

  document.getElementById("articleInput").addEventListener("input", updateCounters);
  document.getElementById("generateBtn").addEventListener("click", submitSummary);
  document.getElementById("clearInputBtn").addEventListener("click", clearInput);
  document.getElementById("copySummaryBtn").addEventListener("click", copySummary);
  document.getElementById("downloadTxtBtn").addEventListener("click", downloadText);
  document.getElementById("downloadPdfBtn").addEventListener("click", downloadPdf);
  document.getElementById("printSummaryBtn").addEventListener("click", printSummary);
  document.getElementById("shareSummaryBtn").addEventListener("click", shareSummary);
  document.getElementById("favoriteSummaryBtn").addEventListener("click", () => {
    if (!state.currentSummary) {
      return;
    }
    const entry = state.history.find((item) => item.summary === state.currentSummary);
    if (entry) {
      toggleFavorite(entry.id);
    } else {
      saveHistory();
      const freshEntry = state.history.find((item) => item.summary === state.currentSummary);
      if (freshEntry) {
        toggleFavorite(freshEntry.id);
      }
    }
  });
  document.getElementById("saveHistoryBtn").addEventListener("click", saveHistory);
  document.getElementById("clearHistoryBtn").addEventListener("click", clearHistory);
  document.getElementById("historySearch").addEventListener("input", renderHistory);
  document.getElementById("themeToggle").addEventListener("click", () => {
    const root = document.documentElement;
    const isLight = root.getAttribute("data-theme") === "light";
    root.setAttribute("data-theme", isLight ? "dark" : "light");
    document.getElementById("themeToggle").textContent = isLight ? "☀️" : "🌙";
  });

  document.getElementById("historyList").addEventListener("click", (event) => {
    const button = event.target.closest("button");
    if (!button) return;
    const id = button.dataset.reopen || button.dataset.delete;
    if (button.dataset.reopen) {
      const entry = state.history.find((item) => item.id === id);
      if (entry) {
        state.currentSummary = entry.summary;
        state.currentAnalysis = { headline: entry.title };
        showResult({ summary: entry.summary, analysis: state.currentAnalysis });
      }
    }
    if (button.dataset.favorite) {
      toggleFavorite(id);
      return;
    }
    if (button.dataset.delete) {
      state.history = state.history.filter((item) => item.id !== id);
      persistHistory();
      renderHistory();
    }
  });

  loadHistory();
});
