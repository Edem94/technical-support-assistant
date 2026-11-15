// Veloria support assistant front end. No build step: plain DOM, talks to POST /ask and GET /health.
// Model output is always inserted as text nodes, never as HTML.

const MAX_LENGTH = 2000;
const REQUEST_TIMEOUT_MS = 60000;

const SUGGESTIONS = [
  { product: "VeloSync", text: "VeloSync shows error VS-1042 and one file never syncs. What should I do?" },
  { product: "VeloGuard VPN", text: "VeloGuard won't connect on hotel Wi-Fi. How can I get it working?" },
  { product: "VeloBook 14", text: "My VeloBook 14 battery drains overnight while it's asleep. Is there a fix?" },
  { product: "Veloria ID", text: "I lost my phone with my authenticator app. How do I sign in?" },
];

const OUTCOMES = {
  answered: "Answered",
  escalate: "Needs a support agent",
  decline: "Outside what I can answer",
};

const SOURCE_TYPES = {
  kb_article: "Help article",
  error_code: "Error code",
  known_issue: "Known issue",
  ticket: "Past ticket",
  manual: "Manual",
};

const $ = (selector, root = document) => root.querySelector(selector);
const thread = $("#thread");
const welcome = $("#welcome");
const form = $("#composer");
const input = $("#question");
const sendButton = $("#send");
const counter = $("#counter");
let busy = false;

// ---------------------------------------------------------------- theme

function storedTheme() {
  try { return localStorage.getItem("theme"); } catch { return null; }
}

function applyTheme(theme) {
  const root = document.documentElement;
  if (theme) root.dataset.theme = theme; else delete root.dataset.theme;
  const dark = theme ? theme === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
  root.toggleAttribute("data-dark", dark);
}

applyTheme(storedTheme());
matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => applyTheme(storedTheme()));
$("#theme-toggle").addEventListener("click", () => {
  const next = document.documentElement.hasAttribute("data-dark") ? "light" : "dark";
  try { localStorage.setItem("theme", next); } catch { /* private mode: theme just won't persist */ }
  applyTheme(next);
});

// ---------------------------------------------------------------- service status

async function checkHealth() {
  const status = $("#status");
  const text = $(".status-text", status);
  try {
    const response = await fetch("/health");
    const body = await response.json();
    const ok = response.ok && body.status === "ok";
    status.dataset.state = ok ? "ok" : "down";
    text.textContent = ok ? "Online" : "Unavailable";
    status.title = ok ? `Model: ${body.model}` : body.error || "The assistant is not ready.";
  } catch {
    status.dataset.state = "down";
    text.textContent = "Offline";
    status.title = "Cannot reach the server.";
  }
}

// ---------------------------------------------------------------- rendering helpers

function fromTemplate(id) {
  return $(id).content.firstElementChild.cloneNode(true);
}

function scrollToBottom() {
  thread.scrollTop = thread.scrollHeight;
}

// Wrap error codes such as VS-1042 or VB-E09 in <code>.
const CODE_PATTERN = /\b[A-Z]{2}-[A-Z]?\d{2,4}\b/g;

function appendInline(parent, text) {
  let last = 0;
  for (const match of text.matchAll(CODE_PATTERN)) {
    parent.append(text.slice(last, match.index));
    const code = document.createElement("code");
    code.textContent = match[0];
    parent.append(code);
    last = match.index + match[0].length;
  }
  parent.append(text.slice(last));
}

// Turn plain answer text into paragraphs and lists. Handles "1. ", "1) ", "Step 1: " and "- " lines,
// and inline numbered steps like "... Step 2: ..." that the model writes on one line.
function renderAnswer(container, text) {
  const normalised = text
    .replace(/\s+(?=(?:Step|Option) \d+[:.)]\s)/g, "\n")
    .replace(/\s+(?=\d+\)\s)/g, "\n");
  const lines = normalised.split(/\n+/).map((line) => line.trim()).filter(Boolean);
  let list = null;
  for (const line of lines) {
    const numbered = line.match(/^(?:(?:Step|Option) )?\d+[.):]\s+(.*)$/);
    const bullet = line.match(/^[-•*]\s+(.*)$/);
    if (numbered || bullet) {
      const type = numbered ? "OL" : "UL";
      if (!list || list.tagName !== type) {
        list = document.createElement(type.toLowerCase());
        container.append(list);
      }
      const item = document.createElement("li");
      appendInline(item, (numbered || bullet)[1]);
      list.append(item);
    } else {
      list = null;
      const paragraph = document.createElement("p");
      appendInline(paragraph, line);
      container.append(paragraph);
    }
  }
}

