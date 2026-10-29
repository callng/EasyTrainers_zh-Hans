# 汉化验证

建议使用 Python 3.12，在仓库根目录运行：

```powershell
python -m pip install -r Localization/Tests/requirements.txt
python -X utf8 Localization/Tests/validate_ui.py
python -X utf8 Localization/Tests/validate_world_editor.py
python -X utf8 Localization/Tests/validate_font.py
python -X utf8 Localization/Tests/validate_repository.py
```

`validate_ui.py` 会先执行 `validate_localization.py`：使用 LuaJIT 2.1 编译所有 Lua 文件，并模拟语言切换、动态通知、UTF-8 文本处理和界面组件，检查当前上游语言键、占位符和模块路径。

`validate_world_editor.py` 使用实际世界编辑器 Lua 模块测试动态通知、键鼠与手柄提示、中英切换、HUD 翻译后的测量与截断、9,782 条物件原始记录，以及中文/英文搜索和切换语言后的索引刷新。测试模拟游戏 API，不调用原生插件。

`validate_font.py` 不需要第三方 Python 包。它检查随仓库字体的 SHA-256 与全部译文字形，并在系统临时目录内启动 Windows PowerShell，测试字体安装、配置备份、其他字段保留、重复执行和错误输入处理，不访问实际游戏目录。

这些检查不代替游戏内实测。

`validate_repository.py` 检查 JSON 重复键、残留合并标记、文本编码，以及英文语言、原始传送数据、物件目录、初始配置和图片等上游资源的完整性；文本文件允许正常的 LF/CRLF 转换。
