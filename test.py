# -*- coding: utf-8 -*-
from lupa import LuaRuntime
lua = LuaRuntime(unpack_returned_tuples=True)
lua.require('lua/modinfo')
lua.eval('print(modinfo.name)')
