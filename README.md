# 工作台 · 任务启动面板（Python 桌面版）

把原 HTML 版任务面板复刻为 Windows 桌面程序：UI 复用 `web/index.html`，Python 通过 pywebview 提供窗口与本地能力。

## 功能
- 左侧分类导航（含任务计数、新建/重命名/换色/删除分类）
- 右侧任务卡片 / 列表双视图（右上角切换，自动记忆）
- 大类内二级分类分组（抽屉里填二级分类即可）
- 任务：多快捷入口、状态勾选、星标置顶、优先级、全局搜索
- **本地能力（Python 后端）**：
  - 本地文件：`os.startfile` 用系统默认程序打开
  - 本地文件夹：直接调用系统 Explorer 打开
  - 网址：默认浏览器打开
- 配置持久化在程序目录下 `config.json`，左下角"导出/导入"做备份

## 运行
1. 安装依赖（仅首次）：
   ```
   pip install -r requirements.txt
   ```
2. 启动：双击 `启动.bat`，或命令行执行
   ```
   python main.py
   ```

## 目录结构
```
task-panel-py/
  main.py          # 入口：创建窗口、暴露 Python API
  web/index.html   # UI（与网页版一致）
  config.json      # 运行后自动生成的配置
  requirements.txt
```

## 说明
- Windows 上使用系统自带的 Edge WebView2 运行时（Win10/11 一般已预装）。
- 示例路径为占位，点任务卡片右下角铅笔改成你的真实文件/文件夹路径即可。
