# Reuse the already verified LuaJIT and language fixtures.
from pathlib import Path
exec(compile(Path(__file__).with_name("validate_localization.py").read_text(encoding="utf-8-sig"), "validate_localization.py", "exec"))
lua.execute('''
package.loaded["Core/Language"] = Language
rendered = {}
local function capture(...) rendered[#rendered + 1] = select(select("#", ...), ...) end
ImGui = {
 GetWindowDrawList=function() return {} end,
 CalcTextSize=function(text,hide,wrap) return #text * 8, wrap and math.max(16,math.ceil(#text*8/wrap)*16) or 16 end,
 GetFontSize=function() return 16 end,
 GetCursorScreenPos=function() return 0,0 end,
 SetCursorScreenPos=function() end,
 PushTextWrapPos=function() end, PopTextWrapPos=function() end,
 Text=capture, TextColored=capture,
 ColorConvertU32ToFloat4=function() return {1,1,1,1} end,
 ColorConvertFloat4ToU32=function() return 1 end,
 Separator=function() end, Spacing=function() end,
}
GetDisplayResolution=function() return 1920,1080 end
package.loaded["UI/Core/Draw"]={Text=capture,FitText=function(t) return t end,RectFilled=function() end,Rect=function() end,Line=function() end,LeftAccent=function() end}
package.loaded["UI/Core/Context"]={OptionCount=1,DeltaTime=0.016,Bounds={X=20,Y=20,Width=400,Height=600}}
package.loaded["UI/Widgets/Core/Widget"]={
 Begin=function() return {Visible=true,X=0,Y=0,Width=400,Height=36,Hovered=false,Selected=false} end,
 Prepare=function() return false end,GetTextY=function() return 10 end,IsActivated=function() return false end}
package.loaded["UI/Style/Style"]=setmetatable({}, {__index=function() return 1 end})
package.loaded["UI/Style/Layout"]={Rounding=4,FontScale=100}
package.loaded["UI/Core/Icons"]={Get=function() return nil end,Draw=function() return false end,DrawImage=function() return false end}
package.loaded["UI/Style/Icons"]={Back="<",Submenu=">",Dropdown="v",Check="x"}
package.loaded["UI/Widgets/Button/ButtonStyle"]={Padding=8}
package.loaded["UI/Widgets/Toggle/ToggleStyle"]={Padding=8,Size=16,Inset=3,Rounding=2}
package.loaded["UI/Widgets/Break/BreakStyle"]={Padding=8}
package.loaded["Core/Mouse"]={GetPosition=function() return 0,0 end,IsClicked=function() return false end}
package.loaded["UI/Navigation/Navigation"]={State={MouseEnabled=false,Mode={Menu=1,Color=2,Dropdown=3},EnterMode=function() end,LeaveMode=function() end},Input={}}
package.loaded["UI/Widgets/Surface/Surface"]={Create=function() return {} end,Open=function() end,Close=function() end}
package.loaded["UI/Widgets/Surface/SurfaceStyle"]={Padding=8,Rounding=2}
package.loaded["UI/Widgets/Core/Highlight"]={Set=function() end}
package.loaded["UI/Widgets/Dropdown/DropdownStyle"]={}
package.loaded["UI/Widgets/Dropdown/DropdownNavigation"]={Update=function() end}
''')
load=lambda rel:lua.execute((b/rel).read_text(encoding='utf-8-sig'))
anim=load('UI/Widgets/Animation/Animation.lua');lua.globals().package.loaded['UI/Widgets/Animation/Animation']=anim
button=load('UI/Widgets/Button/Button.lua');button.Draw('Quantity','', 'Weapons Vendor','stable-id')
assert '数量' in list(lua.globals().rendered.values());assert '武器商人' in list(lua.globals().rendered.values())
toggle=load('UI/Widgets/Toggle/Toggle.lua');toggle.Draw('Infinite Stamina',lua.table_from({'value':False}),'','stable-toggle')
assert '无限耐力' in list(lua.globals().rendered.values())
brk=load('UI/Widgets/Break/Break.lua');brk.Draw('Owned Items  /  9','left');assert '已拥有物品  /  9' in list(lua.globals().rendered.values())
tip=load('UI/Panels/Tip/Tip.lua');tip.Set('500 available items','original-source');assert tip.SubmittedText=='500 件可用物品' and tip.SubmittedSource=='original-source'
lua.globals().package.loaded['UI/Panels/Tip/Tip']=tip
notification=load('UI/Panels/Notification/Notification.lua');notification.Info('All Maelstrom vehicles unlocked');assert notification.Queue[1].Text=='已解锁全部漩涡帮载具'
lua.globals().package.loaded['UI/Panels/Notification/Notification']=notification
panel=load('UI/Panels/SidePanel/SidePanel.lua');panel.SubmitInfo('test',table({'Eyebrow':'ITEM DATABASE','Title':'Weapons Vendor','Rows':[{'Label':'Category','Value':'Consumables'}]}));panel.Submitted['test'].Draw()
assert '消耗品' in list(lua.globals().rendered.values())
drop=load('UI/Widgets/Dropdown/Dropdown.lua');ref=lua.table_from({'index':1});items=lua.table_from(['Weapons Vendor','Ripperdoc Vendor']);seen=[]
drop.Open('stable','Category',ref,items,lambda i,item:seen.append((i,item)));assert drop.Select(2);assert ref.index==2 and seen==[(2,'Ripperdoc Vendor')]
cp=load('UI/Widgets/ColorPicker/ColorPicker.lua');color=lua.table_from({'Red':10,'Green':20,'Blue':30,'Alpha':255});cp.Open('stable','Color',color);lua.globals().package.loaded['UI/Navigation/Navigation'].Input.RightPressed=True;cp.Update();assert color.Red==15 and color['红色'] is None
print('Widget display translation, raw dropdown values and original RGBA channel keys: pass.')
# Exercise the actual teleport view with stable source records across a language switch.
teleports=json.loads((b/'Config/JSON/Teleports.json').read_text(encoding='utf-8-sig'))['teleports'];tpdata=table(teleports)
lua.globals().tpdata=tpdata
lua.execute('''
quickLabels=nil
package.loaded["UI/Panels/Map/TeleportMap"]={Show=function() end,Focus=function() end,ClearFocus=function() end,SetPoints=function() end,Submit=function() end,Hide=function() end}
package.loaded["Controls/Restrictions"]={ClearStuck=function() return 0 end}
package.loaded["UI/Options/Buttons"]=setmetatable({StringCyclerClick=function(label,ref,items) quickLabels=items; return false end},{__index=function() return function() return false end end})
package.loaded["UI/Navigation/Submenu"]={Create=function(title,draw) return {Title=title,Draw=draw} end}
package.loaded["Features/Teleports/TeleportLocations"]={GetAll=function() return tpdata end,
 GetVendors=function() return {["Weapons Vendor"]={tpdata[1]}} end,
 GetApartments=function() return {{name="Northside",position={x=0,y=0,z=0}}} end,
 GetPriority=function() return {"Weapons Vendor"} end}
package.loaded["Utils/Teleport"]={DistanceFromPlayer=function() return 100 end}
package.loaded["Features/Teleports/AutoTeleport"]={}
package.loaded["Features/Teleports/TeleportViewStates"]=setmetatable({ShowQuick={value=true}},{__index=function() return {value=false} end})
package.loaded["View/Teleports/CustomTeleportView"]={}
''')
view=load('View/Teleports/TeleportView.lua');view.Draw();zhquick=list(lua.globals().quickLabels.values());assert any('武器商人' in s for s in zhquick) and any('北区' in s for s in zhquick)
lang.Load('en');view.Draw();enquick=list(lua.globals().quickLabels.values());assert any('Weapons Vendor' in s for s in enquick) and any('Northside' in s for s in enquick)
lang.Load('zh-cn');view.Draw();assert list(lua.globals().quickLabels.values())==zhquick
print('Teleport menu cache refresh: Chinese / English / Chinese pass, all',len(teleports),'source records preserved.')

