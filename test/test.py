# -*- coding: utf-8 -*-
# from lupa import LuaRuntime
# lua = LuaRuntime(unpack_returned_tuples=True)
# lua.require('lua/modinfo')
# lua.eval('print(modinfo.name)')
# import json
# from luamaker import LuaMaker

# f = open("test.json", "r", encoding='utf-8')
# t = json.load(f)
# f.close()

# ttt = LuaMaker.makeLuaTable(t)

# f = open("test.lua", "w", encoding='utf-8')
# f.write("return"+ttt)
# f.close()
from slpp import slpp as lua
from LuaTableParser import LuaTableReader, LuaTableParser

f = open("forest.lua", 'r', encoding='utf-8')
data = f.read()
f.close()
# data = assert(loadstring(data))()
# for i,j in pairs(data['overrides']) do print(i,j) end
data = data.replace("return", "")
# data = '{ array = { 65, 23, 5 }, dict = { string = "value", array = { 3, 6, 4}, mixed = { 43, 54.3, false, string = "value", 9 } } }'
# print(lua.decode(data))
# f = open("test5.lua", 'w', encoding='utf-8')
# f.write(data)
# f.close()
# p = LuaTableReader(data)
# a = p.loadLuaTable("test.lua")
# a = p.load("test5.lua")
# print(p)
p1 = LuaTableParser()
p1.load(data)
d = p1.dumpDict()
print(d)
# p1.loadDict(d)
# la = p1.dump()
# print(la)
# p.loadLuaTable('test.lua')
# data = data.replace("return", "")
# print(data)
# print(lua.decode(data))
