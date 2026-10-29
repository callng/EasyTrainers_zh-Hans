# EasyTrainer 简体中文汉化

基于 [Avi6481 / EasyTrainers](https://github.com/Avi6481/EasyTrainers) 的简体中文汉化分支，当前基线为 **2.3**（上游提交 `3d1fda9be9cd47e0f31d31bbc4c0a4633b861350`）。原作者为 Avi；汉化已获原作者许可。

保留原版功能、英语选项和作者署名，汉化菜单、帮助说明、通知、物品与武器分类、载具菜单、传送地点及新版地图、黑墙能力、武器调校和世界编辑器等界面。采用《赛博朋克 2077》的肉体、反应、技术能力、镇定、专长、街头声望、义体、快速破解、不朽等用语。

## 安装汉化

1. 退出游戏，备份现有的 `EasyTrainer` 文件夹和个人配置。
2. 安装原作者对应版本的完整 EasyTrainer，以及其要求的 Cyber Engine Tweaks（CET）、RED4ext、redscript 等前置。本仓库维护 Lua 汉化与字体修复，不包含原作者的 DLL 或 REDscript；这些组件继续使用原作者发布的版本。**当前 Lua 基于 2.3，请搭配 2.3 的原版组件，不要将旧版 2.2 整包当作 2.3 安装包。**
3. 下载本仓库 ZIP（绿色 `Code` → `Download ZIP`）并解压。将解压目录内的运行文件覆盖到游戏中的以下目录，使 `init.lua` 直接位于 `EasyTrainer` 文件夹内：

   ```text
   <游戏根目录>\bin\x64\plugins\cyber_engine_tweaks\mods\EasyTrainer\
   ```

   升级时保留你已有的 `Config/JSON/Settings.json`、`bindings.json` 及其他个人配置；本仓库不再附带会覆盖语言选择的 `Settings.json`。

   本仓库根目录就是 Mod 目录，不要多套一层 `EasyTrainers_zh-Hans-main`。至少完整复制 `Assets`、`Config`、`Controls`、`Core`、`Features`、`Sessions`、`UI`、`Utils`、`View`、`lang`、`Localization` 和 `init.lua`。通过 Git 克隆时不需要复制 `.git`。
4. 首次安装默认选择简体中文；已有配置保留原来的语言选择。进入 `Settings → Translations → 简体中文` 切换。中文界面可在“设置 → 语言”中切回 English。
5. 武器、义体、载具、专长等数据库名称优先使用游戏自身的本地化。建议将游戏文字语言设为简体中文，以使用官方译名。外部 Mod 未提供中文的名称、内部 ID、作者姓名和自定义输入保留原样。

使用模组管理器时，按原 Mod 的方式部署这些文件；下方字体工具必须从**实际游戏目录中的部署副本**运行。

## 本次同步：世界编辑器

已跟进上游三个提交：`71d95fa`、`5725c50`、`3d1fda9`。同步新版菜单名称，补齐世界编辑器的自由镜头、物件生成、选取与搬运、位置与旋转、父子附着、剪贴板、撤销/重做、场景保存和 HUD 提示。

- 在主菜单进入“世界编辑器”，打开编辑器开关；也可在其“设置 → 操作 → 开关编辑器”中绑定快捷键。上游 `EDITOR_TOGGLE` 初始没有绑定，不能假定它与主菜单按键相同。
- 物件目录的 9,782 条记录提供中文显示，并支持中文或英文搜索。原始名称、分类标识、资源路径与场景数据保持原样；型号、尺寸、变体后缀以及无法确认官方译名的品牌保留原文，便于核对资源。
- 网格物件需要原作者最新版 `EasyTrainerUtility`。请安装与本次世界编辑器更新配套的原版 DLL/REDscript，仅替换 Lua 文件不能升级原生组件。
- 升级时保留自己的 `Config/JSON/bindings.json`、`WorldEditorSaves.json`、`WeaponTuningPresets.json` 及其他个人配置，避免覆盖快捷键、场景存档和预设。

### 主菜单按键说明

本次上游随附的 `Config/JSON/bindings.json` 将主菜单 `TOGGLE` 设为 **Insert**（键码 45），而 Lua 内置后备值仍为 **F4**。实际按键由你的配置决定。若覆盖文件后 F4 没反应，先尝试 Insert，再在“设置 → 按键绑定”中查看或修改“开关菜单”。本汉化保持上游绑定文件原样，不会强制改为 F4。

## 中文字体：方框、问号或缺字

**仓库直接附带完整 Noto Sans SC 字体，下载仓库即可取得，无需另找字体或联网下载。**

- 字体：`Localization/Fonts/NotoSansSC-Regular.otf`
- 字体授权：`Localization/OFL-Noto-CJK.txt`（SIL Open Font License 1.1）
- 固定来源、版本和 SHA-256：[`Localization/FONT-SOURCE.md`](Localization/FONT-SOURCE.md)

启用步骤：

1. 完整安装本仓库的文件，保留 `Localization/Fonts` 子目录。
2. 先启动一次游戏，让 CET 生成 `config.json`，然后退出游戏。
3. 进入以下目录，双击 **`启用完整中文字体.cmd`**：

   ```text
   bin\x64\plugins\cyber_engine_tweaks\mods\EasyTrainer\Localization\
   ```

4. 工具会校验并将随包字体复制到：

   ```text
   bin\x64\plugins\cyber_engine_tweaks\fonts\NotoSansSC-Regular.otf
   ```

   然后备份 CET 配置，并只修改以下两个配置字段：

   ```json
   {
     "font": {
       "path": "NotoSansSC-Regular.otf",
       "language": "ChineseFull"
     }
   }
   ```

   上面的 JSON 仅说明两个字段，**不要用它覆盖完整 `config.json`**。工具保留字号、快捷键、控制台和其他 CET 设置；已正确配置时不会重复改写。若同名字体原先不同，工具也会先备份原字体。
5. 重启游戏后生效。此设置作用于 CET 的共享字体，因此其他 CET 界面也会使用该字体；不会改动游戏本身的字体文件。

### 恢复字体设置

退出游戏。在 `bin\x64\plugins\cyber_engine_tweaks` 中找到工具生成的：

```text
config.json.before-EasyTrainer-zh-*.bak
```

选择需要恢复的备份，复制并命名为同目录的 `config.json`。如果工具替换过已有同名字体，对应备份位于 `fonts` 目录，以 `NotoSansSC-Regular.otf.before-EasyTrainer-zh-` 开头，可按需恢复。

## 汉化与中文适配修复

- 覆盖语言文件，并补齐 Lua 中直接写死的显示文本、动态通知、筛选项目与计量单位。
- 翻译仅作用于显示层；保留数据库 ID、传送坐标、分类标识、回调参数、RGBA 通道和存档数据。
- 保留中英切换与英语回退；切换时刷新传送菜单缓存和物件中文搜索索引。
- 修正打字机动画公共前缀和输入长度截断的 UTF-8 边界，避免拆断中文字符。
- 中文提示和通知按实际换行测量高度，并兼容新版菜单文字缩放。
- 字体和一键启用工具一并版本管理，保留原作者与第三方组件署名及许可证。

## 验证

校验脚本和依赖说明见 [`Localization/Tests/README.md`](Localization/Tests/README.md)，检查记录见 [`Localization/汉化校验记录.txt`](Localization/汉化校验记录.txt)。包含 LuaJIT 语法、语言键与占位符、中英切换、中文 UTF-8 边界、显示组件、世界编辑器动态提示与 HUD、物件双语搜索、原始数据保持和字体覆盖检查；字体配置工具使用独立临时目录测试。

**尚未进行游戏内实测。** 中文输入法、不同分辨率、原生插件版本和其他 Mod 组合仍需在游戏中验证。

## 致谢与授权

- EasyTrainer 原作者：Avi / Avi6481；[上游仓库](https://github.com/Avi6481/EasyTrainers)。原作者的关于页面、署名和链接保留。
- 原有致谢与传送数据来源：Dank Rafft、capncoolio2、LocationKingGRP 等，保持上游内容。
- Noto Sans SC 字体来自 CET 官方仓库，版权归字体原作者所有，按 SIL OFL 1.1 分发，详见随附许可证和字体来源说明。
- `cp2077-cet-kit` 的原有 MIT 许可证保留在 `Core/cp2077-cet-kit/LICENSE.txt`。
- 本汉化基于原作者许可维护；此说明不替原作者代码、DLL 或第三方资源重新指定许可证。
