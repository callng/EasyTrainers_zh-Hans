import pathlib,sys,json,re

from lupa.luajit21 import LuaRuntime
b=pathlib.Path(__file__).resolve().parents[2];lua=LuaRuntime(unpack_returned_tuples=True)
compile=lua.eval('function(s,n) local f,e=loadstring(s,n); return f~=nil,e end');errors=[]
for p in b.rglob('*.lua'):
 ok,e=compile(p.read_text(encoding='utf-8-sig'),'@'+str(p.relative_to(b)))
 if not ok:errors.append((str(p.relative_to(b)),e))
assert not errors,errors
print('LuaJIT 2.1: all',len(list(b.rglob('*.lua'))),'Lua files compile.')
def table(o):
 if isinstance(o,dict):return lua.table_from({k:table(v) for k,v in o.items()})
 if isinstance(o,list):return lua.table_from([table(v) for v in o])
 return o
en=json.loads((b/'lang/en.json').read_text(encoding='utf-8-sig'));zh=json.loads((b/'lang/zh-cn.json').read_text(encoding='utf-8'))
lua.globals().docs=table({'lang/en.json':en,'lang/zh-cn.json':zh})
lua.execute('package.loaded["Core/Logger"]={Log=function() end}; package.loaded["Core/JsonHelper"]={Read=function(p) return docs[p] end}; dir=function() return {"en.json","zh-cn.json"} end')
lang=lua.execute((b/'Core/Language.lua').read_text());lua.globals().Language=lang
assert lang.Load('zh-cn')
for k,v in zh['_text'].items():assert lang.Text(k)==v,(k,v,lang.Text(k))
print('Exact display mappings:',len(zh['_text']),'pass')

assert lang.Text('No cyberware in Legs slot.\nEquip Reinforced Tendons first.') == '腿部未安装义体。\n请先装备强化肌腱。'
assert lang.Text('Infinite Jumps enabled.\nLoad a save to apply.') == '无限跳跃已启用。\n重新读取存档后生效。'

cases={
'Bound Infinite Health to Ctrl + H':'已将“无限生命值”绑定为 Ctrl + H',
'Binding in: 3':'开始绑定倒计时：3',
'Press any key to bind (8)':'请按下要绑定的按键（8）',
'Get ready to bind Infinite Stamina in 3 seconds':'准备绑定“无限耐力”，3 秒后开始',
'Saved MyPreset':'已保存：MyPreset',
'Added All Crafting Components':'已添加：全部制作组件',
'Weapons Vendor  [42]':'武器商人  [42]',
'All Maelstrom vehicles unlocked':'已解锁全部漩涡帮载具',
'500 available items':'500 件可用物品',
'Removed 3 spawned vehicles':'已移除 3 辆生成的载具',
'Skipped 2 day(s)':'已跳过 2 天',
'Switch to the 24h_weather_rain weather state.':'切换天气：雨天。',
'8 Results':'8 个结果',
'Owned Items  /  9':'已拥有物品  /  9'}
for k,v in cases.items():
 out=lang.Text(k);print(k,'=>',out)
 assert out==v,(k,out,v)
assert lang.Format('Removed %d spawned vehicles',7)=='已移除 7 辆生成的载具'
print('Format example:',lang.Format('%s %dx %s','Added',2,'测试物品'))
assert not lang.Load('../oops');assert lang.GetCurrentCode()=='zh-cn'
assert lang.Load('en')
for k in cases:assert lang.Text(k)==k,(k,lang.Text(k))
assert lang.Format('Removed %d spawned vehicles',7)=='Removed 7 spawned vehicles'
assert lang.Load('zh-cn');assert lang.GetCurrentName()=='简体中文'
print('Chinese -> English -> Chinese switching and invalid-code handling pass.')
# Typewriter tests run on actual LuaJIT byte strings; check every emitted prefix.
a=lua.execute((b/'UI/Widgets/Animation/Animation.lua').read_text())
for before,after in [('中文一','中文二'),('你','好'),('中','串'),('abc中文','abc中英'),('🙂甲','🙂乙'),('','你好'),('完成','完')]:
 writer=a.CreateTypewriter();a.SetText(writer,before);a.UpdateTypewriter(writer,100,52);a.SetText(writer,after)
 assert after.startswith(writer.Displayed),(before,after,writer.Displayed)
 for _ in range(20):
  a.UpdateTypewriter(writer,.02,52);assert after.startswith(writer.Displayed)
 assert writer.Displayed==after
