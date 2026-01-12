# Yolo

## 使用说明

1. 安装 Python 3.10+。
2. 创建虚拟环境并安装依赖：

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows 使用 .venv\\Scripts\\activate
   pip install -r requirements.txt
   ```

3. 运行入口脚本（默认入口在 `src/main.py`，请替换为你的实际逻辑）：

   ```bash
   python src/main.py
   ```

## 使用 PyInstaller 打包

1. 确保已安装依赖（`requirements.txt` 含 MediaPipe/OpenCV/PyInstaller）。
2. 使用打包脚本生成可执行文件：

   ```bash
   python packaging/build.py --onefile --name YoloApp
   ```

3. 在 `dist/YoloApp/` 下获取输出文件：
   - Windows：`YoloApp.exe`
   - macOS：可执行文件或 `.app`（如需 `.app`，可改用 `--windowed` 并使用 `pyinstaller --windowed` 配合适配）

## 隐私声明

- 应用仅在本地运行，默认不收集、存储或上传任何个人数据。
- 摄像头/媒体输入只用于本地处理（如手势识别或图像分析）。
- 若你在应用中自行实现联网、日志或远程服务，请在界面或文档中明确告知用户。
