const navLinks = document.querySelectorAll(".nav-link");
const panels = document.querySelectorAll(".panel");
const sensitivity = document.getElementById("sensitivity");
const sensitivityValue = document.getElementById("sensitivity-value");
const logList = document.getElementById("gesture-log");
const logCount = document.getElementById("log-count");
const resetLog = document.getElementById("reset-log");
const gestureToggle = document.getElementById("gesture-toggle");
const recognitionStatus = document.getElementById("recognition-status");
const currentGesture = document.getElementById("current-gesture");

const gestures = ["左滑", "右滑", "握拳", "张开手", "OK 手势"];

const updateLogCount = () => {
  logCount.textContent = `${logList.children.length} 条`;
};

navLinks.forEach(link => {
  link.addEventListener("click", () => {
    navLinks.forEach(item => item.classList.remove("is-active"));
    panels.forEach(panel => panel.classList.remove("is-visible"));

    link.classList.add("is-active");
    const target = document.getElementById(link.dataset.target);
    target.classList.add("is-visible");
  });
});

sensitivity.addEventListener("input", event => {
  sensitivityValue.textContent = event.target.value;
});

resetLog.addEventListener("click", () => {
  logList.innerHTML = "";
  updateLogCount();
});

gestureToggle.addEventListener("change", event => {
  recognitionStatus.textContent = event.target.checked ? "运行中" : "已暂停";
  recognitionStatus.style.color = event.target.checked ? "#e8ecf2" : "#f59e0b";
});

setInterval(() => {
  const newGesture = gestures[Math.floor(Math.random() * gestures.length)];
  currentGesture.textContent = newGesture;
  const time = new Date().toLocaleTimeString("zh-CN", { hour12: false });
  const item = document.createElement("li");
  item.textContent = `${time} ${newGesture} → 已触发操作`;
  logList.prepend(item);

  while (logList.children.length > 8) {
    logList.removeChild(logList.lastChild);
  }
  updateLogCount();
}, 6000);

updateLogCount();

const versionElement = document.getElementById("electron-version");
if (window.appInfo) {
  versionElement.textContent = window.appInfo.version;
}