print('UTF8 typewriter switching: all prefixes valid.')
lua.execute('package.loaded["Core/Input"]={ConsumeTypedText=function() return nativeText end, IsKeyDown=function() return false end, EndTextCapture=function() end, BeginTextCapture=function() end}')
typing=lua.execute((b/'Core/Typing.lua').read_text())
for t in ['中'*100,'a'*255+'中','🙂'*70,'a'*254+'🙂','a'*256+'乙']:
 lua.globals().nativeText=t;out,_,_=typing.Update('');assert len(out.encode('utf-8'))<=256 and t.startswith(out)
print('UTF8 text entry byte limit: pass.')
# Require resolution supports both module.lua and module/init.lua.
missing={}
for p in b.rglob('*.lua'):
 for m in re.finditer(r'require\s*\(?["\']([^"\']+)["\']',p.read_text(encoding='utf-8-sig')):
  mod=m[1]
  if not (b/(mod+'.lua')).exists() and not (b/mod/'init.lua').exists():missing.setdefault(mod,[]).append(str(p.relative_to(b)))
assert not missing,missing
print('All local module requires resolve.')

# Every current upstream key and placeholder is represented in Simplified Chinese.
def flatten(obj, prefix=""):
    result = {}
    for key, value in obj.items():
        path = prefix + key
        if isinstance(value, dict): result.update(flatten(value, path + "."))
        elif isinstance(value, str): result[path] = value
    return result
english, chinese = flatten(en), flatten(zh)
placeholder = re.compile(r"\{[A-Za-z0-9_]+\}|%(?:[-+#0]*\d*(?:\.\d+)?)[cdiouxXeEfgGqs]")
for key, value in english.items():
    assert key in chinese, ("Missing key", key)
    if key.startswith("_meta."): continue
    assert sorted(placeholder.findall(value)) == sorted(placeholder.findall(chinese[key])), key
    assert chinese[key] or not value, ("Empty translation", key)
for value, translated in zh["_text"].items():
    assert sorted(placeholder.findall(value)) == sorted(placeholder.findall(translated)), (value, translated)
for item in zh["_patterns"]:
    assert sorted(re.findall(r"\{\d+\}", item["source"])) == sorted(re.findall(r"\{\d+\}", item["target"])), item
new_cases = {
    "Cleared keyboard binding for Infinite Health": "已清除“无限生命值”的键盘绑定",
    "Press a key to bind, Del to clear (8)": "按任意键绑定，按 Delete 清除（8）",
    "Added 5000 eddies": "已添加 5000 欧元",
    "Removed 7 weapons": "已移除 7 件武器",
    "Last 8 Items": "最近 8 件物品",
    "Everything in Consumables": "消耗品中的全部物品",
    "12 items in one list.": "在同一列表中显示 12 件物品。",
    "Slot 2": "武器槽 2",
    "25 /s": "25 次/秒",
    "15 pellets": "15 颗弹丸",
}
for source, expected in new_cases.items(): assert lang.Text(source) == expected, (source, lang.Text(source))
assert lang.Format("Hotkey: %s. Press %s to rebind.", "Ctrl + H", "F9") == "快捷键：Ctrl + H。按 F9 重新绑定。"
assert lang.Format("%.1f km across", 2.5) == "横向范围 2.5 千米"
assert lang.Get("weaponsmenu.noreload.label") == "无限弹匣"
assert lang.Tip("playerdev.quick.unlockperks.done", table({"count": 42})) == "已获得 42 级专长"
lang.Load("en")
for source in new_cases: assert lang.Text(source) == source
lang.Load("zh-cn")
print("Current upstream language keys:", len(english), "all present with matching placeholders.")
print("Version 2.3 dynamic notifications, map scale and English round-trip: pass.")
