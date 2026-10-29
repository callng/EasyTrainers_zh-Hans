"""Exercise editor localization through actual Lua modules without game/native plugins."""
from pathlib import Path
import json
import re

exec(compile(Path(__file__).with_name("validate_localization.py").read_text(encoding="utf-8-sig"), "validate_localization.py", "exec"))
lua.globals().package.loaded["Core/Language"] = lang
load = lambda path: lua.execute((b / path).read_text(encoding="utf-8-sig"))

# Every newly introduced editor menu/help literal is either translated, formatted,
# or deliberately technical (axis/unit tokens, action IDs, punctuation).
view_source = (b / "View/WorldEditor/WorldEditorView.lua").read_text(encoding="utf-8-sig")
ignored = {"deg", "%s (%d)", "Placed ", "Copied ", ". Now editing the copy.",
           " can't be copied. Only listed props and vehicles can.", "Removed ",
           " from the scene.", "Attached To ", "Detached ", "Couldn't load ",
           "    ", "  - "}
for line in view_source.splitlines():
    if "require(" in line:
        continue
    for source in re.findall(r'"((?:[^"\\]|\\.)*)"', line):
        if " " in source and source not in ignored:
            assert source in zh["_text"], ("Untranslated editor menu/help literal", source)

cases = {
    "Search Results (12)": "搜索结果（12）",
    "Scene (3)": "场景（3）",
    "Copied Cellphone. Now editing the copy.": "已复制：手机。正在编辑副本。",
    "Copied 3 props.": "已复制 3 个物件。",
    "Pasted 1 prop.": "已粘贴 1 个物件。",
    "Attached 2 props to Cellphone.": "已将 2 个物件 附着到 手机。",
    "Removed Cellphone from the scene.": "已从场景移除：手机。",
    "Hold B and press RT on a parent for Cellphone.": "为“手机”选择父实体：瞄准目标，按住 B 并按 RT。",
    "CARRYING PROP": "搬运中：道具",
    "SELECTED VEHICLE": "已选择：载具",
    "Picking Native": "拾取方式：原生",
    "Camera Off 2.0 deg": "镜头：偏差 2.0 度",
    "V 12.5 m away": "距 V 12.5 米",
    "Hold B and press RT on what it goes on to attach it.": "瞄准父实体，按住 B 并按 RT 以选择附着目标。",
    "LT + Right Stick": "LT + 右摇杆",
    "Close the menu, then press Y to attach.": "关闭菜单后按 Y 完成附着。",
}
for source, expected in cases.items():
    assert lang.Text(source) == expected, (source, lang.Text(source), expected)
assert lang.Format("Saved %s (%d props).%s", "我的场景", 3, lang.Format(" Skipped %d.", 2)) == "已保存“我的场景”（3 个物件）。 已跳过 2 个。"
assert lang.Format("Loading %s (%d props).", "我的场景", 3) == "正在加载“我的场景”（3 个物件）。"
assert lang.Format("%s (%d left).", "Undone", 2) == "已撤销（剩余 2 步）。"
for count in (1, 3):
    assert lang.Format("Detached %d prop." if count == 1 else "Detached %d props.", count) == f"已分离 {count} 个物件。"
assert lang.Text("Scene 1") == "场景 1"
assert lang.Text("This car couldn't be taken out of traffic, so it can't be moved.") == "无法将此载具从交通系统中移出，因此不能移动。"
assert lang.Text("CARRYING ITEM") == "搬运中：物品"
assert lang.GetInputKey(1) == "鼠标左键" and lang.GetInputKey(2) == "鼠标右键"
lang.Load("en")
for source in cases:
    assert lang.Text(source) == source
assert lang.Format("Saved %s (%d props).%s", "My scene", 3, " Skipped 2.") == "Saved My scene (3 props). Skipped 2."
lang.Load("zh-cn")
print("Editor menus, composed notifications, controller hints and English round-trip: pass.")

# Catalog names/paths remain source data. Search can match either language, and
# translated search terms are invalidated when changing the selected language.
catalog_rows = load("Assets/Props/PropCatalog.lua")
lua.globals().package.loaded["Assets/Props/PropCatalog"] = catalog_rows
catalog = load("Features/WorldEditor/PropCatalog.lua")
assert catalog.Count() == len(catalog_rows) == 9782
categories = list(catalog.GetCategories().values())
for category in categories:
    assert category.Name in zh["_text"]
    for group in category.Groups.values():
        assert group.Name in zh["_text"]
        for entry in group.Props.values():
            assert entry.Name in zh["_text"], entry.Name
raw = {row[4]: (row[1], row[2], row[3]) for row in catalog_rows.values()}
for category in categories:
    for group in category.Groups.values():
        for entry in group.Props.values():
            assert (entry.Name, entry.Category, entry.Group) == raw[entry.Path]
for query in ["chair", "椅子", "荒坂", "广告", "螳螂刀"]:
    assert len(catalog.Search(query)) > 0, query
