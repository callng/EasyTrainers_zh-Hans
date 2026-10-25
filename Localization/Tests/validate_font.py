import pathlib,json,struct,shutil
b=pathlib.Path(__file__).resolve().parents[2];zh=json.loads((b/'lang/zh-cn.json').read_text(encoding='utf-8'))
f=(b/'Localization/Fonts/NotoSansSC-Regular.otf').read_bytes()
u16=lambda p:struct.unpack_from('>H',f,p)[0];u32=lambda p:struct.unpack_from('>I',f,p)[0]
tables={}
for i in range(u16(4)):
 p=12+16*i;tables[f[p:p+4].decode()]=(u32(p+8),u32(p+12))
cmap=tables['cmap'][0];sub=[]
for i in range(u16(cmap+2)):
 p=cmap+4+8*i;platform,encoding=u16(p),u16(p+2);off=cmap+u32(p+4)
 if platform in [0,3] and u16(off) in [4,12]:sub.append(off)
def has(cp):
 for base in sub:
  fmt=u16(base)
  if fmt==12:
   for i in range(u32(base+12)):
    p=base+16+12*i;start,end,glyph=u32(p),u32(p+4),u32(p+8)
    if start<=cp<=end and glyph+cp-start:return True
  elif cp<=0xffff:
   n=u16(base+6)//2;ends=base+14;starts=ends+2*n+2;deltas=starts+2*n;ranges=deltas+2*n
   for i in range(n):
    if u16(starts+2*i)<=cp<=u16(ends+2*i):
     delta=u16(deltas+2*i);ran=u16(ranges+2*i)
     glyph=(cp+delta)&0xffff if ran==0 else u16(ranges+2*i+ran+2*(cp-u16(starts+2*i)))
     if glyph:return True
     break
 return False
def texts(o):
 if isinstance(o,dict):
  for v in o.values():yield from texts(v)
 elif isinstance(o,list):
  for v in o:yield from texts(v)
 elif isinstance(o,str):yield o
chars=set(''.join(texts(zh)));missing=[c for c in chars if ord(c)>=128 and not has(ord(c))]
print('Chinese localization unique glyphs',len(chars),'missing from bundled font',missing);assert not missing

import tempfile, subprocess, hashlib, copy
expected_hash = "a2b93e6c2db05d6bbbf6f27d413ec73269735b7b679019c8a5aa9670ff0ffbf2"
assert hashlib.sha256(f).hexdigest() == expected_hash
with tempfile.TemporaryDirectory(prefix="EasyTrainer-font-test-") as scratch:
    root = pathlib.Path(scratch)
    loc = root / "mods" / "EasyTrainer" / "Localization"
    loc.mkdir(parents=True)
    (loc / "Fonts").mkdir()
    shutil.copy2(b / "Localization" / "Enable-ChineseFont.ps1", loc / "Enable-ChineseFont.ps1")
    shutil.copy2(b / "Localization" / "Fonts" / "NotoSansSC-Regular.otf", loc / "Fonts" / "NotoSansSC-Regular.otf")
    config_path = root / "config.json"
    original = {"font":{"path":"custom.ttf","language":"Default","size":18.5,"oversample_h":3},
                "bindings":{"key":123,"ui":[12,45]},"patches":{"enabled":True},"other":["中文",None,42]}
    def invoke():
        return subprocess.run(["powershell.exe","-NoLogo","-NoProfile","-ExecutionPolicy","Bypass","-File",str(loc/"Enable-ChineseFont.ps1")],capture_output=True)
    def write(value):
        config_path.write_text(json.dumps(value,ensure_ascii=False),encoding="utf-8")
    def backups(): return sorted(root.glob("config.json.before-EasyTrainer-zh-*.bak"))
    write(original)
    before = config_path.read_bytes()
    result = invoke(); assert result.returncode == 0, result.stdout
    expected = copy.deepcopy(original);expected["font"].update(path="NotoSansSC-Regular.otf",language="ChineseFull")
    assert json.loads(config_path.read_text(encoding="utf-8-sig")) == expected
    assert len(backups()) == 1 and backups()[0].read_bytes() == before
    installed = root/"fonts"/"NotoSansSC-Regular.otf"
    assert hashlib.sha256(installed.read_bytes()).hexdigest() == expected_hash
    unchanged = config_path.read_bytes()
    assert invoke().returncode == 0
    assert config_path.read_bytes() == unchanged and len(backups()) == 1
    # A missing/different installed font is repaired even if config already matches.
    installed.write_bytes(b"previous-font")
    assert invoke().returncode == 0
    assert config_path.read_bytes() == unchanged and len(backups()) == 1
    saved_fonts=list((root/"fonts").glob("*.bak")); assert len(saved_fonts)==1 and saved_fonts[0].read_bytes()==b"previous-font"
    assert hashlib.sha256(installed.read_bytes()).hexdigest() == expected_hash
    # Preserve unrelated settings when the font object is absent.
    write({"bindings":{"open":123},"other":"retained"})
    assert invoke().returncode == 0
    assert json.loads(config_path.read_text(encoding="utf-8-sig")) == {"bindings":{"open":123},"other":"retained","font":{"path":"NotoSansSC-Regular.otf","language":"ChineseFull"}}
    # Invalid config/font nodes and invalid source fonts must fail without rewriting config.
    for bad in ["broken JSON", "[]", json.dumps({"font":"invalid","bindings":{"open":123}})]:
        config_path.write_text(bad,encoding="utf-8"); count=len(backups())
        assert invoke().returncode != 0
        assert config_path.read_text(encoding="utf-8") == bad and len(backups()) == count
    write(original); before=config_path.read_bytes(); count=len(backups())
    (loc/"Fonts"/"NotoSansSC-Regular.otf").write_bytes(b"corrupt-font")
    assert invoke().returncode != 0
    assert config_path.read_bytes()==before and len(backups())==count
    config_path.unlink()
    assert invoke().returncode != 0 and not config_path.exists()
print("Bundled font hash and glyph coverage: pass.")
print("Windows PowerShell helper: install, backup, setting preservation, idempotence, repair and failure checks pass.")