function addUserMessage(question) {
  const node = fromTemplate("#tpl-user");
  $(".bubble", node).textContent = question;
  thread.append(node);
}

function addAssistantMessage(data, seconds) {
  const node = fromTemplate("#tpl-assistant");
  const badge = $(".badge", node);
  badge.dataset.outcome = data.outcome;
  badge.textContent = OUTCOMES[data.outcome] || data.outcome;
  $(".meta", node).textContent = `${seconds.toFixed(1)}s`;

  if (data.escalate) {
    $(".escalation", node).hidden = false;
    $(".escalation-reason", node).textContent =
      data.escalation_reason || "This needs a person to look at it.";
  }

  renderAnswer($(".answer", node), data.answer);

  if (data.sources.length) {
    $(".sources", node).hidden = false;
    const list = $(".source-list", node);
    for (const source of data.sources) {
      const item = document.createElement("li");
      item.className = "source";
      item.title = source.title;
      const id = document.createElement("span");
      id.className = "source-id";
      id.textContent = source.id;
      const title = document.createElement("span");
      title.className = "source-title";
      title.textContent = source.title;
      const type = document.createElement("span");
      type.className = "source-type";
      type.textContent = SOURCE_TYPES[source.type] || source.type;
      item.append(id, title, type);
      list.append(item);
    }
  }

  const copy = $(".copy", node);
  copy.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(data.answer);
      $("span", copy).textContent = "Copied";
    } catch {
      $("span", copy).textContent = "Copy failed";
    }
    setTimeout(() => { $("span", copy).textContent = "Copy"; }, 1500);
  });

  thread.append(node);
}

function addError(message, question) {
  const node = fromTemplate("#tpl-error");
  $(".error-text", node).textContent = message;
  $(".retry", node).addEventListener("click", () => {
    node.remove();
    ask(question, { retry: true });
  });
  thread.append(node);
}

// ---------------------------------------------------------------- asking

function errorMessage(status, body) {
  if (status === 422) return "That question couldn't be sent. Please check it isn't empty or too long.";
  if (body && typeof body.detail === "string") return body.detail;
  return "Something went wrong on our side. Please try again.";
}

async function ask(question, { retry = false } = {}) {
  if (busy) return;
  busy = true;
  updateComposer();
  welcome.hidden = true;
  if (!retry) addUserMessage(question);
  const thinking = fromTemplate("#tpl-thinking");
  thread.append(thinking);
  scrollToBottom();

  const started = performance.now();
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);
  try {
    const response = await fetch("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
      signal: controller.signal,
    });
    const body = await response.json().catch(() => null);
    thinking.remove();
    if (response.ok && body) {
      addAssistantMessage(body, (performance.now() - started) / 1000);
    } else {
      addError(errorMessage(response.status, body), question);
    }
  } catch (error) {
    thinking.remove();
    addError(
      error.name === "AbortError"
        ? "The assistant took too long to answer. Please try again."
        : "Can't reach the server. Check your connection and try again.",
      question,
    );
  } finally {
    clearTimeout(timer);
    busy = false;
    updateComposer();
    scrollToBottom();
    input.focus();
  }
}

// ---------------------------------------------------------------- composer

function updateComposer() {
  const length = input.value.length;
  sendButton.disabled = busy || !input.value.trim();
  counter.textContent = length > MAX_LENGTH * 0.8 ? `${length} / ${MAX_LENGTH}` : "";
  counter.dataset.near = String(length > MAX_LENGTH * 0.9);
  input.style.height = "auto";
  input.style.height = `${input.scrollHeight}px`;
}

function submit() {
  const question = input.value.trim();
  if (!question || busy) return;
  input.value = "";
  updateComposer();
  ask(question);
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  submit();
});

input.addEventListener("input", updateComposer);
input.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey && !event.isComposing) {
    event.preventDefault();
    submit();
  }
});

$("#new-chat").addEventListener("click", () => {
  if (busy) return;
  thread.querySelectorAll(".message").forEach((node) => node.remove());
  welcome.hidden = false;
  input.value = "";
  updateComposer();
  input.focus();
});

for (const suggestion of SUGGESTIONS) {
  const button = document.createElement("button");
  button.type = "button";
  button.className = "suggestion";
  const product = document.createElement("span");
  product.className = "suggestion-product";
  product.textContent = suggestion.product;
  const text = document.createElement("span");
  text.className = "suggestion-text";
  text.textContent = suggestion.text;
  button.append(product, text);
  button.addEventListener("click", () => ask(suggestion.text));
  $("#suggestions").append(button);
}

checkHealth();
updateComposer();
input.focus();
