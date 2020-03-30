fuc="getver"
name = "Mushroom House"
description = [[

咕咕咕咕咕
非常感谢好友 逆行人生帮忙测试mod
谢谢羽中画了这么好看的贴图
感谢那些帮我解决代码问题提供思路的各位大佬

如果游戏中使用了不正常的传送之类的导致视角锁定之类的情况出现
可以 输入指令   /c_resethouse 来恢复视野

谢谢你们！
咕咕咕咕咕
]]
author = "羽中,小班花"
version = "2.4"

forumthread = ""

dst_compatible = true
dont_starve_compatible = false
reign_of_giants_compatible = false
all_clients_require_mod=true

api_version = 10 
priority = -1

icon_atlas = "modicon.xml"
icon = "modicon.tex"

server_filter_tags = {"xiaobanhua"}

configuration_options =
{
	{
        name = "HouseLanguage",
        label = "Language/语言",
		hover = "Language/语言",
        options =	{
						{description = "English", data = true},
						{description = "中文", data = false},
					},
		default = true,
    },
   {
        name = "HouseHammered",
        label = "CanbeHammered",
        hover = "Can be Hammered/是否可以被锤",
        options = 
        {
            {description = "Yes(可以)", data = true},
            {description = "No(不可以)", data = false},
        },
        default = true,
    },
   {
        name = "NewWalls",
        label = "Wall Skins",
        hover = "Wall Skins/地板和墙壁皮肤",
        options = 
        {
            {description = "Yes(有)", data = true},
            {description = "No(没有)", data = false},
        },
        default = true,
    },
}