const { contextBridge } = require("electron");

contextBridge.exposeInMainWorld("appInfo", {
  version: process.versions.electron
});