# Exercise actual hotkey-tip composition rather than translating the whole joined message.
lua.execute('''
package.loaded["UI/Options/BindButton"]={Format=function(action) return action=="MISC" and "F9" or "Ctrl + H" end,IsCapturing=function() return false end}
package.loaded["UI/Registry/OptionRegistry"]={FindByAction=function() return {} end,IsHotkeyable=function() return true end,GetHotkeyAction=function() return "test" end}
package.loaded["Config/OptionConfig"]={}
package.loaded["Controls/State"]={}
package.loaded["Core/Typing"]={}
package.loaded["UI/Widgets/Break/Break"]={}
package.loaded["UI/Widgets/Toggle/Toggle"]={}
package.loaded["UI/Widgets/Dropdown/Dropdown"]={}
package.loaded["UI/Widgets/ColorPicker/ColorPicker"]={}
package.loaded["UI/Widgets/Button/Button"]={Draw=function(label,tip) capturedHotkeyTip=tip;return false,{Selected=false} end}
''')
buttons=load("UI/Options/Buttons.lua")
source="Removes recoil kick from all guns. Weapon Tuning > Recoil lets you reduce it partially instead."
buttons.Option("No Recoil",source,lua.eval("function() end"))
assert lua.globals().capturedHotkeyTip == lang.Text(source)+" 快捷键：Ctrl + H。按 F9 重新绑定。"
lang.Load("en");buttons.Option("No Recoil",source,lua.eval("function() end"))
assert lua.globals().capturedHotkeyTip == source+" Hotkey: Ctrl + H. Press F9 to rebind."
lang.Load("zh-cn")
print("Real hotkey tooltip composition: Chinese / English pass.")
