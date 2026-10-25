import pathlib, json, hashlib, re
root = pathlib.Path(__file__).resolve().parents[2]
def unique(pairs):
    result = {}
    for key, value in pairs:
        assert key not in result, ("Duplicate JSON key", key)
        result[key] = value
    return result
for file in root.rglob("*.json"):
    if ".git" not in file.parts: json.loads(file.read_text(encoding="utf-8-sig"),object_pairs_hook=unique)
manifest=json.loads(pathlib.Path(__file__).with_name("upstream-integrity.json").read_text())
for path, expected in manifest["files"].items():
    data=(root/path).read_bytes()
    if not path.endswith(".png"):data=data.replace(b"\r\n",b"\n")
    assert hashlib.sha256(data).hexdigest()==expected, ("Upstream resource changed",path)
for file in root.rglob("*.lua"):
    text=file.read_text(encoding="utf-8-sig")
    assert not re.search(r"^(<<<<<<<|=======|>>>>>>>)",text,re.M),file
    assert "\ufffd" not in text,file
zh=json.loads((root/"lang/zh-cn.json").read_text(encoding="utf-8"))
assert "\ufffd" not in json.dumps(zh,ensure_ascii=False)
settings=root/"Config/JSON/Settings.json"
assert not settings.exists(),"Do not ship personal language/settings files"
print("JSON uniqueness, merge markers, encoding and",len(manifest["files"]),"upstream resources: pass.")
