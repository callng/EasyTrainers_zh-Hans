local Buttons = require("UI/Options/Buttons")
local Submenu = require("UI/Navigation/Submenu")
local Notification = require("UI/Panels/Notification/Notification")
local JsonHelper = require("Core/JsonHelper")
local Language = require("Core/Language")

local SETTINGS_PATH = "Config/JSON/Settings.json"
local LANGUAGE_FOLDER = "lang"

local s_Settings = nil
local s_Languages = nil
local s_Names = {}
local s_Selected = { index = 1 }

local function LoadLanguages()
    s_Languages = Language.GetAvailable(LANGUAGE_FOLDER)
    s_Settings = JsonHelper.LoadOrCreate(SETTINGS_PATH, { shown = false, Lang = "zh-cn" }) or { Lang = "zh-cn" }
    s_Names = {}

    local current = s_Settings.Lang or Language.GetCurrentCode()
    s_Selected.index = 1
    for index, language in ipairs(s_Languages) do
        table.insert(s_Names, language.name)
        if language.code == current then s_Selected.index = index end
    end
end

local function SetLanguage(index)
    local language = s_Languages[index]
    if not language or not Language.Load(language.code) then
        Notification.Error(L("languagemenu.loadfailed"))
        return
    end

    s_Settings.Lang = language.code
    if not JsonHelper.Write(SETTINGS_PATH, s_Settings) then
        Notification.Warning(L("languagemenu.savefailed"))
        return
    end

    local message = Language.Get("loadmessage")
    if message ~= "" and message ~= "loadmessage" then Notification.Success(message) end
end

local function TranslationsView()
    if not s_Languages then LoadLanguages() end

    Buttons.Option(L("languagemenu.reload.label"), L("languagemenu.reload.tip"), LoadLanguages)
    Buttons.OptionExtended(L("languagemenu.current"), "", Language.GetCurrentName(), L("languagemenu.tip"))
    if #s_Languages <= 1 then
        Buttons.OptionExtended(L("languagemenu.onlyone"), "", "", L("languagemenu.tip"))
    end

    Buttons.Break(L("languagemenu.title"))
    Buttons.Radio("", s_Selected, s_Names, L("languagemenu.tip"), SetLanguage)
end

return Submenu.Create("languagemenu.title", TranslationsView)
