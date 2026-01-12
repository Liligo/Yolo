const { app, BrowserWindow, Menu, Tray, nativeImage, shell } = require("electron");
const path = require("path");

let mainWindow;
let tray;

const trayIconDataUrl =
  "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAAbFBMVEUAAAD///////////////////////////////8/Pz9SUlL///8rKyv8/Pz09PRfX18kJCSAgIBfX19AQEBnZ2fPz8/m5ube3t6QkJDw8PC2trZ0dHR/f39HR0c5OTl6enqWlpaV7jH3AAAADnRSTlMA9tgIlKQbfH0T5qf8ev7dUfoAAABeSURBVHgBfY7JCsAgCERb7f9/5yZkSgKC1d0E1KTY8wgp2QfAElRkXv0Z8J7Jx0bBrTWs13VqkG2zYMc0WibPjqI8m3x1n0ZC7GmT9Ni8sYwE8J2p4rG2l7AAAAAElFTkSuQmCC";

const createWindow = () => {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 760,
    minWidth: 960,
    minHeight: 640,
    backgroundColor: "#0c0f14",
    webPreferences: {
      preload: path.join(__dirname, "preload.js")
    }
  });

  mainWindow.loadFile(path.join(__dirname, "index.html"));

  mainWindow.on("close", event => {
    if (!app.isQuiting) {
      event.preventDefault();
      mainWindow.hide();
    }
  });
};

const createTray = () => {
  const trayIcon = nativeImage.createFromDataURL(trayIconDataUrl);
  tray = new Tray(trayIcon);

  const contextMenu = Menu.buildFromTemplate([
    { label: "显示主窗口", click: () => mainWindow.show() },
    { label: "打开日志目录", click: () => shell.openPath(app.getPath("logs")) },
    { type: "separator" },
    {
      label: "退出",
      click: () => {
        app.isQuiting = true;
        app.quit();
      }
    }
  ]);

  tray.setToolTip("YOLO Gesture Control");
  tray.setContextMenu(contextMenu);
  tray.on("double-click", () => mainWindow.show());
};

app.whenReady().then(() => {
  createWindow();
  createTray();

  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    } else {
      mainWindow.show();
    }
  });
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});
