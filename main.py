# -*- coding: utf-8 -*-
"""
工作台 · 任务启动面板（Python 桌面版）
基于 pywebview：UI 复用 web/index.html，Python 负责配置持久化与本地文件/文件夹调用。
"""
import os
import sys
import json
import subprocess
import webbrowser

import webview

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, "web")
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")


class Api:
    """暴露给前端 JS 的接口，通过 window.pywebview.api 调用。"""

    def load_config(self):
        """读取本地配置；不存在时返回 None，前端用内置默认数据。"""
        try:
            if os.path.exists(CONFIG_PATH):
                with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception as e:
            print("[load_config] 读取失败:", e, file=sys.stderr)
        return None

    def save_config(self, db):
        """把整个任务面板数据写入 config.json。"""
        try:
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(db, f, ensure_ascii=False, indent=2)
            return {"ok": True, "path": CONFIG_PATH}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def open_path(self, path):
        """用系统默认程序打开本地文件；若是目录则用资源管理器打开。"""
        try:
            if not path:
                return {"ok": False, "error": "路径为空"}
            path = str(path).strip().replace("/", os.sep)
            if sys.platform == "win32":
                # exe 程序：临时切到其所在目录再用 ShellExecute 启动（等同双击，必弹独立窗口），
                # 启动后立即切回原目录，避免内部相对路径配置文件找不到
                if os.path.isfile(path) and path.lower().endswith(".exe"):
                    old_cwd = os.getcwd()
                    try:
                        os.chdir(os.path.dirname(path))
                        os.startfile(path)  # noqa: 需要 Windows
                    finally:
                        os.chdir(old_cwd)
                else:
                    os.startfile(path)  # noqa: 需要 Windows
            elif sys.platform == "darwin":
                subprocess.Popen(["open", path])
            else:
                subprocess.Popen(["xdg-open", path])
            return {"ok": True}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def open_url(self, url):
        """用默认浏览器打开网址。"""
        try:
            webbrowser.open(url)
            return {"ok": True}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def reveal_path(self, path):
        """在资源管理器中选中某个文件（Windows）。"""
        try:
            if sys.platform == "win32" and os.path.exists(path):
                subprocess.Popen(["explorer", "/select,", path])
                return {"ok": True}
            return self.open_path(path)
        except Exception as e:
            return {"ok": False, "error": str(e)}


def main():
    api = Api()
    webview.create_window(
        title="工作台 · 任务启动面板",
        url=os.path.join(WEB_DIR, "index.html"),
        js_api=api,
        width=1440,
        height=900,
        min_size=(1100, 720),
        resizable=True,
        background_color="#f4f6f9",
    )
    # Windows 上默认使用 Edge WebView2（系统自带运行时）
    webview.start(debug=False)


if __name__ == "__main__":
    main()
