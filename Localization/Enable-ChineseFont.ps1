$ErrorActionPreference = 'Stop'
function Get-FontSha256 {
    param([string]$Path)
    $algorithm = [System.Security.Cryptography.SHA256]::Create()
    $stream = [System.IO.File]::OpenRead($Path)
    try {
        return ([System.BitConverter]::ToString($algorithm.ComputeHash($stream))).Replace('-', '').ToLowerInvariant()
    } finally {
        $stream.Dispose()
        $algorithm.Dispose()
    }
}
try {
    if (Get-Process -Name 'Cyberpunk2077' -ErrorAction SilentlyContinue) {
        throw '请先退出《赛博朋克 2077》，再运行此工具。'
    }
    $modRoot = Split-Path -Parent $PSScriptRoot
    $cetRoot = Split-Path -Parent (Split-Path -Parent $modRoot)
    $configPath = Join-Path $cetRoot 'config.json'
    $fontDirectory = Join-Path $cetRoot 'fonts'
    $fontPath = Join-Path $fontDirectory 'NotoSansSC-Regular.otf'
    $bundledFont = Join-Path $PSScriptRoot 'Fonts\NotoSansSC-Regular.otf'
    $expectedFontHash = 'a2b93e6c2db05d6bbbf6f27d413ec73269735b7b679019c8a5aa9670ff0ffbf2'
    if (-not (Test-Path -LiteralPath $configPath -PathType Leaf)) {
        throw '未找到 CET 配置。请先将 EasyTrainer 安装到游戏目录，启动一次游戏生成配置，退出游戏后再运行部署到游戏目录中的工具。'
    }
    $configText = [System.IO.File]::ReadAllText($configPath)
    $config = $configText | ConvertFrom-Json -ErrorAction Stop
    if ($null -eq $config -or $config -isnot [System.Management.Automation.PSCustomObject]) {
        throw 'CET 配置格式异常，未作修改。'
    }
    if ($null -eq $config.font) {
        $config | Add-Member -NotePropertyName font -NotePropertyValue ([pscustomobject]@{}) -Force
    }
    if ($config.font -isnot [System.Management.Automation.PSCustomObject]) {
        throw 'CET 字体配置格式异常，未作修改。'
    }
    if (-not (Test-Path -LiteralPath $bundledFont -PathType Leaf)) {
        throw '未找到随汉化附带的字体，请完整复制 Localization 文件夹及其 Fonts 子文件夹。'
    }
    if ((Get-FontSha256 -Path $bundledFont) -ne $expectedFontHash) {
        throw '附带字体的校验值不匹配，请重新下载仓库中的字体文件。'
    }
    if (-not (Test-Path -LiteralPath $fontDirectory -PathType Container)) {
        $null = New-Item -ItemType Directory -Path $fontDirectory
    }
    $fontMatches = (Test-Path -LiteralPath $fontPath -PathType Leaf) -and
        ((Get-FontSha256 -Path $fontPath) -eq $expectedFontHash)
    if (-not $fontMatches) {
        if (Test-Path -LiteralPath $fontPath -PathType Leaf) {
            $fontBackup = $fontPath + '.before-EasyTrainer-zh-' + (Get-Date -Format 'yyyyMMdd-HHmmssfff') + '.bak'
            Copy-Item -LiteralPath $fontPath -Destination $fontBackup -ErrorAction Stop
        }
        Copy-Item -LiteralPath $bundledFont -Destination $fontPath -Force -ErrorAction Stop
        Write-Host '已将仓库附带的完整中文字体安装到 CET fonts 目录。'
    }
    if ($config.font.path -eq 'NotoSansSC-Regular.otf' -and $config.font.language -eq 'ChineseFull') {
        Write-Host '完整简体中文字体已经启用，无需重复修改配置。'
        exit 0
    }
    $backup = $configPath + '.before-EasyTrainer-zh-' + (Get-Date -Format 'yyyyMMdd-HHmmssfff') + '.bak'
    Copy-Item -LiteralPath $configPath -Destination $backup -ErrorAction Stop
    $config.font | Add-Member -NotePropertyName path -NotePropertyValue 'NotoSansSC-Regular.otf' -Force
    $config.font | Add-Member -NotePropertyName language -NotePropertyValue 'ChineseFull' -Force
    $newJson = $config | ConvertTo-Json -Depth 100
    $null = $newJson | ConvertFrom-Json -ErrorAction Stop
    $temporary = $configPath + '.EasyTrainer-zh-' + [guid]::NewGuid().ToString('N') + '.tmp'
    [System.IO.File]::WriteAllText($temporary, $newJson + [Environment]::NewLine, (New-Object System.Text.UTF8Encoding($false)))
    [System.IO.File]::Replace($temporary, $configPath, $backup)
    Write-Host '完整简体中文字体已启用。下次启动游戏生效。'
    Write-Host ('原配置备份：' + $backup)
    Write-Host '只调整 font.path 和 font.language，其余设置保留。'
    exit 0
} catch {
    Write-Host ('未能启用中文字体：' + $_.Exception.Message) -ForegroundColor Red
    exit 1
}
