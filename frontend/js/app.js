const uploadForm = document.querySelector("#uploadForm");
const fileInput = document.querySelector("#fileInput");
const fileName = document.querySelector("#fileName");
const uploadButton = document.querySelector("#uploadButton");
const uploadMessage = document.querySelector("#uploadMessage");
const documentInfo = document.querySelector("#documentInfo");
const healthStatus = document.querySelector("#healthStatus");

const chatForm = document.querySelector("#chatForm");
const questionInput = document.querySelector("#questionInput");
const sendButton = document.querySelector("#sendButton");
const chatMessages = document.querySelector("#chatMessages");

function apiUrl(path) {
  return `${API_CONFIG.BASE_URL}${path}`;
}

function setUploadMessage(text, type = "muted") {
  uploadMessage.textContent = text;
  uploadMessage.className = `message ${type}`;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function scrollToBottom() {
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addMessage(role, text, sources = []) {
  const wrapper = document.createElement("div");
  wrapper.className = role === "user" ? "user-message" : "assistant-message";

  const content = document.createElement("div");
  content.innerHTML = `<div class="bubble">${escapeHtml(text)}</div>`;

  if (role === "assistant" && sources.length > 0) {
    const sourcesEl = document.createElement("div");
    sourcesEl.className = "sources";

    sources.forEach((source, index) => {
      const filename = source.filename || source.metadata?.filename || "未知文件";
      const chunkIndex = source.chunk_index ?? source.metadata?.chunk_index ?? "-";
      const score = source.score !== undefined ? Number(source.score).toFixed(3) : "-";
      const contentText = source.content || source.page_content || "";

      const item = document.createElement("div");
      item.className = "source-item";
      item.innerHTML = `
        <div class="source-title">
          <span>引用 ${index + 1}：${escapeHtml(filename)} / chunk ${escapeHtml(chunkIndex)}</span>
          <span>score ${escapeHtml(score)}</span>
        </div>
        <div>${escapeHtml(contentText)}</div>
      `;
      sourcesEl.appendChild(item);
    });

    content.appendChild(sourcesEl);
  }

  wrapper.appendChild(content);
  chatMessages.appendChild(wrapper);
  scrollToBottom();
}

function renderDocumentInfo(data) {
  documentInfo.classList.remove("empty");
  documentInfo.innerHTML = `
    <div><strong>文件名：</strong>${escapeHtml(data.filename || "-")}</div>
    <div><strong>大小：</strong>${escapeHtml(data.file_size ?? "-")} bytes</div>
    <div><strong>状态：</strong>${escapeHtml(data.status || "-")}</div>
    <div><strong>切分数：</strong>${escapeHtml(data.chunk_count ?? 0)}</div>
    <div><strong>MD5：</strong>${escapeHtml(data.file_hash || "-")}</div>
  `;
}

async function checkHealth() {
  try {
    const response = await fetch(apiUrl(API_CONFIG.HEALTH_PATH));
    if (!response.ok) {
      throw new Error("health check failed");
    }
    healthStatus.classList.remove("offline");
    healthStatus.classList.add("online");
    healthStatus.title = "后端已连接";
  } catch {
    healthStatus.classList.remove("online");
    healthStatus.classList.add("offline");
    healthStatus.title = "后端未连接";
  }
}

fileInput.addEventListener("change", () => {
  const file = fileInput.files[0];
  fileName.textContent = file ? file.name : "选择 txt 文件";
});

uploadForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const file = fileInput.files[0];
  if (!file) {
    setUploadMessage("请先选择 txt 文件。", "error");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  uploadButton.disabled = true;
  setUploadMessage("正在上传并处理资料...", "muted");

  try {
    const response = await fetch(apiUrl(API_CONFIG.UPLOAD_PATH), {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (!response.ok || data.status === "failed") {
      throw new Error(data.detail || data.message || "上传失败");
    }

    renderDocumentInfo(data);

    if (data.duplicate) {
      setUploadMessage(data.message || "该文件已经上传过。", "error");
    } else {
      setUploadMessage(data.message || "上传成功。", "success");
    }
  } catch (error) {
    setUploadMessage(error.message || "上传失败，请检查后端服务。", "error");
  } finally {
    uploadButton.disabled = false;
  }
});

chatForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const question = questionInput.value.trim();
  if (!question) {
    questionInput.focus();
    return;
  }

  addMessage("user", question);
  questionInput.value = "";
  sendButton.disabled = true;

  const loadingId = `loading-${Date.now()}`;
  const loading = document.createElement("div");
  loading.className = "assistant-message";
  loading.id = loadingId;
  loading.innerHTML = `<div class="bubble">正在根据课程资料生成回答...</div>`;
  chatMessages.appendChild(loading);
  scrollToBottom();

  try {
    const response = await fetch(apiUrl(API_CONFIG.CHAT_PATH), {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        question,
        top_k: 5,
      }),
    });

    const data = await response.json();

    if (!response.ok || data.status === "failed") {
      throw new Error(data.detail || data.message || "问答失败");
    }

    document.querySelector(`#${loadingId}`)?.remove();
    addMessage("assistant", data.answer || "没有生成回答。", data.sources || []);
  } catch (error) {
    document.querySelector(`#${loadingId}`)?.remove();
    addMessage("assistant", error.message || "请求失败，请检查后端服务。");
  } finally {
    sendButton.disabled = false;
    questionInput.focus();
  }
});

questionInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    chatForm.requestSubmit();
  }
});

checkHealth();