english_paths = [entry.Path for entry in catalog.Search("chair").values()]
lang.Load("en")
assert len(catalog.Search("椅子")) == 0
assert [entry.Path for entry in catalog.Search("chair").values()] == english_paths
lang.Load("zh-cn")
assert len(catalog.Search("椅子")) > 0
print("All 9,782 prop records and source paths preserved; bilingual search and cache invalidation pass.")

# Run clipboard composition against the actual module; both skipped clauses and
# plural counts must survive translation, while the captured scene is untouched.
lua.execute('''
notifications = {}
local function note(text) notifications[#notifications + 1] = Language.Text(text) end
package.loaded["UI/Panels/Notification/Notification"]={Info=note,Warning=note,Error=note}
package.loaded["Core/Input"]={IsController=function() return false end}
package.loaded["Features/WorldEditor/Selection"]={GetAll=function() return {{Entity="one"},{Entity="two"}} end,Clear=function() end}
package.loaded["Features/WorldEditor/PropSpawner"]={Delete=function(entity) return entity=="one" end}
package.loaded["Features/WorldEditor/Layout"]={
 WithChildren=function(items) return items end,
 Capture=function() return {Items={{Name="Cellphone"},{Name="Other"}}},1 end,
 Target=function() return {} end, OffsetTo=function() return {} end,
 Spawn=function() return 2 end,SelectRoot=function() end}
''')
clipboard = load("Features/WorldEditor/Clipboard.lua")
assert clipboard.CopyItems(lua.table_from([]))
assert lua.globals().notifications[1] == "已复制 2 个物件。 已跳过无法复制的 1 个实体。"
clipboard.DeleteSelection()
assert lua.globals().notifications[2] == "已删除 1 个物件。 地图原有实体保持不变。"
clipboard.Paste()
assert lua.globals().notifications[3] == "已粘贴 2 个物件。"
print("Actual clipboard copy/delete/paste and skipped-entity clauses: pass.")

# Find local rendering helpers through Lua debug upvalues, keeping production
# APIs unchanged. Verify translation happens before measurement and truncation.
lua.execute('''
rendered, measured, fitted = {}, {}, {}
local gp = {}
for index,name in ipairs({"DPAD_UP","DPAD_DOWN","DPAD_LEFT","DPAD_RIGHT","START","BACK","LEFT_STICK","RIGHT_STICK","LEFT_BUMPER","RIGHT_BUMPER","LEFT_TRIGGER","RIGHT_TRIGGER","A","B","X","Y"}) do gp[name]=index end
package.loaded["Core/Input"].GP=gp
local function record(text) rendered[#rendered+1]=text end
ImGui={CalcTextSize=function(text) measured[#measured+1]=text; return #text*8 end}
package.loaded["UI/Core/Draw"]={
 Text=function(_,_,_,_,text) record(text) end,
 FitText=function(text) fitted[#fitted+1]=text; return text end,
 RectFilled=function() end,LeftAccent=function() end}
package.loaded["UI/Style/Layout"]={}
package.loaded["UI/Style/Style"]=setmetatable({}, {__index=function() return 1 end})
package.loaded["UI/Widgets/Animation/Animation"]={WithAlpha=function(color) return color end}
package.loaded["Features/World/WorldTime"]={}
package.loaded["Utils/Physics"]={}
for _,name in ipairs({"FreeCam","Inspector","Picker","Selection","Grab","Grabbables","Attachments","Scene","Clipboard"}) do
 package.loaded["Features/WorldEditor/"..name]={}
end
package.loaded["Utils/Entities"]={Safe=function(f) local ok,value=pcall(f); if ok then return value end end}
package.loaded["Controls/Bindings"]={Actions={}}
function FindHelper(root,name,seen)
 seen=seen or {}; if seen[root] then return nil end;seen[root]=true
 for i=1,100 do
  local key,value=debug.getupvalue(root,i);if not key then break end
  if key==name then return value end
  if type(value)=="function" then local found=FindHelper(value,name,seen); if found then return found end end
 end
end
''')
hud = load("Features/WorldEditor/Hud.lua")
find = lua.globals().FindHelper
segment = find(hud.Render, "Segment")
width = find(hud.Render, "TextWidth")
shadow = find(hud.Render, "ShadowText")
tagged = find(hud.Render, "Tagged")
assert segment("WORLD EDITOR", 1, 0, None).Text == "世界编辑器"
width("World Editor")
assert lua.globals().measured[1] == "世界编辑器"
shadow(lua.table_from({}), 0, 0, 1, "CARRYING PROP", 1)
assert lua.globals().rendered[1] == "搬运中：道具"
tagged("SELECTED", 1, "Cellphone")
assert lua.globals().fitted[1] == "手机"
lang.Load("en")
assert segment("WORLD EDITOR", 1, 0, None).Text == "WORLD EDITOR"
tagged("SELECTED", 1, "Cellphone")
assert lua.globals().fitted[2] == "Cellphone"
lang.Load("zh-cn")
print("Actual HUD helpers translate before measuring/truncating; Chinese and English pass.")
