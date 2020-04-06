--The name of the mod displayed in the 'mods' screen.
name = "Status Announcements"

--A description of the mod.
description =
    'Alt-click parts of the HUD to announce their status ("I\'m wounded!", "I have 2 twigs.", "We need more drying racks."). ALT+SHIFT click to announce items.'

--Who wrote this awesome mod?
author = "rezecib"

--A version number so you can ask people if they are running an old version of your mod.
version = "2.6.7"

--This lets other players know if your mod is out of date. This typically needs to be updated every time there's a new game update.
api_version = 10

dst_compatible = true

--This lets clients know if they need to get the mod from the Steam Workshop to join the game
all_clients_require_mod = false

--This determines whether it causes a server to be marked as modded (and shows in the mod list)
client_only_mod = true

--This lets people search for servers with this mod by these tags
server_filter_tags = {}

icon_atlas = "statusannouncements.xml"
icon = "statusannouncements.tex"

forumthread = "/files/file/923-dst-status-announcements"

--[[
Credits:
    Silentdarkness1 for coming up with most of the character-specific quotes
	Acemurdock and OSMRhodey for helping out with the Woodie quotes
	SuperPsiPower (and friends) for helping out with the Webber quotes
	Vinicius Araújo for translating the quotes to Brazilian Portuguese
	GoforDream and Shang for translating to Chinese
	Gum for translating to Spanish
	deshkas and Shire for a partial Russian translation
	Redhead for translating to German
]]
configuration_options = {
    {
        name = "LANGUAGE",
        label = "Which language to use",
        options = {
            {description = "Detect", data = "detect", hover = "Detect the language based on language mods installed."},
            {description = "English", data = "english"},
            {description = "Deutsch", data = "german"},
            {description = "Português (BR)", data = "brazil"},
            {description = "Chinese", data = "chinese"},
            {description = "русский", data = "russian"},
            {description = "Español", data = "spanish"},
        },
        default = "detect"
    },
    {
        name = "WHISPER",
        label = "Whisper by default",
        options = {
            {description = "Yes", data = true},
            {description = "No", data = false}
        },
        default = false
    },
    {
        name = "EXPLICIT",
        label = "Show current/max",
        options = {
            {description = "Yes", data = true},
            {description = "No", data = false}
        },
        default = true,
        hover = "When announcing stats, show the numbers for your current and max stat."
    },
    {
        name = "SHOWPROTOTYPER",
        label = "Announce Prototyper",
        options = {
            {description = "Yes", data = true},
            {description = "No", data = false}
        },
        default = true,
        hover = "When announcing a crafting recipe, whether to announce that you need a science machine or another prototyper."
    },
    {
        name = "SHOWEMOJI",
        label = "Announce Emoji",
        options = {
            {description = "Yes", data = true},
            {description = "No", data = false}
        },
        default = true,
        hover = 'When announcing stats, show an emoji for the stat (if using "Show current/max").'
    },
    {
        name = "SHOWDURABILITY",
        label = "Announce Durability",
        options = {
            {description = "Yes", data = true},
            {description = "No", data = false}
        },
        default = true,
        hover = "Whether to announce the durability/freshness of an item when announcing that you have it."
    },
    {
        name = "OVERRIDEB",
        label = "Controller Cancel",
        options = {
            {description = "Yes", data = true},
            {description = "No", data = false}
        },
        default = true,
        hover = "When controller inventory is open, allow the B/cancel button\nto be used to announce temperature\n(if you are using Combined Status)."
    },
    {
        name = "OVERRIDESELECT",
        label = "Controller Map",
        options = {
            {description = "Yes", data = true},
            {description = "No", data = false}
        },
        default = true,
        hover = "When controller inventory is open, allow the SELECT/map button\nto be used to announce the season\n(if you are using Combined Status)."
    },
    {
        name = "WILSON",
        label = "Custom Wilson Quotes",
        options = {
            {description = "Yes", data = true},
            {description = "No", data = false}
        },
        default = true
    },
    {
        name = "WILLOW",
        label = "Custom Willow Quotes",
        options = {
            {description = "Yes", data = true},
            {description = "No", data = false}
        },
        default = true
    },
    {
        name = "WX78",
        label = "Custom WX-78 Quotes",
        options = {
            {description = "Yes", data = true},
            {description = "No", data = false}
        },
        default = true
    },
    {
        name = "WICKERBOTTOM",
        label = "Custom Wickerbottom Quotes",
        options = {
            {description = "Yes", data = true},
            {description = "No", data = false}
        },
        default = true
    },
    {
        name = "WOLFGANG",
        label = "Custom Wolfgang Quotes",
        options = {
            {description = "Yes", data = true},
            {description = "No", data = false}
        },
        default = true
    },
    {
        name = "WENDY",
        label = "Custom Wendy Quotes",
        options = {
            {description = "Yes", data = true},
            {description = "No", data = false}
        },
        default = true
    },
    {
        name = "WOODIE",
        label = "Custom Woodie Quotes",
        options = {
            {description = "Yes", data = true},
            {description = "No", data = false}
        },
        default = true
    },
    {
        name = "WES",
        label = "Custom Wes Quotes",
        options = {
            {description = "Yes", data = true},
            {description = "No", data = false}
        },
        default = true
    },
    {
        name = "WAXWELL",
        label = "Custom Maxwell Quotes",
        options = {
            {description = "Yes", data = true},
            {description = "No", data = false}
        },
        default = true
    },
    {
        name = "WEBBER",
        label = "Custom Webber Quotes",
        options = {
            {description = "Yes", data = true},
            {description = "No", data = false}
        },
        default = true
    },
    {
        name = "WATHGRITHR",
        label = "Custom Wigfrid Quotes",
        options = {
            {description = "Yes", data = true},
            {description = "No", data = false}
        },
        default = true
    },
    {
        name = "WINONA",
        label = "Custom Winona Quotes",
        options = {
            {description = "Yes", data = true},
            {description = "No", data = false}
        },
        default = true
    },
    {
        name = "WORMWOOD",
        label = "Custom Wormwood Quotes",
        options = {
            {description = "Yes", data = true},
            {description = "No", data = false}
        },
        default = true
    },
    {
        name = "WURT",
        label = "Custom Wurt Quotes",
        options = {
            {description = "Yes", data = true},
            {description = "No", data = false}
        },
        default = true
    },
    {
        name = "WORTOX",
        label = "Custom Wortox Quotes",
        options = {
            {description = "Yes", data = true},
            {description = "No", data = false}
        },
        default = true
    },
    {
        name = "WARLY",
        label = "Custom Warly Quotes",
        options = {
            {description = "Yes", data = true},
            {description = "No", data = false}
        },
        default = true
    },
    {
        name = "WALANI",
        label = "Custom Walani Quotes",
        options = {
            {description = "Yes", data = true},
            {description = "No", data = false}
        },
        default = true
    },
    {
        name = "WOODLEGS",
        label = "Custom Woodlegs Quotes",
        options = {
            {description = "Yes", data = true},
            {description = "No", data = false}
        },
        default = true
    },
    {
        name = "WILBUR",
        label = "Custom Wilbur Quotes",
        options = {
            {description = "Yes", data = true},
            {description = "No", data = false}
        },
        default = true
    }
}
